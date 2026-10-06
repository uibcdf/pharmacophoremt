"""Ranking metrics with unbiased ties. Higher dimensionless scores rank first."""

import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._ackredit import attributed, credit_criterion
from pharmacophoremt._private.smonitor.exceptions import ArgumentError


def _ranking(labels, scores):
    try:
        labels, scores = np.asarray(labels), np.asarray(scores, dtype=float)
    except (TypeError, ValueError) as error:
        raise ArgumentError(
            argument="labels/scores", reason="expected numerical arrays"
        ) from error
    if (
        labels.ndim != 1
        or scores.ndim != 1
        or len(labels) != len(scores)
        or not len(labels)
    ):
        raise ArgumentError(
            argument="labels/scores", reason="expected nonempty, equally sized vectors"
        )
    if not np.all(np.isin(labels, [0, 1])) or not np.all(np.isfinite(scores)):
        raise ArgumentError(
            argument="labels/scores", reason="labels must be 0 or 1 and scores finite"
        )
    return labels.astype(int), scores


def _positive(value, argument, maximum=None):
    if isinstance(value, (bool, np.bool_)):
        raise ArgumentError(argument=argument, reason="expected a positive real number")
    try:
        value = float(value)
    except (TypeError, ValueError) as error:
        raise ArgumentError(
            argument=argument, reason="expected a positive real number"
        ) from error
    if (
        not np.isfinite(value)
        or value <= 0
        or (maximum is not None and value > maximum)
    ):
        raise ArgumentError(
            argument=argument,
            reason=f"expected a finite value in (0, {maximum or 'infinity'}]",
        )
    return value


@signal(tags=["validation", "metric", "ef"])
@arg_digest()
@attributed("numpy")
def enrichment_factor(labels, scores, fraction=0.01, *, skip_digestion=False):
    """Return EF in ceil(fraction * N) entries; boundary ties share credit.

    Empty inputs are invalid. A dataset with no actives returns zero.
    """
    labels, scores = _ranking(labels, scores)
    fraction = _positive(fraction, "fraction", maximum=1)
    active = int(labels.sum())
    if not active:
        return 0.0
    top = max(1, int(np.ceil(fraction * len(labels))))
    boundary = np.sort(scores)[-top]
    above, tied = scores > boundary, scores == boundary
    hits = labels[above].sum() + (top - above.sum()) * labels[tied].mean()
    return float((hits / top) / (active / len(labels)))


@signal(tags=["validation", "metric", "auc"])
@arg_digest()
@attributed("numpy")
def roc_auc(labels, scores, *, skip_digestion=False):
    """Return P(active > decoy) + half P(tie), or NaN for a single class."""
    labels, scores = _ranking(labels, scores)
    positives = int(labels.sum())
    negatives = len(labels) - positives
    if not positives or not negatives:
        return float("nan")
    order = np.argsort(scores, kind="stable")
    ranked_scores, ranked_labels = scores[order], labels[order]
    starts = np.r_[0, np.flatnonzero(np.diff(ranked_scores)) + 1]
    ends = np.r_[starts[1:], len(labels)]
    below, wins = 0, 0.0
    for start, end in zip(starts, ends):
        active = int(ranked_labels[start:end].sum())
        decoy = int(end - start - active)
        wins += active * (below + 0.5 * decoy)
        below += decoy
    return float(wins / (positives * negatives))


@signal(tags=["validation", "metric", "bedroc"])
@arg_digest()
@attributed("numpy")
def bedroc(labels, scores, alpha=20.0, *, skip_digestion=False):
    """Return BEDROC between the worst (0) and best (1) possible rankings.

    Truchon and Bayly (2007), DOI 10.1021/ci600426e. With fixed class counts,
    normalized exponential rank sums equal the normalized RIE expression.
    Ties average positional weights. A single-class dataset returns NaN.
    """
    labels, scores = _ranking(labels, scores)
    alpha = _positive(alpha, "alpha")
    n, active = len(labels), int(labels.sum())
    if not active or active == n:
        return float("nan")
    order = np.argsort(-scores, kind="stable")
    ranked_scores, ranked_labels = scores[order], labels[order]
    # The common rank-one exponent and additive offset cancel. expm1
    # preserves small-alpha differences without underflowing the first rank.
    weights = np.expm1(-alpha * (np.arange(n, dtype=float) / n))
    starts = np.r_[0, np.flatnonzero(np.diff(ranked_scores)) + 1]
    ends = np.r_[starts[1:], n]
    observed = sum(
        float(ranked_labels[a:b].sum()) * weights[a:b].mean()
        for a, b in zip(starts, ends)
    )
    best, worst = float(weights[:active].sum()), float(weights[-active:].sum())
    result = float(np.clip((observed - worst) / (best - worst), 0, 1))
    credit_criterion("bedroc", "pharmacophoremt.validation.metrics.bedroc")
    return result
