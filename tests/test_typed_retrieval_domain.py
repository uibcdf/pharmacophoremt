"""Complete six-family native mappings, boundary observations and orientation stages."""

import math
import os
from copy import deepcopy

import pytest

from phmt_test_support.feature_snapshot import FeatureSnapshotStudy
from phmt_test_support.snapshot_retrieval import (
    SnapshotRetrievalStudy,
    reference_proposals,
)
from phmt_test_support.typed_retrieval import (
    check_native,
    compare_domain,
    declaration,
    load_entries,
)


@pytest.fixture(scope="module")
def entries():
    return load_entries(os.environ.get("PHMT_RECEIVING_CONTEXT", "source"))


@pytest.fixture(scope="module")
def scientific(entries):
    return compare_domain(entries, declaration())


def test_full_four_query_cannot_accept_a_three_feature_native_target(entries):
    query = next(q for q in declaration()["queries"] if q["key"] == "mixed-four")
    native = FeatureSnapshotStudy(entries[4]["snapshot"]).decode_inventory()
    assert len(native["features"]) == 3
    assert reference_proposals(query, native) == []


def test_all_six_families_are_admitted_with_original_work_positions(entries):
    index = SnapshotRetrievalStudy(entries, 1)
    description = index.describe()
    assert description["eligible_original_ordinals"] == [1, 3, 4, 5, 6, 7, 8, 9, 10]
    assert description["pair_entries"] == 42
    assert {
        r["kind"]
        for row in description["original_occurrences"]
        for r in row["original_feature_maps"]
    } == {
        "hydrophobicity",
        "hb donor",
        "hb acceptor",
        "aromatic ring",
        "positive charge",
        "negative charge",
    }
    assert description["original_occurrences"][0]["feature_count"] == 0
    assert description["original_occurrences"][2]["feature_count"] == 2


@pytest.mark.parametrize("key", ["donors4", "ring3", "mixed3", "mixed4"])
def test_captured_native_maps_and_geometry_match_prospective_witnesses(entries, key):
    case = next(c for c in declaration()["parents"] if c["key"] == key)
    positions = {
        "donors4": (1, 6),
        "ring3": (3, 7),
        "mixed3": (4, 8),
        "mixed4": (5, 9),
    }[key]
    for i in positions:
        check_native(
            case, FeatureSnapshotStudy(entries[i]["snapshot"]).decode_inventory()
        )


@pytest.mark.parametrize("width", [0.125, 0.5, 1.0])
def test_zero_length_donor_anchor_preserves_each_original_occurrence(entries, width):
    index = SnapshotRetrievalStudy(entries, width)
    result = index.lookup(declaration()["queries"][0], current_entries=entries)
    assert result["complete"]
    assert result["index_candidate_ordinals"] == [0, 4, 8]
    assert result["candidate_ordinals"] == [1, 6, 10]
    assert result["not_indexed_original_ordinals"] == [0, 2]
    assert index.original_bytes(1) == index.original_bytes(10)
    assert index.describe()["original_occurrences"][1]["work_key"] == "nm"
    assert index.describe()["original_occurrences"][6]["work_key"] == "1 nm"


def test_three_point_query_keeps_full_mapping_inside_a_four_feature_target(entries):
    query = next(q for q in declaration()["queries"] if q["key"] == "mixed-three")
    native = FeatureSnapshotStudy(entries[5]["snapshot"]).decode_inventory()
    assert reference_proposals(query, native) == [[[0, 0], [1, 2], [2, 3]]]


@pytest.mark.parametrize(
    "bad", ["missing_donor", "missing_ring", "extra_orientation", "wrong_count"]
)
def test_incomplete_query_orientation_refuses_before_native_reference(
    entries, monkeypatch, bad
):
    from pharmacophoremt import screening

    query = deepcopy(declaration()["queries"][1 if bad == "missing_ring" else 0])
    if bad == "missing_donor":
        query.pop("directions")
    elif bad == "missing_ring":
        query.pop("normals")
    elif bad == "extra_orientation":
        query["directions"][2] = [1, 0, 0]
    else:
        query["directions"].pop()

    def unexpected(*args, **kwargs):
        pytest.fail(
            "native reference reached before missing/extra query geometry refusal"
        )

    monkeypatch.setattr(screening, "get_rigid_feature_correspondences", unexpected)
    with pytest.raises(ValueError):
        reference_proposals(
            query, FeatureSnapshotStudy(entries[1]["snapshot"]).decode_inventory()
        )


