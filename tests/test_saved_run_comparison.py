"""Paired saved runs retain full arms and compare the same scored originals."""

import json
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
from copy import deepcopy
from types import SimpleNamespace

import ackredit as ack
import pytest
import test_public_run_results as run_fixtures

import pharmacophoremt as phmt
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt_results import ScreeningRunError, ScreeningRunView
from tests.test_saved_results import hit, negative
from tests.test_saved_run_analysis import saved as saved


@pytest.fixture
def paired(saved):
    right = run_fixtures.TestPublicRunResults()
    right.setUp()
    try:
        right.context = {
            "execution": {"score_method": "seeded_hit"},
            "producer": {"version": "other-original-producer"},
        }
        for row, key in zip(right.mapping, "vwxyz", strict=True):
            row.update(work_key=key, source_key="source:repeated")
        right.write_manifest()
        right.cohort = saved.cohort
        destinations = dict(v=30, w=5, x=12, y=101, z=90)
        right.input_mapping = [
            {"work_key": row["work_key"], "input_index": destinations[row["work_key"]]}
            for row in reversed(right.mapping)
        ]
        right.unscored = [
            {"input_index": 70, "stage": "preparation", "reason": "unavailable"}
        ]
        right.native = dict(
            v=negative(0),
            w=hit(0),
            x=hit(0),
            y={"input_index": 0, "status": "failed", "error": {"original": True}},
        )
        right.native["v"].pop("input_index")
        for key, native in right.native.items():
            native["pose_id"] = key
        with right.create() as store:
            for key in "yxwv":
                native = right.native[key]
                attempt = store.begin(key)
                store.stage(
                    attempt,
                    {
                        **next(row for row in right.mapping if row["work_key"] == key),
                        "native_result": deepcopy(native),
                        "ranking_score": None
                        if native["status"] == "failed"
                        else float(native["status"] == "matched"),
                        "score_method": "seeded_hit@1",
                    },
                )
                store.publish(attempt)
        yield SimpleNamespace(left=saved, right=right, cohort=saved.cohort)
    finally:
        right.doCleanups()


def descriptor(view, fixture):
    return dict(
        run_view=view,
        input_mapping=fixture.input_mapping,
        score_method="seeded_hit",
        unscored=fixture.unscored,
        source_metadata={"producer": "original", "attribution": {"saved": True}},
    )


def compare(cohort, baseline, comparison, **options):
    return getattr(phmt.validation, "compare_screening_runs")(
        cohort, baseline, comparison, ef_fractions=(0.5,), **options
    )


def open_pair(stack, paired):
    left = stack.enter_context(ScreeningRunView.open(paired.left.path))
    right = stack.enter_context(ScreeningRunView.open(paired.right.path))
    return descriptor(left, paired.left), descriptor(right, paired.right)


def test_existing_batch_comparison_does_not_accept_saved_run_descriptors(paired):
    with ExitStack() as stack:
        left, right = open_pair(stack, paired)
        with pytest.raises(ArgumentError):
            phmt.validation.compare_screening_results(paired.cohort, left, right)


def test_partial_arms_have_independent_exact_common_subset_oracles(paired, monkeypatch):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail("saved-run comparison must not access molecular systems")

    for name in ("get", "convert", "select", "extract"):
        monkeypatch.setattr(msm, name, forbidden)
    before = paired.left.directory_bytes(), paired.right.directory_bytes()
    with ExitStack() as stack:
        left, right = open_pair(stack, paired)
        result = compare(paired.cohort, left, right)
        assert (
            left["run_view"].configuration
            == result["arms"]["baseline"]["run_configuration"]
        )
        assert (
            right["run_view"].configuration
            == result["arms"]["comparison"]["run_configuration"]
        )
        assert len(list(left["run_view"].work_items())) == 5
    assert result["schema"] == "pharmacophoremt.screening_run_comparison@1"
    assert result["score_method"] == "seeded_hit@1"
    for arm, counts in [("baseline", (2, 1, 2, 1)), ("comparison", (3, 1, 1, 1))]:
        summary = result["arms"][arm]
        assert summary["schema"] == "pharmacophoremt.screening_run_summary@1"
        assert (summary["n_total"], summary["n_actives"], summary["n_inactives"]) == (
            6,
            3,
            3,
        )
        assert (
            tuple(
                summary[key]
                for key in [
                    "n_evaluated",
                    "n_native_failed",
                    "n_pending_work",
                    "n_upstream_unscored",
                ]
            )
            == counts
        )
    common = result["common_subset"]
    assert common["input_indices"] == [30, 5] and common["labels"] == [1, 0]
    assert common["scores"] == {"baseline": [1, 0], "comparison": [0, 1]}
    for arm, expected in [("baseline", 1), ("comparison", 0)]:
        metrics = common["metrics"][arm]
        assert (
            metrics["n_evaluated"],
            metrics["n_actives"],
            metrics["n_inactives"],
        ) == (2, 1, 1)
        assert metrics["AUC"] == metrics["BEDROC"] == expected
        assert metrics["EF@50%"] == 2 * expected
    assert common["delta_comparison_minus_baseline"] == {
        "AUC": -1,
        "BEDROC": -1,
        "EF@50%": -2,
    }
    assert result["arms"]["comparison"]["metrics"]["AUC"] == 0.25
    assert (
        "input_index"
        not in result["arms"]["baseline"]["records"][1]["outcome"]["native_result"]
    )
    assert (
        result["arms"]["baseline"]["records"][0]["outcome"]["native_result"][
            "input_index"
        ]
        == result["arms"]["baseline"]["records"][2]["outcome"]["native_result"][
            "input_index"
        ]
        == 0
    )
    assert (paired.left.directory_bytes(), paired.right.directory_bytes()) == before
    json.dumps(result, allow_nan=False)


