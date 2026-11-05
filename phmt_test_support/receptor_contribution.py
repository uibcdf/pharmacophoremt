"""Execute the frozen #90 receptor development study through supported tools.

Run: python -m phmt_test_support.receptor_contribution --output FILE
Unshipped case orchestration only. MolSysMT owns every molecular operation;
independent original-coordinate geometry/clash oracles live in the tests.
"""

import argparse
import hashlib
import json
from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory

import molsysmt as msm
import numpy as np

from pharmacophoremt import _ackredit, attribution
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt.io import load_json, load_yaml, to_yaml
from pharmacophoremt.modeler import from_receptor_features, get_features
from pharmacophoremt.screening import PoseEvaluator
from phmt_test_support.prepared_ccd_ligands import state_payload
from phmt_test_support.prepared_receptor_workflow import credit_input, load_input
from phmt_test_support.prepared_workflow import models_equivalent
from phmt_test_support.saved_model_reader import native_record
from phmt_test_support.validate_eralpha_template import portable

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "tests/data/receptor_contribution/plan.json"
PLAN_SHA256 = "4358f73bf84aa334bf1b69822558860bc1f7cc6c0c071c1ad0dcc58978923981"


def load_plan():
    raw = PLAN.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PLAN_SHA256:
        raise ValueError("Frozen scientific plan changed; require a dated amendment")
    plan = json.loads(raw)
    for name, key in [
        ("eligibility.json", "eligibility_ledger_sha256"),
        ("eligibility_rule.json", "eligibility_rule_sha256"),
    ]:
        if hashlib.sha256(PLAN.with_name(name).read_bytes()).hexdigest() != plan[key]:
            raise ValueError("Frozen eligibility input changed")
    return plan


def source_custody(source):
    return dict(
        coordinates_nm=puw.get_value(
            msm.get(source, coordinates=True), to_unit="nm"
        ).tolist(),
        chemical_history=json.dumps(state_payload(source), sort_keys=True),
        analyses={
            label: portable(
                msm.convert(
                    source.interactions[label], to_form="molsysmt.InteractionsDict"
                ).data
            )
            for label in ["hydrophobic", "hbonds", "pi_pi"]
        },
    )


def candidate_custody(candidate):
    return dict(
        coordinates_nm=puw.get_value(
            msm.get(candidate, coordinates=True), to_unit="nm"
        ).tolist(),
        chemical_history=json.dumps(state_payload(candidate), sort_keys=True),
    )


