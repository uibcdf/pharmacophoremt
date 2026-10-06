"""Retrospective accounting protects input identity and failure semantics."""

import numpy as np
import pytest

from pharmacophoremt._private.smonitor.exceptions import PoseEvaluationError
from pharmacophoremt.screening import PoseEvaluator
from pharmacophoremt.validation.retrospective import RetrospectiveValidator
from tests.test_pose_evaluation import model_from_source, system


def test_placed_pose_retrospective_has_perfect_known_ranking_and_generator_inputs():
    source = system()
    model, _ = model_from_source(source)
    negative = system(
        coordinates=np.array(
            [
                [0, 0, 0],
                [0.15, 0, 0],
                [0.3, 0, 0],
                [0, 0.3, 0],
                [0.15, 0.3, 0],
                [0.3, 0.3, 0],
            ]
        )
        + 2
    )
    validator = RetrospectiveValidator(model, evaluator=PoseEvaluator(model))
    report = validator.run(
        iter([source, source]), iter([negative]), selection=[0, 1, 2]
    )
    assert report["scores"].tolist() == [1, 1, 0]
    assert report["evaluated_indices"].tolist() == [0, 1, 2]
    assert report["AUC"] == report["BEDROC"] == 1
    assert report["n_actives_found"] == report["n_actives_evaluated"] == 2


def test_failure_requires_explicit_exclusion_and_does_not_become_a_decoy():
    source = system()
    model, _ = model_from_source(source)
    validator = RetrospectiveValidator(model, evaluator=PoseEvaluator(model))
    with pytest.raises(PoseEvaluationError):
        validator.run([source], ["invalid system"], selection=[0, 1, 2])
    report = validator.run(
        [source], ["invalid system"], selection=[0, 1, 2], on_error="record"
    )
    assert report["n_decoys"] == report["n_failed"] == 1
    assert report["n_decoys_evaluated"] == 0
    assert report["scores"].tolist() == [1]
    assert np.isnan(report["AUC"])
    assert report["failures"][0]["input_index"] == 1


def test_legacy_accounting_uses_indices_and_configured_essential_threshold(monkeypatch):
    from pharmacophoremt.screening.virtual_screening import VirtualScreening

    source = system()
    model, _ = model_from_source(source)

    def evaluate_fixture(self, database):
        # Bounded adapter fixture: ranking chemistry is tested in the real route.
        assert len(database) == 3
        self.evaluations = [
            dict(
                input_index=0,
                status="matched",
                fit_value=0.8,
                essential_match_ratio=0.5,
            ),
            dict(
                input_index=1, status="matched", fit_value=0.9, essential_match_ratio=1
            ),
            dict(
                input_index=2,
                status="not_matched",
                fit_value=0,
                essential_match_ratio=0,
            ),
        ]
        return []

    monkeypatch.setattr(VirtualScreening, "run", evaluate_fixture)
    report = RetrospectiveValidator(model, min_match_ratio=0.75).run(
        [source, source], [source]
    )
    assert report["scores"].tolist() == [0.8, 0.9, 0]
    assert report["n_actives_found"] == 1
