"""Independent rigid-search admission retains scientific budgets and children."""

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
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
from pharmacophoremt.screening import PoseEvaluator, RigidPoseSearch
from phmt_test_support.absence_inputs import moved, system
from tests.test_nested_facade_contracts import query
from tests.test_seeded_scoring import hydrophobic_query, ionic_case

RIGID = importlib.import_module("pharmacophoremt.screening.rigid_search")
NAMES = ["__init__", "evaluate", "run"]


@pytest.mark.parametrize("name", NAMES)
def test_explicit_keyword_only_control_keeps_definition_and_forwarded_contract(name):
    operation = getattr(RigidPoseSearch, name)
    control = inspect.signature(operation).parameters["skip_digestion"]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY and control.default is False
    child = type(
        "ApplicationSearch", (RigidPoseSearch,), {"__module__": "consumer.search"}
    )
    plan = getattr(child, name).digestion_plan
    assert plan.contract_caller == operation.__module__ + "." + name
    description = describe_contract(
        plan.contracts.resolve(plan.contract_caller), plan.domains
    )
    if name == "run":
        assert "skip_digestion" not in description["admitted_domains"][0]["members"]
    else:
        assert description["admits"] == "signature"


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_child_or_reader(name, flag, monkeypatch):
    q = query()
    search = RigidPoseSearch(q)

    def forbidden(*args, **kwargs):
        pytest.fail(
            "Invalid operation control must refuse before child work or reader acquisition"
        )

    class Borrowed:
        def __iter__(self):
            forbidden()

    monkeypatch.setattr(RIGID, "PoseEvaluator", forbidden)
    monkeypatch.setattr(RIGID, "get_features", forbidden)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        if name == "__init__":
            RigidPoseSearch(q, skip_digestion=flag)
        elif name == "evaluate":
            search.evaluate(object(), skip_digestion=flag)
        else:
            search.run(Borrowed(), skip_digestion=flag)


