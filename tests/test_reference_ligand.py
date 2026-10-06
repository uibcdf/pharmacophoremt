"""Analytical controls for native reference-ligand construction and evaluation."""

import json

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import model
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.io import load_json, to_json
from pharmacophoremt.modeler import from_ligand, get_features
from pharmacophoremt.screening import PoseEvaluator
from pharmacophoremt.validation.retrospective import RetrospectiveValidator
from tests.test_pose_evaluation import system


def benzene(rotation=None, translation=0, unit="nm"):
    angles = np.arange(6) * np.pi / 3
    coordinates = np.column_stack(
        (0.14 * np.cos(angles), 0.14 * np.sin(angles), np.zeros(6))
    )
    if rotation is not None:
        coordinates = coordinates @ rotation.T
    return system("c1ccccc1", coordinates + translation, unit=unit)


def test_reference_ligand_to_evaluation_and_retrospective_ranking():
    source = system("CCC", [[0, 0, 0], [0.15, 0, 0], [0.3, 0, 0]])
    query = from_ligand(source, name="propane")
    assert query.n_interaction_sites == 1
    assert query.metadata["definition"] == "classical_atomic_formal@1"
    assert query.interaction_sites[0].metadata["atom_indices"] == [1]
    assert model(source, method="reference-ligand").n_interaction_sites == 1
    evaluator = PoseEvaluator(query)
    displaced = system("CCC", [[2, 0, 0], [2.15, 0, 0], [2.3, 0, 0]])
    report = RetrospectiveValidator(query, evaluator=evaluator).run(
        [source], [displaced]
    )
    assert report["scores"].tolist() == [1, 0]
    assert report["AUC"] == report["BEDROC"] == 1
    assert report["n_actives_found"] == 1


def test_aromatic_geometry_comes_from_public_provider_and_normal_is_unoriented(
    monkeypatch,
):
    calls = []
    provider = msm.structure.get_least_squares_plane

    def recorded(*args, **kwargs):
        calls.append(kwargs["selection"])
        return provider(*args, **kwargs)

    monkeypatch.setattr(msm.structure, "get_least_squares_plane", recorded)
    source = benzene()
    query = from_ligand(source, features=["aromatic ring"], radius="0.03 nm")
    site = query.interaction_sites[0]
    assert site.metadata["atom_indices"] == list(range(6))
    np.testing.assert_allclose(
        puw.get_value(site.center, to_unit="nm"), [0, 0, 0], atol=1e-15
    )
    assert site.shape_name == "disk"
    assert calls == [[list(range(6))]]
    site.shape.normal = -site.shape.normal
    evaluator = PoseEvaluator(query, direction_tolerance="10 degrees")
    assert evaluator.evaluate(source)["status"] == "matched"
    # Same center and chemistry, orthogonal plane: only the angular control fails.
    orthogonal = benzene(rotation=np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]))
    assert evaluator.evaluate(orthogonal)["status"] == "not_matched"
    assert evaluator.evaluate(benzene(translation=[1, 0, 0]))["status"] == "not_matched"


def test_formal_charge_group_centroid_sign_and_source_membership(monkeypatch):
    calls = []
    provider = msm.structure.get_center

    def recorded(*args, **kwargs):
        calls.append(kwargs["selection"])
        return provider(*args, **kwargs)

    monkeypatch.setattr(msm.structure, "get_center", recorded)
    source = system(
        "CC(=O)[O-].[NH4+]",
        [[0, 0, 0], [0.15, 0, 0], [0.25, 0.1, 0], [0.25, -0.1, 0], [0.6, 0, 0]],
    )
    inventory = get_features(source, features=["positive charge", "negative charge"])
    negative = next(
        record
        for record in inventory["features"]
        if record["kind"] == "negative charge"
    )
    assert negative["atom_indices"] == [1, 2, 3]
    assert negative["geometry_atom_indices"] == [2, 3]
    np.testing.assert_allclose(
        puw.get_value(negative["center"], to_unit="nm"), [0.25, 0, 0]
    )
    assert puw.get_value(negative["charge"], to_unit="e") == -1
    assert calls == [[[2, 3], [4]]]
    query = from_ligand(source, features=["negative charge"], radius="0.02 nm")
    assert PoseEvaluator(query).evaluate(source)["status"] == "matched"
    query.interaction_sites[0].features = ["positive charge"]
    assert PoseEvaluator(query).evaluate(source)["status"] == "not_matched"
    # Selection of only one oxygen must not invent a partial charge center.
    with pytest.raises(
        Exception, match="selection cuts a compound charge center"
    ) as caught:
        from_ligand(source, selection=[3], features=["negative charge"])
    assert type(caught.value).__name__ == "ArgumentError"
    assert type(caught.value).__module__.startswith("molsysmt.")


