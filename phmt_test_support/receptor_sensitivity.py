"""Fixed receptor projection experiment; no molecular or parameter-search engine.

Run: python -m phmt_test_support.receptor_sensitivity --output FILE
The declaration fixes every setting before execution; all chemistry uses MolSysMT.
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
    edit_pharmacophore,
    extract_pharmacophore,
    from_receptor_projections,
    get_features,
)
from pharmacophoremt.screening import PoseEvaluator
from phmt_test_support.absence_inputs import system
from phmt_test_support.interaction_cases import aromatic_build_case
from phmt_test_support.saved_model_reader import native_record

PLAN = Path(__file__).resolve().parents[1] / "tests/data/receptor_sensitivity/plan.json"


def run_case(policy, directory):
    """Execute all declared cells once, retaining complete native models/results."""
    declaration_bytes = PLAN.read_bytes()
    plan = json.loads(declaration_bytes)
    rows = []
    configuration = puw.configure.report()
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with puw.context(standard_units=policy), attribution():
        charge = plan["charge_input"]
        source = system(charge["smiles"], charge["coordinates_nm"])
        aromatic, first_ring, second_ring = aromatic_build_case("parallel")
        sources = {"charge": source, "aromatic": aromatic}
        coordinates_before = {
            name: puw.get_value(msm.get(value, coordinates=True), to_unit="nm").tolist()
            for name, value in sources.items()
        }
        receptor = get_features(
            source, selection=charge["receptor_selection"], features=["positive charge"]
        )
        heavy = get_features(source, selection=[0], features=["included volume"])
        ring = get_features(aromatic, selection=first_ring, features=["aromatic ring"])
        inventories = Pharmacophore()
        inventories.metadata = {"charge": receptor, "heavy": heavy, "ring": ring}
        inventories_before = native_record(inventories, directory, "inventories-before")

        def specification(index, distance):
            return dict(
                feature_index=index,
                projection_direction=[1, 0, 0],
                distance=puw.quantity(distance, "nm"),
                label=f"prespecified charge projection {index}",
            )

        def charge_query(distance, radius):
            return from_receptor_projections(
                receptor,
                projection_specs=[specification(0, distance)],
                radius=puw.quantity(radius, "nm"),
            )

        def record(
            cell_id,
            family,
            settings,
            query,
            molecular_system=source,
            selection=None,
            **options,
        ):
            result = PoseEvaluator(query, **options).evaluate(
                molecular_system,
                selection=charge["candidate_selection"]
                if selection is None
                else selection,
                pose_id=cell_id,
            )
            rows.append(
                dict(
                    cell_id=cell_id,
                    family=family,
                    settings=settings,
                    result=result,
                    model=native_record(query, directory, cell_id),
                )
            )

        for ri, radius in enumerate(plan["radius_nm"]):
            for di, distance in enumerate(plan["distance_nm"]):
                record(
                    f"placement-r{ri}-d{di}",
                    "placement",
                    dict(distance_nm=distance, radius_nm=radius),
                    charge_query(distance, radius),
                )

        for di, distance in enumerate(plan["point_contrast_distance_nm"]):
            for ti, tolerance in enumerate(plan["point_tolerance_nm"]):
                record(
                    f"point-contrast-d{di}-t{ti}",
                    "point_contrast",
                    dict(distance_nm=distance, point_tolerance_nm=tolerance),
                    charge_query(distance, plan["point_contrast_radius_nm"]),
                    point_tolerance=puw.quantity(tolerance, "nm"),
                )

        # The facade requires matching cached selection/frame/state declarations.
        single = get_features(source, selection=[0], features=["positive charge"])
        for ei, radius in enumerate(plan["exclusion_radius_nm"]):
            query = StructureBasedModeler(
                source,
                feature_inventory=single,
                projection_specs=[specification(0, 0.5)],
                radius="0.125 nm",
                excluded_volume_inventory=heavy,
                excluded_volume_radius=puw.quantity(radius, "nm"),
            ).build()
            record(
                f"exclusion-{ei}", "exclusion", dict(exclusion_radius_nm=radius), query
            )

        base = from_receptor_projections(
            receptor,
            projection_specs=[specification(0, 0.5), specification(1, 0.5)],
            radius="0.125 nm",
        )
        base_before = native_record(base, directory, "constraint-source-before")
        for variant in plan["constraint_variants"]:
            operation = variant["operation"]
            reason = "prespecified analytical ablation: " + operation
            if operation == "baseline":
                query = base
            elif operation in {"remove_missing", "remove_present"}:
                query = extract_pharmacophore(
                    base,
                    site_indices=[0 if operation == "remove_missing" else 1],
                    reason=reason,
                )
            else:
                options = {"essential": operation == "essential_zero"}
                if operation in {"essential_zero", "optional_zero"}:
                    options["weight"] = 0
                query = edit_pharmacophore(
                    base, site_indices=[1], reason=reason, **options
                )
            record(
                "constraint-" + variant["id"],
                "constraint",
                dict(operation=operation, min_fit_value=variant["min_fit_value"]),
                query,
                min_fit_value=variant["min_fit_value"],
            )
        base_after = native_record(base, directory, "constraint-source-after")

        for ti, tolerance in enumerate(plan["direction_tolerance_degrees"]):
            for ai, angle in enumerate(plan["aromatic_tilt_degrees"]):
                radians = np.deg2rad(angle)
                query = from_receptor_projections(
                    ring,
                    radius="0.125 nm",
                    projection_specs=[
                        dict(
                            feature_index=0,
                            projection_direction=[0, 0, 1],
                            distance="0.35 nm",
                            label=f"declared axis tilt {angle}",
                            target_normal=[np.sin(radians), 0, np.cos(radians)],
                        )
                    ],
                )
                record(
                    f"aromatic-t{ti}-a{ai}",
                    "aromatic",
                    dict(tilt_degrees=angle, direction_tolerance_degrees=tolerance),
                    query,
                    molecular_system=aromatic,
                    selection=second_ring,
                    direction_tolerance=puw.quantity(tolerance, "degrees"),
                )

        invalid_query = charge_query(0.5, 0.125)
        failure = PoseEvaluator(invalid_query).run(
            [source],
            on_error="record",
            selection=charge["candidate_selection"],
            structure_index=plan["invalid_frame"],
        )[0]
        rows.append(
            dict(
                cell_id="invalid-frame",
                family="failure",
                settings={"structure_index": plan["invalid_frame"]},
                result=failure,
                model=native_record(invalid_query, directory, "invalid-frame"),
            )
        )
        coordinates_after = {
            name: puw.get_value(msm.get(value, coordinates=True), to_unit="nm").tolist()
            for name, value in sources.items()
        }
        inventories_after = native_record(inventories, directory, "inventories-after")
    return dict(
        schema="pharmacophoremt.receptor-sensitivity-result@1",
        plan_sha256=hashlib.sha256(declaration_bytes).hexdigest(),
        policy=policy,
        rows=rows,
        source_coordinates_before_nm=coordinates_before,
        source_coordinates_after_nm=coordinates_after,
        inventories_before=inventories_before,
        inventories_after=inventories_after,
        constraint_source_before=base_before,
        constraint_source_after=base_after,
        application_policy_restored=puw.configure.report() == configuration,
        scope="Analytical fixed-pose parameter settings, not independent molecules or biological validation.",
        search_budget=0,
        holdout_access=False,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(PLAN.read_text())
    with TemporaryDirectory(prefix="phmt-receptor-sensitivity-") as temporary:
        output = [
            run_case(policy, Path(temporary) / str(index))
            for index, policy in enumerate([plan["policy"], plan["alternate_policy"]])
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
