"""Equivalent length units retain inclusive clique boundaries without absolute fuzz."""

import numpy as np
import pytest

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import get_aligned_feature_cliques
from phmt_test_support.absence_inputs import inventory


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("policy", ["nm", "pm"])
@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("scale", [1e-12, 0.125, 1e5])
@pytest.mark.parametrize("excess", [-32, 0, 32])
def test_inclusive_boundary_and_beyond_roundoff_negatives(
    skip, policy, unit, scale, excess
):
    # Exact nominal separation equals the declared tolerance at excess=0.
    # Thirty-two epsilons is deliberately outside the eight-epsilon allowance.
    separation = scale * (1 + excess * np.finfo(float).eps)
    sources = [inventory([[0, 0, 0]]), inventory([[separation, 0, 0]])]
    for source in sources:
        record = source["features"][0]
        record["center"] = puw.quantity(
            puw.get_value(record["center"], to_unit=unit), unit
        )
    tolerance = puw.quantity(scale if unit == "nm" else scale * 1000, unit)
    with puw.context(standard_units=[policy, "ps", "radians"]):
        result = get_aligned_feature_cliques(
            sources,
            ligand_ids=["a", "b"],
            distance_tolerance=tolerance,
            skip_digestion=skip,
        )
    connected = excess <= 0
    assert result["complete"] and bool(result["groups"]) is connected
    assert result["n_graph_edges"] == int(connected)
    assert result["n_maximal_cliques"] == (1 if connected else 2)


@pytest.mark.parametrize("skip", [False, True])
def test_tiny_positive_tolerance_has_no_default_absolute_acceptance(skip):
    result = get_aligned_feature_cliques(
        [inventory([[0, 0, 0]]), inventory([[2e-18, 0, 0]])],
        ligand_ids=["a", "b"],
        distance_tolerance="1e-18 nm",
        skip_digestion=skip,
    )
    assert result["complete"] and result["groups"] == []
    assert result["n_graph_edges"] == 0 and result["n_maximal_cliques"] == 2


@pytest.mark.parametrize("skip", [False, True])
def test_roundoff_allowance_accepts_four_epsilons_of_relative_excess(skip):
    separation = 0.125 * (1 + 4 * np.finfo(float).eps)
    with puw.context(standard_units=["nm", "ps", "radians"]):
        result = get_aligned_feature_cliques(
            [inventory([[0, 0, 0]]), inventory([[separation, 0, 0]])],
            ligand_ids=["a", "b"],
            distance_tolerance="0.125 nm",
            skip_digestion=skip,
        )
    assert result["groups"] == [[[0, 0], [1, 0]]] and result["complete"]
