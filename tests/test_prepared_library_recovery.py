"""Public saved-query recovery preserves the analytical reference controls."""

import json
from copy import deepcopy
from dataclasses import replace
from functools import wraps

import pytest

from pharmacophoremt import Pharmacophore
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
from pharmacophoremt.io import to_json
from pharmacophoremt.screening import PoseEvaluator, PreparedInput, screen_prepared
from pharmacophoremt.screening import prepared_runs as recovery
from pharmacophoremt.screening.prepared_runs import (
    build_prepared_run_plan as build_recovery_plan,
)
from pharmacophoremt.screening.prepared_runs import (
    resume_prepared_run as resume_prepared,
)
from pharmacophoremt_results import ScreeningRunStore as ReferenceLedger
from phmt_test_support.absence_inputs import COORDINATES, reference
from tests.test_conformer_screening import ensemble, moved_coordinates
from tests.test_pose_evaluation import model_from_source, system
from tests.test_prepared_library_reference import TrackedSource
from tests.test_seeded_scoring import hydrophobic_query


@pytest.fixture
def prepared_run(tmp_path):
    source = system()
    query, _ = model_from_source(source)
    query_path = tmp_path / "query.json"
    to_json(query, str(query_path))
    mappings = [
        {
            "work_key": f"work:{index}",
            "source_key": "fixture:shared-record",
            "occurrence_key": f"row:{index}",
        }
        for index in range(2)
    ]
    manifest = tmp_path / "work.jsonl"
    manifest.write_text(
        "".join(json.dumps(mapping) + "\n" for mapping in mappings),
        encoding="utf-8",
    )
    compatibility = {
        "prepared_snapshot": "controlled-explicit-coordinate-fixture@1",
        "preparation": {"provider": "MolSysMT", "chemical_state": "reference"},
        "features": "classical_atomic_formal@1",
        "index": None,
        "grouping": "declared-work-occurrences@1",
        "numerical": {"coordinate_precision": "float64", "backend_threads": 1},
    }
    plan = build_recovery_plan(
        query_path,
        screening_method="placed",
        score_method="checked_pose_coverage",
        compatibility=compatibility,
        evaluation_options={"selection": [0, 1, 2]},
    )
    return {
        "source": source,
        "query_path": query_path,
        "manifest": manifest,
        "path": tmp_path / "original.sqlite3",
        "mappings": mappings,
        "entries": [
            PreparedInput(**mapping, molecular_system=source) for mapping in mappings
        ],
        "compatibility": compatibility,
        "plan": plan,
    }


def create(case, *, path=None, plan=None, run_id="run:original", parent_run_id=None):
    plan = plan or case["plan"]
    return ReferenceLedger.create(
        path or case["path"],
        run_id=run_id,
        parent_run_id=parent_run_id,
        query_bytes=plan.query_bytes,
        context=plan.context,
        manifest_path=case["manifest"],
    )


def reopen(case, *, path=None, plan=None):
    plan = plan or case["plan"]
    return ReferenceLedger.open(
        path or case["path"],
        query_bytes=plan.query_bytes,
        context=plan.context,
        manifest_path=case["manifest"],
    )


def observe_evaluations(monkeypatch):
    calls = []
    original = PoseEvaluator.evaluate

    @wraps(original)
    def observed(self, molecular_system, *args, **kwargs):
        calls.append(kwargs.get("pose_id"))
        return original(self, molecular_system, *args, **kwargs)

    monkeypatch.setattr(PoseEvaluator, "evaluate", observed)
    return calls


def build_changed(case, **changes):
    arguments = {
        "screening_method": "placed",
        "score_method": "checked_pose_coverage",
        "compatibility": deepcopy(case["compatibility"]),
        "evaluation_options": {"selection": [0, 1, 2]},
    }
    arguments.update(changes)
    return build_recovery_plan(case["query_path"], **arguments)


