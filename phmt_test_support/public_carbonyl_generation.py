"""Replay #93's unchanged source/poses through the public cached generator."""

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from pharmacophoremt import _ackredit, attribution
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt.io import load_json, load_yaml, to_yaml
from pharmacophoremt.modeler import from_receptor_features, get_features
from phmt_test_support.carbonyl_acceptor_receiving import (
    PLAN_SHA256,
    _custody,
    _declared_source,
    _directions,
    _evaluator,
    _payload_record,
    load_plan,
    verify_provider,
)
from phmt_test_support.evidence_archive import read_archived_evidence
from phmt_test_support.prepared_workflow import models_equivalent
from phmt_test_support.receptor_contribution import _record_result
from phmt_test_support.saved_model_reader import native_record

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "devguide/evidence/carbonyl_acceptor_receiving_20261105_summary.json"


def generate(inventory, directions, position, plan):
    return from_receptor_features(
        inventory,
        receptor_profile="donor_aromatic_carbonyl_experimental",
        donor_distances=[puw.quantity(0.35, "nm")],
        aromatic_distances=[puw.quantity(0.35, "nm")],
        acceptor_directions=directions,
        acceptor_structure_position=position,
        acceptor_distances=[puw.quantity(0.35, "nm")],
        acceptor_target_orientation="towards_receptor",
        radius=puw.quantity(0.02, "nm"),
        max_hypotheses=2,
    )


@_ackredit.attributed("molsysmt", "numpy", "pyunitwizard")
def _execute(directory):
    plan = load_plan()
    verify_provider()
    summary, original = read_archived_evidence(
        ORIGINAL, identity_key="scientific_results"
    )
    output = dict(
        schema="pharmacophoremt.public-carbonyl-replay@1",
        plan_sha256=PLAN_SHA256,
        original_result_sha256=summary["scientific_results"]["uncompressed_sha256"],
        policies=[],
        cells=[],
        failures=[],
    )
    source = _declared_source(plan["source"])
    output["source_before"] = _custody(source)
    for policy in plan["policies"]:
        with puw.context(standard_units=list(policy["standard_units"].values())):
            raw = _directions(source, plan["source"], plan)
            context = dict(
                policy_id=policy["id"],
                provider=_payload_record(raw),
                negative_queries=[],
            )
            output["policies"].append(context)
            for row in [r for r in plan["matrix"] if r["policy_id"] == policy["id"]]:
                cell = dict(
                    cell_id=row["id"],
                    status="started",
                    models=[],
                    outcomes={},
                    recovery=[],
                )
                output["cells"].append(cell)
                try:
                    inventory = get_features(
                        source,
                        selection=[2],
                        structure_index=row["source_structure_index"],
                        features=["hb acceptor"],
                    )
                    cell["inventory_before"] = detached(inventory)
                    result = generate(inventory, raw, row["structure_position"], plan)
                    models = result["models"]
                    cell["generation_report"] = result["report"]
                    cell["complete"] = result["complete"]
                    old = next(
                        c for c in original["cells"] if c["cell_id"] == row["id"]
                    )
                    candidates = {}
                    cell["candidates_before"] = {}
                    for control in plan["controls"]:
                        name = control["id"]
                        # Original measured pose is a fixed replay input. MolSysMT
                        # reconstructs the same declared indexed-D/O source.
                        candidates[name] = _declared_source(
                            dict(
                                smiles=plan["candidate"]["smiles"],
                                coordinates=dict(
                                    unit="nm",
                                    values=old["candidates_before"][name][
                                        "coordinates_nm"
                                    ],
                                ),
                            )
                        )
                        cell["candidates_before"][name] = _custody(candidates[name])
                    for index, model in enumerate(models):
                        model_row = dict(
                            index=index,
                            native=native_record(
                                model, directory, row["id"] + f"-{index}"
                            ),
                        )
                        cell["models"].append(model_row)
                        evaluator = _evaluator(model, plan)
                        for name, candidate in candidates.items():
                            try:
                                value = _record_result(
                                    evaluator.evaluate(candidate, pose_id=name),
                                    model_row,
                                )
                                outcome = dict(
                                    status="returned", model_index=index, result=value
                                )
                            except Exception as error:
                                outcome = dict(
                                    status="failed",
                                    model_index=index,
                                    error=dict(
                                        type=type(error).__name__, message=str(error)
                                    ),
                                )
                            cell["outcomes"].setdefault(name, []).append(outcome)
                        name = f"lobe{index}_aligned"
                        for suffix, read in [("json", load_json), ("yaml", load_yaml)]:
                            path = directory / (row["id"] + f"-{index}." + suffix)
                            if suffix == "yaml":
                                to_yaml(model, path)
                            restored = read(path)
                            native = native_record(
                                restored,
                                directory,
                                row["id"] + f"-{index}-read-" + suffix,
                            )
                            cell["recovery"].append(
                                dict(
                                    format=suffix,
                                    model_index=index,
                                    candidate=name,
                                    native_equivalent=models_equivalent(
                                        model_row["native"], native
                                    ),
                                    native=native,
                                    result=_evaluator(restored, plan).evaluate(
                                        candidates[name], pose_id=name
                                    ),
                                )
                            )
                    cell["inventory_after"] = detached(inventory)
                    cell["candidates_after"] = {
                        name: _custody(c) for name, c in candidates.items()
                    }
                    cell["status"] = "returned"
                except Exception as error:
                    cell.update(
                        status="failed",
                        error=dict(type=type(error).__name__, message=str(error)),
                    )
                print("completed", row["id"], flush=True)
            context["provider_after"] = _payload_record(raw)
            for spec in plan["negative_sources"]:
                record = dict(id=spec["id"])
                context["negative_queries"].append(record)
                try:
                    negative = _declared_source(spec)
                    record["source_before"] = _custody(negative)
                    cache = _directions(negative, spec, plan)
                    record["provider"] = _payload_record(cache)
                    inventory = get_features(
                        negative, selection=spec["selection"], features=["hb acceptor"]
                    )
                    generated = generate(inventory, cache, 0, plan)
                    record.update(
                        returned_models=len(generated["models"]),
                        report=generated["report"],
                        score=None,
                        source_after=_custody(negative),
                    )
                except Exception as error:
                    record["failure"] = dict(
                        type=type(error).__name__, message=str(error)
                    )
    output["source_after"] = _custody(source)
    output["actual_counts"] = dict(
        source_position_policy_blocks=len(output["cells"]),
        returned_models=sum(len(c["models"]) for c in output["cells"]),
        primary_evaluations=sum(
            len(v) for c in output["cells"] for v in c["outcomes"].values()
        ),
        recovery_evaluations=sum(len(c["recovery"]) for c in output["cells"]),
        negative_queries=sum(len(p["negative_queries"]) for p in output["policies"]),
        negative_pose_evaluations=0,
    )
    failed = any(
        c["status"] != "returned"
        or any(
            v["status"] != "returned"
            for values in c["outcomes"].values()
            for v in values
        )
        or any(not r["native_equivalent"] for r in c["recovery"])
        for c in output["cells"]
    )
    failed = failed or any(
        n.get("failure") for p in output["policies"] for n in p["negative_queries"]
    )
    output["execution_status"] = "partial_failure" if failed else "completed"
    return output


def run_study(directory):
    policy = puw.configure.report()
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with attribution():
        result = _execute(directory)
    result["application_policy_restored"] = puw.configure.report() == policy
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="public-carbonyl-", dir=args.output.parent) as work:
        result = run_study(work)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result["actual_counts"]), flush=True)
    return 0 if result["execution_status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
