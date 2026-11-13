"""Explicit curation controls preserve native constraints and source custody."""

import inspect
from copy import deepcopy

import molsysmt as msm
import pytest
from argdigest import describe_contract

from pharmacophoremt import Pharmacophore, io
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import GaussianKernel, Sphere
from pharmacophoremt.io.phmt import _to_dict
from pharmacophoremt.modeler import (
    copy_pharmacophore,
    edit_pharmacophore,
    extract_pharmacophore,
    get_interaction_site_indices,
)

OPERATIONS = [
    get_interaction_site_indices,
    copy_pharmacophore,
    extract_pharmacophore,
    edit_pharmacophore,
    Pharmacophore.merge,
]


def model():
    class LiveSource:
        def __deepcopy__(self, memo):
            pytest.fail("Molecular copying belongs to MolSysMT")

    result = Pharmacophore(
        name="literal 2 m", score=0.8, ref_struct=3, molecular_system=LiveSource()
    )
    result.metadata = {"original": {"values": ["literal 1 ps"]}}
    result.add_interaction_site(
        InteractionSite(Sphere("[0,0,0] nm", ".1 nm"), "hydrophobicity")
    )
    result.add_interaction_site(
        InteractionSite(GaussianKernel("[1,0,0] nm", ".1 nm"), "hb donor")
    )
    return result


def call(operation, source, options):
    if operation is Pharmacophore.merge:
        return source.merge(source, **options)
    if operation is edit_pharmacophore:
        return operation(source, weight=2, **options)
    return operation(source, **options)