@pytest.mark.parametrize("mode", ["self", "swapped"])
def test_same_snapshot_and_swapped_arms_keep_original_order(paired, mode):
    with ExitStack() as stack:
        left, right = open_pair(stack, paired)
        result = (
            compare(paired.cohort, left, left)
            if mode == "self"
            else compare(paired.cohort, right, left)
        )
        assert len(list(left["run_view"].results())) == 3
    common = result["common_subset"]
    assert common["input_indices"] == [30, 5]
    expected = (
        {"AUC": 0, "BEDROC": 0, "EF@50%": 0}
        if mode == "self"
        else {"AUC": 1, "BEDROC": 1, "EF@50%": 2}
    )
    assert common["delta_comparison_minus_baseline"] == expected


@pytest.mark.parametrize("mode", ["empty", "single_active", "single_inactive"])
def test_only_common_scored_originals_define_degenerate_statistics(paired, mode):
    destinations = {
        "empty": dict(v=90, w=12, x=70, y=101, z=30),
        "single_active": dict(v=30, w=70, x=12, y=101, z=90),
        "single_inactive": dict(v=90, w=5, x=12, y=101, z=30),
    }[mode]
    paired.right.input_mapping = [
        {"work_key": key, "input_index": index} for key, index in destinations.items()
    ]
    missing = (
        {row["input_index"] for row in paired.cohort} - set(destinations.values())
    ).pop()
    paired.right.unscored = [
        {"input_index": missing, "stage": "source", "reason": "unavailable"}
    ]
    with ExitStack() as stack:
        left, right = open_pair(stack, paired)
        result = compare(paired.cohort, left, right)
    common = result["common_subset"]
    assert (
        common["input_indices"]
        == {"empty": [], "single_active": [30], "single_inactive": [5]}[mode]
    )
    for metrics in common["metrics"].values():
        assert metrics["AUC"] is metrics["BEDROC"] is None
        assert (
            metrics["EF@50%"]
            == {"empty": None, "single_active": 1, "single_inactive": 0}[mode]
        )
    assert common["delta_comparison_minus_baseline"]["AUC"] is None
    assert common["delta_comparison_minus_baseline"]["BEDROC"] is None
    assert common["delta_comparison_minus_baseline"]["EF@50%"] == (
        None if mode == "empty" else 0
    )
    json.dumps(result, allow_nan=False)


@pytest.mark.parametrize("arm", ["baseline", "comparison"])
@pytest.mark.parametrize(
    "defect",
    [
        "not_dict",
        "missing_view",
        "missing_mapping",
        "missing_criterion",
        "batch_evaluations",
        "unknown_key",
        "wrong_view",
        "incomplete_mapping",
    ],
)
def test_strict_descriptors_and_existing_summary_admission_are_preserved(
    paired, arm, defect
):
    with ExitStack() as stack:
        left, right = open_pair(stack, paired)
        arms = dict(baseline=left, comparison=right)
        selected = dict(arms[arm])
        if defect == "not_dict":
            selected = []
        elif defect == "missing_view":
            selected.pop("run_view")
        elif defect == "missing_mapping":
            selected.pop("input_mapping")
        elif defect == "missing_criterion":
            selected.pop("score_method")
        elif defect == "batch_evaluations":
            selected["evaluations"] = []
        elif defect == "unknown_key":
            selected["choose_top"] = 1
        elif defect == "wrong_view":
            selected["run_view"] = object()
        else:
            selected["input_mapping"] = selected["input_mapping"][:-1]
        arms[arm] = selected
        with pytest.raises(ArgumentError):
            compare(paired.cohort, **arms)


@pytest.mark.parametrize("arm", ["baseline", "comparison"])
def test_closed_real_views_keep_their_existing_failure(paired, arm):
    with ExitStack() as stack:
        left, right = open_pair(stack, paired)
        arms = dict(baseline=left, comparison=right)
        arms[arm]["run_view"].close()
        with pytest.raises(ScreeningRunError):
            compare(paired.cohort, **arms)


def test_existing_wrong_thread_connection_error_is_preserved(paired):
    with ExitStack() as stack:
        left, right = open_pair(stack, paired)
        with ThreadPoolExecutor(max_workers=1) as pool:
            result = pool.submit(compare, paired.cohort, left, right)
            with pytest.raises(ScreeningRunError):
                result.result()


