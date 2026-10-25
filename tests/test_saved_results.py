"""Detached result accounting has analytical oracles and no molecular work."""

import json
from copy import deepcopy

import ackredit as ack
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import _ackredit
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.validation import (
    compare_screening_results,
    summarize_screening_results,
)


def negative(index):
    return {
        "input_index": index,
        "status": "not_matched",
        "fit_value": None,
        "pose_evaluated": False,
        "search": {
            "method": "rigid_triplet_seed_hit@1",
            "identity_pose_tested": False,
            "n_fitted": 0,
            "enumeration_complete": True,
        },
        "attribution": {"original_calculation": "never credit this saved source"},
    }


def hit(index):
    result = negative(index)
    result.update(
        status="matched",
        fit_value=1.0,
        pose_evaluated=True,
        assignments=[{"site_id": "site"}],
        missing_essential_sites=[],
        excluded_volume_clashes=[],
    )
    result["search"]["n_fitted"] = 1
    return result


def arm(results, indices, *, unscored=(), method="seeded_hit"):
    return {
        "evaluations": results,
        "input_mapping": [
            {"native_input_index": r["input_index"], "input_index": i}
            for r, i in zip(results, indices, strict=True)
        ],
        "unscored": unscored,
        "score_method": method,
        "source_metadata": {
            "producer": "saved-producer",
            "attribution": {"source": True},
        },
    }


def summarize(cohort, saved, **kwargs):
    return summarize_screening_results(cohort, **saved, **kwargs)


def test_original_sparse_indices_distinct_samples_and_native_failure_are_preserved(
    monkeypatch,
):
    import molsysmt as msm

    def no_molecules(*args, **kwargs):
        pytest.fail("saved-result summaries must not access molecular systems")

    for name in ("get", "convert", "select", "extract"):
        monkeypatch.setattr(msm, name, no_molecules)
    cohort = [
        {"input_index": 7, "label": 0, "source_id": "repeated"},
        {"input_index": 40, "label": 1, "source_id": "repeated"},
        {"input_index": 12, "label": 1},
        {"input_index": 99, "label": 0},
    ]
    failure = {
        "input_index": 8,
        "status": "failed",
        "error": {"cause": "native reason"},
    }
    saved = arm(
        [hit(5), negative(2), failure],
        [40, 7, 99],
        unscored=[
            {
                "input_index": 12,
                "stage": "acquisition",
                "reason": "HTTP 404",
                "http_status": 404,
            }
        ],
    )
    before = deepcopy((cohort, saved))
    result = summarize(cohort, saved)
    assert result["n_total"] == 4 and result["n_evaluated"] == 2
    assert result["n_actives"] == result["n_inactives"] == 2
    assert result["n_native_failed"] == result["n_upstream_unscored"] == 1
    assert result["n_actives_unscored"] == result["n_inactives_unscored"] == 1
    assert result["unscored_by_stage"] == {"acquisition": 1, "native_evaluation": 1}
    assert result["evaluated_indices"] == [7, 40]
    assert result["labels"] == [0, 1] and result["scores"] == [0.0, 1.0]
    assert result["metrics"]["AUC"] == result["metrics"]["BEDROC"] == 1
    assert result["records"][0]["native_evaluation"]["pose_evaluated"] is False
    assert result["records"][3]["native_evaluation"]["error"] == failure["error"]
    assert result["missing_binary_score_AUC_sensitivity"] == {
        "pessimistic_hypothetical": 0.5,
        "optimistic_hypothetical": 1.0,
    }
    assert (cohort, saved) == before
    result["records"][0]["native_evaluation"]["attribution"].clear()
    result["source_metadata"]["attribution"].clear()
    result["records"][0]["cohort"]["source_id"] = "changed"
    assert (cohort, saved) == before


def test_ties_are_independent_of_native_and_original_order():
    cohort = [{"input_index": i, "label": i % 2} for i in range(4)]
    saved = arm([negative(i) for i in range(4)], [0, 1, 2, 3])
    first = summarize(cohort, saved, ef_fractions=(0.25,))
    saved["evaluations"].reverse()
    saved["input_mapping"].reverse()
    second = summarize(cohort[::-1], saved, ef_fractions=(0.25,))
    assert first["metrics"] == second["metrics"]
    assert first["metrics"]["AUC"] == 0.5
    assert first["metrics"]["BEDROC"] == pytest.approx(0.5)
    assert first["metrics"]["EF@25%"] == 1.0


