"""Analytical rankings and independent reference calculations."""

from itertools import combinations, permutations

import numpy as np
import pytest
from rdkit.ML.Scoring import Scoring

from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.validation.metrics import bedroc, enrichment_factor, roc_auc


@pytest.mark.parametrize(
    "labels,expected", [([1, 1, 0, 0], 1), ([1, 0, 1, 0], 0.75), ([0, 0, 1, 1], 0)]
)
def test_known_rankings(labels, expected):
    scores = [4, 3, 2, 1]
    assert (
        roc_auc(labels, scores)
        == expected
        == Scoring.CalcAUC(list(zip(scores, labels)), 1)
    )
    assert bedroc(labels, scores) == pytest.approx(
        Scoring.CalcBEDROC(list(zip(scores, labels)), 1, 20)
    )


def test_ties_are_unbiased_and_independent_of_input_order():
    labels, scores = np.array([1, 0, 1, 0]), np.ones(4)
    assert roc_auc(labels, scores) == 0.5
    assert enrichment_factor(labels, scores, 0.25) == 1
    baseline = bedroc(labels, scores)
    for order in ([3, 1, 0, 2], [0, 2, 1, 3]):
        assert roc_auc(labels[order], scores[order]) == 0.5
        assert bedroc(labels[order], scores[order]) == baseline
        assert enrichment_factor(labels[order], scores[order], 0.25) == 1


def test_boundary_ties_share_enrichment_and_bedroc_matches_expected_permutations():
    scores, labels = [3, 2, 2, 1], [1, 1, 0, 0]
    assert enrichment_factor(labels, scores, 0.5) == 1.5
    expected = np.mean(
        [
            Scoring.CalcBEDROC(list(zip(scores, order)), 1, 20)
            for order in ([1, 1, 0, 0], [1, 0, 1, 0])
        ]
    )
    assert bedroc(labels, scores) == pytest.approx(expected)


@pytest.mark.parametrize("alpha", [1e-8, 1, 20, 1000])
def test_bedroc_extremes(alpha):
    assert bedroc([1, 1, 0, 0], [4, 3, 2, 1], alpha) == pytest.approx(1)
    assert bedroc([0, 0, 1, 1], [4, 3, 2, 1], alpha) == pytest.approx(0)


@pytest.mark.parametrize(
    "labels,scores", [([], []), ([2, 0], [1, 0]), ([1], [1, 0]), ([1, 0], [np.nan, 0])]
)
@pytest.mark.parametrize("metric", [roc_auc, bedroc, enrichment_factor])
def test_invalid_rankings_raise(labels, scores, metric):
    with pytest.raises(ValueError):
        metric(labels, scores)


def test_single_class_and_fraction_contracts():
    assert np.isnan(roc_auc([1, 1], [2, 1]))
    assert np.isnan(bedroc([0, 0], [2, 1]))
    assert enrichment_factor([0, 0], [2, 1]) == 0
    for fraction in (0, 1.1, np.nan):
        with pytest.raises(ValueError):
            enrichment_factor([1, 0], [1, 0], fraction)


@pytest.mark.parametrize("n_actives", [1, 2, 4])
def test_all_small_unbalanced_rankings_agree_with_rdkit(n_actives):
    """Exercise every active-position combination, including rare actives."""
    scores = np.arange(5, 0, -1)
    for positions in combinations(range(5), n_actives):
        labels = np.zeros(5, dtype=int)
        labels[list(positions)] = 1
        reference = list(zip(scores.tolist(), labels.tolist(), strict=True))
        assert roc_auc(labels, scores) == pytest.approx(Scoring.CalcAUC(reference, 1))
        for alpha in (1, 20, 80):
            assert bedroc(labels, scores, alpha) == pytest.approx(
                Scoring.CalcBEDROC(reference, 1, alpha), abs=1e-12
            )
        expected = Scoring.CalcEnrichment(reference, 1, [0.2, 0.4, 0.8])
        for fraction, value in zip((0.2, 0.4, 0.8), expected, strict=True):
            assert enrichment_factor(labels, scores, fraction) == pytest.approx(value)


def test_three_way_boundary_tie_matches_all_reference_tie_resolutions():
    labels, scores = np.array([1, 0, 1, 0, 0]), np.array([3, 2, 2, 2, 1])
    reference_rankings = [[1, 1, 0, 0, 0], [1, 0, 1, 0, 0], [1, 0, 0, 1, 0]]
    expected_bedroc = np.mean(
        [
            Scoring.CalcBEDROC(list(zip(scores.tolist(), order, strict=True)), 1, 20)
            for order in reference_rankings
        ]
    )
    # Average reference ranks over all placements of the tied active. Input
    # permutation must never select one favorable tie resolution.
    for order in permutations(range(5)):
        order = list(order)
        assert roc_auc(labels[order], scores[order]) == pytest.approx(5 / 6)
        assert bedroc(labels[order], scores[order]) == pytest.approx(expected_bedroc)
        assert enrichment_factor(labels[order], scores[order], 0.4) == pytest.approx(
            5 / 3
        )


@pytest.mark.parametrize("value", [0, -1, np.nan, np.inf, True, "invalid"])
def test_invalid_metric_parameters_retain_argument_diagnostics(value):
    for metric, parameter in ((bedroc, "alpha"), (enrichment_factor, "fraction")):
        with pytest.raises(ArgumentError) as error:
            metric([1, 0], [1, 0], **{parameter: value})
        assert error.value.extra["argument"] == parameter
        assert error.value.extra["reason"]


@pytest.mark.parametrize("metric", [roc_auc, bedroc, enrichment_factor])
@pytest.mark.parametrize(
    "labels,scores",
    [
        ([[1, 0]], [1, 0]),
        ([1, 0], [[1, 0]]),
        ([1, np.nan], [1, 0]),
        ([1, 0], [np.inf, 0]),
    ],
)
def test_invalid_ranking_shapes_and_nonfinite_values_have_diagnostics(
    metric, labels, scores
):
    with pytest.raises(ArgumentError) as error:
        metric(labels, scores)
    assert error.value.extra["argument"] in {"labels", "scores", "labels/scores"}
    assert error.value.extra["reason"]
