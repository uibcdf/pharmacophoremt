"""Finite, equivalent native-proposal workload; no production index selection."""

import gc
import json
import sys
import tracemalloc
from copy import deepcopy
from pathlib import Path
from time import perf_counter_ns, process_time_ns

from phmt_test_support.feature_snapshot_case import projection
from phmt_test_support.snapshot_retrieval import (
    SnapshotRetrievalStudy,
    _digest,
    _entries,
    reference_proposals,
)
from phmt_test_support.typed_retrieval import declaration as typed_declaration
from phmt_test_support.typed_retrieval import load_entries

DIRECTORY = Path(__file__).resolve().parents[1] / "tests/data/retrieval_cost"


def declaration():
    spec = json.loads((DIRECTORY / "declaration.json").read_text())
    if spec["schema"] != "pharmacophoremt.retrieval-cost-case@1":
        raise ValueError("Unknown retrieval cost declaration")
    return spec


class PreparedCorpus:
    """One detached original snapshot/native pool, shared equally by both routes."""

    def __init__(self, entries):
        snapshots, self.manifest = _entries(entries)
        self.binding = _digest(self.manifest)
        self.native = [snapshot.decode_inventory() for snapshot in snapshots]
        self.original_bytes = [snapshot.to_bytes() for snapshot in snapshots]
        self.entries = deepcopy(entries)

    def check_binding(self, entries):
        _, current = _entries(entries)
        if _digest(current) != self.binding:
            raise ValueError("Original snapshot/work bindings changed")

    def fingerprint(self):
        return [projection(inventory) for inventory in self.native]

    def storage(self):
        unique = {
            row["snapshot_sha256"]: raw
            for row, raw in zip(self.manifest, self.original_bytes)
        }
        return {
            "work_occurrences": len(self.manifest),
            "original_snapshot_bytes_by_work": sum(map(len, self.original_bytes)),
            "unique_snapshot_hashes": len(unique),
            "unique_original_snapshot_bytes": sum(map(len, unique.values())),
            "persisted_index_bytes": None,
            "persisted_index_reason": "No persisted index representation exists",
        }


class ProposalWorkload:
    """The same prepared pool/reference with optional unchanged study lookup."""

    def __init__(self, corpus, strategy):
        if strategy not in ("scan", "index"):
            raise ValueError("Declare scan or index")
        self.corpus, self.strategy = corpus, strategy
        self.index = (
            SnapshotRetrievalStudy(corpus.entries, 1.0) if strategy == "index" else None
        )
        if self.index is not None and self.index.manifest_sha256 != corpus.binding:
            raise ValueError("Native pool and index original bindings disagree")

    def query(self, query, *, current_entries):
        if self.index is None:
            self.corpus.check_binding(current_entries)
            candidates = list(range(len(self.corpus.native)))
        else:
            lookup = self.index.lookup(query, current_entries=current_entries)
            if not lookup["complete"]:
                raise ValueError("Incomplete lookup cannot be a complete cost sample")
            candidates = lookup["candidate_ordinals"]
        mappings = [[] for _ in self.corpus.native]
        for ordinal in candidates:
            mappings[ordinal] = reference_proposals(query, self.corpus.native[ordinal])
        joined = []
        for ordinal, alternatives in enumerate(mappings):
            original = self.corpus.manifest[ordinal]
            features = self.corpus.native[ordinal]["features"]
            for pairs in alternatives:
                joined.append(
                    {
                        "work_ordinal": ordinal,
                        "work_key": original["work_key"],
                        "snapshot_sha256": original["snapshot_sha256"],
                        "pairs": pairs,
                        "matched_original_feature_maps": [
                            {
                                "feature_index": j,
                                **{
                                    k: deepcopy(features[j][k])
                                    for k in (
                                        "kind",
                                        "atom_indices",
                                        "geometry_atom_indices",
                                    )
                                },
                            }
                            for _, j in pairs
                        ],
                    }
                )
        unseen = [i for i in range(len(mappings)) if i not in candidates]
        short = [
            i
            for i in unseen
            if len(self.corpus.native[i]["features"]) < len(query["features"])
        ]
        return {
            "query": query["key"],
            "original_full_mappings": mappings,
            "joined_mappings": joined,
            "native_evaluated_ordinals": candidates,
            "cardinality_negative_ordinals": short,
            "prefiltered_ordinals": [i for i in unseen if i not in short],
            "reference_calls": len(candidates),
            "complete": True,
            "final_pose_or_activity_acceptance": False,
        }


def measured_call(function):
    """Standard clocks only; reject observation taxes on the measured body."""
    if (
        sys.getprofile() is not None
        or sys.gettrace() is not None
        or tracemalloc.is_tracing()
    ):
        raise ValueError(
            "Disable profiling/tracing/allocation measurement before timing"
        )
    wall, cpu = perf_counter_ns(), process_time_ns()
    result = function()
    cpu_elapsed, wall_elapsed = process_time_ns() - cpu, perf_counter_ns() - wall
    return {"wall_ns": wall_elapsed, "cpu_ns": cpu_elapsed}, result


