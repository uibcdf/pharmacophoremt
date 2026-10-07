"""Retrospective accounting protects input identity and failure semantics."""

import numpy as np
import pytest

from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
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


def test_failures_in_both_classes_preserve_positions_and_evaluated_denominators():
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
    report = RetrospectiveValidator(model, evaluator=PoseEvaluator(model)).run(
        iter(["invalid active", source, source]),
        iter([negative, "invalid decoy"]),
        selection=[0, 1, 2],
        on_error="record",
        ef_fractions=(1 / 3,),
    )
    assert report["n_actives"] == 3 and report["n_decoys"] == 2
    assert report["n_evaluated"] == 3 and report["n_failed"] == 2
    assert report["n_actives_evaluated"] == report["n_actives_found"] == 2
    assert report["n_decoys_evaluated"] == 1
    assert report["evaluated_indices"].tolist() == [1, 2, 3]
    assert report["scores"].tolist() == [1, 1, 0]
    assert report["labels"].tolist() == [1, 1, 0]
    assert [row["input_index"] for row in report["failures"]] == [0, 4]
    assert all(row["fit_value"] is None and row["error"] for row in report["failures"])
    assert report["AUC"] == report["BEDROC"] == 1
    assert report["EF@33.3333%"] == pytest.approx(1.5)


def test_full_positive_coverage_with_steric_veto_is_not_an_accepted_active():
    source = system()
    model, _ = model_from_source(source)
    model.add_interaction_site(
        InteractionSite(Sphere("[0,0,0] nm", "0.05 nm"), "excluded volume")
    )
    report = RetrospectiveValidator(model, evaluator=PoseEvaluator(model)).run(
        [source],
        [source],
        selection=[0, 1, 2],
    )
    assert report["scores"].tolist() == [1, 1]
    assert report["n_actives_found"] == report["n_failed"] == 0
    assert report["n_actives_evaluated"] == report["n_decoys_evaluated"] == 1
    assert report["AUC"] == 0.5
    assert all(
        row["status"] == "not_matched" and row["excluded_volume_clashes"]
        for row in report["evaluations"]
    )


def test_legacy_conversion_failure_is_excluded_without_losing_repeated_inputs():
    """Exercise actual conversion/accounting on a prepared analytical fixture."""
    source = system()
    model, _ = model_from_source(source)
    validator = RetrospectiveValidator(model)
    with pytest.raises(PoseEvaluationError):
        validator.run([source], ["invalid legacy system"])
    report = validator.run(
        iter([source, source]), iter(["invalid legacy system"]), on_error="record"
    )
    assert report["scores"].tolist() == [1, 1]
    assert report["evaluated_indices"].tolist() == [0, 1]
    assert (
        report["n_actives"]
        == report["n_actives_evaluated"]
        == report["n_actives_found"]
        == 2
    )
    assert report["n_decoys"] == report["n_failed"] == 1
    assert report["n_decoys_evaluated"] == 0
    assert np.isnan(report["AUC"]) and np.isnan(report["BEDROC"])
    assert report["failures"][0]["input_index"] == 2
    assert report["failures"][0]["fit_value"] is None
    assert report["failures"][0]["error"]["stage"] == "conversion"


@pytest.mark.parametrize(
    "actives,decoys", [([], []), (["invalid active"], ["invalid decoy"])]
)
def test_empty_or_entirely_failed_batches_have_no_manufactured_metrics(actives, decoys):
    source = system()
    model, _ = model_from_source(source)
    validator = RetrospectiveValidator(model, evaluator=PoseEvaluator(model))
    with pytest.raises(ArgumentError) as error:
        validator.run(actives, decoys, selection=[0, 1, 2], on_error="record")
    assert error.value.extra["argument"] == "dataset"
    assert error.value.extra["reason"] == "no successfully evaluated inputs"
