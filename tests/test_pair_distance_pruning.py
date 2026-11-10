"""Analytical final-acceptance witnesses for the public triplet candidate filter.

The original binary case is unchanged from #160. Cached cases are mathematical
feature inventories; the ion case also runs real public molecular recognition
and evaluation. None establishes biological validity or continuous-search scope.
"""

from fractions import Fraction
from math import dist

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import Pharmacophore
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Point, Sphere
from pharmacophoremt.modeler import from_ligand, get_features
from pharmacophoremt.screening import PoseEvaluator, get_correspondences
from phmt_test_support.absence_inputs import inventory, system

KINDS = ["positive charge", "negative charge", "hydrophobicity"]


def case(*, exponent=0, multiplier=1, span=1, shape="sphere", zero_weight=False):
    scale = 2.0**exponent
    radius = scale / 8
    delta = scale * 2.0**-52
    reference = np.array([[0, 0, 0], [span * scale, 0, 0], [0, scale, 0]])
    candidate = reference.copy()
    candidate[0, 0] -= radius + multiplier * delta
    candidate[1, 0] += radius + multiplier * delta
    query = Pharmacophore()
    for index, (center, kind) in enumerate(zip(reference, KINDS, strict=True)):
        center = puw.quantity(center, "nm")
        geometry = (
            Point(center)
            if shape == "point"
            else Sphere(center, puw.quantity(radius, "nm"))
        )
        query.add_interaction_site(
            InteractionSite(
                geometry,
                kind,
                essential=True,
                weight=0 if zero_weight and index == 0 else 1,
            )
        )
    return query, inventory(candidate, KINDS), reference, candidate, radius


def final_match(query, features, radius):
    records = [
        {**row, "center": puw.get_value(row["center"], to_unit="nm")}
        for row in features["features"]
    ]
    # Exercise the unchanged actual assignment/acceptance operation on cached
    # analytical records, without substituting a mocked distance/evaluator.
    return PoseEvaluator(query, point_tolerance=puw.quantity(radius, "nm"))._match(
        records, np.empty((0, 3)), np.array([], dtype=int)
    )


def test_original_binary_boundary_retains_a_public_proposal():
    query, features, reference, candidate, radius = case()
    # Independent exact rational witness: no production slack/filter formula.
    expected = Fraction(1, 8) + Fraction(1, 2**52)
    assert Fraction.from_float(dist(reference[0], candidate[0])) == expected
    assert Fraction.from_float(dist(reference[1], candidate[1])) == expected
    assert (
        Fraction.from_float(
            dist(candidate[0], candidate[1]) - dist(reference[0], reference[1])
        )
        == 2 * expected
    )
    assert final_match(query, features, radius)["status"] == "matched"
    result = get_correspondences(query, features)
    assert result["correspondences"] == [[[0, 0], [1, 1], [2, 2]]]
    assert (result["n_trials"], result["n_pruned"], result["complete"]) == (1, 0, True)


@pytest.mark.parametrize("exponent", [-8, 0, 8])
@pytest.mark.parametrize("zero_weight", [False, True])
def test_binary_rescaling_and_zero_weight_essential_keep_the_boundary_seed(
    exponent, zero_weight
):
    query, features, _, _, radius = case(exponent=exponent, zero_weight=zero_weight)
    matched = final_match(query, features, radius)
    assert matched["status"] == "matched" and matched["fit_value"] == 1
    assert matched["missing_essential_sites"] == []
    result = get_correspondences(query, features)
    assert result["correspondences"] == [[[0, 0], [1, 1], [2, 2]]]
    assert result["complete"]


