"""Opt-in #97 synthetic cached-generation baseline; no molecular operations."""

import argparse
import gc
import hashlib
import importlib
import importlib.metadata
import json
import math
import os
import platform
import statistics
import subprocess
import sys
import traceback
import tracemalloc
from pathlib import Path
from time import perf_counter

PLAN = (
    Path(__file__).resolve().parents[1]
    / "tests/data/cached_generation_scaling/plan.json"
)
PLAN_SHA256 = "c60372071eb89aa20133c2964cfd0eff67ea12591f94d8c4589205c859b9d088"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def load_plan():
    raw = PLAN.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PLAN_SHA256:
        raise ValueError("Frozen scaling plan changed; require a new declaration")
    return json.loads(raw)


def inputs(case, plan):
    """Typed PHMT protocol data, without constructing or inspecting molecules."""
    from pharmacophoremt import pyunitwizard as puw

    features, offset = [], 0
    for kind, count, width in (
        ("hb donor", case["donors"], 2),
        ("aromatic ring", case["rings"], 6),
        ("included volume", case["exclusions"], 1),
    ):
        for _ in range(count):
            features.append(
                dict(
                    kind=kind,
                    atom_indices=list(range(offset, offset + width)),
                    center=puw.quantity([len(features), 0, 0], "nm"),
                    direction=puw.quantity([1, 0, 0], "dimensionless")
                    if kind == "hb donor"
                    else None,
                    normal=puw.quantity([0, 0, 1], "dimensionless")
                    if kind == "aromatic ring"
                    else None,
                )
            )
            offset += width
    common = dict(
        definition="classical_atomic_formal@1",
        selected_atom_indices=list(range(offset)),
        structure_index=4,
        chemical_state="reference",
        recognition={"origin": "synthetic PHMT protocol; no molecular source"},
    )
    positives = [r for r in features if r["kind"] != "included volume"]
    exclusions = [r for r in features if r["kind"] == "included volume"]
    inventory = dict(common, features=positives)
    options = dict(
        receptor_profile=plan["profile"],
        donor_distances=[puw.quantity(x, "nm") for x in plan["donor_distances_nm"]],
        aromatic_distances=[
            puw.quantity(x, "nm") for x in plan["aromatic_distances_nm"]
        ],
        radius=puw.quantity(plan["radius_nm"], "nm"),
        max_hypotheses=case["budget"],
    )
    if exclusions:
        options.update(
            excluded_volume_inventory=dict(common, features=exclusions),
            excluded_volume_radius=puw.quantity(plan["excluded_radius_nm"], "nm"),
        )
    return inventory, options


def normalized(value):
    from pharmacophoremt._private.molsysmt import detached

    return detached(value)


