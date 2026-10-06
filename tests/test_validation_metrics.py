"""Analytical rankings and independent reference calculations."""

import numpy as np
import pytest
from rdkit.ML.Scoring import Scoring

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
