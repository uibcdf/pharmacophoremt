"""Fixed #148 hosted receiving client, not a benchmark or general executor.

Only the existing public-fixture selection is admitted. Standard systemd/kernel
controls own resource enforcement; the common SDK owns environment creation and
installed dependency checks. No original benchmark snapshot is read or uploaded.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import re
import resource
import runpy
import signal
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SDK = "1c248b67d1daea256ed7c7f6172c6addb3f0b08f"
PROBE = ".github/workflows/feature_reuse_resource_probe.yaml"
PROBE_SHA = "f983e38a0279eaa0511b7134f22cdf122bae394b936709ab7d0fdb1b79c917a0"
SOURCE_INPUT = "devtools/requirements/controlled_suite_dependencies_py314.txt"
SOURCE_SHA = "380a0d5f758ab7cd375eed70da34f00768f2a0ea6d3f9eb20009ec40997f01ab"
MANAGER_SHA = "80057e007579d482a39dc283dd3e725503e34da7e7c51844957164511cdb917b"
SELECTORS = (
    "tests/test_feature_reuse_experiment.py",
    "tests/test_modular_rigid_tools.py",
    "tests/test_correspondence_geometry.py",
)
THREADS = (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "RAYON_NUM_THREADS",
    "NUMBA_NUM_THREADS",
    "BLIS_NUM_THREADS",
    "GOMAXPROCS",
    "CARGO_BUILD_JOBS",
)
MARGIN = 1610612736


def identity(path):
    digest = hashlib.sha256()
    size = 0
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
            size += len(block)
    return {"bytes": size, "sha256": digest.hexdigest()}


def fixed_inputs(root=ROOT):
    """Reject changed declarations before any installer or native process."""
    if identity(root / PROBE)["sha256"] != PROBE_SHA:
        raise ValueError("review the changed resource-probe source first")
    if identity(root / SOURCE_INPUT)["sha256"] != SOURCE_SHA:
        raise ValueError("review the changed pinned dependency input first")
    original = json.loads(
        (root / "devguide/evidence/feature_reuse_execution_20261107.json").read_text()
    )
    if original["scientific_selectors"] != list(SELECTORS):
        raise ValueError("the fixed native selection changed")
    for path in SELECTORS:
        if identity(root / path) != original["source_files"][path]:
            raise ValueError("an original native guard changed: " + path)
    return {path: identity(root / path) for path in (PROBE, SOURCE_INPUT, *SELECTORS)}


def snapshot(group):
    memory = {
        row.split(":")[0]: int(row.split()[1]) * 1024
        for row in Path("/proc/meminfo").read_text().splitlines()
        if row.split(":")[0] in {"MemTotal", "MemAvailable", "SwapTotal", "SwapFree"}
    }
    return {
        "memory": memory,
        "memory_psi": Path("/proc/pressure/memory").read_text(),
        "unit_memory_psi": (group / "memory.pressure").read_text(),
        "swap_pages": {
            key: int(value)
            for key, value in (
                r.split() for r in Path("/proc/vmstat").read_text().splitlines()
            )
            if key in {"pswpin", "pswpout"}
        },
        "unit_memory_current": int((group / "memory.current").read_text()),
        "unit_memory_peak": int((group / "memory.peak").read_text()),
        "unit_tasks": int((group / "pids.current").read_text()),
        "memory_events": dict(
            r.split() for r in (group / "memory.events").read_text().splitlines()
        ),
        "units": {"memory": "byte", "swap_pages": "page", "psi_avg10": "percent"},
        "load": os.getloadavg(),
        "capacity_reserved": False,
    }


def healthy(sample, budget):
    reserve = (sample["memory"]["MemTotal"] + 4) // 5
    if sample["memory"]["MemAvailable"] < reserve + budget + MARGIN:
        raise RuntimeError("host reserve plus the complete own budget is unavailable")
    for key in ("memory_psi", "unit_memory_psi"):
        if any(
            float(row.split("avg10=")[1].split()[0]) >= 1
            for row in sample[key].splitlines()
        ):
            raise RuntimeError("memory pressure refuses further qualification work")


def own_scope(args):
    if os.environ.get("RUNNER_ENVIRONMENT") != "github-hosted":
        raise ValueError("this fixed receiving route requires its declared hosted job")
    if sys.version_info[:2] != (3, 14):
        raise ValueError("use the declared Python3.14 interpreter")
    if os.getuid() != args.uid or os.getgid() != args.gid or args.uid == 0:
        raise ValueError("the service must run as the unprivileged job user")
    prefix = (
        "phmt148-bootstrap" if args.phase == "bootstrap" else "phmt148-probe-native"
    )
    expected = f"{prefix}-{os.environ['GITHUB_RUN_ID']}-{os.environ['GITHUB_RUN_ATTEMPT']}.service"
    membership = Path("/proc/self/cgroup").read_text().strip()
    if args.unit != expected or membership != "0::/system.slice/" + expected:
        raise ValueError("current process is outside its own declared service")
    group = Path("/sys/fs/cgroup/system.slice") / expected
    budget, tasks = (2147483648, 64) if args.phase == "bootstrap" else (536870912, 32)
    controls = {
        name: (group / name).read_text().strip()
        for name in (
            "memory.max",
            "memory.swap.max",
            "memory.oom.group",
            "pids.max",
            "cpu.max",
            "cpuset.cpus.effective",
        )
    }
    quota, period = controls["cpu.max"].split()
    if (
        controls["memory.max"] != str(budget)
        or controls["memory.swap.max"] != "0"
        or controls["memory.oom.group"] != "1"
        or controls["pids.max"] != str(tasks)
        or quota != period
        or not quota.isdecimal()
        or int(quota) <= 0
        or controls["cpuset.cpus.effective"] != str(args.cpu)
        or os.sched_getaffinity(0) != {args.cpu}
    ):
        raise ValueError("actual kernel controls differ from the declared phase budget")
    if os.getpriority(os.PRIO_PROCESS, 0) != 19:
        raise ValueError("low CPU priority is required")
    if (
        subprocess.check_output(["ionice", "-p", str(os.getpid())], text=True).strip()
        != "idle"
    ):
        raise ValueError("idle I/O priority is required")
    if any(os.environ.get(name) != "1" for name in THREADS):
        raise ValueError("every declared backend/build thread setting must be one")
    if any(
        resource.getrlimit(k) != (-1, -1)
        for k in (resource.RLIMIT_DATA, resource.RLIMIT_AS)
    ):
        raise ValueError(
            "use the aggregate cgroup budget without a DATA/AS mapping cap"
        )
    before = snapshot(group)
    time.sleep(1)
    after = snapshot(group)
    healthy(after, budget)
    if before["swap_pages"] != after["swap_pages"]:
        raise RuntimeError("active swap refuses phase admission")
    return group, budget, controls


def emit(output, record):
    print(json.dumps(record, allow_nan=False), flush=True)
    with (output / "observations.jsonl").open("a") as handle:
        handle.write(json.dumps(record, allow_nan=False) + "\n")


def run_fixed(args, output, group, budget, label):
    """Monitor one of this case's fixed commands; stop only its own descendants."""
    healthy(snapshot(group), budget)
    emit(output, {"stage": label, "status": "starting", "argv": args})
    process = subprocess.Popen(args, cwd=ROOT, start_new_session=True)
    previous = None
    try:
        while True:
            sample = snapshot(group)
            healthy(sample, budget)
            if (
                previous
                and sum(
                    sample["swap_pages"][k] - previous["swap_pages"][k]
                    for k in ("pswpin", "pswpout")
                )
                > 65536
            ):
                raise RuntimeError("intense swap activity stops this owned command")
            emit(output, {"stage": label, "status": "observed", "resources": sample})
            previous = sample
            try:
                code = process.wait(timeout=5)
                break
            except subprocess.TimeoutExpired:
                pass
    except BaseException:
        if process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
        raise
    emit(output, {"stage": label, "status": "completed", "exit_code": code})
    if code:
        raise subprocess.CalledProcessError(code, args)


