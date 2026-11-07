"""Fresh/reused native subworkflow controls; no library or performance claim."""

import json
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError, CliqueLimitError
from pharmacophoremt.modeler import get_features
from phmt_test_support.absence_inputs import (
    COORDINATES,
    FAMILIES,
    SMILES,
    moved,
    system,
)
from phmt_test_support.feature_reuse_experiment import compare_feature_reuse

IONS = "[Na+].[K+].[Li+]"
ION_COORDINATES = np.array([[0.0, 0, 0], [0.3, 0, 0], [0, 0.5, 0]])
ION_FEATURES = ("positive charge",)


def ion_inventory(coordinates=ION_COORDINATES):
    return get_features(
        system(IONS, coordinates), features=ION_FEATURES, chemical_state=0
    )


def references():
    return [
        dict(key="native-triangle", inventory=ion_inventory()),
        dict(
            key="changed-internal-distances",
            inventory=ion_inventory(ION_COORDINATES * [2, 1, 1]),
        ),
    ]


def compare(source, queries, **options):
    return compare_feature_reuse(
        source,
        queries,
        features=ION_FEATURES,
        distance_tolerance="0.02 nm",
        **options,
    )


def test_two_distinct_queries_preserve_full_native_evidence_and_rigid_positive():
    source = moved(system(IONS, ION_COORDINATES))
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    queries = references()
    query_before = deepcopy(queries)
    result = compare(source, queries)
    positive, empty = result["comparisons"]
    assert positive["native_evidence_equal"] and empty["native_evidence_equal"]
    assert positive["proposed_mappings"] >= 1
    assert len(positive["fresh"]["native_evaluations"]) == 1
    evaluation = positive["fresh"]["native_evaluations"][0]
    assert evaluation["native_result"]["status"] == "matched"
    assert evaluation["ranking_score"] == 1.0
    assert evaluation["score_method"] == "checked_pose_coverage@1"
    assert empty["proposed_mappings"] == empty["selected_mappings"] == 0
    assert empty["fresh"]["proposals"]["complete"]
    assert empty["fresh"]["native_evaluations"] == []
    assert "ranking_score" not in empty  # No fitted-pose absence becomes a score.
    assert result["outer_extraction_requests"]["reused"] == 1
    assert result["outer_extraction_requests"]["fresh"] == 2
    assert not result["performance_claim"]
    assert not result["full_rigid_search_equivalence"]
    for original, saved in zip(queries, query_before, strict=True):
        for record, expected in zip(
            original["inventory"]["features"],
            saved["inventory"]["features"],
            strict=True,
        ):
            np.testing.assert_array_equal(
                puw.get_value(record["center"], to_unit="nm"),
                puw.get_value(expected["center"], to_unit="nm"),
            )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )
    json.dumps(result, allow_nan=False)


def test_selected_mapping_prefix_is_separate_from_complete_proposal_family():
    coordinates = np.array([[0, 0, 0], [0.3, 0, 0], [0.15, np.sqrt(3) * 0.15, 0]])
    query = dict(key="symmetric-triangle", inventory=ion_inventory(coordinates))
    result = compare(system(IONS, coordinates), [query], max_placements=1)
    observed = result["comparisons"][0]
    assert observed["fresh"]["proposals"]["complete"]
    assert observed["proposed_mappings"] > observed["selected_mappings"] == 1
    assert observed["omitted_mappings"] == observed["proposed_mappings"] - 1
    assert observed["placement_coverage"] == "selected_prefix_only"
    assert observed["fresh"]["placement_report"]["n_fits"] == 1
    assert observed["fresh"]["placement_report"]["complete"]


def test_directed_donor_geometry_is_reextracted_and_verified_after_rigid_fit():
    reference = system(SMILES, COORDINATES)
    inventory = get_features(reference, features=FAMILIES, chemical_state=0)
    source = moved(reference)
    result = compare_feature_reuse(
        source,
        [dict(key="directed-native-query", inventory=inventory)],
        features=FAMILIES,
        distance_tolerance="0.02 nm",
        min_matches=len(inventory["features"]),
    )
    comparison = result["comparisons"][0]
    assert comparison["native_evidence_equal"]
    assert comparison["fresh"]["native_evaluations"][0]["ranking_score"] == 1.0
    accepted = comparison["fresh"]["placement_report"]["accepted_placements"][0]
    donor_records = [
        record
        for record in accepted["inventory"]["features"]
        if record["kind"] == "hb donor"
    ]
    assert donor_records and all(
        record["direction"] is not None for record in donor_records
    )
    assert result["source_coordinates_unchanged"]


