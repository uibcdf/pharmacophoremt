"""Actual Pharm3D filters, complete native fits and independent known geometry."""

from copy import deepcopy
from fractions import Fraction

import pytest

from pharmacophoremt._private.smonitor.exceptions import CliqueLimitError
from phmt_test_support.rdkit_bounds_comparison import (
    compare_case,
    expectation_passed,
    load_cases,
)

CASES = load_cases()


@pytest.mark.parametrize(
    "case",
    [case for case in CASES if case["boundary"] is not None],
    ids=lambda case: case["key"],
)
def test_boundary_coordinates_define_exact_rational_endpoints(case):
    """The actual binary inputs must define a Pythagorean endpoint exactly."""
    distances = []
    i, j = case["boundary"]["reference_pair"]
    for name in ("reference", "source"):
        assert case[name]["unit"] == "nm"
        first, second = case[name]["centers"][i], case[name]["centers"][j]
        components = [
            Fraction(float(a)) - Fraction(float(b)) for a, b in zip(first, second)
        ]
        x, y, z = (abs(value) for value in components)
        assert 4 * x == 3 * y and z == 0, "binary inputs must keep the exact 3:4 ratio"
        distance = x * Fraction(5, 3)
        assert sum(value * value for value in components) == distance * distance
        # Exact representability also removes sqrt rounding ambiguity at this probe.
        assert Fraction(float(distance)) == distance
        distances.append(distance)
    tolerance, unit = case["distance_tolerance"].split()
    assert unit == "nm"
    assert abs(distances[1] - distances[0]) == 2 * Fraction(tolerance)


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["key"])
def test_declared_geometry_and_boundary_expectations(case):
    original = deepcopy(case)
    result = compare_case(case)
    assert expectation_passed(case, result), result
    assert case == original


def test_resource_exhaustion_is_a_failure_rather_than_a_negative():
    with pytest.raises(CliqueLimitError):
        compare_case(CASES[0], max_graph_nodes=1)


def test_empty_geometry_is_outside_the_comparison_domain():
    case = deepcopy(CASES[0])
    case["reference"]["centers"] = []
    with pytest.raises(ValueError, match="three or four"):
        compare_case(case)
