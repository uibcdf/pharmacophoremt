"""
Statistical metrics for pharmacophore validation.

All functions expect:
  labels  : array-like of int/bool (1 = active, 0 = decoy), ordered by
             descending score (first element = top-ranked molecule).
  scores  : array-like of float, same length as labels.

References
----------
Truchon, J.-F.; Bayly, C. I. J. Chem. Inf. Model. 2007, 47, 488-508.
    (BEDROC derivation)
"""

import numpy as np


def enrichment_factor(labels, scores, fraction=0.01):
    """Enrichment Factor (EF) at a given database fraction.

    EF = (hits in top-fraction / compounds in top-fraction) /
         (total actives / total compounds)

    Parameters
    ----------
    labels : array-like of int
        Activity labels (1 = active, 0 = decoy), in *any* order.
    scores : array-like of float
        Screening scores, same order as labels. Higher = better ranked.
    fraction : float
        Database fraction to evaluate (e.g. 0.01 for EF@1%).

    Returns
    -------
    float
        Enrichment factor. Returns 0.0 if there are no actives.
    """
    labels = np.asarray(labels, dtype=int)
    scores = np.asarray(scores, dtype=float)

    n_total = len(labels)
    n_actives = int(np.sum(labels))
    if n_actives == 0:
        return 0.0

    n_top = max(1, int(np.ceil(fraction * n_total)))
    order = np.argsort(scores)[::-1]
    hits_in_top = int(np.sum(labels[order[:n_top]]))

    random_rate = n_actives / n_total
    return (hits_in_top / n_top) / random_rate


def roc_auc(labels, scores):
    """Area Under the ROC Curve (AUC).

    Parameters
    ----------
    labels : array-like of int
        Activity labels (1 = active, 0 = decoy).
    scores : array-like of float
        Screening scores, higher = better ranked.

    Returns
    -------
    float
        AUC in [0, 1]. 0.5 = random, 1.0 = perfect.
    """
    labels = np.asarray(labels, dtype=int)
    scores = np.asarray(scores, dtype=float)

    n_actives = int(np.sum(labels))
    n_decoys = len(labels) - n_actives
    if n_actives == 0 or n_decoys == 0:
        return float('nan')

    order = np.argsort(scores)[::-1]
    sorted_labels = labels[order]

    # Trapezoidal AUC via counting
    tp = 0
    fp = 0
    auc = 0.0
    prev_tp = 0
    for label in sorted_labels:
        if label == 1:
            tp += 1
        else:
            fp += 1
            auc += (tp - prev_tp)
            prev_tp = tp
    # Remaining actives after last decoy
    auc += (tp - prev_tp) * (n_decoys - fp)
    return auc / (n_actives * n_decoys)


def bedroc(labels, scores, alpha=20.0):
    """Boltzmann-Enhanced Discrimination of ROC (BEDROC).

    A metric that gives more weight to early enrichment. alpha controls the
    emphasis: higher alpha = stronger emphasis on the very top of the ranked
    list. Standard value for VS benchmarks: alpha = 20.0.

    Parameters
    ----------
    labels : array-like of int
        Activity labels (1 = active, 0 = decoy).
    scores : array-like of float
        Screening scores, higher = better ranked.
    alpha : float
        Exponential decay parameter (default 20.0).

    Returns
    -------
    float
        BEDROC score in (0, 1]. 1.0 = perfect, ~0.5 = random enrichment.

    References
    ----------
    Truchon & Bayly, J. Chem. Inf. Model. 2007, 47, 488-508, Eq. 15.
    """
    labels = np.asarray(labels, dtype=int)
    scores = np.asarray(scores, dtype=float)

    n = len(labels)
    n_actives = int(np.sum(labels))
    if n_actives == 0 or n_actives == n:
        return float('nan')

    ra = n_actives / n  # fraction of actives

    order = np.argsort(scores)[::-1]
    sorted_labels = labels[order]

    # Ranks are 1-indexed
    ranks = np.where(sorted_labels == 1)[0] + 1  # ranks of actives

    # BEDROC numerator: Boltzmann-weighted sum of active ranks
    ri_sum = float(np.sum(np.exp(-alpha * ranks / n)))

    # Normalisation constants (Eq. 14 & 15 in Truchon & Bayly)
    ra_over_n = ra
    exp_term = np.exp(-alpha * ra_over_n)
    sinh_half = np.sinh(alpha / 2.0)

    # Random BEDROC (rB)
    random_sum = ra * (1.0 - np.exp(-alpha)) / (np.exp(alpha / n) - 1.0)

    # Max BEDROC (mB) — all actives at the top
    max_sum = (1.0 - np.exp(-alpha * ra)) / (1.0 - np.exp(-alpha / n))

    # Min BEDROC (nB) — all actives at the bottom
    min_sum = (1.0 - np.exp(alpha * ra)) / (1.0 - np.exp(alpha / n))

    bedroc_score = (
        (ri_sum / random_sum - 1.0) /
        (max_sum / random_sum - 1.0)
    ) if (max_sum / random_sum - 1.0) != 0.0 else 0.0

    # Clamp to [0, 1] for numerical safety
    return float(np.clip(bedroc_score, 0.0, 1.0))
