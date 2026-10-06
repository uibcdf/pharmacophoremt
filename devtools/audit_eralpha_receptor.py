"""Audit the observed 1QKU receptor without inferring or repairing chemistry.

Run: python -m devtools.audit_eralpha_receptor --output FILE
All molecular selections, chemistry assessments and detector calls use MolSysMT.
This case-specific client does not implement a general readiness calculation.
"""

import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

from devtools.benchmark_rigid_consensus import _source_record
from devtools.prepare_eralpha_ligand import ROOT, SOURCES, credit_inputs, load_manifest
from devtools.prepared_ccd_ligands import state_payload
from devtools.validate_eralpha_template import portable
from devtools.validate_prepared_ccd_ligands import scientific_projection

RECEPTOR_SELECTION = 'molecule_type == "protein" and chain_id == "A"'
SHELL_RADII = ("0.4 nm", "0.5 nm", "0.6 nm")


def _fingerprint(source):
    """Compare the provider's source domains before and after this audit."""
    import molsysmt as msm

    from pharmacophoremt import pyunitwizard as puw

    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="nm")
    identity = msm.get(
        source,
        element="atom",
        atom_id=True,
        atom_name=True,
        atom_type=True,
        group_index=True,
        group_id=True,
        group_name=True,
        chain_id=True,
        output_type="dictionary",
    )
    state = json.dumps(state_payload(source), sort_keys=True, allow_nan=False)
    return dict(
        coordinates_sha256=hashlib.sha256(coordinates.tobytes()).hexdigest(),
        coordinates_shape=list(coordinates.shape),
        chemical_state_sha256=hashlib.sha256(state.encode()).hexdigest(),
        identity_sha256=hashlib.sha256(
            json.dumps(portable(identity), sort_keys=True).encode()
        ).hexdigest(),
    )


