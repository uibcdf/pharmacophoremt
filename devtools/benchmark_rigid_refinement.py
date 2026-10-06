"""Opt-in isolated refinement measurements; analytical controls, no timing gates.

Time only the public refinement call on prepared inventories. Capture a separate
attributed call and complete scientific traces; imports, preparation, warmup,
hashing, serialization, garbage collection and citation rendering are not timed.
RSS is whole-worker lifetime high-water memory, not incremental call allocation.
"""

import argparse
import gc
import hashlib
import json
import os
import platform
import statistics
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

from devtools.benchmark_rigid_consensus import (
    THREAD_VARS,
    _digest,
    _rss,
    _source_record,
)
from devtools.rigid_refinement_workloads import (
    INPUT_FILES,
    ROOT,
    build_workload,
    load_workloads,
)

POLICIES = ("final", "each_step")


def _worker(case, policy, repetitions, warmups):
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
    start = perf_counter()
    reference, source = build_workload(case)
    target = get_features(reference, features=case["features"])
    inventory = get_features(source, features=case["features"])
    preparation_seconds = perf_counter() - start

    def run():
        start = perf_counter()
        result = refine_rigid_feature_correspondences(
            source,
            target,
            case["correspondences"],
            features=case["features"],
            feature_inventory=inventory,
            orientation_policy=policy,
            **case["parameters"],
        )
        elapsed = perf_counter() - start
        report = dict(result["report"])
        report.pop("attribution", None)
        return report, elapsed, result.get("attribution")

    fingerprints, warmup_times, samples = [], [], []
    with phmt.attribution(False):
        for _ in range(warmups):
            report, elapsed, _ = run()
            warmup_times.append(elapsed)
            fingerprints.append(_digest(report))
            del report
            gc.collect()
        rss_before = _rss()
        for _ in range(repetitions):
            report, elapsed, _ = run()
            samples.append(elapsed)
            fingerprints.append(_digest(report))
            del report
            gc.collect()
        rss_after = _rss()
    with phmt.attribution():
        report, _, attribution = run()
    fingerprints.append(_digest(report))
    actual = dict(
        n_placements=len(report["accepted_placements"]),
        n_fits=report["n_fits"],
        max_matches=max(
            (len(p["matches"]["matches"]) for p in report["accepted_placements"]),
            default=0,
        ),
    )
    after = {name: _source_record(module) for name, module in tracked.items()}
    packages = dict(after)
    if "ackredit" in sys.modules:
        packages["ackredit"] = _source_record(sys.modules["ackredit"])
    extensions = []
    for name, module in sorted(sys.modules.items()):
        path = getattr(module, "__file__", None)
        if (
            name.startswith("molsysmt")
            and path
            and Path(path).suffix in {".so", ".pyd", ".dylib"}
        ):
            extensions.append(
                dict(
                    module=name,
                    path=path,
                    sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                )
            )
    return dict(
        case_id=case["case_id"],
        orientation_policy=policy,
        fixture=case,
        fixture_sha256=_digest(case),
        expected=case["expected"][policy],
        outcome=actual,
        expectation_passed=actual == case["expected"][policy],
        scientific_outputs_stable=len(set(fingerprints)) == 1,
        scientific_output_sha256=fingerprints[-1],
        source_hashes_unchanged=before == after,
        report=report,
        attribution=attribution,
        timing=dict(
            samples_seconds=samples,
            median_seconds=statistics.median(samples),
            min_seconds=min(samples),
            max_seconds=max(samples),
            warmup_call_seconds=warmup_times,
            fixture_and_inventory_seconds=preparation_seconds,
            scope="refine_rigid_feature_correspondences only; prepared inventory inputs; setup, warmup, GC, hashing, serialization and attribution excluded",
        ),
        memory=dict(
            process_lifetime_peak_rss_bytes_before_measurements=rss_before,
            process_lifetime_peak_rss_bytes_after_measurements=rss_after,
            scope="whole worker lifetime high-water RSS including imports/preparation/warmups; not incremental allocations; citation call excluded",
        ),
        environment=dict(
            python=sys.version,
            executable=sys.executable,
            platform=platform.platform(),
            machine=platform.machine(),
            cpu_count=os.cpu_count(),
            thread_environment={key: os.environ.get(key) for key in THREAD_VARS},
            molsysmt_policy=dict(
                parallel=msm.configure.parallel_mode,
                num_threads=msm.configure.get_num_threads(),
            ),
            packages=packages,
            versions=dict(numpy=np.__version__, scipy=scipy.__version__),
            molecular_extensions=extensions,
        ),
    )


