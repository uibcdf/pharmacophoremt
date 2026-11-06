"""Retrospective settings admission and analytical cohort-accounting controls."""

from copy import deepcopy

import numpy as np
import pytest
from argdigest import UnknownArgumentError, describe_contract

from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.screening import ConformerScreening, PoseEvaluator, RigidPoseSearch
from pharmacophoremt.validation import (
    RetrospectiveValidator,
    compare_screening_results,
    summarize_screening_results,
)
from tests.test_nested_facade_contracts import query
from tests.test_saved_results import arm

COLLISIONS = [(0.5, 0.5), (0.5, float(np.nextafter(0.5, 1.0)))]


def validator():
    model = query()
    return RetrospectiveValidator(model, evaluator=PoseEvaluator(model))


@pytest.mark.parametrize("fractions", COLLISIONS)
@pytest.mark.parametrize("skip", [False, True])
def test_colliding_keys_fail_before_consuming_inputs_or_evaluating(
    fractions, skip, monkeypatch
):
    tool = validator()
    consumed = []

    def inputs(label):
        consumed.append(label)
        yield object()

    def forbidden(*args, **kwargs):
        pytest.fail("colliding metric keys must fail before native evaluation")

    monkeypatch.setattr(tool.evaluator, "run", forbidden)
    with pytest.raises(ArgumentError, match="distinct reported keys"):
        tool.run(
            inputs("active"),
            inputs("decoy"),
            ef_fractions=fractions,
            skip_digestion=skip,
        )
    assert consumed == []


@pytest.mark.parametrize("fractions", COLLISIONS)
@pytest.mark.parametrize("paired", [False, True])
def test_saved_result_settings_keep_the_same_collision_refusal(fractions, paired):
    saved = arm([], [])
    with pytest.raises(ArgumentError, match="distinct reported keys"):
        if paired:
            compare_screening_results([], saved, saved, ef_fractions=fractions)
        else:
            summarize_screening_results([], **saved, ef_fractions=fractions)


@pytest.mark.parametrize(
    "method,admission", [("__init__", "signature"), ("run", "any")]
)
def test_inherited_retrospective_contract_is_explicit(method, admission):
    mixin = type("Presentation", (), {"__module__": "consumer.validation"})
    child = type(
        "ApplicationValidator",
        (mixin, RetrospectiveValidator),
        {"__module__": "consumer.validation"},
    )
    plan = getattr(child, method).digestion_plan
    owner = f"pharmacophoremt.validation.retrospective.{method}"
    assert plan.contract_owner == "definition" and plan.contract_caller == owner
    contract = plan.contracts.resolve(owner)
    assert contract is not None
    description = describe_contract(contract, plan.domains)
    assert description["admits"] == admission
    assert description["admitted_domains"] == []


@pytest.mark.parametrize(
    "endpoint", [summarize_screening_results, compare_screening_results]
)
def test_saved_result_closed_contract_is_declared(endpoint):
    plan = endpoint.digestion_plan
    owner = f"pharmacophoremt.validation.saved_results.{endpoint.__name__}"
    assert plan.contract_owner == "definition" and plan.contract_caller == owner
    contract = plan.contracts.resolve(owner)
    assert contract is not None
    assert describe_contract(contract, plan.domains)["admits"] == "signature"


@pytest.mark.parametrize(
    "endpoint", [summarize_screening_results, compare_screening_results]
)
@pytest.mark.parametrize("option", ["kwargs", "ef_fraction", "evaluation_options"])
def test_closed_result_contract_refuses_typos_before_values(endpoint, option):
    with pytest.raises(UnknownArgumentError, match=option):
        if endpoint is summarize_screening_results:
            endpoint(None, None, input_mapping=None, score_method=None, **{option: 1})
        else:
            endpoint(None, None, None, **{option: 1})


@pytest.mark.parametrize("skip", [False, True])
def test_distinct_metric_keys_keep_exact_fraction_values_and_input_identity(
    skip, monkeypatch
):
    tool = validator()
    source = object()
    selection = [0, 2]
    calls = []

    def evaluate(systems, **kwargs):
        calls.append((systems, kwargs))
        return [
            {"input_index": 0, "status": "matched", "fit_value": 1.0},
            {"input_index": 1, "status": "not_matched", "fit_value": 0.0},
        ]

    monkeypatch.setattr(tool.evaluator, "run", evaluate)
    result = tool.run(
        iter([source]),
        iter([source]),
        selection=selection,
        ef_fractions=(0.5, 0.51, 1.0),
        skip_digestion=skip,
    )
    assert result["EF@50%"] == 2.0
    assert result["EF@51%"] == result["EF@100%"] == 1.0
    assert result["AUC"] == result["BEDROC"] == 1.0
    assert result["n_actives"] == result["n_decoys"] == 1
    assert result["evaluated_indices"].tolist() == [0, 1]
    assert len(calls) == 1 and all(item is source for item in calls[0][0])
    assert calls[0][1]["selection"] is selection


@pytest.mark.parametrize("cls", [PoseEvaluator, RigidPoseSearch, ConformerScreening])
def test_retrospective_forwards_to_selected_native_batch_and_preserves_failures(
    cls, monkeypatch
):
    evaluator = cls(query())
    tool = RetrospectiveValidator(
        query(), evaluator=evaluator, score_method="checked_pose_coverage"
    )
    inputs = [object(), object(), object()]
    records = [
        {"input_index": 0, "status": "matched", "fit_value": 1.0},
        {
            "input_index": 1,
            "status": "failed",
            "fit_value": None,
            "error": {
                "stage": "source",
                "message": "controlled source failure",
                "cause": "LookupError",
            },
        },
        {"input_index": 2, "status": "not_matched", "fit_value": 0.0},
    ]
    before = deepcopy(records)
    frame = (
        {"structure_indices": [2, 0]}
        if cls is ConformerScreening
        else {"structure_index": 2}
    )
    calls = []

    def run(systems, **options):
        calls.append((systems, options))
        return records

    monkeypatch.setattr(evaluator, "run", run)
    result = tool.run(iter(inputs[:2]), iter(inputs[2:]), on_error="record", **frame)
    assert len(calls) == 1 and calls[0][0] == inputs
    assert calls[0][1] == dict(frame, on_error="record")
    assert result["n_actives"] == 2 and result["n_failed"] == 1
    assert result["n_actives_evaluated"] == result["n_decoys_evaluated"] == 1
    assert result["evaluated_indices"].tolist() == [0, 2]
    assert result["labels"].tolist() == [1, 0] and result["scores"].tolist() == [1, 0]
    assert (
        result["failures"] == [records[1]]
        and result["failures"][0]["fit_value"] is None
    )
    assert records == before
