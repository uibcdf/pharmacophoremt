"""Explicit pair controls retain scientific identity, units and completed work."""

import importlib
import inspect
import json
import math
from copy import deepcopy

import ackredit
import molsysmt as msm
import numpy as np
import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler import get_features
from pharmacophoremt.screening import evaluate_feature_correspondence
from phmt_test_support.absence_inputs import inventory
from tests.test_seeded_scoring import ionic_case

GEOMETRY = importlib.import_module("pharmacophoremt.screening.feature_geometry")


def value(record, unit):
    return puw.get_value(
        puw.QuantityRecord.from_dict(record).to_quantity(), to_unit=unit
    )


def features():
    return inventory([[0, 0, 0], [1, 0, 0]])


def test_explicit_control_and_closed_definition_owned_public_export():
    assert (
        phmt.screening.evaluate_feature_correspondence
        is GEOMETRY.evaluate_feature_correspondence
    )
    control = inspect.signature(evaluate_feature_correspondence).parameters[
        "skip_digestion"
    ]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY and control.default is False
    plan = evaluate_feature_correspondence.digestion_plan
    assert plan.contract_owner == "definition"
    assert (
        plan.contract_caller == GEOMETRY.__name__ + ".evaluate_feature_correspondence"
    )
    assert (
        describe_contract(plan.contracts.resolve(plan.contract_caller), plan.domains)[
            "admits"
        ]
        == "signature"
    )