def oracle(result, case, plan, inventory):
    """Independent mixed-radix numeric/coverage oracle, outside measurement."""
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    def equal(actual, expected):
        np.testing.assert_allclose(actual, expected, rtol=0, atol=1e-12)

    bases = [2] * case["donors"] + [4] * case["rings"]
    total = 2 ** case["donors"] * 4 ** case["rings"]
    count = min(total, case["budget"])
    enumeration = result["report"]["enumeration"]
    for field, expected in dict(
        total_possible=total,
        visited=count,
        returned=count,
        remaining=total - count,
        max_hypotheses=case["budget"],
        complete=count == total,
    ).items():
        assert enumeration[field] == expected, (field, enumeration, expected)
    assert result["complete"] is (count == total)
    assert result["method"] == "cached_receptor_donor_aromatic_faces@1"
    assert len(result["models"]) == count
    assert result["report"]["source_inventory"] == normalized(inventory)
    checked = []
    for ordinal, model in enumerate(result["models"]):
        assert model.n_interaction_sites == len(bases) + case["exclusions"]
        choices = model.metadata["generation"]["choices"]
        assert len(choices) == len(bases)
        sites = []
        for index, site in enumerate(model.interaction_sites):
            center = [float(index), 0.0, 0.0]
            radius = plan["radius_nm"]
            if index < len(bases):
                digit = (ordinal // math.prod(bases[index + 1 :])) % bases[index]
                donor = index < case["donors"]
                distance_index = digit if donor else digit // 2
                face = None if donor else [1, -1][digit % 2]
                distance = plan[
                    "donor_distances_nm" if donor else "aromatic_distances_nm"
                ][distance_index]
                center[0 if donor else 2] += distance if donor else face * distance
                assert site.features == ["hb acceptor" if donor else "aromatic ring"]
                assert site.shape_name == ("sphere" if donor else "disk")
                assert site.weight == 1 and site.essential
                choice = choices[index]
                assert choice["feature_index"] == index
                assert choice["distance_index"] == distance_index
                assert choice["face_sign"] == face
                equal(
                    puw.get_value(
                        puw.QuantityRecord.from_dict(choice["distance"]).to_quantity(),
                        to_unit="nm",
                    ),
                    distance,
                )
                assert (
                    site.metadata["atom_indices"]
                    == inventory["features"][index]["atom_indices"]
                )
                if not donor:
                    equal(
                        puw.get_value(site.shape.normal, to_unit="dimensionless"),
                        [0, 0, 1],
                    )
            else:
                assert site.features == ["excluded volume"]
                assert site.shape_name == "sphere" and site.weight == 0
                assert site.essential
                radius = plan["excluded_radius_nm"]
                assert site.metadata["atom_indices"] == [
                    2 * case["donors"] + 6 * case["rings"] + index - len(bases)
                ]
            equal(puw.get_value(site.center, to_unit="nm"), center)
            equal(puw.get_value(site.radius, to_unit="nm"), radius)
            sites.append(dict(center=center, features=site.features, radius=radius))
        checked.append(sites)
    return dict(
        total_possible=total,
        returned=count,
        remaining=total - count,
        complete=count == total,
        sites_per_model=len(bases) + case["exclusions"],
        geometry_order_sha256=digest(checked),
    )


def identity():
    """Inspect loaded bytes/origins; never infer provider Git from ancestor paths."""
    result = {}
    for name in (
        "pharmacophoremt",
        "numpy",
        "pyunitwizard",
        "argdigest",
        "smonitor",
        "depdigest",
        "molsysmt",
    ):
        module = importlib.import_module(name)
        root = Path(module.__file__).resolve().parent
        files = {
            str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*"))
            if p.is_file() and (p.suffix == ".py" or ".so" in p.name)
        }
        distribution = importlib.metadata.distribution(name)
        result[name] = dict(
            file=str(module.__file__),
            distribution_version=distribution.version,
            module_version=getattr(module, "__version__", None),
            direct_url=json.loads(distribution.read_text("direct_url.json") or "null"),
            file_count=len(files),
            file_tree_sha256=digest(files),
            native_files={p: h for p, h in files.items() if ".so" in p},
        )
    return result


def worker(case, plan, mode):
    setup_start = perf_counter()
    import pharmacophoremt as phmt
    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.modeler import from_receptor_features

    before = identity()
    outer_policy = normalized(puw.configure.report())
    inventory, options = inputs(case, plan)
    original = digest(normalized([inventory, options]))
    setup_seconds = perf_counter() - setup_start
    host_load_before = os.getloadavg() if hasattr(os, "getloadavg") else None
    samples, warmups = [], []
    with puw.context(standard_units=plan["standard_units"]), phmt.attribution(False):
        policy = normalized(puw.configure.report())
        for iteration in range(
            plan["warmups"]
            + (plan["repeats"] if mode == "timing" else plan["allocation_repeats"])
        ):
            gc.collect()
            measured = iteration >= plan["warmups"]
            tracing = measured and mode == "allocations"
            if tracing:
                tracemalloc.start()
            collecting = gc.isenabled()
            gc.disable()
            start = perf_counter()
            try:
                result = from_receptor_features(inventory, **options)
                elapsed = perf_counter() - start
            finally:
                if collecting:
                    gc.enable()
            memory = tracemalloc.get_traced_memory() if tracing else None
            if tracing:
                tracemalloc.stop()
            agreement = oracle(result, case, plan, inventory)
            assert digest(normalized([inventory, options])) == original
            assert normalized(puw.configure.report()) == policy
            sample = dict(oracle=agreement)
            if mode == "timing" or not measured:
                sample["elapsed_seconds"] = elapsed
            if tracing:
                sample.update(
                    traced_current_bytes=memory[0], traced_peak_bytes=memory[1]
                )
            (samples if measured else warmups).append(sample)
            del result
    after = identity()
    assert before == after
    assert normalized(puw.configure.report()) == outer_policy
    assert all(r["oracle"] == samples[0]["oracle"] for r in samples + warmups)
    return dict(
        status="completed",
        setup_seconds=setup_seconds,
        host_load_before=host_load_before,
        host_load_after=os.getloadavg() if hasattr(os, "getloadavg") else None,
        case=case,
        mode=mode,
        samples=samples,
        warmups=warmups,
        identity_before=before,
        identity_after=after,
        inputs_sha256=original,
        policy_restored=True,
        cache_unchanged=True,
        attribution="explicitly disabled; no portable bibliographic capture requested",
    )


def run(output):
    plan = load_plan()
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    work = output.parent / (output.stem + "_workers")
    work.mkdir(exist_ok=False)
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.update(
        plan["thread_environment"], PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1"
    )
    records = []
    data = dict(
        schema="pharmacophoremt.cached-generation-scaling@1",
        plan=plan,
        plan_sha256=PLAN_SHA256,
        driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        python=sys.version,
        executable=sys.executable,
        platform=platform.platform(),
        cpu=Path("/proc/cpuinfo").read_text()
        if Path("/proc/cpuinfo").exists()
        else None,
        affinity=sorted(os.sched_getaffinity(0))
        if hasattr(os, "sched_getaffinity")
        else None,
        records=records,
    )
    for case in plan["cases"]:
        for mode in ("timing", "allocations"):
            destination = work / (case["id"] + "_" + mode + ".json")
            command = [
                sys.executable,
                "-I",
                str(Path(__file__).resolve()),
                "--worker",
                case["id"],
                "--mode",
                mode,
                "--output",
                str(destination),
            ]
            record = dict(case_id=case["id"], mode=mode, argv=command)
            worker_start = perf_counter()
            try:
                with destination.with_suffix(".log").open("w") as log:
                    result = subprocess.run(
                        command,
                        env=env,
                        stdout=log,
                        stderr=subprocess.STDOUT,
                        timeout=plan["worker_timeout_seconds"],
                    )
                record["exit_code"] = result.returncode
                record["result"] = (
                    json.loads(destination.read_text())
                    if destination.exists()
                    else None
                )
            except subprocess.TimeoutExpired:
                record.update(exit_code=None, error="worker timeout")
            record["worker_wall_seconds"] = perf_counter() - worker_start
            record["log"] = destination.with_suffix(".log").read_text()
            records.append(record)
            output.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
            print(case["id"], mode, record["exit_code"], flush=True)
    data["completed"] = all(
        r["exit_code"] == 0 and (r.get("result") or {}).get("status") == "completed"
        for r in records
    )
    data["timing_summary"] = {
        r["case_id"]: dict(
            min_seconds=min(values),
            median_seconds=statistics.median(values),
            max_seconds=max(values),
        )
        for r in records
        if r["mode"] == "timing"
        and (result := r.get("result"))
        and result["status"] == "completed"
        if (values := [s["elapsed_seconds"] for s in result["samples"]])
    }
    output.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
    return 0 if data["completed"] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--worker")
    parser.add_argument("--mode", choices=("timing", "allocations"))
    args = parser.parse_args()
    if not args.worker:
        return run(args.output)
    try:
        plan = load_plan()
        case = next(r for r in plan["cases"] if r["id"] == args.worker)
        result = worker(case, plan, args.mode)
    except Exception:
        result = dict(status="failed", error=traceback.format_exc())
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    return 0 if result["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
