"""Fixture-specific evidence for #22, using only public molecular provider APIs.

Run from a source checkout: python devtools/audit_eralpha.py
This is an input audit, not a general chemical-readiness tool or a scored benchmark.
MolSysMT owns preparation/readiness and template application (#217/#218/#298).
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

import molsysmt as msm
import numpy as np

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import get_features

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests/data/eralpha_audit.json"


def _state(system):
    payload = msm.convert(
        system.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    return payload["states"][payload["reference_chemical_state_index"]]


def _observation(system):
    state = _state(system)
    observation = msm.get(system, n_atoms=True, n_bonds=True, output_type="dictionary")
    observation.update(
        connectivity_completeness=state["connectivity_completeness"],
        component_completeness=state["component_completeness"],
        component_evidence=state["component_evidence"],
        bond_orders=msm.get(system, element="bond", bond_order=True),
        formal_charges=msm.get(system, element="atom", formal_charge=True),
    )
    try:
        inventory = get_features(system)
    except msm.StructuralInconsistencyError as error:
        # Scientific input rejection is evidence, never a score of zero.
        observation.update(
            recognition_status="blocked",
            diagnostic={"code": error.code, "message": str(error)},
        )
    else:
        observation.update(
            recognition_status="completed", n_features=len(inventory["features"])
        )
    return observation


def audit():
    """Inspect the unchanged, checksum-qualified ERalpha regression snapshot."""
    manifest = json.loads(MANIFEST.read_text())
    fixture = ROOT / manifest["fixture"]
    checksum = hashlib.sha256(fixture.read_bytes()).hexdigest()
    if checksum != manifest["sha256"]:
        raise ValueError(
            "ERalpha fixture changed; re-audit its identity and selections."
        )
    source = msm.convert(str(fixture), to_form="molsysmt.MolSys")
    original_coordinates = puw.get_value(
        msm.get(source, coordinates=True), to_unit="nm"
    ).copy()
    original_state = msm.convert(
        source.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    original_state_text = json.dumps(
        original_state, default=lambda x: x.tolist(), sort_keys=True
    )
    indices = msm.select(source, selection=manifest["ligand"]["selection"])
    names = msm.get(source, element="atom", selection=indices, atom_name=True)
    elements = msm.get(source, element="atom", selection=indices, atom_type=True)
    report = {
        "schema": "pharmacophoremt.eralpha_input_audit@1",
        "sha256": checksum,
        "molsysmt_version": msm.__version__,
        "provenance_status": manifest["provenance_status"],
        "counts": msm.get(
            source,
            n_atoms=True,
            n_groups=True,
            n_molecules=True,
            n_structures=True,
            output_type="dictionary",
        ),
        "automatic_small_molecule_selection_count": len(
            msm.select(source, selection='molecule_type == "small molecule"')
        ),
        "ligand_source_atom_indices": [int(index) for index in indices],
        "ligand_atom_names": list(names),
        "ligand_element_counts": dict(Counter(elements)),
        "ligand_group_names": list(
            msm.get(source, element="atom", selection=indices, group_name=True)
        ),
        "coordinate_unit": "nm",
        "coordinates_finite": bool(np.isfinite(original_coordinates).all()),
        "provider_issue": manifest["provider_issue"],
        "parts": {},
    }
    for key in ("ligand", "protein"):
        part = msm.extract(source, selection=manifest[key]["selection"])
        raw = _observation(part)
        # Public conversion is probed, not accepted as chemical preparation.
        text = msm.convert(part, to_form="string:pdb_text")
        converted = msm.convert(
            msm.convert(text, to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
        )
        roundtrip = _observation(converted)
        report["parts"][key] = {
            "native_pdb": raw,
            "pdb_text_rdkit_roundtrip": roundtrip,
        }
    current_state = msm.convert(
        source.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    report["source_unchanged"] = bool(
        np.array_equal(
            original_coordinates,
            puw.get_value(msm.get(source, coordinates=True), to_unit="nm"),
        )
        and original_state_text
        == json.dumps(current_state, default=lambda x: x.tolist(), sort_keys=True)
    )
    return report


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