@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_native_geometry(flag, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid controls must refuse before native pair geometry")

    monkeypatch.setattr(GEOMETRY, "_records", forbidden)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        evaluate_feature_correspondence(features(), features(), [], skip_digestion=flag)


@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
def test_actual_literal_bypass_and_numpy_control_behavior(flag, monkeypatch):
    seen = []
    original = _contracts._boolean

    def boolean(obj, argument):
        if argument == "skip_digestion":
            seen.append(obj)
        return original(obj, argument)

    monkeypatch.setattr(_contracts, "_boolean", boolean)
    result = evaluate_feature_correspondence(
        features(), features(), np.array([[1, 1], [0, 0]]), skip_digestion=flag
    )
    assert [row["pair"] for row in result["pair_tests"]] == [[1, 1], [0, 0]]
    assert result["complete"] and result["all_pairs_valid"]
    assert len(seen) == (0 if flag is True else 1)
    if flag is not True:
        assert seen[0] is flag


@pytest.mark.parametrize("skip", [False, True])
def test_unknown_keyword_is_closed_before_native_geometry(skip, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Unknown keywords cannot enter native geometry")

    monkeypatch.setattr(GEOMETRY, "_records", forbidden)
    with pytest.raises(TypeError):
        evaluate_feature_correspondence(
            features(), features(), [], skip_digestion=skip, distance_tol=".1 nm"
        )


@pytest.mark.parametrize("skip", [False, True])
def test_pair_argument_remains_required(skip):
    with pytest.raises(TypeError):
        evaluate_feature_correspondence(features(), features(), skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "pairs",
    [
        [[-1, 0]],
        [[0, -1]],
        [[0, 0], [0, 1]],
        [[0, 0], [1, 0]],
        [[True, False]],
        [[0.0, 0.0]],
        [[0, 0, 0]],
        np.array([[2**64 - 1, 0]], dtype=np.uint64),
        np.array([[0, 2**63]], dtype=np.uint64),
    ],
)
def test_native_pair_contract_refuses_before_inventory_geometry(
    skip, pairs, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid pair identity must refuse before inventory geometry")

    monkeypatch.setattr(GEOMETRY, "_records", forbidden)
    with pytest.raises(ArgumentError, match="feature_pairs"):
        evaluate_feature_correspondence(
            features(), features(), pairs, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize(
    "argument, amount, unit",
    [
        ("distance_tolerance", 0, "nm"),
        ("distance_tolerance", -0.1, "nm"),
        ("distance_tolerance", float("nan"), "nm"),
        ("distance_tolerance", float("inf"), "nm"),
        ("direction_tolerance", -1, "degrees"),
        ("direction_tolerance", 181, "degrees"),
        ("direction_tolerance", float("nan"), "degrees"),
        ("direction_tolerance", float("inf"), "degrees"),
    ],
)
def test_native_physical_tolerance_guards_precede_even_empty_geometry(
    skip, empty, argument, amount, unit, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid physical criteria must refuse before native geometry")

    monkeypatch.setattr(GEOMETRY, "_records", forbidden)
    pairs = np.empty((0, 2), dtype=np.int64) if empty else np.array([[0, 0]])
    with pytest.raises(ArgumentError, match=argument):
        evaluate_feature_correspondence(
            features(),
            features(),
            pairs,
            skip_digestion=skip,
            **{argument: puw.quantity(amount, unit)},
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("axis", [0, 1])
def test_inventory_range_guard_remains_native(skip, axis):
    pairs = np.array([[0, 0]], dtype=np.int64)
    pairs[0, axis] = 2**63 - 1
    with pytest.raises(ArgumentError, match="indices outside inventories"):
        evaluate_feature_correspondence(
            features(), features(), pairs, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "kind, field", [("hb donor", "direction"), ("aromatic ring", "normal")]
)
def test_required_orientation_geometry_remains_native_even_for_empty_pairs(
    skip, kind, field
):
    source = inventory([[0, 0, 0]], [kind])
    with pytest.raises(ArgumentError, match="invalid " + field + " geometry"):
        evaluate_feature_correspondence(
            source, source, np.empty((0, 2), dtype=np.int64), skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
def test_independent_scalar_oracle_retains_order_boundaries_and_orientation_meaning(
    skip,
):
    reference = inventory(
        [[0, 0, 0], [0, 1, 0], [0, 0, 1]],
        ["hb donor", "aromatic ring", "positive charge"],
        directions=[[1, 0, 0], None, None],
        normals=[None, [0, 0, 1], None],
    )
    candidate = inventory(
        [[0.2, 0, 0], [0, 1, 0], [0, 0, 1]],
        ["hb donor", "aromatic ring", "negative charge"],
        directions=[[math.sqrt(3) / 2, 0.5, 0], None, None],
        normals=[None, [0, 0, -1], None],
    )
    pairs = np.array([[2, 2], [0, 0], [1, 1]], dtype=np.int64)
    report = evaluate_feature_correspondence(
        reference,
        candidate,
        pairs,
        distance_tolerance=puw.quantity(0.2, "nm"),
        direction_tolerance=puw.quantity(30, "degrees"),
        skip_digestion=skip,
    )
    assert [t["pair"] for t in report["pair_tests"]] == pairs.tolist()
    assert (
        report["invalid_kind_pairs"] == report["invalid_orientation_pairs"] == [[2, 2]]
    )
    assert report["invalid_position_pairs"] == []
    assert value(report["position_rmsd"], "nm") == pytest.approx(math.sqrt(0.04 / 3))
    assert value(report["maximum_center_deviation"], "nm") == pytest.approx(0.2)
    assert value(
        report["pair_tests"][1]["orientation_deviation"], "degrees"
    ) == pytest.approx(30)
    assert value(
        report["pair_tests"][2]["orientation_deviation"], "degrees"
    ) == pytest.approx(0)
    assert report["pair_tests"][0]["orientation_deviation"] is None
    assert report["complete"] and not report["all_pairs_valid"]
    json.dumps(report, allow_nan=False)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("angle, valid", [(0, False), (180, True)])
def test_donor_reversal_and_closed_angular_endpoints(skip, angle, valid):
    first = inventory([[0, 0, 0]], ["hb donor"], directions=[[1, 0, 0]])
    second = inventory([[0, 0, 0]], ["hb donor"], directions=[[-1, 0, 0]])
    result = evaluate_feature_correspondence(
        first,
        second,
        np.array([[0, 0]]),
        direction_tolerance=puw.quantity(angle, "degrees"),
        skip_digestion=skip,
    )
    assert result["all_orientations_valid"] is valid
    assert value(
        result["pair_tests"][0]["orientation_deviation"], "degrees"
    ) == pytest.approx(180)


@pytest.mark.parametrize("skip", [False, True])
def test_empty_evaluation_remains_completed_without_measurements_or_search(skip):
    result = evaluate_feature_correspondence(
        inventory([]),
        inventory([]),
        np.empty((0, 2), dtype=np.int64),
        skip_digestion=skip,
    )
    assert result["complete"] and result["all_pairs_valid"]
    assert result["pair_tests"] == result["invalid_pairs"] == []
    assert result["position_rmsd"] is result["maximum_center_deviation"] is None
    assert (
        result["criteria"]["completion_scope"] == "supplied_pairs_in_shared_frame_only"
    )


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_actual_cached_units_custody_detachment_and_new_only_attribution(
    unit, monkeypatch
):
    with puw.context(standard_units=[unit, "ps", "radians"]):
        source, _ = ionic_case()
        cached = get_features(source, features=["positive charge"])
        before = deepcopy(cached)
        coordinates = puw.get_value(
            msm.get(source, coordinates=True), to_unit="nm"
        ).copy()
        pairs = np.array([[2, 2], [0, 0], [1, 1]], dtype=np.int64)

        def forbidden(*args, **kwargs):
            pytest.fail("Cached pair evaluation cannot read or fit molecules")

        with monkeypatch.context() as patch:
            for name in ("get", "select", "convert", "copy"):
                patch.setattr(msm, name, forbidden)
            patch.setattr(msm.structure, "least_rmsd_fit", forbidden)
            with ackredit.session("cached pair geometry") as application:
                captures = []
                for options in (
                    {},
                    {"skip_digestion": False},
                    {"skip_digestion": True},
                ):
                    with (
                        ackredit.capture("one pair evaluation") as capture,
                        phmt.attribution(),
                    ):
                        result = evaluate_feature_correspondence(
                            cached, cached, pairs, **options
                        )
                    assert result["all_pairs_valid"] and result["complete"]
                    assert value(result["position_rmsd"], "nm") == 0
                    assert [t["pair"] for t in result["pair_tests"]] == pairs.tolist()
                    assert result["attribution"]["status"] == "captured"
                    captures.append(capture.attribution.to_dict())
                    result["pair_tests"][0]["pair"][0] = 99
                with (
                    ackredit.capture("empty completed evaluation") as empty_capture,
                    phmt.attribution(),
                ):
                    empty = evaluate_feature_correspondence(
                        cached,
                        cached,
                        np.empty((0, 2), dtype=np.int64),
                        skip_digestion=True,
                    )
                assert (
                    empty["complete"] and empty["attribution"]["status"] == "captured"
                )
                captures.append(empty_capture.attribution.to_dict())
                assert ackredit.current_session() is application
        for capture in captures:
            payload = json.dumps(capture)
            assert (
                "pharmacophoremt.screening.feature_geometry.evaluate_feature_correspondence"
                in payload
            )
            assert "pharmacophoremt.modeler.features.get_features" not in payload
            assert "molsysmt.structure.least_rmsd_fit" not in payload
        assert pairs.tolist() == [[2, 2], [0, 0], [1, 1]]
        assert cached.keys() == before.keys()
        assert cached["selected_atom_indices"] == before["selected_atom_indices"]
        for record, original in zip(cached["features"], before["features"]):
            assert (
                record["kind"] == original["kind"]
                and record["atom_indices"] == original["atom_indices"]
            )
            np.testing.assert_array_equal(
                puw.get_value(record["center"], to_unit="nm"),
                puw.get_value(original["center"], to_unit="nm"),
            )
            assert puw.get_unit(record["center"]) == puw.get_unit(original["center"])
        np.testing.assert_array_equal(
            puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), coordinates
        )
