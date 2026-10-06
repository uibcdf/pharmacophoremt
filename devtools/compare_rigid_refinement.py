"""Opt-in analytical scientific comparison; this is not a timing benchmark."""

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from devtools.benchmark_rigid_consensus import THREAD_VARS, _digest, _source_record
from devtools.rigid_refinement_cases import (
    CASES_PATH,
    build_refinement_case,
    load_refinement_cases,
)

ROOT = Path(__file__).resolve().parents[1]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=CASES_PATH)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    for name in THREAD_VARS:
        os.environ[name] = "1"

    import molsysmt as msm
    import numpy as np
    import pyunitwizard as puw
    import scipy

    import pharmacophoremt as phmt
    from pharmacophoremt.modeler import get_features
    from pharmacophoremt.screening import refine_rigid_feature_correspondences

    msm.configure.set_parallelization(parallel=False, num_threads=1)
    tracked = {"pharmacophoremt": phmt, "molsysmt": msm, "pyunitwizard": puw}
    before = {name: _source_record(module) for name, module in tracked.items()}
    records = []
    for case in load_refinement_cases(args.cases):
        reference, source = build_refinement_case(case)
        target = get_features(reference, features=["hb donor"])
        inventory = get_features(source, features=["hb donor"])
        for policy in ("final", "each_step"):
            reports, attribution = [], None
            for enabled in (False, True):
                with phmt.attribution(enabled):
                    result = refine_rigid_feature_correspondences(
                        source,
                        target,
                        case["correspondences"],
                        features=["hb donor"],
                        feature_inventory=inventory,
                        orientation_policy=policy,
                        **case["parameters"],
                    )
                reports.append(result["report"])
                if enabled:
                    attribution = result["attribution"]
            # Attribution is a separate top-level payload, not scientific output.
            scientific = [
                {k: v for k, v in report.items() if k != "attribution"}
                for report in reports
            ]
            stable = _digest(scientific[0]) == _digest(scientific[1])
            report = scientific[0]
            counts = dict(
                n_fits=report["n_fits"],
                n_placements=len(report["accepted_placements"]),
                max_matches=max(
                    (
                        len(p["matches"]["matches"])
                        for p in report["accepted_placements"]
                    ),
                    default=0,
                ),
            )
            passed = counts == case["expected"][policy]
            record = dict(
                case_id=case["case_id"],
                orientation_policy=policy,
                fixture_sha256=_digest(case),
                parameters=case["parameters"],
                expected=case["expected"][policy],
                counts=counts,
                expectation_passed=passed,
                scientific_outputs_stable=stable,
                scientific_output_sha256=_digest(scientific[0]),
                report=report,
                attribution=attribution,
            )
            records.append(record)
            print(
                f"{case['case_id']} / {policy}: {'PASS' if passed and stable else 'FAIL'}",
                file=sys.stderr,
                flush=True,
            )
    packages = {name: _source_record(module) for name, module in tracked.items()}
    unchanged = packages == before
    if "ackredit" in sys.modules:
        packages["ackredit"] = _source_record(sys.modules["ackredit"])
    extensions = [
        dict(
            module=name,
            path=str(module.__file__),
            sha256=hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest(),
        )
        for name, module in sorted(sys.modules.items())
        if name.startswith("molsysmt")
        and getattr(module, "__file__", None)
        and Path(module.__file__).suffix in {".so", ".pyd", ".dylib"}
    ]

    def git(*arguments):
        return subprocess.run(
            ["git", *arguments], cwd=ROOT, capture_output=True, text=True, check=False
        ).stdout.strip()

    output = dict(
        schema="pharmacophoremt.analytical_refinement_comparison@1",
        recorded_at_utc=datetime.now(timezone.utc).isoformat(),
        scope="analytical scientific counts and actual attribution; no runtime/memory benchmark or biological claim",
        calls="one uncredited and one attributed call per case/policy; identical scientific outputs required",
        fixture_file=str(args.cases.resolve()),
        fixture_sha256=hashlib.sha256(args.cases.read_bytes()).hexdigest(),
        driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        builder_sha256=hashlib.sha256(
            (ROOT / "devtools/rigid_refinement_cases.py").read_bytes()
        ).hexdigest(),
        source_head=git("rev-parse", "HEAD"),
        source_working_state=git("status", "--porcelain"),
        source_hashes_unchanged_during_execution=unchanged,
        environment=dict(
            python=sys.version,
            executable=sys.executable,
            platform=platform.platform(),
            packages=packages,
            versions=dict(numpy=np.__version__, scipy=scipy.__version__),
            molecular_extensions=extensions,
            thread_environment={name: os.environ[name] for name in THREAD_VARS},
            molsysmt_policy=dict(
                parallel=msm.configure.parallel_mode,
                num_threads=msm.configure.get_num_threads(),
            ),
        ),
        records=records,
    )
    args.output.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")
    return (
        0
        if unchanged
        and all(
            r["expectation_passed"] and r["scientific_outputs_stable"] for r in records
        )
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
