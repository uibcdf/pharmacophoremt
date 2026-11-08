"""Analytical cohort summaries preserve original saved-work identity and evidence."""

import json
from copy import deepcopy

import ackredit as ack
import pytest
import test_public_run_results as run_fixtures

import pharmacophoremt as phmt
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.validation import summarize_screening_results
from pharmacophoremt_results import ScreeningRunError, ScreeningRunView
from tests.test_saved_results import hit, negative


@pytest.fixture
def saved():
    f = run_fixtures.TestPublicRunResults()
    f.setUp()
    f.context = {"execution": {"score_method": "seeded_hit"}}
    native = {
        "alpha": hit(0),
        "beta": negative(0),
        "gamma": {
            "input_index": 0,
            "status": "failed",
            "fit_value": None,
            "error": {"stage": "source", "message": "original failure"},
        },
        "delta": hit(0),
        "epsilon": negative(0),
    }
    native["alpha"].pop("input_index")
    for key, value in native.items():
        value["pose_id"] = key

    def outcome(key):
        status = native[key]["status"]
        return {
            **next(row for row in f.mapping if row["work_key"] == key),
            "native_result": deepcopy(native[key]),
            "ranking_score": None if status == "failed" else float(status == "matched"),
            "score_method": "seeded_hit@1",
        }

    def publish(store, key):
        attempt = store.begin(key)
        store.stage(attempt, outcome(key))
        store.publish(attempt)

    with f.create() as store:
        for key in ("beta", "gamma", "alpha"):
            publish(store, key)
        pending = store.begin("delta")
        store.stage(pending, outcome("delta"))
    f.publish_saved = publish
    f.native = native
    f.cohort = [
        {"input_index": 90, "label": 0},
        {"input_index": 30, "label": 1, "source_id": "repeated"},
        {"input_index": 5, "label": 0, "source_id": "repeated"},
        {"input_index": 12, "label": 1},
        {"input_index": 70, "label": 0},
        {"input_index": 101, "label": 1},
    ]
    indices = dict(alpha=30, beta=5, gamma=90, delta=12, epsilon=70)
    f.input_mapping = [
        {"work_key": row["work_key"], "input_index": indices[row["work_key"]]}
        for row in reversed(f.mapping)
    ]
    f.unscored = [{"input_index": 101, "stage": "acquisition", "reason": "unavailable"}]
    try:
        yield f
    finally:
        f.doCleanups()


def summarize(view, f, **options):
    settings = dict(
        input_mapping=f.input_mapping,
        score_method="seeded_hit",
        unscored=f.unscored,
        ef_fractions=(0.5,),
        source_metadata={"producer": "original", "attribution": {"saved": True}},
    )
    settings.update(options)
    return getattr(phmt.validation, "summarize_screening_run")(
        view, f.cohort, **settings
    )


def test_existing_batch_summary_cannot_admit_native_single_input_records(saved):
    with pytest.raises(ArgumentError):
        summarize_screening_results(
            [{"input_index": 30, "label": 1}],
            [saved.native["alpha"]],
            input_mapping=[{"native_input_index": 0, "input_index": 30}],
            score_method="seeded_hit",
        )


def test_tiny_alpha_saved_summary_preserves_finite_metrics_and_missing_denominators(
    saved,
):
    with ScreeningRunView.open(saved.path) as view:
        ordinary = summarize(view, saved)
        observed = summarize(view, saved, bedroc_alpha=5e-324)
    assert observed["metrics"]["BEDROC"] == 1.0
    assert observed["metric_settings"]["bedroc_alpha"] == 5e-324
    for key in (
        "records",
        "n_total",
        "n_evaluated",
        "n_unscored",
        "n_native_failed",
        "n_pending_work",
        "n_upstream_unscored",
        "run_configuration",
    ):
        assert observed[key] == ordinary[key]
    assert "input_index" not in saved.native["alpha"]


