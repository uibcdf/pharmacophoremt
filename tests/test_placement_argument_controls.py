"""Rigid placement admission preserves independent children and molecular custody."""

import importlib
import inspect
import json
from copy import deepcopy
from functools import wraps

import ackredit
import molsysmt as msm
import numpy as np
import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    CliqueLimitError,
    ConsensusLimitError,
)
from pharmacophoremt.modeler import get_features
from pharmacophoremt.screening import get_rigid_feature_placements
from phmt_test_support.absence_inputs import inventory, system
from tests.test_conformer_screening import add_declared_state
from tests.test_seeded_scoring import ionic_case

PLACEMENTS = importlib.import_module("pharmacophoremt.screening.rigid_placements")
CENTERS = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float)
PAIRS = np.array([[2, 2], [0, 0], [1, 1]], dtype=np.int64)


def features():
    return inventory(CENTERS, ["positive charge"] * 3)


def options():
    return dict(features=["positive charge"], feature_inventory=features())


def test_explicit_keyword_only_control_and_closed_definition_owned_export():
    assert (
        phmt.screening.get_rigid_feature_placements
        is PLACEMENTS.get_rigid_feature_placements
    )
    control = inspect.signature(get_rigid_feature_placements).parameters[
        "skip_digestion"
    ]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY and control.default is False
    plan = get_rigid_feature_placements.digestion_plan
    assert plan.contract_owner == "definition"
    assert plan.contract_caller == PLACEMENTS.__name__ + ".get_rigid_feature_placements"
    assert (
        describe_contract(plan.contracts.resolve(plan.contract_caller), plan.domains)[
            "admits"
        ]
        == "signature"
    )


