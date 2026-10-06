"""Keep measured receptor coverage distinct from successful interaction science."""

import json

import ackredit
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from devtools.audit_eralpha_receptor import audit
from devtools.prepare_eralpha_ligand import SOURCES, credit_inputs
from devtools.prepared_ccd_ligands import state_payload
from devtools.validate_eralpha_template import portable
from devtools.validate_prepared_ccd_ligands import scientific_projection
from pharmacophoremt import pyunitwizard as puw


@pytest.fixture(scope="module")
def audited():
    source = msm.convert(str(SOURCES / "1qku.cif"), to_form="molsysmt.MolSys")
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    state = state_payload(source)
    return source, portable(audit(source)), coordinates, state


def test_receptor_scope_uses_label_chain_a_with_source_indices(audited):
    _, report, _, _ = audited
    assert report["source"]["counts"] == dict(
        n_atoms=6596, n_groups=1343, n_structures=1
    )
    assert report["source"]["deposited_label_to_author_chains"]["A"] == ["A"]
    assert report["source"]["deposited_label_to_author_chains"]["D"] == ["A"]
    assert report["ligand_source_atom_indices"] == list(range(5940, 5960))
    assert report["receptor_coverage"]["group_indices"] == list(range(250))
    atoms = report["receptor_coverage"]["chemical_readiness"]["atom_indices"]
    assert atoms == list(range(1990))
    assert set(atoms).isdisjoint(report["ligand_source_atom_indices"])
    assert report["policy"]["waters"] == "excluded"
    assert report["policy"]["bioassembly"] == "not_constructed"


def test_heavy_atom_gaps_are_outside_the_observed_ligand_shells(audited):
    _, report, _, _ = audited
    coverage = report["receptor_coverage"]
    assert coverage["summary"] == dict(assessed=247, incomplete=3, unassessed=0)
    gaps = [group for group in coverage["groups"] if group["status"] == "incomplete"]
    assert [
        (g["group_id"], g["group_name"], g["heavy_atoms"]["missing_atom_names"])
        for g in gaps
    ] == [
        ("301", "SER", ["OG"]),
        ("302", "LYS", ["CD", "CE", "CG", "NZ"]),
        ("303", "LYS", ["CD", "CE", "CG", "NZ"]),
    ]
    gap_indices = {g["group_index"] for g in gaps}
    for shell in report["shells"].values():
        assert gap_indices.isdisjoint(shell["coverage"]["group_indices"])
        assert shell["coverage"]["summary"]["incomplete"] == 0


def test_shell_sensitivity_and_independent_central_residue_identities(audited):
    _, report, _, _ = audited
    shells = [s["coverage"] for s in report["shells"].values()]
    assert [len(s["groups"]) for s in shells] == [12, 19, 23]
    assert set(shells[0]["group_indices"]) < set(shells[1]["group_indices"])
    assert set(shells[1]["group_indices"]) < set(shells[2]["group_indices"])
    central = {(g["group_name"], g["group_id"]) for g in shells[1]["groups"]}
    assert {("GLU", "353"), ("ARG", "394"), ("HIS", "524")} <= central
    assert all(
        "without pbc" in s["spatial_selection"] for s in report["shells"].values()
    )


def test_complete_heavy_inventory_does_not_certify_chemical_readiness(audited):
    _, report, _, _ = audited
    shell = report["shells"]["0.5 nm"]["coverage"]
    readiness = shell["chemical_readiness"]
    assert readiness["connectivity"]["declared_completeness"] == "partial"
    assert readiness["explicit_hydrogen_atom_indices"] == []
    for field in ("formal_charge", "atom_is_aromatic", "n_explicit_hydrogens"):
        assert readiness["fields"][field]["status"] == "missing"
    assert all(
        g["connectivity"]["bond_order"]["status"] == "unassessed"
        for g in shell["groups"]
    )
    assert all(g["protonation"]["status"] == "unassessed" for g in shell["groups"])
    assert "valence" in readiness["unassessed_checks"]
    assert "conformer_quality" in readiness["unassessed_checks"]
    assert report["policy"]["sequence_completeness"] == "not_assessed"
    assert not report["policy"]["generated_ligand_reinserted"]
    assert report["raw_ligand_readiness"]["explicit_hydrogen_atom_indices"] == []


def test_blocked_detectors_are_not_evaluated_empty_or_negative(audited):
    _, report, _, _ = audited
    assert len(report["attempts"]) == 3
    for attempt in report["attempts"].values():
        assert attempt["status"] == "blocked"
        assert attempt["diagnostic"]["code"] == "MSM-ERR-STRUCT-003"
        assert attempt["n_observations"] is None
        assert "result" not in attempt
    assert not report["policy"]["assumption_of_complete_connectivity"]
    json.dumps(report, allow_nan=False)


def test_audit_preserves_original_coordinates_and_chemical_payload(audited):
    source, report, coordinates, state = audited
    assert report["source_unchanged"] and report["before"] == report["after"]
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), coordinates
    )
    assert state_payload(source) == state


def test_actual_credit_only_names_used_observed_data_and_preserves_science(audited):
    source, original, _, _ = audited
    with ackredit.session("receptor gate consumer control"), phmt.attribution(True):
        with ackredit.capture(
            "audit without completed interaction calculation"
        ) as capture:
            result = portable(audit(source))
            credit_inputs(roles=("observed",))
        references = capture.attribution.to_dict()
    assert scientific_projection(original) == scientific_projection(result)
    assert len(references["items"]) == 1
    assert references["items"][0]["type"] == "dataset"
    assert "deposited asymmetric unit" in references["items"][0]["title"]
    assert all(use["roles"] == ["input_data"] for use in references["uses"])
    assert "1QKU" in ackredit.Attribution.from_dict(references).report(format="bibtex")
    with pytest.raises(ValueError, match="Unknown ERalpha input role"):
        credit_inputs(roles=("unexecuted",))


def test_explicit_nm_shells_preserve_scope_under_nondefault_units(audited):
    source, original, _, _ = audited
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        result = portable(audit(source))
    for radius in original["shells"]:
        assert (
            result["shells"][radius]["coverage"]["group_indices"]
            == (original["shells"][radius]["coverage"]["group_indices"])
        )
    assert result["source_unchanged"]
