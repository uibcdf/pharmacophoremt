"""Opt-in fixed saved-reader engineering profile; never a molecular benchmark."""

import argparse
import datetime
import importlib.abc
import importlib.metadata
import json
import os
import platform
import resource
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
    parser.add_argument("--count", type=int, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
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
        for count in COUNTS:
            case = destination / f"work-{count}"
            for phase in ("prepare", "measure"):
                entry = memory_entry()
                command = [
                    sys.executable,
                    "-B",
                    "-m",
                    "devtools.profile_saved_run",
                    "--" + phase,
                    str(case),
                ]
                if phase == "prepare":
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
