"""Public-provider boundaries shared by the placed-pose workflow."""

from copy import deepcopy

import molsysmt as msm
import numpy as np

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    ProviderCapabilityError,
)


def capability(path, *, required=True):
    provider = msm
    for name in path.split("."):
        provider = getattr(provider, name, None)
        if provider is None:
            if required:
                raise ProviderCapabilityError(capability=path)
            return None
    return provider


def source_frame(
    molecular_system, selection, structure_index, *, chemical_state="reference"
):
    """Obtain one complete coordinate frame and source selection from MolSysMT."""
    if (
        isinstance(structure_index, (bool, np.bool_))
        or not isinstance(structure_index, (int, np.integer))
        or structure_index < 0
    ):
        raise ArgumentError(
            argument="structure_index", reason="expected a nonnegative integer"
        )
    coordinates = msm.get(
        molecular_system,
        element="atom",
        coordinates=True,
        structure_indices=[int(structure_index)],
    )
    values = np.asarray(puw.get_value(coordinates, to_unit="nm"), dtype=float)
    if (
        values.ndim != 3
        or values.shape[0] != 1
        or values.shape[2] != 3
        or not np.isfinite(values).all()
    ):
        raise ArgumentError(
            argument="molecular_system", reason="expected one finite coordinate frame"
        )
    indices = np.asarray(
        msm.select(
            molecular_system,
            selection=selection,
            structure_indices=[int(structure_index)],
            chemical_state=chemical_state,
        ),
        dtype=np.int64,
    )
    if indices.ndim != 1 or not indices.size:
        raise ArgumentError(
            argument="selection", reason="expected a nonempty atom selection"
        )
    return values[0], indices


def detached(value):
    """Detach provenance, retaining literal strings and sealing quantity objects."""
    if isinstance(value, str):
        return str(value)  # Normalize numpy.str_ without interpreting literal text.
    if puw.is_quantity(value):
        values = np.asarray(puw.get_value(value, to_unit=puw.get_unit(value)))
        encoding = "json" if np.isfinite(values).all() else "base64"
        return puw.QuantityRecord.from_quantity(value).to_dict(encoding=encoding)
    if isinstance(value, dict):
        return {key: detached(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [detached(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return deepcopy(value)


def _provider_donor_geometry(molecular_system, pairs, structure_index):
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


def donor_directions(molecular_system, pairs, structure_index, coordinates):
    """Share provider receiving; arithmetic is bounded historical absence only.

    Coordinates are the already received nonperiodic nm frame. No recognition
    is repeated: callers retain their own chemical profile and ordered pairs.
    The only local arithmetic is the existing #41 exception for old public
    providers genuinely lacking vectors (owners LMMV/dprada, review 2026-11-11).
    An available provider's error or invalid output is never replaced locally.
    """
    if not len(pairs):
        return np.empty((0, 3)), None, None
    if capability("structure.get_vectors", required=False) is not None:
        directions, geometry = _provider_donor_geometry(
            molecular_system, pairs, structure_index
        )
        return directions, "molsysmt.structure.get_vectors", geometry
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
    return (
        np.asarray(directions),
        "legacy_cartesian_donor_arithmetic_pending_phmt41",
        None,
    )
