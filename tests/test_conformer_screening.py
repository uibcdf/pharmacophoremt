"""Prepared ensemble controls using public molecular provider operations."""

import json
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pandas as pd
import pytest

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
from pharmacophoremt.modeler import from_ligand
from pharmacophoremt.screening import ConformerScreening
from pharmacophoremt.validation.retrospective import RetrospectiveValidator
from tests.test_pose_evaluation import system
from tests.test_rigid_search import COORDINATES, SMILES, moved, reference


def ensemble(*coordinates):
    source = system(SMILES, coordinates[0])
    for frame in coordinates[1:]:
        source.structures.append(coordinates=puw.quantity([frame], "nm"))
    return source


def moved_coordinates():
    source, _ = reference()
    return puw.get_value(msm.get(moved(source), coordinates=True), to_unit="nm")[0]


def distorted_coordinates():
    coordinates = COORDINATES.copy()
    coordinates[-1] += [0, 0, 2]
    return coordinates


def unpack(record):
    return puw.get_value(
        puw.QuantityRecord.from_dict(record).to_quantity(
            unit="nm", dimensionality={"[L]": 1}
        ),
        to_unit="nm",
    )


def add_declared_state(source, charges):
    # Declare a complete state through the provider's public typed codec.
    payload = msm.convert(source, to_form="molsysmt.ChemicalStatesDict")
    payload.data["states"].append(deepcopy(payload.data["states"][0]))
    source.chemical_states = msm.convert(payload, to_form="molsysmt.ChemicalStates")
    msm.set(source, element="atom", chemical_state=1, formal_charge=charges)


def test_recovers_best_pose_across_frames_with_evidence_and_unchanged_input():
    _, query = reference()
    source = ensemble(COORDINATES * [1, 1, -1], moved_coordinates(), COORDINATES)
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    result = ConformerScreening(query).evaluate(source, pose_id="ligand")
    assert result["status"] == "matched" and result["fit_value"] == 1
    assert result["best_conformer_index"] == result["structure_index"] == 1
    assert result["ensemble"]["complete"]
    assert result["ensemble"]["n_evaluated"] == 3
    assert [entry["conformer_index"] for entry in result["conformers"]] == [0, 1, 2]
    assert [entry["status"] for entry in result["conformers"]] == [
        "not_matched",
        "matched",
        "matched",
    ]
    assert all(entry["pose_id"] == "ligand" for entry in result["conformers"])
    assert result["alignment"]["correspondence"]
    assert result["alignment"]["structure_index"] == 1
    assert result["resolved_chemical_state_index"] == 0
    np.testing.assert_allclose(
        unpack(result["pose_coordinates"])[0], COORDINATES, atol=1e-12
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )
    json.dumps(result, allow_nan=False)


def test_requested_order_breaks_ties_and_best_identity_coordinates_keep_units():
    source, query = reference()
    source.structures.append(coordinates=puw.quantity([COORDINATES], "nm"))
    with puw.context(standard_units=["angstrom", "ps", "degrees"]):
        result = ConformerScreening(query).evaluate(
            source, structure_indices=np.array([1, 0]), chemical_state=0
        )
    assert result["best_conformer_index"] == 1
    assert result["ensemble"]["structure_indices"] == [1, 0]
    assert result["alignment"] is None
    assert result["chemical_state"] == result["resolved_chemical_state_index"] == 0
    np.testing.assert_allclose(
        unpack(result["pose_coordinates"]), [COORDINATES], rtol=1e-14, atol=1e-14
    )


def test_all_negative_frames_give_a_complete_scientific_negative():
    _, query = reference()
    source = ensemble(distorted_coordinates(), COORDINATES * [1, 1, -1])
    result = ConformerScreening(query).evaluate(source)
    assert result["status"] == "not_matched"
    assert result["fit_value"] < 1
    assert result["ensemble"]["complete"] and result["ensemble"]["score_resolved"]
    assert result["ensemble"]["n_failed"] == 0


def test_recorded_failure_can_coexist_with_a_proven_maximum_but_raise_is_default():
    _, query = reference()
    source = ensemble(moved_coordinates(), COORDINATES)
    screen = ConformerScreening(query, max_trials=1)
    with pytest.raises(PoseEvaluationError) as caught:
        screen.evaluate(source)
    assert caught.value.__cause__.code == "PHMT-E105"
    result = screen.evaluate(source, on_error="record")
    assert result["status"] == "matched" and result["fit_value"] == 1
    assert result["best_conformer_index"] == 1
    assert not result["ensemble"]["complete"]
    assert result["ensemble"]["proven_maximum"] and result["ensemble"]["score_resolved"]
    failure = result["conformers"][0]
    assert failure["status"] == "failed" and failure["fit_value"] is None
    assert failure["error"]["cause_code"] == "PHMT-E105"
    assert failure["error"]["stage"] == "search_budget"
    assert failure["structure_index"] == failure["resolved_chemical_state_index"] == 0


