"""Opt-in isolated analytical comparison; no timing thresholds or biological claims.

Run as a module from the checkout:
python -m devtools.benchmark_rigid_consensus --output /tmp/rigid-comparison.json
Each case/strategy has its own worker. Imports/fixture construction and warmups
are excluded from measured call times; summaries and attribution are separate.
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

from devtools.rigid_consensus_cases import CASES_PATH, build_case, load_cases

STRATEGIES = ("association_cliques", "triplet_seeds", "ranked_triplet_seeds")
ROOT = Path(__file__).resolve().parents[1]
THREAD_VARS = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMBA_NUM_THREADS",
    "RAYON_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
)


def _digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, allow_nan=False).encode()
    ).hexdigest()


def _rss():
    if sys.platform not in {"linux", "darwin"}:
        return None
    import resource

    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value * (1024 if sys.platform == "linux" else 1))


def _source_record(package):
    directory = Path(package.__file__).resolve().parent
    files = [
        (
            str(path.relative_to(directory)),
            hashlib.sha256(path.read_bytes()).hexdigest(),
        )
        for path in sorted(directory.rglob("*.py"))
    ]
    return dict(
        path=str(directory),
        version=str(getattr(package, "__version__", "unknown")),
        python_source_sha256=_digest(files),
        python_file_count=len(files),
    )


def _run(ligands, parameters, strategy):
    from pharmacophoremt.modeler import from_rigid_ligands
    from pharmacophoremt.validation import summarize_rigid_consensus

    start = perf_counter()
    try:
        raw = from_rigid_ligands(
            ligands, correspondence_strategy=strategy, **parameters
        )
    except Exception as error:
        elapsed = perf_counter() - start
        return (
            dict(
                status="failed",
                error_type=type(error).__name__,
                error_code=getattr(error, "code", None),
                error_message=str(error),
                error_context=getattr(error, "extra", {}),
            ),
            elapsed,
            None,
        )
    elapsed = perf_counter() - start
    summary = summarize_rigid_consensus(raw["report"])
    return (
        dict(
            status="completed" if summary["n_models"] else "completed_empty",
            summary=summary,
        ),
        elapsed,
        raw,
    )


def _matches_expectation(outcome, expected):
    if outcome["status"] != expected["status"]:
        return False
    if expected["status"] == "failed":
        return outcome.get("error_code") == expected["error_code"]
    return all(
        outcome["summary"][key] == value
        for key, value in expected.items()
        if key != "status"
    )


def _worker(case, strategy, repetitions, warmups):
    setup_start = perf_counter()
    import molsysmt as msm
    import networkx as nx
    import numpy as np
    import pyunitwizard as puw
    import scipy

    import pharmacophoremt as phmt

    msm.configure.set_parallelization(parallel=False, num_threads=1)
    ligands = build_case(case)
    parameters = dict(
        case["parameters"], **case.get("strategy_parameters", {}).get(strategy, {})
    )
    setup_seconds = perf_counter() - setup_start
    warmup_times = []
    baseline = None
    with phmt.attribution(False):
        for _ in range(warmups):
            outcome, elapsed, raw = _run(ligands, parameters, strategy)
            warmup_times.append(elapsed)
            baseline = baseline or _digest(outcome)
            if _digest(outcome) != baseline:
                raise RuntimeError("scientific outputs changed between warmup calls")
            del raw
            gc.collect()
        rss_before = _rss()
        samples, outcomes = [], []
        for _ in range(repetitions):
            outcome, elapsed, raw = _run(ligands, parameters, strategy)
            samples.append(elapsed)
            outcomes.append(outcome)
            del raw
            gc.collect()
        rss_after = _rss()
    fingerprints = [_digest(outcome) for outcome in outcomes]
    stable = len(set(fingerprints + ([baseline] if baseline else []))) == 1
    # Deliberate separate citation run: tracking/rendering is not timed.
    with phmt.attribution():
        credited, _, raw = _run(ligands, parameters, strategy)
    attribution = None if raw is None else raw.get("attribution")
    stable = stable and _digest(credited) == fingerprints[0]
    packages = {
        name: _source_record(package)
        for name, package in (
            ("pharmacophoremt", phmt),
            ("molsysmt", msm),
            ("pyunitwizard", puw),
        )
    }
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
    expected = case["expected"][strategy]
    return dict(
        case_id=case["case_id"],
        strategy=strategy,
        fixture_sha256=_digest(case),
        parameters=parameters,
        expected=expected,
        expectation_passed=all(
            _matches_expectation(outcome, expected) for outcome in outcomes
        )
        and _matches_expectation(credited, expected),
        scientific_outputs_stable=stable,
        outcome=outcomes[0],
        scientific_output_sha256=fingerprints[0],
        timing=dict(
            samples_seconds=samples,
            median_seconds=statistics.median(samples),
            min_seconds=min(samples),
            max_seconds=max(samples),
            warmup_call_seconds=warmup_times,
            imports_and_fixture_seconds=setup_seconds,
            scope="from_rigid_ligands_only; imports, fixture construction, warmups, summary and attribution excluded",
        ),
        memory=dict(
            process_lifetime_peak_rss_bytes_before_measurements=rss_before,
            process_lifetime_peak_rss_bytes_after_measurements=rss_after,
            scope="whole worker high-water RSS, including imports, fixture and warmups; not per-call incremental allocation; unavailable on other platforms",
        ),
        environment=dict(
            python=sys.version,
            executable=sys.executable,
            platform=platform.platform(),
            machine=platform.machine(),
            processor=platform.processor(),
            cpu_count=os.cpu_count(),
            thread_environment={key: os.environ.get(key) for key in THREAD_VARS},
            molsysmt_policy=dict(
                parallel=msm.configure.parallel_mode,
                num_threads=msm.configure.get_num_threads(),
            ),
            packages=packages,
            versions=dict(
                numpy=np.__version__, scipy=scipy.__version__, networkx=nx.__version__
            ),
            molecular_extensions=extensions,
        ),
        attribution=attribution,
        attribution_scope="separate identical call; failed calculations have no completed host attribution payload",
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--cases", type=Path, default=CASES_PATH)
    parser.add_argument("--case", action="append", dest="selected_cases")
    parser.add_argument("--repetitions", type=int, default=3)
    parser.add_argument("--warmups", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--worker", help=argparse.SUPPRESS)
    parser.add_argument("--strategy", choices=STRATEGIES, help=argparse.SUPPRESS)
    parser.add_argument(
        "--strategies", nargs="+", choices=STRATEGIES, default=list(STRATEGIES[:2])
    )
    args = parser.parse_args(argv)
    if args.repetitions < 1 or args.warmups < 0 or args.timeout <= 0:
        parser.error("require positive repetitions/timeout and nonnegative warmups")
    cases = load_cases(args.cases)
    if args.worker:
        case = next(case for case in cases if case["case_id"] == args.worker)
        args.output.write_text(
            json.dumps(
                _worker(case, args.strategy, args.repetitions, args.warmups),
                indent=2,
                allow_nan=False,
            )
            + "\n"
        )
        return 0
    if args.output is None:
        parser.error("--output is required")
    if args.selected_cases:
        unknown = set(args.selected_cases) - {case["case_id"] for case in cases}
        if unknown:
            parser.error("unknown cases: " + ", ".join(sorted(unknown)))
        cases = [case for case in cases if case["case_id"] in args.selected_cases]
    if len(set(args.strategies)) != len(args.strategies):
        parser.error("strategies must be unique")
    for case in cases:
        if any(strategy not in case["expected"] for strategy in args.strategies):
            parser.error(
                f"case {case['case_id']} lacks a selected strategy expectation"
            )
    environment = dict(os.environ, **{key: "1" for key in THREAD_VARS})
    records = []
    with tempfile.TemporaryDirectory(prefix="phmt-rigid-benchmark-") as directory:
        for case in cases:
            for strategy in args.strategies:
                output = Path(directory) / "worker.json"
                command = [
                    sys.executable,
                    "-m",
                    "devtools.benchmark_rigid_consensus",
                    "--worker",
                    case["case_id"],
                    "--strategy",
                    strategy,
                    "--output",
                    str(output),
                    "--cases",
                    str(args.cases.resolve()),
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
                        strategy=strategy,
                        worker_status="failed",
                        reason=str(error),
                        expectation_passed=False,
                        scientific_outputs_stable=False,
                    )
                records.append(record)
                print(
                    f"{case['case_id']} / {strategy}: "
                    + (
                        "PASS"
                        if record["expectation_passed"]
                        and record["scientific_outputs_stable"]
                        else "FAIL"
                    ),
                    file=sys.stderr,
                    flush=True,
                )

    def git(*arguments):
        return subprocess.run(
            ["git", *arguments], cwd=ROOT, capture_output=True, text=True, check=False
        ).stdout.strip()

    report = dict(
        schema="pharmacophoremt.analytical_rigid_comparison@1",
        recorded_at_utc=datetime.now(timezone.utc).isoformat(),
        fixture_file=str(args.cases.resolve()),
        fixture_file_sha256=hashlib.sha256(args.cases.read_bytes()).hexdigest(),
        driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        case_builder_sha256=hashlib.sha256(
            (ROOT / "devtools/rigid_consensus_cases.py").read_bytes()
        ).hexdigest(),
        source_head=git("rev-parse", "HEAD"),
        source_working_state=git("status", "--porcelain"),
        repetitions=args.repetitions,
        warmups=args.warmups,
        worker_timeout_seconds=args.timeout,
        strategies=args.strategies,
        fixture_scope="analytical fragment controls; not biological validation or a universal strategy ranking",
        records=records,
    )
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    return (
        0
        if all(
            record["expectation_passed"] and record["scientific_outputs_stable"]
            for record in records
        )
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
