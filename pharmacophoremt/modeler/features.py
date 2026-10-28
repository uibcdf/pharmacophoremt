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


def _donor_geometry(molecular_system, pairs, structure_index):
    """Receive Cartesian unit directions; never repair a provider failure locally."""
    result = capability("structure.get_vectors")(
        molecular_system,
        selection=pairs,
        pairs=True,
        structure_indices=[structure_index],
        pbc=False,
        output_type="dictionary",
    )
    directions = np.asarray(result["directions"], dtype=float)
    offsets = np.arange(len(pairs) + 1)
    if (
        directions.shape != (1, len(pairs), 3)
        or not np.array_equal(result["atom_indices"], pairs[:, 0])
        or not np.array_equal(result["atom_indices_2"], pairs[:, 1])
        or not np.array_equal(result["atom_offsets"], offsets)
        or not np.array_equal(result["atom_offsets_2"], offsets)
        or not np.array_equal(result["structure_indices"], [structure_index])
        or not np.array_equal(result["structure_indices_2"], [structure_index])
        or not result["pairs"]
        or result["pbc"]
        or result["method"] != "directed_cartesian"
        or result["parameters"]["sense"] != "first_to_second"
    ):
        raise ArgumentError(
            argument="MolSysMT donor geometry",
            reason="provider directions do not retain the requested pairs/frame/Cartesian convention",
        )
    distances = puw.get_value(result["distances"], to_unit="nm")
    if (
        np.shape(distances) != (1, len(pairs))
        or not np.isfinite(distances).all()
        or np.any(distances < 0)
    ):
        raise ArgumentError(
            argument="MolSysMT donor geometry",
            reason="expected finite nonnegative distances for the requested donor pairs",
        )
    if np.any(distances == 0):
        raise ArgumentError(
            argument="molecular_system",
            reason="donor and indexed hydrogen have coincident coordinates",
        )
    if not np.isfinite(directions).all() or not np.allclose(
        np.linalg.norm(directions, axis=-1), 1.0, rtol=0, atol=1e-12
    ):
        raise ArgumentError(
            argument="MolSysMT donor geometry",
            reason="expected finite unit directions from the molecular provider",
        )
    return directions[0], detached(result)


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
    Donor-pair directions use public MolSysMT Cartesian vectors when available.
    The older qualified provider route retains its bounded historical arithmetic
    under #41/#375 until the public provider minimum can migrate. The selected
    route is recorded; a failing available provider is never replaced locally.
    No acceptor direction model is supplied. Receptor projections are explicit.

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
        path = "interactions.hbonds.get_hbond_sites"
        recognition_tool = capability(path, required=False)
        if recognition_tool is None:
            path = "physchem.get_hbond_sites"
            recognition_tool = capability(path)
        result = recognition_tool(
            molecular_system, method="smarts_donor_acceptor", **common
        )
        recognition["hydrogen_bond"] = detached(result)
        recognition["hydrogen_bond_route"] = {"recognition": f"molsysmt.{path}"}
        if "hb donor" in requested:
            pairs = np.asarray(result["donor_hydrogen_pairs"], dtype=np.int64)
            provider_vectors = (
                capability("structure.get_vectors", required=False)
                if len(pairs)
                else None
            )
            recognition["hydrogen_bond_route"]["donor_geometry"] = (
                None
                if not len(pairs)
                else "molsysmt.structure.get_vectors"
                if provider_vectors is not None
                else "legacy_cartesian_donor_arithmetic_pending_phmt41"
            )
            if len(pairs) and provider_vectors is not None:
                directions, geometry = _donor_geometry(
                    molecular_system, pairs, structure_index
                )
                recognition["donor_geometry"] = geometry
            else:
                # Existing public 0.23.0 / pinned-CI compatibility only (#41).
                # No acceptor, periodic or other new molecular kernel belongs here.
                directions = []
                for donor, hydrogen in pairs:
                    direction = coordinates[hydrogen] - coordinates[donor]
                    norm = np.linalg.norm(direction)
                    if norm == 0:
                        raise ArgumentError(
                            argument="molecular_system",
                            reason="donor and indexed hydrogen have coincident coordinates",
                        )
                    directions.append(direction / norm)
            for (donor, hydrogen), direction in zip(pairs, directions):
                append(
                    "hb donor",
                    [donor, hydrogen],
                    coordinates[donor],
                    direction=direction,
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