@pytest.mark.parametrize("shape", ["point", "sphere"])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_point_tolerance_and_explicit_unit_policy_preserve_accepted_candidates(
    shape, unit
):
    with puw.context(standard_units=[unit, "ps", "radians"]):
        # A separate declared half-span/four-epsilon variant leaves room for
        # unit conversion roundoff; it does not replace the original witness.
        query, features, _, _, radius = case(span=0.5, multiplier=0.5, shape=shape)
        assert final_match(query, features, radius)["status"] == "matched"
        result = get_correspondences(
            query, features, point_tolerance=puw.quantity(radius, "nm")
        )
        assert result["correspondences"] == [[[0, 0], [1, 1], [2, 2]]]


def test_public_ion_evaluation_and_seed_filter_share_the_original_boundary():
    _, _, reference, candidate, radius = case()
    first = system("[Na+].[Cl-].[K+]", reference)
    second = system("[Na+].[Cl-].[K+]", candidate)
    kinds = ["positive charge", "negative charge"]
    query = from_ligand(first, features=kinds, radius=puw.quantity(radius, "nm"))
    features = get_features(second, features=kinds)
    assert query.n_interaction_sites == len(features["features"]) == 3
    before = puw.get_value(msm.get(second, coordinates=True), to_unit="nm").copy()
    final = PoseEvaluator(query).evaluate(second)
    assert final["status"] == "matched" and final["fit_value"] == 1
    proposals = get_correspondences(query, features)
    assert [[0, 0], [1, 1], [2, 2]] in proposals["correspondences"]
    np.testing.assert_array_equal(
        puw.get_value(msm.get(second, coordinates=True), to_unit="nm"), before
    )


def test_conservative_candidate_band_does_not_widen_final_matching():
    query, features, _, _, radius = case(multiplier=2)
    final = final_match(query, features, radius)
    assert final["status"] == "not_matched"
    assert final["missing_essential_sites"] == [0, 1]
    # A conservative prefilter may retain an uncertain boundary candidate;
    # the unchanged final predicate must still refuse the original geometry.
    proposals = get_correspondences(query, features)
    assert proposals["correspondences"] == [[[0, 0], [1, 1], [2, 2]]]


def test_a_physical_distance_mismatch_remains_pruned():
    query, features, _, _, radius = case(multiplier=2.0**40)
    assert final_match(query, features, radius)["status"] == "not_matched"
    result = get_correspondences(query, features)
    assert result == dict(correspondences=[], n_trials=1, n_pruned=1, complete=True)


def test_raw_product_budget_stays_incomplete_after_a_retained_boundary_seed():
    query, features, _, candidate, _ = case()
    features = inventory([*candidate, candidate[0]], [*KINDS, KINDS[0]])
    result = get_correspondences(query, features, max_trials=1)
    assert result["n_trials"] == 1 and result["n_pruned"] == 0
    assert not result["complete"]
    assert result["correspondences"] == [[[0, 0], [1, 1], [2, 2]]]


@pytest.mark.parametrize("multiplier", [0, -1])
def test_nominal_boundary_and_interior_keep_original_counters(multiplier):
    query, features, _, _, radius = case(multiplier=multiplier)
    assert final_match(query, features, radius)["status"] == "matched"
    result = get_correspondences(query, features)
    assert result == dict(
        correspondences=[[[0, 0], [1, 1], [2, 2]]],
        n_trials=1,
        n_pruned=0,
        complete=True,
    )


def test_association_boundary_retains_an_accepted_mapping():
    from pharmacophoremt.screening import get_rigid_feature_correspondences

    query, features, reference, candidate, radius = case()
    expected = Fraction(1, 8) + Fraction(1, 2**52)
    assert Fraction.from_float(dist(reference[0], candidate[0])) == expected
    assert final_match(query, features, radius)["status"] == "matched"
    result = get_rigid_feature_correspondences(
        inventory(reference, KINDS),
        features,
        distance_tolerance=puw.quantity(radius, "nm"),
    )
    assert result["correspondences"] == [[[0, 0], [1, 1], [2, 2]]]
    assert (result["n_graph_edges"], result["complete"]) == (3, True)


