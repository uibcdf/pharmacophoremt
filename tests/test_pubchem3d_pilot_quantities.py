"""Unit-bearing preparation evidence and absolute geometry preservation controls."""

import json
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import pyunitwizard as puw
from phmt_test_support.absence_inputs import system
from phmt_test_support.pubchem3d_receiving_pilot import (
    _inventory,
    _same_inventory,
    _write,
)


def test_inventory_json_retains_geometry_across_session_policies(tmp_path):
    coordinates_nm = np.array([[[0.0, 0.0, 0.0], [0.15, 0.0, 0.0], [0.3, 0.0, 0.0]]])
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        source = system("CCC", coordinates_nm[0] * 10, unit="angstrom")
        inventory = _inventory(source)
        # A report is an observation of this frame, independent of later edits.
        msm.set(
            source,
            coordinates=puw.quantity(coordinates_nm + 1, "nm"),
        )
        destination = tmp_path / "preparation.json"
        _write(destination, {"inventory": inventory})
    payload = json.loads(destination.read_text())["inventory"]["coordinates"]
    with puw.context(standard_units=["angstrom", "ps", "radians"]):
        restored = puw.QuantityRecord.from_dict(payload).to_quantity(
            unit="nm", dimensionality={"[L]": 1}
        )
        np.testing.assert_allclose(
            puw.get_value(restored, to_unit="nm"),
            coordinates_nm,
            rtol=0,
            atol=1e-15,
        )
    assert puw.is_quantity(inventory["coordinates"])
    assert inventory["n_atoms"] == 3
    assert inventory["n_structures"] == 1


def test_inventory_comparison_converts_units_and_uses_absolute_nm_tolerance():
    first = _inventory(system())
    second = deepcopy(first)
    values_nm = puw.get_value(first["coordinates"], to_unit="nm")
    second["coordinates"] = puw.quantity(values_nm * 10, "angstrom")
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        _same_inventory(first, second)
        within_tolerance = values_nm.copy()
        within_tolerance[0, 0, 0] += 5e-13
        second["coordinates"] = puw.quantity(within_tolerance * 10, "angstrom")
        _same_inventory(first, second)


@pytest.mark.parametrize("change", ["above_tolerance", "unit_scale", "shape"])
def test_inventory_comparison_refuses_changed_geometry(change):
    first = _inventory(system())
    second = deepcopy(first)
    values_nm = puw.get_value(first["coordinates"], to_unit="nm").copy()
    if change == "above_tolerance":
        values_nm[0, 0, 0] += 2e-12
        second["coordinates"] = puw.quantity(values_nm, "nm")
    elif change == "unit_scale":
        # The same numbers in another unit describe a different molecular frame.
        second["coordinates"] = puw.quantity(values_nm, "angstrom")
    else:
        second["coordinates"] = puw.quantity(values_nm[:, :-1], "nm")
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        with pytest.raises(ValueError, match="coordinates differ"):
            _same_inventory(first, second)
