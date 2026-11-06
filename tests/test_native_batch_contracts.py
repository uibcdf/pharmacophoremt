"""Batch option admission is independent of batch length and molecular work."""

import warnings
from inspect import Parameter, signature

import pytest
from argdigest import UnknownArgumentError, describe_contract

from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.screening import (
    ConformerScreening,
    PoseEvaluator,
    RigidPoseSearch,
    VirtualScreening,
)
from tests.test_nested_facade_contracts import query

TOOLS = [PoseEvaluator, RigidPoseSearch, ConformerScreening]


def tool(cls):
    return cls(query())


@pytest.mark.parametrize("cls", TOOLS)
@pytest.mark.parametrize("option", ["typo_option", "evaluation_options", "kwargs"])
@pytest.mark.parametrize("empty", [True, False])
def test_unknown_option_fails_before_input_consumption(cls, option, empty):
    class Inputs:
        consumed = 0

        def __iter__(self):
            self.consumed += 1
            return iter([] if empty else [object()])

    inputs = Inputs()
    with warnings.catch_warnings(record=True) as emitted:
        with pytest.raises(UnknownArgumentError, match=option):
            tool(cls).run(inputs, on_error="record", **{option: True})
    assert inputs.consumed == 0
    assert emitted == []


@pytest.mark.parametrize("cls", TOOLS)
def test_wrong_method_frame_option_fails_even_on_empty_input(cls):
    option = "structure_index" if cls is ConformerScreening else "structure_indices"
    with pytest.raises(UnknownArgumentError, match=option):
        tool(cls).run([], **{option: 0})


@pytest.mark.parametrize("cls", TOOLS)
@pytest.mark.parametrize("method", ["__init__", "evaluate", "run"])
def test_inherited_implementation_retains_definition_contract(cls, method):
    child = type("ApplicationEvaluator", (cls,), {"__module__": "consumer.screening"})
    plan = getattr(child, method).digestion_plan
    owner = f"{cls.__module__}.{method}"
    assert plan.contract_owner == "definition"
    assert plan.contract_caller == owner
    contract = plan.contracts.resolve(owner)
    assert contract is not None
    description = describe_contract(contract, plan.domains)
    if method == "run":
        expected = {
            name
            for name, parameter in signature(cls.evaluate).parameters.items()
            if name not in {"self", "molecular_system"}
            and parameter.kind
            in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY)
        }
        assert set(description["admitted_domains"][0]["members"]) == expected
    else:
        assert description["admits"] == "signature"


@pytest.mark.parametrize("cls", TOOLS)
@pytest.mark.parametrize("on_error", ["raise", "record"])
def test_valid_empty_batch_and_inherited_defaults_remain_valid(cls, on_error):
    child = type("ApplicationEvaluator", (cls,), {"__module__": "consumer.screening"})
    frame = (
        {"structure_indices": [2, 0]}
        if issubclass(cls, ConformerScreening)
        else {"structure_index": 2}
    )
    assert tool(child).run([], on_error=on_error, selection=[0], **frame) == []


@pytest.mark.parametrize("cls", TOOLS)
def test_valid_options_forward_once_and_batch_owns_pose_ids(cls, monkeypatch):
    evaluator = tool(cls)
    source = object()
    selection = [0, 2]
    frames = [2, 0]
    options = (
        {"structure_indices": frames}
        if cls is ConformerScreening
        else {"structure_index": 2}
    )
    calls = []

    def evaluate(system, **kwargs):
        calls.append((system, kwargs))
        return {"status": "not_matched", "fit_value": 0, "pose_id": kwargs["pose_id"]}

    monkeypatch.setattr(evaluator, "evaluate", evaluate)
    result = evaluator.run(
        iter([source, source]),
        selection=selection,
        chemical_state="structure",
        on_error="record",
        **options,
    )
    assert [row["input_index"] for row in result] == [0, 1]
    assert [row["pose_id"] for row in result] == [0, 1]
    assert all(system is source for system, _ in calls)
    assert all(kwargs["selection"] is selection for _, kwargs in calls)
    for _, kwargs in calls:
        assert kwargs["chemical_state"] == "structure"
        if cls is ConformerScreening:
            assert kwargs["structure_indices"] == frames
            assert kwargs["on_error"] == "record"
        else:
            assert kwargs["structure_index"] == 2
            assert "on_error" not in kwargs
    with pytest.raises(ArgumentError, match="batch pose IDs"):
        evaluator.run([], pose_id="caller-owned")


@pytest.mark.parametrize("cls", TOOLS)
def test_internal_bypass_keeps_batch_policy_and_pose_identity_checks(cls):
    evaluator = tool(cls)
    with pytest.raises(ArgumentError, match="on_error"):
        evaluator.run([], on_error="ignore", skip_digestion=True)
    with pytest.raises(ArgumentError, match="batch pose IDs"):
        evaluator.run([], pose_id="override", skip_digestion=True)


@pytest.mark.parametrize("method", ["placed", "rigid", "conformers"])
def test_facade_invalid_empty_run_still_clears_both_caches(method):
    options = {} if method == "placed" else {"search_method": "seeded_hit"}
    screen = VirtualScreening(query(), screening_method=method, **options)
    screen.matches = [object()]
    screen.evaluations = [object()]
    with pytest.raises(UnknownArgumentError, match="typo_option"):
        screen.run([], on_error="record", typo_option=True)
    assert screen.matches == screen.evaluations == []
