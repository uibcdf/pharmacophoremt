"""Independent frozen-geometry, source-map and bounded-search controls."""

import numpy as np
import pytest

from devtools.prepared_search_workflow import ESSENTIAL_SITES, RING_ATOMS, run_case
from devtools.prepared_workflow import models_equivalent
from pharmacophoremt import pyunitwizard as puw


@pytest.fixture(scope="module")
def workflow(tmp_path_factory):
    return run_case(tmp_path_factory.mktemp("prepared-search"), fresh_reader=True)


def quantity_values(record):
    return puw.get_value(
        puw.QuantityRecord.from_dict(record).to_quantity(), to_unit="nm"
    )


def test_declared_anchors_and_prior_query_contract(workflow):
    sites = workflow["model"]["interaction_sites"]
    assert [i for i, row in enumerate(sites) if row["essential"]] == ESSENTIAL_SITES
    assert [sites[i]["metadata"]["atom_indices"] for i in ESSENTIAL_SITES] == [
        RING_ATOMS,
        [0],
        [8],
    ]
    assert [row["weight"] for row in sites] == [3.0, *([1.0] * 9)]
    assert workflow["prior_query"]["interaction_sites"][1]["essential"] is False
    assert workflow["prior_query"]["interaction_sites"][5]["essential"] is False
    assert "three" in workflow["incompatible_query_rejection"]["message"]
    assert workflow["model"]["score"] is None
    assert workflow["model"]["metadata"]["source_model"] == workflow["prior_query"]
    # Independent frozen CTAB atom-zero coordinate, nm.
    np.testing.assert_allclose(
        sites[1]["shape"]["center"], [0.1463, -0.0446, -0.2486], rtol=0, atol=1e-12
    )
    oracle = workflow["oracle"]
    assert oracle["anchor_triangle_area_nm2"] > 0.01
    assert (
        oracle["query_ring_to_atom8_distance_nm"]
        > oracle["selected_max_atom_distance_nm"] + 0.04
    )


def test_two_placements_preserve_the_original_coordinate_and_state_inventory(workflow):
    before = workflow["inputs_before"]
    assert before == workflow["inputs_after"]
    original = np.array(before["source"]["coordinates_nm"])
    frames = np.array(before["frames"]["coordinates_nm"])
    assert frames.shape == (2, 44, 3)
    np.testing.assert_array_equal(frames[0], original[0])
    # Test-only numerical oracle for the declared Rz(+90°) and displacement;
    # the actual molecular transform is the public provider operation.
    expected = original[0] @ np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]).T + [2, 1, 3]
    np.testing.assert_allclose(frames[1], expected, rtol=0, atol=1e-12)
    assert before["source"]["chemical_state"] == before["frames"]["chemical_state"]


@pytest.mark.parametrize("codec", ["json", "yaml", "sdf"])
def test_saved_query_recovers_moved_frame_with_original_atom_correspondence(
    workflow, codec
):
    entry = workflow["results"][codec]
    assert models_equivalent(entry["native"], workflow["model"])
    controls = entry["controls"]
    assert (
        controls["placed"]["status"] == "not_matched"
        and controls["placed"]["fit_value"] == 0
    )
    result = controls["recovered"]
    assert result["status"] == "matched" and result["fit_value"] == 1
    assert result["structure_index"] == 1
    assert result["selected_atom_indices"] == list(range(44))
    assert len(result["assignments"]) == 10
    assert result["alignment"]["provider"] == "molsysmt.structure.least_rmsd_fit"
    assert result["search"]["n_fitted"] == 1
    assert result["search"]["enumeration_complete"]
    assert result["search"]["termination"] == "optimal_fit_found"
    assert np.max(quantity_values(result["alignment"]["rmsd"])) < 1e-12
    original = np.array(workflow["inputs_before"]["source"]["coordinates_nm"])
    np.testing.assert_allclose(
        quantity_values(result["alignment"]["aligned_atom_coordinates"]),
        original,
        rtol=0,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        controls["replayed_coordinates_nm"],
        np.repeat(original, 2, axis=0),
        rtol=0,
        atol=1e-12,
    )
    assert controls["replayed_pose"]["status"] == "matched"
    assert (
        controls["replayed_state"]
        == workflow["inputs_before"]["frames"]["chemical_state"]
    )
    facade = controls["facade"]
    assert facade["hit_input_indices"] == [0, 2]
    assert facade["original_input_references"]
    assert [row["conf_id"] for row in facade["scalar_hits"]] == [1, 1]
    assert [row["status"] for row in facade["evaluations"]] == [
        "matched",
        "failed",
        "matched",
    ]
    assert facade["evaluations"][1]["fit_value"] is None


@pytest.mark.parametrize("codec", ["json", "yaml", "sdf"])
def test_complete_selected_negative_stays_distinct_from_budget_failure(workflow, codec):
    controls = workflow["results"][codec]["controls"]
    negative = controls["selected_negative"]
    assert negative["status"] == "not_matched"
    assert negative["fit_value"] == pytest.approx(8 / 12)
    assert negative["missing_essential_sites"] == [5]
    assert negative["selected_atom_indices"] == RING_ATOMS
    assert negative["search"]["enumeration_complete"]
    assert negative["search"]["n_proposals"] == negative["search"]["n_fitted"] == 0
    assert negative["search"]["termination"] == "enumeration_complete"
    failed = controls["budget_failure"]
    assert failed["status"] == "failed" and failed["fit_value"] is None
    assert failed["error"]["stage"] == "search_budget"
    assert failed["error"]["cause_code"] == "PHMT-E105"


@pytest.mark.parametrize("codec", ["json", "yaml", "sdf"])
@pytest.mark.parametrize("order", [[1, 0], [0, 1]])
def test_frame_ties_and_resolved_score_do_not_hide_failed_searches(
    workflow, codec, order
):
    controls = workflow["results"][codec]["controls"]
    for budget in (10000, 1):
        result = controls["ensembles"][f"{budget}:{order}"]
        assert result["status"] == "matched" and result["fit_value"] == 1
        assert result["best_conformer_index"] == (order[0] if budget == 10000 else 0)
        assert [row["conformer_index"] for row in result["conformers"]] == order
        ensemble = result["ensemble"]
        assert ensemble["structure_indices"] == order
        assert ensemble["n_requested"] == 2
        assert ensemble["score_resolved"] and ensemble["proven_maximum"]
        assert ensemble["complete"] == (budget == 10000)
        assert ensemble["n_failed"] == (0 if budget == 10000 else 1)
        assert ensemble["n_evaluated"] == (2 if budget == 10000 else 1)
        for frame in result["conformers"]:
            assert frame["resolved_chemical_state_index"] == 0
            if budget == 1 and frame["conformer_index"] == 1:
                assert frame["status"] == "failed" and frame["fit_value"] is None
            else:
                assert frame["status"] == "matched" and frame["fit_value"] == 1
                if budget == 1:
                    assert not frame["search"]["enumeration_complete"]
                    assert frame["search"]["termination"] == "optimal_fit_found"
        original = np.array(workflow["inputs_before"]["source"]["coordinates_nm"])
        np.testing.assert_allclose(
            quantity_values(result["pose_coordinates"]), original, rtol=0, atol=1e-12
        )


def test_fresh_readers_keep_evidence_without_new_calculation_credits(workflow):
    reader = workflow["fresh_reader"]
    assert len(reader["models"]) == 3
    assert reader["attribution"]["uses"] == []
    assert all(
        models_equivalent(row, workflow["model"]) for row in reader["models"].values()
    )
