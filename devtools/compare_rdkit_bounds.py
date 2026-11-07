"""Opt-in fixed-distance pharmacophore comparison; not a timing benchmark."""

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    # Refuse an existing owned destination before starting scientific work.
    with args.output.open("x", encoding="utf-8") as output:
        import ackredit
        import molsysmt
        import rdkit

        import pharmacophoremt as phmt
        from phmt_test_support.benchmark_rigid_consensus import (
            THREAD_VARS,
            _source_record,
        )
        from phmt_test_support.rdkit_bounds_comparison import (
            CASES_PATH,
            compare_case,
            expectation_passed,
            load_cases,
        )

        tracked = dict(pharmacophoremt=phmt, molsysmt=molsysmt, rdkit=rdkit)
        before = {name: _source_record(module) for name, module in tracked.items()}
        inputs = [
            CASES_PATH,
            ROOT / "phmt_test_support/rdkit_bounds_comparison.py",
            Path(__file__),
        ]
        report = dict(
            schema="pharmacophoremt.rdkit-bounds-comparison@1",
            recorded_at_utc=datetime.now(timezone.utc).isoformat(),
            source_parent=subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            python=sys.version,
            platform=platform.platform(),
            threads={name: os.environ.get(name) for name in THREAD_VARS},
            sources_before=before,
            input_code_identities={
                str(path.relative_to(ROOT)): dict(
                    bytes=path.stat().st_size,
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                )
                for path in inputs
            },
            provider_versions={
                name: importlib.metadata.version(name)
                for name in [
                    "molsysmt",
                    "rdkit",
                    "numpy",
                    "pyunitwizard",
                    "argdigest",
                    "smonitor",
                    "depdigest",
                    "ackredit",
                ]
            },
            cases=[],
            scope="Analytical distance filters and native rigid placements; no independent chemical perception, embedding, benchmark, activity cohort or installed/public-platform qualification.",
        )

        def retain():
            output.seek(0)
            json.dump(report, output, indent=2, ensure_ascii=False, allow_nan=False)
            output.write("\n")
            output.truncate()
            output.flush()

        with ackredit.session("Pharm3D bounds comparison"), phmt.attribution():
            rdkit_credit = (
                f"pharmacophoremt:comparison:software:rdkit:{rdkit.__version__}"
            )
            ackredit.register_item(
                id=rdkit_credit,
                type="software",
                title="RDKit",
                version=rdkit.__version__,
                url="https://www.rdkit.org/",
            )
            for case in load_cases():
                row = dict(key=case["key"], expected=case["expected"])
                try:
                    row["actual"] = compare_case(case)
                    with ackredit.scope(
                        "devtools.compare_rdkit_bounds.completed_filter"
                    ):
                        ackredit.track_item(rdkit_credit)
                    row["expectation_passed"] = expectation_passed(case, row["actual"])
                    row["execution_status"] = "completed"
                except Exception as error:
                    row.update(
                        execution_status="failed",
                        expectation_passed=False,
                        error_type=type(error).__name__,
                        error_code=getattr(error, "code", None),
                        error=str(error),
                    )
                report["cases"].append(row)
                retain()
                print(
                    f"{case['key']}: {'PASS' if row['expectation_passed'] else 'FAIL'}",
                    file=sys.stderr,
                    flush=True,
                )
            report["attribution"] = ackredit.get_attribution().to_dict()
        report["sources_after"] = {
            name: _source_record(module) for name, module in tracked.items()
        }
        report["sources_unchanged"] = report["sources_after"] == before
        report["native_extensions"] = [
            dict(
                module=name,
                path=str(module.__file__),
                sha256=hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest(),
            )
            for name, module in sorted(sys.modules.items())
            if name.startswith(("molsysmt.", "rdkit."))
            and getattr(module, "__file__", None)
            and str(module.__file__).endswith((".so", ".pyd"))
        ]
        report["passed"] = report["sources_unchanged"] and all(
            row["expectation_passed"] for row in report["cases"]
        )
        retain()
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
