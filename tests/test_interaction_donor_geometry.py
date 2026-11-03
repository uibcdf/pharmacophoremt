"""Observed donor geometry uses provider vectors without changing recognition."""

from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.io import load_json, to_json
from pharmacophoremt.modeler import from_interactions
from phmt_test_support.absence_inputs import system


def prepared_observations(unit="nm"):
    xyz = np.array(
        [
            [0.1, 0, 0],
            [0, 0, 0],
            [0.3, 0.1, 0],
            [0.3, 0, 0],
            [0.35, 0.1, 0],
            [0.35, 0, 0],
        ]
    )
    source = system("[2H]O.C=O.C=O", xyz * (10 if unit == "angstrom" else 1), unit)
    moved = xyz @ np.array([[0.0, 1, 0], [-1, 0, 0], [0, 0, 1]]) + [2, 1, -3]
    source.structures.append(coordinates=puw.quantity([moved], "nm"))
    observed = msm.interactions.hbonds.get_hbonds(
        source,
        selection=[0, 1],
        selection_2=[2, 3, 4, 5],
        selection_mode="between",
        method="donor_acceptor_distance_angle",
        profile="smarts_donor_acceptor",
        distance_threshold="0.4 nm",
        structure_indices=[1],
        pbc=False,
    )
    data = observed.to_dict()
    records = [
        dict(
            structure_index=int(data["structure_indices"][row]),
            **observed.relation(int(index)),
            evidence=str(data["evidence"][row]),
            measurements={k: float(v[row]) for k, v in data["measurements"].items()},
        )
        for row, index in enumerate(data["relation_indices"])
    ]
    mapped = msm.Interactions.from_records(
        records,
        n_atoms=6,
        n_structures=2,
        evaluated_structure_indices=[1],
        method=observed.method,
        software=observed.software,
        measure_units=observed.measure_units,
        parameters=deepcopy(observed.parameters),
        atom_source_indices=[20, 21, 22, 23, 24, 25],
        structure_source_indices=[4, 7],
        source_n_atoms=30,
        source_n_structures=10,
        source_id="declared-geometry-control",
    )
    assert mapped.n_interactions == 2
    return source, mapped


def modern_provider():
    if not hasattr(msm.structure, "get_vectors"):
        pytest.skip("historical public provider; modern receiving requires vectors")


@pytest.mark.parametrize("unit", ["nm", "angstrom"])
def test_observed_pairs_frame_maps_profile_reuse_and_detached_persistence(
    monkeypatch, tmp_path, unit
):
    modern_provider()
    source, observed = prepared_observations(unit)
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    old = detached(observed.to_dict())
    calls, payloads = [], []
    original = msm.structure.get_vectors

    def vectors(*args, **kwargs):
        calls.append(deepcopy(kwargs))
        result = original(*args, **kwargs)
        payloads.append(result)
        return result

    def forbidden(*args, **kwargs):
        pytest.fail("cached observation conversion must not redetect chemistry")

    monkeypatch.setattr(msm.structure, "get_vectors", vectors)
    monkeypatch.setattr(msm.interactions.hbonds, "get_hbonds", forbidden)
    monkeypatch.setattr(msm.interactions.hbonds, "get_hbond_sites", forbidden)
    with puw.context(standard_units=["pm", "ps", "degrees"]):
        query = from_interactions(source, observed, [1, 0], structure_index=1)
    assert len(calls) == 1  # Two observations share one ordered donor/H pair.
    np.testing.assert_array_equal(calls[0]["selection"], [[1, 0]])
    assert calls[0]["pairs"] is True and calls[0]["pbc"] is False
    assert calls[0]["structure_indices"] == [1]
    assert query.n_interaction_sites == 1
    site = query.interaction_sites[0]
    assert site.metadata["atom_indices"] == [1, 0]
    assert site.metadata["source_atom_indices"] == [21, 20]
    assert site.metadata["structure_index"] == 1
    assert len(site.metadata["observations"]) == 2
    assert site.metadata["donor_geometry_route"] == "molsysmt.structure.get_vectors"
    np.testing.assert_allclose(
        puw.get_value(site.direction, to_unit="dimensionless"), [0, 1, 0]
    )
    assert query.metadata["source_structure_indices"] == [4, 7]
    assert query.metadata["parameters"] == detached(observed.parameters)
    geometry = deepcopy(site.metadata["donor_geometry"])
    assert geometry["atom_indices"] == [1] and geometry["atom_indices_2"] == [0]
    assert geometry["structure_indices"] == [1]
    payloads[0]["directions"][:] = 0
    payloads[0]["parameters"].clear()
    assert site.metadata["donor_geometry"] == geometry
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )
    assert detached(observed.to_dict()) == old
    path = tmp_path / "observed_donor.json"
    to_json(query, path)
    restored = load_json(path)
    assert restored.metadata == query.metadata
    assert restored.interaction_sites[0].metadata == site.metadata


