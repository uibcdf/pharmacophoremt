"""Rigid-search scientific controls using real public MolSysMT tools."""

import json

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
from pharmacophoremt.modeler import from_ligand, get_features
from pharmacophoremt.screening import (
    PoseEvaluator,
    RigidPoseSearch,
    align_to_pharmacophore,
    get_correspondences,
)
from pharmacophoremt.validation.retrospective import RetrospectiveValidator
from tests.test_pose_evaluation import system

COORDINATES = np.array(
    [
        [0, 0, 0],
        [0.15, 0, 0],
        [0.3, 0, 0],
        [0.1, 0.5, 0],
        [0, 0.5, 0],
        [0.3, 0.6, 0],
        [0.3, 0.5, 0],
        [0.05, 0.2, 0.7],
    ]
)
SMILES = "CCC.[2H]O.C=O.[NH4+]"
FAMILIES = ["hydrophobicity", "hb donor", "hb acceptor", "positive charge"]


def reference():
    source = system(SMILES, COORDINATES)
    return source, from_ligand(source, features=FAMILIES, radius="0.02 nm")


def moved(source):
    rotated = msm.structure.rotate(
        source,
        rotation=np.array([[0.0, -1, 0], [1, 0, 0], [0, 0, 1]]),
        rotation_center=puw.quantity([0, 0, 0], "nm"),
        in_place=False,
    )
    return msm.structure.translate(
        rotated, translation=puw.quantity([[[2.0, 1, 3]]], "nm"), in_place=False
    )


def test_recovers_rigid_motion_and_retains_portable_alignment_and_donor_direction():
    source, query = reference()
    displaced = moved(source)
    before = puw.get_value(msm.get(displaced, coordinates=True), to_unit="nm").copy()
    assert PoseEvaluator(query).evaluate(displaced)["status"] == "not_matched"
    result = RigidPoseSearch(query).evaluate(displaced, pose_id="ligand-7")
    assert result["status"] == "matched" and result["fit_value"] == 1
    assert result["pose_id"] == "ligand-7"
    assert len(result["assignments"]) == query.n_interaction_sites
    assert result["search"]["n_fitted"] > 0
    assert result["search"]["termination"] == "optimal_fit_found"
    assert result["alignment"]["provider"] == "molsysmt.structure.least_rmsd_fit"
    rmsd = puw.QuantityRecord.from_dict(result["alignment"]["rmsd"]).to_quantity(
        unit="nm", dimensionality={"[L]": 1}
    )
    assert np.max(puw.get_value(rmsd, to_unit="nm")) < 1e-12
    json.dumps(result, allow_nan=False)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(displaced, coordinates=True), to_unit="nm"), before
    )


def test_correspondence_and_alignment_are_independently_reusable_and_use_provider(
    monkeypatch,
):
    source, query = reference()
    displaced = moved(source)
    inventory = get_features(displaced, features=FAMILIES)
    proposals = get_correspondences(query, inventory)
    assert proposals["complete"]
    assert proposals["correspondences"]
    calls = []
    fit = msm.structure.least_rmsd_fit

    def recorded(*args, **kwargs):
        calls.append((kwargs["use_gpu"], kwargs["precision"]))
        return fit(*args, **kwargs)

    monkeypatch.setattr(msm.structure, "least_rmsd_fit", recorded)
    aligned = align_to_pharmacophore(
        displaced, query, proposals["correspondences"][0], feature_inventory=inventory
    )
    assert calls == [(False, "double")]
    assert (
        PoseEvaluator(query).evaluate(aligned["molecular_system"])["status"]
        == "matched"
    )
    np.testing.assert_allclose(
        puw.get_value(
            msm.get(aligned["molecular_system"], coordinates=True), to_unit="nm"
        )[0],
        COORDINATES,
        atol=1e-12,
    )


def test_reflection_and_distorted_geometry_are_negatives_and_rank_below_rigid_positive():
    source, query = reference()
    reflected = system(SMILES, COORDINATES * [1, 1, -1])
    distorted_coordinates = COORDINATES.copy()
    distorted_coordinates[-1] += [0, 0, 2]
    distorted = system(SMILES, distorted_coordinates)
    search = RigidPoseSearch(query)
    assert search.evaluate(reflected)["status"] == "not_matched"
    assert search.evaluate(distorted)["status"] == "not_matched"
    report = RetrospectiveValidator(query, evaluator=search).run(
        [moved(source)], [reflected, distorted]
    )
    assert report["AUC"] == report["BEDROC"] == 1
    assert report["n_actives_found"] == 1
    assert report["scores"][0] == 1
    assert np.all(report["scores"][1:] < 1)


def test_incomplete_enumeration_is_failure_without_a_proven_maximum_fit():
    source, query = reference()
    search = RigidPoseSearch(query, max_trials=1)
    inventory = get_features(moved(source), features=FAMILIES)
    proposals = get_correspondences(query, inventory, max_trials=1)
    assert not proposals["complete"]
    assert proposals["n_trials"] == 1
    with pytest.raises(PoseEvaluationError) as caught:
        search.evaluate(moved(source))
    assert caught.value.extra["stage"] == "search_budget"
    assert caught.value.__cause__.code == "PHMT-E105"
    records = search.run([source, moved(source)], on_error="record")
    assert records[0]["status"] == "matched"
    assert not records[0]["search"]["enumeration_complete"]
    assert records[1]["status"] == "failed" and records[1]["fit_value"] is None
    assert records[1]["input_index"] == 1
    report = RetrospectiveValidator(query, evaluator=search).run(
        [source], [moved(source)], on_error="record"
    )
    assert report["n_failed"] == 1 and report["n_decoys_evaluated"] == 0
    assert report["scores"].tolist() == [1]


def test_alignment_preserves_other_atoms_and_frames_and_handles_angstrom_policy():
    source, query = reference()
    coordinates = np.vstack((COORDINATES, [[4, 5, 6]]))
    complex_source = system(SMILES + ".[Na+]", coordinates)
    complex_source.structures.append(coordinates=puw.quantity([coordinates], "nm"))
    selected = np.arange(8)
    displacement = puw.quantity([[[2, 1, 3]]], "nm")
    displaced = msm.structure.translate(
        complex_source,
        selection=selected,
        structure_indices=[1],
        translation=displacement,
        in_place=False,
    )
    before = puw.get_value(msm.get(displaced, coordinates=True), to_unit="nm").copy()
    with puw.context(standard_units=["angstrom", "ps", "degrees"]):
        inventory = get_features(
            displaced, selection=selected, structure_index=1, features=FAMILIES
        )
        correspondence = get_correspondences(query, inventory)["correspondences"][0]
        result = align_to_pharmacophore(
            displaced,
            query,
            correspondence,
            selection=selected,
            structure_index=1,
            feature_inventory=inventory,
        )
        assert (
            PoseEvaluator(query).evaluate(
                result["molecular_system"], selection=selected, structure_index=1
            )["status"]
            == "matched"
        )
    after = puw.get_value(
        msm.get(result["molecular_system"], coordinates=True), to_unit="nm"
    )
    np.testing.assert_array_equal(after[0], before[0])
    np.testing.assert_array_equal(after[:, 8], before[:, 8])
    np.testing.assert_allclose(after[1, :8], COORDINATES, atol=1e-12)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(displaced, coordinates=True), to_unit="nm"), before
    )


def test_exclusion_veto_is_checked_after_alignment_even_at_unit_coverage():
    source, query = reference()
    query.add_interaction_site(
        InteractionSite(
            Sphere(puw.quantity(COORDINATES[0], "nm"), "0.01 nm"), "excluded volume"
        )
    )
    result = RigidPoseSearch(query).evaluate(moved(source))
    assert result["status"] == "not_matched"
    assert result["fit_value"] == 1
    assert result["excluded_volume_clashes"] == [dict(site_index=5, atom_index=0)]
    assert result["search"]["termination"] == "enumeration_complete"


def test_missing_chemistry_is_a_valid_negative_and_invalid_query_or_indices_raise():
    _, query = reference()
    negative = system("[Na+]", [[0, 0, 0]])
    result = RigidPoseSearch(query).evaluate(negative)
    assert result["status"] == "not_matched" and result["fit_value"] == 0
    assert result["search"]["n_trials"] == result["search"]["n_fitted"] == 0
    with pytest.raises(ArgumentError):
        RigidPoseSearch(query, max_trials=0)
    with pytest.raises(ArgumentError):
        RigidPoseSearch(query, max_trials=True)
    short = from_ligand(system("CCC", COORDINATES[:3]), features=["hydrophobicity"])
    with pytest.raises(ArgumentError, match="three non-collinear"):
        RigidPoseSearch(short)
    source, query = reference()
    inventory = get_features(source, features=FAMILIES)
    with pytest.raises(ArgumentError, match="unique"):
        align_to_pharmacophore(
            source, query, [[0, 0], [1, 1], [1, 2]], feature_inventory=inventory
        )
    with pytest.raises(ArgumentError, match="out of range"):
        align_to_pharmacophore(
            source, query, [[0, 0], [1, 1], [999, 2]], feature_inventory=inventory
        )


def test_provider_failure_retains_cause_and_never_falls_back_to_local_fit(monkeypatch):
    source, query = reference()
    displaced = moved(source)

    def broken(*args, **kwargs):
        raise RuntimeError("provider fit failed")

    monkeypatch.setattr(msm.structure, "least_rmsd_fit", broken)
    with pytest.raises(PoseEvaluationError) as caught:
        RigidPoseSearch(query).evaluate(displaced)
    assert caught.value.extra["stage"] == "alignment"
    assert isinstance(caught.value.__cause__, RuntimeError)


def test_zero_weight_essential_sites_still_anchor_optional_coverage():
    source, query = reference()
    for index, site in enumerate(query.interaction_sites):
        site.essential = index in {0, 1, 4}
        site.weight = 0 if site.essential else 1
    result = RigidPoseSearch(query).evaluate(moved(source))
    assert result["status"] == "matched" and result["fit_value"] == 1
    assert result["missing_essential_sites"] == []
    assert len(result["assignments"]) == 5


def test_zero_angle_tolerance_matches_its_source_and_preserves_rigid_invariance():
    coordinates = COORDINATES.copy()
    coordinates[3] = [0.07, 0.56, 0.04]
    source = system(SMILES, coordinates)
    query = from_ligand(source, features=FAMILIES, radius="0.02 nm")
    original = PoseEvaluator(query, direction_tolerance="0 degrees").evaluate(source)
    transformed = RigidPoseSearch(query, direction_tolerance="0 degrees").evaluate(
        moved(source)
    )
    assert original["status"] == transformed["status"] == "matched"
    assert original["fit_value"] == transformed["fit_value"] == 1
    assert original["criteria"]["angle_comparison_cosine_slack"] < 1e-14


def test_grouped_aromatic_and_charge_features_align_with_plane_orientation():
    angles = np.arange(6) * np.pi / 3
    ring = np.column_stack((0.14 * np.cos(angles), 0.14 * np.sin(angles), np.zeros(6)))
    coordinates = np.vstack(
        (
            ring,
            [
                [0.6, 0.2, 0.1],
                [0.7, 0.2, 0.1],
                [0.85, 0.3, 0.1],
                [0.85, 0.1, 0.1],
                [0, 0.7, 0.4],
            ],
        )
    )
    source = system("c1ccccc1.CC(=O)[O-].[NH4+]", coordinates)
    tilted = msm.structure.rotate(
        source,
        rotation=np.array([[1.0, 0, 0], [0, 0, -1], [0, 1, 0]]),
        rotation_center=puw.quantity([0, 0, 0], "nm"),
        in_place=False,
    )
    displaced = msm.structure.translate(
        tilted, translation=puw.quantity([[[2.0, 1, 3]]], "nm"), in_place=False
    )
    with puw.context(standard_units=["angstrom", "ps", "degrees"]):
        query = from_ligand(
            source,
            features=["aromatic ring", "negative charge", "positive charge"],
            radius="0.03 nm",
        )
        result = RigidPoseSearch(query, direction_tolerance="5 degrees").evaluate(
            displaced
        )
    assert result["status"] == "matched" and result["fit_value"] == 1
    aromatic = next(
        record
        for record in result["assignments"]
        if record["feature"] == "aromatic ring"
    )
    assert aromatic["atom_indices"] == list(range(6))
    assert result["criteria"]["aromatic_normal"] == "unoriented_axis"
