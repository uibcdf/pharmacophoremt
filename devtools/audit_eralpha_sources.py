"""Audit the separately sourced 1QKU/EST inputs for PharmacophoreMT #22.

The downloaded files are immutable inputs. Molecular access and CIF decoding use
MolSysMT; this fixture-specific report neither applies a template nor generates H.
Run from a source checkout: python devtools/audit_eralpha_sources.py
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

import molsysmt as msm
import numpy as np

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import get_features

ROOT = Path(__file__).resolve().parents[1] / "tests/data/eralpha_rcsb"


def audit():
    """Inspect the provenance and preparation gate of the acquired RCSB case."""
    manifest = json.loads((ROOT / "manifest.json").read_text())
    checksums = {}
    for name, metadata in manifest["files"].items():
        checksums[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        if checksums[name] != metadata["sha256"]:
            raise ValueError(f"Source file {name} changed; re-audit the acquired case.")
    source = msm.convert(str(ROOT / "1qku.cif"), to_form="molsysmt.MolSys")
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    before = msm.convert(
        source.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    before_text = json.dumps(before, default=lambda x: x.tolist(), sort_keys=True)
    indices = msm.select(source, selection=manifest["ligand"]["selection"])
    names = list(msm.get(source, element="atom", selection=indices, atom_name=True))
    elements = list(msm.get(source, element="atom", selection=indices, atom_type=True))
    ligand = msm.extract(source, selection=indices)
    entry = msm.convert(
        str(ROOT / "1qku.cif"), to_form="mmcif.PdbxContainers.DataContainer"
    )
    ccd = msm.convert(
        str(ROOT / "EST.cif"), to_form="mmcif.PdbxContainers.DataContainer"
    )
    revision = entry.getObj("pdbx_audit_revision_history")
    observed_revision = dict(
        zip(revision.getAttributeList(), revision.getRow(revision.getRowCount() - 1))
    )
    atoms = ccd.getObj("chem_comp_atom")
    ccd_elements = [
        atoms.getValue("type_symbol", i) for i in range(atoms.getRowCount())
    ]
    ccd_heavy_names = [
        atoms.getValue("atom_id", i)
        for i, element in enumerate(ccd_elements)
        if element != "H"
    ]
    sites = entry.getObj("atom_site")
    rows = [
        i
        for i in range(sites.getRowCount())
        if sites.getValue("label_asym_id", i) == manifest["ligand"]["label_asym_id"]
    ]
    report = {
        "schema": "pharmacophoremt.eralpha_source_audit@1",
        "molsysmt_version": msm.__version__,
        "checksums": checksums,
        "entry_id": entry.getObj("entry").getValue("id", 0),
        "observed_revision": observed_revision,
        "counts": msm.get(
            source,
            n_atoms=True,
            n_groups=True,
            n_structures=True,
            output_type="dictionary",
        ),
        "source_atom_indices": [int(index) for index in indices],
        "ligand_atom_names": names,
        "ligand_element_counts": dict(Counter(elements)),
        "ligand_n_bonds_in_loaded_graph": msm.get(ligand, n_bonds=True),
        "author_asym_ids": sorted({sites.getValue("auth_asym_id", i) for i in rows}),
        "author_residue_ids": sorted({sites.getValue("auth_seq_id", i) for i in rows}),
        "ccd_atom_count": atoms.getRowCount(),
        "ccd_bond_count": ccd.getObj("chem_comp_bond").getRowCount(),
        "ccd_element_counts": dict(Counter(ccd_elements)),
        "heavy_atom_names_agree": set(names) == set(ccd_heavy_names),
        "chemical_mapping_status": "not_validated",
        "hydrogen_generation_status": "not_performed",
        "coordinates_finite": bool(np.isfinite(coordinates).all()),
        "coordinate_unit": "nm",
    }
    try:
        get_features(ligand)
    except msm.StructuralInconsistencyError as error:
        report.update(
            recognition_status="blocked",
            diagnostic={"code": error.code, "message": str(error)},
        )
    else:
        report["recognition_status"] = "completed"
    after = msm.convert(
        source.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    report["source_unchanged"] = bool(
        np.array_equal(
            coordinates, puw.get_value(msm.get(source, coordinates=True), to_unit="nm")
        )
        and before_text
        == json.dumps(after, default=lambda x: x.tolist(), sort_keys=True)
    )
    report["files_unchanged"] = all(
        hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == checksum
        for name, checksum in checksums.items()
    )
    return report


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