def test_zero_feature_source_retains_empty_native_proposals_without_fabricated_score():
    result = compare(system("[Cl-]", [[0, 0, 0]]), references())
    assert result["reused_inventory"]["features"] == []
    for comparison in result["comparisons"]:
        assert comparison["proposed_mappings"] == 0
        assert comparison["fresh"]["proposals"]["complete"]
        assert comparison["fresh"]["placement_report"]["n_fits"] == 0
        assert comparison["fresh"]["native_evaluations"] == []


def test_nondefault_unit_policy_preserves_explicit_length_and_rmsd_records():
    with puw.context(standard_units=["angstrom", "fs", "degrees"]):
        result = compare(moved(system(IONS, ION_COORDINATES)), references())
    center = puw.QuantityRecord.from_dict(
        result["reused_inventory"]["features"][1]["center"]
    ).to_quantity(unit="nm", dimensionality={"[L]": 1})
    assert np.isfinite(puw.get_value(center, to_unit="nm")).all()
    alignment = result["comparisons"][0]["fresh"]["placement_report"][
        "accepted_placements"
    ][0]["alignment"]
    rmsd = puw.QuantityRecord.from_dict(alignment["rmsd"]).to_quantity(
        unit="nm", dimensionality={"[L]": 1}
    )
    assert np.max(puw.get_value(rmsd, to_unit="nm")) < 1e-12
    assert (
        result["comparisons"][0]["fresh"]["native_evaluations"][0]["ranking_score"]
        == 1.0
    )


def test_explicit_second_frame_is_checked_without_changing_either_source_frame():
    source = system(IONS, ION_COORDINATES)
    source.structures.append(
        coordinates=puw.quantity([ION_COORDINATES + [2, 1, 3]], "nm")
    )
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    result = compare(source, references(), structure_index=1)
    assert result["source_options"]["structure_index"] == 1
    assert result["source_options"]["chemical_state"] == 0
    assert result["reused_inventory"]["structure_index"] == 1
    assert (
        result["comparisons"][0]["fresh"]["native_evaluations"][0]["ranking_score"]
        == 1.0
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )


@pytest.mark.parametrize(
    "options",
    [
        dict(max_graph_nodes=1),
        dict(correspondence_strategy="triplet_seeds", max_trials=1),
    ],
)
def test_native_resource_limits_propagate_without_recording_a_negative(options):
    with pytest.raises(CliqueLimitError):
        compare(system(IONS, ION_COORDINATES), references(), **options)


def test_invalid_reference_geometry_propagates_native_argument_failure():
    collinear = ion_inventory([[0, 0, 0], [0.3, 0, 0], [0.6, 0, 0]])
    with pytest.raises(ArgumentError, match="non-collinear"):
        compare(
            system(IONS, ION_COORDINATES), [dict(key="invalid", inventory=collinear)]
        )


@pytest.mark.parametrize(
    "field,value",
    [
        ("structure_index", 1),
        ("chemical_state", "reference"),
        ("selected_atom_indices", [2, 1, 0]),
    ],
)
def test_native_alignment_refuses_wrong_cached_source_axes(monkeypatch, field, value):
    queries = references()
    actual = phmt.modeler.get_features

    def wrong_axes(*args, **kwargs):
        inventory = actual(*args, **kwargs)
        inventory[field] = value
        return inventory

    monkeypatch.setattr(phmt.modeler, "get_features", wrong_axes)
    with pytest.raises(ArgumentError, match="contract differs"):
        compare(system(IONS, ION_COORDINATES), queries)


@pytest.mark.parametrize(
    "queries,features,maximum",
    [
        ([], ION_FEATURES, 1),
        ([dict(key="a", inventory={}), dict(key="a", inventory={})], ION_FEATURES, 1),
        ([dict(key="a", inventory={})], "positive charge", 1),
        ([dict(key="a", inventory={})], ION_FEATURES, True),
    ],
)
def test_invalid_experiment_declarations_fail_before_source_access(
    monkeypatch, queries, features, maximum
):
    def forbidden(*args, **kwargs):
        raise AssertionError("invalid declarations must fail before source access")

    monkeypatch.setattr(msm, "get", forbidden)
    with pytest.raises(ValueError):
        compare_feature_reuse(None, queries, features=features, max_placements=maximum)


def test_application_owned_attribution_wraps_comparison_without_changing_native_arms():
    ackredit = pytest.importorskip("ackredit")
    source = system(IONS, ION_COORDINATES)
    queries = references()
    with ackredit.session("feature-reuse-control") as application, phmt.attribution():
        result = compare(source, queries)
        assert ackredit.current_session() is application
    assert result["attribution"]["status"] == "captured"
    assert result["attribution"]["references"]["items"]
    assert result["attribution"]["references"]["uses"]
    assert all(row["native_evidence_equal"] for row in result["comparisons"])
    assert "attribution" not in result["reused_inventory"]
