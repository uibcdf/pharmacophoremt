"""Donor-inclusive consumer acceptance of MolSysMT's fixed-state EST route."""

import json

import ackredit
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from devtools.prepare_eralpha_hydrogens import SELECTED_FEATURES, add_hydrogens
from devtools.prepare_eralpha_ligand import credit_inputs, prepare_case
from devtools.prepared_ccd_ligands import motion_frames, state_payload
from devtools.validate_eralpha_hydrogens import donor_controls
from devtools.validate_eralpha_template import placed_controls, portable, valid_controls
from devtools.validate_prepared_ccd_ligands import scientific_projection, self_recovery
from pharmacophoremt import pyunitwizard as puw


@pytest.fixture(scope="module")
def prepared():
    return add_hydrogens(prepare_case())


def test_declared_inventory_becomes_atoms_with_old_and_parent_maps(prepared):
    report = portable(prepared["report"])
    addition = report["hydrogen_addition"]
    assert addition["status"] == "added" and addition["n_added_hydrogens"] == 24
    assert (
        addition["method"] == "local_hydrogen_placement"
        and addition["engine"] == "RDKit"
    )
    assert addition["parameters"] == dict(addCoords=True, pH=None, optimize=False)
    assert report["prepared_counts"] == dict(n_atoms=44, n_bonds=47, n_structures=1)
    assert addition["atom_correspondence"] == [[i, i] for i in range(20)]
    pairs = np.asarray(addition["parent_hydrogen_pairs"])
    assert pairs.shape == (24, 2)
    assert sorted(pairs[:, 1]) == list(range(20, 44))
    assert (
        np.bincount(pairs[:, 0], minlength=20).tolist()
        == report["template_preparation"]["manifest"]["expected_hydrogen_counts"]
    )
    assert report["inventory_after"]["status"] == "available"
    assert report["inventory_after"]["missing_hydrogen_counts"] == [0] * 44
    assert report["prepared_atom_ids"][:20] == report["original_atom_ids"]
    assert len(set(addition["generated_atom_ids"])) == 24
    assert report["source_atom_indices"] == list(range(5940, 5960))
    assert addition["dropped_attributes"] == ["b_factor"]
    json.dumps(report, allow_nan=False)


def test_observed_pose_stereo_charge_and_generated_bond_geometry(prepared):
    report = portable(prepared["report"])
    expected = [
        report["template_preparation"]["manifest"]["expected_stereo"][name]
        for name in report["template_preparation"]["source_atom_names"]
    ]
    assert report["cip_declared"]["atom_stereochemistry"][:20] == expected
    assert report["cip_from_coordinates"]["atom_stereochemistry"][:20] == expected
    assert expected[8] == "R"
    assert report["heavy_coordinates_preserved"] and report["input_unchanged"]
    assert report["readiness"]["environment_refinement"] == "not_performed"
    columns = report["prepared_state"]["states"][0]["atom_attributes"]["columns"]
    assert columns["formal_charge"]["values"] == [0] * 44
    assert columns["n_implicit_hydrogens"]["values"] == [0] * 44
    assert columns["n_explicit_hydrogens"]["values"] == [0] * 44
    pairs = np.asarray(report["hydrogen_addition"]["parent_hydrogen_pairs"])
    lengths = puw.QuantityRecord.from_dict(report["added_bond_lengths"]).to_quantity()
    values = puw.get_value(lengths, to_unit="nm").reshape(-1)
    oxygen = np.isin(pairs[:, 0], [3, 18])
    assert np.all((values[oxygen] > 0.09) & (values[oxygen] < 0.105))
    assert np.all((values[~oxygen] > 0.10) & (values[~oxygen] < 0.115))


def test_actual_oxygen_donor_hydrogen_geometry_is_distinct_from_stored_counts(prepared):
    assert prepared["report"]["feature_counts"] == {
        "hydrophobicity": 9,
        "hb donor": 2,
        "hb acceptor": 2,
        "aromatic ring": 1,
    }
    pairs = prepared["inventory"]["recognition"]["hydrogen_bond"][
        "donor_hydrogen_pairs"
    ]
    assert pairs == [[3, 22], [18, 40]]
    donors = [
        record
        for record in prepared["inventory"]["features"]
        if record["kind"] == "hb donor"
    ]
    for record in donors:
        assert puw.get_value(record["direction"], to_unit="dimensionless").shape == (3,)
        assert np.linalg.norm(
            puw.get_value(record["direction"], to_unit="dimensionless")
        ) == pytest.approx(1)


def test_five_essential_sites_direction_negatives_and_persistence(prepared, tmp_path):
    placed = placed_controls(prepared, tmp_path, features=SELECTED_FEATURES)
    assert valid_controls(placed, n_sites=5)
    assert len(placed["positive"]["assignments"]) == 5
    assert placed["orthogonal_normal_negative"]["fit_value"] == pytest.approx(0.8)
    donors = donor_controls(prepared)
    assert donors["heavy_only"]["status"] == "not_matched"
    assert donors["heavy_only"]["fit_value"] == pytest.approx(0.6)
    assert len(donors["heavy_only"]["missing_essential_sites"]) == 2
    assert donors["reversed_donor_direction"]["status"] == "not_matched"
    assert donors["reversed_donor_direction"]["fit_value"] == pytest.approx(0.8)


def test_second_hydrogen_addition_is_an_unchanged_independent_copy(prepared):
    source = prepared["molecular_system"]
    original_payload = state_payload(source)
    before_history = portable(source.chemical_states.get_preparation_history())
    repeated = msm.build.add_missing_hydrogens(
        source, mode="fixed_chemical_state", pH=None, engine="RDKit", return_report=True
    )
    assert repeated["molecular_system"] is not source
    assert repeated["report"]["status"] == "unchanged"
    assert repeated["report"]["n_added_hydrogens"] == 0
    assert repeated["report"]["parent_hydrogen_pairs"].shape == (0, 2)
    actual, expected = (
        state_payload(repeated["molecular_system"]),
        state_payload(source),
    )
    for state in actual["states"] + expected["states"]:
        state.pop("preparation_history", None)
    assert actual == expected
    assert state_payload(source) == original_payload
    after_history = repeated[
        "molecular_system"
    ].chemical_states.get_preparation_history()
    assert portable(after_history[: len(before_history)]) == portable(before_history)
    appended = after_history[len(before_history) :]
    assert [record["report"]["schema"] for record in appended] == [
        "molsysmt.terminal_attachment@1",
        "molsysmt.hydrogen_addition@1",
    ]
    assert all(record["report"]["status"] == "unchanged" for record in appended)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"),
        puw.get_value(
            msm.get(repeated["molecular_system"], coordinates=True), to_unit="nm"
        ),
    )


def test_strict_annotation_policy_rejects_without_changing_heavy_source(prepared):
    source = prepared["heavy_case"]["molecular_system"]
    before_state = state_payload(source)
    before_coordinates = puw.get_value(
        msm.get(source, coordinates=True), to_unit="nm"
    ).copy()
    before_bfactor = puw.get_value(
        msm.get(source, b_factor=True), to_unit="nm**2"
    ).copy()
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.build.add_missing_hydrogens(
            source,
            mode="fixed_chemical_state",
            pH=None,
            engine="RDKit",
            attribute_policy="strict",
        )
    assert state_payload(source) == before_state
    np.testing.assert_array_equal(
        before_coordinates,
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"),
    )
    np.testing.assert_array_equal(
        before_bfactor, puw.get_value(msm.get(source, b_factor=True), to_unit="nm**2")
    )


def test_nondefault_units_do_not_change_declared_state_or_observed_pose(prepared):
    with puw.context(standard_units=["pm", "fs"]):
        result = add_hydrogens(prepared["heavy_case"])
    assert (
        result["report"]["heavy_coordinates_preserved"]
        and result["report"]["input_unchanged"]
    )
    assert state_payload(result["molecular_system"]) == state_payload(
        prepared["molecular_system"]
    )
    np.testing.assert_allclose(
        puw.get_value(
            msm.get(result["molecular_system"], coordinates=True), to_unit="nm"
        ),
        puw.get_value(
            msm.get(prepared["molecular_system"], coordinates=True), to_unit="nm"
        ),
        atol=1e-14,
    )


@pytest.mark.parametrize("policy", ["final", "each_step"])
def test_rigid_recovery_preserves_all_five_directional_features(prepared, policy):
    result = self_recovery(prepared, policy)
    assert result["outcome"] == dict(n_placements=1, n_fits=3, max_matches=5)
    assert result["returned_pairs_valid"] and result["source_coordinates_unchanged"]
    assert result["proposals"]["correspondences"] == [[[0, 0], [1, 1], [4, 4]]]


def test_motion_control_keeps_source_box_and_does_not_invent_original_frame_ids(
    prepared,
):
    source = prepared["molecular_system"]
    original_box = msm.get(source, box=True)
    original_ids = msm.get(source, structure_id=True)
    frames = motion_frames(source)
    assert msm.get(frames, n_structures=True) == 2
    for index in (0, 1):
        np.testing.assert_array_equal(
            puw.get_value(
                msm.get(frames, box=True, structure_indices=[index]), to_unit="nm"
            ),
            puw.get_value(original_box, to_unit="nm"),
        )
    if original_ids is None:
        assert msm.get(frames, structure_id=True) is None
    np.testing.assert_array_equal(
        puw.get_value(
            msm.get(frames, coordinates=True, structure_indices=[0]), to_unit="nm"
        ),
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"),
    )


def test_actual_hydrogen_method_capture_with_host_tracking_enabled_and_disabled(
    tmp_path,
):
    observations = []
    for enabled in (False, True):
        with ackredit.session("EST H preparation consumer"), phmt.attribution(enabled):
            with ackredit.capture("fixed-state ligand H") as capture:
                case = add_hydrogens(prepare_case())
                if enabled:
                    credit_inputs()
                directory = tmp_path / str(enabled)
                directory.mkdir()
                placed = placed_controls(case, directory, features=SELECTED_FEATURES)
            references = capture.attribution.to_dict()
            observations.append(
                scientific_projection(
                    portable(dict(preparation=case["report"], placed=placed))
                )
            )
    assert observations[0] == observations[1]
    method = case["report"]["hydrogen_addition"]["references"][0]["id"]
    assert method in {item["id"] for item in references["items"]}
    assert any(
        use["item_id"] == method
        and use["used_by"] == "molsysmt.build.add_missing_hydrogens"
        for use in references["uses"]
    )
    assert len([item for item in references["items"] if item["type"] == "dataset"]) == 3
    assert not any(
        item.get("doi") == "10.3390/molecules26237201" for item in references["items"]
    )
    assert "RDKit" in ackredit.Attribution.from_dict(references).report(format="bibtex")
