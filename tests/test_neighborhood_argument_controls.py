"""Independent native comparison/ranking admission, oracles and custody controls."""

import importlib
import inspect
import json
import math
from copy import deepcopy
from itertools import permutations

import ackredit
import molsysmt as msm
import numpy as np
import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.smonitor.exceptions import ArgumentError, CliqueLimitError
from pharmacophoremt.screening import (
    get_feature_pair_dissimilarities,
    rank_rigid_feature_correspondences,
)
from phmt_test_support.absence_inputs import inventory

OWNER = importlib.import_module("pharmacophoremt.screening.feature_neighborhoods")
OPERATIONS = [get_feature_pair_dissimilarities, rank_rigid_feature_correspondences]
MAPPING = [[0, 0], [1, 1], [2, 2]]


def features():
    return inventory([[0, 0, 0], [0.25, 0, 0], [0, 0.5, 0]])


def report():
    # A declared finite comparison, not authenticated molecular provenance.
    return dict(
        method="typed_neighborhood_assignment@1",
        complete=True,
        n_reference=3,
        n_candidate=3,
        costs=[[0.25, 0.125, 0.5], [0.125, 0.5, 0.125], [0.5, 0.125, 0.25]],
        compatible=[[True] * 3 for _ in range(3)],
        criteria={"nested": {"values": [7]}},
        attribution={"status": "retained_origin", "records": ["original"]},
    )


def arguments(operation):
    if operation is get_feature_pair_dissimilarities:
        return features(), inventory([])
    return [], report()


