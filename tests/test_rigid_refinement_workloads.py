"""Seed, tolerance, mixed-family and 3D analytical refinement controls."""

import molsysmt as msm
import numpy as np
import pytest

from devtools.rigid_refinement_workloads import build_workload, load_workloads
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import get_features
from pharmacophoremt.screening import (
    evaluate_feature_correspondence,
    refine_rigid_feature_correspondences,
)


@pytest.fixture(
    scope="module", params=load_workloads(), ids=lambda case: case["case_id"]
)
def workload(request):
    case = request.param
    reference, source = build_workload(case)
    return (
        case,
        source,
        get_features(reference, features=case["features"]),
        get_features(source, features=case["features"]),
    )


@pytest.mark.parametrize("policy", ["final", "each_step"])
def test_declared_workload_outcomes_and_valid_returned_pairs(workload, policy):
    case, source, target, inventory = workload
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    result = refine_rigid_feature_correspondences(
        source,
        target,
        case["correspondences"],
        features=case["features"],
        feature_inventory=inventory,
        orientation_policy=policy,
        **case["parameters"],
    )
    expected = case["expected"][policy]
    assert len(result["placements"]) == expected["n_placements"], case["rationale"]
    assert result["report"]["n_fits"] == expected["n_fits"]
    assert (
        max((len(p["matches"]["matches"]) for p in result["placements"]), default=0)
        == expected["max_matches"]
    )
    assert result["report"]["complete"]
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )
    for placement in result["placements"]:
        geometry = evaluate_feature_correspondence(
            target,
            placement["inventory"],
            placement["matches"]["matches"],
            distance_tolerance=case["parameters"]["distance_tolerance"],
            direction_tolerance=case["parameters"]["direction_tolerance"],
        )
        assert geometry["all_pairs_valid"]
        assert len(placement["matches"]["matches"]) >= case["parameters"]["min_matches"]
