"""Execute frozen #93 carbonyl receiving through public molecular/PHMT tools.

Source-only case orchestration. Run with --output FILE; this is not a public
acceptor profile, molecular geometry engine or installed package command.
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
from pharmacophoremt.io import load_json, load_yaml, to_yaml
from pharmacophoremt.modeler import from_receptor_projections, get_features
from pharmacophoremt.screening import PoseEvaluator
from phmt_test_support.prepared_workflow import models_equivalent
from phmt_test_support.receptor_contribution import _record_result, candidate_custody
from phmt_test_support.saved_model_reader import native_record

DATA = Path(__file__).resolve().parents[1] / "tests/data/carbonyl_acceptor_receiving"
PLAN_SHA256 = "b0af26640c0b7ff6cadde2c7f7e499141921adc29fd2ec7f4c1666218be92340"


def load_plan():
    raw = (DATA / "plan.json").read_bytes()
    if hashlib.sha256(raw).hexdigest() != PLAN_SHA256:
        raise ValueError("Frozen receiving plan changed; require a dated amendment")
    plan = json.loads(raw)
    if (
        hashlib.sha256((DATA / "provider_review.json").read_bytes()).hexdigest()
        != plan["provider_review_sha256"]
    ):
        raise ValueError("Frozen provider review changed")
    return plan


def verify_provider():
    review = json.loads((DATA / "provider_review.json").read_text())
    root = Path(msm.__file__).resolve().parents[1]
    for path, record in review["files"].items():
        if hashlib.sha256((root / path).read_bytes()).hexdigest() != record["sha256"]:
            raise ValueError("Reviewed experimental provider source changed: " + path)


def _integer(value, shape=None):
    array = np.asarray(value)
    if array.dtype.kind not in "iu" or (shape is not None and array.shape != shape):
        raise ValueError("Malformed provider integer correspondence")
    return array


def _receive_payload(payload, *, n_atoms, selection, structures):
    """Validate a cached source contract; compute no molecular geometry."""
    if (
        payload["schema"] != "molsysmt.hbond_site_directions@1"
        or payload["method"] != "ideal_local_geometry"
        or payload["site_method"] != "smarts_donor_acceptor"
        or payload["chemical_state_index"] != 0
        or payload["sites"]["chemical_state_index"] != 0
        or payload["parameters"]["pbc"] is not False
        or payload["assume_complete_connectivity"] is not False
        or payload["software"]["molsysmt"] != msm.__version__
        or payload["units"]["directions"] != "dimensionless"
    ):
        raise ValueError("Unexpected provider schema/method/state/producer/units")
    for field, expected in [
        ("site_roles", {0: "donor", 1: "acceptor"}),
        (
            "site_models",
            {
                0: "unsupported",
                1: "observed_donor_hydrogen",
                2: "carbonyl_trigonal",
                3: "aromatic_nitrogen_bisector",
                4: "nitrile_linear",
            },
        ),
        ("status", {0: "unsupported", 1: "defined", 2: "undefined"}),
    ]:
        if {int(k): v for k, v in payload["codes"][field].items()} != expected:
            raise ValueError("Provider code meanings changed")
    for key, expected in [
        ("atom_source_indices", list(range(n_atoms))),
        ("selected_atom_indices", selection),
        ("evaluated_structure_indices", structures),
    ]:
        if not np.array_equal(_integer(payload[key]), expected):
            raise ValueError("Provider source/selection/structure axis changed")
    anchors = _integer(payload["site_atom_indices"])
    n = len(anchors)
    roles = _integer(payload["site_roles"], (n,))
    models = _integer(payload["site_models"], (n,))
    status = _integer(payload["status"], (len(structures), n))
    offsets = _integer(payload["support_atom_offsets"], (n + 1,))
    support = _integer(payload["support_atom_indices"])
    if (
        anchors.ndim != 1
        or support.ndim != 1
        or np.any(anchors < 0)
        or np.any(anchors >= n_atoms)
        or np.any(support < 0)
        or np.any(support >= n_atoms)
        or not set(roles.tolist()) <= {0, 1}
        or not set(models.tolist()) <= {0, 1, 2, 3, 4}
        or not set(status.ravel().tolist()) <= {0, 1, 2}
        or offsets[0] != 0
        or offsets[-1] != len(support)
        or np.any(np.diff(offsets) < 1)
    ):
        raise ValueError("Invalid provider role/model/status/support codes")
    for site in range(n):
        if (
            support[offsets[site]] != anchors[site]
            or (roles[site] == 0) != (models[site] == 1)
            or (models[site] == 0 and np.any(status[:, site] != 0))
            or (models[site] != 0 and np.any(status[:, site] == 0))
        ):
            raise ValueError("Incoherent provider site/support/status")
    pairs = _integer(payload["donor_hydrogen_pairs"])
    acceptors = _integer(payload["acceptor_atom_indices"])
    if pairs.shape != (sum(roles == 0), 2) or not np.array_equal(
        anchors, np.concatenate([pairs[:, 0], acceptors])
    ):
        raise ValueError("Provider role/participant correspondence changed")
    directions = np.asarray(payload["directions"], dtype=float)
    count = len(directions)
    origins = np.asarray(puw.get_value(payload["origins"], to_unit="nm"))
    if (
        directions.shape != (count, 3)
        or origins.shape != (count, 3)
        or not np.isfinite(directions).all()
        or not np.isfinite(origins).all()
        or not np.allclose(np.linalg.norm(directions, axis=1), 1, atol=1e-12, rtol=0)
    ):
        raise ValueError("Invalid finite unit-bearing provider geometry")
    correspondence = [
        _integer(payload[key], (count,))
        for key in [
            "direction_structure_positions",
            "direction_site_indices",
            "direction_indices",
        ]
    ]
    expected = [
        (position, site, local)
        for position in range(len(structures))
        for site in range(n)
        if status[position, site] == 1
        for local in range(2 if models[site] == 2 else 1)
    ]
    actual = list(zip(*[v.tolist() for v in correspondence], strict=True))
    source_frames = _integer(payload["direction_structure_indices"], (count,))
    if actual != expected or source_frames.tolist() != [
        structures[position] for position, _, _ in actual
    ]:
        raise ValueError("Provider sparse source position/multiplicity changed")
    image_offsets = _integer(payload["image_offsets"], (count + 1,))
    images = _integer(payload["image_vectors"])
    lengths = [offsets[site + 1] - offsets[site] for _, site, _ in actual]
    if (
        image_offsets[0] != 0
        or np.diff(image_offsets).tolist() != lengths
        or images.shape != (sum(lengths), 3)
        or np.any(images)
    ):
        raise ValueError("Provider nonperiodic support-image packing changed")
    return [
        record
        for record, (_, site, _) in enumerate(actual)
        if roles[site] == 1 and models[site] == 2
    ]


def _declared_source(spec):
    source = msm.convert(
        msm.convert("smiles:" + spec["smiles"], to_form="rdkit.Mol"),
        to_form="molsysmt.MolSys",
    )
    coordinates = spec["coordinates"]
    source.structures.append(
        coordinates=puw.quantity(coordinates["values"], coordinates["unit"])
    )
    return source


def _custody(source):
    return dict(
        candidate_custody(source),
        analyses={
            key: detached(msm.convert(value, to_form="molsysmt.InteractionsDict").data)
            for key, value in source.interactions.items()
        },
    )


def _directions(source, spec, plan):
    return msm.interactions.hbonds.get_hbond_site_directions(
        source,
        selection=spec["selection"],
        structure_indices=spec.get(
            "structure_indices", spec.get("requested_structure_indices")
        ),
        chemical_state=plan["chemical_state"],
        method=plan["provider_method"],
        site_method=plan["site_method"],
        pbc=plan["pbc"],
    )


def _payload_record(payload):
    record = detached(payload)
    return dict(
        payload=record,
        sha256=hashlib.sha256(json.dumps(record, sort_keys=True).encode()).hexdigest(),
        array_layouts={
            key: dict(shape=list(value.shape), dtype=str(value.dtype))
            for key, value in payload.items()
            if isinstance(value, np.ndarray)
        },
    )


def _evaluator(model, plan):
    return PoseEvaluator(
        model,
        min_fit_value=plan["query"]["min_fit"],
        direction_tolerance=puw.quantity(1, "degrees"),
    )


def _block(source, payload, admitted, row, plan, directory, provider_sha256, output):
    inventory = get_features(
        source,
        selection=plan["source"]["selection"],
        structure_index=row["source_structure_index"],
        chemical_state=plan["chemical_state"],
        features=["hb acceptor"],
    )
    before = detached(inventory)
    output["inventory_before"] = before
    records = [
        i
        for i in admitted
        if payload["direction_structure_positions"][i] == row["structure_position"]
    ]
    models, model_rows = [], []
    output["models"] = model_rows
    for i in records:
        site = int(payload["direction_site_indices"][i])
        anchor = int(payload["site_atom_indices"][site])
        matches = [
            j
            for j, f in enumerate(inventory["features"])
            if f["atom_indices"] == [anchor]
        ]
        if len(matches) != 1:
            raise ValueError(
                "Provider acceptor does not map uniquely to native inventory"
            )
        feature = matches[0]
        if not np.allclose(
            puw.get_value(inventory["features"][feature]["center"], to_unit="nm"),
            puw.get_value(payload["origins"][i], to_unit="nm"),
            atol=1e-12,
            rtol=0,
        ):
            raise ValueError("Provider acceptor origin/inventory frame mismatch")
        direction = puw.quantity(payload["directions"][i], "dimensionless")
        model = from_receptor_projections(
            inventory,
            projection_specs=[
                dict(
                    feature_index=feature,
                    projection_direction=direction,
                    target_direction=-direction,
                    distance=puw.quantity(0.35, "nm"),
                    label=f"carbonyl lobe {int(payload['direction_indices'][i])}",
                    evidence=dict(
                        receiving_profile=plan["source_profile"],
                        provider_result_sha256=provider_sha256,
                        provider_schema=payload["schema"],
                        provider_method=payload["method"],
                        provider_software=payload["software"],
                        provider_record_index=i,
                        provider_site_index=site,
                        provider_local_direction=int(payload["direction_indices"][i]),
                        source_structure_position=row["structure_position"],
                        source_structure_index=row["source_structure_index"],
                        source_support=payload["support_atom_indices"][
                            payload["support_atom_offsets"][site] : payload[
                                "support_atom_offsets"
                            ][site + 1]
                        ],
                        target_direction_origin=plan["query"]["target_direction_rule"],
                    ),
                )
            ],
            radius=puw.quantity(0.02, "nm"),
            name=row["id"] + f"-lobe{len(models)}",
        )
        models.append(model)
        output["built_models"] = len(models)
        model_rows.append(
            dict(
                index=len(models) - 1,
                provider_record_index=i,
                native=native_record(
                    model, directory, row["id"] + f"-{len(models) - 1}"
                ),
            )
        )
    candidates, candidate_before, candidate_inventories = {}, {}, {}
    output.update(
        candidates_before=candidate_before, candidate_inventories=candidate_inventories
    )
    for control in plan["controls"]:
        candidate = _declared_source(
            dict(
                smiles=plan["candidate"]["smiles"],
                coordinates=plan["candidate"]["base_coordinates"],
            )
        )
        rotations = [
            plan["candidate"]["rotations_from_x_to_target"][control["source_lobe"]]
        ]
        if control["donor_axis_sign"] == 1:
            rotations.append(plan["candidate"]["reversed_axis_rotation"])
        rotations.append(
            plan["source"]["frame_transforms"][row["source_structure_index"]][
                "rotation"
            ]
        )
        for rotation in rotations:
            candidate = msm.structure.rotate(
                candidate,
                rotation=rotation,
                rotation_center=puw.quantity([0, 0, 0], "nm"),
                in_place=False,
            )
        displacement = control["displacement"]
        candidate = msm.structure.translate(
            candidate,
            translation=models[control["source_lobe"]].interaction_sites[0].center
            + puw.quantity(displacement["values"], displacement["unit"]),
            in_place=False,
        )
        inv = get_features(candidate, features=["hb donor"])
        if (
            len(inv["features"]) != 1
            or inv["features"][0]["atom_indices"] != plan["candidate"]["donor_pair"]
        ):
            raise ValueError("Declared indexed donor witness recognition changed")
        candidates[control["id"]] = candidate
        candidate_before[control["id"]] = _custody(candidate)
        candidate_inventories[control["id"]] = detached(inv)
    outcomes, recovery = {}, []
    output.update(outcomes=outcomes, recovery=recovery)
    for index, (model, model_row) in enumerate(zip(models, model_rows, strict=True)):
        evaluator = _evaluator(model, plan)
        for name, candidate in candidates.items():
            try:
                result = _record_result(
                    evaluator.evaluate(candidate, pose_id=name), model_row
                )
                outcome = dict(status="returned", model_index=index, result=result)
            except Exception as error:
                outcome = dict(
                    status="failed",
                    model_index=index,
                    error=dict(type=type(error).__name__, message=str(error)),
                )
            outcomes.setdefault(name, []).append(outcome)
        matching = f"lobe{index}_aligned"
        for suffix, read in [("json", load_json), ("yaml", load_yaml)]:
            try:
                path = directory / (row["id"] + f"-{index}." + suffix)
                if suffix == "yaml":
                    to_yaml(model, path)
                restored = read(path)
                native = native_record(
                    restored, directory, row["id"] + f"-{index}-read-" + suffix
                )
                recovery.append(
                    dict(
                        format=suffix,
                        model_index=index,
                        candidate=matching,
                        native_equivalent=models_equivalent(
                            model_row["native"], native
                        ),
                        native=native,
                        result=_evaluator(restored, plan).evaluate(
                            candidates[matching], pose_id=matching
                        ),
                    )
                )
            except Exception as error:
                recovery.append(
                    dict(
                        status="failed",
                        format=suffix,
                        model_index=index,
                        error=dict(type=type(error).__name__, message=str(error)),
                    )
                )
    output.update(
        cell_id=row["id"],
        status="returned",
        models=model_rows,
        outcomes=outcomes,
        recovery=recovery,
        inventory_before=before,
        inventory_after=detached(inventory),
        candidate_inventories=candidate_inventories,
        candidates_before=candidate_before,
        candidates_after={name: _custody(c) for name, c in candidates.items()},
    )


@_ackredit.attributed("molsysmt", "numpy", "pyunitwizard")
def _execute(directory, plan, requested, include_negatives):
    verify_provider()
    source = _declared_source(plan["source"])
    output = dict(
        schema="pharmacophoremt.carbonyl-acceptor-run@1",
        plan_sha256=PLAN_SHA256,
        source_before=_custody(source),
        policies=[],
        cells=[],
        failures=[],
    )
    for policy in plan["policies"]:
        rows = [
            r
            for r in plan["matrix"]
            if r["id"] in requested and r["policy_id"] == policy["id"]
        ]
        if not rows:
            continue
        with puw.context(standard_units=list(policy["standard_units"].values())):
            context = dict(
                policy_id=policy["id"],
                negative_queries=[],
                positive_provider_attempted=True,
            )
            output["policies"].append(context)
            try:
                payload = _directions(source, plan["source"], plan)
                context["provider"] = _payload_record(payload)
                admitted = _receive_payload(
                    payload, n_atoms=3, selection=[2], structures=[0, 1, 0]
                )
                for row in rows:
                    try:
                        record = dict(
                            cell_id=row["id"],
                            status="started",
                            models=[],
                            outcomes={},
                            recovery=[],
                        )
                        output["cells"].append(record)
                        _block(
                            source,
                            payload,
                            admitted,
                            row,
                            plan,
                            directory,
                            context["provider"]["sha256"],
                            record,
                        )
                    except Exception as error:
                        record.update(
                            status="failed",
                            error=dict(type=type(error).__name__, message=str(error)),
                        )
                    print("completed", row["id"], flush=True)
                context["provider_after"] = _payload_record(payload)
            except Exception as error:
                output["failures"].append(
                    dict(
                        stage="positive_provider_receiving",
                        policy_id=policy["id"],
                        type=type(error).__name__,
                        message=str(error),
                    )
                )
            if include_negatives:
                for spec in plan["negative_sources"]:
                    record = dict(id=spec["id"], models=[], score=None)
                    context["negative_queries"].append(record)
                    try:
                        negative = _declared_source(spec)
                        record["source_before"] = _custody(negative)
                        record["provider_attempted"] = True
                        raw = _directions(negative, spec, plan)
                        record["provider"] = _payload_record(raw)
                        n_atoms = len(spec["coordinates"]["values"][0])
                        selection = (
                            list(range(n_atoms))
                            if spec["selection"] == "all"
                            else spec["selection"]
                        )
                        records = _receive_payload(
                            raw, n_atoms=n_atoms, selection=selection, structures=[0]
                        )
                        record["admitted_records"] = records
                        record["admission_status"] = (
                            "no_defined_carbonyl"
                            if not records
                            else "unexpected_defined_carbonyl"
                        )
                        record["source_after"] = _custody(negative)
                    except Exception as error:
                        record["failure"] = dict(
                            type=type(error).__name__, message=str(error)
                        )
    output["source_after"] = _custody(source)
    returned = [c for c in output["cells"] if c["status"] == "returned"]
    output["actual_counts"] = dict(
        positive_provider_direction_calls=sum(
            p.get("positive_provider_attempted", False) for p in output["policies"]
        ),
        negative_provider_direction_calls=sum(
            n.get("provider_attempted", False)
            for p in output["policies"]
            for n in p["negative_queries"]
        ),
        source_position_policy_blocks=len(output["cells"]),
        returned_models=sum(c.get("built_models", 0) for c in output["cells"]),
        primary_evaluations=sum(
            len(v) for c in output["cells"] for v in c["outcomes"].values()
        ),
        recovery_evaluations=sum(len(c["recovery"]) for c in output["cells"]),
        negative_queries=sum(len(p["negative_queries"]) for p in output["policies"]),
        negative_pose_evaluations=0,
    )
    failed = (
        output["failures"]
        or len(returned) != len(output["cells"])
        or len(output["cells"]) != len(requested)
    )
    failed = failed or any(
        o["status"] != "returned"
        for c in returned
        for values in c["outcomes"].values()
        for o in values
    )
    failed = failed or any(
        not r.get("native_equivalent", False) for c in returned for r in c["recovery"]
    )
    failed = failed or any(
        n.get("failure") or n.get("admitted_records")
        for p in output["policies"]
        for n in p["negative_queries"]
    )
    output["execution_status"] = "partial_failure" if failed else "completed"
    return output


def run_study(directory, *, cell_ids=None, tracking=True):
    plan = load_plan()
    allowed = {r["id"] for r in plan["matrix"]}
    requested = allowed if cell_ids is None else set(cell_ids)
    if not requested or requested - allowed:
        raise ValueError("Choose a nonempty subset of frozen receiving cells")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    units = puw.configure.report()
    with attribution(enabled=tracking):
        result = _execute(directory, plan, requested, cell_ids is None)
    result["application_policy_restored"] = puw.configure.report() == units
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--cell", action="append", dest="cell_ids")
    parser.add_argument("--without-attribution", action="store_true")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(
        prefix="carbonyl-receiving-", dir=args.output.parent
    ) as work:
        result = run_study(
            work, cell_ids=args.cell_ids, tracking=not args.without_attribution
        )
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result["actual_counts"]), flush=True)
    return 0 if result["execution_status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
