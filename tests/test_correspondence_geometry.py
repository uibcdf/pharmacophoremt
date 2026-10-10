"""Public seed eligibility with typed features sharing the same physical center."""

from itertools import combinations
from math import dist

import numpy as np
import pytest

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler import from_feature_inventory
from pharmacophoremt.screening import (
    get_correspondences,
    get_rigid_feature_correspondences,
)

ORIGINS = [[0, 0, 0], [10.961, 1.2027, 2.2746], [-100, 200, -300]]
STRATEGIES = [
    "query",
    "association_cliques",
    "triplet_seeds",
    "ranked_triplet_seeds",
]


def inventory(centers):
    kinds = ["hb donor", "hb acceptor", "aromatic ring"]
    return dict(
        definition="classical_atomic_formal@1",
        structure_index=0,
        chemical_state="reference",
        selected_atom_indices=[0, 1, 2],
        recognition={},
        features=[
            dict(
                kind=kind,
                atom_indices=[i],
                geometry_atom_indices=[i],
                center=puw.quantity(point, "nm"),
                charge=None,
                direction=puw.quantity([1, 0, 0], "dimensionless")
                if kind == "hb donor"
                else None,
                normal=puw.quantity([0, 0, 1], "dimensionless")
                if kind == "aromatic ring"
                else None,
            )
            for i, (kind, point) in enumerate(zip(kinds, centers))
        ],
    )


def propose(reference, candidate, strategy, tolerance=".02 nm"):
    if strategy == "query":
        query = from_feature_inventory(reference, radius=tolerance)
        return get_correspondences(query, candidate)
    return get_rigid_feature_correspondences(
        reference,
        candidate,
        correspondence_strategy=strategy,
        distance_tolerance=tolerance,
    )


@pytest.mark.parametrize("origin", ORIGINS)
@pytest.mark.parametrize("strategy", STRATEGIES)
@pytest.mark.parametrize("order", [(0, 1, 2), (2, 0, 1), (0, 2, 1)])
def test_two_physical_centers_never_define_a_rigid_triplet(origin, strategy, order):
    first = np.asarray(origin, dtype=float)
    last = first + [-0.6796666666666666, 0.4689333333333333, 0.17735]
    centers = np.asarray([first, first, last])[list(order)]
    assert len(np.unique(centers, axis=0)) == 2
    features = inventory(centers)
    with pytest.raises(ArgumentError, match="non-collinear"):
        propose(features, features, strategy)


@pytest.mark.parametrize("origin", ORIGINS)
@pytest.mark.parametrize("strategy", STRATEGIES)
def test_three_distinct_noncollinear_centers_still_propose_the_identity(
    origin, strategy
):
    origin = np.asarray(origin, dtype=float)
    features = inventory([origin, origin + [1, 0, 0], origin + [0, 1, 0]])
    result = propose(features, features, strategy)
    assert result["complete"]
    assert result["correspondences"] == [[[0, 0], [1, 1], [2, 2]]]


@pytest.mark.parametrize("origin", ORIGINS)
@pytest.mark.parametrize("strategy", STRATEGIES)
def test_two_center_candidate_is_a_completed_empty_proposal(origin, strategy):
    origin = np.asarray(origin, dtype=float)
    reference = [origin, origin + [0.125, 0, 0], origin + [0, 0.125, 0]]
    candidate = [
        origin,
        origin,
        origin + [-0.6796666666666666, 0.4689333333333333, 0.17735],
    ]
    assert len(np.unique(candidate, axis=0)) == 2
    # A loose 1 nm tolerance admits every pair-distance condition. The empty
    # result must therefore come from the candidate's degenerate geometry.
    for a, b in combinations(range(3), 2):
        assert (
            abs(dist(reference[a], reference[b]) - dist(candidate[a], candidate[b])) < 2
        )
    result = propose(inventory(reference), inventory(candidate), strategy, "1 nm")
    assert result["complete"]
    assert result["correspondences"] == []
    assert result["n_pruned"] == 1
