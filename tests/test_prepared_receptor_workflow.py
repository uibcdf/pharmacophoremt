"""Independent cached-fragment projection/contact and persistence controls."""

import numpy as np
import pytest

from devtools.prepared_receptor_workflow import (
    PHE_ATOMS,
    RING_ATOMS,
    expectations_passed,
    run_case,
)
from devtools.prepared_workflow import models_equivalent
from pharmacophoremt import pyunitwizard as puw


@pytest.fixture(scope="module")
def workflow(tmp_path_factory):
    return run_case(tmp_path_factory.mktemp("prepared-receptor"), fresh_reader=True)


def values(record, unit="nm"):
    return puw.get_value(
        puw.QuantityRecord.from_dict(record).to_quantity(), to_unit=unit
    )


def test_archived_preparation_and_all_cached_observations_are_unchanged(workflow):
    identity = workflow["input_identity"]
    assert (
        identity["native_evidence"]["uncompressed_sha256"]
        == "a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a"
    )
    assert identity["historical_recorded_utc"].startswith("2026-10-07")
    assert workflow["inputs_before"] == workflow["inputs_after"]
    before = np.array(workflow["inputs_before"]["coordinates_nm"])
    assert before.shape == (1, 4047, 3)
    np.testing.assert_allclose(
        workflow["translated_coordinates_nm"], before + [0, 0, 0.35], rtol=0, atol=1e-12
    )
    np.testing.assert_allclose(
        workflow["displaced_coordinates_nm"], before + [2, 0, 0], rtol=0, atol=1e-12
    )
    assert workflow["ligand_selection"] == list(range(4003, 4047))
    assert workflow["selection"] == [*PHE_ATOMS, *range(2772, 2781)]
    assert (
        workflow["projected_inventory"]["selected_atom_indices"]
        == workflow["selection"]
    )
    assert workflow["projected_inventory"]["chemical_state"] == "reference"
    assert workflow["projected_inventory"]["structure_index"] == 0
    assert (
        "NaN" in workflow["inputs_before"]["chemical_state_json"]
    )  # Unknown native history retained as text.


def test_projection_means_plane_axis_and_independent_exclusion_bounds(workflow):
    coordinates = np.array(workflow["inputs_before"]["coordinates_nm"])[0]
    points = coordinates[RING_ATOMS]
    center = points.mean(axis=0)
    np.testing.assert_allclose(
        center, [10.3282, 1.9207666666666665, 2.0210166666666667], rtol=0, atol=1e-12
    )
    inventory = workflow["projected_inventory"]
    assert len(inventory["features"]) == 1
    source_feature = inventory["features"][0]
    assert source_feature["atom_indices"] == RING_ATOMS
    np.testing.assert_allclose(
        values(source_feature["center"]), center, rtol=0, atol=1e-12
    )
    normal = np.linalg.svd(points - center)[2][
        -1
    ]  # Test-only independent plane oracle.
    assert abs(
        np.dot(normal, values(source_feature["normal"], "dimensionless"))
    ) == pytest.approx(1, abs=1e-12)
    for name, delta in (("projected", 0.35), ("opposite", -0.35), ("collision", 0.35)):
        model = workflow["models"][name]
        assert len(model["interaction_sites"]) == 12
        site = model["interaction_sites"][0]
        assert site["metadata"]["source_feature_index"] == 0
        assert site["metadata"]["atom_indices"] == RING_ATOMS
        assert (
            site["metadata"]["structure_index"] == 0
            and site["metadata"]["chemical_state"] == "reference"
        )
        assert site["weight"] == 1 and site["essential"]
        np.testing.assert_allclose(
            site["shape"]["center"], center + [0, 0, delta], rtol=0, atol=1e-12
        )
        assert abs(np.dot(site["shape"]["normal"], normal)) == pytest.approx(
            1, abs=1e-12
        )
        assert model["metadata"]["supplied_projection_specs"][0][
            "projection_direction"
        ] == [0, 0, 2 if delta > 0 else -2]
        assert model["metadata"]["policy"]["molecular_geometry_inference"] is False
        for atom, excluded in zip(PHE_ATOMS, model["interaction_sites"][1:]):
            assert excluded["metadata"]["atom_indices"] == [atom]
            assert excluded["weight"] == 0
            np.testing.assert_allclose(
                excluded["shape"]["center"], coordinates[atom], rtol=0, atol=1e-12
            )
    # Bound the declared positive from original atoms, independently of evaluator output.
    moved = coordinates[PHE_ATOMS] + [0, 0, 0.35]
    distances = np.linalg.norm(
        moved[:, None] - coordinates[PHE_ATOMS][None, :], axis=-1
    )
    assert distances.min() > 0.01
    np.testing.assert_allclose(np.diag(distances), 0.35, rtol=0, atol=1e-12)
    assert np.all(np.diag(distances) < 0.40)
    assert (
        0.35 > 0.02 and 0.70 > 0.02
    )  # Original and opposite centers cannot fill the positive radius.