def test_available_observed_vector_failure_propagates(monkeypatch):
    modern_provider()
    source, observed = prepared_observations()
    failure = RuntimeError("controlled observed-vector failure")

    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(msm.structure, "get_vectors", fail)
    with pytest.raises(RuntimeError) as caught:
        from_interactions(source, observed, [0, 1], structure_index=1)
    assert caught.value is failure


@pytest.mark.parametrize(
    "corruption",
    ["pair", "frame", "offset", "pbc", "method", "sense", "direction", "distance"],
)
def test_invalid_observed_vector_payload_is_not_reconstructed(monkeypatch, corruption):
    modern_provider()
    source, observed = prepared_observations()
    original = msm.structure.get_vectors

    def corrupt(*args, **kwargs):
        result = original(*args, **kwargs)
        if corruption == "pair":
            result["atom_indices_2"] = [5]
        elif corruption == "frame":
            result["structure_indices"] = [0]
        elif corruption == "offset":
            result["atom_offsets"] = [0, 2]
        elif corruption == "pbc":
            result["pbc"] = True
        elif corruption == "method":
            result["method"] = "directed_minimum_image"
        elif corruption == "sense":
            result["parameters"]["sense"] = "second_to_first"
        elif corruption == "direction":
            result["directions"][:] = 0
        else:
            result["distances"] = puw.quantity([[float("nan")]], "nm")
        return result

    monkeypatch.setattr(msm.structure, "get_vectors", corrupt)
    with pytest.raises(ArgumentError, match="MolSysMT donor geometry"):
        from_interactions(source, observed, [0, 1], structure_index=1)


def test_historical_observed_geometry_is_explicit_absence_only(monkeypatch):
    source, observed = prepared_observations()
    monkeypatch.delattr(msm.structure, "get_vectors", raising=False)
    query = from_interactions(source, observed, [0, 1], structure_index=1)
    site = query.interaction_sites[0]
    assert (
        site.metadata["donor_geometry_route"]
        == "legacy_cartesian_donor_arithmetic_pending_phmt41"
    )
    assert "donor_geometry" not in site.metadata
    np.testing.assert_allclose(
        puw.get_value(site.direction, to_unit="dimensionless"), [0, 1, 0]
    )


@pytest.mark.parametrize("historical", [False, True])
def test_coincident_observed_donor_has_visible_failure(monkeypatch, historical):
    if not historical:
        modern_provider()
    source, observed = prepared_observations()
    # Deliberately degenerate declared input, not a valid cached physical observation.
    xyz = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    xyz[1, 0] = xyz[1, 1]
    msm.set(source, coordinates=puw.quantity(xyz, "nm"))
    if historical:
        monkeypatch.delattr(msm.structure, "get_vectors", raising=False)
    with pytest.raises(ArgumentError, match="coincident"):
        from_interactions(source, observed, [0, 1], structure_index=1)


def test_acceptor_and_internal_observations_need_no_donor_vectors(monkeypatch):
    source, observed = prepared_observations()

    def forbidden(*args, **kwargs):
        pytest.fail("no selected donor geometry is needed")

    monkeypatch.setattr(msm.structure, "get_vectors", forbidden, raising=False)
    acceptors = from_interactions(source, observed, [2, 3, 4, 5], structure_index=1)
    assert acceptors.n_interaction_sites == 2
    assert all(
        s.shape_name == "sphere" and "donor_geometry" not in s.metadata
        for s in acceptors.interaction_sites
    )
    assert (
        from_interactions(
            source, observed, "all", structure_index=1
        ).n_interaction_sites
        == 0
    )
    empty = msm.Interactions.from_records(
        [],
        n_atoms=6,
        n_structures=2,
        evaluated_structure_indices=[1],
        method=observed.method,
        software=observed.software,
        measure_units=observed.measure_units,
        parameters=deepcopy(observed.parameters),
    )
    query = from_interactions(source, empty, [0, 1], structure_index=1)
    assert query.n_interaction_sites == 0
    assert query.metadata["evaluated_structure_indices"] == [1]
