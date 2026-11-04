"""Real ArgDigest contracts for native shapes and application subclasses."""

import numpy as np
import pytest
from argdigest import UnknownArgumentError, describe_contract

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.interaction_site import (
    CationPiDisk,
    HBDonorSphereAndVector,
    HydrophobicPoint,
    HydrophobicSphere,
)
from pharmacophoremt.interaction_site.shape import Disk, Point, Sphere, SphereAndVector

CASES = [
    pytest.param(Point, {"position": "[10,20,30] angstrom"}, id="point"),
    pytest.param(
        Sphere, {"center": "[10,20,30] angstrom", "radius": "2 angstrom"}, id="sphere"
    ),
    pytest.param(
        SphereAndVector,
        {
            "center": "[10,20,30] angstrom",
            "radius": "2 angstrom",
            "direction": [0, 4, 0],
        },
        id="directed",
    ),
    pytest.param(
        Disk,
        {"center": "[10,20,30] angstrom", "normal": [0, 0, 4], "radius": "2 angstrom"},
        id="disk",
    ),
]


def application_shape(shape):
    """An inherited mixin implementation in a different application's module."""
    mixin = type("PresentationMixin", (), {"__module__": "consumer.presentation"})
    base = type("CustomShape", (mixin, shape), {"__module__": "consumer.geometry"})
    return type("DeepShape", (base,), {"__module__": "consumer.geometry"})


@pytest.mark.parametrize("shape,arguments", CASES)
def test_native_shape_contract_is_declared_and_follows_inheritance(shape, arguments):
    inherited = application_shape(shape)
    plan = inherited.__init__.digestion_plan
    owner = f"{shape.__module__}.__init__"
    assert plan.contract_caller == owner
    contract = plan.contracts.resolve(owner)
    assert contract is not None  # Do not silently fall back to the signature default.
    description = describe_contract(contract, plan.domains)
    assert description["caller"] == owner
    assert description["admits"] == "signature"
    assert description["admitted_domains"] == []
    with pytest.raises(UnknownArgumentError) as refusal:
        inherited(**arguments, raduis="2 angstrom")
    assert "consumer.geometry.DeepShape.__init__" in str(refusal.value)


@pytest.mark.parametrize("shape,arguments", CASES)
@pytest.mark.parametrize("length_unit", ["nm", "angstrom"])
@pytest.mark.parametrize("positional", [False, True])
def test_inherited_geometry_preserves_calls_and_application_policy(
    shape, arguments, length_unit, positional
):
    inherited = application_shape(shape)
    with puw.context(standard_units=[length_unit, "ps", "degrees"]):
        policy = puw.configure.report()
        result = (
            inherited(*arguments.values()) if positional else inherited(**arguments)
        )
        location = result.position if shape is Point else result.center
        np.testing.assert_allclose(puw.get_value(location, to_unit="nm"), [1, 2, 3])
        if shape is not Point:
            assert float(puw.get_value(result.radius, to_unit="nm")) == pytest.approx(
                0.2
            )
        if shape is SphereAndVector:
            np.testing.assert_allclose(
                puw.get_value(result.direction, to_unit="dimensionless"), [0, 1, 0]
            )
        if shape is Disk:
            np.testing.assert_allclose(
                puw.get_value(result.normal, to_unit="dimensionless"), [0, 0, 1]
            )
        after = puw.configure.report()
        for key in ["default_form", "default_parser", "standard_units", "provenance"]:
            assert after[key] == policy[key]


@pytest.mark.parametrize("shape,arguments", CASES)
@pytest.mark.parametrize("failure", ["typo", "alias", "missing", "duplicate"])
def test_closed_geometry_signatures_reject_wrong_calls(shape, arguments, failure):
    arguments = arguments.copy()
    first = next(iter(arguments))
    inherited = application_shape(shape)
    if failure in {"typo", "alias"}:
        # center/position are distinct shape parameters, never implicit aliases.
        extra = (
            "raduis"
            if failure == "typo"
            else ("center" if shape is Point else "position")
        )
        with pytest.raises(UnknownArgumentError):
            inherited(**arguments, **{extra: "1 nm"})
    elif failure == "missing":
        del arguments[first]
        with pytest.raises(TypeError):
            inherited(**arguments)
    else:
        with pytest.raises(TypeError):
            inherited(arguments[first], **arguments)


@pytest.mark.parametrize("shape,arguments", CASES)
def test_inherited_geometry_keeps_host_value_diagnostics_and_skip(shape, arguments):
    arguments = arguments.copy()
    location = "position" if shape is Point else "center"
    arguments[location] = [1, 2, 3]
    inherited = application_shape(shape)
    with pytest.raises(ArgumentError) as caught:
        inherited(**arguments)
    assert caught.value.code == "PHMT-E102"
    assert caught.value.__cause__ is not None
    assert location in str(caught.value)
    # The existing explicit bypass admits bare coordinates interpreted by the body.
    result = inherited(**arguments, skip_digestion=True)
    np.testing.assert_allclose(
        puw.get_value(getattr(result, location), to_unit="nm"), [1, 2, 3]
    )


@pytest.mark.parametrize(
    "wrapper,arguments",
    [
        pytest.param(HydrophobicPoint, CASES[0].values[1], id="point"),
        pytest.param(HydrophobicSphere, CASES[1].values[1], id="sphere"),
        pytest.param(HBDonorSphereAndVector, CASES[2].values[1], id="directed"),
        pytest.param(CationPiDisk, CASES[3].values[1], id="disk"),
    ],
)
def test_feature_composition_preserves_geometry_contract(wrapper, arguments):
    site = wrapper(**arguments)
    location = site.shape.position if "position" in arguments else site.center
    np.testing.assert_allclose(puw.get_value(location, to_unit="nm"), [1, 2, 3])
    assert site.n_features == 1