def test_saved_bytes_defaults_and_options_are_detached_from_live_callers(prepared_run):
    case = prepared_run
    options = {"selection": [0, 1, 2]}
    compatibility = deepcopy(case["compatibility"])
    plan = build_changed(case, evaluation_options=options, compatibility=compatibility)
    original_bytes = case["query_path"].read_bytes()
    assert plan.query_bytes == original_bytes
    execution = plan.context["execution"]
    assert execution["constructor_options"]["point_tolerance"] == "0.10 nm"
    assert execution["constructor_options"]["min_fit_value"] == 0
    assert execution["evaluation_options"]["structure_index"] == 0
    assert execution["evaluation_options"]["chemical_state"] == "reference"
    assert execution["on_error"] == "record"
    options["selection"][:] = [3, 4, 5]
    compatibility["preparation"]["chemical_state"] = "changed"
    execution["evaluation_options"]["selection"].clear()
    assert plan.context["execution"]["evaluation_options"]["selection"] == [0, 1, 2]
    assert plan.context["compatibility"] == case["compatibility"]
    # Evaluator reconstruction must use captured bytes, rather than reopen this path.
    case["query_path"].write_bytes(b"deliberately no longer a native query")
    actual = plan.new_evaluator().evaluate(case["source"], selection=[0, 1, 2])
    assert actual["status"] == "matched" and actual["fit_value"] == 1
    assert plan.query_bytes == original_bytes


def test_reopen_skips_confirmed_work_and_matches_composed_native_reference(
    prepared_run, monkeypatch
):
    case = prepared_run
    plan = case["plan"]
    calls = observe_evaluations(monkeypatch)
    with create(case) as ledger:
        outputs = resume_prepared(ledger, iter(case["entries"]), plan=plan)
        first = next(outputs)
        outputs.close()
        assert first["work_key"] == "work:0"
        assert calls == ["work:0"]
        assert len(list(ledger.results())) == 1
    with reopen(case) as ledger:
        remaining = list(resume_prepared(ledger, iter(case["entries"]), plan=plan))
        assert [row["work_key"] for row in remaining] == ["work:1"]
        assert calls == ["work:0", "work:1"]
        actual = list(ledger.results())
    execution = plan.context["execution"]
    expected = list(
        screen_prepared(
            iter(case["entries"]),
            plan.new_evaluator(),
            score_method=execution["score_method"],
            on_error=execution["on_error"],
            evaluation_options=execution["evaluation_options"],
        )
    )
    assert actual == expected == [first, *remaining]
    assert [row["occurrence_key"] for row in actual] == ["row:0", "row:1"]
    assert [row["ranking_score"] for row in actual] == [1, 1]
    json.dumps(actual, allow_nan=False)


@pytest.mark.parametrize("interruption", ["before_commit", "after_commit"])
def test_interruption_distinguishes_staged_work_from_confirmed_undelivered_result(
    prepared_run, monkeypatch, interruption
):
    case = prepared_run
    calls = observe_evaluations(monkeypatch)
    with create(case) as ledger:
        original_publish = ledger.publish

        def interrupted_publish(attempt_id):
            if interruption == "after_commit":
                original_publish(attempt_id)
            raise OSError("controlled interruption at publication boundary")

        monkeypatch.setattr(ledger, "publish", interrupted_publish)
        outputs = resume_prepared(ledger, case["entries"], plan=case["plan"])
        with pytest.raises(OSError, match="controlled interruption"):
            next(outputs)
        assert calls == ["work:0"]
        assert (ledger.committed("work:0") is None) == (interruption == "before_commit")
    with reopen(case) as ledger:
        delivered = list(resume_prepared(ledger, case["entries"], plan=case["plan"]))
        if interruption == "before_commit":
            assert calls == ["work:0", "work:0", "work:1"]
            assert [row["work_key"] for row in delivered] == ["work:0", "work:1"]
            assert len(list(ledger.attempts("work:0"))) == 2
        else:
            assert calls == ["work:0", "work:1"]
            assert [row["work_key"] for row in delivered] == ["work:1"]
            assert len(list(ledger.attempts("work:0"))) == 1
        assert [row["work_key"] for row in ledger.results()] == ["work:0", "work:1"]


