"""Cached inspection and ordered comparison retain explicit scientific scope."""

import inspect
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
from argdigest import describe_contract

from pharmacophoremt import Pharmacophore, io
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Cylinder, Point, Sphere
from pharmacophoremt.io.phmt import _to_dict

NAMES = ["get_distance_matrix", "to_dataframe", "similarity"]
COLUMNS = ["index", "features", "shape", "center", "radius"]


def model(xs=(0, 1), *, feature="hydrophobicity", kind="point"):
    result = Pharmacophore(name="cached 2 m", score=0.8, ref_struct=0)
    result.metadata = {"original": {"values": ["literal 1 ps"]}}
    for x in xs:
        center = puw.quantity([x, 0, 0], "nm")
        shape = Point(center) if kind == "point" else Sphere(center, ".1 nm")
        result.add_interaction_site(InteractionSite(shape, feature))
    return result


def call(source, name, options):
    args = [source] if name == "similarity" else []
    return getattr(source, name)(*args, **options)


@pytest.mark.parametrize("name", NAMES)
def test_explicit_control_and_inherited_defining_signature_contract(name):
    operation = getattr(Pharmacophore, name)
    control = inspect.signature(operation).parameters["skip_digestion"]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY and control.default is False
    owner = operation.__module__ + "." + operation.__name__
    plan = operation.digestion_plan
    assert plan.contract_caller == owner
    assert (
        describe_contract(plan.contracts.resolve(owner), plan.domains)["admits"]
        == "signature"
    )

    class ApplicationHypothesis(Pharmacophore):
        pass

    result = call(ApplicationHypothesis(), name, {"skip_digestion": False})
    if name == "similarity":
        assert result == 0


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_default_false_true_keep_analytical_distance_score_and_table_units(
    unit, monkeypatch, tmp_path
):
    def forbidden(*args, **kwargs):
        pytest.fail("Cached inspection must not inspect molecules")

    for name in ["get", "select", "convert", "copy", "merge", "set"]:
        monkeypatch.setattr(msm, name, forbidden)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        source = model()
        source.interaction_sites[1].shape = Sphere("[.3,.4,0] nm", ".1 nm")
        before = deepcopy(_to_dict(source))
        policy = puw.configure.report()
        for control in [{}, {"skip_digestion": False}, {"skip_digestion": True}]:
            matrix = source.get_distance_matrix(**control)
            np.testing.assert_allclose(
                puw.get_value(matrix, to_unit="nm"),
                [[0, 0.5], [0.5, 0]],
                atol=1e-14,
                rtol=0,
            )
            matrix[0, 1] = puw.quantity(9, "nm")
            frame = source.to_dataframe(**control)
            assert list(frame.columns) == COLUMNS
            assert frame["index"].tolist() == [0, 1]
            assert frame["shape"].tolist() == ["point", "sphere"]
            assert frame.loc[0, "radius"] is None
            for index, site in enumerate(source.interaction_sites):
                assert frame.loc[index, "features"] is site.features
                assert frame.loc[index, "center"] is site.center
            frame.loc[0, "shape"] = "table-only replacement"
            assert source.similarity(source, tolerance_nm=0, **control) == 1
            assert _to_dict(source) == before
        path = tmp_path / "query.json"
        io.to_json(source, path)
        restored = io.load_json(path)
        np.testing.assert_allclose(
            puw.get_value(restored.get_distance_matrix(), to_unit="nm"),
            [[0, 0.5], [0.5, 0]],
            atol=1e-14,
            rtol=0,
        )
        assert restored.metadata == source.metadata
        assert source.similarity(restored, tolerance_nm=1e-12) == 1
        assert puw.configure.report() == policy


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("count", [0, 1])
def test_empty_and_singleton_outputs_keep_schema_and_shape(skip, count):
    source = model(xs=range(count))
    assert list(source.to_dataframe(skip_digestion=skip).columns) == COLUMNS
    assert source.get_distance_matrix(skip_digestion=skip).shape == (count, count)
    assert source.similarity(source, skip_digestion=skip) == count


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("control", [None, 0, 1, "true"])
def test_nonboolean_controls_are_refused(name, control):
    with pytest.raises(ArgumentError):
        call(model(), name, {"skip_digestion": control})


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("skip", [False, True])
def test_unknown_options_and_inconsistent_model_are_refused(name, skip):
    source = model()
    with pytest.raises(TypeError):
        call(source, name, {"unknown_inspection_option": 1, "skip_digestion": skip})
    source.n_interaction_sites = 0
    with pytest.raises(ArgumentError, match="consistent native model"):
        call(source, name, {"skip_digestion": skip})


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "tolerance", [-1, np.nan, np.inf, True, None, ".1", [0.1], 10**1000]
)
def test_invalid_numeric_nan_or_infinite_tolerance_is_never_a_scientific_score(
    skip, tolerance
):
    source = model()
    with pytest.raises(ArgumentError):
        source.similarity(source, tolerance_nm=tolerance, skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_invalid_other_model_is_refused_including_bypass(skip):
    source = model()
    with pytest.raises(ArgumentError):
        source.similarity(object(), skip_digestion=skip)


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize(
    "tolerance,expected", [(0, 0), (np.float32(0.25), 1), (np.int64(1), 1)]
)
def test_numeric_threshold_keeps_its_fixed_nm_meaning(unit, tolerance, expected):
    with puw.context(standard_units=[unit, "ps", "radians"]):
        assert model([0]).similarity(model([0.2]), tolerance) == expected


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "center", [[0, 0, 0], "[0,0,0] ps", "[nan,0,0] nm", "[0,0] nm"]
)
def test_invalid_present_center_cannot_turn_into_a_nan_or_hidden_nonmatch(skip, center):
    source = model()
    source.interaction_sites[0].shape.position = center
    with pytest.raises(ArgumentError):
        source.get_distance_matrix(skip_digestion=skip)
    with pytest.raises(ArgumentError):
        source.similarity(model(), skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_centerless_shapes_remain_unmatched_without_an_invented_center(skip):
    source = model(xs=[])
    source.add_interaction_site(
        InteractionSite(Cylinder("[0,0,0] nm", "[1,0,0] nm", ".1 nm"), "hydrophobicity")
    )
    assert source.similarity(source, skip_digestion=skip) == 0
    frame = source.to_dataframe(skip_digestion=skip)
    assert frame.loc[0, "center"] is None
    np.testing.assert_array_equal(
        puw.get_value(source.get_distance_matrix(skip_digestion=skip), to_unit="nm"),
        [[0]],
    )
    source.add_interaction_site(InteractionSite(Point("[2,0,0] nm"), "hydrophobicity"))
    with pytest.raises(ArgumentError, match="center"):
        source.get_distance_matrix(skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_legacy_greedy_order_dependence_stays_visible_under_205(skip):
    left, right = model([0.1, 0]), model([0, 0.3])
    assert left.similarity(right, 0.21, skip_digestion=skip) == 0.5
    assert right.similarity(left, 0.21, skip_digestion=skip) == 1
    alternatives = model([0], feature=["hb donor", "hb acceptor"])
    assert (
        alternatives.similarity(
            model([0], feature="hb acceptor"), 0, skip_digestion=skip
        )
        == 1
    )
    repeated = model([0, 0])
    assert repeated.similarity(model([0]), 0, skip_digestion=skip) == pytest.approx(
        2 / 3
    )
    assert (
        model([0], feature="hb donor").similarity(model([0]), skip_digestion=skip) == 0
    )


@pytest.mark.parametrize("skip", [False, True])
def test_distance_internal_bypass_uses_only_established_native_inputs(
    skip, monkeypatch
):
    source = model()
    calls = []
    original = source.get

    def observed(*args, **kwargs):
        calls.append(kwargs)
        return original(*args, **kwargs)

    monkeypatch.setattr(source, "get", observed)
    source.get_distance_matrix(skip_digestion=skip)
    assert calls == [{"get_center": True, "skip_digestion": True}]