def manager_controls(manager):
    """Receive this exact manager's effective serial acquisition settings."""
    if any(
        os.environ.get(name) != "1"
        for name in ("MAMBA_EXTRACT_THREADS", "MAMBA_DOWNLOAD_THREADS")
    ):
        raise ValueError("explicit serial extraction and download are required")
    actual = identity(manager)
    if actual != {"bytes": 14606408, "sha256": MANAGER_SHA}:
        raise ValueError("the manager differs from the reviewed official binary")
    version = subprocess.check_output(
        [str(manager), "--version"], text=True, timeout=10
    ).strip()
    if version != "1.5.10":
        raise ValueError("use the reviewed Micromamba1.5.10 binary")
    controls = json.loads(
        subprocess.check_output(
            [
                str(manager),
                "config",
                "list",
                "extract_threads",
                "download_threads",
                "--json",
            ],
            text=True,
            timeout=10,
        )
    )
    if controls != {"extract_threads": 1, "download_threads": 1} or any(
        type(value) is not int for value in controls.values()
    ):
        raise ValueError("effective manager acquisition concurrency must equal one")
    return {"manager": actual, "version": version, "controls": controls}


def bootstrap(args, group, budget):
    out = args.output
    temporary = Path(os.environ["RUNNER_TEMP"]).resolve()
    expected_name = f"phmt148-native-{os.environ['GITHUB_RUN_ID']}-{os.environ['GITHUB_RUN_ATTEMPT']}"
    if args.name != expected_name or not args.manager.resolve().is_relative_to(
        temporary
    ):
        raise ValueError("use this job's fixed fresh environment and manager")
    emit(
        out,
        {
            "stage": "manager_controls_received",
            **manager_controls(args.manager),
            "scope": "Effective configuration only; transaction behavior remains unqualified",
        },
    )
    run_fixed(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--target",
            str(ROOT / ".molsyssuite-tools"),
            "PyYAML>=6",
            "Jinja2>=3,<4",
            "packaging>=24",
        ],
        out,
        group,
        budget,
        "sdk-tools",
    )
    run_fixed(
        [
            sys.executable,
            str(ROOT / "devtools/conda_environment.py"),
            "create",
            "devtools/conda-envs/test_env_py314.yaml",
            "--python-minor",
            "3.14",
            "--manager",
            str(args.manager),
            "--name",
            args.name,
        ],
        out,
        group,
        budget,
        "sdk-create",
    )
    inventory = json.loads(
        subprocess.check_output([str(args.manager), "env", "list", "--json"], text=True)
    )
    matches = [
        Path(p).resolve() for p in inventory["envs"] if Path(p).name == args.name
    ]
    if len(matches) != 1 or not matches[0].is_relative_to(
        Path(os.environ["MAMBA_ROOT_PREFIX"]).resolve()
    ):
        raise ValueError("manager did not create the unique owned environment")
    prefix = matches[0]
    python = str(prefix / "bin/python")
    os.environ["PATH"] = str(prefix / "bin") + os.pathsep + os.environ["PATH"]
    os.environ["CONDA_PREFIX"] = str(prefix)
    run_fixed(
        [python, "-m", "pip", "install", "--no-deps", "-r", str(ROOT / SOURCE_INPUT)],
        out,
        group,
        budget,
        "pinned-providers",
    )
    run_fixed(
        [python, "-m", "pip", "install", ".", "--no-deps"],
        out,
        group,
        budget,
        "package",
    )
    run_fixed(
        [
            python,
            str(ROOT / "devtools/check_dependency_routes.py"),
            "--context",
            "ci-3.14",
        ],
        out,
        group,
        budget,
        "installed-context",
    )
    run_fixed([python, "-m", "pip", "check"], out, group, budget, "pip-check")
    record = {
        "stage": "bootstrap_received",
        "prefix": str(prefix),
        "python": python,
        "manager": identity(args.manager),
        "manager_version": subprocess.check_output(
            [str(args.manager), "--version"], text=True
        ).strip(),
        "sdk_revision": SDK,
        "scope": "Acquisition only; no native test or benchmark acceptance",
    }
    with (out / "prefix.json").open("x") as handle:
        json.dump(record, handle, indent=2)
        handle.write("\n")
    emit(out, record)
    print("PHMT148_NATIVE_PYTHON=" + python, flush=True)


