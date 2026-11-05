"""Fixed #86 receptor hypotheses; molecular operations remain in MolSysMT.

Run: python -m phmt_test_support.receptor_hypothesis_pilot --output FILE
This unshipped experiment does not introduce a public modeling/search API.
"""

import argparse
import hashlib
import json
import traceback
from copy import deepcopy
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory

import molsysmt as msm

from pharmacophoremt import Pharmacophore, attribution
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.io import load_json, load_yaml, to_yaml
from pharmacophoremt.modeler import from_receptor_projections, get_features
from phmt_test_support.prepared_ccd_ligands import state_payload
from phmt_test_support.prepared_receptor_workflow import credit_input, load_input
from phmt_test_support.prepared_workflow import models_equivalent
from phmt_test_support.saved_model_reader import native_record
from phmt_test_support.validate_eralpha_template import portable

PLAN = (
    Path(__file__).resolve().parents[1]
    / "tests/data/receptor_hypothesis_pilot/plan.json"
)
PROFILE = "fixed_donor_ring_complement@1"


def generate(inventory, plan, budget):
    """Enumerate this fixed cached two-family experiment, without molecular access."""
    if type(budget) is not int or budget < 0:
        raise ValueError("the fixed pilot budget must be a nonnegative integer")
    required = {"hb donor": [], "aromatic ring": []}
    omitted = []
    for index, record in enumerate(inventory["features"]):
        if record["kind"] in required:
            required[record["kind"]].append(index)
        else:
            omitted.append(
                dict(
                    feature_index=index,
                    atom_indices=list(record["atom_indices"]),
                    kind=record["kind"],
                    reason="ideal_acceptor_profile_not_adopted"
                    if record["kind"] == "hb acceptor"
                    else "outside_pilot_profile",
                )
            )
    missing = [kind for kind, indices in required.items() if not indices]
    if missing:
        return dict(
            profile=PROFILE,
            status="not_applicable",
            missing_families=missing,
            budget=budget,
            total_possible=0,
            visited=0,
            returned=0,
            remaining=0,
            complete=True,
            omitted=deepcopy(omitted),
            hypotheses=[],
        )
    if any(len(indices) != 1 for indices in required.values()):
        raise ValueError("the fixed PHE404 pilot requires one donor and one ring")
    donor_index, ring_index = required["hb donor"][0], required["aromatic ring"][0]
    donor, ring = inventory["features"][donor_index], inventory["features"][ring_index]
    if donor.get("direction") is None or ring.get("normal") is None:
        raise ValueError("missing cached donor direction or aromatic axis")
    choices = list(
        product(
            enumerate(plan["donor_distance_nm"]),
            enumerate(plan["ring_distance_nm"]),
            enumerate(plan["face_signs"]),
        )
    )
    hypotheses = []
    for (di, distance), (ri, ring_distance), (fi, sign) in choices[:budget]:
        identity = f"d{di}-r{ri}-f{fi}"
        choice = dict(
            donor_distance_nm=distance,
            ring_distance_nm=ring_distance,
            face_sign=sign,
        )
        evidence = dict(
            profile=PROFILE,
            hypothesis_id=identity,
            choices=choice,
            direction_origin="cached public MolSysMT geometry",
            projection_origin="declared pharmacophoric hypothesis",
        )
        specs = [
            dict(
                feature_index=donor_index,
                projection_direction=donor["direction"],
                distance=puw.quantity(distance, "nm"),
                label=identity + " donor complement",
                evidence=evidence,
            ),
            dict(
                feature_index=ring_index,
                projection_direction=sign * ring["normal"],
                distance=puw.quantity(ring_distance, "nm"),
                target_normal=ring["normal"],
                label=identity + " aromatic face",
                evidence=evidence,
            ),
        ]
        model = from_receptor_projections(
            inventory,
            projection_specs=specs,
            radius=puw.quantity(plan["radius_nm"], "nm"),
            name=identity,
        )
        model.metadata["generation"] = dict(
            profile=PROFILE,
            hypothesis_id=identity,
            choices=choice.copy(),
            budget=budget,
            order=plan["order"],
            omitted=deepcopy(omitted),
            assumptions="essential/weight-one construction; no binding-importance inference",
        )
        hypotheses.append(dict(hypothesis_id=identity, choices=choice, model=model))
    count = len(hypotheses)
    return dict(
        profile=PROFILE,
        status="enumerated",
        missing_families=[],
        budget=budget,
        total_possible=len(choices),
        visited=count,
        returned=count,
        remaining=len(choices) - count,
        complete=count == len(choices),
        omitted=omitted,
        hypotheses=hypotheses,
    )