def test_confirmed_native_failure_remains_unscored_and_is_not_reevaluated(
    prepared_run, monkeypatch
):
    case = prepared_run
    entries = list(case["entries"])
    entries[0] = replace(entries[0], molecular_system="invalid molecular system")
    calls = observe_evaluations(monkeypatch)
    with create(case) as ledger:
        outputs = resume_prepared(ledger, entries, plan=case["plan"])
        failure = next(outputs)
        outputs.close()
        assert failure["native_result"]["status"] == "failed"
        assert failure["native_result"]["error"]["code"] == "PHMT-E103"
        assert failure["ranking_score"] is None
    with reopen(case) as ledger:
        remaining = list(resume_prepared(ledger, entries, plan=case["plan"]))
        assert [row["work_key"] for row in remaining] == ["work:1"]
        assert calls == ["work:0", "work:1"]
        assert ledger.committed("work:0") == failure
        assert [row["ranking_score"] for row in ledger.results()] == [None, 1]


@pytest.mark.parametrize(
    "boundary",
    ["prepared_snapshot", "preparation", "features", "index", "grouping", "numerical"],
)
def test_changed_declared_boundary_is_refused_before_source_iteration(
    prepared_run, boundary
):
    case = prepared_run
    compatibility = deepcopy(case["compatibility"])
    compatibility[boundary] = {"changed_boundary": boundary}
    changed = build_changed(case, compatibility=compatibility)
    events = []
    reader = TrackedSource(case["entries"], events)
    with create(case) as ledger:
        with pytest.raises(ArgumentError):
            resume_prepared(ledger, reader, plan=changed)
        assert events == []
        assert list(ledger.results()) == []
    with pytest.raises(ValueError):
        with reopen(case, plan=changed):
            pass


@pytest.mark.parametrize("change", ["query_bytes", "selection", "frame", "on_error"])
def test_changed_saved_query_or_execution_settings_require_another_run(
    prepared_run, change
):
    case = prepared_run
    with create(case) as ledger:
        list(resume_prepared(ledger, case["entries"], plan=case["plan"]))
    if change == "query_bytes":
        case["query_path"].write_bytes(case["query_path"].read_bytes() + b"\n")
        changed = build_changed(case)
    elif change == "selection":
        changed = build_changed(case, evaluation_options={"selection": [3, 4, 5]})
    elif change == "frame":
        changed = build_changed(
            case, evaluation_options={"selection": [0, 1, 2], "structure_index": 1}
        )
    else:
        changed = build_changed(case, on_error="raise")
    with pytest.raises(ValueError):
        with reopen(case, plan=changed):
            pass
    with reopen(case) as ledger:
        assert [row["ranking_score"] for row in ledger.results()] == [1, 1]


@pytest.mark.parametrize("source_change", ["reordered", "short"])
def test_reordered_or_incomplete_source_fails_without_erasing_confirmed_prefix(
    prepared_run, monkeypatch, source_change
):
    case = prepared_run
    calls = observe_evaluations(monkeypatch)
    entries = (
        list(reversed(case["entries"]))
        if source_change == "reordered"
        else case["entries"][:1]
    )
    with create(case) as ledger:
        with pytest.raises(ArgumentError):
            list(resume_prepared(ledger, entries, plan=case["plan"]))
        if source_change == "reordered":
            assert calls == []
            assert list(ledger.results()) == []
        else:
            assert calls == ["work:0"]
            assert [row["work_key"] for row in ledger.results()] == ["work:0"]
    with reopen(case) as ledger:
        rest = list(resume_prepared(ledger, case["entries"], plan=case["plan"]))
        assert [row["work_key"] for row in rest] == (
            ["work:0", "work:1"] if source_change == "reordered" else ["work:1"]
        )
        assert [row["work_key"] for row in ledger.results()] == ["work:0", "work:1"]


def test_second_saved_query_uses_linked_run_and_preserves_original_results(
    prepared_run, tmp_path
):
    case = prepared_run
    with create(case) as ledger:
        original = list(resume_prepared(ledger, case["entries"], plan=case["plan"]))
    query = Pharmacophore()
    query.add_interaction_site(
        InteractionSite(Sphere("[10,10,10] nm", "0.02 nm"), "hydrophobicity")
    )
    second_path = tmp_path / "second-query.json"
    to_json(query, str(second_path))
    second = build_recovery_plan(
        second_path,
        screening_method="placed",
        score_method="checked_pose_coverage",
        compatibility=case["compatibility"],
        evaluation_options={"selection": [0, 1, 2]},
    )
    with create(
        case,
        path=tmp_path / "second.sqlite3",
        plan=second,
        run_id="run:second-query",
        parent_run_id="run:original",
    ) as ledger:
        actual = list(resume_prepared(ledger, case["entries"], plan=second))
        assert ledger.parent_run_id == "run:original"
        assert [row["ranking_score"] for row in actual] == [0, 0]
        assert [row["native_result"]["status"] for row in actual] == [
            "not_matched",
            "not_matched",
        ]
        assert [row["occurrence_key"] for row in actual] == ["row:0", "row:1"]
    with reopen(case) as ledger:
        assert list(ledger.results()) == original
        assert [row["ranking_score"] for row in original] == [1, 1]


