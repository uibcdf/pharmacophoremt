import json
from pathlib import Path

import molsysmt as msm
import pytest

import pharmacophoremt as phmt
from devtools.audit_eralpha import audit
from devtools.audit_eralpha_sources import audit as audit_sources
from pharmacophoremt._private.smonitor.exceptions import ArgumentError


def test_eralpha_pharmacophore_extraction_requires_native_observations(monkeypatch):
    """Retirement guard: #5's chemistry recovery is historical, not a fallback."""
    pdb_file = Path(__file__).parent / "data/eralpha_complex.pdb"
    assert pdb_file.is_file()

    def forbidden(*args, **kwargs):
        pytest.fail("The legacy snapshot must not trigger molecular inference")

    for name in ("convert", "select", "get"):
        monkeypatch.setattr(msm, name, forbidden)
    for selections in (
        {},
        {"ligand_selection": "group_index == 8076"},
        {
            "ligand_selection": "group_index == 8076",
            "receptor_selection": 'molecule_type == "protein"',
        },
    ):
        with pytest.raises(ArgumentError):
            phmt.model(str(pdb_file), method="complex-based", **selections)


def test_eralpha_native_input_audit():
    """The real snapshot cannot silently become a native negative or empty query."""
    manifest = json.loads(
        (Path(__file__).parent / "data/eralpha_audit.json").read_text()
    )
    report = audit()
    assert report["sha256"] == manifest["sha256"]
    assert report["counts"] == manifest["expected_counts"]
    assert report["ligand_source_atom_indices"] == list(range(27528, 27572))
    assert report["ligand_atom_names"] == manifest["ligand"]["atom_names"]
    assert report["ligand_element_counts"] == manifest["ligand"]["element_counts"]
    assert set(report["ligand_group_names"]) == {""}
    assert report["automatic_small_molecule_selection_count"] == 0
    assert report["coordinates_finite"] and report["source_unchanged"]
    assert report["provenance_status"] == "derivation_and_chemical_identity_unverified"
    for key in ("ligand", "protein"):
        for route, observation in report["parts"][key].items():
            assert observation["n_atoms"] == manifest[key]["n_atoms"]
            assert observation["n_bonds"] == manifest[key]["n_bonds"]
            assert observation["recognition_status"] == "blocked"
            assert observation["diagnostic"]["code"] == "MSM-ERR-STRUCT-003"
            assert "fit_value" not in observation and "n_features" not in observation
            if route == "native_pdb":
                assert observation["connectivity_completeness"] == "partial"
                assert observation["formal_charges"] is None
                assert all(order is None for order in observation["bond_orders"])
                assert (
                    "connectivity declared complete"
                    in observation["diagnostic"]["message"]
                )
            else:
                assert observation["connectivity_completeness"] == "complete"
                assert set(observation["bond_orders"]) == {0}
                assert (
                    "supported declared order" in observation["diagnostic"]["message"]
                )


def test_eralpha_rcsb_source_identity_and_preparation_gate():
    """Deposited provenance does not silently imply complete ligand preparation."""
    manifest = json.loads(
        (Path(__file__).parent / "data/eralpha_rcsb/manifest.json").read_text()
    )
    report = audit_sources()
    assert report["entry_id"] == "1QKU"
    assert report["checksums"] == {
        name: data["sha256"] for name, data in manifest["files"].items()
    }
    assert report["observed_revision"] == manifest["entry"]["observed_revision"]
    assert report["counts"] == manifest["expected_counts"]
    assert report["source_atom_indices"] == manifest["ligand"]["source_atom_indices"]
    assert report["ligand_atom_names"] == manifest["ligand"]["atom_names"]
    assert report["ligand_element_counts"] == {"C": 18, "O": 2}
    assert report["ligand_n_bonds_in_loaded_graph"] == 23
    assert report["author_asym_ids"] == ["A"]
    assert report["author_residue_ids"] == ["600"]
    assert report["ccd_atom_count"] == 44 and report["ccd_bond_count"] == 47
    assert report["ccd_element_counts"] == {"C": 18, "H": 24, "O": 2}
    assert report["heavy_atom_names_agree"]
    assert report["chemical_mapping_status"] == "not_validated"
    assert report["hydrogen_generation_status"] == "not_performed"
    assert report["recognition_status"] == "blocked"
    assert report["diagnostic"]["code"] == "MSM-ERR-STRUCT-003"
    assert "connectivity declared complete" in report["diagnostic"]["message"]
    assert "fit_value" not in report
    assert report["source_unchanged"] and report["files_unchanged"]
    assert report["coordinates_finite"] and report["coordinate_unit"] == "nm"
