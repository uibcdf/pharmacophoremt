"""Aligned-ligand model admission preserves reference scope and native children."""

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
    ConsensusLimitError,
)
from pharmacophoremt.modeler import from_aligned_ligands
from phmt_test_support.absence_inputs import system
from tests.test_conformer_screening import add_declared_state

OWNER = importlib.import_module("pharmacophoremt.modeler.aligned_consensus")
COORDINATES = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [9, 8, 7]], dtype=float)


def placeholders():
    return [
        dict(ligand_id="a", molecular_system=object()),
        dict(ligand_id="b", molecular_system=object()),
    ]


def prepared():
    shifted = system("[Na+].[K+].[Li+].[Cl-]", COORDINATES + [10, 0, 0])
    shifted.structures.append(
        coordinates=puw.quantity([COORDINATES + [0.125, 0, 0]], "nm")
    )
    reference = system("[Na+].[K+].[Li+].[Cl-]", COORDINATES)
    for source in (shifted, reference):
        add_declared_state(source, [1, 1, 1, -1])
    empty = system("[He]", [[3, 4, 5]])
    return [
        dict(
            ligand_id="shifted",
            molecular_system=shifted,
            selection=[2, 0, 1],
            structure_index=1,
            chemical_state=1,
        ),
        dict(
            ligand_id="reference",
            molecular_system=reference,
            selection=[1, 2, 0],
            structure_index=0,
            chemical_state=1,
        ),
        dict(ligand_id="empty", molecular_system=empty),
    ]


def test_explicit_keyword_only_closed_definition_owned_export():
    assert phmt.modeler.from_aligned_ligands is from_aligned_ligands
    control = inspect.signature(from_aligned_ligands).parameters["skip_digestion"]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY and control.default is False
    plan = from_aligned_ligands.digestion_plan
    assert plan.contract_owner == "definition"
    assert plan.contract_caller == OWNER.__name__ + ".from_aligned_ligands"
    assert (
        describe_contract(plan.contracts.resolve(plan.contract_caller), plan.domains)[
            "admits"
        ]
        == "signature"
    )


