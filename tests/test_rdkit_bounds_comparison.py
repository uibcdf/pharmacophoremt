"""Actual Pharm3D filters, complete native fits and independent known geometry."""

from copy import deepcopy

import pytest

from pharmacophoremt._private.smonitor.exceptions import CliqueLimitError
from phmt_test_support.rdkit_bounds_comparison import (
    compare_case,
    expectation_passed,
    load_cases,
)

CASES = load_cases()


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
