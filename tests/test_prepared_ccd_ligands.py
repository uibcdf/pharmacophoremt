"""Prepared real-chemistry controls; no biological truth or energy assertions."""

import json
from collections import Counter
from copy import deepcopy

import ackredit
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from devtools.prepared_ccd_ligands import (
    MANIFEST_PATH,
    credit_source,
    load_cases,
    motion_frames,
    prepare_case,
    state_payload,
)
from devtools.validate_prepared_ccd_ligands import (
    cross_consensus,
    prepared_screening,
    scientific_projection,
    self_recovery,
)
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_rigid_ligands
from pharmacophoremt.validation import summarize_rigid_consensus


@pytest.fixture(scope="module", params=load_cases(), ids=lambda case: case["case_id"])
def prepared(request):
    return prepare_case(request.param["case_id"])


def test_qualified_preparation_preserves_identity_and_declared_chemistry(prepared):
    report = prepared["report"]
    expected = report["source"]["expected"]
    assert report["prepared_counts"] == dict(
        n_atoms=expected["n_atoms"], n_bonds=expected["n_bonds"], n_structures=1
    )
    assert report["element_counts"]["H"] == expected["n_hydrogens"]
    assert report["feature_counts"] == expected["all_feature_counts"]
    assert report["source_atom_ids"] == report["prepared_atom_ids"]
    assert report["source_elements"] == report["prepared_elements"]
    assert 0 <= report["coordinate_rmsd_nm"] < 1e-12
    assert (
        report["source_coordinates_unchanged"]
        and report["source_state_unchanged"]
        and report["source_bytes_unchanged"]
    )
    raw, ready = [
        report[key]["states"][0] for key in ("source_state", "prepared_state")
    ]
    assert (
        raw["connectivity_completeness"]
        == ready["connectivity_completeness"]
        == "complete"
    )
    for key in ("formal_charge", "n_unpaired_electrons", "stereochemistry"):
        assert (
            raw["atom_attributes"]["columns"][key]["values"]
            == ready["atom_attributes"]["columns"][key]["values"]
        )
    for key in ("atom1_index", "atom2_index"):
        assert (
            raw["bonds"]["columns"][key]["values"]
            == ready["bonds"]["columns"][key]["values"]
        )
    for state in (raw, ready):
        assert not any(
            state["atom_attributes"]["columns"]["formal_charge"]["null_mask"]
        )
    assert all(raw["atom_attributes"]["columns"]["is_aromatic"]["null_mask"])
    assert not any(ready["atom_attributes"]["columns"]["is_aromatic"]["null_mask"])
    assert not any(ready["bonds"]["columns"]["is_aromatic"]["null_mask"])
    assert report["raw_recognition"]["status"] == "blocked"
    assert report["raw_recognition"]["code"] == "MSM-ERR-STRUCT-003"
    assert "is_aromatic" in report["raw_recognition"]["message"]
    if report["source"]["case_id"] == "EST":
        assert (
            Counter(raw["atom_attributes"]["columns"]["stereochemistry"]["values"])["S"]
            == 4
        )
    else:
        assert (
            raw["bonds"]["columns"]["stereochemistry"]["values"]
            == ready["bonds"]["columns"]["stereochemistry"]["values"]
        )
        assert "trans" in ready["bonds"]["columns"]["stereochemistry"]["values"]
    json.dumps(report, allow_nan=False)


def test_motion_frames_preserve_the_prepared_source(prepared):
    source = prepared["molecular_system"]
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    state = state_payload(source)
    frames = motion_frames(source)
    assert msm.get(frames, n_structures=True) == 2
    np.testing.assert_array_equal(
        puw.get_value(
            msm.get(frames, structure_indices=[0], coordinates=True), to_unit="nm"
        ),
        coordinates,
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), coordinates
    )
    assert state_payload(source) == state
    assert state_payload(frames) == state
    moved_rmsd = msm.structure.get_rmsd(
        frames,
        structure_indices=[1],
        selection="all",
        reference_molecular_system=source,
        reference_selection="all",
        use_gpu=False,
        parallel=False,
    )
    assert puw.get_value(moved_rmsd, to_unit="nm")[0] > 1


@pytest.mark.parametrize("policy", ["final", "each_step"])
def test_real_ligand_donor_and_aromatic_self_recovery(prepared, policy):
    result = self_recovery(prepared, policy)
    n = prepared["report"]["source"]["expected"]["search_feature_count"]
    assert result["outcome"] == dict(n_placements=1, n_fits=n - 2, max_matches=n)
    assert result["returned_pairs_valid"] and result["source_coordinates_unchanged"]
    assert len(result["pair_evaluations"]) == 1
    assert result["pair_evaluations"][0]["all_positions_valid"]
    assert result["pair_evaluations"][0]["all_orientations_valid"]
    assert result["report"]["criteria"]["orientation_policy"] == policy


