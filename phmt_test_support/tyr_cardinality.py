"""Frozen #91 dual-donor TYR controls; molecular operations use MolSysMT.

Run from the source checkout: python -m phmt_test_support.tyr_cardinality --output FILE
This is unshipped case orchestration, not a new public molecular/modeling API.
"""

import argparse
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import molsysmt as msm
import numpy as np

from pharmacophoremt import _ackredit, attribution
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt.modeler import get_features
from phmt_test_support.prepared_receptor_workflow import credit_input, load_input
from phmt_test_support.receptor_contribution import (
    candidate_custody,
    execute_cell,
    source_custody,
)

PLAN = Path(__file__).resolve().parents[1] / "tests/data/tyr_cardinality/plan.json"
PLAN_SHA256 = "29b62982967e19855c0429716815a2c39f645cea7fd2042be0f86567925aac81"


def load_plan():
    raw = PLAN.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PLAN_SHA256:
        raise ValueError("Frozen TYR plan changed; require a dated amendment")
    plan = json.loads(raw)
    for name, key in [
        ("eligibility.json", "eligibility_sha256"),
        ("eligibility_rule.json", "eligibility_rule_sha256"),
    ]:
        if hashlib.sha256(PLAN.with_name(name).read_bytes()).hexdigest() != plan[key]:
            raise ValueError("Frozen TYR eligibility changed")
    return plan


