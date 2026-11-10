"""Original ordinal/map evidence, native-reference equality and stale reuse refusal."""

import hashlib
import os
from copy import deepcopy

import pytest

from phmt_test_support.feature_snapshot import FeatureSnapshotStudy
from phmt_test_support.snapshot_retrieval import (
    SnapshotRetrievalStudy,
    compare_retrieval,
    declaration,
    load_entries,
    project,
)


@pytest.fixture(scope="module")
def original_entries():
    return load_entries(os.environ.get("PHMT_RECEIVING_CONTEXT", "source"))


@pytest.fixture
def entries(original_entries):
    return deepcopy(original_entries)


@pytest.fixture(scope="module")
def scientific(original_entries):
    return compare_retrieval(original_entries, declaration())


def reencode(record):
    from pharmacophoremt_results import canonical_json

    record["payload_sha256"] = hashlib.sha256(
        canonical_json(record["payload"]).encode()
    ).hexdigest()
    return canonical_json(record).encode()


def test_native_empty_short_and_repeated_work_retains_full_original_bindings(entries):
    index = SnapshotRetrievalStudy(entries, 1)
    description = index.describe()
    rows = description["original_occurrences"]
    assert [r["feature_count"] for r in rows] == [0, 3, 2, 1, 3, 3, 2, 0, 1]
    assert description["eligible_original_ordinals"] == [1, 4, 5]
    assert description["pair_entries"] == 9
    assert [r["work_key"] for r in rows][1:6:3] == ["nm", "1 nm"]
    assert rows[1]["parent"]["source_key"] == "nm"
    assert rows[1]["parent"]["occurrence_key"] == "1 nm"
    assert rows[5]["work_key"] == "repeat=α"
    assert index.original_bytes(1) == index.original_bytes(5)
    assert rows[1]["work_ordinal"] != rows[5]["work_ordinal"]
    assert rows[0]["coverage"] == {
        "aromatic ring": {"count": 0, "status": "evaluated_empty"}
    }
    assert [r["indexing"] for r in rows].count(
        "fewer-than-three-in-full-query-profile"
    ) == 6
    for i, entry in enumerate(entries):
        assert index.original_bytes(i) == entry["snapshot"]
        assert (
            FeatureSnapshotStudy(index.original_bytes(i)).to_dict()
            == FeatureSnapshotStudy(entry["snapshot"]).to_dict()
        )
    assert not description["molecular_origin_authenticated"]


@pytest.mark.parametrize("width", [0.125, 0.5, 1.0])
def test_compact_postings_translate_to_interleaved_original_work_positions(
    entries, width
):
    index = SnapshotRetrievalStudy(entries, width)
    result = index.lookup(declaration()["queries"][0], current_entries=entries)
    assert result["complete"] and not result["unseen_outcomes_are_unknown"]
    assert result["index_candidate_ordinals"] == [0, 1, 2]
    assert result["candidate_ordinals"] == [1, 4, 5]
    assert result["not_indexed_original_ordinals"] == [0, 2, 3, 6, 7, 8]


@pytest.mark.parametrize(
    "key", ["identity", "cross-bin-feasible", "same-anchor-impossible", "wrong-kind"]
)
def test_complete_native_reference_and_rational_witness_cover_every_original(
    scientific, key
):
    expected = (
        [[[0, 0], [1, 1], [2, 2]]] if key in ("identity", "cross-bin-feasible") else []
    )
    mappings = scientific["reference_full_mappings"][key]
    assert len(mappings) == 9
    for ordinal, row in enumerate(mappings):
        assert row == (expected if ordinal in (1, 4, 5) else [])
    assert scientific["complete"]
    assert scientific["independent_rational_mapping_comparisons"] == 36
    assert len(scientific["rows"]) == 12
    assert scientific["all_original_mappings_equal_exhaustive"]
    assert scientific["all_original_mappings_equal_rational_oracle"]


