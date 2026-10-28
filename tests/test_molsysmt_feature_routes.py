"""Provider-owned donor geometry preserves the existing pharmacophore definition."""

import copy

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler import from_ligand, get_features
from pharmacophoremt.screening import PoseEvaluator
from phmt_test_support.absence_inputs import system


def water(unit="nm"):
    coordinates = np.array([[0.1, 0.2, 0.2], [0, 0, 0], [0, -0.3, 0]])
    if unit == "angstrom":
        coordinates *= 10
    return system("[2H]O[3H]", coordinates, unit=unit)


def modern_provider():
    if not hasattr(msm.structure, "get_vectors"):
        pytest.skip("older public provider; modern route has a separate receiving gate")


@pytest.mark.parametrize("unit", ["nm", "angstrom"])
def test_public_vectors_supply_donor_pairs_units_frames_and_unchanged_source(
    monkeypatch, unit
):
    modern_provider()
    source = water(unit)
    second = puw.get_value(msm.get(source, coordinates=True), to_unit="nm")[0].copy()
    second[0] = [0, 0.3, 0]
    second[2] = [-0.3, 0, 0]
    source.structures.append(coordinates=puw.quantity([second], "nm"))
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    calls = []
    original = msm.structure.get_vectors

    def observed(*args, **kwargs):
        calls.append(copy.deepcopy(kwargs))
        return original(*args, **kwargs)

    monkeypatch.setattr(msm.structure, "get_vectors", observed)
    with puw.context(standard_units=["pm", "ps", "degrees"]):
        result = get_features(
            source,
            selection=[2, 1, 0],
            structure_index=1,
            features=["hb donor", "hb acceptor"],
        )
    donors = [r for r in result["features"] if r["kind"] == "hb donor"]
    assert [r["atom_indices"] for r in donors] == [[1, 0], [1, 2]]
    np.testing.assert_allclose(
        [puw.get_value(r["direction"], to_unit="dimensionless") for r in donors],
        [[0, 1, 0], [-1, 0, 0]],
        atol=1e-14,
    )
    assert len(calls) == 1
    np.testing.assert_array_equal(calls[0]["selection"], [[1, 0], [1, 2]])
    assert calls[0]["structure_indices"] == [1]
    assert calls[0]["pairs"] is True and calls[0]["pbc"] is False
    assert (
        result["recognition"]["hydrogen_bond_route"]["recognition"]
        == "molsysmt.interactions.hbonds.get_hbond_sites"
    )
    assert (
        result["recognition"]["hydrogen_bond_route"]["donor_geometry"]
        == "molsysmt.structure.get_vectors"
    )
    assert result["recognition"]["donor_geometry"]["method"] == "directed_cartesian"
    assert result["definition"] == "classical_atomic_formal@1"
    assert all(
        r["direction"] is None for r in result["features"] if r["kind"] == "hb acceptor"
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )


def test_provider_failure_propagates_and_empty_inventory_never_calls_vectors(
    monkeypatch,
):
    modern_provider()
    failure = RuntimeError("controlled molecular-provider failure")

    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(msm.structure, "get_vectors", fail)
    with pytest.raises(RuntimeError) as caught:
        get_features(water(), features=["hb donor"])
    assert caught.value is failure
    empty = get_features(system("CCC"), features=["hb donor"])
    assert empty["features"] == []
    assert empty["recognition"]["hydrogen_bond_route"]["donor_geometry"] is None
    assert "donor_geometry" not in empty["recognition"]


def test_available_recognition_failure_never_tries_historical_namespace(monkeypatch):
    modern_provider()
    failure = RuntimeError("controlled recognition-provider failure")

    def fail(*args, **kwargs):
        raise failure

    def historical(*args, **kwargs):
        pytest.fail("an available recognition tool must not be replaced after failure")

    monkeypatch.setattr(msm.interactions.hbonds, "get_hbond_sites", fail)
    monkeypatch.setattr(msm.physchem, "get_hbond_sites", historical, raising=False)
    with pytest.raises(RuntimeError) as caught:
        get_features(water(), features=["hb donor"])
    assert caught.value is failure


@pytest.mark.parametrize(
    "corruption",
    ["pairs", "frame", "offsets", "pbc", "method", "sense", "direction", "distance"],
)
def test_invalid_available_provider_results_do_not_trigger_local_reconstruction(
    monkeypatch, corruption
):
    modern_provider()
    original = msm.structure.get_vectors

    def corrupt(*args, **kwargs):
        result = original(*args, **kwargs)
        if corruption == "pairs":
            result["atom_indices_2"] = result["atom_indices_2"][::-1]
        elif corruption == "frame":
            result["structure_indices"] = [99]
        elif corruption == "offsets":
            result["atom_offsets"] = [0, 2, 2]
        elif corruption == "pbc":
            result["pbc"] = True
        elif corruption == "method":
            result["method"] = "directed_minimum_image"
        elif corruption == "sense":
            result["parameters"]["sense"] = "second_to_first"
        elif corruption == "direction":
            result["directions"][:] = 0
        else:
            result["distances"] = puw.quantity([[float("nan"), 0.3]], "nm")
        return result

    monkeypatch.setattr(msm.structure, "get_vectors", corrupt)
    with pytest.raises(ArgumentError, match="MolSysMT donor geometry"):
        get_features(water(), features=["hb donor"])


def test_coincident_donor_hydrogen_keeps_visible_failure():
    source = water()
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="nm")
    coordinates[0, 0] = coordinates[0, 1]
    msm.set(source, element="atom", coordinates=puw.quantity(coordinates, "nm"))
    with pytest.raises(ArgumentError, match="coincident"):
        get_features(source, features=["hb donor"])


def test_historical_namespace_and_geometry_are_bounded_compatibility_only(monkeypatch):
    current = getattr(msm.interactions.hbonds, "get_hbond_sites", None)
    if current is not None:
        monkeypatch.setattr(msm.physchem, "get_hbond_sites", current, raising=False)
        monkeypatch.delattr(msm.interactions.hbonds, "get_hbond_sites")
    monkeypatch.delattr(msm.structure, "get_vectors", raising=False)
    source = water()
    result = get_features(source, features=["hb donor"])
    assert result["recognition"]["hydrogen_bond_route"] == {
        "recognition": "molsysmt.physchem.get_hbond_sites",
        "donor_geometry": "legacy_cartesian_donor_arithmetic_pending_phmt41",
    }
    assert "donor_geometry" not in result["recognition"]
    np.testing.assert_allclose(
        puw.get_value(result["features"][0]["direction"], to_unit="dimensionless"),
        [1 / 3, 2 / 3, 2 / 3],
    )
    query = from_ligand(source, features=["hb donor"])
    assert PoseEvaluator(query).evaluate(source)["status"] == "matched"