@pytest.mark.parametrize("operation", OPERATIONS)
def test_explicit_control_and_defining_closed_contract(operation):
    parameter = inspect.signature(operation).parameters["skip_digestion"]
    assert parameter.kind is inspect.Parameter.KEYWORD_ONLY
    assert parameter.default is False
    owner = operation.__module__ + "." + operation.__name__
    plan = operation.digestion_plan
    assert plan.contract_caller == owner
    contract = plan.contracts.resolve(owner)
    assert contract is not None
    assert describe_contract(contract, plan.domains)["admits"] == "signature"


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("operation", OPERATIONS)
def test_default_false_true_preserve_native_output_and_independent_ownership(
    unit, operation, tmp_path, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Cached model operations must not inspect molecules")

    for name in ["get", "select", "convert", "copy", "merge", "set"]:
        monkeypatch.setattr(msm, name, forbidden)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        source = model()
        before = deepcopy(_to_dict(source))
        policy = puw.configure.report()
        snapshots = []
        for index, options in enumerate(
            [{}, {"skip_digestion": False}, {"skip_digestion": True}]
        ):
            result = call(operation, source, options)
            assert _to_dict(source) == before
            if operation is get_interaction_site_indices:
                assert result == [0, 1]
                result.clear()
                continue
            assert result.molecular_system is source.molecular_system
            snapshots.append(_to_dict(result))
            assert all(
                site is not original
                for site in result.interaction_sites
                for original in source.interaction_sites
            )
            assert result.score == (0.8 if operation is copy_pharmacophore else None)
            if operation in [extract_pharmacophore, edit_pharmacophore]:
                assert result.metadata["source_model"] == before
            path = tmp_path / f"{index}.json"
            io.to_json(result, path)
            restored = io.load_json(path)
            assert _to_dict(restored) == _to_dict(result)
            result.interaction_sites[0].features.append("aromatic ring")
            result.interaction_sites[0].shape.center += puw.quantity([1, 0, 0], "nm")
            assert _to_dict(source) == before
        if snapshots:
            assert snapshots == [snapshots[0]] * 3
        assert puw.configure.report() == policy


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("control", [None, 0, 1, "true"])
def test_nonboolean_controls_fail_before_work(operation, control):
    source = model()
    before = deepcopy(_to_dict(source))
    with pytest.raises(ArgumentError):
        call(operation, source, {"skip_digestion": control})
    assert _to_dict(source) == before


@pytest.mark.parametrize("operation", OPERATIONS)
def test_unknown_options_are_refused(operation):
    with pytest.raises(TypeError):
        call(operation, model(), {"unknown_curation_option": True})


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("indices", [[0, 0], [-1], [2], [True]])
def test_invalid_indices_remain_native_refusals_without_mutation(skip, indices):
    source = model()
    before = deepcopy(_to_dict(source))
    for operation in [get_interaction_site_indices, extract_pharmacophore]:
        with pytest.raises(ArgumentError):
            operation(source, site_indices=indices, skip_digestion=skip)
    with pytest.raises(ArgumentError):
        edit_pharmacophore(
            source, site_indices=indices, weight=2, in_place=True, skip_digestion=skip
        )
    assert _to_dict(source) == before


@pytest.mark.parametrize("skip", [False, True])
def test_empty_unknown_filter_geometry_and_alias_guards_remain_active(skip):
    source = model()
    before = deepcopy(_to_dict(source))
    options = {"skip_digestion": skip}
    assert get_interaction_site_indices(source, site_indices=[], **options) == []
    assert (
        extract_pharmacophore(source, site_indices=[], **options).n_interaction_sites
        == 0
    )
    with pytest.raises(ArgumentError):
        get_interaction_site_indices(source, feature_names="hb donro", **options)
    with pytest.raises(ArgumentError):
        edit_pharmacophore(source, site_indices=[], weight=2, **options)
    with pytest.raises(ArgumentError):
        edit_pharmacophore(source, radius=".2 nm", in_place=True, **options)
    assert _to_dict(source) == before
    source.add_interaction_site(source.interaction_sites[0])
    before = deepcopy(_to_dict(source))
    with pytest.raises(ArgumentError, match="shared site"):
        edit_pharmacophore(source, site_indices=[0], weight=2, in_place=True, **options)
    assert _to_dict(source) == before


@pytest.mark.parametrize("skip", [False, True])
def test_inherited_merge_keeps_definition_contract_and_native_frame_refusal(skip):
    class ApplicationHypothesis(Pharmacophore):
        pass

    left = ApplicationHypothesis(ref_struct=3)
    right = model()
    assert left.merge(right, skip_digestion=skip).ref_struct == 3
    right.ref_struct = 4
    with pytest.raises(ArgumentError, match="reference frames"):
        left.merge(right, skip_digestion=skip)
    with pytest.raises(ArgumentError):
        left.merge(object(), skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_outer_bypass_is_not_blindly_propagated_to_public_children(skip, monkeypatch):
    import pharmacophoremt.modeler.composition as composition
    import pharmacophoremt.modeler.curation as curation

    calls = []
    for owner, name in [
        (curation, "get_interaction_site_indices"),
        (curation, "copy_pharmacophore"),
        (composition, "compose_pharmacophores"),
    ]:
        original = getattr(owner, name)

        def observed(*args, _name=name, _original=original, **kwargs):
            calls.append((_name, kwargs.get("skip_digestion", False)))
            return _original(*args, **kwargs)

        monkeypatch.setattr(owner, name, observed)
    source = model()
    extract_pharmacophore(source, skip_digestion=skip)
    edit_pharmacophore(source, weight=2, skip_digestion=skip)
    source.merge(source, skip_digestion=skip)
    assert calls == [
        ("get_interaction_site_indices", False),
        ("copy_pharmacophore", False),
        ("get_interaction_site_indices", False),
        ("copy_pharmacophore", False),
        ("compose_pharmacophores", False),
    ]


@pytest.mark.parametrize("skip", [False, True])
def test_inconsistent_native_models_fail_in_copy_even_with_bypass(skip):
    source = model()
    source.n_interaction_sites += 1
    with pytest.raises(ArgumentError, match="consistent native model"):
        copy_pharmacophore(source, skip_digestion=skip)