@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_native_inventory_or_fitting(flag, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid controls must refuse before native inventory or fitting")

    monkeypatch.setattr(PLACEMENTS, "_records", forbidden)
    monkeypatch.setattr(PLACEMENTS, "_fit_feature_mapping", forbidden)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        get_rigid_feature_placements(
            object(), features(), [], skip_digestion=flag, **options()
        )


@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
def test_literal_bypass_and_numpy_behavior_observed_before_native_inventory(
    flag, monkeypatch
):
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
    monkeypatch.setattr(PLACEMENTS, "_records", reached)
    with pytest.raises(ReachedInventory):
        get_rigid_feature_placements(
            object(), features(), [], skip_digestion=flag, **options()
        )
    assert len(seen) == (0 if flag is True else 1)
    if flag is not True:
        assert seen[0] is flag


@pytest.mark.parametrize("skip", [False, True])
def test_unknown_keyword_is_closed_before_native_work(skip, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Unknown options cannot reach native placement work")

    monkeypatch.setattr(PLACEMENTS, "_records", forbidden)
    with pytest.raises(TypeError):
        get_rigid_feature_placements(
            object(), features(), [], skip_digestion=skip, max_fit=1, **options()
        )


@pytest.mark.parametrize("skip", [False, True])
def test_mapping_collection_remains_required(skip):
    with pytest.raises(TypeError):
        get_rigid_feature_placements(object(), features(), skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize("argument", ["max_fits", "max_matrix_entries", "min_matches"])
@pytest.mark.parametrize("bad", [0, True, 0.5, None])
def test_invalid_native_limits_refuse_before_inventory_even_if_empty(
    skip, empty, argument, bad, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid budgets/minimum must refuse before native inventory")

    monkeypatch.setattr(PLACEMENTS, "_records", forbidden)
    monkeypatch.setattr(PLACEMENTS, "_source_inventory", forbidden)
    with pytest.raises(ArgumentError, match=argument):
        get_rigid_feature_placements(
            object(),
            features(),
            [] if empty else [PAIRS],
            skip_digestion=skip,
            **options(),
            **{argument: bad},
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("empty", [False, True])
def test_minimum_match_count_cannot_drop_below_rigid_three(skip, empty, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("A two-center minimum must refuse before inventory work")

    monkeypatch.setattr(PLACEMENTS, "_records", forbidden)
    with pytest.raises(ArgumentError, match="min_matches"):
        get_rigid_feature_placements(
            object(),
            features(),
            [] if empty else [PAIRS],
            min_matches=2,
            skip_digestion=skip,
            **options(),
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "bad",
    [
        np.array([[0, 0], [1, 1]]),
        np.array([[0, 0], [1, 1], [1, 2]]),
        np.array([[0, 0], [1, 1], [2, -1]]),
        np.array([[0, 0], [1, 1], [2, 2**64 - 1]], dtype=np.uint64),
    ],
)
def test_all_mappings_refuse_malformed_later_alternative_before_inventory(
    skip, bad, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("A malformed later mapping cannot cause even the first fit")

    monkeypatch.setattr(PLACEMENTS, "_records", forbidden)
    monkeypatch.setattr(PLACEMENTS, "_fit_feature_mapping", forbidden)
    with pytest.raises(ArgumentError, match="correspondence"):
        get_rigid_feature_placements(
            object(), features(), [PAIRS, bad], skip_digestion=skip, **options()
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize(
    "argument, amount, unit",
    [
        ("distance_tolerance", 0, "nm"),
        ("distance_tolerance", float("nan"), "nm"),
        ("direction_tolerance", -1, "degrees"),
        ("direction_tolerance", 181, "degrees"),
    ],
)
def test_physical_criteria_remain_native_even_for_empty_placement(
    skip, empty, argument, amount, unit, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid physical criteria cannot reach inventory or fitting")

    monkeypatch.setattr(PLACEMENTS, "_records", forbidden)
    with pytest.raises(ArgumentError, match=argument):
        get_rigid_feature_placements(
            object(),
            features(),
            [] if empty else [PAIRS],
            skip_digestion=skip,
            **options(),
            **{argument: puw.quantity(amount, unit)},
        )


@pytest.mark.parametrize("skip", [False, True])
def test_scheduled_fit_limit_refuses_before_any_inventory_acquisition(
    skip, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Exhausted fit capacity cannot acquire inventory or fit")

    monkeypatch.setattr(PLACEMENTS, "_records", forbidden)
    monkeypatch.setattr(PLACEMENTS, "_source_inventory", forbidden)
    with pytest.raises(CliqueLimitError) as caught:
        get_rigid_feature_placements(
            object(),
            features(),
            [PAIRS, PAIRS],
            max_fits=1,
            skip_digestion=skip,
            **options(),
        )
    assert caught.value.code == "PHMT-E107"


@pytest.mark.parametrize("skip", [False, True])
def test_valid_empty_request_retains_zero_fits_and_real_query_child_admission(
    skip, monkeypatch
):
    calls = []
    original = PLACEMENTS.from_feature_inventory

    def query(*args, **kwargs):
        assert "skip_digestion" not in kwargs
        calls.append("default")
        return original(*args, **kwargs)

    def forbidden(*args, **kwargs):
        pytest.fail("An empty cached request cannot fit or extract a molecular system")

    monkeypatch.setattr(PLACEMENTS, "from_feature_inventory", query)
    monkeypatch.setattr(PLACEMENTS, "get_features", forbidden)
    monkeypatch.setattr(PLACEMENTS, "_fit_feature_mapping", forbidden)
    result = get_rigid_feature_placements(
        object(),
        features(),
        [],
        max_fits=np.int64(1),
        max_matrix_entries=np.int64(1),
        skip_digestion=skip,
        **options(),
    )
    assert result["complete"] and result["placements"] == []
    assert result["report"]["n_fits"] == 0
    assert (
        result["report"]["accepted_placements"]
        == result["report"]["rejected_placements"]
        == []
    )
    assert (
        result["report"]["criteria"]["completion_scope"]
        == "explicit_supplied_mappings_only"
    )
    assert calls == ["default"]


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("violation", ["range", "state", "chemistry"])
def test_native_alignment_axis_and_chemistry_guards_stay_before_fit(
    skip, violation, monkeypatch
):
    source, _ = ionic_case()
    cached = get_features(source, features=["positive charge"])
    target = deepcopy(cached)
    pairs = PAIRS.copy()
    if violation == "range":
        pairs[0, 1] = 99
    elif violation == "state":
        cached["chemical_state"] = 1
    else:
        target["features"][0]["kind"] = "negative charge"

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid native axes/chemistry cannot fit")

    monkeypatch.setattr(msm.structure, "least_rmsd_fit", forbidden)
    with pytest.raises(ArgumentError):
        get_rigid_feature_placements(
            source,
            target,
            [pairs],
            features=["positive charge", "negative charge"],
            feature_inventory=cached,
            skip_digestion=skip,
        )


@pytest.mark.parametrize("skip", [False, True])
def test_actual_provider_failure_is_not_an_empty_placement_or_fallback(
    skip, monkeypatch
):
    source, _ = ionic_case()
    cached = get_features(source, features=["positive charge"])
    failure = RuntimeError("actual placement fit provider failure")

    def broken(*args, **kwargs):
        raise failure

    monkeypatch.setattr(msm.structure, "least_rmsd_fit", broken)
    with pytest.raises(RuntimeError) as caught:
        get_rigid_feature_placements(
            source,
            cached,
            [PAIRS],
            feature_inventory=cached,
            features=["positive charge"],
            skip_digestion=skip,
        )
    assert caught.value is failure


@pytest.mark.parametrize("skip", [False, True])
def test_exhausted_post_fit_assignment_budget_is_failure_not_empty_success(skip):
    source, _ = ionic_case()
    cached = get_features(source, features=["positive charge"])
    with pytest.raises(ConsensusLimitError) as caught:
        get_rigid_feature_placements(
            source,
            cached,
            [PAIRS],
            feature_inventory=cached,
            features=["positive charge"],
            max_matrix_entries=1,
            skip_digestion=skip,
        )
    assert caught.value.code == "PHMT-E106"


@pytest.mark.parametrize("skip", [False, True])
def test_completed_but_insufficient_full_inventory_matching_retains_rejection(skip):
    source, _ = ionic_case()
    cached = get_features(source, features=["positive charge"])
    result = get_rigid_feature_placements(
        source,
        cached,
        [PAIRS],
        feature_inventory=cached,
        features=["positive charge"],
        min_matches=4,
        skip_digestion=skip,
    )
    assert result["complete"] and result["placements"] == []
    assert result["report"]["n_fits"] == 1
    (rejected,) = result["report"]["rejected_placements"]
    assert rejected["reason"] == "post_fit_geometry_or_match_count"
    assert len(rejected["matches"]["matches"]) == 3
    assert rejected["invalid_seed_pairs"] == []


@pytest.mark.parametrize("skip", [False, True])
def test_changed_post_fit_feature_membership_still_refuses(skip, monkeypatch):
    source, _ = ionic_case()
    cached = get_features(source, features=["positive charge"])
    original = PLACEMENTS.get_features

    def changed(*args, **kwargs):
        assert "skip_digestion" not in kwargs
        result = original(*args, **kwargs)
        result["features"].reverse()
        return result

    monkeypatch.setattr(PLACEMENTS, "get_features", changed)
    with pytest.raises(ArgumentError, match="changed feature identities"):
        get_rigid_feature_placements(
            source,
            cached,
            [PAIRS],
            feature_inventory=cached,
            features=["positive charge"],
            skip_digestion=skip,
        )


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("cached", [False, True])
def test_real_proper_duplicate_placements_keep_children_frame_state_units_and_custody(
    unit, cached, monkeypatch
):
    with puw.context(standard_units=[unit, "ps", "radians"]):
        source = system("[Na+].[K+].[Li+].[Cl-]", [*CENTERS, [4, 5, 6]])
        add_declared_state(source, [1, 1, 1, -1])
        source.structures.append(coordinates=msm.get(source, coordinates=True))
        indices = [2, 0, 1]
        target = get_features(
            source,
            selection=indices,
            structure_index=1,
            chemical_state=1,
            features=["positive charge"],
        )
        source = msm.structure.rotate(
            source,
            selection=indices,
            structure_indices=[1],
            rotation=np.array([[0.0, -1, 0], [1, 0, 0], [0, 0, 1]]),
            rotation_center=puw.quantity([0, 0, 0], "nm"),
            in_place=False,
        )
        source = msm.structure.translate(
            source,
            selection=indices,
            structure_indices=[1],
            translation=puw.quantity([[[2.0, 1, 3]]], "nm"),
            in_place=False,
        )
        source_inventory = get_features(
            source,
            selection=indices,
            structure_index=1,
            chemical_state=1,
            features=["positive charge"],
        )
        before_inventory = deepcopy(source_inventory)
        before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
        calls = {
            name: []
            for name in (
                "align_to_pharmacophore",
                "get_features",
                "from_feature_inventory",
                "evaluate_feature_correspondence",
                "get_aligned_feature_matches",
            )
        }

        def observe(name, original):
            @wraps(original)
            def child(*args, **kwargs):
                assert "skip_digestion" not in kwargs
                calls[name].append("default")
                return original(*args, **kwargs)

            return child

        for name in calls:
            monkeypatch.setattr(
                PLACEMENTS, name, observe(name, getattr(PLACEMENTS, name))
            )
        with ackredit.session("proper duplicate placements") as application:
            for controls in ({}, {"skip_digestion": False}, {"skip_digestion": True}):
                with (
                    ackredit.capture("one placement operation") as capture,
                    phmt.attribution(),
                ):
                    result = get_rigid_feature_placements(
                        source,
                        target,
                        [PAIRS, PAIRS],
                        feature_inventory=source_inventory if cached else None,
                        selection=indices,
                        structure_index=1,
                        chemical_state=1,
                        features=["positive charge"],
                        distance_tolerance=puw.quantity(0.02, "nm"),
                        max_fits=2,
                        **controls,
                    )
                assert ackredit.current_session() is application
                assert result["complete"] and result["report"]["n_fits"] == 2
                assert [p["proposal_index"] for p in result["placements"]] == [0, 1]
                assert result["report"]["rejected_placements"] == []
                assert result["attribution"]["status"] == "captured"
                credit = json.dumps(capture.attribution.to_dict())
                assert (
                    "get_rigid_feature_placements" in credit
                    and "least_rmsd_fit" in credit
                )
                for placement in result["placements"]:
                    assert placement["molecular_system"] is not source
                    assert len(placement["matches"]["matches"]) == 3
                    assert placement["pair_evaluation"]["all_pairs_valid"]
                    assert [
                        row["pair"]
                        for row in placement["pair_evaluation"]["pair_tests"]
                    ] == PAIRS.tolist()
                    after = puw.get_value(
                        msm.get(placement["molecular_system"], coordinates=True),
                        to_unit="nm",
                    )
                    np.testing.assert_allclose(after[1, :3], CENTERS, atol=1e-12)
                    np.testing.assert_array_equal(after[0], before[0])
                    np.testing.assert_array_equal(after[:, 3], before[:, 3])
                    assert placement["alignment"]["selected_atom_indices"] == indices
                saved = json.loads(json.dumps(result["report"], allow_nan=False))
                result["placements"][0]["inventory"]["features"].clear()
                assert result["report"] == saved
        assert {name: len(events) for name, events in calls.items()} == {
            "align_to_pharmacophore": 6,
            "get_features": 6 if cached else 9,
            "from_feature_inventory": 3,
            "evaluate_feature_correspondence": 6,
            "get_aligned_feature_matches": 6,
        }
        np.testing.assert_array_equal(
            puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
        )
        assert (
            source_inventory["selected_atom_indices"]
            == before_inventory["selected_atom_indices"]
            == indices
        )
        for record, original in zip(
            source_inventory["features"], before_inventory["features"]
        ):
            assert record["atom_indices"] == original["atom_indices"]
            assert puw.get_unit(record["center"]) == puw.get_unit(original["center"])
            np.testing.assert_array_equal(
                puw.get_value(record["center"], to_unit="nm"),
                puw.get_value(original["center"], to_unit="nm"),
            )
        np.testing.assert_array_equal(PAIRS, [[2, 2], [0, 0], [1, 1]])