@pytest.mark.parametrize("mode", ["empty", "upstream", "native", "active", "inactive"])
def test_empty_failed_and_single_class_metrics_are_explicit_and_json_safe(mode):
    cohort, saved = [], arm([], [])
    if mode != "empty":
        cohort = [{"input_index": 3, "label": int(mode != "inactive")}]
        if mode == "upstream":
            saved["unscored"] = [
                {"input_index": 3, "stage": "preparation", "reason": "unavailable"}
            ]
        else:
            entry = (
                {"input_index": 0, "status": "failed", "error": {"message": "failed"}}
                if mode == "native"
                else negative(0)
            )
            saved = arm([entry], [3])
    report = summarize(cohort, saved)
    assert report["metrics"]["AUC"] is report["metrics"]["BEDROC"] is None
    assert report["metrics"]["EF@10%"] == {"active": 1.0, "inactive": 0.0}.get(mode)
    json.dumps(report, allow_nan=False)


@pytest.mark.parametrize(
    "defect",
    [
        "duplicate_cohort",
        "bad_label",
        "unknown_mapping",
        "duplicate_original",
        "duplicate_native",
        "missing_mapping",
        "extra_mapping",
        "bad_index",
        "label_conflict",
        "unaccounted",
        "overlap",
        "unknown_cause",
        "duplicate_cause",
        "no_reason",
        "search_cause",
        "incomplete_negative",
        "wrong_criterion",
        "mapping_label",
    ],
)
def test_malformed_or_ambiguous_evidence_is_rejected(defect):
    cohort = [{"input_index": 4, "label": 1}, {"input_index": 8, "label": 0}]
    saved = arm(
        [hit(0)],
        [4],
        unscored=[{"input_index": 8, "stage": "acquisition", "reason": "404"}],
    )
    if defect == "duplicate_cohort":
        cohort.append(cohort[0])
    elif defect == "bad_label":
        cohort[0]["label"] = True
    elif defect == "unknown_mapping":
        saved["input_mapping"][0]["input_index"] = 999
    elif defect == "duplicate_original":
        saved["input_mapping"].append({"native_input_index": 1, "input_index": 4})
    elif defect == "duplicate_native":
        saved["evaluations"].append(saved["evaluations"][0])
    elif defect == "missing_mapping":
        saved["input_mapping"] = []
    elif defect == "extra_mapping":
        saved["input_mapping"].append({"native_input_index": 1, "input_index": 8})
    elif defect == "bad_index":
        saved["evaluations"][0]["input_index"] = True
    elif defect == "label_conflict":
        saved["evaluations"][0]["label"] = 0
    elif defect == "unaccounted":
        saved["unscored"] = []
    elif defect == "overlap":
        saved["unscored"][0]["input_index"] = 4
    elif defect == "unknown_cause":
        saved["unscored"][0]["input_index"] = 999
    elif defect == "duplicate_cause":
        saved["unscored"].append(saved["unscored"][0])
    elif defect == "no_reason":
        saved["unscored"][0]["reason"] = " "
    elif defect == "search_cause":
        saved["unscored"][0]["stage"] = "search"
    elif defect == "incomplete_negative":
        saved["evaluations"][0] = negative(0)
        saved["evaluations"][0]["search"]["enumeration_complete"] = False
    elif defect == "wrong_criterion":
        saved["evaluations"][0]["search"]["identity_pose_tested"] = True
    else:
        saved["input_mapping"][0]["label"] = 0
    with pytest.raises(ArgumentError):
        summarize(cohort, saved)


def test_pair_uses_common_indices_and_reports_undefined_disjoint_subsets():
    cohort = [{"input_index": i, "label": i % 2} for i in range(4)]

    def cause(i):
        return {"input_index": i, "stage": "preparation", "reason": "unavailable"}

    baseline = arm([hit(0), negative(1), negative(2)], [0, 1, 2], unscored=[cause(3)])
    comparison = arm([hit(8), negative(9), hit(10)], [1, 2, 3], unscored=[cause(0)])
    paired = compare_screening_results(cohort, baseline, comparison)
    common = paired["common_subset"]
    assert common["input_indices"] == [1, 2]
    assert common["metrics"]["baseline"]["AUC"] == 0.5
    assert common["metrics"]["comparison"]["AUC"] == 1.0
    assert common["delta_comparison_minus_baseline"]["AUC"] == 0.5
    assert paired["arms"]["baseline"]["n_total"] == 4
    comparison = arm([hit(0)], [3], unscored=[cause(i) for i in (0, 1, 2)])
    disjoint = compare_screening_results(cohort, baseline, comparison)
    assert disjoint["common_subset"]["input_indices"] == []
    assert set(
        disjoint["common_subset"]["delta_comparison_minus_baseline"].values()
    ) == {None}


