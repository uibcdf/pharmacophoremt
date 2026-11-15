"""Rigid proposal admission preserves finite families, budgets and source custody."""

import importlib
import inspect
import json
from copy import deepcopy
from functools import wraps
from itertools import combinations

import ackredit
import molsysmt as msm
import numpy as np
import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.smonitor.exceptions import ArgumentError, CliqueLimitError
from pharmacophoremt.screening import get_rigid_feature_correspondences
from phmt_test_support.absence_inputs import inventory

OWNER = importlib.import_module("pharmacophoremt.screening.rigid_correspondence")
STRATEGIES = ["association_cliques", "triplet_seeds", "ranked_triplet_seeds"]
CENTERS = np.array([[0, 0, 0], [0.25, 0, 0], [0, 0.5, 0], [0.0625, 0.1875, 0.75]])


def features():
    return inventory(CENTERS)


def test_explicit_keyword_only_control_and_closed_definition_owned_export():
    operation = get_rigid_feature_correspondences
    assert phmt.screening.get_rigid_feature_correspondences is operation
    control = inspect.signature(operation).parameters["skip_digestion"]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY and control.default is False
    plan = operation.digestion_plan
    assert plan.contract_owner == "definition"
    assert plan.contract_caller == OWNER.__name__ + ".get_rigid_feature_correspondences"
    contract = plan.contracts.resolve(plan.contract_caller)
    assert describe_contract(contract, plan.domains)["admits"] == "signature"