@pytest.mark.parametrize("exponent", [-8, 0, 8])
@pytest.mark.parametrize("order", [(0, 1, 2), (2, 0, 1)])
def test_association_rescaling_preserves_original_occurrence_mapping(exponent, order):
    from pharmacophoremt.screening import get_rigid_feature_correspondences

    query, features, reference, candidate, radius = case(exponent=exponent)
    assert final_match(query, features, radius)["status"] == "matched"
    features = inventory(candidate[list(order)], [KINDS[i] for i in order])
    result = get_rigid_feature_correspondences(
        inventory(reference, KINDS),
        features,
        distance_tolerance=puw.quantity(radius, "nm"),
    )
    assert result["correspondences"] == [[[i, order.index(i)] for i in range(3)]]
    assert result["complete"]


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_association_explicit_units_keep_the_boundary_candidate(unit):
    from pharmacophoremt.screening import get_rigid_feature_correspondences

    with puw.context(standard_units=[unit, "ps", "radians"]):
        query, features, reference, _, radius = case(span=0.5, multiplier=0.5)
        assert final_match(query, features, radius)["status"] == "matched"
        result = get_rigid_feature_correspondences(
            inventory(reference, KINDS),
            features,
            distance_tolerance=puw.quantity(radius, "nm"),
        )
        assert result["correspondences"] == [[[0, 0], [1, 1], [2, 2]]]


def test_association_conservative_band_leaves_final_rejection_authoritative():
    from pharmacophoremt.screening import get_rigid_feature_correspondences

    query, features, reference, _, radius = case(multiplier=2)
    assert final_match(query, features, radius)["status"] == "not_matched"
    result = get_rigid_feature_correspondences(
        inventory(reference, KINDS),
        features,
        distance_tolerance=puw.quantity(radius, "nm"),
    )
    assert result["correspondences"] == [[[0, 0], [1, 1], [2, 2]]]


def test_association_physical_mismatch_remains_a_completed_empty_result():
    from pharmacophoremt.screening import get_rigid_feature_correspondences

    query, features, reference, _, radius = case(multiplier=2.0**40)
    assert final_match(query, features, radius)["status"] == "not_matched"
    result = get_rigid_feature_correspondences(
        inventory(reference, KINDS),
        features,
        distance_tolerance=puw.quantity(radius, "nm"),
    )
    assert result["correspondences"] == [] and result["complete"]


def test_association_boundary_still_enforces_the_declared_graph_bound():
    from pharmacophoremt._private.smonitor.exceptions import CliqueLimitError
    from pharmacophoremt.screening import get_rigid_feature_correspondences

    _, features, reference, _, radius = case()
    with pytest.raises(CliqueLimitError):
        get_rigid_feature_correspondences(
            inventory(reference, KINDS),
            features,
            distance_tolerance=puw.quantity(radius, "nm"),
            max_graph_nodes=2,
        )


def test_public_ion_evaluation_and_association_share_the_original_boundary():
    from pharmacophoremt.screening import get_rigid_feature_correspondences

    _, _, reference, candidate, radius = case()
    first = system("[Na+].[Cl-].[K+]", reference)
    second = system("[Na+].[Cl-].[K+]", candidate)
    kinds = ["positive charge", "negative charge"]
    query = from_ligand(first, features=kinds, radius=puw.quantity(radius, "nm"))
    source_features = get_features(second, features=kinds)
    before = puw.get_value(msm.get(second, coordinates=True), to_unit="nm").copy()
    assert PoseEvaluator(query).evaluate(second)["status"] == "matched"
    result = get_rigid_feature_correspondences(
        get_features(first, features=kinds),
        source_features,
        distance_tolerance=puw.quantity(radius, "nm"),
    )
    assert [[0, 0], [1, 1], [2, 2]] in result["correspondences"]
    np.testing.assert_array_equal(
        puw.get_value(msm.get(second, coordinates=True), to_unit="nm"), before
    )