def prepare_region(source, region, plan):
    """Construct this declared O/benzene witness using public MolSysMT only."""
    inventories = {
        name: get_features(source, selection=region["selection"], features=families)
        for name, families in [
            ("donor", ["hb donor"]),
            ("ring", ["aromatic ring"]),
            ("joint", ["hb donor", "hb acceptor", "aromatic ring"]),
            ("heavy", ["included volume"]),
        ]
    }
    donor = inventories["donor"]["features"]
    ring = inventories["ring"]["features"]
    if len(donor) != 1 or len(ring) != 1:
        raise ValueError("Declared single donor/ring eligibility changed")
    donor, ring = donor[0], ring[0]
    if (
        list(donor["atom_indices"]) != region["donor_atoms"]
        or list(ring["atom_indices"]) != region["ring_atoms"]
    ):
        raise ValueError("Declared source correspondence changed")
    if [r["atom_indices"][0] for r in inventories["heavy"]["features"]] != region[
        "heavy_atom_indices"
    ]:
        raise ValueError("Declared heavy-atom coverage changed")
    components = []
    for smiles, atoms in [
        ("O", [region["donor_atoms"][0]]),
        ("c1ccccc1", region["ring_atoms"]),
    ]:
        component = msm.convert(
            msm.convert("smiles:" + smiles, to_form="rdkit.Mol"),
            to_form="molsysmt.MolSys",
        )
        coordinates = msm.get(source, selection=atoms, coordinates=True)
        component.structures.append(coordinates=coordinates)
        components.append(component)
    oxygen = msm.structure.translate(
        components[0],
        translation=puw.quantity(0.35, "nm") * donor["direction"],
        in_place=False,
    )
    benzene = msm.structure.translate(
        components[1],
        translation=puw.quantity(0.35, "nm") * ring["normal"],
        in_place=False,
    )
    displacement = puw.quantity(plan["candidate_definition"]["displacement_nm"], "nm")
    shifted_oxygen = msm.structure.translate(
        oxygen, translation=displacement, in_place=False
    )
    shifted_benzene = msm.structure.translate(
        benzene, translation=displacement, in_place=False
    )
    axis = int(
        np.argmin(np.abs(puw.get_value(ring["normal"], to_unit="dimensionless")))
    )
    center = get_features(benzene, features=["aromatic ring"])["features"][0]["center"]
    rotation = plan["candidate_definition"]["rotation"]["matrices"][axis]
    rotated_benzene = msm.structure.rotate(
        benzene, rotation=rotation, rotation_center=center, in_place=False
    )
    candidates = {
        name: msm.merge(parts, keep_ids=False)
        for name, parts in [
            ("intact", [oxygen, benzene]),
            ("donor_displaced", [shifted_oxygen, benzene]),
            ("ring_displaced", [oxygen, shifted_benzene]),
            ("both_displaced", [shifted_oxygen, shifted_benzene]),
            ("ring_rotated", [oxygen, rotated_benzene]),
        ]
    }
    preflight = {}
    for name, candidate in candidates.items():
        inventory = get_features(
            candidate,
            features=["hb donor", "hb acceptor", "aromatic ring", "included volume"],
        )
        kinds = {
            kind: [
                r["atom_indices"] for r in inventory["features"] if r["kind"] == kind
            ]
            for kind in ["hb donor", "hb acceptor", "aromatic ring", "included volume"]
        }
        if kinds != {
            "hb donor": [],
            "hb acceptor": [[0]],
            "aromatic ring": [list(range(1, 7))],
            "included volume": [[i] for i in range(7)],
        }:
            raise ValueError(
                "Frozen candidate recognition/atom correspondence changed: "
                + repr(kinds)
            )
        preflight[name] = dict(
            inventory=detached(inventory), custody=candidate_custody(candidate)
        )
    return inventories, candidates, dict(rotation_axis_index=axis, candidates=preflight)


def aggregate(generation, outcomes):
    valid = [r["result"] for r in outcomes if r["status"] == "returned"]
    failed = len(outcomes) - len(valid)
    return dict(
        status="unevaluated"
        if not outcomes
        else "partial_failure"
        if failed
        else "evaluated",
        evaluated=len(valid),
        failed=failed,
        best_positive_fit=max((r["fit_value"] for r in valid), default=None),
        any_accepted=any(r["status"] == "matched" for r in valid) if valid else None,
        full_positive=sum(r["fit_value"] == 1 for r in valid),
        full_positive_vetoed=sum(
            r["fit_value"] == 1 and bool(r["excluded_volume_clashes"]) for r in valid
        ),
        enumeration_complete=generation["complete"],
    )


def _record_result(result, model_row):
    # Each evaluator has one fixed model metadata payload. Store it once with
    # its model; all remaining original result fields stay in the outcome row.
    # Together model_index/result reconstruct the exact original result.
    metadata = result.pop("model_metadata")
    if "evaluation_model_metadata" in model_row:
        if metadata != model_row["evaluation_model_metadata"]:
            raise ValueError(
                "One evaluator's model metadata changed between candidates"
            )
    else:
        model_row["evaluation_model_metadata"] = metadata
    return result