def test_partial_run_has_exact_independent_counts_scores_metrics_and_identities(
    saved, monkeypatch
):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail("saved-run analysis must not access molecular systems")

    for name in ("get", "convert", "select", "extract"):
        monkeypatch.setattr(msm, name, forbidden)
    before = saved.directory_bytes()
    original_inputs = deepcopy((saved.cohort, saved.input_mapping, saved.unscored))
    with ScreeningRunView.open(saved.path) as view:
        original = {row["work_key"]: row for row in view.results()}
        configuration = view.configuration
        result = summarize(view, saved)
    assert result["schema"] == "pharmacophoremt.screening_run_summary@1"
    assert result["run_configuration"] == configuration
    assert (result["n_total"], result["n_actives"], result["n_inactives"]) == (6, 3, 3)
    assert (
        result["n_evaluated"],
        result["n_native_failed"],
        result["n_pending_work"],
        result["n_upstream_unscored"],
        result["n_unscored"],
    ) == (2, 1, 2, 1, 4)
    assert result["unscored_by_stage"] == {
        "native_evaluation": 1,
        "screening_run": 2,
        "acquisition": 1,
    }
    assert result["evaluated_indices"] == [30, 5]
    assert result["labels"] == [1, 0] and result["scores"] == [1, 0]
    assert result["metrics"]["AUC"] == result["metrics"]["BEDROC"] == 1
    assert result["metrics"]["EF@50%"] == 2
    assert result["input_mapping"] == saved.input_mapping
    rows = result["records"]
    assert [row["input_index"] for row in rows] == [90, 30, 5, 12, 70, 101]
    assert rows[1]["outcome"] == original["alpha"]
    assert "input_index" not in rows[1]["outcome"]["native_result"]
    assert (
        rows[0]["outcome"]["native_result"]["input_index"]
        == rows[2]["outcome"]["native_result"]["input_index"]
        == 0
    )
    assert rows[1]["work_item"]["manifest_ordinal"] == 0
    assert rows[3]["outcome"] is rows[4]["outcome"] is rows[5]["outcome"] is None
    assert rows[5]["work_item"] is None
    assert all("native_evaluation" not in row for row in rows)
    assert saved.directory_bytes() == before
    assert (saved.cohort, saved.input_mapping, saved.unscored) == original_inputs
    json.dumps(result, allow_nan=False)


def test_complete_run_keeps_failures_separate_and_uses_all_scored_work(saved):
    with saved.reopen() as store:
        saved.publish_saved(store, "delta")
        saved.publish_saved(store, "epsilon")
    with ScreeningRunView.open(saved.path) as view:
        result = summarize(view, saved)
    assert result["n_evaluated"] == 4 and result["n_pending_work"] == 0
    assert result["n_native_failed"] == result["n_upstream_unscored"] == 1
    assert result["metrics"]["AUC"] == result["metrics"]["BEDROC"] == 1
    assert result["metrics"]["EF@50%"] == 2


@pytest.mark.parametrize(
    "defect",
    [
        "duplicate_work",
        "duplicate_destination",
        "unknown_work",
        "unknown_original",
        "missing_work",
        "extra_key",
        "bool_index",
        "label_missing",
        "label_bool",
        "cohort_duplicate",
        "cause_overlap",
        "cause_missing",
        "cause_reserved",
    ],
)
def test_ambiguous_or_incomplete_mapping_labels_and_causes_are_refused(saved, defect):
    if defect == "duplicate_work":
        saved.input_mapping.append(saved.input_mapping[0])
    elif defect == "duplicate_destination":
        saved.input_mapping[0]["input_index"] = saved.input_mapping[1]["input_index"]
    elif defect == "unknown_work":
        saved.input_mapping[0]["work_key"] = "unknown"
    elif defect == "unknown_original":
        saved.input_mapping[0]["input_index"] = 999
    elif defect == "missing_work":
        saved.input_mapping.pop()
    elif defect == "extra_key":
        saved.input_mapping[0]["native_input_index"] = 0
    elif defect == "bool_index":
        saved.input_mapping[0]["input_index"] = True
    elif defect == "label_missing":
        saved.cohort[0].pop("label")
    elif defect == "label_bool":
        saved.cohort[0]["label"] = True
    elif defect == "cohort_duplicate":
        saved.cohort.append(saved.cohort[0])
    elif defect == "cause_overlap":
        saved.unscored[0]["input_index"] = 30
    elif defect == "cause_missing":
        saved.unscored.clear()
    else:
        saved.unscored[0]["stage"] = "screening_run"
    with ScreeningRunView.open(saved.path) as view:
        with pytest.raises(ArgumentError):
            summarize(view, saved)


