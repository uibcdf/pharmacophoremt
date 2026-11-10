"""Opt-in persistence/retrieval study; caller admits and limits resources."""

import argparse
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
        raise ValueError("Declare the SHA-256 of the admitted execution context")
    with args.output.open("x"):
        import ackredit

        import pharmacophoremt as phmt
        from pharmacophoremt import pyunitwizard as puw
        from phmt_test_support.feature_snapshot import FeatureSnapshotStudy
        from phmt_test_support.feature_snapshot_case import producer_context
        from phmt_test_support.feature_store import (
            FeatureStoreReaderStudy,
            FeatureStoreStudy,
        )
        from phmt_test_support.retrieval_checkpoint import RetrievalCheckpoint
        from phmt_test_support.typed_retrieval import (
            compare_domain,
            declaration,
            load_entries,
        )

        report = {
            "schema": "pharmacophoremt.feature-store-retrieval-result@1",
            "status": "running",
            "producer": producer_context(args.admission_sha256),
            "original_snapshot_context": args.snapshot_context,
            "policies": [],
            "performance_measured": False,
            "persisted_lookup_index": False,
            "final_pose_or_activity_acceptance": False,
        }
        with ackredit.session("Immutable feature-store retrieval"), phmt.attribution():
            checkpoint = RetrievalCheckpoint(
                args.output, report, lambda: ackredit.get_attribution().to_dict()
            )
            checkpoint.retain()
            try:
                original = load_entries(args.snapshot_context)
                rows = []
                credits_before = ackredit.get_attribution().to_dict()
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
                    generation = writer.seal(rows)
                    writer.publish(generation, expected_current=None)
                    report["operations"] = writer.attempts()
                with FeatureStoreReaderStudy(args.store) as reader:
                    report["generation"] = reader.describe()
                    reopened = [
                        {"work_key": r["work_key"], "snapshot": r["snapshot"]}
                        for r in reader.entries()
                    ]
                assert reopened == original
                assert ackredit.get_attribution().to_dict() == credits_before
                report["roundtrip_preserves_original_bytes_order_and_credit"] = True
                checkpoint.retain()
                spec = declaration()
                for unit in spec["unit_contexts"]:
                    policy = {"unit_policy": unit, "status": "running"}
                    report["policies"].append(policy)

                    def progress(state):
                        policy["scientific"] = state
                        checkpoint.retain()

                    with puw.context(standard_units=[unit, "ps", "radians"]):
                        policy["scientific"] = compare_domain(
                            reopened, spec, progress=progress
                        )
                    policy["status"] = "completed"
                    checkpoint.retain()
                report["status"] = "completed"
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
                    "complete_rows": sum(
                        len(p.get("scientific", {}).get("rows", []))
                        for p in report["policies"]
                    ),
                }
            )
        )
        return 0 if report["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
