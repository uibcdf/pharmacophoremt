"""Fixed #85 prepared-receptor experiment; all molecular operations use MolSysMT.

Run: python -m phmt_test_support.prepared_receptor_sensitivity --output FILE
This is unshipped case orchestration, not a preparation or parameter-search API.
"""

import argparse
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory

import molsysmt as msm
import numpy as np

from pharmacophoremt import Pharmacophore, attribution
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import (
    StructureBasedModeler,
    extract_pharmacophore,
    from_receptor_projections,
    get_features,
)
from pharmacophoremt.screening import PoseEvaluator
from phmt_test_support.prepared_ccd_ligands import state_payload
from phmt_test_support.prepared_receptor_workflow import credit_input, load_input
from phmt_test_support.saved_model_reader import native_record
from phmt_test_support.validate_eralpha_template import portable

PLAN = (
    Path(__file__).resolve().parents[1]
    / "tests/data/prepared_receptor_sensitivity/plan.json"
)


def run_case(policy, directory):
    """Execute the fixed declared settings, preserving source and native outputs."""
    import ackredit

    raw_plan = PLAN.read_bytes()
    plan = json.loads(raw_plan)
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    configuration = puw.configure.report()
    rows = []
    with (
        puw.context(standard_units=policy),
        attribution(),
        ackredit.capture(
            "prepared receptor sensitivity", context={"issue": "pharmacophoremt#85"}
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
            source, selection=selection, features=["aromatic ring"]
        )
        heavy = get_features(source, selection=selection, features=["included volume"])
        holder = Pharmacophore()
        holder.metadata = dict(aromatic=inventory, heavy=heavy)
        inventories_before = native_record(holder, directory, "inventories-before")
        moved = msm.structure.translate(
            source,
            translation=puw.quantity(plan["translation_nm"], "nm"),
            in_place=False,
        )
        rotated = msm.structure.rotate(
            source,
            rotation=np.asarray(plan["rotation"]),
            rotation_center=inventory["features"][0]["center"],
            in_place=False,
        )
        turned = msm.structure.translate(
            rotated,
            translation=puw.quantity(plan["translation_nm"], "nm"),
            in_place=False,
        )

        def spec(sign, distance, axis_sign=1):
            return dict(
                feature_index=0,
                projection_direction=[0, 0, sign],
                distance=puw.quantity(distance, "nm"),
                target_normal=axis_sign * inventory["features"][0]["normal"],
                label=f"prespecified PHE404 face {sign} axis {axis_sign}",
                evidence={
                    "candidate": "methodological transformed PHE404, no binding-pose inference"
                },
            )

        def query(sign=1, distance=None, radius=None, axis_sign=1):
            return from_receptor_projections(
                inventory,
                projection_specs=[
                    spec(
                        sign,
                        plan["base_distance_nm"] if distance is None else distance,
                        axis_sign,
                    )
                ],
                radius=puw.quantity(
                    plan["base_radius_nm"] if radius is None else radius, "nm"
                ),
            )

        def record(cell_id, family, settings, model, candidate=moved, tolerance=None):
            tolerance = (
                plan["base_direction_tolerance_degrees"]
                if tolerance is None
                else tolerance
            )
            result = PoseEvaluator(
                model,
                direction_tolerance=puw.quantity(tolerance, "degrees"),
                min_fit_value=1,
            ).evaluate(candidate, selection=selection, pose_id=cell_id)
            rows.append(
                dict(
                    cell_id=cell_id,
                    family=family,
                    settings=settings,
                    model=native_record(model, directory, cell_id),
                    result=result,
                )
            )

        for fi, sign in enumerate(plan["face_signs"]):
            for ri, radius in enumerate(plan["radius_nm"]):
                for di, distance in enumerate(plan["distance_nm"]):
                    record(
                        f"placement-f{fi}-r{ri}-d{di}",
                        "placement",
                        dict(face=sign, distance_nm=distance, radius_nm=radius),
                        query(sign, distance, radius),
                    )

        wide = None
        for ei, radius in enumerate(plan["exclusion_radius_nm"]):
            model = StructureBasedModeler(
                source,
                feature_inventory=inventory,
                projection_specs=[spec(1, plan["base_distance_nm"])],
                radius=puw.quantity(plan["base_radius_nm"], "nm"),
                excluded_volume_inventory=heavy,
                excluded_volume_radius=puw.quantity(radius, "nm"),
            ).build([0])
            record(
                f"exclusion-{ei}", "exclusion", dict(exclusion_radius_nm=radius), model
            )
            wide = model
        wide_before = native_record(wide, directory, "wide-before")
        retained = extract_pharmacophore(
            wide,
            site_indices=[0],
            reason="prespecified removal of PHE404 exclusion vetoes",
        )
        record(
            "exclusion-removal", "curation", {"retained_site_indices": [0]}, retained
        )
        wide_after = native_record(wide, directory, "wide-after")

        for ai, sign in enumerate(plan["axis_signs"]):
            for ti, tolerance in enumerate(plan["direction_tolerance_degrees"]):
                record(
                    f"orientation-a{ai}-t{ti}",
                    "orientation",
                    dict(axis_sign=sign, tolerance_degrees=tolerance),
                    query(axis_sign=sign),
                    candidate=turned,
                    tolerance=tolerance,
                )

        baseline = query()
        record("original-pose", "original", {}, baseline, candidate=source)
        failed = PoseEvaluator(baseline).run(
            [source],
            on_error="record",
            selection=selection,
            structure_index=plan["invalid_frame"],
        )[0]
        rows.append(
            dict(
                cell_id="invalid-frame",
                family="failure",
                settings={"structure_index": plan["invalid_frame"]},
                model=native_record(baseline, directory, "invalid-frame"),
                result=failed,
            )
        )
        after = snapshot()
        inventories_after = native_record(holder, directory, "inventories-after")
        candidate_coordinates = {
            name: puw.get_value(msm.get(value, coordinates=True), to_unit="nm").tolist()
            for name, value in [("translated", moved), ("rotated_translated", turned)]
        }
    return dict(
        schema="pharmacophoremt.prepared-receptor-sensitivity-result@1",
        plan_sha256=hashlib.sha256(raw_plan).hexdigest(),
        policy=policy,
        input_identity=identity,
        selection=list(selection),
        inputs_before=before,
        inputs_after=after,
        inventories_before=inventories_before,
        inventories_after=inventories_after,
        wide_before=wide_before,
        wide_after=wide_after,
        candidate_coordinates_nm=candidate_coordinates,
        rows=rows,
        workflow_attribution=captured.attribution.to_dict(),
        application_policy_restored=puw.configure.report() == configuration,
        search_budget=0,
        holdout_access=False,
        scope="Analytical controls on cached prepared PHE404 geometry; transformed copies are methodological candidates, not new ligands or biological binding poses.",
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(PLAN.read_text())
    with TemporaryDirectory(prefix="phmt-prepared-sensitivity-") as temporary:
        output = [
            run_case(policy, Path(temporary) / str(index))
            for index, policy in enumerate(plan["policies"])
        ]
    args.output.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")
    print(
        json.dumps(
            {"policies": len(output), "attempts": sum(len(x["rows"]) for x in output)}
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