@pytest.mark.parametrize("policy", ["final", "each_step"])
def test_real_ligand_public_consumer_and_frame_identity(prepared, policy):
    source = prepared["molecular_system"]
    frames = motion_frames(source)
    n = prepared["report"]["source"]["expected"]["search_feature_count"]
    result = from_rigid_ligands(
        [
            dict(ligand_id="reference", molecular_system=source),
            dict(ligand_id="moved", molecular_system=frames, structure_index=1),
        ],
        features=["hb donor", "hb acceptor", "aromatic ring"],
        correspondence_strategy="ranked_triplet_seeds",
        n_seeds=1,
        refinement_strategy="greedy",
        orientation_policy=policy,
        min_matches=n,
        min_sites=n,
        distance_tolerance=".02 nm",
        direction_tolerance="20 degrees",
    )
    summary = summarize_rigid_consensus(result["report"])
    assert summary["n_models"] == 1 and summary["max_joint_sites"] == n
    assert summary["n_fits"] == n - 2
    assert result["report"]["sources"][1]["structure_index"] == 1


@pytest.fixture(scope="module")
def ligand_pair():
    return [prepare_case(case["case_id"]) for case in load_cases()]


@pytest.mark.parametrize(
    "workload",
    json.loads(MANIFEST_PATH.read_text())["cross_workloads"],
    ids=lambda case: case["case_id"],
)
@pytest.mark.parametrize("policy", ["final", "each_step"])
def test_declared_cross_ligand_hypotheses(ligand_pair, workload, policy):
    before = [state_payload(item["molecular_system"]) for item in ligand_pair]
    result = cross_consensus(ligand_pair, workload, policy)
    assert result["outcome"] == workload["expected"][policy]
    assert result["report"]["complete"]
    assert [state_payload(item["molecular_system"]) for item in ligand_pair] == before
    json.dumps(result, allow_nan=False)


def test_source_identity_gate_rejects_changed_checksum(monkeypatch):
    import devtools.prepared_ccd_ligands as module

    cases = deepcopy(load_cases())
    cases[0]["sha256"] = "0" * 64
    monkeypatch.setattr(module, "load_cases", lambda: cases)
    with pytest.raises(ValueError, match="CCD source changed"):
        prepare_case(cases[0]["case_id"])


def test_real_prepared_frame_screening_and_retained_pose(prepared):
    result = prepared_screening(prepared)
    assert result["outcome"] == dict(
        status="matched",
        fit_value=1.0,
        best_conformer_index=1,
        n_evaluated=2,
        complete=True,
    )
    assert [frame["conformer_index"] for frame in result["result"]["conformers"]] == [
        1,
        0,
    ]
    assert all(frame["status"] == "matched" for frame in result["result"]["conformers"])
    pose = puw.QuantityRecord.from_dict(
        result["result"]["pose_coordinates"]
    ).to_quantity()
    assert puw.get_value(pose, to_unit="nm").shape == (
        1,
        prepared["report"]["source"]["expected"]["n_atoms"],
        3,
    )
    json.dumps(result, allow_nan=False)


def test_actual_resource_and_strategy_citations_are_distinct():
    with ackredit.session("prepared ligand resource control"), phmt.attribution():
        prepared = prepare_case("EST")
        credit_source("EST")
        result = self_recovery(prepared, "final")
        references = ackredit.get_attribution().to_dict()
        bibliography = ackredit.get_attribution().report(format="bibtex")
    assert result["returned_pairs_valid"]
    assert "10.1093/bioinformatics/btu789" in bibliography
    assert "10.3390/molecules26237201" in bibliography
    datasets = [item["id"] for item in references["items"] if item["type"] == "dataset"]
    assert len(datasets) == 1 and "ccd:EST:" in datasets[0]
    assert any(
        use["item_id"] == datasets[0] and use["roles"] == ["input_data"]
        for use in references["uses"]
    )
    assert any(
        use.get("context", {}).get("method") == "g3ps_refinement_final"
        for use in references["uses"]
    )
    assert any(
        item.get("title", "").lower().startswith("rdkit")
        for item in references["items"]
    )


def test_modular_workflow_scientific_fields_are_stable_with_tracking():
    outputs = []
    for enabled in (False, True):
        with (
            ackredit.session("independent step attribution"),
            phmt.attribution(enabled),
        ):
            result = self_recovery(prepare_case("EST"), "final")
            outputs.append(result)
    assert "attribution" not in outputs[0]["report"]["reference_inventory"]
    assert (
        outputs[1]["report"]["reference_inventory"]["attribution"]["status"]
        == "captured"
    )
    assert scientific_projection(outputs[0]) == scientific_projection(outputs[1])