def test_predecessor_exact_successor_operands_are_distinct_original_binary64_values():
    queries = {q["key"]: q for q in declaration()["queries"]}
    xs = [
        queries[k]["features"][1][1][0]
        for k in ("boundary-inside", "boundary-exact", "boundary-outside")
    ]
    assert xs == [math.nextafter(5.25, -math.inf), 5.25, math.nextafter(5.25, math.inf)]
    for key, value in zip(
        ("boundary-inside", "boundary-exact", "boundary-outside"), xs
    ):
        assert float.fromhex(queries[key]["anchor_x_binary64_hex"]) == value
        assert queries[key]["classification"] == "native-candidate-band"
    assert len(set(xs)) == 3


def test_complete_native_mapping_equality_does_not_relabel_boundary_oracle_differences(
    scientific,
):
    assert scientific["complete"] and len(scientific["rows"]) == 36
    assert scientific["strict_oracle_comparisons"] == 99
    assert len(scientific["candidate_band_observations"]) == 33
    assert scientific["strict_native_rational_equal"]
    assert not scientific["candidate_band_native_rational_equal"]
    assert any(
        not r["equal"] and r["native"] and not r["rational"]
        for r in scientific["candidate_band_observations"]
    )
    assert all(row["equal_native_exhaustive"] for row in scientific["rows"])
    assert scientific["all_native_full_query_mappings_preserved"]


def test_two_donor_proposals_keep_hydrogen_identity_and_separate_direction_acceptance(
    scientific,
):
    checks = [r for r in scientific["orientation_checks"] if r["query"] == "donor-four"]
    assert [r["work_ordinal"] for r in checks] == [1, 6, 10]
    for row in checks:
        assert len(row["checks"]) == 2
        assert sum(c["evaluation"]["all_pairs_valid"] for c in row["checks"]) == 1
        assert all(c["evaluation"]["all_positions_valid"] for c in row["checks"])
        assert (
            len({tuple(tuple(pair) for pair in c["pairs"]) for c in row["checks"]}) == 2
        )
    mapped = next(
        r for r in scientific["rows"] if r["query"] == "donor-four" and r["width"] == 1
    )["joined_mappings"]
    assert len(mapped) == 6
    assert [r["work_ordinal"] for r in mapped] == [1, 1, 6, 6, 10, 10]
    assert {
        tuple(m["atom_indices"])
        for r in mapped
        for m in r["matched_original_feature_maps"]
        if m["kind"] == "hb donor"
    } == {(1, 0), (1, 2)}


def test_aromatic_normal_sign_and_reflection_remain_separate_stage_meanings(scientific):
    checks = [
        r for r in scientific["orientation_checks"] if r["query"] == "aromatic-three"
    ]
    assert [r["work_ordinal"] for r in checks] == [3, 7]
    assert all(
        len(row["checks"]) == 2
        and all(c["evaluation"]["all_pairs_valid"] for c in row["checks"])
        for row in checks
    )
    for query in ("mixed-four", "mixed-four-reflected"):
        mappings = scientific["reference_full_mappings"][query]
        assert [i for i, pairs in enumerate(mappings) if pairs] == [5, 9]
        assert all(len(pairs) == 4 for rows in mappings for pairs in rows)
    assert not scientific["final_pose_or_activity_acceptance"]


def test_translated_near_collinear_and_short_inputs_keep_declared_finite_coverage(
    scientific,
):
    reference = scientific["reference_full_mappings"]
    assert reference["mixed-three"] == reference["translated-mixed"]
    assert reference["near-collinear"] == [[]] * 11
    assert reference["insufficient-kind"] == [[]] * 11
    assert all(not rows[0] and not rows[2] for rows in reference.values())
    assert scientific["native_inputs_unchanged"]
    assert scientific["prefix_lookup"]["pending_candidate_ordinals"] == [6, 10]
    assert not scientific["prefix_lookup"]["complete"]
    assert scientific["prefix_lookup"]["unseen_outcomes_are_unknown"]