def _passed(record):
    return all(
        record.get(key, False)
        for key in (
            "expectation_passed",
            "scientific_outputs_stable",
            "source_hashes_unchanged",
        )
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--case", action="append", dest="selected_cases")
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--warmups", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--worker", help=argparse.SUPPRESS)
    parser.add_argument("--policy", choices=POLICIES, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.repetitions < 1 or args.warmups < 0 or args.timeout <= 0:
        parser.error("require positive repetitions/timeout and nonnegative warmups")
    cases = load_workloads()
    if args.worker:
        case = next(case for case in cases if case["case_id"] == args.worker)
        args.output.write_text(
            json.dumps(
                _worker(case, args.policy, args.repetitions, args.warmups),
                indent=2,
                allow_nan=False,
            )
            + "\n"
        )
        return 0
    if args.selected_cases:
        unknown = set(args.selected_cases) - {case["case_id"] for case in cases}
        if unknown:
            parser.error("unknown cases: " + ", ".join(sorted(unknown)))
        cases = [case for case in cases if case["case_id"] in args.selected_cases]
    environment = dict(os.environ, **{key: "1" for key in THREAD_VARS})
    records = []
    inputs = (
        *INPUT_FILES,
        *(
            ROOT / ("devtools/" + name)
            for name in (
                "benchmark_rigid_refinement.py",
                "rigid_refinement_workloads.py",
                "rigid_refinement_cases.py",
                "rigid_consensus_cases.py",
                "benchmark_rigid_consensus.py",
            )
        ),
    )

    def identities():
        return {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in inputs
        }

    before = identities()
    with tempfile.TemporaryDirectory(prefix="phmt-refinement-benchmark-") as directory:
        for case in cases:
            for policy in POLICIES:
                output = Path(directory) / "worker.json"
                command = [
                    sys.executable,
                    "-m",
                    "devtools.benchmark_rigid_refinement",
                    "--worker",
                    case["case_id"],
                    "--policy",
                    policy,
                    "--output",
                    str(output),
                    "--repetitions",
                    str(args.repetitions),
                    "--warmups",
                    str(args.warmups),
                ]
                try:
                    process = subprocess.run(
                        command,
                        cwd=ROOT,
                        env=environment,
                        capture_output=True,
                        text=True,
                        timeout=args.timeout,
                    )
                    if process.returncode:
                        raise RuntimeError(
                            f"worker exit {process.returncode}: {process.stderr[-2000:]}"
                        )
                    record = json.loads(output.read_text())
                except (
                    subprocess.TimeoutExpired,
                    RuntimeError,
                    OSError,
                    ValueError,
                ) as error:
                    record = dict(
                        case_id=case["case_id"],
                        orientation_policy=policy,
                        worker_status="failed",
                        reason=str(error),
                    )
                records.append(record)
                print(
                    f"{case['case_id']} / {policy}: {'PASS' if _passed(record) else 'FAIL'}",
                    file=sys.stderr,
                    flush=True,
                )
    signatures = [
        _digest(
            dict(
                packages=r["environment"]["packages"],
                molecular_extensions=r["environment"]["molecular_extensions"],
            )
        )
        for r in records
        if "environment" in r
    ]
    same_sources = len(signatures) == len(records) and len(set(signatures)) == 1

    def git(*arguments):
        return subprocess.run(
            ["git", *arguments], cwd=ROOT, capture_output=True, text=True, check=False
        ).stdout.strip()

    result = dict(
        schema="pharmacophoremt.refinement_benchmark@1",
        recorded_at_utc=datetime.now(timezone.utc).isoformat(),
        source_head=git("rev-parse", "HEAD"),
        source_working_state=git("status", "--porcelain"),
        input_sha256=before,
        input_hashes_unchanged=before == identities(),
        worker_sources_identical=same_sources,
        repetitions=args.repetitions,
        warmups=args.warmups,
        worker_timeout_seconds=args.timeout,
        scope="analytical prepared fragments; no biological validation, conformational energies or universal ranking",
        records=records,
    )
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    return (
        0
        if same_sources
        and result["input_hashes_unchanged"]
        and all(_passed(r) for r in records)
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
