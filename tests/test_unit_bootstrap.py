"""Receive bootstrap against real fresh-process PyUnitWizard registry states."""

import subprocess
import sys

import pytest


@pytest.mark.parametrize("state", ["unloaded", "preloaded", "application-policy"])
def test_import_preserves_existing_registry_cache_and_application_units(state):
    script = r"""
import sys
import warnings
import pyunitwizard as puw

state = sys.argv[1]
assert not puw.configure.has_active_policy()
if state == "application-policy":
    puw.configure.set_default_form("pint")
    puw.configure.set_default_parser("pint")
    puw.configure.set_standard_units(["angstrom", "fs", "degrees"], provenance="application")
if state != "unloaded":
    original = puw.quantity(1, "nm", form="pint")
    registry = original._REGISTRY
    cache = puw.configure.get_pint_registry_cache()
    assert "pint" in puw.configure.report()["loaded_libraries"]
    units = puw.configure.report()["standard_units"]
else:
    assert "pint" not in puw.configure.report()["loaded_libraries"]

with warnings.catch_warnings(record=True) as observed:
    warnings.simplefilter("always", RuntimeWarning)
    import pharmacophoremt as phmt

assert puw.configure.has_active_policy()
assert not any("set_pint_registry_cache() has no effect" in str(w.message) for w in observed)
quantity = puw.quantity(2, "nm", form="pint")
assert float(puw.get_value(quantity, to_unit="angstrom")) == 20
if state != "unloaded":
    assert quantity._REGISTRY is registry
    assert original._REGISTRY is registry
    assert float(puw.get_value(original, to_unit="nm")) == 1
    assert puw.configure.get_pint_registry_cache() == cache
if state == "application-policy":
    assert puw.configure.report()["standard_units"] == units
else:
    assert "nm" in puw.configure.report()["standard_units"]
"""
    result = subprocess.run(
        [sys.executable, "-B", "-c", script, state],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
