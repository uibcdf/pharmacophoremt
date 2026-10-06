"""Independent environment-assignment and seed-selection controls."""

import itertools
import json
import math
from copy import deepcopy
from pathlib import Path

import ackredit
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from devtools.benchmark_rigid_consensus import _matches_expectation
from devtools.rigid_consensus_cases import build_case, load_cases
from pharmacophoremt._private.smonitor.exceptions import ArgumentError, CliqueLimitError
from pharmacophoremt.modeler import from_rigid_ligands
from pharmacophoremt.screening import (
    get_feature_pair_dissimilarities,
    get_rigid_feature_correspondences,
    rank_rigid_feature_correspondences,
)
from pharmacophoremt.validation import summarize_rigid_consensus
from tests.test_aligned_consensus import inventory

CASES = Path(__file__).parent / "data/ranked_seed_cases.json"


@pytest.mark.parametrize("case", load_cases(CASES), ids=lambda case: case["case_id"])
def test_ranked_frozen_selection_case_expectations(case):
    parameters = dict(
        case["parameters"], **case["strategy_parameters"]["ranked_triplet_seeds"]
    )
    result = from_rigid_ligands(
        build_case(case), correspondence_strategy="ranked_triplet_seeds", **parameters
    )
    summary = summarize_rigid_consensus(result["report"])
    outcome = dict(
        status="completed" if result["models"] else "completed_empty", summary=summary
    )
    assert _matches_expectation(outcome, case["expected"]["ranked_triplet_seeds"])
    assert summary["n_fits"] <= 1


def exhaustive_environment_cost(first, second, row, column, tolerance):
    """Small independent permutation oracle using scalar typed distances."""
    if first["features"][row]["kind"] != second["features"][column]["kind"]:
        return 1.0
    from pharmacophoremt import pyunitwizard as puw

    def neighbors(source, focal):
        center = puw.get_value(source["features"][focal]["center"], to_unit="nm")
        return [
            (r["kind"], math.dist(center, puw.get_value(r["center"], to_unit="nm")))
            for index, r in enumerate(source["features"])
            if index != focal
        ]

    left, right = neighbors(first, row), neighbors(second, column)
    size = max(len(left), len(right))
    if not size:
        return 0.0
    best = math.inf
    for permutation in itertools.permutations(range(size)):
        total = 0
        for i, j in enumerate(permutation):
            if i >= len(left) or j >= len(right) or left[i][0] != right[j][0]:
                total += 1
            else:
                total += min(abs(left[i][1] - right[j][1]) / (2 * tolerance), 1)
        best = min(best, total)
    return best / max(len(first["features"]), len(second["features"]))


def test_neighborhood_assignment_agrees_with_independent_permutation_oracle():
    rng = np.random.default_rng(284)
    for n_first, n_second in ((2, 4), (3, 3), (4, 2)):
        first = inventory(
            rng.uniform(0, 1, (n_first, 3)),
            ["hb acceptor", "positive charge", "hb acceptor", "negative charge"][
                :n_first
            ],
        )
        second = inventory(
            rng.uniform(0, 1, (n_second, 3)),
            ["positive charge", "hb acceptor", "negative charge", "hb acceptor"][
                :n_second
            ],
        )
        result = get_feature_pair_dissimilarities(
            first, second, distance_tolerance="0.2 nm"
        )
        for i in range(n_first):
            for j in range(n_second):
                assert result["costs"][i][j] == pytest.approx(
                    exhaustive_environment_cost(first, second, i, j, 0.2)
                )
                assert result["compatible"][i][j] == (
                    first["features"][i]["kind"] == second["features"][j]["kind"]
                )
        json.dumps(result, allow_nan=False)


def test_unmatched_neighbors_cost_one_and_singletons_and_empty_axes_are_explicit():
    one = inventory([[0, 0, 0]])
    many = inventory([[0, 0, 0], [0.2, 0, 0], [0, 0.3, 0]])
    assert get_feature_pair_dissimilarities(one, many)["costs"][0] == pytest.approx(
        [2 / 3] * 3
    )
    assert get_feature_pair_dissimilarities(one, one)["costs"] == [[0]]
    incompatible = inventory([[0, 0, 0]], ["positive charge"])
    result = get_feature_pair_dissimilarities(one, incompatible)
    assert result["costs"] == [[1]] and result["compatible"] == [[False]]
    for first, second in (
        (inventory([]), many),
        (many, inventory([])),
        (inventory([]), inventory([])),
    ):
        report = get_feature_pair_dissimilarities(first, second, max_matrix_entries=1)
        assert report["complete"] and report["n_pair_assignments"] == 0
        assert (
            rank_rigid_feature_correspondences([], json.loads(json.dumps(report)))[
                "n_selected"
            ]
            == 0
        )