@pytest.mark.parametrize(
    "settings",
    [
        {"score_method": None},
        {"score_method": "seeded_hit@1"},
        {"score_method": "checked_pose_coverage"},
        {"ef_fractions": [0.5, 0.5]},
        {"bedroc_alpha": 0},
    ],
)
def test_invalid_or_different_explicit_criteria_and_metric_settings_are_refused(
    saved, settings
):
    with ScreeningRunView.open(saved.path) as view:
        with pytest.raises(ArgumentError):
            summarize(view, saved, **settings)


def test_result_is_deeply_detached_and_original_view_remains_usable(saved):
    before = saved.directory_bytes()
    with ScreeningRunView.open(saved.path) as view:
        expected = summarize(view, saved)
        changed = summarize(view, saved)
        changed["records"][1]["outcome"]["native_result"].clear()
        changed["records"][1]["cohort"].clear()
        changed["run_configuration"].clear()
        changed["source_metadata"].clear()
        assert summarize(view, saved) == expected
        assert view.progress()["counts"]["committed_work"] == 3
    assert saved.directory_bytes() == before


def test_closed_view_is_refused_and_writer_is_not_admitted(saved):
    with ScreeningRunView.open(saved.path) as view:
        pass
    with pytest.raises(ScreeningRunError):
        summarize(view, saved)
    with saved.reopen() as writer:
        with pytest.raises(ArgumentError):
            summarize(writer, saved)


def test_unknown_keyword_is_refused_by_the_public_argdigest_contract():
    from argdigest import UnknownArgumentError

    endpoint = getattr(phmt.validation, "summarize_screening_run")
    with pytest.raises(UnknownArgumentError):
        endpoint(None, None, input_mapping=None, score_method=None, work_mapping=[])


def test_new_metric_attribution_keeps_original_source_credit_separate(saved):
    with ack.capture("saved run analysis") as capture, phmt.attribution():
        with ScreeningRunView.open(saved.path) as view:
            result = summarize(view, saved)
    assert result["attribution"]["status"] == "captured"
    recorded = json.dumps(capture.attribution.to_dict())
    assert "validation.screening_runs.summarize_screening_run" in recorded
    assert "validation.metrics.bedroc" in recorded
    assert "never credit this saved source" not in recorded
    assert (
        result["records"][1]["outcome"]["native_result"]["attribution"]
        == saved.native["alpha"]["attribution"]
    )


