"""Independent end-to-end prepared controls, without biological truth labels."""

import json

import molsysmt as msm
import numpy as np
import pytest

from devtools.prepared_ccd_ligands import prepare_case
from devtools.prepared_workflow import FEATURES, models_equivalent, run_case


@pytest.fixture(scope="module")
def workflow(tmp_path_factory):
    return run_case(tmp_path_factory.mktemp("prepared-workflow"), fresh_reader=True)


def test_fixed_input_oracle_and_molecular_ownership(workflow):
    report = workflow["preparation"]
    assert report["selected_features"] == FEATURES
    assert report["feature_counts"] == {"hydrophobicity": 9, "aromatic ring": 1}
    assert report["source_atom_ids"] == report["prepared_atom_ids"]
    assert report["source_elements"] == report["prepared_elements"]
    assert report["source_coordinates_unchanged"] and report["source_state_unchanged"]
    assert report["source_bytes_unchanged"]
    ring = workflow["original_model"]["interaction_sites"][-1]
    assert ring["metadata"]["atom_indices"] == [0, 1, 2, 4, 5, 10]
    # Independent CTAB values: first original atom, Å -> nm. No self-query oracle.
    np.testing.assert_allclose(
        workflow["original_source_atom_zero_nm"],
        [0.1463, -0.0446, -0.2486],
        rtol=0,
        atol=1e-12,
    )
    assert workflow["inputs_before"] == workflow["inputs_after"]
    assert workflow["source_coordinates_and_states_unchanged"]
    positions = [np.asarray(row["coordinates_nm"]) for row in workflow["inputs_before"]]
    np.testing.assert_allclose(
        positions[0] - positions[1],
        np.broadcast_to([0, 0, 0.05], positions[0].shape),
        atol=1e-12,
    )
    np.testing.assert_allclose(
        positions[2] - positions[1],
        np.broadcast_to([0, 0, 2.0], positions[2].shape),
        atol=1e-12,
    )
    assert workflow["oracle"]["near_min_hydrophobic_distance_nm"] > 0.02
    assert workflow["oracle"]["far_min_hydrophobic_distance_nm"] > 0.10


def test_curation_preserves_observations_and_declared_constraints(workflow):
    original = workflow["original_model"]
    narrow, wide = [workflow["models"][name] for name in ("narrow", "wide")]
    assert original["score"] == 0.9
    assert all(
        row["essential"] and row["weight"] == 1 for row in original["interaction_sites"]
    )
    assert narrow["score"] is wide["score"] is None
    sites = narrow["interaction_sites"]
    assert sites[0]["features"] == ["aromatic ring"]
    assert sites[0]["essential"] and sites[0]["weight"] == 3
    assert all(not row["essential"] and row["weight"] == 1 for row in sites[1:])
    assert sum(row["weight"] for row in sites) == 12
    current = narrow
    while current["metadata"].get("operation") == "edit_constraints":
        current = current["metadata"]["source_model"]
    assert current["metadata"]["operation"] == "extract_sites"
    assert current["metadata"]["site_map"] == [
        dict(source_site_index=index, site_index=output)
        for output, index in enumerate([9, *range(9)])
    ]
    assert current["metadata"]["source_model"] == original
    for a, b in zip(sites, wide["interaction_sites"]):
        assert a["shape"]["center"] == b["shape"]["center"]
        assert a["metadata"] == b["metadata"]
    assert (
        sites[0]["shape"]["normal"] == wide["interaction_sites"][0]["shape"]["normal"]
    )


@pytest.mark.parametrize("codec", ["json", "yaml", "sdf"])
@pytest.mark.parametrize("variant", ["narrow", "wide", "veto"])
def test_saved_hypotheses_control_matching_and_ranking(workflow, codec, variant):
    record = workflow["results"][variant + "." + codec]
    assert models_equivalent(record["native"], workflow["models"][variant])
    output = record["screening"]
    evaluations = output["evaluations"]
    expected = {
        "narrow": ["not_matched", "matched", "not_matched", "failed", "matched"],
        "wide": ["matched", "matched", "not_matched", "failed", "matched"],
        "veto": ["matched", "not_matched", "not_matched", "failed", "not_matched"],
    }[variant]
    assert [row["status"] for row in evaluations] == expected
    assert [row["input_index"] for row in evaluations] == list(range(5))
    assert [row["fit_value"] for row in evaluations] == pytest.approx(
        [0.0 if variant == "narrow" else 3 / 12, 1.0, 0.0, None, 1.0]
    )
    assert evaluations[2]["missing_essential_sites"] == [0]
    assert evaluations[3]["status"] == "failed" and evaluations[3]["fit_value"] is None
    assert "error" in evaluations[3]
    if variant == "narrow":
        assert evaluations[0]["missing_essential_sites"] == [0]
    else:
        assert not evaluations[0]["missing_essential_sites"]
        assert len(evaluations[0]["assignments"]) == 1
        assert evaluations[0]["assignments"][0]["site_index"] == 0
    if variant == "veto":
        assert evaluations[1]["excluded_volume_clashes"]
        assert not evaluations[1]["missing_essential_sites"]
        assert evaluations[1]["fit_value"] == 1  # Exclusion is independent of coverage.
    assert (
        output["hit_input_indices"]
        == {"narrow": [1, 4], "wide": [1, 4, 0], "veto": [0]}[variant]
    )
    assert output["hit_source_references_preserved"]
    assert [row["input_index"] for row in output["scalar_hits"]] == output[
        "hit_input_indices"
    ]
    assert all(row["conf_id"] == 0 for row in output["scalar_hits"])
    for row in (evaluations[0], evaluations[1], evaluations[2], evaluations[4]):
        assert row["structure_index"] == 0
        assert row["chemical_state"] == evaluations[1]["chemical_state"]
    json.dumps(evaluations, allow_nan=False)


def test_fresh_reader_preserves_detached_models_without_new_credits(workflow):
    reader = workflow["fresh_reader"]
    assert reader["attribution"]["uses"] == []
    assert len(reader["models"]) == 9
    for name, restored in reader["models"].items():
        assert models_equivalent(restored, workflow["models"][name.split(".")[0]])


def test_selected_preparation_does_not_invoke_hbond_geometry(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("This fixture selection must not request hydrogen-bond sites")

    monkeypatch.setattr(msm.physchem, "get_hbond_sites", forbidden)
    prepared = prepare_case("EST", features=FEATURES)
    assert {row["kind"] for row in prepared["inventory"]["features"]} == set(FEATURES)