@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_native_work(flag, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid control reached native inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        get_rigid_feature_correspondences(
            features(), inventory([]), skip_digestion=flag
        )


@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
def test_only_literal_true_bypasses_ordinary_control_digestion(flag, monkeypatch):
    seen = []
    original = _contracts._boolean

    def boolean(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    class ReachedInventory(Exception):
        pass

    def reached(*args, **kwargs):
        raise ReachedInventory

    monkeypatch.setattr(_contracts, "_boolean", boolean)
    monkeypatch.setattr(OWNER, "_records", reached)
    with pytest.raises(ReachedInventory):
        get_rigid_feature_correspondences(
            features(), inventory([]), skip_digestion=flag
        )
    assert len(seen) == (0 if flag is True else 1)
    if flag is not True:
        assert seen[0] is flag


@pytest.mark.parametrize("skip", [False, True])
def test_unknown_keyword_stays_closed_before_inventory(skip, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Unknown keyword reached native inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(TypeError):
        get_rigid_feature_correspondences(
            features(), inventory([]), unexpected=True, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("arguments", [(), (None,)])
def test_both_inventories_remain_required(skip, arguments):
    with pytest.raises(TypeError):
        get_rigid_feature_correspondences(*arguments, skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("value", [None, True, 0, "unknown", []])
def test_invalid_strategy_refuses_before_inventory_even_with_empty_candidate(
    skip, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid strategy reached native inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match="correspondence_strategy"):
        get_rigid_feature_correspondences(
            features(),
            inventory([]),
            correspondence_strategy=value,
            skip_digestion=skip,
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "argument", ["max_graph_nodes", "max_cliques", "max_trials", "max_matrix_entries"]
)
@pytest.mark.parametrize("value", [0, -1, True, 1.5])
def test_all_budget_domains_remain_native_even_for_unused_family(
    skip, argument, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid budget reached native inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match=argument):
        get_rigid_feature_correspondences(
            features(), inventory([]), skip_digestion=skip, **{argument: value}
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("value", [0, 2, True, 3.5])
def test_rigid_minimum_cannot_drop_below_three_even_for_triplets(
    skip, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid minimum reached native inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match="min_matches"):
        get_rigid_feature_correspondences(
            features(),
            inventory([]),
            correspondence_strategy="triplet_seeds",
            min_matches=value,
            skip_digestion=skip,
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("value", ["0 nm", "-1 nm", "nan nm", "inf nm", "1 ps"])
def test_positive_finite_length_is_native_before_inventory(skip, value, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid physical tolerance reached native inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match="distance_tolerance"):
        get_rigid_feature_correspondences(
            features(), inventory([]), distance_tolerance=value, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("value", [0, -1, True, 1.5])
def test_ranked_seed_count_remains_native_for_empty_candidates(
    skip, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid seed count reached native inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match="n_seeds"):
        get_rigid_feature_correspondences(
            features(),
            inventory([]),
            correspondence_strategy="ranked_triplet_seeds",
            n_seeds=value,
            skip_digestion=skip,
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("strategy", STRATEGIES[:2])
def test_finite_seed_selection_stays_exclusive_to_ranked_method(skip, strategy):
    with pytest.raises(ArgumentError, match="n_seeds"):
        get_rigid_feature_correspondences(
            features(),
            inventory([]),
            correspondence_strategy=strategy,
            n_seeds=1,
            skip_digestion=skip,
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("strategy", STRATEGIES)
def test_completed_empty_candidate_keeps_declared_scope_and_unused_capacity(
    skip, strategy
):
    result = get_rigid_feature_correspondences(
        features(),
        inventory([]),
        correspondence_strategy=strategy,
        max_graph_nodes=1,
        max_cliques=1,
        max_trials=1,
        max_matrix_entries=1,
        skip_digestion=skip,
    )
    assert result["complete"] and result["correspondences"] == []
    assert result["method"] == "rigid_" + strategy + "@1"
    assert (
        result["criteria"]["completion_scope"]
        == "declared_finite_correspondence_proposal_family"
    )
    assert "skip_digestion" not in result["criteria"]
    if strategy == "ranked_triplet_seeds":
        assert result["selection_exhaustive"] and result["n_omitted_seeds"] == 0
        assert result["neighborhood_comparison"]["n_pair_assignments"] == 0


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "options,stage",
    [
        ({"max_graph_nodes": 15}, "association_graph"),
        ({"max_cliques": 1}, "association_cliques"),
        (
            {"correspondence_strategy": "triplet_seeds", "max_trials": 1},
            "triplet_proposals",
        ),
        (
            {"correspondence_strategy": "ranked_triplet_seeds", "max_trials": 1},
            "triplet_proposals",
        ),
        (
            {
                "correspondence_strategy": "ranked_triplet_seeds",
                "max_matrix_entries": 15,
            },
            "feature_neighborhoods",
        ),
    ],
)
def test_exhaustion_is_original_failure_never_partial_or_empty_success(
    skip, options, stage
):
    with pytest.raises(CliqueLimitError) as caught:
        get_rigid_feature_correspondences(
            features(), features(), skip_digestion=skip, **options
        )
    assert caught.value.code == "PHMT-E107" and caught.value.extra["stage"] == stage
    assert caught.value.extra["complete"] is False


@pytest.mark.parametrize("skip", [False, True])
def test_node_budget_refuses_before_graph_allocation(skip, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Exhausted node budget allocated a graph")

    monkeypatch.setattr(OWNER.nx, "Graph", forbidden)
    with pytest.raises(CliqueLimitError):
        get_rigid_feature_correspondences(
            features(), features(), max_graph_nodes=15, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("strategy", STRATEGIES)
def test_collinear_reference_and_incomplete_native_geometry_still_refuse(
    skip, strategy
):
    for reference in (inventory([[0, 0, 0], [1, 0, 0], [2, 0, 0]]), inventory([])):
        with pytest.raises(ArgumentError, match="reference_inventory"):
            get_rigid_feature_correspondences(
                reference,
                inventory([]),
                correspondence_strategy=strategy,
                skip_digestion=skip,
            )
    missing_direction = inventory(CENTERS, ["hb donor"] * 4)
    with pytest.raises(ArgumentError):
        get_rigid_feature_correspondences(
            features(),
            missing_direction,
            correspondence_strategy=strategy,
            skip_digestion=skip,
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("reflection", [False, True])
@pytest.mark.parametrize("strategy", STRATEGIES)
def test_exact_rigid_and_reflected_family_oracles_keep_units_children_and_custody(
    skip, unit, reflection, strategy, monkeypatch
):
    # Unique edge lengths give one full mapping and its four distinct triplets.
    assert len({float(np.linalg.norm(a - b)) for a, b in combinations(CENTERS, 2)}) == 6
    order = [2, 0, 3, 1]
    transform = np.array([[0, -1, 0], [1, 0, 0], [0, 0, -1 if reflection else 1]])
    first = features()
    second = inventory(CENTERS[order] @ transform + [4, 2, 1])
    for source in (first, second):
        for record in source["features"]:
            value = puw.get_value(record["center"], to_unit=unit)
            record["center"] = puw.quantity(value, unit)
    before = [
        deepcopy(puw.get_value(r["center"], to_unit=unit))
        for source in (first, second)
        for r in source["features"]
    ]
    calls = {
        name: []
        for name in (
            "from_feature_inventory",
            "get_correspondences",
            "get_feature_pair_dissimilarities",
            "rank_rigid_feature_correspondences",
        )
    }
    for name in calls:
        original = getattr(OWNER, name)

        def spy(operation, child):
            @wraps(operation)
            def observed(*args, **kwargs):
                calls[child].append(kwargs.copy())
                assert "skip_digestion" not in kwargs
                return operation(*args, **kwargs)

            return observed

        monkeypatch.setattr(OWNER, name, spy(original, name))

    def forbidden(*args, **kwargs):
        pytest.fail("Invariant proposals must not read or fit molecular systems")

    monkeypatch.setattr(msm, "get", forbidden)
    monkeypatch.setattr(msm.structure, "least_rmsd_fit", forbidden)
    tolerance = puw.quantity(0.0001 if unit == "nm" else 0.1, unit)
    result = get_rigid_feature_correspondences(
        first,
        second,
        correspondence_strategy=strategy,
        distance_tolerance=tolerance,
        min_matches=4,
        n_seeds=2 if strategy == "ranked_triplet_seeds" else None,
        skip_digestion=skip,
    )
    mapping = [[i, order.index(i)] for i in range(4)]
    triplets = sorted([list(pairs) for pairs in combinations(mapping, 3)])
    expected = [mapping] if strategy == "association_cliques" else triplets
    if strategy == "ranked_triplet_seeds":
        expected = expected[:2]
        assert result["n_ranked_seeds"] == result["n_omitted_seeds"] == 2
        assert not result["selection_exhaustive"]
        scores = result["seed_ranking"]["scores"]
        np.testing.assert_allclose(scores, [0, 0], atol=1e-10, rtol=0)
        assert scores == sorted(scores)
        assert result["seed_ranking"]["complete"]
        selected = result["correspondences"]
        assert len(selected) == 2 and selected[0] != selected[1]
        assert all(seed in triplets for seed in selected)
        # Unit conversion perturbs near-zero ranking ties; all four exact
        # geometric triplets remain valid. Exact nm ties retain lexicographic order.
        if unit == "nm":
            assert selected == expected
    else:
        assert result["correspondences"] == expected
    assert result["complete"]
    assert result["criteria"]["min_matches"] == 4  # Does not change triplet size.
    assert result["criteria"]["pair_distance_multiplier"] == 2
    for name, observed in calls.items():
        needed = (
            strategy != "association_cliques"
            if name in ("from_feature_inventory", "get_correspondences")
            else strategy == "ranked_triplet_seeds"
        )
        assert len(observed) == int(needed)
    after = [
        puw.get_value(r["center"], to_unit=unit)
        for source in (first, second)
        for r in source["features"]
    ]
    for original, current in zip(before, after):
        np.testing.assert_array_equal(original, current)
    result["criteria"]["distance_tolerance"] = "99 nm"
    assert float(puw.get_value(tolerance, to_unit="nm")) == pytest.approx(0.0001)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "child",
    [
        "get_correspondences",
        "get_feature_pair_dissimilarities",
        "rank_rigid_feature_correspondences",
    ],
)
def test_original_child_failure_is_preserved_without_partial_science(
    skip, child, monkeypatch
):
    error = RuntimeError("Original proposal child failure")

    def failing(*args, **kwargs):
        assert "skip_digestion" not in kwargs
        raise error

    monkeypatch.setattr(OWNER, child, failing)
    with pytest.raises(RuntimeError) as caught:
        get_rigid_feature_correspondences(
            features(),
            features(),
            correspondence_strategy="ranked_triplet_seeds",
            skip_digestion=skip,
        )
    assert caught.value is error


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("strategy", STRATEGIES)
def test_actual_application_capture_credits_reached_method_only(skip, strategy):
    with ackredit.session("proposal-contract"), phmt.attribution():
        result = get_rigid_feature_correspondences(
            features(),
            features(),
            correspondence_strategy=strategy,
            skip_digestion=skip,
        )
    payload = result["attribution"]
    assert payload["status"] == "captured"
    titles = [r["title"] for r in payload["references"]["items"]]
    assert any("cliques" in t.lower() for t in titles) == (
        strategy == "association_cliques"
    )
    assert any("rectangular assignment" in t for t in titles) == (
        strategy == "ranked_triplet_seeds"
    )
    assert "MolSysMT" not in titles
    assert not any("Kabsch" in t for t in titles)
    json.dumps(payload, allow_nan=False)