@pytest.mark.parametrize("mode", ["empty", "all_pending", "single_class", "no_actives"])
def test_empty_pending_and_single_class_oracles_are_explicit(saved, mode):
    saved.path = saved.root / "variant.sqlite3"
    if mode == "empty":
        saved.mapping = []
        saved.cohort, saved.input_mapping, saved.unscored = [], [], []
    elif mode in {"single_class", "no_actives"}:
        saved.mapping = saved.mapping[:1]
        saved.cohort = [{"input_index": 7, "label": int(mode == "single_class")}]
        saved.input_mapping = [{"work_key": "alpha", "input_index": 7}]
        saved.unscored = []
    saved.write_manifest()
    with saved.create() as store:
        if mode in {"single_class", "no_actives"}:
            saved.publish_saved(store, "alpha")
    with ScreeningRunView.open(saved.path) as view:
        result = summarize(view, saved)
    assert result["n_native_failed"] == 0
    if mode == "empty":
        assert (
            result["n_total"] == result["n_evaluated"] == result["n_pending_work"] == 0
        )
        assert set(result["metrics"].values()) <= {None, 0}
        assert result["records"] == []
    elif mode == "all_pending":
        assert result["n_total"] == 6 and result["n_pending_work"] == 5
        assert result["n_evaluated"] == 0 and result["n_upstream_unscored"] == 1
        assert result["metrics"]["AUC"] is result["metrics"]["BEDROC"] is None
        assert result["metrics"]["EF@50%"] is None
    else:
        assert result["n_evaluated"] == 1 and result["n_pending_work"] == 0
        assert result["metrics"]["AUC"] is result["metrics"]["BEDROC"] is None
        assert result["metrics"]["EF@50%"] == int(mode == "single_class")
    json.dumps(result, allow_nan=False)


def test_explicit_legacy_view_keeps_native_evidence_and_bytes(saved):
    saved.path = saved.root / "legacy.sqlite3"
    with saved.legacy().create(
        saved.path,
        run_id="legacy:run",
        query_bytes=saved.query,
        context=saved.context,
        manifest_path=saved.manifest,
    ) as store:
        for key in ("alpha", "beta", "gamma"):
            saved.publish_saved(store, key)
    before = saved.directory_bytes()
    with ScreeningRunView.open(saved.path, allow_legacy=True) as view:
        result = summarize(view, saved)
    assert result["run_configuration"]["format"] == "pharmacophoremt.reference-ledger@1"
    assert result["scores"] == [1, 0] and result["n_pending_work"] == 2
    assert result["records"][1]["outcome"]["native_result"] == saved.native["alpha"]
    assert saved.directory_bytes() == before


def test_consistent_store_with_conflicting_native_score_is_refused_by_scientific_analysis(
    saved,
):
    saved.path = saved.root / "conflicting-score.sqlite3"
    saved.context = {"execution": {"score_method": "checked_pose_coverage"}}
    with saved.create() as store:
        attempt = store.begin("alpha")
        store.stage(
            attempt,
            {
                **saved.mapping[0],
                "native_result": {
                    "status": "matched",
                    "fit_value": 0.75,
                    "pose_id": "alpha",
                },
                "ranking_score": 0.25,
                "score_method": "checked_pose_coverage@1",
            },
        )
        store.publish(attempt)
    before = saved.directory_bytes()
    with ScreeningRunView.open(saved.path) as view:
        assert next(view.results())["ranking_score"] == 0.25
        with pytest.raises(ArgumentError, match="stored score"):
            summarize(view, saved, score_method="checked_pose_coverage")
    assert saved.directory_bytes() == before


def test_native_label_conflict_is_refused_without_rewriting_evidence(saved):
    saved.path = saved.root / "conflicting-label.sqlite3"
    saved.native["alpha"]["label"] = 0
    with saved.create() as store:
        saved.publish_saved(store, "alpha")
    before = saved.directory_bytes()
    with ScreeningRunView.open(saved.path) as view:
        with pytest.raises(ArgumentError, match="labels disagree"):
            summarize(view, saved)
    assert saved.directory_bytes() == before


def test_malformed_execution_declaration_has_structured_refusal_even_for_empty_run(
    saved,
):
    saved.path = saved.root / "invalid-execution.sqlite3"
    saved.mapping = []
    saved.write_manifest()
    saved.context = {"execution": []}
    with saved.create():
        pass
    with ScreeningRunView.open(saved.path) as view:
        with pytest.raises(ArgumentError):
            getattr(phmt.validation, "summarize_screening_run")(
                view, [], input_mapping=[], score_method="seeded_hit"
            )