def test_costs_preserve_unit_conversion_and_geometry_permutations_without_molecular_reads(
    monkeypatch,
):
    first = inventory(
        [[0, 0, 0], [0.4, 0, 0], [0, 0.3, 0]],
        ["hb acceptor", "positive charge", "hb acceptor"],
    )
    second = inventory(
        [[2, 1, 3], [2, 1.4, 3], [1.7, 1, 3]],
        ["hb acceptor", "positive charge", "hb acceptor"],
    )

    def forbidden(*args, **kwargs):
        raise AssertionError("descriptor calculation must not read molecular systems")

    monkeypatch.setattr(msm, "get", forbidden)
    direct = get_feature_pair_dissimilarities(first, first)
    moved = get_feature_pair_dissimilarities(first, second)
    np.testing.assert_allclose(direct["costs"], moved["costs"], atol=1e-14)
    angstrom = get_feature_pair_dissimilarities(
        first, second, distance_tolerance="1.5 angstrom"
    )
    np.testing.assert_allclose(moved["costs"], angstrom["costs"])
    reordered = deepcopy(second)
    reordered["features"].reverse()
    np.testing.assert_allclose(
        np.array(moved["costs"])[:, ::-1],
        get_feature_pair_dissimilarities(first, reordered)["costs"],
        atol=1e-14,
    )


