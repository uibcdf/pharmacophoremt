"""Observed receptor geometry plus prepared EST, with explicit exclusion controls.

Run: python -m devtools.validate_eralpha_exclusions --output FILE
No receptor chemistry assignment, interaction detection or physical radius model.
"""

import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
from copy import deepcopy
from pathlib import Path

from devtools.audit_eralpha_receptor import RECEPTOR_SELECTION, _fingerprint
from devtools.benchmark_rigid_consensus import _source_record
from devtools.prepare_eralpha_hydrogens import SELECTED_FEATURES, add_hydrogens
from devtools.prepare_eralpha_ligand import ROOT, credit_inputs, prepare_case
from devtools.validate_eralpha_template import portable
from devtools.validate_prepared_ccd_ligands import scientific_projection


def workflow(directory):
    """Compose public extraction/construction/evaluation with local case choices."""
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.io import load_json, to_json
    from pharmacophoremt.modeler import (
        from_ligand,
        get_excluded_volume_sites,
        get_features,
    )
    from pharmacophoremt.screening import PoseEvaluator

    case = add_hydrogens(prepare_case())
    source = case["heavy_case"]["source"]
    ligand = case["molecular_system"]
    before_source, before_ligand = _fingerprint(source), _fingerprint(ligand)
    selection = (
        f"({RECEPTOR_SELECTION}) within 0.5 nm without pbc "
        'of (group_name == "EST" and chain_id == "D")'
    )
    groups = list(map(int, msm.select(source, selection=selection, element="group")))
    whole_residue_selection = f"group_index == {groups}"
    inventory = get_features(
        source, selection=whole_residue_selection, features=["included volume"]
    )
    readiness = msm.physchem.get_chemical_readiness(
        source, selection=inventory["selected_atom_indices"], structure_indices=0
    )
    # This deliberately broad positive radius makes the controlled colliding
    # translation retain all five feature matches. It is not a biological cutoff.
    query = from_ligand(ligand, features=SELECTED_FEATURES, radius="0.4 nm")
    baseline = PoseEvaluator(query, direction_tolerance="10 degrees", min_fit_value=1)
    unexcluded_reference = baseline.evaluate(ligand)
    exclusions = get_excluded_volume_sites(inventory, radius="0.1 nm")
    offset = query.n_interaction_sites
    for site in exclusions["interaction_sites"]:
        query.add_interaction_site(site)
    query.metadata["exclusion_construction"] = dict(
        report=exclusions["report"], attribution=exclusions.get("attribution")
    )
    evaluator = PoseEvaluator(query, direction_tolerance="10 degrees", min_fit_value=1)
    reference = evaluator.evaluate(ligand)

    receptor_target = msm.select(
        source, selection='chain_id == "A" and group_id == 353 and atom_name == "OE2"'
    )
    ligand_target = msm.select(ligand, selection='atom_name == "O3"')
    if len(receptor_target) != 1 or len(ligand_target) != 1:
        raise ValueError("Reviewed receptor/ligand collision targets changed")
    receptor_coordinates = puw.get_value(
        msm.get(source, coordinates=True), to_unit="nm"
    )
    ligand_coordinates = puw.get_value(msm.get(ligand, coordinates=True), to_unit="nm")
    translation = puw.quantity(
        receptor_coordinates[:, receptor_target, :]
        - ligand_coordinates[:, ligand_target, :],
        "nm",
    )
    collision = msm.structure.translate(ligand, translation=translation, in_place=False)
    unexcluded_collision = baseline.evaluate(collision)
    excluded_collision = evaluator.evaluate(collision)
    wide_exclusions = get_excluded_volume_sites(inventory, radius="0.35 nm")
    wide_query = from_ligand(ligand, features=SELECTED_FEATURES, radius="0.4 nm")
    for site in wide_exclusions["interaction_sites"]:
        wide_query.add_interaction_site(site)
    wide_reference = PoseEvaluator(
        wide_query, direction_tolerance="10 degrees", min_fit_value=1
    ).evaluate(ligand)

    path = Path(directory) / "est_with_receptor_exclusions.json"
    to_json(query, str(path))
    reloaded = load_json(str(path))
    loaded_evaluator = PoseEvaluator(
        reloaded, direction_tolerance="10 degrees", min_fit_value=1
    )
    return dict(
        schema="pharmacophoremt.eralpha_exclusion_workflow@1",
        ligand_preparation=case["report"],
        receptor_selection=RECEPTOR_SELECTION,
        spatial_selection=selection,
        whole_residue_selection=whole_residue_selection,
        receptor_group_indices=groups,
        receptor_chemical_readiness=readiness,
        construction=dict(
            report=exclusions["report"], attribution=exclusions.get("attribution")
        ),
        wide_construction_report=wide_exclusions["report"],
        query_site_offset=offset,
        query_metadata=deepcopy(query.metadata),
        collision_targets=dict(
            receptor_source_atom_index=int(receptor_target[0]),
            ligand_atom_index=int(ligand_target[0]),
            translation=puw.QuantityRecord.from_quantity(translation).to_dict(),
        ),
        outcomes=dict(
            unexcluded_reference=unexcluded_reference,
            reference=reference,
            unexcluded_collision=unexcluded_collision,
            collision=excluded_collision,
            wide_radius_reference=wide_reference,
            reloaded_reference=loaded_evaluator.evaluate(ligand),
            reloaded_collision=loaded_evaluator.evaluate(collision),
        ),
        query_metadata_preserved=reloaded.metadata == query.metadata,
        source_unchanged=before_source == _fingerprint(source),
        ligand_unchanged=before_ligand == _fingerprint(ligand),
        heavy_pose_preserved=bool(
            np.array_equal(
                receptor_coordinates[:, case["report"]["source_atom_indices"], :],
                ligand_coordinates[:, :20, :],
            )
        ),
        policy=dict(
            reference_frame="unchanged deposited 1QKU heavy pose",
            positive_radius="0.4 nm analytical collision control",
            excluded_radius="0.1 nm caller choice",
            sensitivity_radius="0.35 nm caller choice",
            receptor_chemistry="not_prepared",
            interaction_detection="not_performed",
            biological_validation="not_performed",
            physical_radius_model="not_used",
            pbc=False,
            waters="excluded",
            bioassembly="not_constructed",
        ),
    )


