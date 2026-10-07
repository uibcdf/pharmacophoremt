"""Declared prepared fragment -> observed/reference model -> independent controls."""

import json
import subprocess
import sys

import ackredit
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from devtools.prepare_eralpha_interface import prepare_interface
from devtools.prepare_eralpha_ligand import credit_inputs
from devtools.validate_eralpha_interface import build_hypothesis, controls, valid
from devtools.validate_prepared_ccd_ligands import scientific_projection
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.io import load_json


@pytest.fixture(scope="module")
def interface(tmp_path_factory):
    directory = tmp_path_factory.mktemp("eralpha-interface")
    with phmt.attribution(False):
        case = prepare_interface()
        run = controls(case, directory)
    return case, run, directory


def test_closed_fragment_states_and_source_maps_are_explicit(interface):
    case, run, _ = interface
    preparation = run["preparation"]
    declaration = preparation["declaration"]
    assert preparation["receptor_group_ids"] == list(range(304, 551))
    assert declaration["excluded_source_group_ids"] == ["301", "302", "303"]
    assert declaration["residue_states"] == {"HIS": "HIE"}
    assert (
        preparation["receptor_template"]["template_provenance"]["n_terminal_state"]
        == "ammonium"
    )
    assert (
        preparation["receptor_template"]["template_provenance"]["c_terminal_state"]
        == "carboxylate"
    )
    assert preparation["prepared_counts"] == dict(
        n_atoms=4047, n_bonds=4088, n_structures=1
    )
    mapping = np.asarray(preparation["atom_source_indices"])
    assert np.count_nonzero(mapping >= 0) == 1995
    assert np.count_nonzero(mapping == -1) == 2052
    assert len(set(mapping[mapping >= 0])) == 1995
    assert mapping[case["ligand"]][:20].tolist() == list(range(5940, 5960))
    assert preparation["observed_identity_and_coordinates_preserved"]
    assert preparation["source_unchanged"] and run["prepared_input_unchanged"]
    assert not preparation["full_receptor_acceptance"]
    assert preparation["environmental_refinement"] == "not_performed"


def test_evaluated_empty_families_are_retained_as_observations(interface):
    case, run, _ = interface
    assert {
        label: value.n_interactions for label, value in case["analyses"].items()
    } == {
        "hydrophobic": 12,
        "hbonds": 0,
        "pi_pi": 0,
    }
    assert run["site_counts"] == dict(observed=6, reference=5, combined=11, curated=11)
    for observed in run["observations"]["analyses"]:
        assert observed["evaluated_structure_indices"] == [0]
    for analysis in case["analyses"].values():
        assert analysis.source_id == "rcsb:1QKU:deposited-atom-order"
        assert (
            analysis.atom_source_indices.tolist()
            == run["preparation"]["atom_source_indices"]
        )
    assert (
        run["preparation"]["observations"]["hbonds"]["parameters"]["method"]
        == "donor_acceptor_distance_angle"
    )
    # Frozen deposited participants and direct coordinate arithmetic form an
    # independent geometry oracle; model self-placement alone cannot prove them.
    expected_pairs = np.asarray(
        run["preparation"]["declaration"]["expected_hydrophobic_source_pairs"]
    )
    payload = msm.convert(
        case["analyses"]["hydrophobic"], to_form="molsysmt.InteractionsDict"
    ).data
    actual_pairs = payload["atom_source_indices"][payload["participant_atoms"]].reshape(
        -1, 2
    )
    np.testing.assert_array_equal(actual_pairs, expected_pairs)
    coordinates = puw.get_value(
        msm.get(case["source"], coordinates=True), to_unit="nm"
    )[0]
    distances = np.linalg.norm(
        coordinates[expected_pairs[:, 0]] - coordinates[expected_pairs[:, 1]], axis=1
    )
    assert payload["measure_units"]["distance"] == "nm"
    np.testing.assert_allclose(
        payload["measurements"]["distance"], distances, atol=1e-12, rtol=0
    )
    assert np.all(distances <= 0.45)


def test_reference_sites_and_declared_weights_are_distinct_from_contacts(interface):
    case, _, _ = interface
    models = build_hypothesis(case)
    assert all(site.weight == 1 for site in models["combined"].interaction_sites)
    weights = [site.weight for site in models["curated"].interaction_sites]
    assert weights == [0.5] * 6 + [1.0] * 5
    assert all(site.essential for site in models["curated"].interaction_sites)
    assert (
        models["curated"].metadata["case_scope"][
            "reference_sites_are_receptor_observations"
        ]
        is False
    )
    assert [site.features for site in models["reference"].interaction_sites].count(
        ["hb donor"]
    ) == 2
    assert [site.features for site in models["reference"].interaction_sites].count(
        ["hb acceptor"]
    ) == 2