def _captured(label, function, *, timed):
    import ackredit

    with ackredit.capture(label) as captured:
        metrics, result = measured_call(function) if timed else ({}, function())
    try:
        credit = {"status": "recorded", "attribution": captured.attribution.to_dict()}
    except Exception as error:
        credit = {
            "status": "unavailable",
            "attribution": None,
            "failure": {"type": type(error).__name__, "reason": str(error)},
        }
    return {**metrics, "actual_attribution": credit}, result


def run_policy(context, unit, *, calibration=False, progress=None):
    spec, typed = declaration(), typed_declaration()
    if context not in ("source", "installed") or unit not in spec["unit_policies"]:
        raise ValueError("Declare an original context and unit policy")
    if calibration and unit != spec["calibration"]["unit_policy"]:
        raise ValueError("The prospective calibration is nm only")
    expectations = json.loads((DIRECTORY / "expected.json").read_text())
    expected = expectations["contexts"][context]["policies"][unit]
    queries = typed["queries"]
    assert (
        len(queries) == spec["query_count"] and queries[0]["key"] == spec["first_query"]
    )
    state = {
        "complete": False,
        "unit_policy": unit,
        "sample": "calibration" if calibration else "paired",
        "preparation": {},
        "warmups": [],
        "pairs": [],
        "allocations": [],
    }

    def retain():
        if progress is not None:
            progress(state)

    def check(rows):
        for row in rows:
            assert (
                row["complete"]
                and row["original_full_mappings"] == expected[row["query"]]
            ), row["query"]

    def batch(route):
        return [route.query(query, current_entries=entries) for query in queries]

    retain()
    state["preparation"]["original_file_read"], entries = _captured(
        "original file read", lambda: load_entries(context), timed=True
    )
    state["preparation"]["native_reconstruction"], corpus = _captured(
        "common native reconstruction", lambda: PreparedCorpus(entries), timed=True
    )
    before = corpus.fingerprint()
    assert len(corpus.native) == spec["work_occurrences"]
    state["storage"] = corpus.storage()
    retain()
    for strategy in spec["pair_orders"][unit][0]:
        state["current_operation"] = {"phase": "warmup", "strategy": strategy}

        def warm():
            route = ProposalWorkload(corpus, strategy)
            return batch(route)

        capture, rows = _captured("warmup " + strategy, warm, timed=False)
        check(rows)
        state["warmups"].append({"strategy": strategy, "rows": rows, **capture})
        retain()
    orders = spec["pair_orders"][unit][:1] if calibration else spec["pair_orders"][unit]
    for ordinal, order in enumerate(orders):
        pair = {"ordinal": ordinal, "order": order, "strategies": []}
        state["pairs"].append(pair)
        for strategy in order:
            state["current_operation"] = {
                "phase": "paired",
                "pair": ordinal,
                "strategy": strategy,
            }
            gc.collect()
            build, route = _captured(
                "build " + strategy,
                lambda: ProposalWorkload(corpus, strategy),
                timed=True,
            )
            first, row = _captured(
                "first query " + strategy,
                lambda route=route: route.query(queries[0], current_entries=entries),
                timed=True,
            )
            check([row])
            first["row"] = row
            repeated, rows = _captured(
                "reused query batch " + strategy,
                lambda route=route: batch(route),
                timed=True,
            )
            check(rows)
            repeated["rows"] = rows
            pair["strategies"].append(
                {
                    "strategy": strategy,
                    "build": build,
                    "first_query": first,
                    "reused_batch": repeated,
                }
            )
            del route
            retain()
        assert [
            r["joined_mappings"] for r in pair["strategies"][0]["reused_batch"]["rows"]
        ] == [
            r["joined_mappings"] for r in pair["strategies"][1]["reused_batch"]["rows"]
        ]
    if not calibration:
        for strategy in spec["strategies"]:
            state["current_operation"] = {"phase": "allocations", "strategy": strategy}
            if (
                tracemalloc.is_tracing()
                or sys.getprofile() is not None
                or sys.gettrace() is not None
            ):
                raise ValueError("Allocation measurement needs an unobserved process")
            gc.collect()

            def allocate():
                tracemalloc.start()
                try:
                    allocated = PreparedCorpus(entries)
                    route = ProposalWorkload(allocated, strategy)
                    rows = batch(route)
                    current, peak = tracemalloc.get_traced_memory()
                finally:
                    tracemalloc.stop()
                return {"current_bytes": current, "peak_bytes": peak}, rows

            capture, (memory, rows) = _captured(
                "allocations " + strategy, allocate, timed=False
            )
            check(rows)
            state["allocations"].append(
                {"strategy": strategy, **memory, "rows": rows, **capture}
            )
            retain()
    assert corpus.fingerprint() == before
    state.update(
        complete=True,
        original_mappings_equal=True,
        native_pool_unchanged=True,
        timing_scope="warm process/new asset or reused batch; not process/OS cold",
        native_memory_measured=False,
        persisted_index_measured=False,
    )
    retain()
    return state
