"""Run the fixed retrieval case after explicit task-owned source admission."""

import argparse
import importlib.metadata
import json
import sys
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    with args.output.open("x") as output:
        import ackredit

        import pharmacophoremt as phmt
        from phmt_test_support.retrieval_controls import (
            compare_retrieval,
            load_declaration,
        )

        report = {
            "schema": "pharmacophoremt.retrieval-controls-result@1",
            "case_id": "typed-distance-retrieval-v1",
            "python": sys.version,
            "runtime_version": phmt.__version__,
            "versions": {
                n: importlib.metadata.version(n)
                for n in (
                    "pharmacophoremt",
                    "molsysmt",
                    "numpy",
                    "networkx",
                    "pyunitwizard",
                    "ackredit",
                )
            },
            "status": "running",
            "molecular_inputs": 0,
            "performance_measured": False,
        }

        def retain(state=None):
            if state is not None:
                report["scientific"] = state
            output.seek(0)
            json.dump(report, output, indent=2, allow_nan=False)
            output.write("\n")
            output.truncate()
            output.flush()

        with ackredit.session("Finite typed-distance retrieval"), phmt.attribution():
            try:
                report["scientific"] = compare_retrieval(
                    load_declaration(), progress=retain
                )
                report["status"] = "completed"
            except Exception as error:
                report.update(
                    status="failed",
                    failure={"type": type(error).__name__, "reason": str(error)},
                )
            report["actual_attribution"] = ackredit.get_attribution().to_dict()
        retain()
        print(
            json.dumps(
                {
                    "status": report["status"],
                    "completed_rows": len(report.get("scientific", {}).get("rows", [])),
                }
            )
        )
        return 0 if report["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