def test_partial_negative_has_no_definitive_score_and_is_excluded_from_metrics():
    source, query = reference()
    invalid = COORDINATES.copy()
    invalid[3] = invalid[4]  # Indexed donor and hydrogen coincide.
    partial = ensemble(distorted_coordinates(), invalid)
    screen = ConformerScreening(query)
    result = screen.evaluate(partial, on_error="record")
    assert result["status"] == "failed" and result["fit_value"] is None
    assert result["best_conformer_index"] is None
    assert result["best_observed"]["status"] == "not_matched"
    assert result["best_observed"]["conformer_index"] == 0
    assert not result["ensemble"]["score_resolved"]
    negative = ensemble(distorted_coordinates())
    report = RetrospectiveValidator(query, evaluator=screen).run(
        (entry for entry in [source, source]),
        (entry for entry in [partial, negative]),
        on_error="record",
    )
    assert report["n_failed"] == 1 and report["n_evaluated"] == 3
    assert report["n_actives_found"] == 2
    assert report["evaluated_indices"].tolist() == [0, 1, 3]
    assert [entry["input_index"] for entry in report["evaluations"]] == [0, 1, 2, 3]
    assert report["AUC"] == report["BEDROC"] == 1
    assert report["failures"][0]["conformers"][1]["status"] == "failed"


def test_all_failed_frames_retain_each_cause_and_no_best_pose():
    _, query = reference()
    source = ensemble(moved_coordinates(), moved_coordinates())
    result = ConformerScreening(query, max_trials=1).run([source], on_error="record")[0]
    assert result["status"] == "failed" and result["fit_value"] is None
    assert result["best_observed"] is None and result["best_conformer_index"] is None
    assert result["ensemble"]["n_failed"] == 2
    assert result["ensemble"]["n_evaluated"] == 0
    assert all(
        entry["error"]["cause_code"] == "PHMT-E105" for entry in result["conformers"]
    )
    json.dumps(result, allow_nan=False)


def test_excluded_unit_coverage_cannot_resolve_an_ensemble_with_failed_frames():
    _, query = reference()
    query.add_interaction_site(
        InteractionSite(
            Sphere(puw.quantity(COORDINATES[0], "nm"), "0.01 nm"), "excluded volume"
        )
    )
    invalid = COORDINATES.copy()
    invalid[3] = invalid[4]
    result = ConformerScreening(query).evaluate(
        ensemble(COORDINATES, invalid), on_error="record"
    )
    assert result["status"] == "failed" and result["fit_value"] is None
    assert result["best_observed"]["fit_value"] == 1
    assert result["best_observed"]["status"] == "not_matched"
    assert result["best_observed"]["excluded_volume_clashes"]
    assert not result["ensemble"]["proven_maximum"]


