"""Fixed cached ERalpha receptor/observed workflow control, owned by PHMT #52.

Use prepared_workflow --case receptor --output FILE. All molecular decoding,
selection, recognition, geometry and transforms belong to public MolSysMT.
"""

import hashlib
import json
import subprocess
import sys

from devtools.evidence_archive import read_archived_bytes
from devtools.prepared_ccd_ligands import ROOT, state_payload
from devtools.prepared_workflow import codecs, models_equivalent, native_record
from devtools.validate_eralpha_template import portable

SUMMARY = ROOT / "devguide/evidence/eralpha_interface_py314_summary.json"
MANIFEST = ROOT / "tests/data/eralpha_interface/manifest.json"
ARTIFACT = SUMMARY.with_name("eralpha_interface_prepared_py314.h5msm.gz")
INPUT_COMMIT = "a64e369eae1bbd331b7cfd2f17371ce38b73d284"
MODEL_NAMES = ("projected", "opposite", "collision", "observed")
PHE_ATOMS = [791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801]
RING_ATOMS = [796, 797, 798, 799, 800, 801]


def load_input(directory):
    """Load this fixed archived input; no preparation or detection is executed."""
    import molsysmt as msm

    summary, raw = read_archived_bytes(SUMMARY, identity_key="native_evidence")
    path = directory / "prepared-source.h5msm"
    path.write_bytes(raw)
    return msm.convert(str(path), to_form="molsysmt.MolSys"), dict(
        native_evidence=summary["native_evidence"],
        historical_producers=summary["producers"],
        historical_recorded_utc=summary["recorded_utc"],
        original_summary=str(SUMMARY.relative_to(ROOT)),
        preparation="Historical declared fragment; loaded unchanged, not regenerated",
    )


def credit_input():
    """Credit the actually loaded derived artifact; preparation stays historical."""
    import ackredit

    identity = json.loads(SUMMARY.read_text())["native_evidence"]
    item_id = (
        "pharmacophoremt:dataset:prepared-eralpha:" + identity["uncompressed_sha256"]
    )
    ackredit.register_item(
        id=item_id,
        type="dataset",
        title="Archived declared prepared 1QKU ERalpha fragment/EST",
        url="https://github.com/uibcdf/pharmacophoremt/blob/"
        + INPUT_COMMIT
        + "/devguide/evidence/"
        + identity["path"],
        publisher="PharmacophoreMT maintainers",
    )
    ackredit.track_item(
        item_id,
        used_by=__name__ + ".load_input",
        roles=["input_data"],
        context=dict(
            sha256=identity["uncompressed_sha256"],
            artifact=identity["path"],
            preparation="Historical provenance; no new preparation/detection credit",
        ),
    )


def projections(source, inventory, heavy):
    """Declare two synthetic faces and an independently broadened exclusion veto."""
    from pharmacophoremt.modeler import StructureBasedModeler

    models = {}
    facade = None
    for name, sign, radius in (
        ("projected", 2, ".01 nm"),
        ("opposite", -2, ".01 nm"),
        ("collision", 2, ".40 nm"),
    ):
        facade = StructureBasedModeler(
            source,
            feature_inventory=inventory,
            projection_specs=[
                dict(
                    feature_index=0,
                    projection_direction=[0, 0, sign],
                    distance=".35 nm",
                    target_normal=inventory["features"][0]["normal"],
                    label=name + " synthetic PHE404 ring placement",
                    evidence=dict(
                        producer="caller-declared analytical control",
                        orientation_policy="Explicitly retain the cached provider ring axis",
                    ),
                )
            ],
            radius=".02 nm",
            name=name,
            excluded_volume_inventory=heavy,
            excluded_volume_radius=radius,
        )
        models[name] = facade.build([0])
    return models, facade


