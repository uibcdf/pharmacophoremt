"""Opt-in fixed saved-reader engineering profile; never a molecular benchmark."""

import argparse
import datetime
import hashlib
import importlib.abc
import importlib.metadata
import json
import os
import platform
import resource
import shutil
import sqlite3
import statistics
import subprocess
import sys
from pathlib import Path

from phmt_test_support.saved_run_profile import (
    COUNTS,
    PADDING_BYTES,
    build_fixture,
    file_identity,
    measure,
    profile_fixture,
    recover_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
BLOCKED = {
    "pharmacophoremt",
    "molsysmt",
    "numpy",
    "scipy",
    "rdkit",
    "pyunitwizard",
    "ackredit",
}


class ReaderOnly(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split(".")[0] in BLOCKED:
            raise AssertionError("unexpected scientific import: " + fullname)


def memory_entry():
    memory = Path("/proc/meminfo").read_text()
    pressure = Path("/proc/pressure/memory").read_text()
    available = (
        int(
            next(
                row.split()[1]
                for row in memory.splitlines()
                if row.startswith("MemAvailable:")
            )
        )
        * 1024
    )
    assert available > 2 * 1024**3, "defer: insufficient available memory"
    assert all(
        float(row.split("avg10=")[1].split()[0]) < 1 for row in pressure.splitlines()
    ), "defer: memory pressure"
    return {"available_bytes": available, "pressure": pressure}


def context():
    assert not (BLOCKED & set(sys.modules))
    import pharmacophoremt_results as results

    assert (
        Path(results.__file__).resolve() == ROOT / "pharmacophoremt_results/__init__.py"
    )

    cpu = platform.processor()
    if Path("/proc/cpuinfo").exists():
        cpu = next(
            (
                row.split(":", 1)[1].strip()
                for row in Path("/proc/cpuinfo").read_text().splitlines()
                if row.startswith("model name")
            ),
            cpu,
        )
    return {
        "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": sys.version,
        "sqlite_version": sqlite3.sqlite_version,
        "platform": platform.platform(),
        "cpu_model": cpu,
        "load_average": list(os.getloadavg()),
        "affinity": sorted(os.sched_getaffinity(0)),
        "nice": os.getpriority(os.PRIO_PROCESS, 0),
        "rlimit_as": list(resource.getrlimit(resource.RLIMIT_AS)),
        "rlimit_data": list(resource.getrlimit(resource.RLIMIT_DATA)),
        "backend_threads": {
            name: os.environ.get(name)
            for name in (
                "OPENBLAS_NUM_THREADS",
                "OMP_NUM_THREADS",
                "MKL_NUM_THREADS",
                "NUMEXPR_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS",
                "BLIS_NUM_THREADS",
                "RAYON_NUM_THREADS",
            )
        },
        "reader_origin": results.__file__,
        "reader_source_files": {
            str(path.relative_to(ROOT)): file_identity(path)
            for path in sorted((ROOT / "pharmacophoremt_results").glob("*.py"))
        },
        "case_source_files": {
            str(path.relative_to(ROOT)): file_identity(path)
            for path in [
                ROOT / "phmt_test_support/saved_run_profile.py",
                Path(__file__),
            ]
        },
        "loaded_support_providers": {
            name: {
                "version": importlib.metadata.version(name),
                "origin": module.__file__,
            }
            for name in ("argdigest", "smonitor", "depdigest")
            if (module := sys.modules.get(name)) is not None
        },
        "cached_distribution_metadata": {
            "pharmacophoremt": importlib.metadata.version("pharmacophoremt")
        },
        "scientific_imports_blocked": sorted(BLOCKED),
        "aggregate_memory_swap_tasks_quota": "not enforced; no owned user cgroup",
        "scope": "Qualified existing source/provider context; not a public installed artifact or dependency solve.",
    }


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def copy_failed_fixture(source, destination):
    """Copy one declared interrupted preparation, never replay saved commands."""
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if destination.is_relative_to(source):
        raise ValueError("recovery output must be outside the original profile")
    report_path = source / "run.json"
    report_bytes = report_path.read_bytes()
    report_identity = {
        "bytes": len(report_bytes),
        "sha256": hashlib.sha256(report_bytes).hexdigest(),
    }
    report = json.loads(report_bytes)
    if (
        report.get("schema") != "pharmacophoremt.saved-reader-profile-run@1"
        or report.get("status") != "failed"
    ):
        raise ValueError("choose an original failed fixed-profile run")
    failed = report["commands"][-1]
    count = failed.get("count")
    if (
        failed.get("phase") != "prepare"
        or failed.get("timed_out") is not True
        or type(count) is not int
        or count not in COUNTS
    ):
        raise ValueError("recovery requires a declared preparation timeout")
    original = source / f"work-{count}"
    allowed = {"run.sqlite3", "run.sqlite3-journal", "work.jsonl"}
    paths = list(original.iterdir())
    if original.is_symlink() or any(
        p.is_symlink() or not p.is_file() or p.name not in allowed for p in paths
    ):
        raise ValueError("unexpected or linked partial-fixture files")
    files = {p.name: file_identity(p) for p in paths}
    if not {"run.sqlite3", "work.jsonl"} <= set(files):
        raise ValueError("partial fixture requires its database and manifest")
    case = destination / f"work-{count}"
    shutil.copytree(original, case)
    assert files == {p.name: file_identity(p) for p in case.iterdir()}
    assert file_identity(report_path) == report_identity
    return count, {
        "source_profile": str(source),
        "source_report_identity": report_identity,
        "source_case": str(original),
        "source_files": files,
        "copied_case": str(case),
        "original_preparation_qualified": False,
    }


def verify_original(recovery):
    assert (
        file_identity(Path(recovery["source_profile"]) / "run.json")
        == recovery["source_report_identity"]
    )
    for name, expected in recovery["source_files"].items():
        assert file_identity(Path(recovery["source_case"]) / name) == expected


def child(arguments):
    sys.meta_path.insert(0, ReaderOnly())
    entry = memory_entry()
    initial = context()
    if arguments.prepare is not None:
        configuration, timing = measure(
            lambda: build_fixture(arguments.prepare, arguments.count, PADDING_BYTES)
        )
        report = {
            "configuration": configuration,
            "preparation": timing,
            "context_before": initial,
            "context_after": context(),
            "memory_entry": entry,
        }
        write(arguments.prepare / "preparation.json", report)
    elif arguments.recover_fixture is not None:
        result, timing = measure(
            lambda: recover_fixture(
                arguments.recover_fixture, arguments.count, PADDING_BYTES
            )
        )
        write(
            arguments.recover_fixture / "recovery.json",
            {
                "result": result,
                "recovery": timing,
                "context_before": initial,
                "context_after": context(),
                "memory_entry": entry,
                "original_one_shot_preparation_qualified": False,
            },
        )
    else:
        destination = arguments.measure / "measurement.json"
        with destination.open("x", encoding="utf-8") as output:

            def retain(report):
                output.seek(0)
                json.dump(report, output, indent=2)
                output.write("\n")
                output.truncate()
                output.flush()

            result = profile_fixture(arguments.measure, repeats=5, on_update=retain)
            result.update(
                context_before=initial, context_after=context(), memory_entry=entry
            )
            result["whole_process_peak_rss_bytes"] = resource.getrusage(
                resource.RUSAGE_SELF
            ).ru_maxrss * (1 if sys.platform == "darwin" else 1024)
            result["sample_statistics"] = {
                operation: {
                    clock: {
                        "median_ns": statistics.median(row[clock] for row in rows),
                        "min_ns": min(row[clock] for row in rows),
                        "max_ns": max(row[clock] for row in rows),
                    }
                    for clock in ("wall_ns", "process_cpu_ns")
                }
                for operation, rows in result["samples"].items()
            }
            assert (
                result["context_before"]["reader_source_files"]
                == result["context_after"]["reader_source_files"]
            )
            assert (
                result["context_before"]["case_source_files"]
                == result["context_after"]["case_source_files"]
            )
            retain(result)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output", type=Path)
    group.add_argument("--prepare", type=Path, help=argparse.SUPPRESS)
    group.add_argument("--measure", type=Path, help=argparse.SUPPRESS)
    group.add_argument("--recover-fixture", type=Path, help=argparse.SUPPRESS)
    parser.add_argument(
        "--recover-from",
        type=Path,
        metavar="FAILED_PROFILE",
        help="Copy one interrupted preparation and profile its recovered reader; preserve the original failure.",
    )
    parser.add_argument("--count", type=int, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if args.recover_from is not None and args.output is None:
        parser.error("--recover-from requires a fresh --output directory")
    if args.output is None:
        return child(args)
    destination = args.output.resolve()
    destination.mkdir()
    report = {
        "schema": "pharmacophoremt.saved-reader-profile-run@1",
        "status": "running",
        "sizes": list(COUNTS),
        "padding_bytes": PADDING_BYTES,
        "commands": [],
        "cases": [],
        "scope": "Synthetic reader engineering profile only; OS cache uncontrolled, no speedup or molecular throughput.",
    }
    report_path = destination / "run.json"
    write(report_path, report)
    try:
        counts = COUNTS
        phases = ("prepare", "measure")
        if args.recover_from is not None:
            memory_entry()
            # Inspect only fixed control metadata; execute our known module/flags.
            count, recovery = copy_failed_fixture(args.recover_from, destination)
            report.update(
                schema="pharmacophoremt.saved-reader-profile-recovery@1",
                recovery=recovery,
                sizes=[count],
                scope="One separately bounded copied-fixture recovery and missed reader phase. Original failed preparation remains unqualified; no molecular throughput claim.",
            )
            counts, phases = (count,), ("recover-fixture", "measure")
            write(report_path, report)
        for count in counts:
            case = destination / f"work-{count}"
            for phase in phases:
                entry = memory_entry()
                command = [
                    sys.executable,
                    "-B",
                    "-m",
                    "devtools.profile_saved_run",
                    "--" + phase,
                    str(case),
                ]
                if phase in {"prepare", "recover-fixture"}:
                    command.extend(["--count", str(count)])
                stdout = destination / f"{phase}-{count}.stdout"
                stderr = destination / f"{phase}-{count}.stderr"
                record = {
                    "phase": phase,
                    "count": count,
                    "arguments": command,
                    "memory_entry": entry,
                }
                report["commands"].append(record)
                write(report_path, report)
                try:
                    with stdout.open("xb") as out, stderr.open("xb") as error:
                        completed = subprocess.run(
                            command,
                            cwd=ROOT,
                            stdout=out,
                            stderr=error,
                            timeout=180,
                            check=False,
                        )
                    record.update(
                        exit_code=completed.returncode,
                        stdout=file_identity(stdout),
                        stderr=file_identity(stderr),
                    )
                except subprocess.TimeoutExpired:
                    record.update(
                        timed_out=True,
                        timeout_seconds=180,
                        stdout=file_identity(stdout),
                        stderr=file_identity(stderr),
                    )
                    raise
                write(report_path, report)
                if completed.returncode:
                    raise RuntimeError(
                        f"{phase} failed for {count}; retain original logs"
                    )
            measurement = json.loads((case / "measurement.json").read_text())
            assert measurement["status"] == "completed"
            report["cases"].append(
                {
                    "count": count,
                    "measurement": str(
                        (case / "measurement.json").relative_to(destination)
                    ),
                    "identity": file_identity(case / "measurement.json"),
                }
            )
            write(report_path, report)
            print(f"{count}: verified profile complete", flush=True)
        report["status"] = "completed"
        if args.recover_from is not None:
            verify_original(report["recovery"])
            report["original_files_unchanged"] = True
    except BaseException as error:
        report.update(
            status="failed", error_type=type(error).__name__, error=str(error)
        )
        write(report_path, report)
        raise
    write(report_path, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
