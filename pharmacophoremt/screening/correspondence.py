"""Chemical triplet proposals for the classical rigid-search method."""

from itertools import combinations, product
from math import inf, isfinite, nextafter

import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.screening.pose_evaluation import (
    _POSITION_RELATIVE_SLACK,
    PoseEvaluator,
)


def _pair_distance_exceeds_tolerance(candidate, reference, radius_a, radius_b):
    """Reject only beyond physical tolerance and the candidate roundoff band.

    All inputs are already normalized lengths. Reuse final positive-site slack
    for the radius sum and a conservative allowance for both computed norms.
    Outward rounding retains uncertain boundary candidates for final evaluation;
    it does not alter physical radii or the final matching predicate.
    """
    if not (isfinite(candidate) and isfinite(reference)):
        return False
    difference = abs(candidate - reference)
    physical_limit = radius_a + radius_b
    if difference <= physical_limit:
        return False
    outward_limit = nextafter(physical_limit, inf)
    allowance = _POSITION_RELATIVE_SLACK * (outward_limit + candidate + reference)
    return difference > nextafter(outward_limit + allowance, inf)


def _centers_of_sites(sites):
    return np.asarray(
        [
            puw.get_value(
                site.center if site.center is not None else site.shape.position,
                to_unit="nm",
            )
            for site in sites
        ],
        dtype=float,
    )


def _noncollinear(centers):
    # A computed centroid can leave rounding residuals on identical points,
    # inventing a second singular direction at a displaced coordinate origin.
    # Anchor differences to an existing point so coincident centers stay zero.
    return np.linalg.matrix_rank(centers - centers[0]) >= 2


def _essential_anchors(evaluator):
    essentials = [(index, site) for index, site in evaluator.query if site.essential]
    if len(essentials) < 3 or not _noncollinear(
        _centers_of_sites([site for _, site in essentials])
    ):
        raise ArgumentError(
            argument="pharmacophore",
            reason="rigid triplet search requires at least three non-collinear essential centers",
        )
    return essentials


@signal(tags=["screening", "correspondence"])
@arg_digest()
@attributed("numpy", "pyunitwizard")
def get_correspondences(
    pharmacophore, feature_inventory, *, point_tolerance="0.10 nm", max_trials=10000
):
    """Propose chemically compatible, injective essential-site triplets.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        Classical query supported by PoseEvaluator.
    feature_inventory : dict
        Output of modeler.get_features in the unchanged source frame.
    point_tolerance : length quantity, default='0.10 nm'
        Position tolerance for Point sites.
    max_trials : int, default=10000
        Bound on raw triplet candidate products, including rejected products.

    Returns
    -------
    dict
        Correspondences as lists of (site index, feature index), trial/pruning
        counts, and explicit complete flag. Incomplete enumeration never claims
        there were no matches. Feature indices refer to the supplied inventory.

    Notes
    -----
    At least three essential sites must have non-collinear centers. Each seed
    uses three different candidate records. Pair-distance pruning uses the sum
    of the corresponding site tolerances plus an outward-rounded candidate
    allowance for final positive-site slack and the two computed norms. This
    may retain candidates that final evaluation rejects; physical tolerances
    and final matching are unchanged. Degenerate triplets are omitted.
    Site feature lists are alternatives, as in PoseEvaluator. Record uniqueness
    does not require disjoint atom membership across distinct chemical roles.
    This is a seed proposal method, not a complete continuous constraint solver.

    Examples
    --------
    >>> proposals = get_correspondences(query, inventory, max_trials=10000)
    >>> first_seed = proposals['correspondences'][0]
    """
    evaluator = PoseEvaluator(pharmacophore, point_tolerance=point_tolerance)
    essentials = _essential_anchors(evaluator)
    if feature_inventory is None:
        raise ArgumentError(
            argument="feature_inventory", reason="provide modeler.get_features output"
        )
    records = feature_inventory["features"]
    candidate_centers = np.asarray(
        [puw.get_value(record["center"], to_unit="nm") for record in records],
        dtype=float,
    )
    pools = {
        index: [
            column
            for column, record in enumerate(records)
            if record["kind"] in site.features
        ]
        for index, site in essentials
    }
    proposals, n_trials, n_pruned = [], 0, 0
    available = [(index, site) for index, site in essentials if pools[index]]
    for sites in combinations(available, 3):
        reference = _centers_of_sites([site for _, site in sites])
        if not _noncollinear(reference):
            continue
        radii = [
            float(puw.get_value(site.radius, to_unit="nm"))
            if site.radius is not None
            else evaluator.point_tolerance
            for _, site in sites
        ]
        for columns in product(*(pools[index] for index, _ in sites)):
            if n_trials == max_trials:
                return dict(
                    correspondences=proposals,
                    n_trials=n_trials,
                    n_pruned=n_pruned,
                    complete=False,
                )
            n_trials += 1
            if len(set(columns)) != 3:
                n_pruned += 1
                continue
            candidate = candidate_centers[list(columns)]
            if not _noncollinear(candidate) or any(
                _pair_distance_exceeds_tolerance(
                    np.linalg.norm(candidate[a] - candidate[b]),
                    np.linalg.norm(reference[a] - reference[b]),
                    radii[a],
                    radii[b],
                )
                for a, b in ((0, 1), (0, 2), (1, 2))
            ):
                n_pruned += 1
                continue
            proposals.append(
                [[index, int(column)] for (index, _), column in zip(sites, columns)]
            )
    return dict(
        correspondences=proposals, n_trials=n_trials, n_pruned=n_pruned, complete=True
    )
