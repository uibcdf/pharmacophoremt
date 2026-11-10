"""Opt-in six-family native retrieval case; caller admits and limits resources."""

import argparse
import json
import re
import sys
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--snapshot-context", required=True, choices=("source", "installed")
    )
    parser.add_argument("--admission-sha256", required=True)
    args = parser.parse_args(argv)
    if not re.fullmatch("[a-f0-9]{64}", args.admission_sha256):
        raise ValueError("Declare the SHA-256 of the admitted execution context")
    with args.output.open("x") as output:
        import ackredit

        import pharmacophoremt as phmt
        from pharmacophoremt import pyunitwizard as puw
        from phmt_test_support.feature_snapshot_case import producer_context
        from phmt_test_support.typed_retrieval import (
            DIRECTORY,
            compare_domain,
            declaration,
            identity,
            load_entries,
        )

        report = {
            "schema": "pharmacophoremt.typed-retrieval-result@1",
            "case_id": "six-family-native-retrieval-v1",
            "status": "running",
            "python": sys.version,
            "producer": producer_context(args.admission_sha256),
            "original_snapshot_context": args.snapshot_context,
            "original_snapshot_manifest": identity(DIRECTORY / "originals.json"),
            "policies": [],
            "performance_measured": False,
            "final_pose_or_activity_acceptance": False,
        }

        def retain():
            output.seek(0)
            json.dump(report, output, indent=2, allow_nan=False)
            output.write("\n")
            output.truncate()
            output.flush()

        retain()
        with ackredit.session("Six-family native retrieval"), phmt.attribution():
            try:
                spec = declaration()
                entries = load_entries(args.snapshot_context)
                for unit in spec["unit_contexts"]:
                    policy = {"unit_policy": unit, "status": "running"}
                    report["policies"].append(policy)
                    credits_before = ackredit.get_attribution().to_dict()

                    def progress(state):
                        if not policy.get("reading_originals_created_no_credit"):
                            assert state["reference_calls"] == {
                                "exhaustive": 0,
                                "retrieved": 0,
                            }
                            assert (
                                ackredit.get_attribution().to_dict() == credits_before
                            )
                            policy["reading_originals_created_no_credit"] = True
                        policy["scientific"] = state
                        retain()

                    with puw.context(standard_units=[unit, "ps", "radians"]):
                        policy["scientific"] = compare_domain(
                            entries, spec, progress=progress
                        )
                    policy["status"] = "completed"
                    retain()
                report["status"] = "completed"
            except Exception as error:
                report.update(
                    status="failed",
                    failure={"type": type(error).__name__, "reason": str(error)},
                )
                if report["policies"] and report["policies"][-1]["status"] == "running":
                    report["policies"][-1]["status"] = "failed"
            report["actual_attribution"] = ackredit.get_attribution().to_dict()
        retain()
        print(
            json.dumps(
                {
                    "status": report["status"],
                    "complete_policies": sum(
                        p["status"] == "completed" for p in report["policies"]
                    ),
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
