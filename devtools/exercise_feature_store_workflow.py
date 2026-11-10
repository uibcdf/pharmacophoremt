"""Opt-in guided/expert technical exercise; not a human usability result."""

import argparse
import hashlib
import json
import re
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--store", required=True, type=Path)
    parser.add_argument(
        "--snapshot-context", required=True, choices=("source", "installed")
    )
    parser.add_argument("--admission-sha256", required=True)
    args = parser.parse_args(argv)
    if not re.fullmatch("[a-f0-9]{64}", args.admission_sha256):
        raise ValueError("Declare the admitted execution-context SHA-256")
    with args.output.open("x"):
        import ackredit

        import pharmacophoremt as phmt
        from pharmacophoremt import pyunitwizard as puw
        from phmt_test_support.feature_snapshot import FeatureSnapshotStudy
        from phmt_test_support.feature_snapshot_case import producer_context, projection
        from phmt_test_support.feature_store import (
            FeatureStoreReaderStudy,
            FeatureStoreStudy,
        )
        from phmt_test_support.feature_store_workflow import (
            FeatureStoreWorkflowStudy,
            WorkflowRefusalStudy,
            explain_reuse,
            inspect_reuse,
            prepare_reuse,
            recover_publication,
        )
        from phmt_test_support.retrieval_checkpoint import RetrievalCheckpoint
        from phmt_test_support.typed_retrieval import load_entries

        report = {
            "schema": "pharmacophoremt.feature-store-workflow-exercise@1",
            "status": "running",
            "producer": producer_context(args.admission_sha256),
            "original_snapshot_context": args.snapshot_context,
            "human_participants": 0,
            "policies": [],
            "molecular_operations": 0,
            "feature_generation_and_matching": 0,
            "performance_measured": False,
        }
        with ackredit.session("Feature-store workflow exercise"), phmt.attribution():
            checkpoint = RetrievalCheckpoint(
                args.output, report, lambda: ackredit.get_attribution().to_dict()
            )
            checkpoint.retain()
            before_credit = ackredit.get_attribution().to_dict()
            try:
                original = load_entries(args.snapshot_context)
                rows = []
                for entry in original:
                    parent = FeatureSnapshotStudy(entry["snapshot"]).describe()[
                        "parent"
                    ]
                    rows.append(
                        {
                            "work_key": entry["work_key"],
                            "source_key": parent["source_key"],
                            "occurrence_key": parent["occurrence_key"],
                            "status": "ready",
                            "snapshot": entry["snapshot"],
                        }
                    )
                with FeatureStoreStudy(args.store, create=True) as writer:
                    first = writer.seal(rows)
                    writer.publish(first, expected_current=None)
                    first_attempt = next(
                        r["attempt"]
                        for r in writer.attempts()
                        if r["started"]["operation"] == "publish"
                    )

                def bytes_identity():
                    return {
                        str(p.relative_to(args.store)): hashlib.sha256(
                            p.read_bytes()
                        ).hexdigest()
                        for p in args.store.rglob("*")
                        if p.is_file()
                    }

                before = bytes_identity()
                requests = [
                    {
                        "task": "reuse_selected_donors",
                        "families": ["hb donor", "positive charge"],
                        "keys": ["repeat=α", "1 nm", "nm"],
                        "expected": "captured_features_ready",
                    },
                    {
                        "task": "known_empty_aromatic",
                        "families": ["aromatic ring"],
                        "keys": ["empty:nm"],
                        "expected": "captured_features_ready",
                    },
                    {
                        "task": "unobserved_donors",
                        "families": ["hb donor"],
                        "keys": ["empty:nm"],
                        "expected": "evaluate_missing_families",
                    },
                    {
                        "task": "exact_literal_keys",
                        "families": ["hb donor"],
                        "keys": [" nm"],
                        "expected": "unknown_work_key",
                    },
                    {
                        "task": "stale_generation",
                        "families": ["hb donor"],
                        "keys": ["nm"],
                        "generation": "0" * 64,
                        "expected": "generation_mismatch",
                    },
                    {
                        "task": "explicit_empty_selection",
                        "families": ["hb donor"],
                        "keys": [],
                        "expected": "empty_selection",
                    },
                ]
                for unit in ("nm", "pm"):
                    policy = {"unit_policy": unit, "tasks": []}
                    report["policies"].append(policy)
                    with (
                        FeatureStoreWorkflowStudy(args.store) as guided,
                        FeatureStoreReaderStudy(args.store) as expert,
                        puw.context(standard_units=[unit, "ps", "radians"]),
                    ):
                        for request in requests:
                            outputs = []
                            for route in ("guided", "expert"):
                                try:
                                    preview = (
                                        guided.inspect(
                                            request["families"],
                                            work_keys=request["keys"],
                                        )
                                        if route == "guided"
                                        else inspect_reuse(
                                            expert,
                                            request["families"],
                                            work_keys=request["keys"],
                                        )
                                    )
                                    expected = request.get(
                                        "generation", preview["generation"]
                                    )
                                    result = (
                                        guided.reuse(
                                            request["families"],
                                            expected_generation=expected,
                                            work_keys=request["keys"],
                                        )
                                        if route == "guided"
                                        else prepare_reuse(
                                            expert,
                                            request["families"],
                                            expected_generation=expected,
                                            work_keys=request["keys"],
                                        )
                                    )
                                    outputs.append(
                                        {
                                            "report": result["report"],
                                            "inventories": [
                                                {
                                                    "work_ordinal": r["work_ordinal"],
                                                    "work_key": r["work_key"],
                                                    "inventory": projection(
                                                        r["inventory"]
                                                    ),
                                                }
                                                for r in result["inventories"]
                                            ],
                                        }
                                    )
                                except WorkflowRefusalStudy as error:
                                    outputs.append(
                                        {"report": error.report, "inventories": None}
                                    )
                            assert outputs[0] == outputs[1]
                            actual = outputs[0]
                            assert (
                                actual["report"]["decision"]["code"]
                                == request["expected"]
                            )
                            assert actual["report"].get("query_admitted") is None
                            policy["tasks"].append(
                                {
                                    "task": request["task"],
                                    "equal_routes": True,
                                    "output": actual,
                                    "explanation": explain_reuse(actual["report"]),
                                }
                            )
                            assert ackredit.get_attribution().to_dict() == before_credit
                            checkpoint.retain()
                assert bytes_identity() == before
                report["inspection_and_reuse_preserved_all_store_bytes"] = True
                with FeatureStoreWorkflowStudy(args.store) as pinned:
                    changed = [dict(r) for r in rows]
                    changed[1]["work_key"] = "new literal key"
                    with FeatureStoreStudy(args.store) as writer:
                        second = writer.seal(changed)
                        writer.publish(second, expected_current=first)
                        second_attempt = next(
                            r["attempt"]
                            for r in writer.attempts()
                            if r["started"].get("candidate") == second
                        )
                    assert (
                        pinned.inspect(["hb donor"], work_keys=["nm"])["generation"]
                        == first
                    )
                    report["pinned_reader_generation"] = first
                after_refresh = bytes_identity()
                report["recovery"] = [
                    recover_publication(args.store, first_attempt),
                    recover_publication(args.store, second_attempt),
                ]
                assert [r["decision"]["code"] for r in report["recovery"]] == [
                    "publication_changed",
                    "candidate_is_current",
                ]
                try:
                    recover_publication(
                        args.store, second_attempt, retry=True, expected_current=second
                    )
                except WorkflowRefusalStudy as error:
                    assert error.code == "candidate_is_current"
                    report["needless_retry_refusal"] = error.report
                else:
                    raise AssertionError("Needless retry was accepted")
                assert bytes_identity() == after_refresh
                assert ackredit.get_attribution().to_dict() == before_credit
                report.update(
                    status="completed",
                    reading_created_no_credit=True,
                    pinned_session_did_not_switch=True,
                    recovery_did_not_write=True,
                    original_snapshot_bytes_sha256=[
                        hashlib.sha256(r["snapshot"]).hexdigest() for r in original
                    ],
                )
            except Exception as error:
                report.update(
                    status="failed",
                    failure={"type": type(error).__name__, "reason": str(error)},
                )
            checkpoint.retain()
        print(
            json.dumps(
                {
                    "status": report["status"],
                    "tasks": sum(len(p["tasks"]) for p in report["policies"]),
                    "human_participants": 0,
                }
            )
        )
        return 0 if report["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