def execute_cell(row, inventories, candidates, plan, directory):
    variant = next(v for v in plan["variants"] if v["id"] == row["variant"])
    key = row["variant"] if row["variant"] in ["donor", "ring"] else "joint"
    options = {}
    if variant["exclusion_radius_nm"] is not None:
        options = dict(
            excluded_volume_inventory=inventories["heavy"],
            excluded_volume_radius=puw.quantity(variant["exclusion_radius_nm"], "nm"),
        )
    generated = from_receptor_features(
        inventories[key],
        receptor_profile=plan["profile"],
        donor_distances=[puw.quantity(v, "nm") for v in plan["donor_distances_nm"]],
        aromatic_distances=[
            puw.quantity(v, "nm") for v in plan["aromatic_distances_nm"]
        ],
        radius=puw.quantity(row["query_radius_nm"], "nm"),
        max_hypotheses=row["max_hypotheses"],
        **options,
    )
    models, outcomes = [], {control: [] for control in plan["controls"]}
    for index, model in enumerate(generated["models"]):
        model_row = dict(
            index=index, native=native_record(model, directory, row["id"] + f"-{index}")
        )
        evaluator = PoseEvaluator(
            model,
            min_fit_value=plan["min_fit_value"],
            direction_tolerance=puw.quantity(
                plan["direction_tolerance_degrees"], "degrees"
            ),
        )
        for control in plan["controls"]:
            try:
                result = evaluator.evaluate(candidates[control], pose_id=control)
                result = _record_result(result, model_row)
                outcomes[control].append(
                    dict(model_index=index, status="returned", result=result)
                )
            except Exception as error:
                outcomes[control].append(
                    dict(
                        model_index=index,
                        status="failed",
                        error=dict(
                            type=type(error).__name__,
                            code=getattr(error, "code", None),
                            message=str(error),
                        ),
                    )
                )
        models.append(model_row)
    recovery = []
    if models:
        positives = [
            r["model_index"]
            for r in outcomes["intact"]
            if r["status"] == "returned" and r["result"]["fit_value"] == 1
        ]
        index = positives[0] if positives else 0
        model, original = generated["models"][index], models[index]["native"]
        for suffix, read in [("json", load_json), ("yaml", load_yaml)]:
            try:
                path = directory / (row["id"] + f"-{index}." + suffix)
                if suffix == "yaml":
                    to_yaml(model, str(path))
                restored = read(str(path))
                record = native_record(
                    restored, directory, row["id"] + "-read-" + suffix
                )
                result = PoseEvaluator(
                    restored,
                    min_fit_value=plan["min_fit_value"],
                    direction_tolerance=puw.quantity(
                        plan["direction_tolerance_degrees"], "degrees"
                    ),
                ).evaluate(candidates["intact"], pose_id="intact")
                recovery.append(
                    dict(
                        format=suffix,
                        model_index=index,
                        native_equivalent=models_equivalent(original, record),
                        native=record,
                        result=result,
                    )
                )
            except Exception as error:
                recovery.append(
                    dict(
                        format=suffix,
                        model_index=index,
                        status="failed",
                        error=dict(type=type(error).__name__, message=str(error)),
                    )
                )
    report = dict(generated["report"])
    return dict(
        cell_id=row["id"],
        status="returned",
        generation_report=report,
        complete=generated["complete"],
        models=models,
        outcomes=outcomes,
        aggregates={
            name: aggregate(generated, values) for name, values in outcomes.items()
        },
        recovery=recovery,
    )


