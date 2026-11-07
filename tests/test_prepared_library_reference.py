"""Analytical controls for the unshipped incremental prepared-input reference."""

import gc
import json
import weakref
from copy import deepcopy
from dataclasses import replace

import pytest
from argdigest import UnknownArgumentError

from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.screening import (
    ConformerScreening,
    PoseEvaluator,
    RigidPoseSearch,
)
from phmt_test_support.absence_inputs import COORDINATES, reference, system
from phmt_test_support.prepared_library_reference import PreparedInput, screen_prepared
from tests.test_conformer_screening import (
    distorted_coordinates,
    ensemble,
    moved_coordinates,
)
from tests.test_pose_evaluation import model_from_source
from tests.test_seeded_scoring import hydrophobic_query, ionic_case


class TrackedSource:
    """Expose pulls/closure independently of scientific evaluation."""

    def __init__(self, entries, events):
        self.entries = iter(entries)
        self.events = events

    def __iter__(self):
        self.events.append("iter")
        return self

    def __next__(self):
        self.events.append("next")
        return next(self.entries)

    def close(self):
        self.events.append("source.close")


@pytest.fixture
def placed():
    source = system()
    query, _ = model_from_source(source)
    return source, PoseEvaluator(query)


def prepared(source, key="work:0", *, occurrence="row:0"):
    return PreparedInput(key, "fixture:shared-record", occurrence, source)


def test_lazy_close_stops_pulling_and_releases_borrowed_source(placed):
    source, evaluator = placed
    events = []
    reader = TrackedSource([prepared(source), prepared(source, "work:1")], events)
    reader_ref = weakref.ref(reader)
    outputs = screen_prepared(
        reader,
        evaluator,
        score_method="checked_pose_coverage",
        evaluation_options={"selection": [0, 1, 2]},
    )
    assert events == []
    first = next(outputs)
    assert events == ["iter", "next"]
    assert first["native_result"]["status"] == "matched"
    json.dumps(first, allow_nan=False)
    assert "mol" not in first and "molecular_system" not in first
    del reader
    outputs.close()
    gc.collect()
    assert reader_ref() is None
    assert events == ["iter", "next"]
    with pytest.raises(StopIteration):
        next(outputs)


@pytest.mark.parametrize(
    ("overrides", "error"),
    [
        ({"evaluation_options": {"selection_typo": "all"}}, UnknownArgumentError),
        ({"evaluation_options": {"pose_id": "caller-assigned"}}, ArgumentError),
        ({"on_error": "ignore"}, ArgumentError),
        ({"score_method": "seeded_hit"}, ArgumentError),
        ({"score_method": "unknown-score"}, ArgumentError),
        ({"evaluator": object()}, ArgumentError),
        ({"evaluation_options": {"on_error": "record"}}, ArgumentError),
        ({"evaluation_options": {"skip_digestion": True}}, ArgumentError),
        ({"evaluation_options": ["selection"]}, ArgumentError),
    ],
)
def test_invalid_plan_is_rejected_before_iterating_even_empty_source(
    placed, overrides, error
):
    _, evaluator = placed
    events = []
    reader = TrackedSource([], events)
    options = {"evaluator": evaluator, "score_method": "checked_pose_coverage"}
    options.update(overrides)
    with pytest.raises(error):
        screen_prepared(reader, **options)
    assert events == []


def test_evaluation_options_mapping_is_copied_before_iteration(placed):
    source, evaluator = placed
    options = {"selection": [0, 1, 2]}
    outputs = screen_prepared(
        [prepared(source)],
        evaluator,
        score_method="checked_pose_coverage",
        evaluation_options=options,
    )
    options["selection"][:] = [3, 4, 5]
    assert next(outputs)["native_result"]["selected_atom_indices"] == [0, 1, 2]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("work_key", ""),
        ("work_key", 7),
        ("source_key", ""),
        ("source_key", None),
        ("occurrence_key", ""),
        ("occurrence_key", False),
    ],
)
def test_malformed_mapping_fails_before_scientific_evaluation(
    placed, monkeypatch, field, value
):
    source, evaluator = placed

    def forbidden(*args, **kwargs):
        raise AssertionError("malformed mapping reached native evaluation")

    monkeypatch.setattr(evaluator, "evaluate", forbidden)
    entry = replace(prepared(source), **{field: value})
    outputs = screen_prepared([entry], evaluator, score_method="checked_pose_coverage")
    with pytest.raises(ArgumentError):
        next(outputs)


