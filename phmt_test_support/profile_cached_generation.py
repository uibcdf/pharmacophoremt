"""Opt-in #98 fixed-work profile; reuse #97 inputs/oracle without molecular work."""

import argparse
import cProfile
import gc
import hashlib
import importlib.util
import json
import pstats
import traceback
from pathlib import Path
from time import perf_counter

HELPER = Path(__file__).with_name("benchmark_cached_generation.py")
HELPER_SHA256 = "165b6ddc6feca62b0004d0f2aad66bd8f334af008a19e077fb7b6289e3333d84"


def memory_admission():
    memory = {
        line.split(":")[0]: int(line.split()[1])
        for line in Path("/proc/meminfo").read_text().splitlines()
        if line.startswith(("MemAvailable:", "SwapTotal:", "SwapFree:"))
    }
    pressure = Path("/proc/pressure/memory").read_text()
    full = next(line for line in pressure.splitlines() if line.startswith("full "))
    avg10 = float(full.split()[1].split("=")[1])
    return dict(
        memory_kib=memory,
        memory_pressure=pressure,
        admitted=memory["MemAvailable"] >= 4194304 and avg10 == 0,
    )


def run(output):
    data = dict(
        schema="pharmacophoremt.cached-generation-profile@1",
        driver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        admission=memory_admission(),
        calls=[],
    )
    output.write_text(json.dumps(data, indent=2) + "\n")
    if not data["admission"]["admitted"]:
        return dict(data, status="deferred_resource_pressure")
    if hashlib.sha256(HELPER.read_bytes()).hexdigest() != HELPER_SHA256:
        raise ValueError("Original #97 helper bytes changed")
    spec = importlib.util.spec_from_file_location("phmt98_original_helper", HELPER)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    import pharmacophoremt as phmt
    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.io import to_json
    from pharmacophoremt.modeler import from_receptor_features

    plan = helper.load_plan()
    case = next(c for c in plan["cases"] if c["id"] == "budget_32")
    data.update(case=case, plan_sha256=helper.PLAN_SHA256, helper_sha256=HELPER_SHA256)
    data["identity_before"] = helper.identity()
    original_policy = helper.normalized(puw.configure.report())
    source, options = helper.inputs(case, plan)
    inputs_hash = helper.digest(helper.normalized([source, options]))
    native = output.parent / (output.stem + "_native")
    native.mkdir(exist_ok=False)
    data["inputs_sha256"] = inputs_hash
    with puw.context(standard_units=plan["standard_units"]), phmt.attribution(False):
        policy = helper.normalized(puw.configure.report())
        for mode in ["warmup", "profile", "control_1", "control_2"]:
            admission = memory_admission()
            data["current_mode"] = mode
            output.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
            if not admission["admitted"]:
                return dict(
                    data,
                    status="deferred_resource_pressure",
                    interrupted_before=mode,
                    last_admission=admission,
                )
            gc.collect()
            profile = cProfile.Profile() if mode == "profile" else None
            collecting = gc.isenabled()
            gc.disable()
            start = perf_counter()
            try:
                if profile is None:
                    result = from_receptor_features(source, **options)
                else:
                    result = profile.runcall(from_receptor_features, source, **options)
                elapsed = perf_counter() - start
            finally:
                if collecting:
                    gc.enable()
                if profile is not None:
                    profile.dump_stats(str(output.with_suffix(".prof")))
            agreement = helper.oracle(result, case, plan, source)
            payload = dict(
                report=helper.normalized(
                    {k: v for k, v in result.items() if k != "models"}
                ),
                models=[],
            )
            for index, model in enumerate(result["models"]):
                path = native / f"{mode}_{index}.json"
                to_json(model, path)
                payload["models"].append(json.loads(path.read_text()))
            data["calls"].append(
                dict(
                    mode=mode,
                    elapsed_seconds=elapsed,
                    oracle=agreement,
                    full_payload_sha256=helper.digest(payload),
                    payload=payload,
                    admission=admission,
                )
            )
            assert inputs_hash == helper.digest(helper.normalized([source, options]))
            assert helper.normalized(puw.configure.report()) == policy
            if profile is not None:
                stats = pstats.Stats(profile)
                data["profile"] = dict(
                    total_calls=stats.total_calls,
                    primitive_calls=stats.prim_calls,
                    total_exclusive_seconds=stats.total_tt,
                    functions=[
                        dict(
                            function=list(key),
                            primitive_calls=cc,
                            total_calls=nc,
                            exclusive_seconds=tt,
                            cumulative_seconds=ct,
                            callers=[
                                dict(function=list(caller), stats=list(values))
                                for caller, values in callers.items()
                            ],
                        )
                        for key, (cc, nc, tt, ct, callers) in stats.stats.items()
                    ],
                )
            output.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
            del result
    data["identity_after"] = helper.identity()
    assert data["identity_before"] == data["identity_after"]
    assert helper.normalized(puw.configure.report()) == original_policy
    assert len({r["full_payload_sha256"] for r in data["calls"]}) == 1
    assert all(r["oracle"] == data["calls"][0]["oracle"] for r in data["calls"])
    return dict(
        data,
        status="completed",
        inputs_sha256=inputs_hash,
        caches_unchanged=True,
        unit_policy_restored=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        result = run(output)
    except Exception:
        result = json.loads(output.read_text()) if output.exists() else {}
        result.update(status="failed", error=traceback.format_exc())
    output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(result["status"], flush=True)
    return 0 if result["status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