def audit(source=None):
    """Retain bounded residue coverage and genuine detector failures separately.

    Indices in all reports refer to the unchanged complete asymmetric unit.
    Shells include whole residues having an observed atom within the declared
    nonperiodic distance of label-chain D EST. They are spatial scopes, not
    inferred interaction sets or bioassemblies. No water or other protein copy
    is silently included in the chosen chain-A receptor.
    """
    import molsysmt as msm

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.modeler import get_features

    manifest = load_manifest()
    if source is None:
        source = msm.convert(str(SOURCES / "1qku.cif"), to_form="molsysmt.MolSys")
    before = _fingerprint(source)
    ligand_selection = manifest["source_selection"]
    ligand_indices = list(map(int, msm.select(source, selection=ligand_selection)))
    if ligand_indices != manifest["source_atom_indices"]:
        raise ValueError("Observed EST correspondence changed; review source identity")
    receptor = msm.build.get_residue_chemical_coverage(
        source, selection=RECEPTOR_SELECTION, structure_indices=0
    )
    entry = msm.convert(
        str(SOURCES / "1qku.cif"), to_form="mmcif.PdbxContainers.DataContainer"
    )
    sites = entry.getObj("atom_site")
    author_chains = {}
    for row in range(sites.getRowCount()):
        label = sites.getValue("label_asym_id", row)
        author_chains.setdefault(label, set()).add(sites.getValue("auth_asym_id", row))
    shells = {}
    for radius in SHELL_RADII:
        selection = (
            f"({RECEPTOR_SELECTION}) within {radius} without pbc "
            f"of ({ligand_selection})"
        )
        groups = msm.select(source, selection=selection, element="group")
        shells[radius] = dict(
            spatial_selection=selection,
            radius=puw.QuantityRecord.from_quantity(
                puw.quantity(float(radius.split()[0]), "nm")
            ).to_dict(),
            coverage=msm.build.get_residue_chemical_coverage(
                source, selection=groups, structure_indices=0
            ),
        )

    calls = {
        "receptor_features": lambda: get_features(
            msm.extract(source, selection=RECEPTOR_SELECTION)
        ),
        "hydrophobic_observations": lambda: (
            msm.interactions.hydrophobic.get_hydrophobic_interactions(
                source,
                selection=RECEPTOR_SELECTION,
                selection_2=ligand_selection,
                selection_mode="between",
                structure_indices=[0],
                pbc=False,
                method="atom_pair_distance",
                profile="smarts_hydrophobic_atoms",
                distance_threshold="0.45 nm",
            )
        ),
        "hbond_observations": lambda: msm.interactions.hbonds.get_hbonds(
            source,
            selection=RECEPTOR_SELECTION,
            selection_2=ligand_selection,
            selection_mode="between",
            structure_indices=[0],
            pbc=False,
            method="prolif",
            distance_threshold="0.35 nm",
            angle_threshold="130 degrees",
        ),
    }
    attempts = {}
    for name, calculate in calls.items():
        try:
            result = calculate()
        except msm.StructuralInconsistencyError as error:
            attempts[name] = dict(
                status="blocked",
                diagnostic=dict(
                    code=error.code, type=type(error).__name__, message=str(error)
                ),
                n_observations=None,
            )
        else:
            attempts[name] = dict(
                status="completed",
                result=result
                if name == "receptor_features"
                else msm.convert(result, to_form="molsysmt.InteractionsDict").to_dict(),
            )
    raw_ligand_readiness = msm.physchem.get_chemical_readiness(
        source, selection=ligand_indices, structure_indices=0
    )
    after = _fingerprint(source)
    return dict(
        schema="pharmacophoremt.eralpha_receptor_audit@1",
        source=dict(
            path="tests/data/eralpha_rcsb/1qku.cif",
            uri=manifest["source_uri"],
            sha256=manifest["source_sha256"],
            revision=manifest["source_revision"],
            counts=msm.get(
                source,
                n_atoms=True,
                n_groups=True,
                n_structures=True,
                output_type="dictionary",
            ),
            chains=msm.get(
                source,
                element="chain",
                chain_id=True,
                n_atoms=True,
                output_type="dictionary",
            ),
            deposited_label_to_author_chains={
                label: sorted(authors) for label, authors in author_chains.items()
            },
        ),
        receptor_selection=RECEPTOR_SELECTION,
        ligand_selection=ligand_selection,
        ligand_source_atom_indices=ligand_indices,
        receptor_coverage=receptor,
        shells=shells,
        attempts=attempts,
        requested_detector_parameters={
            "hydrophobic_distance": puw.QuantityRecord.from_quantity(
                puw.quantity(0.45, "nm")
            ).to_dict(),
            "hbond_distance": puw.QuantityRecord.from_quantity(
                puw.quantity(0.35, "nm")
            ).to_dict(),
            "hbond_angle": puw.QuantityRecord.from_quantity(
                puw.quantity(130, "degrees")
            ).to_dict(),
        },
        raw_ligand_readiness=raw_ligand_readiness,
        policy=dict(
            chemical_state="reference",
            structure_index=0,
            pbc=False,
            hydrogen_bond_method="prolif",
            hydrogen_policy="indexed_atoms_only",
            hydrophobic_method="atom_pair_distance",
            hydrophobic_profile="smarts_hydrophobic_atoms",
            ligand_preparation="raw_observed_no_hydrogens",
            generated_ligand_reinserted=False,
            preparation="not_performed",
            protonation="not_selected",
            biological_validation="not_performed",
            bioassembly="not_constructed",
            sequence_completeness="not_assessed",
            waters="excluded",
            assumption_of_complete_connectivity=False,
        ),
        before=before,
        after=after,
        source_unchanged=before == after,
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    import ackredit
    import molsysmt as msm
    import pyunitwizard

    import pharmacophoremt as phmt

    producers = dict(
        pharmacophoremt=phmt, molsysmt=msm, pyunitwizard=pyunitwizard, ackredit=ackredit
    )
    before = {name: _source_record(module) for name, module in producers.items()}
    paths = [
        ROOT / name
        for name in (
            "devtools/audit_eralpha_receptor.py",
            "devtools/prepare_eralpha_ligand.py",
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

    inputs = hashes()
    runs = []
    for enabled in (False, True):
        with (
            ackredit.session("observed 1QKU receptor audit"),
            phmt.attribution(enabled),
        ):
            with ackredit.capture("receptor coverage and calculation gates") as capture:
                report = audit()
                if enabled:
                    # The observed entry is the only scientific dataset consumed.
                    credit_inputs(roles=("observed",))
            runs.append(
                dict(
                    host_tracking=enabled,
                    report=portable(report),
                    attribution=capture.attribution.to_dict(),
                )
            )
    after = {name: _source_record(module) for name, module in producers.items()}
    projection = [scientific_projection(run["report"]) for run in runs]
    output = dict(
        schema="pharmacophoremt.eralpha_receptor_audit_run@1",
        created_utc=datetime.now(timezone.utc).isoformat(),
        python=dict(version=platform.python_version(), executable=sys.executable),
        environment=before,
        inputs=inputs,
        runs=runs,
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
        producer_sources_unchanged=before == after,
        input_files_unchanged=inputs == hashes(),
        tracking_independent_science=projection[0] == projection[1],
        timing="not_measured",
        memory="not_measured",
    )
    args.output.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")
    if not (
        output["producer_sources_unchanged"]
        and output["input_files_unchanged"]
        and output["tracking_independent_science"]
        and all(run["report"]["source_unchanged"] for run in runs)
    ):
        raise RuntimeError("Source preservation or attribution independence failed")
    print(
        "PASS: source-preserving receptor audit; no preparation or biological acceptance"
    )


if __name__ == "__main__":
    main()