def test_structure_state_policy_uses_each_declared_state_instead_of_reference():
    source = system("[Na+].[K+].[Li+]", [[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    query = from_ligand(source, features=["positive charge"], radius="0.02 nm")
    add_declared_state(source, [0, 0, 0])
    state = 1
    source.structures.append(coordinates=msm.get(source, coordinates=True))
    msm.set(
        source,
        element="system",
        structure_chemical_state_index=[0, state],
    )
    screen = ConformerScreening(query)
    result = screen.evaluate(
        source, structure_indices=[1, 0], chemical_state="structure"
    )
    assert result["best_conformer_index"] == 0
    assert [
        entry["resolved_chemical_state_index"] for entry in result["conformers"]
    ] == [1, 0]
    assert [entry["status"] for entry in result["conformers"]] == [
        "not_matched",
        "matched",
    ]
    assert (
        result["conformers"][0]["recognition"]["formal_charge"]["chemical_state_index"]
        == 1
    )
    explicit = screen.evaluate(
        source, structure_indices=[1], chemical_state="reference"
    )
    assert (
        explicit["status"] == "matched"
        and explicit["resolved_chemical_state_index"] == 0
    )
    assert msm.get(source, structure_chemical_state_index=True) == [0, 1]


def test_state_dependent_selection_uses_the_same_frame_state_as_recognition():
    source = system(
        "[Na+].[K+].[Li+].[Na+]", [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0]]
    )
    query = from_ligand(
        source, selection=[0, 1, 2], features=["positive charge"], radius="0.02 nm"
    )
    add_declared_state(source, [0, 1, 1, 1])
    source.structures.append(coordinates=msm.get(source, coordinates=True))
    msm.set(source, element="system", structure_chemical_state_index=[0, 1])
    result = ConformerScreening(query).evaluate(
        source,
        selection="formal_charge==1",
        structure_indices=[1],
        chemical_state="structure",
    )
    assert result["status"] == "matched"
    assert result["selected_atom_indices"] == [1, 2, 3]
    assert result["resolved_chemical_state_index"] == 1
    assert unpack(result["pose_coordinates"]).shape == (1, 3, 3)
    assert [entry["atom_indices"] for entry in result["assignments"]] == [[3], [1], [2]]


def test_selection_preserves_spectators_and_best_coordinates_match_selected_order():
    _, query = reference()
    coordinates = np.vstack((COORDINATES, [[4, 5, 6]]))
    source = system(SMILES + ".[Na+]", coordinates)
    source.structures.append(coordinates=msm.get(source, coordinates=True))
    prepared = msm.structure.translate(
        source,
        selection=list(range(8)),
        structure_indices=[1],
        translation=puw.quantity([[[2, 1, 3]]], "nm"),
        in_place=False,
    )
    before = puw.get_value(msm.get(prepared, coordinates=True), to_unit="nm").copy()
    result = ConformerScreening(query).evaluate(
        prepared, selection="atom_index < 8", structure_indices=[1]
    )
    assert result["best_conformer_index"] == 1
    assert result["selected_atom_indices"] == list(range(8))
    np.testing.assert_allclose(
        unpack(result["pose_coordinates"])[0], COORDINATES, atol=1e-12
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(prepared, coordinates=True), to_unit="nm"), before
    )


def test_hit_priority_precedes_coverage_and_partial_hits_remain_unresolved():
    _, query = reference()
    query.interaction_sites[-1].essential = False
    query.add_interaction_site(
        InteractionSite(
            Sphere(puw.quantity(COORDINATES[0], "nm"), "0.01 nm"), "excluded volume"
        )
    )
    positive = COORDINATES.copy()
    positive[0] += [0, 0, 0.1]  # Spectator outside the exclusion.
    positive[-1] += [0, 0, 2]  # Optional charge site is absent from the pose.
    source = ensemble(COORDINATES, positive)
    screen = ConformerScreening(query)
    result = screen.evaluate(source)
    assert result["conformers"][0]["fit_value"] == 1
    assert result["conformers"][0]["status"] == "not_matched"
    assert result["status"] == "matched" and result["fit_value"] == 0.8
    assert result["best_conformer_index"] == 1
    invalid = COORDINATES.copy()
    invalid[3] = invalid[4]
    source.structures.append(coordinates=puw.quantity([invalid], "nm"))
    partial = screen.evaluate(source, on_error="record")
    assert partial["status"] == "failed" and partial["fit_value"] is None
    assert partial["best_observed"]["status"] == "matched"
    assert partial["best_observed"]["fit_value"] == 0.8
    assert not partial["ensemble"]["score_resolved"]


def test_missing_frame_state_is_retained_and_other_frames_still_run():
    source, query = reference()
    source.structures.append(coordinates=msm.get(source, coordinates=True))
    msm.set(
        source,
        element="system",
        structure_chemical_state_index=[pd.NA, 0],
    )
    result = ConformerScreening(query).evaluate(
        source, chemical_state="structure", on_error="record"
    )
    assert result["status"] == "matched" and result["best_conformer_index"] == 1
    assert result["conformers"][0]["error"]["stage"] == "chemical_state"
    assert result["ensemble"]["n_failed"] == 1


@pytest.mark.parametrize(
    "indices", [[], [0, 0], [-1], [True], [0.5], "first", [0, [1]]]
)
def test_invalid_frame_contracts_raise_coded_argument_errors(indices):
    source, query = reference()
    with pytest.raises(ArgumentError):
        ConformerScreening(query).evaluate(source, structure_indices=indices)


def test_provider_bounds_and_empty_frame_inventory_are_failures_not_negatives():
    source, query = reference()
    screen = ConformerScreening(query)
    result = screen.run([source], structure_indices=[3], on_error="record")[0]
    assert result["status"] == "failed" and result["fit_value"] is None
    assert result["error"]["stage"] == "frames"
    assert result["error"]["cause_code"] is not None
    invalid_state = screen.run([source], chemical_state=99, on_error="record")[0]
    assert invalid_state["status"] == "failed" and invalid_state["fit_value"] is None
    assert invalid_state["conformers"][0]["resolved_chemical_state_index"] is None
    assert invalid_state["conformers"][0]["error"]["stage"] == "chemical_state"
    assert invalid_state["conformers"][0]["error"]["cause_code"] is not None
    empty = msm.convert(
        msm.convert("smiles:" + SMILES, to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
    )
    result = screen.run([empty], on_error="record")[0]
    assert result["status"] == "failed" and result["fit_value"] is None
    assert result["error"]["stage"] == "frames"