def test_pair_refuses_different_criteria_and_non_arm_options():
    cohort = [{"input_index": 0, "label": 1}]
    baseline = arm([hit(0)], [0])
    comparison = arm([hit(0)], [0], method="checked_pose_coverage")
    with pytest.raises(ArgumentError, match="same score criterion"):
        compare_screening_results(cohort, baseline, comparison)
    baseline["unexpected"] = True
    with pytest.raises(ArgumentError):
        compare_screening_results(cohort, baseline, comparison)


def test_checked_coverage_reuses_native_metric_contract_without_binary_sensitivity():
    cohort = [
        {"input_index": i, "label": label} for i, label in enumerate([1, 0, 1, 0])
    ]
    results = [
        {"input_index": i, "status": "not_matched", "fit_value": score}
        for i, score in enumerate([0.9, 0.7, 0.5, 0.3])
    ]
    report = summarize(
        cohort,
        arm(results, list(range(4)), method="checked_pose_coverage"),
        ef_fractions=(0.5,),
    )
    assert report["score_method"] == "checked_pose_coverage@1"
    assert report["metrics"]["AUC"] == 0.75
    assert report["metrics"]["EF@50%"] == 1.0
    assert report["n_actives_found"] == report["n_inactives_found"] == 0
    assert report["missing_binary_score_AUC_sensitivity"] is None


@pytest.mark.parametrize(
    "kwargs",
    [
        {"score_method": None},
        {"score_method": "seeded_hit@1"},
        {"ef_fractions": [0]},
        {"ef_fractions": [1.1]},
        {"ef_fractions": [0.1, 0.1]},
        {"ef_fractions": [True]},
        {"bedroc_alpha": 0},
        {"bedroc_alpha": float("inf")},
        {"source_metadata": []},
    ],
)
def test_even_empty_summaries_require_valid_explicit_settings(kwargs):
    saved = arm([], [])
    saved.update(kwargs)
    with pytest.raises(ArgumentError):
        summarize([], saved)


def test_new_metrics_credit_actual_operations_without_recrediting_saved_sources():
    cohort = [{"input_index": i, "label": i} for i in range(2)]
    saved = arm([negative(0), hit(1)], [0, 1])
    before = deepcopy(saved)
    with ack.session("saved-summary application") as application:
        with ack.capture("new metrics") as capture, phmt.attribution():
            report = summarize(cohort, saved)
        assert ack.current_session() is application
    assert report["attribution"]["status"] == "captured"
    text = json.dumps(capture.attribution.to_dict())
    assert "validation.metrics.bedroc" in text
    assert "validation.saved_results.summarize_screening_results" in text
    assert "never credit this saved source" not in text
    assert "molsysmt.structure.least_rmsd_fit" not in text
    assert "pharmacophoremt.modeler.features.get_features" not in text
    assert saved == before
    assert report["source_metadata"] == saved["source_metadata"]
    with ack.capture("empty metrics") as empty_capture, phmt.attribution():
        summarize([], arm([], []))
    assert "validation.metrics.bedroc" not in json.dumps(
        empty_capture.attribution.to_dict()
    )


@pytest.mark.parametrize("provider_state", ["absent", "broken"])
def test_optional_attribution_failure_preserves_summary(monkeypatch, provider_state):
    def backend():
        if provider_state == "broken":
            raise RuntimeError("controlled provider failure")
        return None

    monkeypatch.setattr(_ackredit, "backend", backend)
    cohort = [{"input_index": i, "label": i} for i in range(2)]
    with phmt.attribution():
        report = summarize(cohort, arm([negative(0), hit(1)], [0, 1]))
    assert report["metrics"]["AUC"] == report["metrics"]["BEDROC"] == 1.0
    assert report["attribution"]["status"] != "captured"
