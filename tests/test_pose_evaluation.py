"""Analytical placed-pose workflow using real MolSysMT chemical recognition."""

import json

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import Pharmacophore
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere, SphereAndVector
from pharmacophoremt.modeler import from_interactions
from pharmacophoremt.screening import PoseEvaluator


def system(smiles="CCC.CCC", coordinates=None, unit="nm"):
    source = msm.convert(
        msm.convert("smiles:" + smiles, to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
    )
    if coordinates is None:
        coordinates = [
            [0, 0, 0],
            [0.15, 0, 0],
            [0.30, 0, 0],
            [0, 0.3, 0],
            [0.15, 0.3, 0],
            [0.30, 0.3, 0],
        ]
    source.structures.append(coordinates=puw.quantity([coordinates], unit))
    return source


def model_from_source(source):
    observations = msm.interactions.hydrophobic.get_hydrophobic_interactions(
        source,
        selection=[0, 1, 2],
        selection_2=[3, 4, 5],
        structure_indices=[0],
        selection_mode="between",
        pbc=False,
    )
    return from_interactions(source, observations, [0, 1, 2]), observations


def test_native_interactions_to_pose_preserves_indices_units_and_provenance():
    source = system()
    model, observations = model_from_source(source)
    assert model.n_interaction_sites == 1
    assert model.interaction_sites[0].metadata["atom_indices"] == [1]
    assert model.metadata["software"]["molsysmt"] == msm.__version__
    result = PoseEvaluator(model).evaluate(
        source, selection=[0, 1, 2], pose_id="ligand"
    )
    assert result["status"] == "matched"
    assert result["fit_value"] == 1
    assert result["assignments"][0]["atom_indices"] == [1]
    assert (
        result["recognition"]["hydrophobicity"]["method"] == "smarts_hydrophobic_atoms"
    )
    assert "attribution" in result["recognition"]["hydrophobicity"]
    json.dumps(result, allow_nan=False)
    assert observations.to_dict()["relation_indices"].tolist() == [0]


def test_translation_negative_and_shared_rigid_transform_and_units():
    source = system()
    model, _ = model_from_source(source)
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="nm")[0]
    evaluator = PoseEvaluator(model)
    moved = system(coordinates=coordinates + [2, 1, 0])
    assert evaluator.evaluate(moved, selection=[0, 1, 2])["status"] == "not_matched"
    rotation = np.array([[0.0, -1, 0], [1, 0, 0], [0, 0, 1]])
    transformed = system(
        coordinates=(coordinates @ rotation.T + [2, 1, 0]) * 10, unit="angstrom"
    )
    transformed_model, _ = model_from_source(transformed)
    result = PoseEvaluator(transformed_model).evaluate(transformed, selection=[0, 1, 2])
    assert result["status"] == "matched"
    assert (
        result["fit_value"]
        == evaluator.evaluate(source, selection=[0, 1, 2])["fit_value"]
    )


def test_one_to_one_assignment_and_zero_weight_essential_site():
    source = system()
    model, _ = model_from_source(source)
    site = model.interaction_sites[0]
    model.add_interaction_site(
        InteractionSite(Sphere(site.center, site.radius), "hydrophobicity", weight=0)
    )
    result = PoseEvaluator(model).evaluate(source, selection=[0, 1, 2])
    assert result["status"] == "not_matched"
    assert len(result["assignments"]) == 1
    assert len(result["missing_essential_sites"]) == 1


def test_excluded_volume_vetoes_otherwise_matching_pose():
    source = system()
    model, _ = model_from_source(source)
    model.add_interaction_site(
        InteractionSite(Sphere("[0,0,0] nm", "0.05 nm"), "excluded volume")
    )
    result = PoseEvaluator(model).evaluate(source, selection=[0, 1, 2])
    assert result["status"] == "not_matched"
    assert result["excluded_volume_clashes"] == [{"site_index": 1, "atom_index": 0}]


def test_failures_have_no_score_and_duplicate_inputs_keep_their_indices():
    source = system()
    model, _ = model_from_source(source)
    results = PoseEvaluator(model).run(
        [source, "invalid molecular system", source],
        selection=[0, 1, 2],
        on_error="record",
    )
    assert [row["input_index"] for row in results] == [0, 1, 2]
    assert [row["status"] for row in results] == ["matched", "failed", "matched"]
    assert results[1]["fit_value"] is None
    assert results[1]["error"]["code"] == "PHMT-E103"


def test_coincident_donor_checks_real_donor_hydrogen_direction():
    # The source isotope preserves an indexed H through the SMILES conversion.
    source = system("[2H]O", [[0.1, 0, 0], [0, 0, 0]])
    sites = msm.physchem.get_hbond_sites(source, method="smarts_donor_acceptor")
    assert sites["donor_hydrogen_pairs"].tolist() == [[1, 0]]
    model = Pharmacophore()
    model.add_interaction_site(
        InteractionSite(SphereAndVector("[0,0,0] nm", "0.15 nm", [1, 0, 0]), "hb donor")
    )
    assert PoseEvaluator(model).evaluate(source)["status"] == "matched"
    model.interaction_sites[0].shape = SphereAndVector(
        "[0,0,0] nm", "0.15 nm", [-1, 0, 0]
    )
    assert PoseEvaluator(model).evaluate(source)["status"] == "not_matched"


