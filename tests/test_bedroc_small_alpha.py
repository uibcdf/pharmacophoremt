"""Independent high-precision controls for the small-alpha BEDROC limit."""

from decimal import Decimal, localcontext
from itertools import permutations

import numpy as np
import pytest

from pharmacophoremt.validation.metrics import bedroc


def _decimal_tie_average(labels, scores, alpha):
    # Enumerate valid rank orders and evaluate the defining exponential sum.
    # No production metric, tie grouping or rank-sum implementation is reused.
    with localcontext() as context:
        context.prec = 400
        n, active = len(labels), sum(labels)
        value = Decimal.from_float(float(alpha))
        weights = [(-value * Decimal(rank) / n).exp() for rank in range(1, n + 1)]
        best, worst = sum(weights[:active]), sum(weights[-active:])
        results = []
        for order in permutations(range(n)):
            if all(scores[a] >= scores[b] for a, b in zip(order, order[1:])):
                observed = sum(
                    weights[rank] for rank, i in enumerate(order) if labels[i]
                )
                results.append((observed - worst) / (best - worst))
        return float(sum(results) / len(results))


@pytest.mark.parametrize(
    "alpha",
    [
        5e-324,
        1e-320,
        1e-300,
        1e-50,
        np.finfo(float).eps / 2,
        np.finfo(float).eps,
        np.finfo(float).eps * 2,
        1e-8,
    ],
)
@pytest.mark.parametrize(
    "labels,scores",
    [([1, 0], [0, 0]), ([1, 0, 1, 0], [2, 2, 1, 1]), ([0, 1, 0, 0], [4, 3, 2, 1])],
)
def test_small_alpha_matches_independent_decimal_tie_average(labels, scores, alpha):
    expected = _decimal_tie_average(labels, scores, alpha)
    with np.errstate(divide="raise", invalid="raise", under="ignore"):
        actual = bedroc(labels, scores, alpha)
    assert np.isfinite(actual)
    assert actual == pytest.approx(expected, abs=2e-15, rel=0)


def test_subnormal_alpha_preserves_unbiased_ties_and_input_permutations():
    labels, scores = np.array([1, 0, 1, 0]), np.ones(4)
    for order in permutations(range(4)):
        order = list(order)
        assert bedroc(labels[order], scores[order], 5e-324) == 0.5


@pytest.mark.parametrize("labels", [[0, 0], [1, 1]])
def test_small_alpha_single_class_remains_undefined(labels):
    assert np.isnan(bedroc(labels, [1, 0], 5e-324))


def test_small_alpha_retains_actual_criterion_and_application_session():
    import json

    import ackredit as ack

    import pharmacophoremt as phmt

    with ack.session("small-alpha-application") as application:
        with phmt.attribution():
            assert bedroc([1, 0], [0, 0], 5e-324) == 0.5
        assert ack.current_session() is application
        record = ack.get_attribution().to_dict()
        assert "10.1021/ci600426e" in json.dumps(record)
        assert any(
            "scientific_criterion" in use.get("roles", []) for use in record["uses"]
        )
        assert "pharmacophoremt.validation.metrics.roc_auc" in json.dumps(record)
