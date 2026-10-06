"""Public seed eligibility with typed features sharing the same physical center."""

import numpy as np
import pytest

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler import from_feature_inventory
from pharmacophoremt.screening import get_correspondences


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


@pytest.mark.parametrize(
    "origin", [[0, 0, 0], [10.961, 1.2027, 2.2746], [-100, 200, -300]]
)
def test_two_physical_centers_never_define_a_rigid_triplet(origin):
    first = np.asarray(origin, dtype=float)
    last = first + [-0.6796666666666666, 0.4689333333333333, 0.17735]
    features = inventory([first, first, last])
    query = from_feature_inventory(features, radius=".02 nm")
    with pytest.raises(ArgumentError, match="non-collinear"):
        get_correspondences(query, features)


@pytest.mark.parametrize(
    "origin", [[0, 0, 0], [10.961, 1.2027, 2.2746], [-100, 200, -300]]
)
def test_three_distinct_noncollinear_centers_still_propose_the_identity(origin):
    origin = np.asarray(origin, dtype=float)
    features = inventory([origin, origin + [1, 0, 0], origin + [0, 1, 0]])
    query = from_feature_inventory(features, radius=".02 nm")
    result = get_correspondences(query, features)
    assert result["complete"]
    assert result["correspondences"] == [[[0, 0], [1, 1], [2, 2]]]