def test_reference_displacement_and_independent_orientation_controls(interface):
    _, run, _ = interface
    outcomes = run["outcomes"]
    assert outcomes["reference"]["status"] == "matched"
    assert outcomes["reference"]["fit_value"] == 1
    assert len(outcomes["reference"]["assignments"]) == 11
    assert outcomes["displaced_negative"]["status"] == "not_matched"
    assert outcomes["displaced_negative"]["fit_value"] == 0
    assert outcomes["reversed_normal"]["status"] == "matched"
    for label in ("reversed_donor_direction", "orthogonal_normal_negative"):
        assert outcomes[label]["status"] == "not_matched"
        assert outcomes[label]["fit_value"] == pytest.approx(7 / 8)
        assert len(outcomes[label]["missing_essential_sites"]) == 1


def test_receptor_exclusion_veto_is_independent_of_positive_fit(interface):
    _, run, _ = interface
    excluded = run["exclusions"]
    assert excluded["n_sites"] == 153
    assert len(excluded["observed_shell_group_ids"]) == 19
    assert excluded["collision_receptor_source_atom_index"] == 394
    assert excluded["collision_ligand_source_atom_index"] == 5943
    assert excluded["outcomes"]["reference"]["status"] == "matched"
    assert excluded["outcomes"]["unexcluded_collision"]["status"] == "matched"
    collision = excluded["outcomes"]["collision"]
    assert collision["status"] == "not_matched" and collision["excluded_volume_clashes"]
    assert all(value["fit_value"] == 1 for value in excluded["outcomes"].values())


def test_native_history_unknowns_maps_and_units_survive_saved_readers(interface):
    case, run, directory = interface
    assert all(run["persistence"].values())
    loaded = msm.convert(
        directory / "prepared_interface.h5msm", to_form="molsysmt.MolSys"
    )
    native = loaded.chemical_states.get_preparation_history()
    normalization = next(
        record["report"]
        for record in native
        if record["report"]["schema"] == "molsysmt.aromatic_bond_normalization@1"
    )
    original = next(
        record["report"]
        for record in case["molecular_system"].chemical_states.get_preparation_history()
        if record["report"]["schema"] == "molsysmt.aromatic_bond_normalization@1"
    )
    assert np.isnan(normalization["original_fractional_bond_orders"]).any()
    assert (
        normalization["original_fractional_bond_orders"].dtype
        == original["original_fractional_bond_orders"].dtype
    )
    np.testing.assert_array_equal(
        normalization["original_fractional_bond_orders"],
        original["original_fractional_bond_orders"],
    )
    for label in ("nondefault_units", "reloaded", "reloaded_observed_only"):
        assert run["outcomes"][label]["status"] == "matched"
        assert run["outcomes"][label]["fit_value"] == 1
        for assignment in run["outcomes"][label]["assignments"]:
            distance = puw.QuantityRecord.from_dict(
                assignment["distance"]
            ).to_quantity()
            assert puw.get_value(distance, to_unit="nm") == pytest.approx(0)
    assert valid(run)


def test_tracking_independent_science_and_detached_fresh_reader(interface, tmp_path):
    case, plain, _ = interface
    with ackredit.session("prepared-interface consumer"), phmt.attribution(True):
        with ackredit.capture("prepared molecular interface and hypothesis") as capture:
            tracked = controls(case, tmp_path)
            credit_inputs()
        refs = capture.attribution.to_dict()
    assert scientific_projection(tracked) == scientific_projection(plain)
    assert tracked["outcomes"]["reference"]["attribution"]["status"] == "captured"
    assert "1QKU" in ackredit.Attribution.from_dict(refs).report(format="bibtex")
    saved = load_json(tmp_path / "query.json").metadata["attribution"]
    references = tmp_path / "references.json"
    references.write_text(json.dumps(saved["references"]))
    script = """
import json,sys
import ackredit as ack
from pharmacophoremt.io import load_json
with ack.session('fresh reader'):
    model = load_json(sys.argv[1])
    expected = json.load(open(sys.argv[2]))
    assert model.metadata['attribution']['references'] == expected
    assert ack.Attribution.from_dict(expected).report(format='bibtex')
    assert ack.get_attribution().to_dict()['items'] == []
"""
    result = subprocess.run(
        [sys.executable, "-c", script, str(tmp_path / "query.json"), str(references)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