@pytest.mark.parametrize("operation", OPERATIONS)
def test_explicit_keyword_only_closed_definition_owned_exports(operation):
    assert getattr(phmt.screening, operation.__name__) is operation
    flag = inspect.signature(operation).parameters["skip_digestion"]
    assert flag.kind is inspect.Parameter.KEYWORD_ONLY and flag.default is False
    plan = operation.digestion_plan
    assert plan.contract_owner == "definition"
    assert plan.contract_caller == OWNER.__name__ + "." + operation.__name__
    contract = plan.contracts.resolve(plan.contract_caller)
    assert describe_contract(contract, plan.domains)["admits"] == "signature"


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_native_scientific_work(
    operation, flag, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid control reached native scientific work")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    monkeypatch.setattr(OWNER, "credit_criterion", forbidden)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        operation(*arguments(operation), skip_digestion=flag)


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
def test_literal_true_alone_bypasses_ordinary_control_digestion(
    operation, flag, monkeypatch
):
    seen = []
    original = _contracts._boolean

    def boolean(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    monkeypatch.setattr(_contracts, "_boolean", boolean)
    result = operation(*arguments(operation), skip_digestion=flag)
    assert result["complete"]
    assert len(seen) == (0 if flag is True else 1)
    if flag is not True:
        assert seen[0] is flag


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("count", [0, 1])
def test_both_required_inputs_stay_required(operation, skip, count):
    with pytest.raises(TypeError):
        operation(*arguments(operation)[:count], skip_digestion=skip)


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("skip", [False, True])
def test_unknown_keyword_stays_closed(operation, skip):
    with pytest.raises(TypeError):
        operation(*arguments(operation), unexpected=True, skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize("value", [0, -1, True, 1.5])
def test_comparison_budget_domain_refuses_before_inventory_even_when_empty(
    skip, empty, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid matrix budget reached inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match="max_matrix_entries"):
        get_feature_pair_dissimilarities(
            features(),
            inventory([]) if empty else features(),
            max_matrix_entries=value,
            skip_digestion=skip,
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("value", ["0 nm", "-1 nm", "nan nm", "inf nm", "1 ps"])
def test_comparison_physical_domain_refuses_before_inventory_even_when_empty(
    skip, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid tolerance reached inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match="distance_tolerance"):
        get_feature_pair_dissimilarities(
            features(), inventory([]), distance_tolerance=value, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("value", [0, -1, True, 1.5])
def test_ranking_seed_count_domain_is_mandatory_even_for_empty_seeds(skip, value):
    with pytest.raises(ArgumentError, match="n_seeds"):
        rank_rigid_feature_correspondences(
            [], report(), n_seeds=value, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize(
    "change",
    [
        {"method": "unknown"},
        {"complete": False},
        {"complete": np.bool_(True)},
        {"n_reference": -1},
        {"n_candidate": True},
        {"n_reference": 4},
        {"costs": [[float("nan")] * 3] * 3},
        {"costs": [[1.01] * 3] * 3},
        {"compatible": [[1] * 3] * 3},
        {"criteria": None},
    ],
)
def test_invalid_comparison_evidence_cannot_rank_even_empty_requests(
    skip, empty, change
):
    comparison = report()
    comparison.update(change)
    with pytest.raises(ArgumentError, match="feature_pair_dissimilarities"):
        rank_rigid_feature_correspondences(
            [] if empty else [MAPPING], comparison, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "bad",
    [
        [[-1, 0], [1, 1], [2, 2]],
        np.array([[0, 0], [1, 1], [2, np.iinfo(np.uint64).max]], dtype=np.uint64),
        [[False, False], [True, True], [True, False]],
        [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]],
        [[0, 0], [0, 1], [2, 2]],
        [[0, 0], [1, 0], [2, 2]],
        [[0, 0], [1, 1]],
        [[0, 0], [1, 1], [2, 2], [3, 3]],
        [[0, 0], [1, 1], [2, 3]],
    ],
)
def test_malformed_later_mapping_never_returns_partial_ranking(skip, bad):
    with pytest.raises(ArgumentError):
        rank_rigid_feature_correspondences(
            [MAPPING, bad], report(), skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
def test_incompatible_pair_and_nonsequence_collection_still_refuse(skip):
    comparison = report()
    comparison["compatible"][1][1] = False
    with pytest.raises(ArgumentError, match="incompatible"):
        rank_rigid_feature_correspondences([MAPPING], comparison, skip_digestion=skip)
    with pytest.raises(ArgumentError, match="correspondences"):
        rank_rigid_feature_correspondences(
            np.array([MAPPING]), report(), skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
def test_native_feature_geometry_is_still_required_during_comparison(skip):
    bad = inventory([[0, 0, 0]], ["hb donor"])
    with pytest.raises(ArgumentError):
        get_feature_pair_dissimilarities(features(), bad, skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_exhausted_matrix_budget_is_original_failure_before_assignment(
    skip, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Exhausted matrix budget reached assignment")

    monkeypatch.setattr(OWNER, "linear_sum_assignment", forbidden)
    with pytest.raises(CliqueLimitError) as caught:
        get_feature_pair_dissimilarities(
            features(), features(), max_matrix_entries=8, skip_digestion=skip
        )
    assert caught.value.code == "PHMT-E107"
    assert caught.value.extra["stage"] == "feature_neighborhoods"
    assert caught.value.extra["observed"] == 9 and caught.value.extra["limit"] == 8
    assert caught.value.extra["complete"] is False


@pytest.mark.parametrize("skip", [False, True])
def test_original_assignment_failure_keeps_exception_and_source_custody(
    skip, monkeypatch
):
    error = RuntimeError("Original assignment failure")
    first, second = features(), features()
    original = [
        puw.get_value(r["center"], to_unit="nm").copy()
        for source in (first, second)
        for r in source["features"]
    ]

    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(OWNER, "linear_sum_assignment", fail)
    with pytest.raises(RuntimeError) as caught:
        get_feature_pair_dissimilarities(first, second, skip_digestion=skip)
    assert caught.value is error
    current = [
        puw.get_value(r["center"], to_unit="nm")
        for source in (first, second)
        for r in source["features"]
    ]
    for before, after in zip(original, current):
        np.testing.assert_array_equal(before, after)


def environment_oracle(first, second, row, column, tolerance):
    if first["features"][row]["kind"] != second["features"][column]["kind"]:
        return 1

    def neighbors(source, focal):
        origin = puw.get_value(source["features"][focal]["center"], to_unit="nm")
        return [
            (r["kind"], math.dist(origin, puw.get_value(r["center"], to_unit="nm")))
            for i, r in enumerate(source["features"])
            if i != focal
        ]

    left, right = neighbors(first, row), neighbors(second, column)
    size = max(len(left), len(right))
    best = math.inf
    for permutation in permutations(range(size)):
        total = 0
        for i, j in enumerate(permutation):
            if i >= len(left) or j >= len(right) or left[i][0] != right[j][0]:
                total += 1
            else:
                total += min(abs(left[i][1] - right[j][1]) / (2 * tolerance), 1)
        best = min(best, total)
    return best / max(len(first["features"]), len(second["features"]))


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_asymmetric_typed_assignment_matches_independent_oracle_and_keeps_units(
    skip, unit, monkeypatch
):
    first = inventory([[0, 0, 0], [0.25, 0, 0]], ["hb acceptor", "positive charge"])
    second = inventory(
        [[2, 1, 0], [2, 1.375, 0], [1.5, 1, 0], [2, 1, 0.5]],
        ["positive charge", "hb acceptor", "negative charge", "hb acceptor"],
    )
    for source in (first, second):
        for record in source["features"]:
            record["center"] = puw.quantity(
                puw.get_value(record["center"], to_unit=unit), unit
            )
    originals = [
        puw.get_value(r["center"], to_unit=unit).copy()
        for source in (first, second)
        for r in source["features"]
    ]

    def forbidden(*args, **kwargs):
        pytest.fail("Neighborhood comparison cannot read or fit molecular systems")

    monkeypatch.setattr(msm, "get", forbidden)
    monkeypatch.setattr(msm.structure, "least_rmsd_fit", forbidden)
    tolerance = puw.quantity(0.125 if unit == "nm" else 125, unit)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        application_policy = deepcopy(puw.configure.get_standard_units())
        result = get_feature_pair_dissimilarities(
            first,
            second,
            distance_tolerance=tolerance,
            max_matrix_entries=np.int64(16),
            skip_digestion=skip,
        )
        assert puw.configure.get_standard_units() == application_policy
    expected = [
        [environment_oracle(first, second, i, j, 0.125) for j in range(4)]
        for i in range(2)
    ]
    np.testing.assert_allclose(result["costs"], expected, rtol=0, atol=1e-12)
    assert result["compatible"] == [
        [False, True, False, True],
        [True, False, False, False],
    ]
    assert result["n_pair_assignments"] == 3
    assert (
        result["largest_matrix_entries"] == 16
        and result["n_assignment_matrix_entries"] == 27
    )
    assert result["criteria"]["normalization"] == "larger_whole_inventory_feature_count"
    assert (
        result["criteria"]["orientation_policy"] == "post_fit_only"
        and result["complete"]
    )
    assert "skip_digestion" not in result["criteria"]
    for before, record in zip(
        originals, [r for source in (first, second) for r in source["features"]]
    ):
        np.testing.assert_array_equal(
            before, puw.get_value(record["center"], to_unit=unit)
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("axes", [(0, 3), (3, 0), (0, 0)])
def test_completed_empty_axes_keep_shape_without_unused_assignment_capacity(
    skip, axes, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Empty axes cannot execute an assignment")

    monkeypatch.setattr(OWNER, "linear_sum_assignment", forbidden)
    sources = [inventory([[i, 0, 0] for i in range(n)]) for n in axes]
    comparison = get_feature_pair_dissimilarities(
        *sources, max_matrix_entries=1, skip_digestion=skip
    )
    assert comparison["complete"] and comparison["largest_matrix_entries"] == 0
    assert (
        comparison["n_pair_assignments"]
        == comparison["n_assignment_matrix_entries"]
        == 0
    )
    assert (comparison["n_reference"], comparison["n_candidate"]) == axes
    assert comparison["costs"] == [[] for _ in range(axes[0])]
    assert comparison["compatible"] == [[] for _ in range(axes[0])]
    ranked = rank_rigid_feature_correspondences(
        [], json.loads(json.dumps(comparison)), n_seeds=np.int64(1), skip_digestion=skip
    )
    assert ranked["complete"] and ranked["selection_exhaustive"]
    assert ranked["n_selected"] == ranked["n_omitted"] == ranked["n_supplied"] == 0


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("limit", [None, 1, np.int64(3), 50])
def test_independent_ranking_oracle_keeps_duplicates_ties_selection_and_detached_provenance(
    skip, limit
):
    comparison = json.loads(json.dumps(report()))
    a = [[0, 1], [1, 0], [2, 2]]  # 0.5
    b = MAPPING  # 1.0
    c = [[0, 1], [1, 2], [2, 0]]  # 0.75
    supplied = [list(reversed(b)), list(reversed(a)), c, a, b]
    before = deepcopy(supplied), deepcopy(comparison)
    result = rank_rigid_feature_correspondences(
        supplied, comparison, n_seeds=limit, skip_digestion=skip
    )
    count = 5 if limit is None else min(limit, 5)
    assert result["correspondences"] == [a, a, c, b, b][:count]
    assert result["scores"] == [0.5, 0.5, 0.75, 1, 1][:count]
    assert result["supplied_proposal_indices"] == [1, 3, 2, 0, 4][:count]
    assert result["n_supplied"] == 5 and result["n_selected"] == count
    assert result["n_omitted"] == 5 - count and result["complete"]
    assert result["selection_exhaustive"] == (count == 5)
    assert (
        result["criteria"]["completion_scope"]
        == "supplied_guesses_and_declared_seed_selection"
    )
    assert "skip_digestion" not in result["criteria"]
    assert (supplied, comparison) == before
    comparison["attribution"]["records"].clear()
    comparison["criteria"]["nested"]["values"].clear()
    assert result["source_attribution"]["records"] == ["original"]
    assert result["criteria"]["dissimilarity_criteria"]["nested"]["values"] == [7]
    supplied[0].clear()
    assert result["correspondences"] == [a, a, c, b, b][:count]


@pytest.mark.parametrize("skip", [False, True])
def test_real_application_sessions_credit_only_reached_comparison_and_ranking_operations(
    skip,
):
    with ackredit.session("neighborhood-controls"), phmt.attribution():
        first = get_feature_pair_dissimilarities(
            features(), features(), skip_digestion=skip
        )
        second = get_feature_pair_dissimilarities(
            features(), features(), skip_digestion=skip
        )
        ranked = rank_rigid_feature_correspondences(
            [MAPPING], first, skip_digestion=skip
        )
        empty_comparison = get_feature_pair_dissimilarities(
            inventory([]), features(), skip_digestion=skip
        )
        empty_ranking = rank_rigid_feature_correspondences(
            [], first, skip_digestion=skip
        )
    for payload in (first["attribution"], second["attribution"]):
        assert payload["status"] == "captured"
        text = json.dumps(payload)
        assert (
            "10.3390/molecules26237201" in text and "10.1109/TAES.2016.140952" in text
        )
    assert ranked["source_attribution"] == first["attribution"]
    ranking_credit = json.dumps(ranked["attribution"])
    assert "10.3390/molecules26237201" in ranking_credit
    assert "10.1109/TAES.2016.140952" not in ranking_credit
    for result in (empty_comparison, empty_ranking):
        assert "10.3390/molecules26237201" not in json.dumps(result["attribution"])
        assert "10.1109/TAES.2016.140952" not in json.dumps(result["attribution"])
