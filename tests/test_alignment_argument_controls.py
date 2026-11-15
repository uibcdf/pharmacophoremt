"""Independent alignment admission retains native geometry and molecular custody."""

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
from pharmacophoremt.modeler import from_feature_inventory, from_ligand, get_features
from pharmacophoremt.screening import PoseEvaluator, align_to_pharmacophore
from phmt_test_support.absence_inputs import inventory, system
from tests.test_conformer_screening import add_declared_state
from tests.test_seeded_scoring import ionic_case

ALIGNMENT = importlib.import_module("pharmacophoremt.screening.alignment")
PAIRS = [[0, 0], [1, 1], [2, 2]]
CENTERS = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=float)


def query():
    return from_feature_inventory(
        inventory(CENTERS, ["positive charge"] * 3), radius=".02 nm"
    )


def test_explicit_keyword_only_control_and_closed_definition_owned_export():
    assert phmt.screening.align_to_pharmacophore is ALIGNMENT.align_to_pharmacophore
    control = inspect.signature(align_to_pharmacophore).parameters["skip_digestion"]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY and control.default is False
    plan = align_to_pharmacophore.digestion_plan
    assert plan.contract_owner == "definition"
    assert plan.contract_caller == ALIGNMENT.__name__ + ".align_to_pharmacophore"
    contract = describe_contract(
        plan.contracts.resolve(plan.contract_caller), plan.domains
    )
    assert contract["admits"] == "signature"


@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_query_or_molecular_work(flag, monkeypatch):
    q = query()

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid controls must refuse before query/provider work")

    for name in ("PoseEvaluator", "source_frame", "get_features", "capability"):
        monkeypatch.setattr(ALIGNMENT, name, forbidden)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        align_to_pharmacophore(object(), q, PAIRS, skip_digestion=flag)


@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
def test_literal_bypass_is_local_and_query_child_keeps_default(flag, monkeypatch):
    q = query()
    seen, children = [], []
    original = _contracts._boolean
    original_child = ALIGNMENT.PoseEvaluator

    def boolean(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    def child(*args, **kwargs):
        assert "skip_digestion" not in kwargs
        children.append("default")
        return original_child(*args, **kwargs)

    class ReachedFrame(Exception):
        pass

    def frame(*args, **kwargs):
        raise ReachedFrame

    monkeypatch.setattr(_contracts, "_boolean", boolean)
    monkeypatch.setattr(ALIGNMENT, "PoseEvaluator", child)
    monkeypatch.setattr(ALIGNMENT, "source_frame", frame)
    with pytest.raises(ReachedFrame):
        align_to_pharmacophore(object(), q, PAIRS, skip_digestion=flag)
    assert children == ["default"]
    assert len(seen) == (0 if flag is True else 1) + 1
    if flag is not True:
        assert seen[0] is flag
    assert seen[-1] is False


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "pairs",
    [
        [],
        [[0, 0], [1, 1]],
        [0, 1, 2],
        [[0], [1], [2]],
        [[0, 0, 0]] * 3,
        [[0, 0], [1, 1], [-1, 2]],
        [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]],
        [[False, False]] * 3,
    ],
)
def test_mandatory_mapping_shape_and_index_guard_precedes_query_and_frame(
    skip, pairs, monkeypatch
):
    q = query()

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid mappings cannot reach a query or molecular frame")

    monkeypatch.setattr(ALIGNMENT, "PoseEvaluator", forbidden)
    monkeypatch.setattr(ALIGNMENT, "source_frame", forbidden)
    with pytest.raises(ArgumentError, match="correspondence"):
        align_to_pharmacophore(object(), q, pairs, skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "kind", ["duplicate", "range", "chemistry", "frame", "selection", "state"]
)
def test_native_mapping_and_cached_axis_guards_precede_fit_copy_set(
    skip, kind, monkeypatch
):
    source, q = ionic_case()
    features = get_features(source, features=["positive charge"])
    pairs = deepcopy(PAIRS)
    if kind == "duplicate":
        pairs[-1] = [1, 2]
    elif kind == "range":
        pairs[-1] = [2, 99]
    elif kind == "chemistry":
        features["features"][0]["kind"] = "negative charge"
    elif kind == "frame":
        features["structure_index"] = 1
    elif kind == "selection":
        features["selected_atom_indices"] = [2, 1, 0]
    else:
        features["chemical_state"] = 1

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid cached axes or mappings cannot enter fit/copy/set")

    monkeypatch.setattr(ALIGNMENT, "capability", forbidden)
    with pytest.raises(ArgumentError):
        align_to_pharmacophore(
            source, q, pairs, feature_inventory=features, skip_digestion=skip
        )