def run_study(directory, *, cell_ids=None, tracking=True, preflight_only=False):
    """Run unchanged declared rows; subsets are explicit supplemental controls."""
    plan = load_plan()
    requested = (
        set(cell_ids) if cell_ids is not None else {r["id"] for r in plan["matrix"]}
    )
    if not requested or requested - {r["id"] for r in plan["matrix"]}:
        raise ValueError("Select only nonempty subsets of declared cell IDs")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    policy_before = puw.configure.report()
    output = dict(
        schema="pharmacophoremt.receptor-contribution-run@1",
        plan_sha256=PLAN_SHA256,
        tracking_requested=tracking,
        preflight_only=preflight_only,
        requested_cells=sorted(requested),
        regions=[],
        cells=[],
        failures=[],
    )
    with ExitStack() as stack:
        stack.enter_context(attribution(enabled=tracking))
        capture = None
        output["workflow_attribution"] = dict(
            status="disabled" if not tracking else "unavailable"
        )
        if tracking:
            try:
                provider = _ackredit.backend()
                if provider is not None:
                    capture = stack.enter_context(
                        provider.capture(
                            "frozen receptor contribution",
                            context={"issue": "pharmacophoremt#90"},
                        )
                    )
            except Exception as error:
                output["workflow_attribution"] = dict(
                    status="failed", reason=f"{type(error).__name__}: {error}"
                )
        source, identity = load_input(directory)
        if identity["native_evidence"]["uncompressed_sha256"] != plan["native_sha256"]:
            raise ValueError("Frozen native input identity changed")
        if capture is not None:
            credit_input()
        output["input_identity"] = identity
        output["source_before"] = source_custody(source)
        for policy in plan["policies"]:
            with puw.context(standard_units=policy["standard_units"]):
                for region in plan["regions"]:
                    rows = [
                        r
                        for r in plan["matrix"]
                        if r["id"] in requested
                        and r["group_id"] == region["group_id"]
                        and r["policy_id"] == policy["id"]
                    ]
                    if not rows:
                        continue
                    label = f"PHE{region['group_id']}-{policy['id']}"
                    try:
                        inventories, candidates, preflight = prepare_region(
                            source, region, plan
                        )
                    except Exception as error:
                        output["failures"].append(
                            dict(
                                stage="preflight",
                                region=label,
                                type=type(error).__name__,
                                message=str(error),
                            )
                        )
                        continue
                    inventory_before = detached(inventories)
                    if not preflight_only:
                        for row in rows:
                            try:
                                output["cells"].append(
                                    execute_cell(
                                        row, inventories, candidates, plan, directory
                                    )
                                )
                            except Exception as error:
                                output["cells"].append(
                                    dict(
                                        cell_id=row["id"],
                                        status="failed",
                                        error=dict(
                                            type=type(error).__name__,
                                            message=str(error),
                                        ),
                                    )
                                )
                            print("completed", row["id"], flush=True)
                    after_candidates = {
                        name: candidate_custody(candidate)
                        for name, candidate in candidates.items()
                    }
                    output["regions"].append(
                        dict(
                            group_id=region["group_id"],
                            policy_id=policy["id"],
                            inventories=inventory_before,
                            preflight=preflight,
                            candidate_custody_after=after_candidates,
                            inventories_after=detached(inventories),
                        )
                    )
        output["source_after"] = source_custody(source)
    if capture is not None:
        try:
            output["workflow_attribution"] = dict(
                status="captured", references=capture.attribution.to_dict()
            )
        except Exception as error:
            output["workflow_attribution"] = dict(
                status="failed", reason=f"{type(error).__name__}: {error}"
            )
    output["application_policy_restored"] = puw.configure.report() == policy_before
    returned = [r for r in output["cells"] if r["status"] == "returned"]
    output["actual_counts"] = dict(
        generation_cells=len(output["cells"]),
        returned_models=sum(len(r["models"]) for r in returned),
        primary_evaluations=sum(
            len(v) for r in returned for v in r["outcomes"].values()
        ),
        successful_primary_evaluations=sum(
            v["status"] == "returned"
            for r in returned
            for values in r["outcomes"].values()
            for v in values
        ),
        recovery_evaluations=sum(len(r["recovery"]) for r in returned),
        unevaluated_candidate_slots=sum(not r["models"] for r in returned)
        * len(plan["controls"]),
    )
    output["execution_status"] = (
        "partial_failure"
        if output["failures"]
        or len(returned) != len(output["cells"])
        or output["actual_counts"]["primary_evaluations"]
        != output["actual_counts"]["successful_primary_evaluations"]
        else "completed"
    )
    output["producer_modules"] = {
        name: dict(
            path=str(Path(module.__file__).resolve()),
            version=str(getattr(module, "__version__", "unknown")),
        )
        for name, module in [("molsysmt", msm), ("numpy", np), ("pyunitwizard", puw)]
    }
    if any(
        not item.get("native_equivalent", False)
        for row in returned
        for item in row["recovery"]
    ):
        output["execution_status"] = "partial_failure"
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cell", action="append", dest="cell_ids")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--without-attribution", action="store_true")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(
        prefix="receptor-contribution-", dir=args.output.parent
    ) as work:
        output = run_study(
            work,
            cell_ids=args.cell_ids,
            tracking=not args.without_attribution,
            preflight_only=args.preflight_only,
        )
    args.output.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")
    print(json.dumps(output["actual_counts"]), flush=True)
    return 0 if output["execution_status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