def test_observed_pairs_keep_deposited_source_maps_and_direct_distance_oracle(workflow):
    payload = workflow["inputs_before"]["analyses"]["hydrophobic"]
    atoms = np.array(payload["participant_atoms"]).reshape(-1, 2)
    mapping = np.array(payload["atom_source_indices"])
    pairs = mapping[atoms]
    expected = [
        [673, 5944],
        [673, 5945],
        [701, 5944],
        [813, 5940],
        [813, 5941],
        [813, 5950],
        [815, 5940],
        [815, 5941],
        [815, 5944],
        [815, 5945],
        [815, 5949],
        [815, 5950],
    ]
    np.testing.assert_array_equal(pairs, expected)
    assert workflow["oracle"]["expected_hydrophobic_source_pairs"] == expected
    assert payload["source_id"] == "rcsb:1QKU:deposited-atom-order"
    coordinates = np.array(workflow["inputs_before"]["coordinates_nm"])[0]
    distance = np.linalg.norm(
        coordinates[atoms[:, 0]] - coordinates[atoms[:, 1]], axis=1
    )
    np.testing.assert_allclose(
        payload["measurements"]["distance"], distance, rtol=0, atol=1e-12
    )
    assert np.all(distance <= 0.45) and payload["measure_units"]["distance"] == "nm"
    model = workflow["models"]["observed"]
    assert len(model["interaction_sites"]) == 6
    assert {
        row["label"]: row["n_sites"] for row in model["metadata"]["components"]
    } == {"hydrophobic": 6, "hbonds": 0, "pi_pi": 0}
    analysis = model["metadata"]["interaction_collection"]["analyses"]
    assert {row["label"]: row["n_observations"] for row in analysis} == {
        "hydrophobic": 12,
        "hbonds": 0,
        "pi_pi": 0,
    }
    assert all(row["evaluated_structure_indices"] == [0] for row in analysis)
    # Hydrophobic observed participants span far less than the declared 2 nm x displacement.
    centers = np.array([s["shape"]["center"] for s in model["interaction_sites"]])
    assert np.ptp(centers[:, 0]) + 0.15 < 2


def test_empty_models_and_failed_uncached_frames_never_publish_stale_success(workflow):
    assert workflow["empty"]["interaction_sites"] == []
    assert workflow["empty"]["metadata"]["omitted_feature_indices"] == [0]
    assert len(workflow["exclusion_only"]["interaction_sites"]) == 11
    assert all(
        s["weight"] == 0 for s in workflow["exclusion_only"]["interaction_sites"]
    )
    assert set(workflow["empty_query_rejections"]) == {"empty", "exclusion_only"}
    assert set(workflow["failed_rebuilds"]) == {
        "structure",
        "complex",
        "complex_uncovered",
    }
    uncovered = workflow["failed_rebuilds"]["complex_uncovered"]
    assert uncovered["requested_frame"] == 0
    assert all(
        indices == [] for indices in uncovered["evaluated_structure_indices"].values()
    )
    for failed in workflow["failed_rebuilds"].values():
        assert failed["result_is_none"] and failed["code"]


@pytest.mark.parametrize("codec", ["json", "yaml", "sdf"])
def test_saved_positive_negative_veto_and_observed_queries_keep_original_maps(
    workflow, codec
):
    for name in ("projected", "opposite", "collision", "observed"):
        key = name + "." + codec
        entry = workflow["results"][key]
        assert models_equivalent(entry["native"], workflow["models"][name])
        original, moved = entry["outcomes"]["original"], entry["outcomes"]["translated"]
        assert original["status"] == (
            "matched" if name == "observed" else "not_matched"
        )
        assert moved["status"] == ("matched" if name == "projected" else "not_matched")
        assert moved["fit_value"] == (1 if name in {"projected", "collision"} else 0)
        assert moved["selected_atom_indices"] == (
            workflow["ligand_selection"]
            if name == "observed"
            else workflow["selection"]
        )
        assert models_equivalent(
            workflow["fresh_reader"]["models"][key], workflow["models"][name]
        )
        assert workflow["models"][name]["score"] is None
    assert workflow["fresh_reader"]["attribution"]["uses"] == []
    assert expectations_passed(workflow)
