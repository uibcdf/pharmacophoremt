"""Independent exact-input oracle and real PHMT receiving for prepared P1."""

from copy import deepcopy
from fractions import Fraction
from itertools import combinations

import pytest

from phmt_test_support.pharmer_p1 import (
    expectation_passed,
    load_declaration,
    qualify_case,
)

DECLARATION, QUERY = load_declaration()
CASES = DECLARATION["cases"]


def squared_distance(first, second):
    return sum(
        (Fraction(float(a)) - Fraction(float(b))) ** 2 for a, b in zip(first, second)
    )


def test_binary_query_and_source_units_define_the_original_inputs():
    assert DECLARATION["source_unit"] == "nm"
    assert DECLARATION["query_unit"] == "angstrom"
    assert Fraction(DECLARATION["radius_nm"]) == Fraction(1, 32)
    for point, center in zip(
        QUERY["points"], DECLARATION["reference_centers_nm"], strict=True
    ):
        assert point["name"] == "PositiveIon" and point["enabled"] is True
        assert set(point) == {"name", "x", "y", "z", "radius", "enabled"}
        assert [Fraction(point[axis]) / 10 for axis in ("x", "y", "z")] == [
            Fraction(x) for x in center
        ]
        assert Fraction(point["radius"]) / 10 == Fraction(1, 32)
    assert DECLARATION["external"]["state"] == "not_executed"


@pytest.mark.parametrize("case", CASES[:2], ids=lambda row: row["key"])
def test_positive_original_mapping_has_an_exact_proper_inverse(case):
    rotation = DECLARATION["source_to_reference_rotation"]
    translation = DECLARATION["source_to_reference_translation_nm"]
    assert rotation == [[0, 1, 0], [-1, 0, 0], [0, 0, 1]]
    # This fixed signed permutation has determinant +1, orthogonal columns,
    # and an exact rational inverse; no production fit/distance code is used.
    assert rotation[0][1] * rotation[1][0] * rotation[2][2] == -1
    for site, atom in case["expected"]["correspondences"][0]:
        center = case["centers"][atom]
        actual = [
            sum(Fraction(a) * Fraction(b) for a, b in zip(row, center)) + Fraction(t)
            for row, t in zip(rotation, translation)
        ]
        assert actual == [
            Fraction(x) for x in DECLARATION["reference_centers_nm"][site]
        ]


def test_rational_edge_separation_forces_the_unique_positive_mapping():
    centers = DECLARATION["reference_centers_nm"]
    assert sorted(
        squared_distance(centers[a], centers[b]) for a, b in combinations(range(3), 2)
    ) == [Fraction(1, 4), Fraction(1), Fraction(5, 4)]
    # Distance intervals for1/2,1,sqrt(5/4) are disjoint at the pair2r cutoff.
    assert Fraction(1, 2) + Fraction(1, 16) < 1
    assert (1 + Fraction(1, 16)) ** 2 < Fraction(5, 4)
    # Each scalene edge must preserve its identity, fixing all three vertices.
    assert [row["expected"]["n_trials"] for row in CASES] == [27, 27, 27]
    assert [row["expected"]["n_pruned"] for row in CASES] == [26, 26, 27]


def test_stretched_original_edge_proves_no_required_rigid_placement():
    centers = CASES[2]["centers"]
    assert squared_distance(centers[0], centers[2]) == 4
    reference = DECLARATION["reference_centers_nm"]
    assert all(
        squared_distance(reference[a], reference[b]) < Fraction(25, 16)
        for a, b in combinations(range(3), 2)
    )
    assert 2 - Fraction(5, 4) > Fraction(1, 16)
    assert CASES[2]["expected"]["correspondences"] == []


@pytest.mark.parametrize("case", CASES, ids=lambda row: row["key"])
@pytest.mark.parametrize("attribution", [False, True])
def test_public_phmt_arm_matches_the_frozen_independent_answers(case, attribution):
    import ackredit

    import pharmacophoremt as phmt

    original = deepcopy(case)
    with ackredit.session("P1 receiving"), phmt.attribution(enabled=attribution):
        result = qualify_case(case)
    assert expectation_passed(case, result), result
    assert ("attribution" in result["proposals"]) is attribution
    assert result["external_state"] == "not_executed"
    assert case == original


def test_incomplete_proposal_is_a_failed_case_rather_than_a_negative():
    with pytest.raises(RuntimeError, match="incomplete; no answer accepted"):
        qualify_case(CASES[0], max_trials=1)