def test_neighborhood_budget_preflights_before_assignment(monkeypatch):
    import pharmacophoremt.screening.feature_neighborhoods as module

    def forbidden(*args, **kwargs):
        raise AssertionError("over-budget comparison reached the solver")

    monkeypatch.setattr(module, "linear_sum_assignment", forbidden)
    source = inventory([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    with pytest.raises(CliqueLimitError) as caught:
        get_feature_pair_dissimilarities(source, source, max_matrix_entries=8)
    assert caught.value.code == "PHMT-E107"


def test_ranking_sums_scores_canonicalizes_ties_and_detaches_source_evidence():
    source = inventory([[0, 0, 0], [0.4, 0, 0], [0, 0.3, 0]])
    costs = get_feature_pair_dissimilarities(source, source)
    costs["attribution"] = {"status": "retained_origin", "records": ["a"]}
    mapping = [[0, 0], [1, 1], [2, 2]]
    duplicate = list(reversed(mapping))
    other = [[0, 1], [1, 0], [2, 2]]
    result = rank_rigid_feature_correspondences(
        [other, duplicate, mapping], costs, n_seeds=2
    )
    assert result["correspondences"] == [mapping, mapping]
    assert result["supplied_proposal_indices"] == [1, 2]
    assert (
        result["scores"] == [0, 0]
        and result["n_omitted"] == 1
        and not result["selection_exhaustive"]
    )
    costs["attribution"]["records"].clear()
    assert result["source_attribution"]["records"] == ["a"]
    all_seeds = rank_rigid_feature_correspondences([other, mapping], costs)
    assert all_seeds["selection_exhaustive"] and all_seeds["n_selected"] == 2


@pytest.mark.parametrize(
    "mutate",
    [
        lambda r: r.update(complete=False),
        lambda r: r.update(costs=[[float("nan")] * 3] * 3),
        lambda r: r.update(costs=[[2.0] * 3] * 3),
        lambda r: r.update(compatible=[[1] * 3] * 3),
        lambda r: r.update(n_reference=4),
    ],
)
def test_invalid_saved_comparison_cannot_be_ranked(mutate):
    source = inventory([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    report = get_feature_pair_dissimilarities(source, source)
    mutate(report)
    with pytest.raises(ArgumentError):
        rank_rigid_feature_correspondences([], report)


def test_ranking_rejects_incompatible_out_of_range_and_nontriplet_mappings():
    source = inventory(
        [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]],
        ["hb acceptor", "positive charge", "negative charge", "hb acceptor"],
    )
    report = get_feature_pair_dissimilarities(source, source)
    for mapping in (
        [[0, 1], [1, 0], [2, 2]],
        [[0, 0], [1, 1], [2, 4]],
        [[0, 0], [1, 1], [2, 2], [3, 3]],
    ):
        with pytest.raises(ArgumentError):
            rank_rigid_feature_correspondences([mapping], report)


def test_all_ranked_seeds_preserve_the_unranked_proposal_family_and_limits_remain_explicit():
    source = inventory([[0, 0, 0], [0.4, 0, 0], [0, 0.3, 0]])
    basic = get_rigid_feature_correspondences(
        source, source, correspondence_strategy="triplet_seeds"
    )
    ranked = get_rigid_feature_correspondences(
        source, source, correspondence_strategy="ranked_triplet_seeds"
    )
    assert sorted(ranked["correspondences"]) == basic["correspondences"]
    assert ranked["selection_exhaustive"] and ranked["n_trials"] == basic["n_trials"]
    limited = get_rigid_feature_correspondences(
        source, source, correspondence_strategy="ranked_triplet_seeds", n_seeds=1
    )
    assert (
        limited["complete"]
        and len(limited["correspondences"]) == 1
        and not limited["selection_exhaustive"]
    )
    with pytest.raises(CliqueLimitError):
        get_rigid_feature_correspondences(
            source,
            source,
            correspondence_strategy="ranked_triplet_seeds",
            n_seeds=1,
            max_trials=1,
        )
    with pytest.raises(ArgumentError, match="ranked_triplet_seeds"):
        get_rigid_feature_correspondences(source, source, n_seeds=1)


def test_seed_limit_can_miss_an_existing_full_match_in_real_provider_workflow():
    case = next(
        c
        for c in load_cases(CASES)
        if c["case_id"] == "ranked_reflection_false_negative"
    )
    ligands = build_case(case)
    limited = from_rigid_ligands(
        ligands,
        correspondence_strategy="ranked_triplet_seeds",
        n_seeds=1,
        **case["parameters"],
    )
    exhaustive = from_rigid_ligands(
        ligands, correspondence_strategy="ranked_triplet_seeds", **case["parameters"]
    )
    assert limited["complete"] and limited["models"] == []
    assert len(exhaustive["models"]) == 8
    first, second = map(
        summarize_rigid_consensus, [limited["report"], exhaustive["report"]]
    )
    assert first["n_fits"] == 1 and second["n_fits"] == 16
    assert first["sources"][1]["proposal_selection_exhaustive"] is False
    assert second["max_joint_sites"] == 4


def test_consumer_calls_public_descriptor_and_ranking_tools(monkeypatch):
    from pharmacophoremt.screening import rigid_correspondence as module

    calls = []
    comparison, ranking = (
        module.get_feature_pair_dissimilarities,
        module.rank_rigid_feature_correspondences,
    )

    def observe_comparison(*args, **kwargs):
        calls.append("comparison")
        return comparison(*args, **kwargs)

    def observe_ranking(*args, **kwargs):
        calls.append("ranking")
        return ranking(*args, **kwargs)

    monkeypatch.setattr(module, "get_feature_pair_dissimilarities", observe_comparison)
    monkeypatch.setattr(module, "rank_rigid_feature_correspondences", observe_ranking)
    case = next(c for c in load_cases() if c["case_id"] == "symmetric_3")
    result = from_rigid_ligands(
        build_case(case),
        correspondence_strategy="ranked_triplet_seeds",
        n_seeds=1,
        **case["parameters"],
    )
    assert result["models"] and calls == ["comparison", "ranking"]


def test_ackredit_credits_executed_seed_stage_and_actual_solver_in_enclosing_session():
    source = inventory([[0, 0, 0], [0.4, 0, 0], [0, 0.3, 0]])
    with ackredit.session("ranked-seed-control"), phmt.attribution():
        first = get_feature_pair_dissimilarities(source, source)
        second = get_feature_pair_dissimilarities(source, source)
        assert (
            first["attribution"]["status"]
            == second["attribution"]["status"]
            == "captured"
        )
        for payload in (first["attribution"], second["attribution"]):
            text = json.dumps(payload)
            assert (
                "10.3390/molecules26237201" in text
                and "10.1109/TAES.2016.140952" in text
            )
            assert "methodological_basis" in text and "excluded_stages" in text
        ranked = rank_rigid_feature_correspondences([[[0, 0], [1, 1], [2, 2]]], first)
        assert "10.3390/molecules26237201" in phmt.attribution_report(
            ranked["attribution"], format="bibtex"
        )
        absent = get_feature_pair_dissimilarities(inventory([]), source)
        assert "10.3390/molecules26237201" not in json.dumps(absent["attribution"])