def run_case(policy, directory):
    """Record the prespecified case, including original native input custody."""
    import ackredit

    raw_plan = PLAN.read_bytes()
    plan = json.loads(raw_plan)
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    configuration = puw.configure.report()
    with (
        puw.context(standard_units=policy),
        attribution(),
        ackredit.capture(
            "receptor hypothesis generation", context={"issue": "pharmacophoremt#86"}
        ) as captured,
    ):
        source, identity = load_input(directory)
        credit_input()
        selection = msm.select(source, selection=plan["selection"])

        def snapshot():
            return dict(
                coordinates_nm=puw.get_value(
                    msm.get(source, coordinates=True), to_unit="nm"
                ).tolist(),
                chemical_state_json=json.dumps(state_payload(source), sort_keys=True),
                analyses={
                    label: portable(
                        msm.convert(
                            source.interactions[label],
                            to_form="molsysmt.InteractionsDict",
                        ).data
                    )
                    for label in ["hydrophobic", "hbonds", "pi_pi"]
                },
            )

        before = snapshot()
        inventory = get_features(
            source,
            selection=selection,
            structure_index=plan["structure_index"],
            chemical_state=plan["chemical_state"],
            features=plan["features"],
        )
        if inventory["recognition"]["hydrogen_bond_route"]["donor_geometry"] != (
            "molsysmt.structure.get_vectors"
        ):
            raise ValueError(
                "this pilot requires the modern public provider vector route"
            )
        holder = Pharmacophore()
        holder.metadata = dict(inventory=inventory)
        inventories_before = native_record(holder, directory, "inventories-before")
        runs = []
        persistence = []
        for budget in plan["budgets"]:
            report = generate(inventory, plan, budget)
            records = []
            for row in report["hypotheses"]:
                stem = f"budget-{budget}-{row['hypothesis_id']}"
                original = native_record(row["model"], directory, stem)
                if budget == plan["total_hypotheses"]:
                    json_model = load_json(directory / (stem + ".json"))
                    json_record = native_record(json_model, directory, stem + "-json")
                    yaml_path = directory / (stem + ".yaml")
                    to_yaml(row["model"], yaml_path)
                    yaml_model = load_yaml(yaml_path)
                    yaml_record = native_record(yaml_model, directory, stem + "-yaml")
                    persistence.append(
                        dict(
                            hypothesis_id=row["hypothesis_id"],
                            json=models_equivalent(json_record, original),
                            yaml=models_equivalent(yaml_record, original),
                            json_exact=json_record == original,
                            yaml_exact=yaml_record == original,
                        )
                    )
                records.append(dict(row, model=original))
            runs.append(dict(report, hypotheses=records))
        try:
            get_features(
                source,
                selection=selection,
                structure_index=plan["invalid_structure_index"],
                chemical_state=plan["chemical_state"],
                features=plan["features"],
            )
        except Exception as error:
            failure = dict(
                status="failed",
                stage="inventory",
                structure_index=plan["invalid_structure_index"],
                exception_type=type(error).__name__,
                message=str(error),
                traceback=traceback.format_exc(),
            )
        else:
            raise AssertionError(
                "the declared invalid structure unexpectedly succeeded"
            )
        after = snapshot()
        inventories_after = native_record(holder, directory, "inventories-after")
    return dict(
        schema="pharmacophoremt.receptor-hypothesis-pilot-result@1",
        plan_sha256=hashlib.sha256(raw_plan).hexdigest(),
        policy=policy,
        input_identity=identity,
        selection=list(selection),
        inputs_before=before,
        inputs_after=after,
        inventories_before=inventories_before,
        inventories_after=inventories_after,
        runs=runs,
        persistence=persistence,
        failed_inventory=failure,
        workflow_attribution=captured.attribution.to_dict(),
        application_policy_restored=puw.configure.report() == configuration,
        holdout_access=False,
        scope="Fixed cached donor/ring hypotheses; no pocket, steric, energetic or biological claim",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(PLAN.read_text())
    with TemporaryDirectory(prefix="phmt-receptor-hypotheses-") as temporary:
        output = [
            run_case(policy, Path(temporary) / str(index))
            for index, policy in enumerate(plan["policies"])
        ]
    args.output.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"policies": len(output), "hypotheses_per_full_run": 8}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
