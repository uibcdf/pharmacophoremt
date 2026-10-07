"""Reproducible native 1QKU fragment/EST preparation and hypothesis controls.

Run: python -m devtools.validate_eralpha_interface --output FILE
Analytical acceptance only; no affinity, enrichment or environment refinement.
"""

import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from devtools.audit_eralpha_receptor import RECEPTOR_SELECTION
from devtools.benchmark_rigid_consensus import _source_record
from devtools.prepare_eralpha_interface import MANIFEST, prepare_interface
from devtools.prepare_eralpha_ligand import ROOT, credit_inputs
from devtools.validate_eralpha_template import portable
from devtools.validate_prepared_ccd_ligands import scientific_projection


def build_hypothesis(case):
    """Compose observed contacts and reference features, then explicitly curate.

    Empty evaluated families remain in the observed component. Ligand-reference
    sites are separately labeled; they do not become receptor observations.
    Hydrophobic weights are caller choices fixed in the case declaration.
    """
    from pharmacophoremt import modeler

    policy = case["report"]["declaration"]["hypothesis"]
    source, ligand = case["molecular_system"], case["ligand"]
    observed = modeler.from_interaction_collection(
        source,
        case["analyses"],
        ligand,
        radius=policy["observed_radius"],
        name="prepared_fragment_observations",
    )
    reference = modeler.from_ligand(
        source,
        selection=ligand,
        features=policy["reference_features"],
        radius=policy["reference_radius"],
        name="observed_EST_reference",
    )
    combined = modeler.compose_pharmacophores(
        {"observed_contacts": observed, "ligand_reference": reference},
        duplicate_policy="keep",
        name="declared_fragment_and_EST_hypothesis",
    )
    indices = modeler.get_interaction_site_indices(
        combined, feature_names="hydrophobicity"
    )
    curated = modeler.edit_pharmacophore(
        combined,
        site_indices=indices,
        weight=policy["hydrophobic_weight"],
        reason="Case-declared hydrophobic weight; no fit optimization",
    )
    curated.metadata["case_scope"] = dict(
        source_sha256=case["report"]["declaration"]["source_sha256"],
        model="explicit_closed_fragment_304_550_plus_EST",
        full_receptor_acceptance=False,
        environmental_refinement="not_performed",
        reference_sites_are_receptor_observations=False,
    )
    return dict(
        observed=observed, reference=reference, combined=combined, curated=curated
    )