def test_placed_native_batch_parity_preserves_order_and_repeated_source(placed):
    positive, evaluator = placed
    negative = system(
        coordinates=[
            [2, 1, 0],
            [2.15, 1, 0],
            [2.3, 1, 0],
            [2, 1.3, 0],
            [2.15, 1.3, 0],
            [2.3, 1.3, 0],
        ]
    )
    molecules = [negative, positive, positive]
    entries = [
        prepared(molecule, f"work:{i}", occurrence=f"row:{i}")
        for i, molecule in enumerate(molecules)
    ]
    expected = evaluator.run(molecules, selection=[0, 1, 2])
    outputs = list(
        screen_prepared(
            iter(entries),
            evaluator,
            score_method="checked_pose_coverage",
            evaluation_options={"selection": [0, 1, 2]},
        )
    )
    assert [row["work_key"] for row in outputs] == ["work:0", "work:1", "work:2"]
    assert [row["occurrence_key"] for row in outputs] == ["row:0", "row:1", "row:2"]
    assert len({row["source_key"] for row in outputs}) == 1
    assert [row["ranking_score"] for row in outputs] == [0, 1, 1]
    assert all(row["score_method"] == "checked_pose_coverage@1" for row in outputs)
    for original, actual in zip(expected, outputs, strict=True):
        normalized = dict(original, pose_id=actual["work_key"])
        normalized.pop("input_index")
        assert actual["native_result"] == normalized
        assert (
            "input_index" not in actual and "input_index" not in actual["native_result"]
        )
    json.dumps(outputs, allow_nan=False)


def test_recorded_input_failure_is_unscored_and_next_occurrence_continues(placed):
    source, evaluator = placed
    outputs = list(
        screen_prepared(
            [
                prepared(source, "valid:0"),
                prepared("invalid molecular system", "bad:1"),
                prepared(source, "valid:2"),
            ],
            evaluator,
            score_method="checked_pose_coverage",
            on_error="record",
            evaluation_options={"selection": [0, 1, 2]},
        )
    )
    assert [row["native_result"]["status"] for row in outputs] == [
        "matched",
        "failed",
        "matched",
    ]
    assert [row["ranking_score"] for row in outputs] == [1, None, 1]
    failure = outputs[1]["native_result"]
    assert failure["pose_id"] == "bad:1" and failure["fit_value"] is None
    assert failure["error"]["code"] == "PHMT-E103"
    assert failure["error"]["stage"] == "source"
    assert "bad:1" in failure["error"]["message"]
    json.dumps(outputs, allow_nan=False)


def test_raise_policy_stops_before_the_following_input(placed):
    source, evaluator = placed
    events = []
    reader = TrackedSource(
        [prepared("invalid molecular system"), prepared(source, "later")], events
    )
    outputs = screen_prepared(reader, evaluator, score_method="checked_pose_coverage")
    with pytest.raises(PoseEvaluationError):
        next(outputs)
    assert events == ["iter", "next"]


def test_source_failure_is_not_reclassified_as_a_molecular_negative(placed):
    source, evaluator = placed

    def reader():
        yield prepared(source)
        raise OSError("analytical source interruption")

    outputs = screen_prepared(
        reader(),
        evaluator,
        score_method="checked_pose_coverage",
        on_error="record",
        evaluation_options={"selection": [0, 1, 2]},
    )
    assert next(outputs)["ranking_score"] == 1
    with pytest.raises(OSError, match="source interruption"):
        next(outputs)