@pytest.mark.parametrize("options", [{}, {"skip_digestion": True}])
@pytest.mark.parametrize("axis", ["source", "target"])
@pytest.mark.parametrize("origin", [[0, 0, 0], [10.961, 1.2027, 2.2746]])
@pytest.mark.parametrize("geometry", ["line", "two_centers"])
def test_collinear_anchor_centers_refuse_before_molecular_fit(
    axis, origin, options, geometry, monkeypatch
):
    origin = np.array(origin)
    line = origin + [[0, 0, 0], [1, 0, 0], [2, 0, 0]]
    if geometry == "two_centers":
        line[1] = line[0]
    target = line if axis == "target" else origin + CENTERS
    candidate = line if axis == "source" else origin + CENTERS
    q = from_feature_inventory(
        inventory(target, ["positive charge"] * 3), radius=".02 nm"
    )
    source = system("[Na+].[K+].[Li+]", candidate)
    features = inventory(candidate, ["positive charge"] * 3)

    def forbidden(*args, **kwargs):
        pytest.fail("Documented non-collinear anchors must be checked before fit")

    monkeypatch.setattr(ALIGNMENT, "capability", forbidden)
    with pytest.raises(ArgumentError, match="non-collinear"):
        align_to_pharmacophore(source, q, PAIRS, feature_inventory=features, **options)


@pytest.mark.parametrize("skip", [False, True])
def test_nonfinite_cached_anchor_refuses_before_molecular_fit(skip, monkeypatch):
    source, q = ionic_case()
    features = get_features(source, features=["positive charge"])
    features["features"][0]["center"] = puw.quantity([float("nan"), 0, 0], "nm")

    def forbidden(*args, **kwargs):
        pytest.fail("Nonfinite centers cannot enter molecular fitting")

    monkeypatch.setattr(ALIGNMENT, "capability", forbidden)
    with pytest.raises(ArgumentError):
        align_to_pharmacophore(
            source, q, PAIRS, feature_inventory=features, skip_digestion=skip
        )


@pytest.mark.parametrize("axis", [0, 1])
@pytest.mark.parametrize("large", [2**63, 2**64 - 1])
def test_unsigned_overflow_is_refused_during_literal_bypass(axis, large, monkeypatch):
    q = query()
    pairs = np.array(PAIRS, dtype=np.uint64)
    pairs[2, axis] = large

    def forbidden(*args, **kwargs):
        pytest.fail(
            "Unsigned overflow must refuse before query/source work even during bypass"
        )

    monkeypatch.setattr(ALIGNMENT, "PoseEvaluator", forbidden)
    monkeypatch.setattr(ALIGNMENT, "source_frame", forbidden)
    with pytest.raises(ArgumentError, match="correspondence"):
        align_to_pharmacophore(object(), q, pairs, skip_digestion=True)