def test_joined_results_keep_each_original_feature_and_atom_mapping(scientific):
    row = next(
        r for r in scientific["rows"] if r["query"] == "identity" and r["width"] == 1
    )
    joined = row["joined_mappings"]
    assert [j["work_ordinal"] for j in joined] == [1, 4, 5]
    assert [j["work_key"] for j in joined] == ["nm", "1 nm", "repeat=α"]
    assert joined[0]["snapshot_sha256"] == joined[2]["snapshot_sha256"]
    for match in joined:
        assert match["pairs"] == [[0, 0], [1, 1], [2, 2]]
        assert match["parent"]["source_key"] == "nm"
        assert match["parent"]["occurrence_key"] == "1 nm"
        assert [r["feature_index"] for r in match["matched_original_feature_maps"]] == [
            0,
            1,
            2,
        ]
        assert [r["atom_indices"] for r in match["matched_original_feature_maps"]] == [
            [0],
            [1],
            [2],
        ]
        assert [
            r["geometry_atom_indices"] for r in match["matched_original_feature_maps"]
        ] == [[0], [1], [2]]


def test_unsafe_bin_misses_and_geometric_false_positives_remain_visible(scientific):
    cross = next(
        r
        for r in scientific["rows"]
        if r["query"] == "cross-bin-feasible" and r["width"] == 1
    )
    impossible = next(
        r
        for r in scientific["rows"]
        if r["query"] == "same-anchor-impossible" and r["width"] == 1
    )
    assert cross["exact_bin_missing_positive_ordinals"] == [4]
    assert impossible["lookup"]["candidate_ordinals"] == [1, 4, 5]
    assert impossible["original_full_mappings"] == [[]] * 9
    assert not scientific["final_pose_or_activity_acceptance"]


def test_prefix_preserves_original_pending_ordinals_and_unsearched_unknown_work(
    entries,
):
    index = SnapshotRetrievalStudy(entries, 1)
    prefix = index.lookup(
        declaration()["queries"][0], current_entries=entries, max_candidates=1
    )
    assert prefix["candidate_ordinals"] == [1]
    assert prefix["pending_candidate_ordinals"] == [4, 5]
    assert not prefix["complete"] and prefix["unseen_outcomes_are_unknown"]
    bins = index.lookup(
        declaration()["queries"][0], current_entries=entries, max_lookup_bins=1
    )
    assert bins["unsearched_bin_interval"] is not None
    assert not bins["complete"] and bins["unseen_outcomes_are_unknown"]


@pytest.mark.parametrize(
    "change",
    [
        "work_key",
        "order",
        "source",
        "producer",
        "coverage",
        "atom_map",
        "recognition",
        "charge",
        "unindexed_direction",
    ],
)
def test_same_point_projection_cannot_hide_changed_original_byte_or_work_bindings(
    entries, monkeypatch, change
):
    from phmt_test_support.retrieval_controls import StudyIndex

    index = SnapshotRetrievalStudy(entries, 1)
    current = deepcopy(entries)
    ordinal = 2 if change == "unindexed_direction" else 1
    record = FeatureSnapshotStudy(current[ordinal]["snapshot"]).to_dict()
    payload = record["payload"]
    if change == "work_key":
        current[1]["work_key"] = "renamed work"
    elif change == "order":
        current.reverse()
    else:
        if change == "source":
            payload["parent"]["source_key"] = "different source"
        elif change == "producer":
            payload["producer"]["versions"]["declared_note"] = "changed"
        elif change == "coverage":
            payload["request"]["features"].insert(0, "hydrophobicity")
            payload["coverage"]["hydrophobicity"] = {
                "count": 0,
                "status": "evaluated_empty",
            }
        elif change == "atom_map":
            payload["inventory"]["features"][0]["geometry_atom_indices"] = [2]
        elif change == "recognition":
            payload["inventory"]["recognition"]["declared_note"] = "changed"
        else:
            from pharmacophoremt import pyunitwizard as puw

            field, value, unit = (
                ("direction", [-1, 0, 0], "dimensionless")
                if change == "unindexed_direction"
                else ("charge", 2, "e")
            )
            payload["inventory"]["features"][0][field] = (
                puw.QuantityRecord.from_quantity(
                    puw.quantity(value, unit), field=f"features[0].{field}"
                ).to_dict()
            )
        current[ordinal]["snapshot"] = reencode(record)
        FeatureSnapshotStudy(current[ordinal]["snapshot"])

    def unexpected(*args, **kwargs):
        pytest.fail("posting lookup reached after changed original binding")

    monkeypatch.setattr(StudyIndex, "lookup", unexpected)
    with pytest.raises(ValueError, match="bindings changed"):
        index.lookup(declaration()["queries"][0], current_entries=current)