def test_seeded_no_fit_negative_stays_distinct_from_failure():
    source = system("CCC", [[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0]])
    evaluator = RigidPoseSearch(hydrophobic_query(), search_method="seeded_hit")
    negative, failure = list(
        screen_prepared(
            [
                prepared(source, "negative"),
                prepared("invalid molecular system", "failed"),
            ],
            evaluator,
            score_method="seeded_hit",
            on_error="record",
        )
    )
    native = negative["native_result"]
    assert native["status"] == "not_matched" and native["fit_value"] is None
    assert native["pose_evaluated"] is False
    assert native["search"]["enumeration_complete"] is True
    assert native["search"]["n_fitted"] == 0
    assert "assignments" not in native
    assert negative["ranking_score"] == 0
    assert failure["native_result"]["status"] == "failed"
    assert failure["ranking_score"] is None


def test_exhausted_search_budget_is_failed_and_unscored():
    source, query = ionic_case(extra_optional=True)
    evaluator = RigidPoseSearch(query, search_method="seeded_hit", max_trials=1)
    output = next(
        screen_prepared(
            [prepared(source, "budget:6")],
            evaluator,
            score_method="seeded_hit",
            on_error="record",
        )
    )
    native = output["native_result"]
    assert native["status"] == "failed" and native["fit_value"] is None
    assert output["ranking_score"] is None
    assert native["pose_id"] == "budget:6"
    assert native["error"]["stage"] == "search_budget"
    assert native["error"]["cause_code"] == "PHMT-E105"


def test_partial_conformer_hit_preserves_nested_identity_and_failure():
    _, query = reference()
    source = ensemble(moved_coordinates(), COORDINATES)
    evaluator = ConformerScreening(query, max_trials=1)
    output = next(
        screen_prepared(
            [prepared(source, "ensemble:7")],
            evaluator,
            score_method="checked_pose_coverage",
            on_error="record",
        )
    )
    native = output["native_result"]
    frozen = deepcopy(output)
    assert native == evaluator.evaluate(source, pose_id="ensemble:7", on_error="record")
    assert output == frozen
    assert native["status"] == "matched" and output["ranking_score"] == 1
    assert native["best_conformer_index"] == 1
    assert native["ensemble"]["complete"] is False
    assert native["ensemble"]["score_resolved"] is True
    assert [frame["status"] for frame in native["conformers"]] == ["failed", "matched"]
    assert all(frame["pose_id"] == "ensemble:7" for frame in native["conformers"])
    assert native["conformers"][0]["error"]["cause_code"] == "PHMT-E105"
    assert native["conformers"][0]["error"]["stage"] == "search_budget"
    json.dumps(output, allow_nan=False)


def test_unresolved_partial_negative_keeps_observed_witness_unscored():
    _, query = reference()
    invalid = COORDINATES.copy()
    invalid[3] = invalid[4]
    source = ensemble(distorted_coordinates(), invalid)
    output = next(
        screen_prepared(
            [prepared(source, "unresolved:8")],
            ConformerScreening(query),
            score_method="checked_pose_coverage",
            on_error="record",
        )
    )
    native = output["native_result"]
    assert native["status"] == "failed" and output["ranking_score"] is None
    assert native["fit_value"] is None and native["best_conformer_index"] is None
    assert native["ensemble"]["score_resolved"] is False
    assert native["best_observed"]["status"] == "not_matched"
    assert native["best_observed"]["pose_id"] == "unresolved:8"
    assert all(frame["pose_id"] == "unresolved:8" for frame in native["conformers"])


def test_requested_conformer_tie_order_is_preserved():
    _, query = reference()
    source = ensemble(COORDINATES, COORDINATES)
    output = next(
        screen_prepared(
            [prepared(source, "tied:9")],
            ConformerScreening(query),
            score_method="checked_pose_coverage",
            evaluation_options={"structure_indices": [1, 0]},
        )
    )
    native = output["native_result"]
    assert native["best_conformer_index"] == 1
    assert native["ensemble"]["structure_indices"] == [1, 0]
    assert [frame["conformer_index"] for frame in native["conformers"]] == [1, 0]
    assert all(frame["pose_id"] == "tied:9" for frame in native["conformers"])