def run_case(directory, *, fresh_reader=False):
    import molsysmt as msm

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt._private.smonitor.exceptions import ArgumentError
    from pharmacophoremt.modeler import (
        ComplexBasedModeler,
        StructureBasedModeler,
        get_features,
    )
    from pharmacophoremt.screening import PoseEvaluator

    source, identity = load_input(directory)
    selection = msm.select(source, selection='group_id == "404"')
    ligand = msm.select(source, selection='group_name == "EST"')
    analyses = {
        label: source.interactions[label]
        for label in ("hydrophobic", "hbonds", "pi_pi")
    }

    def snapshot():
        return dict(
            coordinates_nm=puw.get_value(
                msm.get(source, coordinates=True), to_unit="nm"
            ).tolist(),
            # Keep native unknown NaNs as literal text in a finite outer JSON record.
            chemical_state_json=json.dumps(state_payload(source), sort_keys=True),
            analyses={
                label: portable(
                    msm.convert(value, to_form="molsysmt.InteractionsDict").data
                )
                for label, value in analyses.items()
            },
        )

    before = snapshot()
    inventory = get_features(source, selection=selection, features=["aromatic ring"])
    heavy = get_features(source, selection=selection, features=["included volume"])
    models, structure_facade = projections(source, inventory, heavy)
    complex_facade = ComplexBasedModeler(
        source,
        ligand_selection=ligand,
        interaction_collection=analyses,
        name="observed",
    )
    models["observed"] = complex_facade.build([0])
    original = {
        name: native_record(model, directory, name + "-original")
        for name, model in models.items()
    }
    failures = {}
    for name, facade in (("structure", structure_facade), ("complex", complex_facade)):
        try:
            facade.build([1])
        except (ArgumentError, msm.ArgumentError) as error:
            failures[name] = dict(
                code=error.code,
                message=str(error),
                result_is_none=facade.result is None,
            )
        else:
            raise RuntimeError(
                "An uncached/unevaluated frame must fail without stale results"
            )
    complex_facade.interaction_collection = {
        label: value.invalidate_structures([0]) for label, value in analyses.items()
    }
    try:
        complex_facade.build([0])
    except ArgumentError as error:
        failures["complex_uncovered"] = dict(
            code=error.code,
            message=str(error),
            result_is_none=complex_facade.result is None,
            requested_frame=0,
            evaluated_structure_indices={
                label: list(value.evaluated_structure_indices)
                for label, value in complex_facade.interaction_collection.items()
            },
        )
    else:
        raise RuntimeError("Invalidated observations cannot cover an existing frame")
    empty = StructureBasedModeler(
        source, feature_inventory=inventory, projection_specs=[]
    ).build()
    excluded_only = StructureBasedModeler(
        source,
        feature_inventory=inventory,
        projection_specs=[],
        excluded_volume_inventory=heavy,
        excluded_volume_radius=".01 nm",
    ).build()
    empty_rejections = {}
    for name, model in (("empty", empty), ("exclusion_only", excluded_only)):
        try:
            PoseEvaluator(model)
        except ArgumentError as error:
            empty_rejections[name] = dict(code=error.code, message=str(error))
        else:
            raise RuntimeError(
                "Empty or exclusion-only models cannot be positive queries"
            )
    moved = msm.structure.translate(source, translation="[0,0,.35] nm", in_place=False)

    far = msm.structure.translate(source, translation="[2,0,0] nm", in_place=False)

    def outcomes(model, name):
        evaluator = PoseEvaluator(
            model, direction_tolerance="1 degree", min_fit_value=1
        )
        selected = ligand if name == "observed" else selection
        return dict(
            original=evaluator.evaluate(source, selection=selected),
            translated=evaluator.evaluate(
                far if name == "observed" else moved, selection=selected
            ),
        )

    results, artifacts = {}, {}
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        for suffix, write, read in codecs():
            for name, model in models.items():
                path = directory / (name + "." + suffix)
                write(model, path)
                raw = path.read_bytes()
                artifacts[path.name] = dict(
                    sha256=hashlib.sha256(raw).hexdigest(),
                    byte_count=len(raw),
                    utf8=raw.decode(),
                )
                with puw.context(standard_units=["angstrom", "ps", "radians"]):
                    restored = read(path)
                    results[path.name] = dict(
                        native=native_record(restored, directory, "restored"),
                        outcomes=outcomes(restored, name),
                    )
    reader = None
    if fresh_reader:
        child = subprocess.run(
            [
                sys.executable,
                "-m",
                "devtools.prepared_workflow",
                "--case",
                "receptor",
                "--read",
                str(directory),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        reader = dict(**json.loads(child.stdout), stderr=child.stderr)
    after = snapshot()
    return dict(
        input_identity=identity,
        translated_coordinates_nm=puw.get_value(
            msm.get(moved, coordinates=True), to_unit="nm"
        ).tolist(),
        displaced_coordinates_nm=puw.get_value(
            msm.get(far, coordinates=True), to_unit="nm"
        ).tolist(),
        inputs_before=before,
        inputs_after=after,
        source_coordinates_states_and_analyses_unchanged=before == after,
        selection=list(selection),
        ligand_selection=list(ligand),
        projected_inventory=original["projected"]["metadata"]["source_inventory"],
        models=original,
        empty=native_record(empty, directory, "empty"),
        exclusion_only=native_record(excluded_only, directory, "exclusion-only"),
        empty_query_rejections=empty_rejections,
        failed_rebuilds=failures,
        oracle=dict(
            ring_atom_indices=RING_ATOMS,
            heavy_atom_indices=PHE_ATOMS,
            frozen_ring_center_nm=[10.3282, 1.9207666666666665, 2.0210166666666667],
            declared_translation_nm=[0, 0, 0.35],
            observed_displacement_nm=[2, 0, 0],
            projected_separation_nm=0.70,
            narrow_exclusion_radius_nm=0.01,
            veto_radius_nm=0.40,
            expected_hydrophobic_source_pairs=json.loads(MANIFEST.read_text())[
                "expected_hydrophobic_source_pairs"
            ],
            coordinate_tolerance_nm=1e-12,
            candidate_policy="Translated PHE404 is a methodological molecular candidate, not a different ligand/conformer or biological binding prediction",
        ),
        results=results,
        artifacts=artifacts,
        fresh_reader=reader,
    )


def expectations_passed(result):
    if not result["source_coordinates_states_and_analyses_unchanged"]:
        return False
    if not all(row["result_is_none"] for row in result["failed_rebuilds"].values()):
        return False
    if (
        result["empty"]["interaction_sites"]
        or len(result["exclusion_only"]["interaction_sites"]) != 11
    ):
        return False
    expected = {
        "projected": (("not_matched", 0), ("matched", 1)),
        "opposite": (("not_matched", 0), ("not_matched", 0)),
        "collision": (("not_matched", 0), ("not_matched", 1)),
        "observed": (("matched", 1), ("not_matched", 0)),
    }
    for key, record in result["results"].items():
        name = key.split(".")[0]
        if not models_equivalent(record["native"], result["models"][name]):
            return False
        for position, (status, score) in zip(
            ("original", "translated"), expected[name]
        ):
            row = record["outcomes"][position]
            if row["status"] != status or row["fit_value"] != score:
                return False
    reader = result["fresh_reader"]
    return reader is None or (
        not reader["attribution"]["uses"]
        and all(
            models_equivalent(model, result["models"][key.split(".")[0]])
            for key, model in reader["models"].items()
        )
    )
