"""Independent public controls retain native scientific ownership and child checks."""

import importlib
import inspect

import molsysmt as msm
import numpy as np
import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt import Pharmacophore
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.screening import PoseEvaluator, VirtualScreening
from tests.test_nested_facade_contracts import query
from tests.test_pose_evaluation import model_from_source, system

POSE = importlib.import_module("pharmacophoremt.screening.pose_evaluation")
NAMES = ["__init__", "evaluate", "run"]


@pytest.mark.parametrize("name", NAMES)
def test_explicit_keyword_only_control_keeps_definition_contract(name):
    operation = getattr(PoseEvaluator, name)
    parameter = inspect.signature(operation).parameters["skip_digestion"]
    assert (
        parameter.kind is inspect.Parameter.KEYWORD_ONLY and parameter.default is False
    )
    child = type("ApplicationPose", (PoseEvaluator,), {"__module__": "consumer.poses"})
    plan = getattr(child, name).digestion_plan
    assert plan.contract_caller == operation.__module__ + "." + name
    contract = plan.contracts.resolve(plan.contract_caller)
    description = describe_contract(contract, plan.domains)
    if name == "run":
        assert "skip_digestion" not in description["admitted_domains"][0]["members"]
    else:
        assert description["admits"] == "signature"


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_copy_source_or_input(name, flag, monkeypatch):
    q = query()
    evaluator = PoseEvaluator(q)

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid operation control must refuse before scientific work")

    class Borrowed:
        def __iter__(self):
            forbidden()

    monkeypatch.setattr(POSE, "deepcopy", forbidden)
    monkeypatch.setattr(POSE, "source_frame", forbidden)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        if name == "__init__":
            PoseEvaluator(q, skip_digestion=flag)
        elif name == "evaluate":
            evaluator.evaluate(object(), skip_digestion=flag)
        else:
            evaluator.run(Borrowed(), skip_digestion=flag)


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
def test_actual_public_bypass_is_literal(name, flag, monkeypatch):
    q = query()
    evaluator = PoseEvaluator(q)
    seen = []
    original = _contracts._boolean

    def observe(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    def source_failure(*args, **kwargs):
        raise RuntimeError("source boundary entered")

    monkeypatch.setattr(_contracts, "_boolean", observe)
    monkeypatch.setattr(POSE, "source_frame", source_failure)
    if name == "__init__":
        PoseEvaluator(q, skip_digestion=flag)
    elif name == "evaluate":
        with pytest.raises(PoseEvaluationError) as caught:
            evaluator.evaluate(object(), skip_digestion=flag)
        assert isinstance(caught.value.__cause__, RuntimeError)
    else:
        assert evaluator.run([], skip_digestion=flag) == []
    assert len(seen) == (0 if flag is True else 1)
    if flag is not True:
        assert seen[0] is flag


@pytest.mark.parametrize(
    "options", [{}, {"skip_digestion": False}, {"skip_digestion": True}]
)
def test_batch_keeps_real_child_default_admission_and_failure_denominator(
    options, monkeypatch
):
    evaluator = PoseEvaluator(query())
    seen = []
    original = _contracts._boolean

    def observe(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    def source_failure(*args, **kwargs):
        raise RuntimeError("source failed")

    monkeypatch.setattr(_contracts, "_boolean", observe)
    monkeypatch.setattr(POSE, "source_frame", source_failure)
    source = object()
    rows = evaluator.run(iter([source, source]), on_error="record", **options)
    assert [row["input_index"] for row in rows] == [0, 1]
    assert [row["pose_id"] for row in rows] == [0, 1]
    assert all(row["status"] == "failed" and row["fit_value"] is None for row in rows)
    assert all(row["error"]["cause"] == "RuntimeError" for row in rows)
    assert seen == ([False] if options.get("skip_digestion") is not True else []) + [
        False,
        False,
    ]


@pytest.mark.parametrize("skip", [False, True])
def test_batch_keeps_legacy_evaluate_override_without_forwarding_its_control(skip):
    calls = []

    class ApplicationPose(PoseEvaluator):
        def evaluate(self, molecular_system, *, selection, pose_id):
            calls.append((molecular_system, selection, pose_id))
            return {"status": "not_matched", "fit_value": 0, "pose_id": pose_id}

    source = object()
    selection = [0, 2]
    rows = ApplicationPose(query()).run(
        [source, source], selection=selection, skip_digestion=skip
    )
    assert [row["input_index"] for row in rows] == [0, 1]
    assert [pose for _, _, pose in calls] == [0, 1]
    assert all(s is source and sel is selection for s, sel, _ in calls)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "kind",
    ["wrong_model", "empty_model", "bare_length", "angle", "nan_fit", "bool_fit"],
)
def test_constructor_scientific_invariants_remain_active(skip, kind):
    q = query()
    options = {}
    if kind == "wrong_model":
        q = object()
    elif kind == "empty_model":
        q = Pharmacophore()
    elif kind == "bare_length":
        options["point_tolerance"] = 0.1
    elif kind == "angle":
        options["direction_tolerance"] = "181 degrees"
    elif kind == "nan_fit":
        options["min_fit_value"] = float("nan")
    else:
        options["min_fit_value"] = True
    with pytest.raises(ArgumentError):
        PoseEvaluator(q, skip_digestion=skip, **options)


@pytest.mark.parametrize("frame", [-1, True, "1"])
def test_bypass_keeps_native_frame_guard_and_cause_before_provider_access(
    frame, monkeypatch
):
    evaluator = PoseEvaluator(query())

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid frame cannot reach the molecular provider")

    monkeypatch.setattr(msm, "get", forbidden)
    with pytest.raises(PoseEvaluationError) as caught:
        evaluator.evaluate(object(), structure_index=frame, skip_digestion=True)
    assert isinstance(caught.value.__cause__, ArgumentError)
    assert caught.value.extra["stage"] == "source"


@pytest.mark.parametrize("skip", [False, True])
def test_batch_policy_and_pose_identity_guards_survive_bypass(skip):
    evaluator = PoseEvaluator(query())
    with pytest.raises(ArgumentError, match="on_error"):
        evaluator.run([], on_error="ignore", skip_digestion=skip)
    with pytest.raises(ArgumentError, match="batch pose IDs"):
        evaluator.run([], pose_id="caller-owned", skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_facade_constructor_does_not_bypass_native_constructor(skip, monkeypatch):
    q = query()
    seen = []
    original = _contracts._boolean

    def observe(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    monkeypatch.setattr(_contracts, "_boolean", observe)
    VirtualScreening(q, screening_method="placed", skip_digestion=skip)
    assert seen == ([False] if skip is False else []) + [False]


def test_forwarded_option_domains_exclude_operation_local_control():
    from pharmacophoremt._private.arg_digestion.native_screening import (
        _evaluation_options,
    )
    from pharmacophoremt._private.arg_digestion.screening_facade import _options

    assert "skip_digestion" not in _evaluation_options(
        "pose_evaluation", "PoseEvaluator"
    )
    assert "skip_digestion" not in _options(PoseEvaluator)


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_real_placed_positive_negative_failure_parity_and_source_custody(unit):
    with puw.context(standard_units=[unit, "ps", "radians"]):
        source = system()
        q, _ = model_from_source(source)
        coords = puw.get_value(msm.get(source, coordinates=True), to_unit="nm")[
            0
        ].copy()
        negative = system(coordinates=coords + 2)
        expected = None
        for options in ({}, {"skip_digestion": False}, {"skip_digestion": True}):
            evaluator = PoseEvaluator(q, **options)
            with phmt.attribution():
                positive = evaluator.evaluate(
                    source, selection=[0, 1, 2], pose_id="fixed", **options
                )
            assert positive["attribution"]["status"] == "captured"
            assert positive["status"] == "matched" and positive["fit_value"] == 1
            assert positive["criteria"]["essential"] == "all"
            assert positive["criteria"]["assignment"] == "one_to_one"
            tolerance = puw.QuantityRecord.from_dict(
                positive["criteria"]["point_tolerance"]
            )
            assert tolerance.field == "point_tolerance"
            quantity = tolerance.to_quantity(unit="nm", dimensionality={"[L]": 1})
            assert float(puw.get_value(quantity, to_unit="nm")) == pytest.approx(0.1)
            observed = {
                key: positive[key]
                for key in (
                    "status",
                    "fit_value",
                    "assignments",
                    "selected_atom_indices",
                    "criteria",
                    "pose_id",
                )
            }
            if expected is None:
                expected = observed
            else:
                assert observed == expected
            rows = evaluator.run(
                iter([source, negative, "invalid source", source]),
                selection=[0, 1, 2],
                on_error="record",
                **options,
            )
            assert [row["input_index"] for row in rows] == [0, 1, 2, 3]
            assert [row["pose_id"] for row in rows] == [0, 1, 2, 3]
            assert [row["status"] for row in rows] == [
                "matched",
                "not_matched",
                "failed",
                "matched",
            ]
            assert [row["fit_value"] for row in rows] == [1, 0, None, 1]
        np.testing.assert_array_equal(
            puw.get_value(msm.get(source, coordinates=True), to_unit="nm")[0], coords
        )