def valid(run):
    outcomes = run["outcomes"]
    return (
        run["source_unchanged"]
        and run["ligand_unchanged"]
        and run["heavy_pose_preserved"]
        and run["query_metadata_preserved"]
        and len(run["receptor_group_indices"]) == 19
        and run["construction"]["report"]["n_sites"] == 153
        and all(
            outcomes[key]["status"] == "matched"
            for key in (
                "unexcluded_reference",
                "reference",
                "unexcluded_collision",
                "reloaded_reference",
            )
        )
        and all(
            outcomes[key]["status"] == "not_matched"
            for key in (
                "collision",
                "wide_radius_reference",
                "reloaded_collision",
            )
        )
        and all(value["fit_value"] == 1 for value in outcomes.values())
    )


def main(argv=None):
    import tempfile
    from datetime import datetime, timezone

    import ackredit
    import molsysmt as msm
    import pyunitwizard

    import pharmacophoremt as phmt

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    producers = dict(
        pharmacophoremt=phmt, molsysmt=msm, pyunitwizard=pyunitwizard, ackredit=ackredit
    )
    before = {name: _source_record(module) for name, module in producers.items()}
    paths = [
        ROOT / name
        for name in (
            "devtools/validate_eralpha_exclusions.py",
            "devtools/audit_eralpha_receptor.py",
            "devtools/prepare_eralpha_ligand.py",
            "devtools/prepare_eralpha_hydrogens.py",
            "devtools/prepared_ccd_ligands.py",
            "devtools/validate_eralpha_template.py",
            "devtools/validate_prepared_ccd_ligands.py",
            "devtools/benchmark_rigid_consensus.py",
            "tests/data/eralpha_rcsb/1qku.cif",
            "tests/data/eralpha_rcsb/EST.cif",
            "tests/data/eralpha_rcsb/manifest.json",
            "tests/data/eralpha_template/est_template.h5msm",
            "tests/data/eralpha_template/manifest.json",
            "tests/data/eralpha_template/acquisition.json",
        )
    ]

    def input_hashes():
        return {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths
        }

    inputs, runs = input_hashes(), []
    for enabled in (False, True):
        with (
            ackredit.session("observed receptor geometry exclusions"),
            phmt.attribution(enabled),
        ):
            with tempfile.TemporaryDirectory(prefix="phmt-exclusions-") as directory:
                with ackredit.capture(
                    "prepared ligand and receptor geometry composition"
                ) as capture:
                    run = portable(workflow(directory))
                    if enabled:
                        credit_inputs()
                run["attribution"] = capture.attribution.to_dict()
                runs.append(dict(host_tracking=enabled, valid=valid(run), result=run))
    after = {name: _source_record(module) for name, module in producers.items()}
    report = dict(
        schema="pharmacophoremt.eralpha_exclusion_validation@1",
        created_utc=datetime.now(timezone.utc).isoformat(),
        python=platform.python_version(),
        environment=before,
        executable=sys.executable,
        versions={
            name: importlib.metadata.version(name)
            for name in (
                "numpy",
                "scipy",
                "rdkit",
                "argdigest",
                "depdigest",
                "smonitor",
            )
        },
        molecular_extensions=[
            dict(
                module=name,
                path=module.__file__,
                sha256=hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest(),
            )
            for name, module in sorted(sys.modules.items())
            if name.startswith("molsysmt")
            and getattr(module, "__file__", None)
            and Path(module.__file__).suffix in {".so", ".pyd", ".dylib"}
        ],
        inputs=inputs,
        producers_unchanged=before == after,
        inputs_unchanged=inputs == input_hashes(),
        runs=runs,
        tracking_independent_science=(
            scientific_projection(runs[0]["result"])
            == scientific_projection(runs[1]["result"])
        ),
        timing="not_measured",
        memory="not_measured",
    )
    report["valid"] = (
        report["producers_unchanged"]
        and report["inputs_unchanged"]
        and report["tracking_independent_science"]
        and all(run["valid"] for run in runs)
    )
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print("PASS" if report["valid"] else "FAIL", "observed receptor exclusion geometry")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
