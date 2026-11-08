"""Declare/check one fixed feature-reuse workload without molecular imports.

This developer control neither executes a benchmark nor admits an execution
route. Native measurement and resource isolation remain separate pending work.
"""

import argparse
import datetime
import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "devguide/evidence/feature_reuse_plan_20261107.json"
ORIGINAL_SHA256 = "eeea9d49ae9c00d096d64b1ed2e00a8bb8ae6e463cb0afb3723dac4ff724e98f"
WORKLOADS = (
    ("one-caffeine", ("caffeine-acceptors",)),
    ("one-aspirin", ("aspirin-acceptors",)),
    ("two-mixed", ("caffeine-acceptors", "aspirin-acceptors")),
    ("eight-repeated", ("caffeine-acceptors", "aspirin-acceptors") * 4),
)
REPEATS = 4


def original_plan():
    raw = ORIGINAL.read_bytes()
    if hashlib.sha256(raw).hexdigest() != ORIGINAL_SHA256:
        raise ValueError("original prospective equality plan changed")
    return json.loads(raw)


def workload_pairs():
    """Return all 48 declared pairs, with balanced serial process order."""
    pairs = []
    for repeat in range(REPEATS):
        for cid in (1983, 2244, 2519):
            for key, references in WORKLOADS:
                pairs.append(
                    {
                        "pair_key": f"cid-{cid}:{key}:repeat-{repeat}",
                        "cid": cid,
                        "workload": key,
                        "repeat": repeat,
                        "arm_order": ["fresh", "reused"]
                        if repeat % 2 == 0
                        else ["reused", "fresh"],
                        "queries": [
                            {"key": f"{key}:{index}", "reference": reference}
                            for index, reference in enumerate(references)
                        ],
                    }
                )
    return pairs


def build_plan(*, parent_source, recorded_at_utc):
    if type(parent_source) is not str or not re.fullmatch(
        "[0-9a-f]{40}", parent_source
    ):
        raise ValueError("parent_source requires one full lower-case Git SHA")
    if type(recorded_at_utc) is not str:
        raise ValueError("recorded_at_utc requires an explicit UTC timestamp")
    recorded = datetime.datetime.fromisoformat(recorded_at_utc)
    if recorded.utcoffset() != datetime.timedelta(0):
        raise ValueError("recorded_at_utc requires an explicit UTC timestamp")
    original = original_plan()
    return {
        "schema": "pharmacophoremt.feature-reuse-profile-plan@1",
        "issue": "https://github.com/uibcdf/pharmacophoremt/issues/148",
        "owners": ["LMMV", "dprada"],
        "parent_source": parent_source,
        "recorded_at_utc": recorded_at_utc,
        "state": "declared_not_executed",
        "original_equality_plan": {
            "file": str(ORIGINAL.relative_to(ROOT)),
            "sha256": ORIGINAL_SHA256,
        },
        **{
            key: deepcopy(original[key])
            for key in (
                "source_records",
                "references",
                "requested_families",
                "source_options",
                "settings",
                "publication",
            )
        },
        "pairs": workload_pairs(),
        "denominators": {
            "sources": 3,
            "distinct_reference_geometries": 2,
            "workloads_per_source": 4,
            "repeats": REPEATS,
            "timed_pairs": 48,
            "timed_arm_processes": 96,
            "timed_query_requests_per_arm": 144,
            "outer_source_extractions": {"fresh": 144, "reused": 48},
            "outer_extraction_scope": "excludes reference and native post-fit/evaluator recognition",
        },
        "admission_pilot": {
            "cid": 2244,
            "workload": "two-mixed",
            "arm_order": ["fresh", "reused"],
            "arm_processes": 2,
            "included_in_timed_samples": False,
            "purpose": "Verify native equality, positive fitting, resource envelope and monitoring before admitting 96 timed processes.",
        },
        "measurement_contract": {
            "processes": "Fresh process per arm; serial, no concurrent own checks/builds/timing.",
            "preparation": "Imports, H5MSM loading and reference inventory construction precede algorithm timing; retain their separate costs and whole-command time.",
            "warmup": "No extra molecular warmup inside an arm. Separate admission pilot; OS cache is uncontrolled, never called cold.",
            "fresh": "Extract source features once inside every query's timed interval.",
            "reused": "Time source inventory construction once; charge it to the workload total, then reuse the same inventory.",
            "query": "Identical public correspondence, first canonical mapping placement, native post-fit extraction/checking, query construction, PoseEvaluator, checked_pose_coverage and quantity-preserving detachment.",
            "timers": "Wall perf_counter_ns and process_time_ns; each extraction, each complete query, and end-to-end build-plus-queries. First and remaining requests reported separately.",
            "outside_timing": "Cross-arm full evidence comparison, source/reference/inventory immutability checks and output hashing/writing. Native post-fit checks remain inside timing.",
            "memory": "Managed aggregate memory peak and whole-process peak RSS reported separately; neither is incremental inventory allocation. Detached inventory JSON bytes are a logical payload size only.",
            "scientific_gate": "Full detached native evidence equal per corresponding request; preserve source hashes, mapping omissions, no-placement and checked-pose outcomes. No full RigidPoseSearch equivalence.",
            "statistics": "Retain all four paired samples and process order; descriptive median/min/max per source/workload/arm. Ratios only for complete scientifically equal pairs; report incomplete/failed denominators and no-benefit outcomes. No population inference from repeated geometries.",
            "attribution": "Same explicit disabled capture for timed arms; separate untimed actual attribution receiving with an application-owned session before interpretation.",
        },
        "execution_admission": {
            "status": "pending_safe_route_and_native_driver",
            "native_driver": "not_implemented_or_qualified",
            "scheduler_or_owned_cgroup_required": True,
            "memory_bytes": 536870912,
            "swap_bytes": 0,
            "max_tasks": 32,
            "logical_cpus": 1,
            "backend_threads": 1,
            "nice": 19,
            "io": "idle",
            "arm_wall_seconds": 180,
            "entry_and_monitoring": "Recheck scheduler/allocation, CPU/load, RAM, PSI and swap activity. Preserve at least20percent physical RAM plus aggregate own task budget. Stop own group and retain partial outputs on significant pressure; capacity is not a reservation.",
            "resource_owner": "https://github.com/uibcdf/uibcdf-infrastructure/issues/1",
            "architecture_owner": "https://github.com/uibcdf/moli/issues/96",
            "preserved_failure": "The prior DATA512MiB/OpenMM mapping case remains failed; no repeat of that exhausted route, budget escalation, borrowed user bus or global machine change.",
        },
        "claims": {
            "native_measurement_executed": False,
            "performance_improvement": False,
            "persistent_cache_or_index_qualified": False,
            "large_library_capacity_qualified": False,
            "biological_validation": False,
            "supported_installed_or_release_qualification": False,
        },
    }


