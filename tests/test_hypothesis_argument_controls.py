"""Hypothesis admission retains shared support, occurrence custody and finite search."""

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
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError, CliqueLimitError
from pharmacophoremt.modeler import get_aligned_consensus_hypotheses
from phmt_test_support.absence_inputs import inventory
from tests.test_aligned_cliques import exhaustive_packages
from tests.test_aligned_model_argument_controls import prepared

OWNER = importlib.import_module("pharmacophoremt.modeler.aligned_cliques")


def empty_sources():
    return [inventory([]), inventory([])]


def test_explicit_keyword_only_closed_definition_owned_export():
    assert (
        phmt.modeler.get_aligned_consensus_hypotheses
        is get_aligned_consensus_hypotheses
    )
    control = inspect.signature(get_aligned_consensus_hypotheses).parameters[
        "skip_digestion"
    ]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY and control.default is False
    plan = get_aligned_consensus_hypotheses.digestion_plan
    assert plan.contract_owner == "definition"
    assert plan.contract_caller == OWNER.__name__ + ".get_aligned_consensus_hypotheses"
    assert (
        describe_contract(plan.contracts.resolve(plan.contract_caller), plan.domains)[
            "admits"
        ]
        == "signature"
    )


@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_discovery(flag, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid control reached discovery")

    monkeypatch.setattr(OWNER, "get_aligned_feature_cliques", forbidden)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        get_aligned_consensus_hypotheses(
            empty_sources(), ligand_ids=["a", "b"], skip_digestion=flag
        )


@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
def test_only_literal_true_bypasses_ordinary_control_digestion(flag, monkeypatch):
    seen = []
    original = _contracts._boolean

    def boolean(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    class ReachedDiscovery(Exception):
        pass

    def reached(*args, **kwargs):
        raise ReachedDiscovery

    monkeypatch.setattr(_contracts, "_boolean", boolean)
    monkeypatch.setattr(OWNER, "get_aligned_feature_cliques", reached)
    with pytest.raises(ReachedDiscovery):
        get_aligned_consensus_hypotheses(
            empty_sources(), ligand_ids=["a", "b"], skip_digestion=flag
        )
    assert len(seen) == (0 if flag is True else 1)
    if flag is not True:
        assert seen[0] is flag


@pytest.mark.parametrize("skip", [False, True])
def test_inventory_collection_remains_required(skip):
    with pytest.raises(TypeError):
        get_aligned_consensus_hypotheses(ligand_ids=["a", "b"], skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_ligand_identities_remain_required(skip):
    with pytest.raises(TypeError):
        get_aligned_consensus_hypotheses(empty_sources(), skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_unknown_keyword_stays_closed_before_discovery(skip, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Unknown keyword reached discovery")

    monkeypatch.setattr(OWNER, "get_aligned_feature_cliques", forbidden)
    with pytest.raises(TypeError):
        get_aligned_consensus_hypotheses(
            empty_sources(), ligand_ids=["a", "b"], unknown=True, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "option",
    ["min_support", "min_sites", "max_graph_nodes", "max_cliques", "max_combinations"],
)
@pytest.mark.parametrize("value", [0, -1, True, np.bool_(True), 1.5])
def test_native_integer_domains_precede_discovery_even_empty(
    skip, option, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid count or budget reached discovery")

    monkeypatch.setattr(OWNER, "get_aligned_feature_cliques", forbidden)
    with pytest.raises(ArgumentError, match=option):
        get_aligned_consensus_hypotheses(
            empty_sources(),
            ligand_ids=["a", "b"],
            skip_digestion=skip,
            **{option: value},
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "option,value",
    [
        ("distance_tolerance", "0 nm"),
        ("distance_tolerance", "-1 nm"),
        ("distance_tolerance", "nan nm"),
        ("distance_tolerance", "inf nm"),
        ("distance_tolerance", "1 ps"),
        ("direction_tolerance", "-1 degrees"),
        ("direction_tolerance", "181 degrees"),
        ("direction_tolerance", "nan degrees"),
        ("direction_tolerance", "inf degrees"),
        ("direction_tolerance", "1 nm"),
    ],
)
def test_native_physical_domains_precede_discovery_even_empty(
    skip, option, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid physical criterion reached discovery")

    monkeypatch.setattr(OWNER, "get_aligned_feature_cliques", forbidden)
    with pytest.raises(ArgumentError, match=option):
        get_aligned_consensus_hypotheses(
            empty_sources(),
            ligand_ids=["a", "b"],
            skip_digestion=skip,
            **{option: value},
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("sources", [None, [], {}])
def test_invalid_inventory_collection_cannot_complete_empty(skip, sources):
    with pytest.raises(ArgumentError, match="feature_inventories"):
        get_aligned_consensus_hypotheses(
            sources, ligand_ids=["a", "b"], skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("identities", [[], ["a", "a"], ["a", None], "ab"])
def test_invalid_identities_cannot_complete_empty(skip, identities):
    with pytest.raises(ArgumentError, match="ligand_ids"):
        get_aligned_consensus_hypotheses(
            empty_sources(), ligand_ids=identities, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("identities,minimum", [(["a"], 1), (["a", "b"], 3)])
def test_count_and_attainable_support_precede_discovery(
    skip, identities, minimum, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid source count/support reached discovery")

    monkeypatch.setattr(OWNER, "get_aligned_feature_cliques", forbidden)
    with pytest.raises(ArgumentError, match="ligand_ids/min_support"):
        get_aligned_consensus_hypotheses(
            empty_sources(),
            ligand_ids=identities,
            min_support=minimum,
            skip_digestion=skip,
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("kind", ["hb donor", "hb acceptor"])
def test_native_child_validates_malformed_later_geometry_during_bypass(
    skip, kind, monkeypatch
):
    bad = inventory([[0, 0, 0]], [kind])
    if kind == "hb acceptor":
        bad["features"][0]["center"] = puw.quantity([np.nan, 0, 0], "nm")

    def forbidden(*args, **kwargs):
        pytest.fail("Malformed native geometry reached package enumeration")

    monkeypatch.setattr(OWNER, "_packages", forbidden)
    with pytest.raises(ArgumentError):
        get_aligned_consensus_hypotheses(
            [inventory([]), bad], ligand_ids=["a", "b"], skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
def test_original_discovery_exception_remains_failed_not_empty(skip, monkeypatch):
    error = RuntimeError("original discovery failure")

    def failing(*args, **kwargs):
        assert "skip_digestion" not in kwargs
        raise error

    monkeypatch.setattr(OWNER, "get_aligned_feature_cliques", failing)
    with pytest.raises(RuntimeError) as caught:
        get_aligned_consensus_hypotheses(
            empty_sources(), ligand_ids=["a", "b"], skip_digestion=skip
        )
    assert caught.value is error


@pytest.mark.parametrize("skip", [False, True])
def test_later_aggregation_failure_never_publishes_partial_hypotheses(
    skip, monkeypatch
):
    error = RuntimeError("original later aggregation failure")
    original = OWNER.get_consensus_sites
    calls = []

    def failing(*args, **kwargs):
        assert "skip_digestion" not in kwargs
        calls.append(kwargs)
        if len(calls) == 2:
            raise error
        return original(*args, **kwargs)

    def forbidden(*args, **kwargs):
        pytest.fail("Partially aggregated work reached package enumeration")

    monkeypatch.setattr(OWNER, "get_consensus_sites", failing)
    monkeypatch.setattr(OWNER, "_packages", forbidden)
    with pytest.raises(RuntimeError) as caught:
        get_aligned_consensus_hypotheses(
            [inventory([[0, 0, 0], [1, 0, 0]]) for _ in range(2)],
            ligand_ids=["a", "b"],
            skip_digestion=skip,
        )
    assert caught.value is error and len(calls) == 2


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "option,value,stage",
    [("max_graph_nodes", 1, "feature_graph"), ("max_cliques", 1, "feature_cliques")],
)
def test_actual_child_limits_raise_before_packages(
    skip, option, value, stage, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Unresolved discovery reached package enumeration")

    monkeypatch.setattr(OWNER, "_packages", forbidden)
    with pytest.raises(CliqueLimitError) as caught:
        get_aligned_consensus_hypotheses(
            [inventory([[0, 0, 0], [1, 0, 0]]) for _ in range(2)],
            ligand_ids=["a", "b"],
            skip_digestion=skip,
            **{option: value},
        )
    assert caught.value.code == "PHMT-E107"
    assert (
        caught.value.extra["stage"] == stage and caught.value.extra["complete"] is False
    )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("minimum", [1, 2])
def test_occurrence_reuse_stays_alternative_and_rejected_extensions_consume_budget(
    skip, minimum
):
    sources = [inventory([[0, 0, 0], [0, 0, 0]]), inventory([[0.05, 0, 0]])]
    result = get_aligned_consensus_hypotheses(
        sources,
        ligand_ids=["a", "b"],
        min_sites=np.int64(minimum),
        max_combinations=np.int64(3),
        skip_digestion=skip,
    )
    assert result["complete"] and result["n_combinations"] == 3
    assert len(result["candidate_sites"]) == 2
    assert [item["site_indices"] for item in result["hypotheses"]] == (
        [[0], [1]] if minimum == 1 else []
    )
    if minimum == 1:
        assert {
            frozenset(item["site_indices"]) for item in result["hypotheses"]
        } == exhaustive_packages(result["correspondence_groups"], 2)
    with pytest.raises(CliqueLimitError) as caught:
        get_aligned_consensus_hypotheses(
            sources,
            ligand_ids=["a", "b"],
            min_sites=minimum,
            max_combinations=2,
            skip_digestion=skip,
        )
    expected = dict(
        stage="hypothesis_combinations",
        resource="candidate extensions",
        observed=3,
        limit=2,
        complete=False,
    )
    assert caught.value.code == "PHMT-E107"
    assert {key: caught.value.extra[key] for key in expected} == expected


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_joint_intersection_maximality_and_empty_denominators_match_subset_oracle(
    skip, unit, monkeypatch
):
    kinds = ["hydrophobicity", "hb acceptor", "positive charge"]
    memberships = [(0, 2), (0, 1), (0, 1, 2), (1, 2)]
    sources = [
        inventory([[j, 0, 0] for j in member], [kinds[j] for j in member])
        for member in memberships
    ] + [inventory([])]
    identities = ["d", "b", "a", "c", "empty"]
    for source in sources:
        for record in source["features"]:
            record["center"] = puw.quantity(
                puw.get_value(record["center"], to_unit=unit), unit
            )
    before = deepcopy(detached(sources))

    def forbidden(*args, **kwargs):
        pytest.fail("Inventory hypothesis construction must not read or fit molecules")

    monkeypatch.setattr(msm, "get", forbidden)
    monkeypatch.setattr(msm.structure, "least_rmsd_fit", forbidden)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = deepcopy(puw.configure.get_standard_units())
        result = get_aligned_consensus_hypotheses(
            sources,
            ligand_ids=identities,
            min_sites=2,
            max_combinations=7,
            skip_digestion=skip,
        )
        assert puw.configure.get_standard_units() == policy
        assert result["complete"] and result["n_combinations"] == 7
        assert len(result["candidate_sites"]) == len(result["hypotheses"]) == 3
        assert (
            {frozenset(item["site_indices"]) for item in result["hypotheses"]}
            == exhaustive_packages(result["correspondence_groups"], 2)
            == {frozenset(pair) for pair in [(0, 1), (0, 2), (1, 2)]}
        )
        assert [item["hypothesis_id"] for item in result["hypotheses"]] == [
            f"hypothesis_{i:05d}" for i in range(3)
        ]
        for item in result["hypotheses"]:
            groups = [
                result["correspondence_groups"][index] for index in item["site_indices"]
            ]
            common = set(identities[i] for i, _ in groups[0])
            for group in groups[1:]:
                common.intersection_update(identities[i] for i, _ in group)
            assert item["joint_ligand_ids"] == sorted(common)
            assert item["joint_support_count"] == 2 and item[
                "joint_support_fraction"
            ] == pytest.approx(2 / 5)
            members = [tuple(pair) for group in groups for pair in group]
            assert len(members) == len(set(members))
        assert all(
            site["support_count"] == 3
            and site["support_fraction"] == pytest.approx(3 / 5)
            for site in result["candidate_sites"]
        )
        np.testing.assert_allclose(
            sorted(
                tuple(puw.get_value(site["center"], to_unit="nm"))
                for site in result["candidate_sites"]
            ),
            [[0, 0, 0], [1, 0, 0], [2, 0, 0]],
        )
        assert "skip_digestion" not in result["criteria"]
        assert (
            result["criteria"]["hypothesis_support"]
            == "intersection_of_site_supporters"
        )
        impossible = get_aligned_consensus_hypotheses(
            sources, ligand_ids=identities, min_sites=3, skip_digestion=skip
        )
        assert impossible["complete"] and impossible["hypotheses"] == []
    assert detached(sources) == before
    snapshot = deepcopy(detached(result))
    identities[0] = "changed"
    sources[2]["features"][0]["atom_indices"][0] = 99
    assert detached(result) == snapshot


@pytest.mark.parametrize("skip", [False, True])
def test_empty_negative_and_reused_credit_are_observed_by_application(skip):
    with ackredit.session("hypothesis controls"), phmt.attribution():
        with ackredit.capture("empty") as capture:
            empty = get_aligned_consensus_hypotheses(
                empty_sources(),
                ligand_ids=["a", "b"],
                min_sites=9,
                max_combinations=1,
                skip_digestion=skip,
            )
        assert (
            empty["complete"]
            and empty["n_combinations"] == 0
            and empty["hypotheses"] == []
        )
        assert "10.1145/362342.362367" not in json.dumps(capture.attribution.to_dict())
        for label in ("new", "reused"):
            with ackredit.capture(label) as capture:
                negative = get_aligned_consensus_hypotheses(
                    [inventory([[0, 0, 0]]), inventory([[1, 0, 0]])],
                    ligand_ids=["a", "b"],
                    skip_digestion=skip,
                )
            assert (
                negative["complete"]
                and negative["n_combinations"] == 0
                and negative["hypotheses"] == []
            )
            assert "10.1145/362342.362367" in json.dumps(capture.attribution.to_dict())
            assert "10.1145/362342.362367" in json.dumps(negative["attribution"])


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_real_prepared_frames_state_selection_and_children_keep_independent_admission(
    skip, unit, monkeypatch
):
    ligands = prepared()
    originals = [
        puw.get_value(
            msm.get(item["molecular_system"], coordinates=True), to_unit="nm"
        ).copy()
        for item in ligands
    ]
    calls = {
        name: [] for name in ("get_aligned_feature_cliques", "get_consensus_sites")
    }
    for name in calls:
        original = getattr(OWNER, name)

        def spy(operation, child):
            @wraps(operation)
            def observed(*args, **kwargs):
                assert "skip_digestion" not in kwargs
                calls[child].append(kwargs.copy())
                return operation(*args, **kwargs)

            return observed

        monkeypatch.setattr(OWNER, name, spy(original, name))
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = deepcopy(puw.configure.get_standard_units())
        sources = [
            phmt.modeler.get_features(
                item["molecular_system"],
                features=["positive charge"],
                **{
                    key: value
                    for key, value in item.items()
                    if key not in {"molecular_system", "ligand_id"}
                },
            )
            for item in ligands
        ]
        before = deepcopy(detached(sources))
        result = get_aligned_consensus_hypotheses(
            sources,
            ligand_ids=[item["ligand_id"] for item in ligands],
            min_sites=3,
            skip_digestion=skip,
        )
        assert puw.configure.get_standard_units() == policy
        assert result["complete"] and len(result["hypotheses"]) == 1
        assert (
            len(calls["get_aligned_feature_cliques"]) == 1
            and len(calls["get_consensus_sites"]) == 3
        )
        assert result["hypotheses"][0]["joint_ligand_ids"] == ["reference", "shifted"]
        assert result["hypotheses"][0]["joint_support_fraction"] == pytest.approx(2 / 3)
        assert all(
            site["support_count"] == 2
            and site["support_fraction"] == pytest.approx(2 / 3)
            for site in result["candidate_sites"]
        )
        np.testing.assert_allclose(
            sorted(
                tuple(puw.get_value(site["center"], to_unit="nm"))
                for site in result["candidate_sites"]
            ),
            [[0.0625, 0, 0], [0.0625, 1, 0], [1.0625, 0, 0]],
        )
        assert sources[0]["selected_atom_indices"] == [2, 0, 1]
        assert sources[0]["structure_index"] == 1 and sources[1]["structure_index"] == 0
        assert sources[0]["chemical_state"] == sources[1]["chemical_state"] == 1
        assert sources[2]["features"] == [] and detached(sources) == before
    for item, coordinates in zip(ligands, originals):
        np.testing.assert_array_equal(
            puw.get_value(
                msm.get(item["molecular_system"], coordinates=True), to_unit="nm"
            ),
            coordinates,
        )