def controls(case, directory):
    """Exercise independent placed geometry, exclusions, units and saved readers.

    Accepts the explicit prepared case to reuse preparation without rerunning
    detectors. Does not align poses, optimize cutoffs or select a best hypothesis.
    """
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import modeler
    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.io import load_json, to_json
    from pharmacophoremt.screening import PoseEvaluator

    source, ligand = case["molecular_system"], case["ligand"]
    before_state = msm.convert(
        source.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    before_xyz = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    models = build_hypothesis(case)
    query = models["curated"]
    policy = case["report"]["declaration"]["hypothesis"]

    def evaluate(hypothesis, system=source):
        return PoseEvaluator(
            hypothesis,
            direction_tolerance=policy["direction_tolerance"],
            min_fit_value=1,
        ).evaluate(system, selection=ligand)

    positive = evaluate(query)
    displaced = msm.structure.translate(
        source,
        selection=ligand,
        translation=puw.quantity([[[2, 0, 0]]], "nm"),
        in_place=False,
    )
    negative = evaluate(query, displaced)
    donor_index = modeler.get_interaction_site_indices(query, feature_names="hb donor")[
        0
    ]
    ring_index = modeler.get_interaction_site_indices(
        query, feature_names="aromatic ring"
    )[0]
    reversed_donor = modeler.copy_pharmacophore(query)
    reversed_donor.interaction_sites[donor_index].shape.direction *= -1
    donor_negative = evaluate(reversed_donor)
    reversed_normal = modeler.copy_pharmacophore(query)
    reversed_normal.interaction_sites[ring_index].shape.normal *= -1
    normal_sign = evaluate(reversed_normal)
    normal = puw.get_value(
        query.interaction_sites[ring_index].shape.normal, to_unit="dimensionless"
    )
    axis = np.eye(3)[int(np.argmin(np.abs(normal)))]
    orthogonal = np.cross(normal, axis)
    orthogonal /= np.linalg.norm(orthogonal)
    tilted = modeler.copy_pharmacophore(query)
    tilted.interaction_sites[ring_index].shape.normal = puw.quantity(
        orthogonal, "dimensionless"
    )
    angular_negative = evaluate(tilted)

    raw = case["source"]
    shell = f'({RECEPTOR_SELECTION}) within 0.5 nm without pbc of (group_name == "EST" and chain_id == "D")'
    groups = list(map(int, msm.select(raw, selection=shell, element="group")))
    raw_shell_atoms = msm.select(raw, selection=f"group_index == {groups}")
    ids = sorted(
        set(
            map(
                int,
                msm.get(raw, element="atom", selection=raw_shell_atoms, group_id=True),
            )
        )
    )
    # Use the retained original-atom map to cross the preparation/merge domain.
    # Exclusions use observed heavy atoms; generated H have source index -1.
    prepared_shell = np.flatnonzero(
        np.isin(case["report"]["atom_source_indices"], raw_shell_atoms)
    )
    inventory = modeler.get_features(
        source,
        selection=prepared_shell,
        features=["included volume"],
    )
    exclusions = modeler.get_excluded_volume_sites(
        inventory, radius=policy["exclusion_radius"]
    )
    broad = modeler.edit_pharmacophore(
        query,
        radius=policy["collision_control_radius"],
        reason="Independent collision-veto control retaining positive matches",
    )
    excluded = modeler.copy_pharmacophore(broad)
    for site in exclusions["interaction_sites"]:
        excluded.add_interaction_site(site)
    receptor_target = msm.select(
        source, selection='chain_id == "A" and group_id == 353 and atom_name == "OE2"'
    )
    ligand_target = msm.select(
        source, selection='group_name == "EST" and atom_name == "O3"'
    )
    if len(receptor_target) != 1 or len(ligand_target) != 1:
        raise ValueError("Reviewed collision targets changed")
    xyz = puw.get_value(msm.get(source, coordinates=True), to_unit="nm")
    translation = puw.quantity(xyz[:, receptor_target] - xyz[:, ligand_target], "nm")
    colliding = msm.structure.translate(
        source, selection=ligand, translation=translation, in_place=False
    )
    exclusion_outcomes = dict(
        reference=evaluate(excluded),
        unexcluded_collision=evaluate(broad, colliding),
        collision=evaluate(excluded, colliding),
    )

    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    molecular_path, query_path = (
        directory / "prepared_interface.h5msm",
        directory / "query.json",
    )
    msm.convert(source, to_form=molecular_path)
    to_json(query, str(query_path))
    restored_system = msm.convert(molecular_path, to_form="molsysmt.MolSys")
    restored_query = load_json(str(query_path))
    with puw.context(
        standard_units=["pm", "fs", "coulomb", "radians", "dimensionless"]
    ):
        unit_result = evaluate(query)
        reloaded = evaluate(restored_query, restored_system)
        rebuilt = modeler.from_interaction_collection(
            restored_system,
            restored_system.interactions,
            ligand,
            radius=policy["observed_radius"],
        )
        rebuilt_result = evaluate(rebuilt, restored_system)
    np.testing.assert_equal(
        source.chemical_states.get_preparation_history(),
        restored_system.chemical_states.get_preparation_history(),
    )
    expected_reloaded = deepcopy(before_state)
    # H5MSM canonicalizes only these fixture string-column declarations.
    for column in ("component_name", "component_type"):
        expected_reloaded["states"][0]["components"]["columns"][column]["dtype"] = (
            "string"
        )
    np.testing.assert_equal(
        expected_reloaded,
        msm.convert(
            restored_system.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        ).to_dict(),
    )
    np.testing.assert_array_equal(
        before_xyz,
        puw.get_value(msm.get(restored_system, coordinates=True), to_unit="nm"),
    )
    np.testing.assert_equal(
        before_state,
        msm.convert(
            source.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        ).to_dict(),
    )
    np.testing.assert_array_equal(
        before_xyz, puw.get_value(msm.get(source, coordinates=True), to_unit="nm")
    )
    preserved_analyses = all(
        portable(
            msm.convert(
                case["analyses"][label], to_form="molsysmt.InteractionsDict"
            ).data
        )
        == portable(
            msm.convert(
                restored_system.interactions[label], to_form="molsysmt.InteractionsDict"
            ).data
        )
        for label in case["analyses"]
    )
    return portable(
        dict(
            schema="pharmacophoremt.eralpha_interface_controls@1",
            preparation=case["report"],
            observations=models["observed"].metadata["interaction_collection"],
            site_counts={
                label: model.n_interaction_sites for label, model in models.items()
            },
            query=json.loads(query_path.read_text()),
            outcomes=dict(
                reference=positive,
                displaced_negative=negative,
                reversed_donor_direction=donor_negative,
                reversed_normal=normal_sign,
                orthogonal_normal_negative=angular_negative,
                nondefault_units=unit_result,
                reloaded=reloaded,
                reloaded_observed_only=rebuilt_result,
            ),
            exclusions=dict(
                n_sites=exclusions["report"]["n_sites"],
                observed_shell_group_ids=ids,
                radius=policy["exclusion_radius"],
                report=exclusions["report"],
                outcomes=exclusion_outcomes,
                collision_receptor_source_atom_index=case["report"][
                    "atom_source_indices"
                ][int(receptor_target[0])],
                collision_ligand_source_atom_index=case["report"][
                    "atom_source_indices"
                ][int(ligand_target[0])],
            ),
            persistence=dict(
                query_metadata_preserved=restored_query.metadata == query.metadata,
                preparation_history_preserved=True,
                cached_analyses_preserved=preserved_analyses,
                chemical_values_and_coordinates_preserved=True,
            ),
            prepared_input_unchanged=True,
        )
    )


def valid(run):
    """Bound acceptance to declared chemistry and independent geometric controls."""
    outcomes, excluded = run["outcomes"], run["exclusions"]["outcomes"]
    return (
        run["preparation"]["source_unchanged"]
        and run["prepared_input_unchanged"]
        and run["site_counts"] == dict(observed=6, reference=5, combined=11, curated=11)
        and {
            label: value["n_interactions"]
            for label, value in run["preparation"]["observations"].items()
        }
        == run["preparation"]["declaration"]["expected_observations"]
        and all(
            outcomes[label]["status"] == "matched" and outcomes[label]["fit_value"] == 1
            for label in (
                "reference",
                "reversed_normal",
                "nondefault_units",
                "reloaded",
                "reloaded_observed_only",
            )
        )
        and all(
            outcomes[label]["status"] == "not_matched"
            for label in (
                "displaced_negative",
                "reversed_donor_direction",
                "orthogonal_normal_negative",
            )
        )
        and outcomes["displaced_negative"]["fit_value"] == 0
        and len(outcomes["reversed_donor_direction"]["missing_essential_sites"]) == 1
        and len(outcomes["orthogonal_normal_negative"]["missing_essential_sites"]) == 1
        and run["exclusions"]["n_sites"] == 153
        and excluded["reference"]["status"] == "matched"
        and excluded["unexcluded_collision"]["status"] == "matched"
        and excluded["collision"]["status"] == "not_matched"
        and all(value["fit_value"] == 1 for value in excluded.values())
        and all(run["persistence"].values())
    )


def main(argv=None):
    import ackredit
    import molsysmt as msm
    import pyunitwizard

    import pharmacophoremt as phmt

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--artifacts",
        type=Path,
        required=True,
        help="New directory retaining native history and query artifacts",
    )
    args = parser.parse_args(argv)
    args.artifacts.mkdir(parents=True, exist_ok=False)
    packages = dict(
        pharmacophoremt=phmt, molsysmt=msm, pyunitwizard=pyunitwizard, ackredit=ackredit
    )
    before = {name: _source_record(package) for name, package in packages.items()}
    paths = [MANIFEST] + [
        ROOT / name
        for name in (
            "devtools/prepare_eralpha_interface.py",
            "devtools/validate_eralpha_interface.py",
            "devtools/prepare_eralpha_ligand.py",
            "devtools/prepare_eralpha_hydrogens.py",
            "devtools/audit_eralpha_receptor.py",
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

    def hashes():
        return {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths
        }

    inputs, runs = hashes(), []
    for enabled in (False, True):
        with ackredit.session("declared ERalpha interface"), phmt.attribution(enabled):
            with ackredit.capture(
                "prepared fragment and hypothesis controls"
            ) as capture:
                directory = args.artifacts / ("tracked" if enabled else "plain")
                run = controls(prepare_interface(), directory)
                if enabled:
                    credit_inputs()
            run["attribution"] = capture.attribution.to_dict()
        run["tracking"] = enabled
        run["valid"] = valid(run)
        science = scientific_projection(
            {
                key: value
                for key, value in run.items()
                if key not in {"tracking", "valid"}
            }
        )
        run["scientific_sha256"] = hashlib.sha256(
            json.dumps(science, sort_keys=True).encode()
        ).hexdigest()
        run["artifacts"] = {
            path.name: dict(
                path=str(path),
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                n_bytes=path.stat().st_size,
            )
            for path in directory.iterdir()
        }
        runs.append(run)
    unchanged = (
        before == {name: _source_record(package) for name, package in packages.items()}
        and inputs == hashes()
    )
    accepted = (
        unchanged
        and all(run["valid"] for run in runs)
        and runs[0]["scientific_sha256"] == runs[1]["scientific_sha256"]
    )
    report = dict(
        schema="pharmacophoremt.eralpha_interface_validation@1",
        recorded_utc=datetime.now(timezone.utc).isoformat(),
        python=platform.python_version(),
        executable=sys.executable,
        platform=platform.platform(),
        producers=before,
        inputs=inputs,
        producers_and_inputs_unchanged=unchanged,
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
        runs=runs,
        valid=accepted,
        scope="declared closed fragment and analytical controls; no full-receptor, environmental or biological acceptance",
    )
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print("PASS" if accepted else "FAIL", "prepared ERalpha interface controls")
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
