"""Equivalent original native proposals, full bindings and honest measurement scope."""

import json
import os
import runpy
from copy import deepcopy
from pathlib import Path

import pytest

from phmt_test_support import retrieval_cost as cost
from phmt_test_support.typed_retrieval import declaration, load_entries


@pytest.fixture(scope="module")
def entries():
    return load_entries(os.environ.get("PHMT_RECEIVING_CONTEXT", "source"))


@pytest.fixture(scope="module")
def corpus(entries):
    return cost.PreparedCorpus(entries)


@pytest.mark.parametrize("query_index", range(12))
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_same_original_full_native_answers_for_both_routes(
    corpus, entries, query_index, unit
):
    from pharmacophoremt import pyunitwizard as puw

    mode = os.environ.get("PHMT_RECEIVING_CONTEXT", "source")
    original = json.loads((cost.DIRECTORY / "expected.json").read_text())
    query = declaration()["queries"][query_index]
    before = corpus.fingerprint()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        rows = [
            cost.ProposalWorkload(corpus, strategy).query(
                query, current_entries=entries
            )
            for strategy in ("scan", "index")
        ]
    assert all(
        row["original_full_mappings"]
        == original["contexts"][mode]["policies"][unit][query["key"]]
        for row in rows
    )
    assert rows[0]["joined_mappings"] == rows[1]["joined_mappings"]
    for row in rows:
        for joined in row["joined_mappings"]:
            ordinal = joined["work_ordinal"]
            assert joined["work_key"] == entries[ordinal]["work_key"]
            assert (
                joined["snapshot_sha256"] == corpus.manifest[ordinal]["snapshot_sha256"]
            )
            assert [
                m["feature_index"] for m in joined["matched_original_feature_maps"]
            ] == [j for _, j in joined["pairs"]]
    assert corpus.fingerprint() == before


@pytest.mark.parametrize("strategy", ["scan", "index"])
@pytest.mark.parametrize("mutation", ["work", "same_points_other_original"])
def test_stale_original_binding_refuses_before_native_work(
    corpus, entries, monkeypatch, strategy, mutation
):
    route = cost.ProposalWorkload(corpus, strategy)
    changed = deepcopy(entries)
    if mutation == "work":
        changed[1]["work_key"] += ":changed"
    else:
        changed[1]["snapshot"] = entries[6]["snapshot"]

    def forbidden(*args):
        raise AssertionError("Stale workload reached native reference")

    monkeypatch.setattr(cost, "reference_proposals", forbidden)
    with pytest.raises(ValueError, match="bindings changed"):
        route.query(declaration()["queries"][0], current_entries=changed)


def test_native_calls_and_index_negatives_keep_distinct_original_coverage(
    corpus, entries, monkeypatch
):
    original = cost.reference_proposals
    actual_calls = []

    def observed(query, native):
        actual_calls.append(len(native["features"]))
        return original(query, native)

    monkeypatch.setattr(cost, "reference_proposals", observed)
    query = declaration()["queries"][0]
    scan = cost.ProposalWorkload(corpus, "scan").query(query, current_entries=entries)
    assert len(actual_calls) == scan["reference_calls"] == 11
    actual_calls.clear()
    indexed = cost.ProposalWorkload(corpus, "index").query(
        query, current_entries=entries
    )
    assert len(actual_calls) == indexed["reference_calls"] == 3
    assert indexed["native_evaluated_ordinals"] == [1, 6, 10]
    assert indexed["cardinality_negative_ordinals"] == [0, 2, 3, 4, 7, 8]
    assert indexed["prefiltered_ordinals"] == [5, 9]
    assert scan["prefiltered_ordinals"] == scan["cardinality_negative_ordinals"] == []
    assert scan["original_full_mappings"] == indexed["original_full_mappings"]


def test_original_byte_storage_does_not_invent_persisted_index_size(corpus):
    storage = corpus.storage()
    assert storage["work_occurrences"] == 11 and storage["unique_snapshot_hashes"] == 10
    assert (
        storage["original_snapshot_bytes_by_work"]
        > storage["unique_original_snapshot_bytes"]
        > 0
    )
    assert storage["persisted_index_bytes"] is None


def test_returned_original_maps_are_detached_from_native_pool(corpus, entries):
    before = corpus.fingerprint()
    row = cost.ProposalWorkload(corpus, "scan").query(
        declaration()["queries"][0], current_entries=entries
    )
    row["joined_mappings"][0]["matched_original_feature_maps"][0][
        "atom_indices"
    ].append(999)
    assert corpus.fingerprint() == before


@pytest.mark.parametrize("observer", ["profile", "trace", "allocations"])
def test_timer_refuses_instrumented_comparisons(monkeypatch, observer):
    monkeypatch.setattr(cost.sys, "getprofile", lambda: None)
    monkeypatch.setattr(cost.sys, "gettrace", lambda: None)
    monkeypatch.setattr(cost.tracemalloc, "is_tracing", lambda: False)
    if observer == "allocations":
        monkeypatch.setattr(cost.tracemalloc, "is_tracing", lambda: True)
    else:
        monkeypatch.setattr(
            cost.sys,
            "getprofile" if observer == "profile" else "gettrace",
            lambda: object(),
        )
    with pytest.raises(ValueError, match="before timing"):
        cost.measured_call(lambda: pytest.fail("Biased timing body executed"))


def test_native_failure_cannot_be_a_complete_empty_sample(corpus, entries, monkeypatch):
    def fail(*args):
        raise RuntimeError("controlled native failure")

    monkeypatch.setattr(cost, "reference_proposals", fail)
    with pytest.raises(RuntimeError, match="controlled native failure"):
        cost.ProposalWorkload(corpus, "index").query(
            declaration()["queries"][0], current_entries=entries
        )


def test_incomplete_index_lookup_is_not_a_complete_cost_sample(
    corpus, entries, monkeypatch
):
    route = cost.ProposalWorkload(corpus, "index")
    monkeypatch.setattr(
        route.index, "lookup", lambda *args, **kwargs: {"complete": False}
    )
    with pytest.raises(ValueError, match="Incomplete lookup"):
        route.query(declaration()["queries"][0], current_entries=entries)


@pytest.mark.parametrize("invalid", ["existing", "admission"])
def test_cost_driver_refuses_unsafe_output_or_admission(tmp_path, invalid):
    output = tmp_path / "existing.json"
    output.write_bytes(b"original caller bytes")
    path = Path(__file__).resolve().parents[1] / "devtools/benchmark_retrieval_cost.py"
    driver = runpy.run_path(str(path), run_name="cost_driver_under_test")["main"]
    with pytest.raises(FileExistsError if invalid == "existing" else ValueError):
        driver(
            [
                "--output",
                str(output),
                "--snapshot-context",
                "source",
                "--sample",
                "paired",
                "--admission-sha256",
                "a" * 64 if invalid == "existing" else "invalid",
            ]
        )
    assert output.read_bytes() == b"original caller bytes"
