"""Public correspondence controls preserve finite enumeration and seed science."""

import importlib
import inspect
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler import from_feature_inventory, get_features
from pharmacophoremt.screening import get_correspondences
from tests.test_correspondence_geometry import inventory
from tests.test_seeded_scoring import ionic_case

CORRESPONDENCE = importlib.import_module("pharmacophoremt.screening.correspondence")
CENTERS = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
SEEDS = [[[0, 0], [1, 1], [2, 2]], [[0, 0], [1, 2], [2, 1]]]


def cached_case():
    features = inventory(CENTERS)
    for record in features["features"]:
        record.update(kind="hydrophobicity", direction=None, normal=None)
    return from_feature_inventory(features, radius=".02 nm"), features


def test_explicit_control_and_closed_definition_owned_public_export():
    assert phmt.screening.get_correspondences is CORRESPONDENCE.get_correspondences
    control = inspect.signature(get_correspondences).parameters["skip_digestion"]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY and control.default is False
    plan = get_correspondences.digestion_plan
    assert plan.contract_owner == "definition"
    assert plan.contract_caller == CORRESPONDENCE.__name__ + ".get_correspondences"
    contract = describe_contract(
        plan.contracts.resolve(plan.contract_caller), plan.domains
    )
    assert contract["admits"] == "signature"


@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_query_or_enumeration(flag, monkeypatch):
    q, features = cached_case()

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid controls must refuse before native query/product work")

    monkeypatch.setattr(CORRESPONDENCE, "PoseEvaluator", forbidden)
    monkeypatch.setattr(CORRESPONDENCE, "product", forbidden)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        get_correspondences(q, features, skip_digestion=flag)


