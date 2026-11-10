"""Opt-in finite proposal-cost calibration; caller owns resource admission."""

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
    parser.add_argument("--sample", required=True, choices=("calibration", "paired"))
    parser.add_argument("--admission-sha256", required=True)
    args = parser.parse_args(argv)
    if not re.fullmatch("[a-f0-9]{64}", args.admission_sha256):
        raise ValueError("Declare the SHA-256 of the admitted execution context")
    with args.output.open("x"):
        import ackredit

        import pharmacophoremt as phmt
        from pharmacophoremt import pyunitwizard as puw
        from phmt_test_support.feature_snapshot_case import producer_context
        from phmt_test_support.retrieval_checkpoint import RetrievalCheckpoint
        from phmt_test_support.retrieval_cost import declaration, run_policy

        report = {
            "schema": "pharmacophoremt.retrieval-cost-result@1",
            "case_id": "equivalent-native-proposal-cost-v1",
            "status": "running",
            "python": sys.version,
            "producer": producer_context(args.admission_sha256),
            "original_snapshot_context": args.snapshot_context,
            "sample": args.sample,
            "policies": [],
            "production_index_selected": False,
        }
        with ackredit.session("Finite equivalent retrieval costs"), phmt.attribution():
            checkpoint = RetrievalCheckpoint(
                args.output, report, lambda: ackredit.get_attribution().to_dict()
            )
            checkpoint.retain()
            try:
                spec = declaration()
                units = (
                    [spec["calibration"]["unit_policy"]]
                    if args.sample == "calibration"
                    else spec["unit_policies"]
                )
                for unit in units:
                    policy = {"unit_policy": unit, "status": "running"}
                    report["policies"].append(policy)

                    def progress(state):
                        policy["scientific"] = state
                        checkpoint.retain()

                    with puw.context(standard_units=[unit, "ps", "radians"]):
                        policy["scientific"] = run_policy(
                            args.snapshot_context,
                            unit,
                            calibration=args.sample == "calibration",
                            progress=progress,
                        )
                    policy["status"] = "completed"
                    checkpoint.retain()
                report["status"] = "completed"
            except Exception as error:
                report.update(
                    status="failed",
                    failure={"type": type(error).__name__, "reason": str(error)},
                )
                if report["policies"] and report["policies"][-1]["status"] == "running":
                    report["policies"][-1]["status"] = "failed"
            checkpoint.retain()
        print(
            json.dumps(
                {
                    "status": report["status"],
                    "policies": len(report["policies"]),
                    "sample": args.sample,
                }
            )
        )
        return 0 if report["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
