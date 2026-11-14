"""Facade admission, entered-run failure timing and native child independence."""

import inspect

import numpy as np
import pytest
from argdigest import UnknownArgumentError, describe_contract

from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.screening import VirtualScreening
from tests.test_nested_facade_contracts import query


def facade(kind=VirtualScreening, method="placed"):
    options = {} if method == "placed" else {"search_method": "seeded_hit"}
    screen = kind(query(), screening_method=method, **options)
    screen.matches = [object()]
    screen.evaluations = [object()]
    return screen


def test_definition_owned_pipeline_and_legacy_signature():
    method = VirtualScreening.run
    control = inspect.signature(method).parameters["skip_digestion"]
    assert control.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert control.default is False
    plan = method.digestion_plan
    assert plan.contract_caller == "pharmacophoremt.screening.virtual_screening.run"
    assert not plan.enable_argument_digestion
    assert set(plan.pipeline_targets) == {"skip_digestion"}
    description = describe_contract(
        plan.contracts.resolve(plan.contract_caller), plan.domains
    )
    assert description["admits"] == "any"

    class ApplicationScreen(VirtualScreening):
        pass

    assert facade(ApplicationScreen).run([]) == []


@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
@pytest.mark.parametrize("positional", [False, True])
def test_invalid_facade_control_preserves_previous_caches_and_borrowed_input(
    flag, positional
):
    screen = facade()
    old_matches, old_evaluations = screen.matches, screen.evaluations

    class Borrowed:
        def __iter__(self):
            pytest.fail(
                "Invalid facade control cannot acquire or sample borrowed input"
            )

    args = (Borrowed(), flag) if positional else (Borrowed(),)
    kwargs = {} if positional else {"skip_digestion": flag}
    with pytest.raises(ArgumentError, match="skip_digestion"):
        screen.run(*args, **kwargs)
    assert screen.matches is old_matches and screen.evaluations is old_evaluations


@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
@pytest.mark.parametrize("positional", [False, True])
def test_real_public_bypass_is_literal_and_child_receives_no_facade_control(
    flag, positional, monkeypatch
):
    screen = facade()
    seen = []
    original = _contracts._boolean

    def observe(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    monkeypatch.setattr(_contracts, "_boolean", observe)

    def child(systems, *, on_error):
        assert systems == [] and on_error == "raise"
        assert screen.matches == screen.evaluations == []
        return []

    monkeypatch.setattr(screen.evaluator, "run", child)
    args = ([], flag) if positional else ([],)
    kwargs = {} if positional else {"skip_digestion": flag}
    assert screen.run(*args, **kwargs) == []
    assert len(seen) == (0 if flag is True else 1)
    if flag is not True:
        assert seen[0] is flag


@pytest.mark.parametrize(
    "options", [{}, {"skip_digestion": False}, {"skip_digestion": True}]
)
def test_consumes_once_after_reset_and_preserves_opaque_values_and_literal_keyword(
    options,
):
    screen = facade()
    source = object()
    selection = object()
    policy = object()
    nested = {"selection": object()}
    visits = []

    class Borrowed:
        def __iter__(self):
            assert screen.matches == screen.evaluations == []
            visits.append("iteration")
            yield source
            yield source

    def child(systems, *, on_error, **kwargs):
        assert visits == ["iteration"] and systems == [source, source]
        assert all(item is source for item in systems)
        assert on_error is policy
        assert set(kwargs) == {"selection", "evaluation_options"}
        assert kwargs["selection"] is selection
        assert kwargs["evaluation_options"] is nested
        return []

    screen.evaluator.run = child
    assert (
        screen.run(
            Borrowed(),
            on_error=policy,
            selection=selection,
            evaluation_options=nested,
            **options,
        )
        == []
    )
    assert visits == ["iteration"]


@pytest.mark.parametrize("method", ["placed", "rigid", "conformers"])
@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "options",
    [
        {"typo_option": True},
        {"on_error": "ignore"},
        {"evaluation_options": {"selection": "all"}},
    ],
)
def test_native_refusal_follows_materialization_and_reset_even_during_bypass(
    method, skip, options
):
    screen = facade(method=method)
    visits = []

    class Borrowed:
        def __iter__(self):
            assert screen.matches == screen.evaluations == []
            visits.append("iteration")
            yield object()

    with pytest.raises((ArgumentError, UnknownArgumentError)):
        screen.run(Borrowed(), skip_digestion=skip, **options)
    assert visits == ["iteration"]
    assert screen.matches == screen.evaluations == []


@pytest.mark.parametrize("skip", [False, True])
def test_iterator_child_and_score_failure_do_not_publish_partial_caches(skip):
    screen = facade()

    def broken():
        assert screen.matches == screen.evaluations == []
        yield object()
        raise RuntimeError("borrowed reader failed")

    with pytest.raises(RuntimeError, match="borrowed reader failed"):
        screen.run(broken(), skip_digestion=skip)
    assert screen.matches == screen.evaluations == []

    def child(systems, *, on_error, **kwargs):
        raise RuntimeError("native batch failed")

    screen.evaluator.run = child
    with pytest.raises(RuntimeError, match="native batch failed"):
        screen.run([object()], skip_digestion=skip)
    assert screen.matches == screen.evaluations == []

    # A matched malformed record fails at the original ranking boundary.
    screen.evaluator.run = lambda systems, **kwargs: [
        {"status": "matched", "input_index": 0}
    ]
    with pytest.raises((ArgumentError, KeyError)):
        screen.run([object()], skip_digestion=skip)
    assert screen.matches == screen.evaluations == []


@pytest.mark.parametrize("skip", [False, True])
def test_plain_python_binding_errors_do_not_enter_run_or_clear_caches(skip):
    screen = facade()
    old_matches, old_evaluations = screen.matches, screen.evaluations
    with pytest.raises(TypeError):
        screen.run(skip_digestion=skip)
    assert screen.matches is old_matches and screen.evaluations is old_evaluations
    with pytest.raises(TypeError):
        screen.run([], skip, skip_digestion=skip)
    assert screen.matches is old_matches and screen.evaluations is old_evaluations


@pytest.mark.parametrize("method", ["placed", "rigid", "conformers"])
@pytest.mark.parametrize("skip", [False, True])
def test_empty_native_batch_still_validates_options_and_publishes_empty_caches(
    method, skip
):
    screen = facade(method=method)
    assert screen.run([], skip_digestion=skip) == []
    assert screen.matches == screen.evaluations == []
    with pytest.raises(UnknownArgumentError, match="typo_option"):
        screen.run([], skip_digestion=skip, typo_option=True)
    assert screen.matches == screen.evaluations == []