def prepare_region(source, region, plan):
    inventories = {
        variant["id"]: get_features(
            source, selection=region["selection"], features=variant["families"]
        )
        for variant in plan["variants"]
    }
    donors = inventories["donor"]["features"]
    rings = inventories["ring"]["features"]
    if (
        len(donors) != 2
        or len(rings) != 1
        or list(rings[0]["atom_indices"]) != region["ring_atoms"]
    ):
        raise ValueError("Frozen two-donor/one-ring eligibility changed")
    by_element = {}
    for element, atoms in region["donor_pairs_by_element"].items():
        matches = [r for r in donors if list(r["atom_indices"]) == atoms]
        if len(matches) != 1:
            raise ValueError("Frozen N/O donor correspondence changed")
        by_element[element] = matches[0]
    components = {}
    for element in ["N", "O"]:
        component = msm.convert(
            msm.convert("smiles:O", to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
        )
        component.structures.append(
            coordinates=msm.get(
                source,
                selection=[region["donor_pairs_by_element"][element][0]],
                coordinates=True,
            )
        )
        components[element] = msm.structure.translate(
            component,
            translation=puw.quantity(0.35, "nm") * by_element[element]["direction"],
            in_place=False,
        )
    ring = msm.convert(
        msm.convert("smiles:c1ccccc1", to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
    )
    ring.structures.append(
        coordinates=msm.get(source, selection=region["ring_atoms"], coordinates=True)
    )
    ring = msm.structure.translate(
        ring, translation=puw.quantity(0.35, "nm") * rings[0]["normal"], in_place=False
    )
    axis = int(
        np.argmin(np.abs(puw.get_value(rings[0]["normal"], to_unit="dimensionless")))
    )
    center = get_features(ring, features=["aromatic ring"])["features"][0]["center"]
    rotated = msm.structure.rotate(
        ring,
        rotation=plan["rotation_matrices"][axis],
        rotation_center=center,
        in_place=False,
    )
    parts = {
        "intact": [components["N"], components["O"], ring],
        "nitrogen_target_only": [components["N"], ring],
        "oxygen_target_only": [components["O"], ring],
        "ring_only": [ring],
        "ring_rotated": [components["N"], components["O"], rotated],
    }
    candidates = {
        name: msm.merge(values, keep_ids=False) for name, values in parts.items()
    }
    records = {}
    for name, candidate in candidates.items():
        n = len(parts[name]) - 1
        types = list(map(str, msm.get(candidate, element="atom", atom_type=True)))
        inventory = get_features(
            candidate, features=["hb donor", "hb acceptor", "aromatic ring"]
        )
        kinds = {
            kind: [
                f["atom_indices"] for f in inventory["features"] if f["kind"] == kind
            ]
            for kind in ["hb donor", "hb acceptor", "aromatic ring"]
        }
        if types != ["O"] * n + ["C"] * 6 or kinds != {
            "hb donor": [],
            "hb acceptor": [[i] for i in range(n)],
            "aromatic ring": [list(range(n, n + 6))],
        }:
            raise ValueError(
                "Frozen candidate recognition/order changed: " + repr(kinds)
            )
        records[name] = dict(
            inventory=detached(inventory),
            atom_types=types,
            custody=candidate_custody(candidate),
        )
    return inventories, candidates, dict(rotation_axis_index=axis, candidates=records)


@_ackredit.attributed("molsysmt", "numpy", "pyunitwizard")
def _execute(directory, plan, requested):
    """One bounded host attribution boundary for the actual composed workflow."""
    output = dict(
        schema="pharmacophoremt.tyr-cardinality-run@1",
        plan_sha256=PLAN_SHA256,
        requested_cells=sorted(requested),
        regions=[],
        cells=[],
        failures=[],
    )
    source, identity = load_input(directory)
    if identity["native_evidence"]["uncompressed_sha256"] != plan["native_sha256"]:
        raise ValueError("Frozen native source changed")
    # Reuse the component's established attribution calculation. Credit the data
    # only when that capture exists; an absent/failed provider cannot erase science.
    calculation = _ackredit._CURRENT.get()
    output["input_credit_status"] = "not_captured"
    if calculation is not None and calculation.status == "captured":
        try:
            credit_input()
            output["input_credit_status"] = "captured"
        except Exception as error:
            output["input_credit_status"] = f"failed: {type(error).__name__}: {error}"
    output["input_identity"] = identity
    output["source_before"] = source_custody(source)
    for policy in plan["policies"]:
        with puw.context(standard_units=policy["standard_units"]):
            for region in plan["regions"]:
                rows = [
                    r
                    for r in plan["matrix"]
                    if r["id"] in requested
                    and r["policy_id"] == policy["id"]
                    and r["group_id"] == region["group_id"]
                ]
                if not rows:
                    continue
                try:
                    inventories, candidates, preflight = prepare_region(
                        source, region, plan
                    )
                except Exception as error:
                    output["failures"].append(
                        dict(
                            stage="preflight",
                            group_id=region["group_id"],
                            policy_id=policy["id"],
                            type=type(error).__name__,
                            message=str(error),
                        )
                    )
                    continue
                before = detached(inventories)
                for row in rows:
                    try:
                        output["cells"].append(
                            execute_cell(row, inventories, candidates, plan, directory)
                        )
                    except Exception as error:
                        output["cells"].append(
                            dict(
                                cell_id=row["id"],
                                status="failed",
                                error=dict(
                                    type=type(error).__name__, message=str(error)
                                ),
                            )
                        )
                    print("completed", row["id"], flush=True)
                output["regions"].append(
                    dict(
                        group_id=region["group_id"],
                        policy_id=policy["id"],
                        inventories=before,
                        inventories_after=detached(inventories),
                        preflight=preflight,
                        candidate_custody_after={
                            name: candidate_custody(candidate)
                            for name, candidate in candidates.items()
                        },
                    )
                )
    output["source_after"] = source_custody(source)
    returned = [r for r in output["cells"] if r["status"] == "returned"]
    output["actual_counts"] = dict(
        generation_cells=len(output["cells"]),
        returned_models=sum(len(c["models"]) for c in returned),
        primary_evaluations=sum(
            len(v) for c in returned for v in c["outcomes"].values()
        ),
        recovery_evaluations=sum(len(c["recovery"]) for c in returned),
    )
    failed_results = any(
        v["status"] != "returned"
        for c in returned
        for values in c["outcomes"].values()
        for v in values
    )
    failed_recovery = any(
        not v.get("native_equivalent", False) for c in returned for v in c["recovery"]
    )
    output["execution_status"] = (
        "partial_failure"
        if output["failures"]
        or len(returned) != len(output["cells"])
        or failed_results
        or failed_recovery
        else "completed"
    )
    return output


def run_study(directory, *, cell_ids=None, tracking=True):
    plan = load_plan()
    requested = (
        set(cell_ids) if cell_ids is not None else {r["id"] for r in plan["matrix"]}
    )
    if not requested or requested - {r["id"] for r in plan["matrix"]}:
        raise ValueError("Choose a nonempty subset of frozen TYR cell IDs")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    policy = puw.configure.report()
    with attribution(enabled=tracking):
        result = _execute(directory, plan, requested)
    result["application_policy_restored"] = puw.configure.report() == policy
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cell", action="append", dest="cell_ids")
    parser.add_argument("--without-attribution", action="store_true")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(
        prefix="tyr-cardinality-", dir=args.output.parent
    ) as directory:
        result = run_study(
            directory, cell_ids=args.cell_ids, tracking=not args.without_attribution
        )
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result["actual_counts"]), flush=True)
    return 0 if result["execution_status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
