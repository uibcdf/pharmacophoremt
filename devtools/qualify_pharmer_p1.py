"""Opt-in PHMT receiving for frozen P1; the external Pharmer arm is unexecuted."""

import argparse
import hashlib
import importlib.metadata
import json
import sys
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, required=True, help="New original result file"
    )
    args = parser.parse_args(argv)
    # Refuse replacement before scientific imports or work.
    with args.output.open("x") as output:
        import ackredit

        import pharmacophoremt as phmt
        from phmt_test_support.pharmer_p1 import (
            DIRECTORY,
            expectation_passed,
            load_declaration,
            qualify_case,
        )

        declaration, _ = load_declaration()
        report = dict(
            schema="pharmacophoremt.pharmer-p1-result@1",
            case_id=declaration["case_id"],
            python=sys.version,
            runtime_version=phmt.__version__,
            versions={
                name: importlib.metadata.version(name)
                for name in (
                    "pharmacophoremt",
                    "molsysmt",
                    "numpy",
                    "pyunitwizard",
                    "ackredit",
                )
            },
            original_inputs={
                p.name: dict(
                    bytes=p.stat().st_size,
                    sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                )
                for p in sorted(DIRECTORY.glob("*.json"))
            },
            cases=[],
            external={
                "tool": "Pharmer standalone r95",
                "state": "not_executed",
                "reason": "Separate executable/input/feature/index/resource admission required",
            },
            scope="Analytical PHMT arm only; no external search, chemistry equivalence, activity, performance or public/platform qualification.",
        )

        def retain():
            output.seek(0)
            json.dump(report, output, indent=2, allow_nan=False)
            output.write("\n")
            output.truncate()
            output.flush()

        retain()
        with ackredit.session("Pharmer P1 PHMT arm"), phmt.attribution():
            for case in declaration["cases"]:
                row = dict(key=case["key"], expected=case["expected"])
                try:
                    row["actual"] = qualify_case(case)
                    row["expectation_passed"] = expectation_passed(case, row["actual"])
                    row["execution_status"] = "completed"
                except Exception as error:
                    row.update(
                        execution_status="failed",
                        expectation_passed=False,
                        error_type=type(error).__name__,
                        error=str(error),
                    )
                report["cases"].append(row)
                retain()
                print(
                    f"{case['key']}: {row['execution_status']}",
                    file=sys.stderr,
                    flush=True,
                )
            report["attribution"] = ackredit.get_attribution().to_dict()
        report["passed"] = all(row["expectation_passed"] for row in report["cases"])
        retain()
        report["native_extensions"] = []
        for name, module in sorted(sys.modules.items()):
            if not name.startswith(("molsysmt.", "rdkit.")) or not str(
                getattr(module, "__file__", "")
            ).endswith((".so", ".pyd")):
                continue
            with Path(module.__file__).open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            report["native_extensions"].append(
                dict(module=name, path=str(module.__file__), sha256=digest)
            )
        retain()
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
