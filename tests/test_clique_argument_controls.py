"""Public clique admission preserves maximality, finite limits and source custody."""

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
from pharmacophoremt.modeler import get_aligned_feature_cliques
from phmt_test_support.absence_inputs import inventory
from tests.test_aligned_cliques import exhaustive_cliques, keys
from tests.test_aligned_model_argument_controls import prepared

OWNER = importlib.import_module("pharmacophoremt.modeler.aligned_cliques")


def empty_sources():
    return [inventory([]), inventory([])]


def test_explicit_keyword_only_closed_definition_owned_export():
    assert phmt.modeler.get_aligned_feature_cliques is get_aligned_feature_cliques
    parameter = inspect.signature(get_aligned_feature_cliques).parameters[
        "skip_digestion"
    ]
    assert (
        parameter.kind is inspect.Parameter.KEYWORD_ONLY and parameter.default is False
    )
    plan = get_aligned_feature_cliques.digestion_plan
    assert plan.contract_owner == "definition"
    assert plan.contract_caller == OWNER.__name__ + ".get_aligned_feature_cliques"
    assert (
        describe_contract(plan.contracts.resolve(plan.contract_caller), plan.domains)[
            "admits"
        ]
        == "signature"
    )


@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_native_records(flag, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid control reached native records")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        get_aligned_feature_cliques(
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

    monkeypatch.setattr(_contracts, "_boolean", boolean)
    result = get_aligned_feature_cliques(
        empty_sources(), ligand_ids=["a", "b"], skip_digestion=flag
    )
    assert result["complete"] and result["groups"] == []
    assert len(seen) == (0 if flag is True else 1)
    if flag is not True:
        assert seen[0] is flag


@pytest.mark.parametrize("skip", [False, True])
def test_inventory_collection_remains_required(skip):
    with pytest.raises(TypeError):
        get_aligned_feature_cliques(ligand_ids=["a", "b"], skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_ligand_identities_remain_required(skip):
    with pytest.raises(TypeError):
        get_aligned_feature_cliques(empty_sources(), skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_unknown_keyword_stays_closed_before_records(skip, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Unknown keyword reached native records")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(TypeError):
        get_aligned_feature_cliques(
            empty_sources(), ligand_ids=["a", "b"], unknown=True, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("option", ["min_support", "max_graph_nodes", "max_cliques"])
@pytest.mark.parametrize("value", [0, -1, True, np.bool_(True), 1.5])
def test_native_integer_domains_precede_records_even_empty(
    skip, option, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid support or budget reached native records")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match=option):
        get_aligned_feature_cliques(
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
def test_native_physical_domains_precede_records_even_empty(
    skip, option, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid physical criterion reached native records")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match=option):
        get_aligned_feature_cliques(
            empty_sources(),
            ligand_ids=["a", "b"],
            skip_digestion=skip,
            **{option: value},
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("sources", [None, [], {}])
def test_invalid_inventory_collection_cannot_complete_empty(skip, sources):
    with pytest.raises(ArgumentError, match="feature_inventories"):
        get_aligned_feature_cliques(sources, ligand_ids=["a", "b"], skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("identities", [[], ["a", "a"], ["a", None], "ab"])
def test_invalid_identities_cannot_complete_empty(skip, identities):
    with pytest.raises(ArgumentError, match="ligand_ids"):
        get_aligned_feature_cliques(
            empty_sources(), ligand_ids=identities, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("identities,minimum", [(["a"], 1), (["a", "b"], 3)])
def test_count_and_attainable_support_precede_records(
    skip, identities, minimum, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid count/support reached records")

    monkeypatch.setattr(OWNER, "_records", forbidden)
    with pytest.raises(ArgumentError, match="ligand_ids/min_support"):
        get_aligned_feature_cliques(
            empty_sources(),
            ligand_ids=identities,
            min_support=minimum,
            skip_digestion=skip,
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("defect", ["donor", "center", "definition"])
def test_malformed_later_inventory_never_reaches_graph(skip, defect, monkeypatch):
    bad = inventory([[0, 0, 0]])
    if defect == "donor":
        bad["features"][0]["kind"] = "hb donor"
    elif defect == "center":
        bad["features"][0]["center"] = puw.quantity([np.nan, 0, 0], "nm")
    else:
        bad["definition"] = "unknown"

    def forbidden(*args, **kwargs):
        pytest.fail("Malformed later record reached graph")

    monkeypatch.setattr(OWNER.nx, "Graph", forbidden)
    with pytest.raises(ArgumentError):
        get_aligned_feature_cliques(
            [inventory([[0, 0, 0]]), bad],
            ligand_ids=["a", "b"],
            skip_digestion=skip,
        )


@pytest.mark.parametrize("skip", [False, True])
def test_graph_bound_refuses_before_construction_and_exact_bound_completes(
    skip, monkeypatch
):
    sources = [inventory([[0, 0, 0], [1, 0, 0]]) for _ in range(2)]
    result = get_aligned_feature_cliques(
        sources, ligand_ids=["a", "b"], max_graph_nodes=np.int64(4), skip_digestion=skip
    )
    assert result["complete"] and result["n_graph_nodes"] == 4

    def forbidden(*args, **kwargs):
        pytest.fail("Over-budget nodes reached graph construction")

    monkeypatch.setattr(OWNER.nx, "Graph", forbidden)
    with pytest.raises(CliqueLimitError) as caught:
        get_aligned_feature_cliques(
            sources, ligand_ids=["a", "b"], max_graph_nodes=3, skip_digestion=skip
        )
    assert caught.value.code == "PHMT-E107"
    expected = dict(
        stage="feature_graph", resource="nodes", observed=4, limit=3, complete=False
    )
    assert {key: caught.value.extra[key] for key in expected} == expected


@pytest.mark.parametrize("skip", [False, True])
def test_unsupported_maximal_cliques_count_toward_exact_output_bound(skip):
    sources = [inventory([[0, 0, 0], [1, 0, 0]]), inventory([[0, 0, 0], [2, 0, 0]])]
    result = get_aligned_feature_cliques(
        sources, ligand_ids=["z", "a"], max_cliques=np.int64(3), skip_digestion=skip
    )
    assert result["complete"] and result["n_maximal_cliques"] == 3
    assert result["groups"] == [[[1, 0], [0, 0]]]
    assert result["rejected_groups"] == [
        dict(members=[[1, 1]], reason="insufficient_ligand_support"),
        dict(members=[[0, 1]], reason="insufficient_ligand_support"),
    ]
    with pytest.raises(CliqueLimitError) as caught:
        get_aligned_feature_cliques(
            sources, ligand_ids=["z", "a"], max_cliques=2, skip_digestion=skip
        )
    assert caught.value.code == "PHMT-E107"
    expected = dict(
        stage="feature_cliques",
        resource="maximal cliques",
        observed=3,
        limit=2,
        complete=False,
    )
    assert {key: caught.value.extra[key] for key in expected} == expected


@pytest.mark.parametrize("skip", [False, True])
def test_original_mid_enumeration_failure_never_returns_partial_groups(
    skip, monkeypatch
):
    error = RuntimeError("original graph enumeration failure")

    def failing(graph):
        yield [(0, 0), (1, 0)]
        raise error

    monkeypatch.setattr(OWNER.nx, "find_cliques", failing)
    with pytest.raises(RuntimeError) as caught:
        get_aligned_feature_cliques(
            [inventory([[0, 0, 0]]) for _ in range(2)],
            ligand_ids=["a", "b"],
            skip_digestion=skip,
        )
    assert caught.value is error


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_all_maximal_sizes_and_inclusive_geometry_match_subset_oracle(
    skip, unit, monkeypatch
):
    sources = [
        inventory([[0, 0, 0], [1, 0, 0]]),
        inventory([[0.0625, 0, 0], [1.0625, 0, 0]]),
        inventory([[0.125, 0, 0]]),
        inventory([]),
    ]
    identities = ["z", "b", "a", "empty"]
    for source in sources:
        for record in source["features"]:
            record["center"] = puw.quantity(
                puw.get_value(record["center"], to_unit=unit), unit
            )
    before = deepcopy(detached(sources))
    expected = exhaustive_cliques(sources, identities, 0.125, 30)

    def forbidden(*args, **kwargs):
        pytest.fail("Inventory discovery must not read or align molecular systems")

    monkeypatch.setattr(msm, "get", forbidden)
    monkeypatch.setattr(msm.structure, "least_rmsd_fit", forbidden)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = deepcopy(puw.configure.get_standard_units())
        result = get_aligned_feature_cliques(
            sources,
            ligand_ids=identities,
            distance_tolerance=puw.quantity(0.125 if unit == "nm" else 125, unit),
            skip_digestion=skip,
        )
        assert puw.configure.get_standard_units() == policy
    assert keys(result["groups"], identities) == expected
    assert sorted(map(len, result["groups"])) == [2, 3]
    assert result["n_graph_nodes"] == 5 and result["n_graph_edges"] == 4
    assert result["n_ligands"] == 4 and result["complete"]
    assert result["ligand_ids"] == identities
    assert "skip_digestion" not in result["criteria"]
    assert detached(sources) == before
    identities[0] = "changed"
    assert result["ligand_ids"][0] == "z"


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "kind,field,vector,angle,connected",
    [
        ("hb donor", "directions", [-1, 0, 0], 0, False),
        ("hb donor", "directions", [-1, 0, 0], 180, True),
        ("hb donor", "directions", [0, 1, 0], 90, True),
        ("aromatic ring", "normals", [-1, 0, 0], 0, True),
    ],
)
def test_directed_donors_and_unoriented_axes_keep_inclusive_angles(
    skip, kind, field, vector, angle, connected
):
    sources = [
        inventory([[0, 0, 0]], [kind], **{field: [[1, 0, 0]]}),
        inventory([[0, 0, 0]], [kind], **{field: [vector]}),
    ]
    result = get_aligned_feature_cliques(
        sources,
        ligand_ids=["a", "b"],
        direction_tolerance=puw.quantity(angle, "degrees"),
        skip_digestion=skip,
    )
    assert bool(result["groups"]) is connected
    assert result["n_graph_edges"] == int(connected)
    assert keys(result["groups"], ["a", "b"]) == {
        group
        for group in exhaustive_cliques(sources, ["a", "b"], 0.15, angle)
        if len(group) >= 2
    }


@pytest.mark.parametrize("skip", [False, True])
def test_empty_negative_and_reused_credit_are_observed_by_application(skip):
    with ackredit.session("clique control"), phmt.attribution():
        with ackredit.capture("empty") as empty_capture:
            empty = get_aligned_feature_cliques(
                empty_sources(), ligand_ids=["a", "b"], skip_digestion=skip
            )
        assert empty["complete"] and empty["n_maximal_cliques"] == 0
        assert "10.1145/362342.362367" not in json.dumps(empty["attribution"])
        assert "10.1145/362342.362367" not in json.dumps(
            empty_capture.attribution.to_dict()
        )
        for label in ("new", "reused"):
            with ackredit.capture(label) as capture:
                negative = get_aligned_feature_cliques(
                    [inventory([[0, 0, 0]]), inventory([[1, 0, 0]])],
                    ligand_ids=["a", "b"],
                    skip_digestion=skip,
                )
            assert negative["complete"] and negative["groups"] == []
            assert negative["n_maximal_cliques"] == 2
            assert "10.1145/362342.362367" in json.dumps(negative["attribution"])
            assert "10.1145/362342.362367" in json.dumps(capture.attribution.to_dict())


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_real_prepared_frames_states_selection_and_consumers_keep_independent_admission(
    skip, unit, monkeypatch
):
    ligands = prepared()
    original_coordinates = [
        puw.get_value(
            msm.get(item["molecular_system"], coordinates=True), to_unit="nm"
        ).copy()
        for item in ligands
    ]
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
        result = get_aligned_feature_cliques(
            sources,
            ligand_ids=[item["ligand_id"] for item in ligands],
            distance_tolerance="0.15 nm",
            skip_digestion=skip,
        )
        mapped_groups = {
            frozenset(
                (i, tuple(sources[i]["features"][j]["atom_indices"])) for i, j in group
            )
            for group in result["groups"]
        }
        assert mapped_groups == {
            frozenset(((0, (atom,)), (1, (atom,)))) for atom in range(3)
        }
        assert result["n_ligands"] == 3 and result["n_graph_edges"] == 3
        assert sources[0]["selected_atom_indices"] == [2, 0, 1]
        assert sources[0]["structure_index"] == 1 and sources[1]["structure_index"] == 0
        assert sources[0]["chemical_state"] == sources[1]["chemical_state"] == 1
        assert sources[2]["features"] == []
        assert detached(sources) == before
        calls = []
        original = get_aligned_feature_cliques

        @wraps(original)
        def observed(*args, **kwargs):
            assert "skip_digestion" not in kwargs
            calls.append(kwargs.copy())
            return original(*args, **kwargs)

        monkeypatch.setattr(OWNER, "get_aligned_feature_cliques", observed)
        consumer = phmt.modeler.get_aligned_consensus_hypotheses(
            sources, ligand_ids=[item["ligand_id"] for item in ligands]
        )
        assert len(calls) == 1
        assert consumer["complete"] and len(consumer["hypotheses"]) == 1
        assert consumer["hypotheses"][0]["joint_support_fraction"] == pytest.approx(
            2 / 3
        )
        centers = sorted(
            tuple(puw.get_value(site["center"], to_unit="nm"))
            for site in consumer["candidate_sites"]
        )
        np.testing.assert_allclose(
            centers, [[0.0625, 0, 0], [0.0625, 1, 0], [1.0625, 0, 0]]
        )
        assert puw.configure.get_standard_units() == policy
        assert detached(sources) == before
    for ligand, coordinates in zip(ligands, original_coordinates):
        np.testing.assert_array_equal(
            puw.get_value(
                msm.get(ligand["molecular_system"], coordinates=True), to_unit="nm"
            ),
            coordinates,
        )
