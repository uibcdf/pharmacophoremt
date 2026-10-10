"""Reusable chemical participants obtained through public MolSysMT tools."""

import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.molsysmt import capability, detached, source_frame
from pharmacophoremt._private.smonitor.exceptions import ArgumentError

CLASSICAL_FEATURES = (
    "hydrophobicity",
    "hb donor",
    "hb acceptor",
    "aromatic ring",
    "positive charge",
    "negative charge",
)
DEFINITION = "classical_atomic_formal@1"


def _groups(result, prefix="atom"):
    atoms, offsets = result[f"{prefix}_indices"], result[f"{prefix}_offsets"]
    return [
        atoms[start:stop].tolist() for start, stop in zip(offsets[:-1], offsets[1:])
    ]


@signal(tags=["modeling", "features"])
@arg_digest()
@attributed("numpy", "molsysmt", "pyunitwizard")
def get_features(
    molecular_system,
    *,
    selection="all",
    structure_index=0,
    chemical_state="reference",
    features=CLASSICAL_FEATURES,
):
    """Extract participants and their geometry from one prepared ligand frame.

    Parameters
    ----------
    molecular_system : molecular system
        Any source supported by MolSysMT, with declared chemistry and coordinates.
    selection : MolSysMT selection, default='all'
        Participants must be wholly contained in the selection.
    structure_index : int, default=0
        Local coordinate frame.
    chemical_state : str or int, default='reference'
        Chemical state resolved by MolSysMT independently of the frame.
    features : sequence of str
        Requested classical families; 'included volume' also yields heavy atoms.

    Returns
    -------
    dict
        Feature records containing local atom indices, explicit-unit centers,
        dimensionless donor directions or aromatic normals, and detached provider
        recognition/geometry evidence. Charge records retain elementary charges.

    Notes
    -----
    This versioned definition uses MolSysMT's atomic hydrophobic and donor/acceptor
    SMARTS rules, stored-aromatic-bond minimum cycle basis, and declared formal
    charge centers. Charge positions are unweighted centroids of the provider's
    geometry members. No protonation, hydrogen addition, repair, periodic imaging,
    or conformer generation occurs. Missing/ambiguous chemistry raises in MolSysMT.
    Ring membership is not a claim of equivalence to RDKit SSSR.
    Donor-pair vector arithmetic is the remaining molecular-geometry migration
    tracked in MolSysMT #375 / PharmacophoreMT #41; no local acceptor direction
    model is supplied. Receptor hypothesis projections must be explicit.

    Examples
    --------
    >>> inventory = get_features(prepared_ligand, features=['aromatic ring'])
    >>> ring_atoms = inventory['features'][0]['atom_indices']
    """
    requested = set(features)
    if not requested <= set(CLASSICAL_FEATURES) | {"included volume"}:
        raise ArgumentError(
            argument="features",
            reason="expected classical chemical families or included volume",
        )
    coordinates, indices = source_frame(
        molecular_system, selection, structure_index, chemical_state=chemical_state
    )
    common = dict(
        selection=indices,
        structure_indices=[structure_index],
        chemical_state=chemical_state,
    )
    records, recognition = [], {}

    def append(
        kind,
        atoms,
        center,
        *,
        geometry_atoms=None,
        direction=None,
        normal=None,
        charge=None,
    ):
        records.append(
            dict(
                kind=kind,
                atom_indices=[int(atom) for atom in atoms],
                geometry_atom_indices=[
                    int(atom)
                    for atom in (atoms if geometry_atoms is None else geometry_atoms)
                ],
                center=puw.quantity(np.asarray(center, dtype=float).copy(), "nm"),
                direction=None
                if direction is None
                else puw.quantity(
                    np.asarray(direction, dtype=float).copy(), "dimensionless"
                ),
                normal=None
                if normal is None
                else puw.quantity(
                    np.asarray(normal, dtype=float).copy(), "dimensionless"
                ),
                charge=charge,
            )
        )

    if "hydrophobicity" in requested:
        result = capability("physchem.get_hydrophobic_sites")(
            molecular_system, method="smarts_hydrophobic_atoms", **common
        )
        recognition["hydrophobicity"] = detached(result)
        for atom in result["hydrophobic_atom_indices"]:
            append("hydrophobicity", [atom], coordinates[atom])
    if requested & {"hb donor", "hb acceptor"}:
        result = capability("physchem.get_hbond_sites")(
            molecular_system, method="smarts_donor_acceptor", **common
        )
        recognition["hydrogen_bond"] = detached(result)
        if "hb donor" in requested:
            for donor, hydrogen in result["donor_hydrogen_pairs"]:
                direction = coordinates[hydrogen] - coordinates[donor]
                norm = np.linalg.norm(direction)
                if norm == 0:
                    raise ArgumentError(
                        argument="molecular_system",
                        reason="donor and indexed hydrogen have coincident coordinates",
                    )
                append(
                    "hb donor",
                    [donor, hydrogen],
                    coordinates[donor],
                    direction=direction / norm,
                )
        if "hb acceptor" in requested:
            for atom in result["acceptor_atom_indices"]:
                append("hb acceptor", [atom], coordinates[atom])
    if "aromatic ring" in requested:
        result = capability("physchem.get_aromatic_rings")(molecular_system, **common)
        recognition["aromatic_ring"] = detached(result)
        groups = _groups(result)
        if groups:
            plane = capability("structure.get_least_squares_plane")(
                molecular_system,
                selection=groups,
                structure_indices=[structure_index],
                pbc=False,
            )
            recognition["aromatic_geometry"] = detached(plane)
            centers = puw.get_value(plane["centers"], to_unit="nm")[0]
            normals = plane["normals"][0]
            for atoms, center, normal in zip(groups, centers, normals):
                append("aromatic ring", atoms, center, normal=normal)
    if requested & {"positive charge", "negative charge"}:
        result = capability("physchem.get_charge_centers")(molecular_system, **common)
        recognition["formal_charge"] = detached(result)
        groups, geometry_groups = _groups(result), _groups(result, "geometry_atom")
        if groups:
            centers = capability("structure.get_center")(
                molecular_system,
                selection=geometry_groups,
                structure_indices=[structure_index],
            )
            recognition["charge_geometry"] = dict(
                method="molsysmt.structure.get_center",
                weighting="uniform",
                centers=detached(centers),
            )
            centers = puw.get_value(centers, to_unit="nm")[0]
            charges = puw.get_value(result["charges"], to_unit="e")
            for atoms, geometry_atoms, center, charge in zip(
                groups, geometry_groups, centers, charges
            ):
                kind = "positive charge" if charge > 0 else "negative charge"
                if kind in requested:
                    append(
                        kind,
                        atoms,
                        center,
                        geometry_atoms=geometry_atoms,
                        charge=puw.quantity(float(charge), "e"),
                    )
    if "included volume" in requested:
        symbols = np.asarray(
            capability("get")(molecular_system, element="atom", atom_type=True)
        )
        if symbols.shape != (len(coordinates),) or any(
            not isinstance(symbol, str) or not symbol for symbol in symbols
        ):
            raise ArgumentError(
                argument="molecular_system",
                reason="heavy-atom volumes require declared elements",
            )
        for atom in indices[symbols[indices] != "H"]:
            append("included volume", [atom], coordinates[atom])
    return dict(
        definition=DEFINITION,
        features=records,
        recognition=recognition,
        selected_atom_indices=indices.tolist(),
        structure_index=int(structure_index),
        chemical_state=detached(chemical_state),
    )