def test_returned_description_inventory_and_caller_container_are_detached(entries):
    index = SnapshotRetrievalStudy(entries, 1)
    original = index.original_bytes(1)
    description = index.describe()
    description["original_occurrences"][1]["parent"].clear()
    description["settings"].clear()
    inventory = index.original_inventory(1)
    inventory["features"][0]["center"].magnitude[0] = 99
    entries[1]["snapshot"] = b"changed"
    assert index.original_bytes(1) == original
    assert index.describe()["original_occurrences"][1]["parent"]["source_key"] == "nm"
    assert project(index.original_inventory(1))[0][1] == [0, 0, 0]


@pytest.mark.parametrize("bad", ["duplicate", "nontext", "layout"])
def test_invalid_work_manifest_refuses_before_quantity_reconstruction(
    entries, monkeypatch, bad
):
    if bad == "duplicate":
        entries[1]["work_key"] = entries[0]["work_key"]
    elif bad == "nontext":
        entries[0]["work_key"] = True
    else:
        entries[0]["extra"] = "partial"

    def unexpected(*args, **kwargs):
        pytest.fail("quantity reconstruction reached before decidable manifest refusal")

    monkeypatch.setattr(FeatureSnapshotStudy, "decode_inventory", unexpected)
    with pytest.raises(ValueError):
        SnapshotRetrievalStudy(entries, 1)


def test_decoder_failure_propagates_without_a_successful_asset(entries, monkeypatch):
    failure = RuntimeError("controlled original quantity decoding failure")

    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(FeatureSnapshotStudy, "decode_inventory", fail)
    with pytest.raises(RuntimeError) as caught:
        SnapshotRetrievalStudy(entries, 1)
    assert caught.value is failure


def test_reference_failure_preserves_completed_prefix_without_empty_success(
    entries, monkeypatch
):
    from phmt_test_support import snapshot_retrieval as owner

    original, failure, calls, partial = (
        owner.reference_proposals,
        RuntimeError("controlled reference failure"),
        [],
        [],
    )

    def fail_after_prefix(query, native):
        calls.append(len(native["features"]))
        if len(calls) == 4:
            raise failure
        return original(query, native)

    monkeypatch.setattr(owner, "reference_proposals", fail_after_prefix)
    with pytest.raises(RuntimeError) as caught:
        compare_retrieval(
            entries,
            declaration(),
            progress=lambda state: partial.append(deepcopy(state)),
        )
    assert caught.value is failure
    assert calls == [0, 3, 2, 1]
    assert partial[-1]["reference_calls"]["exhaustive"] == 3
    assert len(partial[-1]["reference_full_mappings"]["identity"]) == 3
    assert partial[-1]["rows"] == [] and not partial[-1]["complete"]


def test_partial_native_reference_is_never_completed_empty(entries, monkeypatch):
    from pharmacophoremt import screening
    from phmt_test_support.snapshot_retrieval import reference_proposals

    monkeypatch.setattr(
        screening,
        "get_rigid_feature_correspondences",
        lambda *a, **k: {"complete": False, "correspondences": []},
    )
    with pytest.raises(ValueError, match="did not complete"):
        reference_proposals(
            declaration()["queries"][0],
            SnapshotRetrievalStudy(entries, 1).original_inventory(1),
        )


def test_empty_study_has_no_phantom_work_occurrences():
    index = SnapshotRetrievalStudy([], 1)
    result = index.lookup(declaration()["queries"][0], current_entries=[])
    assert result["complete"] and not result["unseen_outcomes_are_unknown"]
    assert result["candidate_ordinals"] == result["not_indexed_original_ordinals"] == []