def validate_plan(plan):
    """Refuse altered budgets, omitted arms, settings drift or invented results."""
    if not isinstance(plan, dict):
        raise ValueError("plan must be an object")
    expected = build_plan(
        parent_source=plan.get("parent_source"),
        recorded_at_utc=plan.get("recorded_at_utc"),
    )
    # Strict JSON also distinguishes bool/int and refuses nonfinite additions.
    if json.dumps(plan, sort_keys=True, allow_nan=False) != json.dumps(
        expected, sort_keys=True, allow_nan=False
    ):
        raise ValueError("plan differs from the fixed prospective declaration")


def verify_snapshot(path, expected):
    digest, size = hashlib.sha256(), 0
    with Path(path).open("rb") as source:
        while block := source.read(65536):
            digest.update(block)
            size += len(block)
    actual = {"bytes": size, "sha256": digest.hexdigest()}
    if actual != expected:
        raise ValueError(f"snapshot bytes differ: {path}")
    return actual


def verify_inputs(plan, *, snapshot_root=None):
    """Hash only the three frozen files, without decoding molecular content."""
    validate_plan(plan)
    verified = []
    for record in plan["source_records"]:
        path = Path(record["snapshot_path"])
        if snapshot_root is not None:
            path = Path(snapshot_root) / f"cid-{record['cid']}" / path.name
        verified.append(
            {
                "cid": record["cid"],
                "path": str(path),
                **verify_snapshot(path, record["snapshot"]),
            }
        )
    return verified


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", type=Path, metavar="NEW_PLAN")
    mode.add_argument("--check", type=Path, metavar="PLAN")
    parser.add_argument("--parent-source")
    parser.add_argument("--verify-inputs", action="store_true")
    parser.add_argument("--snapshot-root", type=Path)
    args = parser.parse_args(argv)
    if args.write is not None:
        if args.verify_inputs or args.snapshot_root is not None:
            parser.error("input verification requires --check")
        plan = build_plan(
            parent_source=args.parent_source,
            recorded_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )
        with args.write.open("x", encoding="utf-8") as output:
            output.write(json.dumps(plan, indent=2, allow_nan=False) + "\n")
        print("Prospective declaration written; no native calculation executed.")
    else:
        if args.parent_source is not None:
            parser.error("--parent-source requires --write")
        if args.snapshot_root is not None and not args.verify_inputs:
            parser.error("--snapshot-root requires --verify-inputs")
        plan = json.loads(args.check.read_text(encoding="utf-8"))
        validate_plan(plan)
        result = {"valid_declaration": True, "native_measurement_executed": False}
        if args.verify_inputs:
            result["verified_inputs"] = verify_inputs(
                plan, snapshot_root=args.snapshot_root
            )
        print(json.dumps(result, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