def test_different_explicit_criteria_are_refused_even_without_confirmed_work(paired):
    paired.right.path = paired.right.root / "empty-criterion.sqlite3"
    paired.right.context = {"execution": {"score_method": "checked_pose_coverage"}}
    with paired.right.create():
        pass
    with ExitStack() as stack:
        left, right = open_pair(stack, paired)
        right["score_method"] = "checked_pose_coverage"
        with pytest.raises(ArgumentError, match="same score criterion"):
            compare(paired.cohort, left, right)


@pytest.mark.parametrize("mode", ["empty", "all_pending"])
def test_empty_and_wholly_pending_runs_keep_undefined_paired_statistics(paired, mode):
    for fixture in [paired.left, paired.right]:
        fixture.path = fixture.root / "no-confirmations.sqlite3"
        if mode == "empty":
            fixture.mapping = []
            fixture.input_mapping = []
            fixture.unscored = []
            fixture.write_manifest()
        with fixture.create():
            pass
    cohort = [] if mode == "empty" else paired.cohort
    with ExitStack() as stack:
        left, right = open_pair(stack, paired)
        result = compare(cohort, left, right)
    assert result["common_subset"]["input_indices"] == []
    assert set(result["common_subset"]["delta_comparison_minus_baseline"].values()) == {
        None
    }
    for summary in result["arms"].values():
        assert summary["n_evaluated"] == summary["n_native_failed"] == 0
        assert summary["n_pending_work"] == (0 if mode == "empty" else 5)
    json.dumps(result, allow_nan=False)


def test_explicit_legacy_arm_retains_original_format_and_bytes(paired):
    fixture = paired.left
    fixture.path = fixture.root / "legacy-comparison.sqlite3"
    with fixture.legacy().create(
        fixture.path,
        run_id="legacy:pair",
        query_bytes=fixture.query,
        context=fixture.context,
        manifest_path=fixture.manifest,
    ) as store:
        for key in ("alpha", "beta", "gamma"):
            fixture.publish_saved(store, key)
    before = fixture.directory_bytes()
    with (
        ScreeningRunView.open(fixture.path, allow_legacy=True) as left,
        ScreeningRunView.open(paired.right.path) as right,
    ):
        result = compare(
            paired.cohort, descriptor(left, fixture), descriptor(right, paired.right)
        )
    assert (
        result["arms"]["baseline"]["run_configuration"]["format"]
        == "pharmacophoremt.reference-ledger@1"
    )
    assert result["common_subset"]["scores"] == {
        "baseline": [1, 0],
        "comparison": [0, 1],
    }
    assert fixture.directory_bytes() == before


def test_complete_output_is_detached_from_views_and_caller_descriptors(paired):
    before = paired.left.directory_bytes(), paired.right.directory_bytes()
    with ExitStack() as stack:
        left, right = open_pair(stack, paired)
        originals = deepcopy(
            (paired.cohort, paired.left.input_mapping, paired.right.input_mapping)
        )
        result = compare(paired.cohort, left, right)
        snapshot = deepcopy(result)
        result["arms"]["baseline"]["records"][1]["outcome"]["native_result"][
            "attribution"
        ]["original_calculation"] = "changed"
        result["arms"]["comparison"]["source_metadata"]["attribution"]["saved"] = False
        result["arms"]["baseline"]["run_configuration"]["context"]["execution"][
            "score_method"
        ] = "changed"
        result["common_subset"]["scores"]["baseline"].clear()
        assert compare(paired.cohort, left, right) == snapshot
        assert (
            paired.cohort,
            paired.left.input_mapping,
            paired.right.input_mapping,
        ) == originals
        assert left["source_metadata"]["attribution"]["saved"] is True
    assert (paired.left.directory_bytes(), paired.right.directory_bytes()) == before


def test_actual_optional_attribution_keeps_original_sources_and_application_session(
    paired,
):
    with ExitStack() as stack:
        left, right = open_pair(stack, paired)
        with ack.session("enclosing paired application") as application:
            with ack.capture("paired saved analysis") as capture, phmt.attribution():
                result = compare(paired.cohort, left, right)
            assert ack.current_session() is application
    assert result["attribution"]["status"] == "captured"
    recorded = json.dumps(capture.attribution.to_dict())
    assert "validation.screening_runs.compare_screening_runs" in recorded
    assert "validation.metrics.bedroc" in recorded
    assert "never credit this saved source" not in recorded
    assert (
        result["arms"]["baseline"]["records"][1]["outcome"]["native_result"][
            "attribution"
        ]
        == paired.left.native["alpha"]["attribution"]
    )


def test_unknown_keyword_is_refused_before_invalid_arguments_are_used():
    from argdigest import UnknownArgumentError

    with pytest.raises(UnknownArgumentError):
        getattr(phmt.validation, "compare_screening_runs")(
            None, None, None, choose_top=1
        )
