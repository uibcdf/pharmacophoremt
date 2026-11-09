"""Freeze P1 molecular exports; no external engine is acquired or executed."""

import argparse
import hashlib
import importlib.metadata
import json
import sys
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-directory", type=Path, required=True)
    args = parser.parse_args(argv)
    # Claim a new owned directory before scientific imports; never replace work.
    args.output_directory.mkdir()
    with (args.output_directory / "manifest.json").open("x") as stream:
        import pharmacophoremt as phmt
        from phmt_test_support.pharmer_p1 import DIRECTORY, load_declaration
        from phmt_test_support.pharmer_p1_export import export_case

        declaration, _ = load_declaration()
        report = {
            "schema": "pharmacophoremt.pharmer-p1-exports@1",
            "issue": "uibcdf/pharmacophoremt#164",
            "case_id": declaration["case_id"],
            "python": sys.version,
            "runtime_version": phmt.__version__,
            "versions": {
                n: importlib.metadata.version(n)
                for n in ("pharmacophoremt", "molsysmt", "pyunitwizard", "numpy")
            },
            "original_inputs": {
                p.name: {
                    "bytes": p.stat().st_size,
                    "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                }
                for p in sorted(DIRECTORY.glob("*.json"))
            },
            "cases": [],
            "external": "not_executed",
            "scope": "Molecular export/round-trip only; no perception, search, activity or performance qualification.",
        }

        def retain():
            stream.seek(0)
            json.dump(report, stream, indent=2, allow_nan=False)
            stream.write("\n")
            stream.truncate()
            stream.flush()

        retain()
        for case in declaration["cases"]:
            row = {"key": case["key"]}
            try:
                row["actual"] = export_case(
                    case, args.output_directory / (case["key"] + ".sdf")
                )
                row["status"] = "verified-export"
            except Exception as error:
                row.update(
                    status="failed-export",
                    error_type=type(error).__name__,
                    error=str(error),
                )
            report["cases"].append(row)
            retain()
        report["passed"] = all(
            row["status"] == "verified-export" for row in report["cases"]
        )
        retain()
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
