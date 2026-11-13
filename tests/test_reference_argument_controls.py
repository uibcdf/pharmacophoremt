"""Reference-query controls preserve native semantics and source custody."""

import inspect
from copy import deepcopy
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler import from_feature_inventory, from_ligand, get_features

INPUT = Path(__file__).parent / "data/binding_interface_handoff/source.h5msm"


@pytest.fixture(scope="module")
def prepared():
    source = msm.h5msm.read(str(INPUT))
    return source, get_features(source, selection=[2], features=["positive charge"])


@pytest.mark.parametrize("operation", [from_feature_inventory, from_ligand])
def test_control_is_explicit_optional_keyword_only(operation):
    parameter = inspect.signature(operation).parameters["skip_digestion"]
    assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
    assert parameter.default is False


@pytest.mark.parametrize("operation", [from_feature_inventory, from_ligand])
def test_closed_contract_is_owned_by_the_defining_operation(operation):
    owner = "pharmacophoremt.modeler.reference_ligand." + operation.__name__
    plan = operation.digestion_plan
    assert plan.contract_caller == owner
    contract = plan.contracts.resolve(owner)
    assert contract is not None
    description = describe_contract(contract, plan.domains)
    assert description["caller"] == owner
    assert description["admits"] == "signature"
    assert description["admitted_domains"] == []


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_guided_and_inventory_queries_preserve_source_evidence_under_all_controls(
    prepared, unit, tmp_path
):
    source, inventory = prepared
    original = deepcopy(detached(inventory))
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = puw.configure.report()
        # A fresh guided extraction records its current unit policy, while the
        # retained inventory preserves its original sealed quantities.
        expected_guided = detached(
            get_features(source, selection=[2], features=["positive charge"])
        )
        radius = puw.standardize(puw.quantity(0.02, "nm"))
        queries = []
        for index, options in enumerate(
            ({}, {"skip_digestion": False}, {"skip_digestion": True})
        ):
            retained = from_feature_inventory(inventory, radius=radius, **options)
            guided = from_ligand(
                source,
                selection=[2],
                features=["positive charge"],
                radius=radius,
                **options,
            )
            assert retained.n_interaction_sites == guided.n_interaction_sites == 1
            for query in (retained, guided):
                site = query.interaction_sites[0]
                assert site.feature_name == "positive charge"
                assert site.weight == 1 and site.essential
                assert site.metadata["atom_indices"] == [2]
                np.testing.assert_allclose(
                    puw.get_value(site.center, to_unit="nm"), [0, 0.25, 0], atol=1e-12
                )
                assert puw.get_value(site.radius, to_unit="nm") == pytest.approx(0.02)
            assert guided.molecular_system is source
            assert detached(guided.metadata["source_inventory"]) == expected_guided
            path = tmp_path / (str(index) + ".json")
            phmt.io.to_json(retained, str(path))
            restored = phmt.io.load_json(str(path))
            assert restored.metadata == retained.metadata
            assert (
                restored.interaction_sites[0].metadata
                == retained.interaction_sites[0].metadata
            )
            assert (
                restored.interaction_sites[0].essential
                and restored.interaction_sites[0].weight == 1
            )
            queries.append(detached(retained.metadata))
        assert queries == [queries[0]] * 3
        assert puw.configure.report() == policy
    assert detached(inventory) == original
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), coordinates
    )


@pytest.mark.parametrize("skip", [False, True])
def test_inventory_construction_calls_no_molecular_tool(prepared, monkeypatch, skip):
    _, inventory = prepared

    def forbidden(*args, **kwargs):
        pytest.fail("retained inventory construction accessed molecular science")

    import pharmacophoremt.modeler.reference_ligand as owner

    for name in ("get", "select", "convert"):
        monkeypatch.setattr(msm, name, forbidden)
    monkeypatch.setattr(msm.physchem, "get_charge_centers", forbidden)
    monkeypatch.setattr(owner, "get_features", forbidden)
    query = from_feature_inventory(inventory, skip_digestion=skip)
    assert query.n_interaction_sites == 1


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "mutation",
    ["definition", "participants", "frame", "state", "center", "orientation", "empty"],
)
def test_native_semantics_refuse_invalid_inventory_even_under_bypass(
    prepared, skip, mutation
):
    _, original = prepared
    inventory = deepcopy(original)
    if mutation == "definition":
        inventory["definition"] = "unrecognized@999"
    elif mutation == "participants":
        inventory["features"][0]["atom_indices"] = [999]
    elif mutation == "frame":
        inventory["structure_index"] = -1
    elif mutation == "state":
        inventory["chemical_state"] = -1
    elif mutation == "center":
        inventory["features"][0]["center"] = puw.quantity([0, 0.25, 0], "ps")
    elif mutation == "orientation":
        inventory["features"][0]["normal"] = puw.quantity([0, 0, 1], "dimensionless")
    else:
        inventory["features"] = []
    before = detached(inventory)
    with pytest.raises(ArgumentError):
        from_feature_inventory(inventory, skip_digestion=skip)
    assert detached(inventory) == before


@pytest.mark.parametrize("operation", ["inventory", "ligand"])
@pytest.mark.parametrize("control", [None, 0, 1, "true"])
def test_nonboolean_control_is_refused(prepared, operation, control):
    source, inventory = prepared
    function, first = (
        (from_ligand, source)
        if operation == "ligand"
        else (from_feature_inventory, inventory)
    )
    with pytest.raises(ArgumentError):
        function(first, skip_digestion=control)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("operation", ["inventory", "ligand"])
def test_unknown_keywords_fail_before_molecular_access(
    prepared, monkeypatch, skip, operation
):
    source, inventory = prepared

    def forbidden(*args, **kwargs):
        pytest.fail("invalid call reached molecular science")

    import pharmacophoremt.modeler.reference_ligand as owner

    monkeypatch.setattr(owner, "get_features", forbidden)
    function, first = (
        (from_ligand, source)
        if operation == "ligand"
        else (from_feature_inventory, inventory)
    )
    with pytest.raises(TypeError):
        function(first, raduis=".02 nm", skip_digestion=skip)


def test_bypass_is_not_forwarded_to_nested_public_operations(prepared, monkeypatch):
    source, _ = prepared
    import pharmacophoremt.modeler.reference_ligand as owner

    extract, construct = owner.get_features, owner.from_feature_inventory
    calls = []

    def observed_extract(*args, **kwargs):
        calls.append(("extract", dict(kwargs)))
        return extract(*args, **kwargs)

    def observed_construct(*args, **kwargs):
        calls.append(("construct", dict(kwargs)))
        return construct(*args, **kwargs)

    monkeypatch.setattr(owner, "get_features", observed_extract)
    monkeypatch.setattr(owner, "from_feature_inventory", observed_construct)
    query = from_ligand(
        source, selection=[2], features="positive charge", skip_digestion=True
    )
    assert query.n_interaction_sites == 1
    assert [name for name, _ in calls] == ["extract", "construct"]
    assert all("skip_digestion" not in options for _, options in calls)


@pytest.mark.parametrize("skip", [False, True])
def test_guided_empty_requested_family_still_refuses(prepared, skip):
    source, _ = prepared
    with pytest.raises(ArgumentError, match="no requested chemical participants"):
        from_ligand(
            source, selection=[2], features=["aromatic ring"], skip_digestion=skip
        )
