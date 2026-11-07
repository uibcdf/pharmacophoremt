"""Public create/resume/view composition over the established native controls."""

import json
from copy import deepcopy
from dataclasses import replace

import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.screening import (
    PreparedRunPlan,
    PreparedScreeningRun,
    build_prepared_run_plan,
    resume_prepared_run,
)
from pharmacophoremt.screening import prepared_runs as runtime
from pharmacophoremt_results import ScreeningRunView, canonical_json
from tests.test_prepared_library_recovery import observe_evaluations
from tests.test_prepared_library_recovery import prepared_run as _shared_prepared_run
from tests.test_prepared_library_reference import TrackedSource

# Expose the existing public-recovery fixture without duplicating native setup.
prepared_run = _shared_prepared_run


def create(case, **overrides):
    options = {
        "plan": case["plan"],
        "manifest_path": case["manifest"],
        "run_id": "public:original",
    }
    options.update(overrides)
    return PreparedScreeningRun.create(case["path"], **options)


def reopen(case, **overrides):
    options = {"plan": case["plan"], "manifest_path": case["manifest"]}
    options.update(overrides)
    return PreparedScreeningRun.open(case["path"], **options)


def test_public_plan_exports_share_one_definition_and_legacy_aliases():
    from phmt_test_support.prepared_library_recovery import (
        RecoveryPlan,
        build_recovery_plan,
        resume_prepared,
    )

    assert PreparedRunPlan is runtime.PreparedRunPlan is RecoveryPlan
    assert build_prepared_run_plan is runtime.build_prepared_run_plan
    assert build_recovery_plan is build_prepared_run_plan
    assert resume_prepared is resume_prepared_run is runtime.resume_prepared_run
    plan = build_prepared_run_plan.digestion_plan
    owner = "pharmacophoremt.screening.prepared_runs.build_prepared_run_plan"
    assert plan.contract_caller == owner
    description = describe_contract(plan.contracts.resolve(owner), plan.domains)
    assert description["caller"] == owner
    assert description["admits"] == "signature"
    assert plan.enable_argument_digestion and plan.standardizer is None


def test_friendly_reopen_delivers_only_new_confirmations_but_saved_view_is_complete(
    prepared_run, monkeypatch
):
    case = prepared_run
    calls = observe_evaluations(monkeypatch)
    events = []
    reader = TrackedSource(case["entries"], events)
    with create(case) as run:
        assert run.run_id == "public:original" and run.parent_run_id is None
        assert run.query_bytes == case["query_path"].read_bytes()
        assert run.context == case["plan"].context
        outcomes = run.resume(reader)
        assert events == [] and calls == []
        first = next(outcomes)
        outcomes.close()
        assert events == ["iter", "next"] and calls == ["work:0"]
        assert list(run.results()) == [first]
        assert len(list(run.attempts("work:0"))) == 1
        assert run.summary()["counts"]["committed_work"] == 1
        assert run.top_results(limit=1)["records"][0]["outcome"] == first
        assert calls == ["work:0"] and events == ["iter", "next"]
        assert next(reader).work_key == "work:1"
    with ScreeningRunView.open(case["path"]) as view:
        assert view.configuration["format"] == "pharmacophoremt.screening-run@1"
        assert view.summary(score_method="checked_pose_coverage@1")["counts"] == {
            "declared_work": 2,
            "committed_work": 1,
            "scored_work": 1,
            "matched_work": 1,
            "not_matched_work": 0,
            "failed_work": 0,
            "pending_work": 1,
        }
        assert list(view.results()) == [first]
    with reopen(case) as run:
        delivered = list(run.resume(iter(case["entries"])))
        assert [row["work_key"] for row in delivered] == ["work:1"]
        assert calls == ["work:0", "work:1"]
        assert list(run.results()) == [first, *delivered]
        assert len(list(run.attempts("work:0"))) == 1
    with ScreeningRunView.open(case["path"]) as view:
        assert view.summary(score_method="checked_pose_coverage@1")[
            "manifest_work_complete"
        ]
        assert [row["work_key"] for row in view.results()] == ["work:0", "work:1"]


@pytest.mark.parametrize(
    "options", [{"typo": True}, {"skip_digestion": False}, {"skip_digestion": True}]
)
def test_run_factory_rejects_unknown_keywords_without_creating_a_file(
    prepared_run, options
):
    case = prepared_run
    with pytest.raises(TypeError):
        create(case, **options)
    assert not case["path"].exists()


@pytest.mark.parametrize(
    "options", [{"typo": True}, {"skip_digestion": False}, {"skip_digestion": True}]
)
def test_resume_rejects_unknown_keywords_before_borrowing_the_source(
    prepared_run, options
):
    case = prepared_run
    events = []
    reader = TrackedSource(case["entries"], events)
    with create(case) as run:
        with pytest.raises(TypeError):
            run.resume(reader, **options)
        assert events == [] and list(run.results()) == []


def test_invalid_plan_is_refused_before_creating_a_run(prepared_run):
    case = prepared_run
    with pytest.raises(ArgumentError):
        create(case, plan=object())
    assert not case["path"].exists()