@pytest.mark.parametrize("name", NAMES)
@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
def test_literal_public_bypass_keeps_child_default(name, flag, monkeypatch):
    q = query()
    search = RigidPoseSearch(q)
    seen = []
    original = _contracts._boolean

    def observe(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    def recognition_failure(*args, **kwargs):
        raise RuntimeError("recognition entered")

    monkeypatch.setattr(_contracts, "_boolean", observe)
    monkeypatch.setattr(RIGID, "get_features", recognition_failure)
    if name == "__init__":
        RigidPoseSearch(q, skip_digestion=flag)
    elif name == "evaluate":
        with pytest.raises(PoseEvaluationError) as caught:
            search.evaluate(object(), skip_digestion=flag)
        assert isinstance(caught.value.__cause__, RuntimeError)
        assert caught.value.extra["stage"] == "recognition"
    else:
        assert search.run([], skip_digestion=flag) == []
    # Construction validates both its PoseEvaluator and copied Pharmacophore.
    assert len(seen) == (0 if flag is True else 1) + 2 * (name == "__init__")
    if flag is not True:
        assert seen[0] is flag
    if name == "__init__":
        assert seen[-2:] == [False, False]


@pytest.mark.parametrize(
    "options", [{}, {"skip_digestion": False}, {"skip_digestion": True}]
)
def test_real_batch_children_keep_default_control_and_failed_denominator(
    options, monkeypatch
):
    search = RigidPoseSearch(query())
    seen = []
    original = _contracts._boolean

    def observe(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    def recognition_failure(*args, **kwargs):
        raise RuntimeError("recognition failed")

    monkeypatch.setattr(_contracts, "_boolean", observe)
    monkeypatch.setattr(RIGID, "get_features", recognition_failure)
    source = object()
    rows = search.run(iter([source, source]), on_error="record", **options)
    assert [r["input_index"] for r in rows] == [0, 1]
    assert [r["pose_id"] for r in rows] == [0, 1]
    assert all(r["status"] == "failed" and r["fit_value"] is None for r in rows)
    assert all(r["error"]["cause"] == "RuntimeError" for r in rows)
    assert seen == ([False] if options.get("skip_digestion") is not True else []) + [
        False,
        False,
    ]


@pytest.mark.parametrize("skip", [False, True])
def test_batch_preserves_legacy_evaluate_override_without_forwarding_control(skip):
    calls = []

    class ApplicationSearch(RigidPoseSearch):
        def evaluate(self, molecular_system, *, selection, pose_id):
            calls.append((molecular_system, selection, pose_id))
            return {"status": "not_matched", "fit_value": 0, "pose_id": pose_id}

    source = object()
    selection = [0, 2]
    rows = ApplicationSearch(query()).run(
        [source, source], selection=selection, skip_digestion=skip
    )
    assert [r["input_index"] for r in rows] == [0, 1]
    assert [p for _, _, p in calls] == [0, 1]
    assert all(s is source and sel is selection for s, sel, _ in calls)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "kind", ["method", "short_query", "collinear", "fraction", "length"]
)
def test_native_constructor_and_child_invariants_survive_bypass(skip, kind):
    q = query()
    options = {}
    if kind == "method":
        options["search_method"] = "unknown"
    elif kind in {"short_query", "collinear"}:
        q = Pharmacophore()
        for x in range(2 if kind == "short_query" else 3):
            q.add_interaction_site(
                InteractionSite(
                    Sphere(puw.quantity([x, 0, 0], "nm"), ".1 nm"), "hydrophobicity"
                )
            )
    elif kind == "fraction":
        options["min_fit_value"] = float("nan")
    else:
        options["point_tolerance"] = 0.1
    with pytest.raises(ArgumentError):
        RigidPoseSearch(q, skip_digestion=skip, **options)


@pytest.mark.parametrize("budget", [0, -1, True])
def test_bypassed_noncanonical_budget_is_refused_by_owner_before_alignment(
    budget, monkeypatch
):
    source, q = ionic_case()
    search = RigidPoseSearch(q, max_trials=budget, skip_digestion=True)

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid budget cannot reach alignment")

    monkeypatch.setattr(RIGID, "align_to_pharmacophore", forbidden)
    with pytest.raises(PoseEvaluationError) as caught:
        search.evaluate(source, skip_digestion=True)
    assert caught.value.extra["stage"] == "correspondence"
    assert isinstance(caught.value.__cause__, ArgumentError)
    assert "max_trials" in str(caught.value.__cause__)


@pytest.mark.parametrize("skip", [False, True])
def test_batch_policy_and_pose_id_guards_survive_bypass(skip):
    search = RigidPoseSearch(query())
    with pytest.raises(ArgumentError, match="on_error"):
        search.run([], on_error="ignore", skip_digestion=skip)
    with pytest.raises(ArgumentError, match="batch pose IDs"):
        search.run([], pose_id="caller-owned", skip_digestion=skip)


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("method", ["placed_and_triplets", "seeded_hit"])
def test_real_search_parity_custody_attribution_and_independent_pose_child(
    unit, method, monkeypatch
):
    with puw.context(standard_units=[unit, "ps", "radians"]):
        source, q = ionic_case()
        source = moved(source)
        before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
        seen = []
        original = PoseEvaluator.evaluate

        def child(evaluator, *args, **kwargs):
            assert "skip_digestion" not in kwargs
            seen.append("native default admission")
            return original(evaluator, *args, **kwargs)

        monkeypatch.setattr(PoseEvaluator, "evaluate", child)
        expected = None
        for options in ({}, {"skip_digestion": False}, {"skip_digestion": True}):
            search = RigidPoseSearch(q, search_method=method, max_trials=27, **options)
            with phmt.attribution():
                result = search.evaluate(source, pose_id="fixed", **options)
            assert result["status"] == "matched" and result["fit_value"] == 1
            assert result["attribution"]["status"] == "captured"
            assert result["search"]["max_trials"] == 27
            assert result["search"]["identity_pose_tested"] is (
                method == "placed_and_triplets"
            )
            if method == "seeded_hit":
                assert result["ranking_score"] == 1
                assert result["search"]["termination"] == "hit_found"
            record = puw.QuantityRecord.from_dict(result["criteria"]["point_tolerance"])
            assert record.field == "point_tolerance"
            value = record.to_quantity(unit="nm", dimensionality={"[L]": 1})
            assert float(puw.get_value(value, to_unit="nm")) == pytest.approx(0.1)
            observed = {
                key: result[key]
                for key in ("status", "fit_value", "assignments", "search", "criteria")
            }
            if expected is None:
                expected = observed
            else:
                assert observed == expected
            rows = search.run(
                [source, "invalid source", source], on_error="record", **options
            )
            assert [r["input_index"] for r in rows] == [0, 1, 2]
            assert [r["status"] for r in rows] == ["matched", "failed", "matched"]
            assert rows[1]["fit_value"] is None
        assert seen
        np.testing.assert_array_equal(
            puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
        )


@pytest.mark.parametrize("skip", [False, True])
def test_incomplete_budget_retains_unscored_failure_and_original_cause(skip):
    source, q = ionic_case(extra_optional=True)
    search = RigidPoseSearch(
        q, search_method="seeded_hit", max_trials=1, skip_digestion=skip
    )
    row = search.run([source], on_error="record", skip_digestion=skip)[0]
    assert row["status"] == "failed" and row["fit_value"] is None
    assert row["error"]["stage"] == "search_budget"
    assert row["error"]["cause_code"] == "PHMT-E105"


@pytest.mark.parametrize("skip", [False, True])
def test_complete_no_seed_negative_has_no_fabricated_pose(skip):
    source = system("CCC", [[0, 0, 0], [0.15, 0, 0], [0.3, 0, 0]])
    search = RigidPoseSearch(
        hydrophobic_query(), search_method="seeded_hit", skip_digestion=skip
    )
    row = search.evaluate(source, skip_digestion=skip)
    assert row["status"] == "not_matched" and row["ranking_score"] == 0
    assert row["fit_value"] is None and row["pose_evaluated"] is False
    assert "assignments" not in row
    assert row["search"]["n_fitted"] == 0 and row["search"]["enumeration_complete"]