def native(args, group, budget):
    import yaml

    prefix_record = json.loads((args.output / "prefix.json").read_text())
    if Path(sys.executable).resolve() != Path(prefix_record["python"]).resolve():
        raise ValueError("native checks require the newly created interpreter")
    prefix = Path(prefix_record["prefix"])
    os.environ["PATH"] = str(prefix / "bin") + os.pathsep + os.environ["PATH"]
    os.environ["CONDA_PREFIX"] = str(prefix)
    document = yaml.load((ROOT / PROBE).read_text(), Loader=yaml.BaseLoader)
    shell = document["jobs"]["probe"]["steps"][-1]["run"]
    blocks = re.findall(r"<<'PYTHON'\n(.*?)\nPYTHON", shell, re.S)
    if len(blocks) != 2:
        raise ValueError("the frozen probe structure is unavailable")
    probe = args.output / "scope_probe.py"
    with probe.open("x") as handle:
        handle.write(blocks[1] + "\n")
    original_argv = sys.argv
    try:
        sys.argv = [str(probe), args.unit, str(args.cpu), str(args.uid), str(args.gid)]
        runpy.run_path(str(probe), run_name="__main__")
    finally:
        sys.argv = original_argv
    bindings = {}
    for name in (
        "pharmacophoremt",
        "molsysmt",
        "smonitor",
        "depdigest",
        "argdigest",
        "pyunitwizard",
        "ackredit",
        "molsysviewer",
        "numpy",
        "rdkit",
        "openmm",
        "pytest-receptor",
    ):
        dist = importlib.metadata.distribution(name)
        bindings[name] = {
            "version": dist.version,
            "direct_url": json.loads(dist.read_text("direct_url.json") or "null"),
        }
    dist = importlib.metadata.distribution("molsysmt")
    artifacts = [
        dist.locate_file(p)
        for p in dist.files
        if str(p).startswith("molsysmt/_rust") and str(p).endswith(".so")
    ]
    if len(artifacts) != 1:
        raise ValueError("record the unique installed MolSysMT native artifact")
    artifact_before = identity(artifacts[0])
    emit(
        args.output,
        {
            "stage": "native_bindings",
            "python": sys.version,
            "bindings": bindings,
            "native_artifact": {"path": str(artifacts[0]), **artifact_before},
            "fixed_inputs": fixed_inputs(),
        },
    )
    junit = args.output / "native.junit.xml"
    run_fixed(
        [
            sys.executable,
            "-B",
            "-m",
            "pytest",
            *SELECTORS,
            "--receptor=ci",
            "--junitxml=" + str(junit),
        ],
        args.output,
        group,
        budget,
        "native-guards",
    )
    suites = ET.parse(junit).getroot().findall(".//testsuite")
    counts = {
        key: sum(int(s.attrib.get(key, 0)) for s in suites)
        for key in ("tests", "failures", "errors", "skipped")
    }
    if counts != {"tests": 87, "failures": 0, "errors": 0, "skipped": 0}:
        raise ValueError("the complete original native guard selection did not pass")
    if identity(artifacts[0]) != artifact_before:
        raise ValueError("the installed native artifact changed")
    if identity(Path(__file__))["sha256"] != os.environ.get(
        "PHMT148_NATIVE_CLIENT_SHA256"
    ):
        raise ValueError("the native client differs from the reviewed workflow binding")
    fixed_inputs()
    final = snapshot(group)
    if any(
        int(final["memory_events"].get(key, 0)) for key in ("max", "oom", "oom_kill")
    ):
        raise RuntimeError("native memory-limit events require review before admission")
    emit(
        args.output,
        {
            "stage": "native_qualification_received",
            "counts": counts,
            "resources": final,
            "junit": identity(junit),
            "child_peak_rusage": {
                "value": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss * 1024,
                "unit": "byte",
            },
            "scope": "Fixed public-fixture native receiving only; no private-input pilot or performance claim",
        },
    )
    print(junit.read_text(), flush=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("bootstrap", "native"))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--unit", required=True)
    parser.add_argument("--cpu", required=True, type=int)
    parser.add_argument("--uid", required=True, type=int)
    parser.add_argument("--gid", required=True, type=int)
    parser.add_argument("--manager", type=Path)
    parser.add_argument("--name")
    args = parser.parse_args(argv)
    args.output = args.output.resolve()
    temporary = Path(
        os.environ.get("RUNNER_TEMP", "/nonexistent-phmt148-runner")
    ).resolve()
    if (
        not args.output.is_relative_to(temporary)
        or not args.output.is_dir()
        or args.output.stat().st_uid != args.uid
    ):
        parser.error("use the owned job's existing output directory")
    if args.phase == "bootstrap" and (args.manager is None or not args.name):
        parser.error("bootstrap requires the explicit manager and new environment name")
    if identity(Path(__file__))["sha256"] != os.environ.get(
        "PHMT148_NATIVE_CLIENT_SHA256"
    ):
        raise ValueError("the native client differs from the reviewed workflow binding")
    fixed_inputs()
    group, budget, controls = own_scope(args)
    emit(
        args.output,
        {
            "stage": args.phase + "_admitted",
            "controls": controls,
            "resources": snapshot(group),
            "native_qualification_received": False,
        },
    )
    if args.phase == "bootstrap":
        bootstrap(args, group, budget)
    else:
        native(args, group, budget)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