def test_changed_saved_plan_preserves_existing_run_and_reports_incompatibility(
    prepared_run,
):
    case = prepared_run
    with create(case) as run:
        saved = list(run.resume(case["entries"]))
    original = case["path"].read_bytes()
    context = deepcopy(case["plan"].context)
    context["execution"]["evaluation_options"]["selection"] = [3, 4, 5]
    changed = replace(case["plan"], context_json=canonical_json(context))
    with pytest.raises(ValueError):
        with reopen(case, plan=changed):
            pass
    assert case["path"].read_bytes() == original
    with ScreeningRunView.open(case["path"]) as view:
        assert list(view.results()) == saved


def test_changed_companion_execution_identity_is_refused_before_source_iteration(
    prepared_run, monkeypatch
):
    case = prepared_run
    original_identity = deepcopy(case["plan"].context["runtime"])
    companion_fields = [
        name for name in original_identity if "results" in name or "companion" in name
    ]
    assert companion_fields, "the run must bind the actual companion implementation"
    changed = deepcopy(original_identity)
    for name in companion_fields:
        changed[name] = {"changed_companion_source": True}
    events = []
    reader = TrackedSource(case["entries"], events)
    with create(case) as run:
        monkeypatch.setattr(runtime, "_runtime_identity", lambda: changed)
        with pytest.raises(ArgumentError):
            run.resume(reader)
        assert events == [] and list(run.results()) == []


def test_friendly_run_context_is_detached_and_closed_runs_cannot_resume(prepared_run):
    case = prepared_run
    run = create(case)
    original = deepcopy(run.context)
    detached = run.context
    detached["execution"]["evaluation_options"]["selection"].clear()
    assert run.context == original
    run.close()
    run.close()
    events = []
    with pytest.raises(ValueError):
        run.resume(TrackedSource(case["entries"], events))
    assert events == []


def test_factory_unconsumed_close_and_saved_reading_do_not_create_credit(
    prepared_run,
):
    ackredit = pytest.importorskip("ackredit")
    case = prepared_run
    events = []
    with ackredit.session("public-run-lifetime") as application, phmt.attribution():
        before = ackredit.get_attribution().to_dict()
        with create(case) as run:
            outcomes = run.resume(TrackedSource(case["entries"], events))
            assert ackredit.get_attribution().to_dict() == before
            outcomes.close()
            assert run.summary()["counts"]["committed_work"] == 0
            assert run.top_results(limit=5)["records"] == []
            assert ackredit.get_attribution().to_dict() == before
        with ScreeningRunView.open(case["path"]) as view:
            assert list(view.results()) == []
            view.summary(score_method="checked_pose_coverage@1")
        assert ackredit.get_attribution().to_dict() == before
        assert ackredit.current_session() is application
    assert events == []


def test_partial_native_credit_remains_attached_after_reading_and_resume(
    prepared_run,
):
    ackredit = pytest.importorskip("ackredit")
    case = prepared_run
    with ackredit.session("public-run-consumed") as application, phmt.attribution():
        with create(case) as run:
            outcomes = run.resume(iter(case["entries"]))
            first = next(outcomes)
            outcomes.close()
        captured = ackredit.get_attribution().to_dict()
        assert first["native_result"]["attribution"]["status"] == "captured"
        assert first["native_result"]["attribution"]["references"]["uses"]
        frozen = json.dumps(first, sort_keys=True)
        with ScreeningRunView.open(case["path"]) as view:
            assert list(view.results()) == [first]
        assert ackredit.get_attribution().to_dict() == captured
        assert ackredit.current_session() is application
        with reopen(case) as run:
            later = list(run.resume(case["entries"]))
            assert [row["work_key"] for row in later] == ["work:1"]
            assert list(run.results())[0] == first
        assert json.dumps(first, sort_keys=True) == frozen
        assert ackredit.current_session() is application


def test_nondefault_application_units_survive_plan_execution_and_saved_replay(
    prepared_run,
):
    case = prepared_run
    original_query = case["query_path"].read_bytes()
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        policy = puw.configure.report()
        plan = build_prepared_run_plan(
            case["query_path"],
            screening_method="placed",
            score_method="checked_pose_coverage",
            compatibility=case["compatibility"],
            evaluation_options={"selection": [0, 1, 2]},
        )
        with create(case, plan=plan) as run:
            original = list(run.resume(case["entries"]))
        assert puw.configure.report() == policy
        assert plan.query_bytes == original_query
    with puw.context(standard_units=["angstrom", "ps", "radians"]):
        policy = puw.configure.report()
        with ScreeningRunView.open(case["path"]) as view:
            restored = list(view.results())
            assert view.query_bytes == original_query
        assert restored == original
        for outcome in restored:
            record = outcome["native_result"]["criteria"]["point_tolerance"]
            tolerance = puw.QuantityRecord.from_dict(record).to_quantity(
                field="point_tolerance", unit="nm", dimensionality={"[L]": 1}
            )
            assert float(puw.get_value(tolerance, to_unit="nm")) == pytest.approx(0.10)
            assert outcome["ranking_score"] == 1
        assert puw.configure.report() == policy
    assert case["query_path"].read_bytes() == original_query