def test_recovery_creation_and_early_close_leave_caller_reader_owned(prepared_run):
    case = prepared_run
    events = []
    reader = TrackedSource(case["entries"], events)
    with create(case) as ledger:
        outputs = resume_prepared(ledger, reader, plan=case["plan"])
        assert events == []
        assert next(outputs)["work_key"] == "work:0"
        assert events == ["iter", "next"]
        outputs.close()
        assert events == ["iter", "next"]
        assert next(reader).work_key == "work:1"
        assert events == ["iter", "next", "next"]


def test_runtime_mismatch_is_refused_before_pulling_source(prepared_run, monkeypatch):
    case = prepared_run
    events = []
    reader = TrackedSource(case["entries"], events)
    with create(case) as ledger:
        monkeypatch.setattr(recovery, "_runtime_identity", lambda: {"changed": True})
        with pytest.raises(ArgumentError):
            resume_prepared(ledger, reader, plan=case["plan"])
        assert events == []
        assert list(ledger.results()) == []


@pytest.mark.parametrize("case_name", ["seeded_no_fit", "partial_conformer_hit"])
def test_reopened_native_search_evidence_keeps_scores_failures_and_nested_ids(
    prepared_run, tmp_path, case_name
):
    case = prepared_run
    compatibility = deepcopy(case["compatibility"])
    compatibility["prepared_snapshot"] = {"controlled_native_case": case_name}
    if case_name == "seeded_no_fit":
        source = system("CCC", [[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0]])
        query = hydrophobic_query()
        method, score = "rigid", "seeded_hit"
        constructor = {"search_method": "seeded_hit"}
    else:
        _, query = reference()
        source = ensemble(moved_coordinates(), COORDINATES)
        method, score = "conformers", "checked_pose_coverage"
        constructor = {"max_trials": 1}
    query_path = tmp_path / f"{case_name}.json"
    to_json(query, str(query_path))
    plan = build_recovery_plan(
        query_path,
        screening_method=method,
        score_method=score,
        compatibility=compatibility,
        constructor_options=constructor,
    )
    entries = [replace(entry, molecular_system=source) for entry in case["entries"]]
    with create(case, plan=plan) as ledger:
        outcomes = resume_prepared(ledger, entries, plan=plan)
        first = next(outcomes)
        outcomes.close()
    with reopen(case, plan=plan) as ledger:
        newly_committed = list(resume_prepared(ledger, entries, plan=plan))
        assert [row["work_key"] for row in newly_committed] == ["work:1"]
        actual = list(ledger.results())
        assert actual == [first, *newly_committed]
        for outcome in actual:
            native = outcome["native_result"]
            assert native["pose_id"] == outcome["work_key"]
            if case_name == "seeded_no_fit":
                assert outcome["ranking_score"] == 0
                assert native["status"] == "not_matched"
                assert native["fit_value"] is None
                assert native["pose_evaluated"] is False
                assert native["search"]["n_fitted"] == 0
                assert native["search"]["enumeration_complete"] is True
            else:
                assert outcome["ranking_score"] == 1
                assert native["status"] == "matched"
                assert native["best_conformer_index"] == 1
                assert native["ensemble"]["complete"] is False
                assert native["ensemble"]["score_resolved"] is True
                assert [frame["status"] for frame in native["conformers"]] == [
                    "failed",
                    "matched",
                ]
                assert all(
                    frame["pose_id"] == outcome["work_key"]
                    for frame in native["conformers"]
                )
                assert native["conformers"][0]["error"]["cause_code"] == "PHMT-E105"
        json.dumps(actual, allow_nan=False)
