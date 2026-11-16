"""Aligned assignment and aggregation retain native semantics during bypass."""

import importlib
import inspect
import json
from copy import deepcopy

import ackredit
import molsysmt as msm
import numpy as np
import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    ConsensusLimitError,
)
from pharmacophoremt.modeler import get_aligned_feature_matches, get_consensus_sites
from phmt_test_support.absence_inputs import inventory

OWNER = importlib.import_module("pharmacophoremt.modeler.aligned_consensus")
OPERATIONS = [get_aligned_feature_matches, get_consensus_sites]


def features():
    return inventory([[0, 0, 0], [0.125, 0, 0]])


def arguments(operation, empty=True):
    if operation is get_aligned_feature_matches:
        return (features(), inventory([]) if empty else features()), {}
    return ([features(), features()], [] if empty else [[[0, 0], [1, 0]]]), {
        "ligand_ids": ["a", "b"]
    }


@pytest.mark.parametrize("operation", OPERATIONS)
def test_explicit_keyword_only_closed_definition_owned_exports(operation):
    assert getattr(phmt.modeler, operation.__name__) is operation
    control = inspect.signature(operation).parameters["skip_digestion"]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY and control.default is False
    plan = operation.digestion_plan
    assert plan.contract_owner == "definition"
    assert plan.contract_caller == OWNER.__name__ + "." + operation.__name__
    assert (
        describe_contract(plan.contracts.resolve(plan.contract_caller), plan.domains)[
            "admits"
        ]
        == "signature"
    )


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_native_inventory(operation, flag, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid control reached native inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    args, options = arguments(operation)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        operation(*args, **options, skip_digestion=flag)


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
    args, options = arguments(operation)
    assert operation(*args, **options, skip_digestion=flag)["complete"]
    assert len(seen) == (0 if flag is True else 1)
    if flag is not True:
        assert seen[0] is flag


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("count", [0, 1])
def test_required_inputs_stay_required_with_canonical_supplied_values(
    operation, skip, count
):
    args, options = arguments(operation)
    with pytest.raises(TypeError):
        operation(*args[:count], **options, skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_aggregation_ligand_identities_remain_required(skip):
    with pytest.raises(TypeError):
        get_consensus_sites([features(), features()], [], skip_digestion=skip)


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("skip", [False, True])
def test_unknown_keyword_stays_closed_before_inventory(operation, skip, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Unknown keyword reached inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    args, options = arguments(operation)
    with pytest.raises(TypeError):
        operation(*args, **options, unexpected=True, skip_digestion=skip)


@pytest.mark.parametrize("operation", OPERATIONS)
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
def test_native_physical_criteria_refuse_even_empty_before_inventory(
    operation, skip, option, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid physical criterion reached inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    args, options = arguments(operation)
    with pytest.raises(ArgumentError, match=option):
        operation(*args, **options, **{option: value}, skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize("value", [0, -1, True, 1.5])
def test_native_matrix_domain_precedes_inventory_even_when_empty(
    skip, empty, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid budget reached inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match="max_matrix_entries"):
        get_aligned_feature_matches(
            features(),
            inventory([]) if empty else features(),
            max_matrix_entries=value,
            skip_digestion=skip,
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("empty", [False, True])
@pytest.mark.parametrize("value", [0, -1, True, 1.5])
def test_native_support_domain_precedes_inventory_even_for_no_groups(
    skip, empty, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid minimum support reached inventory")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match="min_support"):
        get_consensus_sites(
            [features(), features()],
            [] if empty else [[[0, 0], [1, 0]]],
            ligand_ids=["a", "b"],
            min_support=value,
            skip_digestion=skip,
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("identities", [[], ["a", "a"], ["a", None], "ab"])
def test_invalid_ligand_identities_refuse_even_without_groups(skip, identities):
    with pytest.raises(ArgumentError, match="ligand_ids"):
        get_consensus_sites(
            [features(), features()], [], ligand_ids=identities, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("collection", [None, [], {}])
def test_invalid_inventory_collection_cannot_complete_empty(skip, collection):
    with pytest.raises(ArgumentError, match="feature_inventories"):
        get_consensus_sites(collection, [], ligand_ids=["a", "b"], skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "groups",
    [
        None,
        {},
        [[]],
        [[[-1, 0]]],
        [[[0.0, 0.0]]],
        [[[False, False]]],
        [[[0, 0], [0, 1]]],
        [[[0, 0]], [[0, 0]]],
        [[[2, 0]]],
        [[[0, 2]]],
    ],
)
def test_invalid_or_reused_occurrence_groups_cannot_publish_partial_sites(skip, groups):
    with pytest.raises(ArgumentError, match="correspondence_groups"):
        get_consensus_sites(
            [features(), features()],
            groups,
            ligand_ids=["a", "b"],
            min_support=1,
            skip_digestion=skip,
        )


@pytest.mark.parametrize("skip", [False, True])
def test_identity_count_support_and_mixed_kinds_keep_native_authority(skip):
    first, second = features(), inventory([[0, 0, 0]], ["positive charge"])
    for identities, minimum in ((["a"], 1), (["a", "b"], 3)):
        with pytest.raises(ArgumentError, match="ligand_ids/min_support"):
            get_consensus_sites(
                [first, second],
                [],
                ligand_ids=identities,
                min_support=minimum,
                skip_digestion=skip,
            )
    with pytest.raises(ArgumentError, match="one common feature kind"):
        get_consensus_sites(
            [first, second],
            [[[0, 0], [1, 0]]],
            ligand_ids=["a", "b"],
            skip_digestion=skip,
        )


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize("skip", [False, True])
def test_native_inventory_geometry_is_checked_even_empty_work(operation, skip):
    bad = inventory([[0, 0, 0]], ["hb donor"])
    args, options = (
        ((features(), bad), {})
        if operation is get_aligned_feature_matches
        else (([features(), bad], []), {"ligand_ids": ["a", "b"]})
    )
    with pytest.raises(ArgumentError):
        operation(*args, **options, skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_original_allocation_failure_precedes_assignment(skip, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Exhausted assignment matrix budget reached the solver")

    monkeypatch.setattr(OWNER, "linear_sum_assignment", forbidden)
    with pytest.raises(ConsensusLimitError) as caught:
        get_aligned_feature_matches(
            features(), features(), max_matrix_entries=7, skip_digestion=skip
        )
    assert caught.value.code == "PHMT-E106"
    assert (
        caught.value.extra["matrix_entries"] == 8
        and caught.value.extra["max_matrix_entries"] == 7
    )


@pytest.mark.parametrize("skip", [False, True])
def test_original_assignment_exception_is_preserved(skip, monkeypatch):
    error = RuntimeError("Original aligned assignment failure")

    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(OWNER, "linear_sum_assignment", fail)
    with pytest.raises(RuntimeError) as caught:
        get_aligned_feature_matches(features(), features(), skip_digestion=skip)
    assert caught.value is error


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("axes", [(0, 2), (2, 0), (0, 0)])
def test_completed_empty_axes_preserve_unmatched_indices_without_unused_budget(
    skip, axes, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Empty axes reached the solver")

    monkeypatch.setattr(OWNER, "linear_sum_assignment", forbidden)
    first, second = [inventory([[i, 0, 0] for i in range(size)]) for size in axes]
    result = get_aligned_feature_matches(
        first, second, max_matrix_entries=1, skip_digestion=skip
    )
    assert (
        result["complete"]
        and result["matches"] == []
        and result["n_matrix_entries"] == 0
    )
    assert result["unmatched_reference"] == list(range(axes[0]))
    assert result["unmatched_candidate"] == list(range(axes[1]))


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_unique_maximum_cardinality_oracle_preserves_types_policy_and_source(
    skip, unit, monkeypatch
):
    first = features()
    second = inventory(
        [[0.0625, 0, 0], [-0.0625, 0, 0], [0, 0, 0]],
        ["hb acceptor", "hb acceptor", "positive charge"],
    )
    for source in (first, second):
        for record in source["features"]:
            record["center"] = puw.quantity(
                puw.get_value(record["center"], to_unit=unit), unit
            )
    before = deepcopy(detached([first, second]))

    def forbidden(*args, **kwargs):
        pytest.fail("Inventory matching must not read or fit molecular systems")

    monkeypatch.setattr(msm, "get", forbidden)
    monkeypatch.setattr(msm.structure, "least_rmsd_fit", forbidden)
    tolerance = puw.quantity(0.125 if unit == "nm" else 125, unit)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = deepcopy(puw.configure.get_standard_units())
        result = get_aligned_feature_matches(
            first,
            second,
            distance_tolerance=tolerance,
            max_matrix_entries=np.int64(10),
            skip_digestion=skip,
        )
        assert puw.configure.get_standard_units() == policy
    assert result["matches"] == [[0, 1], [1, 0]]
    assert result["unmatched_reference"] == [] and result["unmatched_candidate"] == [2]
    assert result["n_matrix_entries"] == 10 and result["complete"]
    assert (
        detached([first, second]) == before
        and "skip_digestion" not in result["criteria"]
    )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_centroid_support_rejection_and_original_members_have_independent_answers(
    skip, unit, monkeypatch
):
    first = inventory([[0, 0, 0], [2, 0, 0]])
    second = inventory([[0.125, 0, 0], [2.5, 0, 0]])
    sources = [first, second, inventory([])]
    first["structure_index"] = second["structure_index"] = 1
    second["chemical_state"] = 1
    identities = ["a", "b", "empty"]
    groups = [[[0, 0], [1, 0]], [[0, 1], [1, 1]]]
    for source in sources:
        for record in source["features"]:
            record["center"] = puw.quantity(
                puw.get_value(record["center"], to_unit=unit), unit
            )
    before = deepcopy(detached(sources)), deepcopy(groups)

    def forbidden(*args, **kwargs):
        pytest.fail("Site aggregation must not read molecular systems")

    monkeypatch.setattr(msm, "get", forbidden)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = deepcopy(puw.configure.get_standard_units())
        result = get_consensus_sites(
            sources,
            groups,
            ligand_ids=identities,
            distance_tolerance="0.1 nm",
            skip_digestion=skip,
        )
        assert puw.configure.get_standard_units() == policy
    assert (
        result["complete"]
        and len(result["sites"]) == len(result["rejected_groups"]) == 1
    )
    site, rejected = result["sites"][0], result["rejected_groups"][0]
    np.testing.assert_allclose(
        puw.get_value(site["center"], to_unit="nm"), [0.0625, 0, 0], atol=1e-14
    )
    assert site["support_count"] == 2 and site["support_fraction"] == pytest.approx(
        2 / 3
    )
    assert float(puw.get_value(site["position_rmsd"], to_unit="nm")) == pytest.approx(
        0.0625
    )
    assert rejected["reasons"] == ["position_dispersion"]
    assert float(
        puw.get_value(rejected["maximum_center_deviation"], to_unit="nm")
    ) == pytest.approx(0.25)
    assert (
        site["members"][0]["structure_index"] == 1
        and site["members"][1]["chemical_state"] == 1
    )
    assert (detached(sources), groups) == before and "skip_digestion" not in result[
        "criteria"
    ]
    first["features"][0]["atom_indices"][0] = 99
    groups[0].clear()
    identities.clear()
    assert site["members"][0]["atom_indices"] == [0]
    assert (
        site["members"][0]["geometry"]["center"]
        == before[0][0]["features"][0]["center"]
    )
    assert result["ligand_ids"] == ["a", "b", "empty"]


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("kind", ["hb donor", "aromatic ring"])
def test_directed_donors_and_unoriented_aromatic_axes_retain_distinct_meaning(
    skip, kind
):
    field = "directions" if kind == "hb donor" else "normals"
    first = inventory([[0, 0, 0]], [kind], **{field: [[1, 0, 0]]})
    second = inventory([[0, 0, 0]], [kind], **{field: [[-1, 0, 0]]})
    matching = get_aligned_feature_matches(
        first, second, direction_tolerance="0 degrees", skip_digestion=skip
    )
    result = get_consensus_sites(
        [first, second],
        [[[0, 0], [1, 0]]],
        ligand_ids=["a", "b"],
        direction_tolerance="0 degrees",
        skip_digestion=skip,
    )
    if kind == "hb donor":
        assert matching["matches"] == [] and result["sites"] == []
        assert result["rejected_groups"][0]["reasons"] == ["orientation_dispersion"]
    else:
        assert matching["matches"] == [[0, 0]] and len(result["sites"]) == 1
        site = result["sites"][0]
        np.testing.assert_array_equal(
            puw.get_value(site["normal"], to_unit="dimensionless"), [1, 0, 0]
        )
        assert site["orientation_reference"]["ligand_id"] == "a"


@pytest.mark.parametrize("skip", [False, True])
def test_completed_empty_aggregation_and_actual_reused_assignment_credit(skip):
    with ackredit.session("aligned-native-controls"), phmt.attribution():
        first = get_aligned_feature_matches(features(), features(), skip_digestion=skip)
        second = get_aligned_feature_matches(
            features(), features(), skip_digestion=skip
        )
        empty = get_aligned_feature_matches(
            features(), inventory([]), skip_digestion=skip
        )
        aggregated = get_consensus_sites(
            [features(), inventory([])],
            [],
            ligand_ids=["a", "empty"],
            skip_digestion=skip,
        )
    assert (
        aggregated["complete"]
        and aggregated["sites"] == aggregated["rejected_groups"] == []
    )
    assert aggregated["ligand_ids"] == ["a", "empty"] and aggregated["n_ligands"] == 2
    for result in (first, second):
        assert result["attribution"]["status"] == "captured"
        assert "10.1109/TAES.2016.140952" in json.dumps(result["attribution"])
    for result in (empty, aggregated):
        assert "10.1109/TAES.2016.140952" not in json.dumps(result["attribution"])
