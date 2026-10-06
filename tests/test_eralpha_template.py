"""Observed-pose consumer controls for the provider's curated EST template."""

import json
from copy import deepcopy

import ackredit
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from devtools.prepare_eralpha_ligand import (
    TEMPLATES,
    credit_inputs,
    load_manifest,
    prepare_case,
)
from devtools.prepared_ccd_ligands import state_payload
from devtools.validate_eralpha_template import placed_controls, portable, valid_controls
from devtools.validate_prepared_ccd_ligands import scientific_projection
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import get_features


@pytest.fixture(scope="module")
def prepared():
    return prepare_case()


def test_template_transfer_retains_observed_identity_pose_and_explicit_state(prepared):
    report = portable(prepared["report"])
    assert report["assessment"]["status"] == "compatible"
    assert report["application"]["status"] == "applied"
    assert report["raw_recognition"]["status"] == "blocked"
    assert report["raw_recognition"]["code"] == "MSM-ERR-STRUCT-003"
    assert report["source_atom_indices"] == list(range(5940, 5960))
    assert report["source_atom_names"] == report["manifest"]["source_atom_names"]
    assert report["source_atom_ids"] == report["prepared_atom_ids"]
    assert report["pose_preserved"] and report["source_unchanged"]
    assert report["prepared_counts"] == dict(n_atoms=20, n_bonds=23, n_structures=1)
    assert report["feature_counts"] == {
        "hydrophobicity": 9,
        "hb acceptor": 2,
        "aromatic ring": 1,
    }
    state = report["prepared_state"]["states"][0]
    assert state["connectivity_completeness"] == "complete"
    columns = state["atom_attributes"]["columns"]
    assert columns["formal_charge"]["values"] == [0] * 20
    assert columns["stereochemistry"]["values"] == [
        report["manifest"]["expected_stereo"][name] or ""
        for name in report["source_atom_names"]
    ]
    assert columns["stereochemistry"]["values"][8] == "R"
    assert (
        sum(columns["n_implicit_hydrogens"]["values"])
        + sum(columns["n_explicit_hydrogens"]["values"])
        == 24
    )
    assert (
        report["source_ligand_state"]["states"][0]["connectivity_completeness"]
        == "partial"
    )
    json.dumps(report, allow_nan=False)


def test_stored_hydrogens_do_not_become_directional_donor_geometry(prepared):
    inventory = get_features(prepared["molecular_system"], features=["hb donor"])
    assert inventory["features"] == []
    assert (
        inventory["recognition"]["hydrogen_bond"]["hydrogen_policy"]
        == "indexed_atoms_only"
    )
    assert inventory["recognition"]["hydrogen_bond"]["donor_hydrogen_pairs"] == []
    assert (
        prepared["report"]["readiness"]["directional_donors"]
        == "pending_explicit_hydrogen_coordinates"
    )


def test_placed_geometry_and_two_format_roundtrips(prepared, tmp_path):
    before = puw.get_value(
        msm.get(prepared["molecular_system"], coordinates=True), to_unit="nm"
    ).copy()
    result = placed_controls(prepared, tmp_path)
    assert valid_controls(result)
    assert result["displaced_negative"]["fit_value"] == 0
    assert result["orthogonal_normal_negative"]["fit_value"] == pytest.approx(2 / 3)
    assert len(result["positive"]["assignments"]) == 3
    np.testing.assert_array_equal(
        before,
        puw.get_value(
            msm.get(prepared["molecular_system"], coordinates=True), to_unit="nm"
        ),
    )


@pytest.mark.parametrize("malformed", [False, True])
def test_bad_correspondence_fails_without_modifying_source(prepared, malformed):
    source = prepared["ligand"]
    before = state_payload(source)
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    manifest = load_manifest()
    mapping = deepcopy(manifest["atom_correspondence"])
    if malformed:
        mapping.pop()
        error_type = msm.ArgumentError
    else:
        mapping[0][1], mapping[3][1] = mapping[3][1], mapping[0][1]
        error_type = msm.StructuralInconsistencyError
    with pytest.raises(error_type) as caught:
        msm.physchem.apply_chemical_template(
            source,
            template=TEMPLATES / "est_template.h5msm",
            atom_correspondence=mapping,
            template_provenance=manifest["template_provenance"],
        )
    if not malformed:
        assert caught.value.report["status"] == "conflict"
    assert state_payload(source) == before
    np.testing.assert_array_equal(
        coordinates, puw.get_value(msm.get(source, coordinates=True), to_unit="nm")
    )


def test_artifact_checksum_gate_precedes_molecular_work(monkeypatch, tmp_path):
    import devtools.prepare_eralpha_ligand as client

    for name in ("manifest.json", "acquisition.json", "est_template.h5msm"):
        (tmp_path / name).write_bytes((TEMPLATES / name).read_bytes())
    with (tmp_path / "est_template.h5msm").open("ab") as stream:
        stream.write(b"changed")
    monkeypatch.setattr(client, "TEMPLATES", tmp_path)
    with pytest.raises(ValueError, match="artifact changed"):
        client.load_manifest()


def test_nondefault_units_preserve_template_pose_and_feature_centers(prepared):
    manifest = load_manifest()
    with puw.context(standard_units=["pm", "fs"]):
        applied = msm.physchem.apply_chemical_template(
            prepared["ligand"],
            template=TEMPLATES / "est_template.h5msm",
            atom_correspondence=manifest["atom_correspondence"],
            template_provenance=manifest["template_provenance"],
        )
        inventory = get_features(applied["molecular_system"])
    assert [r["kind"] for r in inventory["features"]] == [
        r["kind"] for r in prepared["inventory"]["features"]
    ]
    for actual, expected in zip(
        inventory["features"], prepared["inventory"]["features"]
    ):
        np.testing.assert_allclose(
            puw.get_value(actual["center"], to_unit="nm"),
            puw.get_value(expected["center"], to_unit="nm"),
            atol=1e-14,
        )


def test_actual_workflow_credit_and_science_independent_of_host_tracking(tmp_path):
    observations = []
    for enabled in (False, True):
        with ackredit.session("EST consumer credit control"), phmt.attribution(enabled):
            case = prepare_case()
            if enabled:
                credit_inputs()
            directory = tmp_path / str(enabled)
            directory.mkdir()
            result = placed_controls(case, directory)
            observations.append(scientific_projection(portable(result)))
            references = ackredit.get_attribution().to_dict()
            if enabled:
                assert result["positive"]["attribution"]["status"] == "captured"
                assert case["report"]["application"]["attribution"]["items"]
    assert observations[0] == observations[1]
    datasets = [item for item in references["items"] if item["type"] == "dataset"]
    assert len(datasets) == 3
    assert any("deposited" in item["title"] for item in datasets)
    assert any("curated" in item["title"] for item in datasets)
    assert not any(
        item.get("doi") == "10.3390/molecules26237201" for item in references["items"]
    )
    saved = ackredit.Attribution.from_dict(references)
    assert "1QKU" in saved.report(format="bibtex")