@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_extraction(flag, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid control reached extraction")

    monkeypatch.setattr(OWNER, "get_features", forbidden)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        from_aligned_ligands(placeholders(), skip_digestion=flag)


@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
def test_only_literal_true_bypasses_ordinary_control_digestion(flag, monkeypatch):
    seen = []
    original = _contracts._boolean

    def boolean(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    class ReachedExtraction(Exception):
        pass

    def reached(*args, **kwargs):
        raise ReachedExtraction

    monkeypatch.setattr(_contracts, "_boolean", boolean)
    monkeypatch.setattr(OWNER, "get_features", reached)
    with pytest.raises(ReachedExtraction):
        from_aligned_ligands(placeholders(), skip_digestion=flag)
    assert len(seen) == (0 if flag is True else 1)
    if flag is not True:
        assert seen[0] is flag


@pytest.mark.parametrize("skip", [False, True])
def test_ligand_collection_remains_required(skip):
    with pytest.raises(TypeError):
        from_aligned_ligands(skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
def test_unknown_keyword_stays_closed_before_extraction(skip, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Unknown keyword reached extraction")

    monkeypatch.setattr(OWNER, "get_features", forbidden)
    with pytest.raises(TypeError):
        from_aligned_ligands(placeholders(), unexpected=True, skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "option,value",
    [
        ("reference_index", -1),
        ("reference_index", True),
        ("reference_index", 0.5),
        ("min_support", 0),
        ("min_support", -1),
        ("min_support", True),
        ("min_support", 1.5),
        ("max_matrix_entries", 0),
        ("max_matrix_entries", -1),
        ("max_matrix_entries", True),
        ("max_matrix_entries", 1.5),
        ("features", []),
        ("features", None),
        ("features", ["unknown"]),
        ("features", ["included volume"]),
        ("distance_tolerance", "0 nm"),
        ("distance_tolerance", "-1 nm"),
        ("distance_tolerance", "nan nm"),
        ("distance_tolerance", "1 ps"),
        ("direction_tolerance", "-1 degrees"),
        ("direction_tolerance", "181 degrees"),
        ("direction_tolerance", "nan degrees"),
        ("direction_tolerance", "1 nm"),
        ("radius", "0 nm"),
        ("radius", "-1 nm"),
        ("radius", "inf nm"),
        ("radius", "1 ps"),
    ],
)
def test_native_domains_and_classical_family_restriction_precede_extraction(
    skip, option, value, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid scientific input reached extraction")

    monkeypatch.setattr(OWNER, "get_features", forbidden)
    with pytest.raises(ArgumentError, match=option):
        from_aligned_ligands(placeholders(), skip_digestion=skip, **{option: value})


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "change",
    ["empty", "single", "duplicate", "missing_source", "unknown_field", "bad_identity"],
)
def test_all_ligand_records_are_checked_before_first_extraction(
    skip, change, monkeypatch
):
    ligands = placeholders()
    if change == "empty":
        ligands = []
    elif change == "single":
        ligands = ligands[:1]
    elif change == "duplicate":
        ligands[1]["ligand_id"] = "a"
    elif change == "missing_source":
        ligands[1].pop("molecular_system")
    elif change == "unknown_field":
        ligands[1]["undeclared"] = True
    else:
        ligands[1]["ligand_id"] = None

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid ligand records reached molecular work")

    monkeypatch.setattr(OWNER, "get_features", forbidden)
    with pytest.raises(ArgumentError):
        from_aligned_ligands(ligands, skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("options", [{"reference_index": 2}, {"min_support": 3}])
def test_reference_and_support_upper_bounds_stay_before_extraction(
    skip, options, monkeypatch
):
    def forbidden(*args, **kwargs):
        pytest.fail("Out-of-range reference/support reached extraction")

    monkeypatch.setattr(OWNER, "get_features", forbidden)
    with pytest.raises(ArgumentError, match="reference_index/min_support"):
        from_aligned_ligands(placeholders(), skip_digestion=skip, **options)


@pytest.mark.parametrize("skip", [False, True])
def test_source_frame_remains_owned_by_validating_extraction_child(skip, monkeypatch):
    ligands = prepared()
    ligands[0]["structure_index"] = -1
    original = OWNER.get_features
    calls = []

    def child(*args, **kwargs):
        calls.append(kwargs)
        assert "skip_digestion" not in kwargs
        return original(*args, **kwargs)

    monkeypatch.setattr(OWNER, "get_features", child)
    with pytest.raises(ArgumentError, match="structure_index"):
        from_aligned_ligands(ligands, features=["positive charge"], skip_digestion=skip)
    assert len(calls) == 1


@pytest.mark.parametrize("skip", [False, True])
def test_later_extraction_failure_preserves_exception_without_partial_model(
    skip, monkeypatch
):
    ligands = prepared()
    error = RuntimeError("Original second extraction failure")
    original = OWNER.get_features
    calls = []

    def child(*args, **kwargs):
        calls.append(kwargs)
        assert "skip_digestion" not in kwargs
        if len(calls) == 2:
            raise error
        return original(*args, **kwargs)

    def forbidden(*args, **kwargs):
        pytest.fail("Failed extraction reached matching")

    monkeypatch.setattr(OWNER, "get_features", child)
    monkeypatch.setattr(OWNER, "get_aligned_feature_matches", forbidden)
    with pytest.raises(RuntimeError) as caught:
        from_aligned_ligands(ligands, features=["positive charge"], skip_digestion=skip)
    assert caught.value is error and len(calls) == 2


@pytest.mark.parametrize("skip", [False, True])
def test_assignment_exhaustion_keeps_original_failure_and_no_aggregation(
    skip, monkeypatch
):
    ligands = prepared()

    def forbidden(*args, **kwargs):
        pytest.fail("Failed assignment reached aggregation")

    monkeypatch.setattr(OWNER, "get_consensus_sites", forbidden)
    with pytest.raises(ConsensusLimitError) as caught:
        from_aligned_ligands(
            ligands,
            reference_index=1,
            features=["positive charge"],
            max_matrix_entries=1,
            skip_digestion=skip,
        )
    assert (
        caught.value.code == "PHMT-E106" and caught.value.extra["matrix_entries"] == 18
    )


@pytest.mark.parametrize("skip", [False, True])
def test_empty_reference_does_not_discover_patterns_supported_only_elsewhere(skip):
    ligands = prepared()
    empty_anchor = [ligands[0], ligands[2], ligands[1]]
    with pytest.raises(ArgumentError, match="no supported geometrically consistent"):
        from_aligned_ligands(
            empty_anchor,
            reference_index=1,
            features=["positive charge"],
            skip_digestion=skip,
        )
    model = from_aligned_ligands(
        empty_anchor,
        reference_index=0,
        features=["positive charge"],
        skip_digestion=skip,
    )
    assert model.n_interaction_sites == 3
    assert all(
        site.metadata["support_fraction"] == pytest.approx(2 / 3)
        for site in model.interaction_sites
    )


@pytest.mark.parametrize("skip", [False, True])
def test_completed_extraction_without_supported_sites_never_returns_an_empty_query(
    skip,
):
    source = system("[He]", [[0, 0, 0]])
    ligands = [dict(ligand_id=label, molecular_system=source) for label in ("a", "b")]
    with pytest.raises(ArgumentError, match="no supported geometrically consistent"):
        from_aligned_ligands(ligands, features=["positive charge"], skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_real_reference_centroids_keep_children_frame_state_units_custody_and_persistence(
    skip, unit, monkeypatch, tmp_path
):
    ligands = prepared()
    originals = [
        puw.get_value(
            msm.get(ligand["molecular_system"], coordinates=True), to_unit="nm"
        ).copy()
        for ligand in ligands
    ]
    calls = {
        name: []
        for name in (
            "get_features",
            "get_aligned_feature_matches",
            "get_consensus_sites",
        )
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
        radius = puw.quantity(0.01 if unit == "nm" else 10, unit)
        with ackredit.session("aligned-model-control"), phmt.attribution():
            model = from_aligned_ligands(
                ligands,
                reference_index=np.int64(1),
                features=["positive charge"],
                radius=radius,
                name="aligned model",
                skip_digestion=skip,
            )
        assert puw.configure.get_standard_units() == policy
    assert (
        model.name == "aligned model" and model.ref_mol == 1 and model.ref_struct == 0
    )
    assert model.n_interaction_sites == 3
    actual = np.array(
        [puw.get_value(site.center, to_unit="nm") for site in model.interaction_sites]
    )
    expected = COORDINATES[:3] + [0.0625, 0, 0]
    np.testing.assert_allclose(
        sorted(actual.tolist()), sorted(expected.tolist()), rtol=0, atol=1e-14
    )
    assert {name: len(observed) for name, observed in calls.items()} == {
        "get_features": 3,
        "get_aligned_feature_matches": 2,
        "get_consensus_sites": 1,
    }
    assert calls["get_features"][0]["selection"] == [2, 0, 1]
    assert (
        calls["get_features"][0]["structure_index"]
        == calls["get_features"][0]["chemical_state"]
        == 1
    )
    assert calls["get_features"][1]["selection"] == [1, 2, 0]
    assert (
        calls["get_features"][1]["structure_index"] == 0
        and calls["get_features"][1]["chemical_state"] == 1
    )
    for site in model.interaction_sites:
        assert (
            site.feature_name == "positive charge"
            and site.essential
            and site.weight == 1
        )
        assert site.metadata["support_count"] == 2 and site.metadata[
            "support_fraction"
        ] == pytest.approx(2 / 3)
        assert site.metadata["members"][0]["ligand_id"] == "reference"
        assert float(puw.get_value(site.radius, to_unit="nm")) == pytest.approx(0.01)
        rmsd = puw.QuantityRecord.from_dict(site.metadata["position_rmsd"]).to_quantity(
            unit="nm", dimensionality={"[L]": 1}
        )
        assert float(puw.get_value(rmsd, to_unit="nm")) == pytest.approx(0.0625)
    assert model.metadata["sources"][0]["selected_atom_indices"] == [2, 0, 1]
    assert model.metadata["sources"][0]["structure_index"] == 1
    assert (
        model.metadata["sources"][1]["chemical_state"] == 1
        and model.metadata["sources"][2]["features"] == []
    )
    assert [
        comparison["inventory_index"] for comparison in model.metadata["comparisons"]
    ] == [0, 2]
    payload = model.metadata["attribution"]
    assert payload["status"] == "captured" and "10.1109/TAES.2016.140952" in json.dumps(
        payload
    )
    filename = tmp_path / "aligned-model.json"
    phmt.io.to_json(model, filename)
    restored = phmt.io.load_json(filename)
    assert restored.metadata == model.metadata
    for original_site, recovered in zip(
        model.interaction_sites, restored.interaction_sites
    ):
        assert (
            recovered.metadata == original_site.metadata
            and recovered.essential
            and recovered.weight == 1
        )
    for source, expected_coordinates in zip(ligands, originals):
        np.testing.assert_array_equal(
            puw.get_value(
                msm.get(source["molecular_system"], coordinates=True), to_unit="nm"
            ),
            expected_coordinates,
        )
    before = deepcopy(model.metadata)
    ligands[0]["selection"].clear()
    assert model.metadata == before
    # Consensus is within 0.15 nm; the narrow emitted radius is independent.
    assert (
        phmt.screening.PoseEvaluator(model).evaluate(
            ligands[1]["molecular_system"], selection=[1, 2, 0], chemical_state=1
        )["status"]
        == "not_matched"
    )