@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
def test_literal_bypass_consumes_own_control_and_keeps_child_default(flag, monkeypatch):
    q, features = cached_case()
    seen, children = [], []
    original_boolean = _contracts._boolean
    original_child = CORRESPONDENCE.PoseEvaluator

    def boolean(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original_boolean(value, argument)

    def child(*args, **kwargs):
        assert "skip_digestion" not in kwargs
        children.append("default")
        return original_child(*args, **kwargs)

    monkeypatch.setattr(_contracts, "_boolean", boolean)
    monkeypatch.setattr(CORRESPONDENCE, "PoseEvaluator", child)
    result = get_correspondences(q, features, skip_digestion=flag)
    assert result["correspondences"] == SEEDS
    assert children == ["default"]
    assert len(seen) == (0 if flag is True else 1) + 1
    if flag is not True:
        assert seen[0] is flag
    assert seen[-1] is False


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize("budget", [0, -1, True, np.bool_(True), 1.5, "3", None])
def test_invalid_budget_refuses_before_child_or_product_even_if_empty(
    skip, empty, budget, monkeypatch
):
    q, features = cached_case()
    if empty:
        features["features"].clear()

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid budgets must refuse before query preparation/enumeration")

    monkeypatch.setattr(CORRESPONDENCE, "PoseEvaluator", forbidden)
    monkeypatch.setattr(CORRESPONDENCE, "product", forbidden)
    with pytest.raises(ArgumentError, match="max_trials"):
        get_correspondences(q, features, max_trials=budget, skip_digestion=skip)


@pytest.mark.parametrize("features", [None, {"features": []}])
def test_native_budget_guard_precedes_unchecked_query_and_inventory(
    features, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("The mandatory budget guard must precede the scientific body")

    monkeypatch.setattr(CORRESPONDENCE, "PoseEvaluator", forbidden)
    with pytest.raises(ArgumentError, match="max_trials"):
        get_correspondences(object(), features, max_trials=-1, skip_digestion=True)


@pytest.mark.parametrize("skip", [False, True])
def test_unknown_keyword_is_closed_before_query_work(skip, monkeypatch):
    q, features = cached_case()

    def forbidden(*args, **kwargs):
        pytest.fail("Unknown keywords cannot enter query preparation")

    monkeypatch.setattr(CORRESPONDENCE, "PoseEvaluator", forbidden)
    with pytest.raises(TypeError):
        get_correspondences(q, features, skip_digestion=skip, max_trial=1)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("geometry", ["short", "collinear"])
def test_native_query_geometry_guards_survive_bypass(skip, geometry):
    centers = CENTERS[:2] if geometry == "short" else [[0, 0, 0], [1, 0, 0], [2, 0, 0]]
    q = from_feature_inventory(inventory(centers), radius=".02 nm")
    with pytest.raises(ArgumentError, match="non-collinear"):
        get_correspondences(q, inventory(CENTERS), skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "budget, trials, pruned, count, complete",
    [
        (1, 1, 1, 0, False),
        (5, 5, 5, 0, False),
        (6, 6, 5, 1, False),
        (8, 8, 6, 2, False),
        (27, 27, 25, 2, True),
        (28, 27, 25, 2, True),
        (np.int64(6), 6, 5, 1, False),
    ],
)
def test_independent_raw_product_counts_seed_order_and_completion(
    skip, budget, trials, pruned, count, complete
):
    q, features = cached_case()
    result = get_correspondences(q, features, max_trials=budget, skip_digestion=skip)
    # Three records in each pool yield 27 raw products: 21 repeat a record,
    # four violate side lengths, and two preserve the right-angle vertex.
    assert result["correspondences"] == SEEDS[:count]
    assert result["n_trials"] == trials and result["n_pruned"] == pruned
    assert result["complete"] is complete


@pytest.mark.parametrize("skip", [False, True])
def test_degenerate_candidate_is_complete_empty_even_with_loose_physical_radii(skip):
    q = from_feature_inventory(inventory(CENTERS), radius="2 nm")
    features = inventory([[0, 0, 0], [0, 0, 0], [0, 1, 0]])
    result = get_correspondences(q, features, skip_digestion=skip)
    assert result["correspondences"] == [] and result["complete"]
    assert result["n_trials"] == result["n_pruned"] == 1


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_real_cached_inventory_units_attribution_and_source_query_custody(
    unit, monkeypatch
):
    with puw.context(standard_units=[unit, "ps", "radians"]):
        source, q = ionic_case()
        features = get_features(source, features=["positive charge"])
        coordinates = puw.get_value(
            msm.get(source, coordinates=True), to_unit="nm"
        ).copy()
        before = deepcopy(features)
        query_centers = [
            puw.get_value(site.center, to_unit="nm").copy()
            for site in q.interaction_sites
        ]

        def forbidden(*args, **kwargs):
            pytest.fail(
                "Cached proposal must not access a molecular provider or fit poses"
            )

        with monkeypatch.context() as patch:
            patch.setattr(msm, "get", forbidden)
            patch.setattr(msm, "select", forbidden)
            for options in ({}, {"skip_digestion": False}, {"skip_digestion": True}):
                with phmt.attribution():
                    result = get_correspondences(q, features, **options)
                assert result["correspondences"] == SEEDS
                assert result["n_trials"] == 27 and result["n_pruned"] == 25
                assert (
                    result["complete"] and result["attribution"]["status"] == "captured"
                )
        np.testing.assert_array_equal(
            coordinates, puw.get_value(msm.get(source, coordinates=True), to_unit="nm")
        )
        assert features.keys() == before.keys()
        assert features["selected_atom_indices"] == before["selected_atom_indices"]
        for record, original in zip(features["features"], before["features"]):
            assert record["kind"] == original["kind"]
            assert record["atom_indices"] == original["atom_indices"]
            np.testing.assert_array_equal(
                puw.get_value(record["center"], to_unit="nm"),
                puw.get_value(original["center"], to_unit="nm"),
            )
        for site, center in zip(q.interaction_sites, query_centers):
            np.testing.assert_array_equal(
                puw.get_value(site.center, to_unit="nm"), center
            )
