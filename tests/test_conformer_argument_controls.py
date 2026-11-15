"""Conformer controls preserve requested frames, failure meaning and children."""

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
from pharmacophoremt.screening import ConformerScreening
from phmt_test_support.absence_inputs import moved, system
from tests.test_conformer_screening import add_declared_state, unpack
from tests.test_nested_facade_contracts import query
from tests.test_seeded_scoring import hydrophobic_query, ionic_case

CONFORMER = importlib.import_module("pharmacophoremt.screening.conformer_screening")
NAMES = ["__init__", "evaluate", "run"]


def ionic_ensemble(*, extra_optional=False):
    source, q = ionic_case(extra_optional=extra_optional)
    source.structures.append(coordinates=msm.get(moved(source), coordinates=True))
    return source, q


@pytest.mark.parametrize("name", NAMES)
def test_explicit_control_keeps_definition_and_forwarded_contract(name):
    method = getattr(ConformerScreening, name)
    control = inspect.signature(method).parameters["skip_digestion"]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY and control.default is False
    child = type(
        "ApplicationEnsemble",
        (ConformerScreening,),
        {"__module__": "consumer.ensembles"},
    )
    plan = getattr(child, name).digestion_plan
    assert plan.contract_caller == method.__module__ + "." + name
    contract = describe_contract(
        plan.contracts.resolve(plan.contract_caller), plan.domains
    )
    if name == "run":
        assert "skip_digestion" not in contract["admitted_domains"][0]["members"]
    else:
        assert contract["admits"] == "signature"


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_child_provider_or_reader(
    name, flag, monkeypatch
):
    q = query()
    screen = ConformerScreening(q)

    def forbidden(*args, **kwargs):
        pytest.fail(
            "Invalid control cannot acquire a reader, enter a child or query frames"
        )

    class Borrowed:
        def __iter__(self):
            forbidden()

    monkeypatch.setattr(CONFORMER, "RigidPoseSearch", forbidden)
    monkeypatch.setattr(CONFORMER, "capability", forbidden)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        if name == "__init__":
            ConformerScreening(q, skip_digestion=flag)
        elif name == "evaluate":
            screen.evaluate(object(), skip_digestion=flag)
        else:
            screen.run(Borrowed(), skip_digestion=flag)


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
def test_literal_bypass_retains_all_default_constructor_children(
    name, flag, monkeypatch
):
    q = query()
    screen = ConformerScreening(q)
    seen = []
    original = _contracts._boolean

    def observe(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    def frame_failure(*args, **kwargs):
        raise RuntimeError("frame boundary entered")

    monkeypatch.setattr(_contracts, "_boolean", observe)
    monkeypatch.setattr(CONFORMER, "capability", frame_failure)
    if name == "__init__":
        ConformerScreening(q, skip_digestion=flag)
    elif name == "evaluate":
        with pytest.raises(PoseEvaluationError) as caught:
            screen.evaluate(object(), skip_digestion=flag)
        assert caught.value.extra["stage"] == "frames"
        assert isinstance(caught.value.__cause__, RuntimeError)
    else:
        assert screen.run([], skip_digestion=flag) == []
    children = (
        3 if name == "__init__" else 0
    )  # RigidPoseSearch, PoseEvaluator, copied model.
    assert len(seen) == (0 if flag is True else 1) + children
    if flag is not True:
        assert seen[0] is flag
    if children:
        assert seen[-children:] == [False] * children


@pytest.mark.parametrize(
    "options", [{}, {"skip_digestion": False}, {"skip_digestion": True}]
)
def test_batch_child_default_policy_and_failed_denominator(options, monkeypatch):
    screen = ConformerScreening(query())
    seen = []
    original = _contracts._boolean

    def observe(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    def frame_failure(*args, **kwargs):
        raise RuntimeError("frames failed")

    monkeypatch.setattr(_contracts, "_boolean", observe)
    monkeypatch.setattr(CONFORMER, "capability", frame_failure)
    rows = screen.run(iter([object(), object()]), on_error="record", **options)
    assert [r["input_index"] for r in rows] == [0, 1]
    assert [r["pose_id"] for r in rows] == [0, 1]
    assert all(r["status"] == "failed" and r["fit_value"] is None for r in rows)
    assert all(r["error"]["stage"] == "frames" for r in rows)
    assert seen == ([False] if options.get("skip_digestion") is not True else []) + [
        False,
        False,
    ]


@pytest.mark.parametrize("skip", [False, True])
def test_batch_preserves_legacy_override_and_forwards_failure_policy_only(skip):
    calls = []

    class ApplicationEnsemble(ConformerScreening):
        def evaluate(self, molecular_system, *, selection, pose_id, on_error):
            calls.append((molecular_system, selection, pose_id, on_error))
            return {"status": "not_matched", "fit_value": 0, "pose_id": pose_id}

    source = object()
    selection = [0, 2]
    rows = ApplicationEnsemble(query()).run(
        [source, source], selection=selection, on_error="record", skip_digestion=skip
    )
    assert [r["input_index"] for r in rows] == [0, 1]
    assert [p for _, _, p, _ in calls] == [0, 1]
    assert all(
        s is source and sel is selection and policy == "record"
        for s, sel, _, policy in calls
    )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("policy", [None, "ignore", [], True])
def test_failure_policy_is_mandatory_before_frame_acquisition(
    skip, policy, monkeypatch
):
    screen = ConformerScreening(query())

    def forbidden(*args, **kwargs):
        pytest.fail("An invalid failure policy cannot acquire frames")

    monkeypatch.setattr(CONFORMER, "capability", forbidden)
    with pytest.raises(ArgumentError, match="on_error"):
        screen.evaluate(object(), on_error=policy, skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "kind", ["method", "budget", "fraction", "empty_query", "length"]
)
def test_constructor_children_keep_native_invariants(skip, kind):
    q = query()
    options = {}
    if kind == "method":
        options["search_method"] = "unknown"
    elif kind == "budget":
        options["max_trials"] = 0
    elif kind == "fraction":
        options["min_fit_value"] = float("nan")
    elif kind == "empty_query":
        q = Pharmacophore()
    else:
        options["point_tolerance"] = 0.1
    with pytest.raises(ArgumentError):
        ConformerScreening(q, skip_digestion=skip, **options)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("kind", ["empty", "bounds"])
def test_missing_or_out_of_bounds_frames_remain_failed_not_negative(
    skip, kind, monkeypatch
):
    source, q = ionic_case()
    screen = ConformerScreening(q)
    options = {"structure_indices": [99]} if kind == "bounds" else {}
    if kind == "empty":
        monkeypatch.setattr(CONFORMER, "capability", lambda name: lambda *a, **kw: [])
    with pytest.raises(PoseEvaluationError) as caught:
        screen.evaluate(source, skip_digestion=skip, **options)
    assert caught.value.extra["stage"] == "frames"
    assert caught.value.__cause__ is not None


@pytest.mark.parametrize("skip", [False, True])
def test_native_batch_policy_and_pose_ids_remain_mandatory(skip):
    screen = ConformerScreening(query())
    with pytest.raises(ArgumentError, match="on_error"):
        screen.run([], on_error="ignore", skip_digestion=skip)
    with pytest.raises(ArgumentError, match="batch pose IDs"):
        screen.run([], pose_id="caller-owned", skip_digestion=skip)


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("method", ["placed_and_triplets", "seeded_hit"])
def test_real_order_ties_quantities_attribution_and_source_custody(
    unit, method, monkeypatch
):
    with puw.context(standard_units=[unit, "ps", "radians"]):
        source, q = ionic_ensemble()
        before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
        expected = None
        for options in ({}, {"skip_digestion": False}, {"skip_digestion": True}):
            screen = ConformerScreening(
                q, max_trials=27, search_method=method, **options
            )
            original = screen.search.evaluate
            frames = []

            def child(system, **kwargs):
                assert "skip_digestion" not in kwargs and "on_error" not in kwargs
                frames.append(kwargs["structure_index"])
                return original(system, **kwargs)

            monkeypatch.setattr(screen.search, "evaluate", child)
            with phmt.attribution():
                row = screen.evaluate(
                    source, structure_indices=[1, 0], pose_id="fixed", **options
                )
            assert frames == [1, 0]
            assert row["attribution"]["status"] == "captured"
            assert row["status"] == "matched" and row["fit_value"] == 1
            assert row["best_conformer_index"] == 1
            assert row["ensemble"]["structure_indices"] == [1, 0]
            assert (
                row["ensemble"]["n_evaluated"] == 2 and row["ensemble"]["n_failed"] == 0
            )
            assert [c["conformer_index"] for c in row["conformers"]] == [1, 0]
            assert [c["resolved_chemical_state_index"] for c in row["conformers"]] == [
                0,
                0,
            ]
            assert unpack(row["pose_coordinates"]).shape == (1, 3, 3)
            record = puw.QuantityRecord.from_dict(row["criteria"]["point_tolerance"])
            assert record.field == "point_tolerance"
            quantity = record.to_quantity(unit="nm", dimensionality={"[L]": 1})
            assert float(puw.get_value(quantity, to_unit="nm")) == pytest.approx(0.1)
            observed = {
                k: row[k]
                for k in ("status", "fit_value", "best_conformer_index", "ensemble")
            }
            if expected is None:
                expected = observed
            else:
                assert observed == expected
        np.testing.assert_array_equal(
            puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("method", ["placed_and_triplets", "seeded_hit"])
def test_recorded_failure_resolves_only_a_criterion_specific_proven_maximum(
    skip, method, monkeypatch
):
    source, q = ionic_ensemble(extra_optional=True)
    screen = ConformerScreening(
        q, max_trials=27, search_method=method, skip_digestion=skip
    )
    original = screen.search.evaluate
    frames = []

    def child(system, **kwargs):
        assert "skip_digestion" not in kwargs
        frames.append(kwargs["structure_index"])
        if kwargs["structure_index"] == 1:
            raise PoseEvaluationError(
                pose_id=kwargs["pose_id"],
                stage="control",
                reason="injected frame failure",
            )
        return original(system, **kwargs)

    monkeypatch.setattr(screen.search, "evaluate", child)
    row = screen.evaluate(
        source, structure_indices=[1, 0], on_error="record", skip_digestion=skip
    )
    assert frames == [1, 0]
    assert row["ensemble"]["n_requested"] == 2
    assert row["ensemble"]["n_evaluated"] == row["ensemble"]["n_failed"] == 1
    assert not row["ensemble"]["complete"]
    assert [c["conformer_index"] for c in row["conformers"]] == [1, 0]
    assert row["conformers"][0]["status"] == "failed"
    assert row["conformers"][0]["fit_value"] is None
    assert row["conformers"][1]["fit_value"] == pytest.approx(0.75)
    binary = method == "seeded_hit"
    assert row["ensemble"]["score_resolved"] is binary
    assert row["ensemble"]["proven_maximum"] is binary
    if binary:
        assert row["status"] == "matched" and row["ranking_score"] == 1
        assert (
            row["fit_value"] == pytest.approx(0.75) and row["best_conformer_index"] == 0
        )
    else:
        assert row["status"] == "failed" and row["fit_value"] is None
        assert row["best_conformer_index"] is None
        assert row["best_observed"]["status"] == "matched"
    with pytest.raises(PoseEvaluationError) as caught:
        screen.evaluate(
            source, structure_indices=[1, 0], on_error="raise", skip_digestion=skip
        )
    assert caught.value.extra["stage"] == "control"


@pytest.mark.parametrize("skip", [False, True])
def test_complete_seeded_negative_keeps_no_pose_and_requested_order(skip):
    source = system("CCC", [[0, 0, 0], [0.15, 0, 0], [0.3, 0, 0]])
    source.structures.append(coordinates=msm.get(source, coordinates=True))
    screen = ConformerScreening(
        hydrophobic_query(), search_method="seeded_hit", skip_digestion=skip
    )
    row = screen.evaluate(source, structure_indices=[1, 0], skip_digestion=skip)
    assert row["status"] == "not_matched" and row["ranking_score"] == 0
    assert row["fit_value"] is None and row["pose_coordinates"] is None
    assert row["best_conformer_index"] == 1
    assert row["ensemble"]["complete"] and row["ensemble"]["score_resolved"]
    assert all(
        c["pose_evaluated"] is False and c["pose_coordinates"] is None
        for c in row["conformers"]
    )


@pytest.mark.parametrize("skip", [False, True])
def test_declared_structure_states_keep_frame_identity_during_bypass(skip):
    source, q = ionic_ensemble()
    add_declared_state(source, [0, 0, 0])
    msm.set(source, element="system", structure_chemical_state_index=[0, 1])
    row = ConformerScreening(q, skip_digestion=skip).evaluate(
        source,
        structure_indices=[1, 0],
        chemical_state="structure",
        skip_digestion=skip,
    )
    assert [c["resolved_chemical_state_index"] for c in row["conformers"]] == [1, 0]
    assert [c["status"] for c in row["conformers"]] == ["not_matched", "matched"]
    assert row["best_conformer_index"] == 0 and row["status"] == "matched"
    assert msm.get(source, structure_chemical_state_index=True) == [0, 1]