def test_all_six_families_round_trip_without_changing_molecular_coordinates(tmp_path):
    smiles = "CCC.[2H]O.C=O.c1ccccc1.CC(=O)[O-].[NH4+]"
    angles = np.arange(6) * np.pi / 3
    ring = np.column_stack(
        (1 + 0.14 * np.cos(angles), 0.14 * np.sin(angles), np.zeros(6))
    )
    coordinates = np.vstack(
        (
            [
                [0, 0, 0],
                [0.15, 0, 0],
                [0.3, 0, 0],
                [0.1, 0.5, 0],
                [0, 0.5, 0],
                [0.3, 0.6, 0],
                [0.3, 0.5, 0],
            ],
            ring,
            [[2, 0, 0], [2.15, 0, 0], [2.25, 0.1, 0], [2.25, -0.1, 0], [2.6, 0, 0]],
        )
    )
    source = system(smiles, coordinates * 10, unit="angstrom")
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    query = from_ligand(source)
    assert {site.features[0] for site in query.interaction_sites} == {
        "hydrophobicity",
        "hb donor",
        "hb acceptor",
        "aromatic ring",
        "positive charge",
        "negative charge",
    }
    result = PoseEvaluator(query).evaluate(source)
    assert result["status"] == "matched"
    assert len(result["assignments"]) == query.n_interaction_sites
    json.dumps(result, allow_nan=False)
    path = tmp_path / "query.json"
    to_json(query, str(path))
    loaded = load_json(str(path))
    assert loaded.metadata == query.metadata
    assert loaded.interaction_sites[-1].metadata == query.interaction_sites[-1].metadata
    assert PoseEvaluator(loaded).evaluate(source)["status"] == "matched"
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )


def test_shared_rigid_transform_and_nondefault_units_preserve_aromatic_fit():
    rotation = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    source = benzene(rotation, translation=[2, 1, 3])
    query = from_ligand(source, features=["aromatic ring"])
    assert PoseEvaluator(query).evaluate(source)["fit_value"] == 1
    inventory = get_features(source, features=["aromatic ring"])
    np.testing.assert_allclose(
        puw.get_value(inventory["features"][0]["center"], to_unit="angstrom"),
        [20, 10, 30],
    )


def test_aromatic_normal_remains_dimensionless_under_degree_policy():
    with puw.context(standard_units=["angstrom", "ps", "degrees"]):
        source = benzene()
        query = from_ligand(source, features=["aromatic ring"])
        np.testing.assert_allclose(
            np.abs(
                puw.get_value(
                    query.interaction_sites[0].shape.normal, to_unit="dimensionless"
                )
            ),
            [0, 0, 1],
        )
        result = PoseEvaluator(query).evaluate(source)
        assert result["status"] == "matched"
        assert (
            result["execution"]["matching_method"]
            == "essential_then_weighted_one_to_one@1"
        )
        assert result["execution"]["backend"] == "numpy_scipy_cpu"
        assert result["criteria"]["feature_definition"] == "classical_atomic_formal@1"


def test_unsupported_feature_and_incomplete_geometry_fail_visibly():
    with pytest.raises(ArgumentError):
        get_features(benzene(), features=["halogen bond"])
    with pytest.raises(Exception, match="selection cuts a perceived ring") as caught:
        from_ligand(benzene(), selection=[0, 1], features=["aromatic ring"])
    assert type(caught.value).__name__ == "ArgumentError"
    assert type(caught.value).__module__.startswith("molsysmt.")
    query = from_ligand(benzene(), features=["aromatic ring"])
    degenerate = system("c1ccccc1", np.zeros((6, 3)))
    with pytest.raises(PoseEvaluationError) as caught:
        PoseEvaluator(query).evaluate(degenerate)
    assert caught.value.extra["stage"] == "recognition"