def test_native_hydrogen_bonds_supply_donor_vector_and_acceptor_site():
    source = system("[2H]O.C=O", [[0.1, 0, 0], [0, 0, 0], [0.3, 0.1, 0], [0.3, 0, 0]])
    observations = msm.interactions.hbonds.get_hbonds(
        source,
        selection=[0, 1],
        selection_2=[2, 3],
        selection_mode="between",
        method="donor_acceptor_distance_angle",
        profile="smarts_donor_acceptor",
        structure_indices=[0],
        pbc=False,
    )
    donor = from_interactions(source, observations, [0, 1])
    acceptor = from_interactions(source, observations, [2, 3])
    assert donor.n_interaction_sites == acceptor.n_interaction_sites == 1
    assert donor.interaction_sites[0].shape_name == "sphere and vector"
    from pharmacophoremt._private.smonitor.exceptions import ArgumentError

    with pytest.raises(ArgumentError, match="crosses the selection boundary"):
        from_interactions(source, observations, [0, 2, 3])
    assert (
        PoseEvaluator(donor).evaluate(source, selection=[0, 1])["status"] == "matched"
    )
    assert (
        PoseEvaluator(acceptor).evaluate(source, selection=[2, 3])["status"]
        == "matched"
    )


def test_model_provenance_survives_native_serialization(tmp_path):
    from pharmacophoremt.io import load_json, to_json

    source = system()
    model, _ = model_from_source(source)
    path = tmp_path / "model.json"
    to_json(model, str(path))
    restored = load_json(str(path))
    assert restored.metadata == model.metadata
    assert restored.interaction_sites[0].metadata == model.interaction_sites[0].metadata
    assert (
        PoseEvaluator(restored).evaluate(source, selection=[0, 1, 2])["status"]
        == "matched"
    )


def test_uncovered_frame_and_missing_provider_capability_raise(monkeypatch):
    from pharmacophoremt._private.smonitor.exceptions import (
        ArgumentError,
        PoseEvaluationError,
    )

    source = system()
    model, observations = model_from_source(source)
    source.structures.append(coordinates=msm.get(source, coordinates=True))
    observations = msm.interactions.hydrophobic.get_hydrophobic_interactions(
        source,
        selection=[0, 1, 2],
        selection_2=[3, 4, 5],
        structure_indices=[0],
        selection_mode="between",
        pbc=False,
    )
    with pytest.raises(ArgumentError, match="not evaluated"):
        from_interactions(source, observations, [0, 1, 2], structure_index=1)
    monkeypatch.delattr(msm.physchem, "get_hydrophobic_sites")
    with pytest.raises(PoseEvaluationError) as caught:
        PoseEvaluator(model).evaluate(source, selection=[0, 1, 2])
    assert caught.value.__cause__.code == "PHMT-E104"


def test_directed_pose_is_invariant_under_degree_unit_policy():
    source = system("[2H]O", [[0.1, 0, 0], [0, 0, 0]])
    with puw.context(standard_units=["angstrom", "ps", "degrees"]):
        model = Pharmacophore()
        model.add_interaction_site(
            InteractionSite(
                SphereAndVector("[0,0,0] nm", "1.5 angstrom", [1, 0, 0]), "hb donor"
            )
        )
        assert PoseEvaluator(model).evaluate(source)["status"] == "matched"


@pytest.mark.parametrize("feature", ["hb donor", "aromatic ring"])
@pytest.mark.parametrize(
    "standard_units", [["nm", "ps", "radians"], ["angstrom", "fs", "degrees"]]
)
def test_zero_angle_roundoff_does_not_hide_a_resolvable_tilt(feature, standard_units):
    from pharmacophoremt.interaction_site.shape import Disk

    if feature == "hb donor":
        source = system("[2H]O", [[0.1, 0, 0], [0, 0, 0]])
    else:
        angles = np.arange(6) * np.pi / 3
        # Declared planar analytical fixture, not inferred molecular geometry.
        coordinates = np.column_stack(
            (0.14 * np.cos(angles), 0.14 * np.sin(angles), np.zeros(6))
        )
        source = system("c1ccccc1", coordinates)
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    tilt = np.deg2rad(0.0001)
    with puw.context(standard_units=standard_units):
        for angle, tolerance, expected in (
            (0.0, "0 degrees", "matched"),
            (tilt, "0 degrees", "not_matched"),
            (tilt, "0.0002 degrees", "matched"),
            (np.pi, "0 degrees", "not_matched" if feature == "hb donor" else "matched"),
        ):
            shape = (
                SphereAndVector(
                    "[0,0,0] nm", ".02 nm", [np.cos(angle), np.sin(angle), 0]
                )
                if feature == "hb donor"
                else Disk("[0,0,0] nm", [np.sin(angle), 0, np.cos(angle)], ".02 nm")
            )
            query = Pharmacophore()
            query.add_interaction_site(InteractionSite(shape, feature))
            result = PoseEvaluator(query, direction_tolerance=tolerance).evaluate(
                source
            )
            assert result["status"] == expected
            assert result["fit_value"] == (1 if expected == "matched" else 0)
            assert result["missing_essential_sites"] == (
                [] if expected == "matched" else [0]
            )
            assert result["criteria"]["angle_comparison_cosine_slack"] < 1e-14
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )
