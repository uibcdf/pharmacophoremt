"""Observed receptor geometry is usable without claiming ready receptor chemistry."""

import json

import ackredit
import pytest

import pharmacophoremt as phmt
from devtools.validate_eralpha_exclusions import valid, workflow
from devtools.validate_eralpha_template import portable
from devtools.validate_prepared_ccd_ligands import scientific_projection


@pytest.fixture(scope="module")
def observed(tmp_path_factory):
    return portable(workflow(tmp_path_factory.mktemp("observed-exclusions")))


def test_observed_receptor_sites_preserve_indices_and_unprepared_chemical_scope(
    observed,
):
    assert valid(observed)
    report = observed["construction"]["report"]
    assert report["n_sites"] == 153
    assert len(observed["receptor_group_indices"]) == 19
    assert observed["query_site_offset"] == 5
    assert all(record["atom_indices"][0] < 1990 for record in report["sites"])
    assert observed["heavy_pose_preserved"]
    assert observed["source_unchanged"] and observed["ligand_unchanged"]
    readiness = observed["receptor_chemical_readiness"]
    assert readiness["fields"]["formal_charge"]["status"] == "missing"
    assert readiness["connectivity"]["declared_completeness"] == "partial"
    assert observed["policy"]["interaction_detection"] == "not_performed"
    assert not report["policy"]["physical_radius_assignment"]
    json.dumps(observed, allow_nan=False)


def test_observed_collision_veto_preserves_full_positive_fit_and_both_index_spaces(
    observed,
):
    outcomes = observed["outcomes"]
    assert outcomes["unexcluded_collision"]["status"] == "matched"
    assert outcomes["collision"]["status"] == "not_matched"
    assert len(outcomes["collision"]["assignments"]) == 5
    assert outcomes["collision"]["fit_value"] == 1
    (clash,) = outcomes["collision"]["excluded_volume_clashes"]
    local_index = clash["site_index"] - observed["query_site_offset"]
    (source_atom,) = observed["construction"]["report"]["sites"][local_index][
        "atom_indices"
    ]
    assert (
        source_atom
        == observed["collision_targets"]["receptor_source_atom_index"]
        == 394
    )
    assert (
        clash["atom_index"] == observed["collision_targets"]["ligand_atom_index"] == 3
    )


def test_observed_radius_choice_and_query_persistence_remain_explicit(observed):
    outcomes = observed["outcomes"]
    assert outcomes["reference"]["status"] == "matched"
    assert outcomes["reference"]["excluded_volume_clashes"] == []
    assert outcomes["wide_radius_reference"]["status"] == "not_matched"
    assert len(outcomes["wide_radius_reference"]["excluded_volume_clashes"]) == 12
    assert outcomes["wide_radius_reference"]["fit_value"] == 1
    assert observed["query_metadata_preserved"]
    for original, loaded in (
        ("reference", "reloaded_reference"),
        ("collision", "reloaded_collision"),
    ):
        assert outcomes[original]["status"] == outcomes[loaded]["status"]
        assert outcomes[original]["assignments"] == outcomes[loaded]["assignments"]
        assert (
            outcomes[original]["excluded_volume_clashes"]
            == outcomes[loaded]["excluded_volume_clashes"]
        )


def test_actual_observed_credit_and_science_are_independent_of_host_tracking(
    tmp_path, observed
):
    from devtools.prepare_eralpha_ligand import credit_inputs

    with (
        ackredit.session("observed receptor geometry workflow"),
        phmt.attribution(True),
    ):
        with ackredit.capture("prepared ligand and exclusions") as capture:
            tracked = portable(workflow(tmp_path))
            credit_inputs()
    assert scientific_projection(tracked) == scientific_projection(observed)
    assert tracked["construction"]["attribution"]["status"] == "captured"
    construction_refs = tracked["construction"]["attribution"]["references"]
    assert construction_refs["items"]
    assert not any(
        use["context"].get("software") == "molsysmt"
        for use in construction_refs["uses"]
    )
    refs = capture.attribution.to_dict()
    assert len([item for item in refs["items"] if item["type"] == "dataset"]) == 3
    assert not any(
        item.get("doi") == "10.3390/molecules26237201" for item in refs["items"]
    )
    assert "1QKU" in ackredit.Attribution.from_dict(refs).report(format="bibtex")