@pytest.mark.parametrize("skip", [False, True])
def test_unknown_keyword_refuses_before_molecular_access(skip, monkeypatch):
    q = query()

    def forbidden(*args, **kwargs):
        pytest.fail("Unknown keywords cannot reach molecular work")

    monkeypatch.setattr(ALIGNMENT, "source_frame", forbidden)
    with pytest.raises(TypeError):
        align_to_pharmacophore(object(), q, PAIRS, skip_digestion=skip, frames=[0])


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("cached", [False, True])
def test_real_proper_fit_preserves_subset_frame_state_units_and_attribution(
    unit, cached, monkeypatch
):
    with puw.context(standard_units=[unit, "ps", "radians"]):
        source, q = ionic_case()
        source = system("[Na+].[K+].[Li+].[Cl-]", [*CENTERS, [4, 5, 6]])
        add_declared_state(source, [1, 1, 1, -1])
        source.structures.append(coordinates=msm.get(source, coordinates=True))
        indices = [2, 0, 1]
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
            translation=puw.quantity([[[2, 1, 3]]], "nm"),
            in_place=False,
        )
        before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
        features = get_features(
            source,
            selection=indices,
            structure_index=1,
            chemical_state=1,
            features=["positive charge"],
        )
        pairs = [
            [
                i,
                next(
                    j
                    for j, r in enumerate(features["features"])
                    if r["atom_indices"] == [i]
                ),
            ]
            for i in range(3)
        ]
        original_fit = msm.structure.least_rmsd_fit
        fit_calls, extractions = [], []
        original_features = ALIGNMENT.get_features

        def fit(*args, **kwargs):
            assert "skip_digestion" not in kwargs
            fit_calls.append(
                (kwargs["use_gpu"], kwargs["precision"], kwargs["in_place"])
            )
            return original_fit(*args, **kwargs)

        def extract(*args, **kwargs):
            assert "skip_digestion" not in kwargs
            extractions.append(kwargs["chemical_state"])
            return original_features(*args, **kwargs)

        monkeypatch.setattr(msm.structure, "least_rmsd_fit", fit)
        monkeypatch.setattr(ALIGNMENT, "get_features", extract)
        for options in ({}, {"skip_digestion": False}, {"skip_digestion": True}):
            with phmt.attribution():
                result = align_to_pharmacophore(
                    source,
                    q,
                    pairs,
                    selection=indices,
                    structure_index=1,
                    chemical_state=1,
                    feature_inventory=features if cached else None,
                    **options,
                )
            assert result["molecular_system"] is not source
            assert result["attribution"]["status"] == "captured"
            evidence = result["alignment"]
            assert (
                evidence["selected_atom_indices"] == indices
                and evidence["structure_index"] == 1
            )
            assert evidence["provider_options"] == {
                "use_gpu": False,
                "precision": "double",
                "engine": "MolSysMT",
            }
            rmsd = puw.QuantityRecord.from_dict(evidence["rmsd"]).to_quantity(
                unit="nm", dimensionality={"[L]": 1}
            )
            assert np.max(puw.get_value(rmsd, to_unit="nm")) < 1e-12
            after = puw.get_value(
                msm.get(result["molecular_system"], coordinates=True), to_unit="nm"
            )
            np.testing.assert_allclose(after[1, :3], CENTERS, atol=1e-12)
            np.testing.assert_array_equal(after[0], before[0])
            np.testing.assert_array_equal(after[:, 3], before[:, 3])
            assert (
                PoseEvaluator(q).evaluate(
                    result["molecular_system"],
                    selection=indices,
                    structure_index=1,
                    chemical_state=1,
                )["status"]
                == "matched"
            )
        assert fit_calls == [(False, "double", False)] * 3
        assert extractions == ([] if cached else [1, 1, 1])
        np.testing.assert_array_equal(
            puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
        )


@pytest.mark.parametrize("skip", [False, True])
def test_nonplanar_reflection_keeps_handedness_and_nonzero_residual(skip):
    centers = np.vstack((CENTERS, [[0, 0, 1]]))
    reference = system("[Na+].[K+].[Li+].[Rb+]", centers)
    source = system("[Na+].[K+].[Li+].[Rb+]", centers * [1, 1, -1])
    q = from_ligand(reference, features=["positive charge"], radius=".02 nm")
    features = get_features(source, features=["positive charge"])
    result = align_to_pharmacophore(
        source,
        q,
        [[i, i] for i in range(4)],
        feature_inventory=features,
        skip_digestion=skip,
    )
    after = puw.get_value(
        msm.get(result["molecular_system"], coordinates=True), to_unit="nm"
    )[0]
    assert np.linalg.det(after[1:] - after[0]) < 0
    assert not np.allclose(after, centers, atol=0.02)
    for i in range(4):
        for j in range(i):
            assert np.linalg.norm(after[i] - after[j]) == pytest.approx(
                np.linalg.norm(centers[i] - centers[j])
            )


@pytest.mark.parametrize("skip", [False, True])
def test_provider_failure_propagates_original_exception_before_copy(skip, monkeypatch):
    source, q = ionic_case()
    failure = RuntimeError("actual provider fit failure")

    def broken(*args, **kwargs):
        raise failure

    def forbidden(*args, **kwargs):
        pytest.fail("A failed fit must not copy or change the molecular source")

    monkeypatch.setattr(msm.structure, "least_rmsd_fit", broken)
    monkeypatch.setattr(msm, "copy", forbidden)
    with pytest.raises(RuntimeError) as caught:
        align_to_pharmacophore(source, q, PAIRS, skip_digestion=skip)
    assert caught.value is failure
