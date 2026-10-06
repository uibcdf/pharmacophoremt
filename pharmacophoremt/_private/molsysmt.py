"""Public-provider boundaries shared by the placed-pose workflow."""

from copy import deepcopy

import molsysmt as msm
import numpy as np

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    ProviderCapabilityError,
)


def capability(path):
    provider = msm
    for name in path.split("."):
        provider = getattr(provider, name, None)
        if provider is None:
            raise ProviderCapabilityError(capability=path)
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
