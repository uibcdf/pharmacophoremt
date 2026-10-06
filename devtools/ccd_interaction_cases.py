"""Checksum-qualified complete CCD components in explicitly designed placements.

This is a fixture client, not a molecular preparation or placement algorithm.
All molecular operations use existing public MolSysMT tools. Coordinates remain
CCD ideal geometries under rigid motion, not deposited complex or energy evidence.
"""

import hashlib
from collections import Counter

import molsysmt as msm
import numpy as np

from devtools.interaction_collection_cases import observe
from devtools.prepared_ccd_ligands import DIRECTORY, prepare_case, state_payload
from devtools.validate_aromatic_interactions import _fingerprint
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached

PLACEMENTS = ("ring_offset", "donor_contact")


def build_case(case_id, placement="ring_offset"):
    """Load one frozen CCD source, rigidly place a copy and merge through MolSysMT."""
    if case_id not in {"EST", "DES"} or placement not in PLACEMENTS:
        raise ValueError("choose a declared CCD identity and controlled placement")
    prepared = prepare_case(case_id)
    ligand = prepared["molecular_system"]
    before = _fingerprint(ligand)
    feature_kind = "aromatic ring" if placement == "ring_offset" else "hb donor"
    chosen = next(
        record
        for record in prepared["inventory"]["features"]
        if record["kind"] == feature_kind
    )
    axis_field = "normal" if placement == "ring_offset" else "direction"
    axis = puw.get_value(chosen[axis_field], to_unit="dimensionless")
    distance = 0.35 if placement == "ring_offset" else 0.28
    translation = puw.quantity(distance * axis, "nm")
    partner = msm.structure.translate(ligand, translation=translation, in_place=False)
    source = msm.merge([ligand, partner], keep_ids=True)
    n_atoms = int(msm.get(ligand, n_atoms=True))
    ligand_indices, partner_indices = (
        list(range(n_atoms)),
        list(range(n_atoms, 2 * n_atoms)),
    )
    selections = dict(ligand=ligand_indices, partner=partner_indices)
    # Observe provider projection of each declared component, rather than rebuilding
    # molecular membership or chemical-state payloads in the consumer.
    projected = {
        role: msm.extract(source, selection=indices)
        for role, indices in selections.items()
    }
    chemistry = state_payload(ligand)
    original = puw.get_value(msm.get(ligand, coordinates=True), to_unit="nm")
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="nm")
    source_record = prepared["report"]["source"]
    path = DIRECTORY / source_record["file"]
    report = dict(
        schema="pharmacophoremt.ccd_interaction_fixture@1",
        case_id=case_id,
        placement=placement,
        preparation=prepared["report"],
        source=source_record,
        n_atoms_per_component=n_atoms,
        source_atom_correspondence=[
            dict(
                role=role,
                local_atom_indices=list(range(n_atoms)),
                merged_atom_indices=indices,
            )
            for role, indices in selections.items()
        ],
        placement_policy=dict(
            kind="caller_declared_rigid_copy",
            feature_selection="first_in_shared_inventory",
            feature_kind=feature_kind,
            feature_atom_indices=chosen["atom_indices"],
            axis_field=axis_field,
            axis=detached(chosen[axis_field]),
            translation=detached(translation),
            internal_coordinates="unchanged",
            optimization=False,
            protein_receptor=False,
        ),
        component_states={
            role: state_payload(system) for role, system in projected.items()
        },
        component_chemistry_preserved=all(
            state_payload(system) == chemistry for system in projected.values()
        ),
        component_atom_identity_preserved=all(
            list(msm.get(system, element="atom", atom_id=True))
            == list(msm.get(ligand, element="atom", atom_id=True))
            and list(msm.get(system, element="atom", atom_type=True))
            == list(msm.get(ligand, element="atom", atom_type=True))
            for system in projected.values()
        ),
        component_counts={
            role: msm.get(system, n_atoms=True, n_bonds=True, output_type="dictionary")
            for role, system in projected.items()
        },
        merged_counts=msm.get(
            source,
            n_atoms=True,
            n_bonds=True,
            n_structures=True,
            output_type="dictionary",
        ),
        merged_state=state_payload(source),
        merged_formal_charges=detached(
            msm.get(source, element="atom", formal_charge=True)
        ),
        element_counts=dict(Counter(msm.get(source, element="atom", atom_type=True))),
        ligand_coordinates_preserved=bool(
            np.array_equal(coordinates[:, ligand_indices, :], original)
        ),
        partner_translation_preserved=bool(
            np.allclose(
                coordinates[:, partner_indices, :],
                original + distance * axis,
                rtol=0,
                atol=1e-15,
            )
        ),
        prepared_source_before=before,
        prepared_source_after=_fingerprint(ligand),
        input_bytes_unchanged=hashlib.sha256(path.read_bytes()).hexdigest()
        == source_record["sha256"],
        scope="complete_real_chemical_components_in_designed_placements_not_biological_complex",
    )
    return dict(
        source=source, ligand=ligand_indices, partner=partner_indices, report=report
    )


def observe_case(case):
    """Use the existing named public-detector recipe with no duplicate empty probe."""
    return observe(case["source"], case["ligand"], case["partner"], include_empty=False)
