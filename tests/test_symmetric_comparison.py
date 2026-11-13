"""Independent finite matching oracles for positive native center comparison."""

import itertools
import json
import math
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    ComparisonLimitError,
)
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import (
    Cylinder,
    Disk,
    GaussianKernel,
    Point,
    Sphere,
    SphereAndVector,
)
from pharmacophoremt.io.phmt import _to_dict


def query(rows, *, sphere=False):
    result = phmt.Pharmacophore(name="literal 2 m", ref_struct=0)
    for x, names in rows:
        center = puw.quantity([x, 0, 0], "nm")
        shape = Sphere(center, ".1 nm") if sphere else Point(center)
        result.add_interaction_site(InteractionSite(shape, names))
    return result


def oracle(left, right, tolerance):
    """Enumerate partial injective maps independently, without NumPy/SciPy."""

    def visit(row, used):
        if row == len(left):
            return 0
        best = visit(row + 1, used)
        x, names = left[row]
        for col, (y, others) in enumerate(right):
            if (
                col not in used
                and set(names) & set(others)
                and math.dist([x, 0, 0], [y, 0, 0]) <= tolerance
            ):
                best = max(best, 1 + visit(row + 1, used | {col}))
        return best

    return visit(0, set())


def check_report(result, left, right, tolerance):
    expected = oracle(left, right, tolerance)
    assert result["complete"] is True
    assert result["n_matches"] == expected
    assert result["similarity"] == (
        2 * expected / (len(left) + len(right)) if left or right else 0
    )
    pairs = result["matches"]
    assert len({p["site_index"] for p in pairs}) == len(pairs)
    assert len({p["other_site_index"] for p in pairs}) == len(pairs)
    for pair in pairs:
        i, j = pair["site_index"], pair["other_site_index"]
        assert set(left[i][1]) & set(right[j][1])
        observed = puw.QuantityRecord.from_dict(pair["distance"]).to_quantity()
        assert float(puw.get_value(observed, to_unit="nm")) == pytest.approx(
            abs(left[i][0] - right[j][0])
        )
    assert sorted(
        result["unmatched_site_indices"] + [p["site_index"] for p in pairs]
    ) == list(range(len(left)))
    assert sorted(
        result["unmatched_other_site_indices"] + [p["other_site_index"] for p in pairs]
    ) == list(range(len(right)))


def test_public_defining_contract_and_default_legacy_route():
    import inspect

    operation = phmt.compare_pharmacophores
    assert phmt.ComparisonLimitError is ComparisonLimitError
    parameter = inspect.signature(operation).parameters["skip_digestion"]
    assert (
        parameter.kind is inspect.Parameter.KEYWORD_ONLY and parameter.default is False
    )
    owner = operation.__module__ + "." + operation.__name__
    plan = operation.digestion_plan
    assert plan.contract_caller == owner
    assert (
        describe_contract(plan.contracts.resolve(owner), plan.domains)["admits"]
        == "signature"
    )
    left = query([(0.1, ["hydrophobicity"]), (0, ["hydrophobicity"])])
    right = query([(0, ["hydrophobicity"]), (0.3, ["hydrophobicity"])])
    assert left.similarity(right, 0.21) == 0.5
    assert left.similarity(right, 0.21, method="ordered_greedy") == 0.5
    assert right.similarity(left, 0.21) == 1
    assert left.similarity(right, 0.21, method="maximum_cardinality") == 1


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("skip", [False, True])
def test_counterexample_and_independent_output_under_units_controls_and_native_readback(
    unit, skip, monkeypatch, tmp_path
):
    def forbidden(*args, **kwargs):
        pytest.fail("Cached comparison must not access molecules")

    for name in ["get", "copy", "convert", "select", "merge", "set"]:
        monkeypatch.setattr(msm, name, forbidden)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        left_rows = [(0.1, ["hydrophobicity"]), (0, ["hydrophobicity"])]
        right_rows = [(0, ["hydrophobicity"]), (0.3, ["hydrophobicity"])]
        left, right = query(left_rows), query(right_rows, sphere=True)
        right.ref_struct = (
            7  # Indices are declarations, not coordinate-basis identities.
        )
        before = deepcopy([_to_dict(left), _to_dict(right)])
        policy = puw.configure.report()
        result = phmt.compare_pharmacophores(
            left, right, distance_tolerance="210 pm", skip_digestion=skip
        )
        check_report(result, left_rows, right_rows, 0.21)
        assert result["n_matches"] == 2 and result["inputs"]["other"]["ref_struct"] == 7
        assert puw.configure.report() == policy
        assert [_to_dict(left), _to_dict(right)] == before
        saved = json.loads(json.dumps(result))
        result["inputs"]["pharmacophore"]["sites"][0]["features"].clear()
        assert [_to_dict(left), _to_dict(right)] == before
        assert saved["inputs"]["pharmacophore"]["sites"][0]["features"] == [
            "hydrophobicity"
        ]
        path = tmp_path / "query.json"
        phmt.io.to_json(left, path)
        restored = phmt.io.load_json(path)
        assert restored.metadata == left.metadata
        assert (
            phmt.compare_pharmacophores(restored, right, distance_tolerance=".21 nm")[
                "similarity"
            ]
            == 1
        )


def test_all_two_site_geometry_feature_combinations_against_exhaustive_oracle():
    atoms = list(itertools.product([0, 0.2, 0.4], [("hydrophobicity",), ("hb donor",)]))
    cases = list(itertools.product(atoms, repeat=2))
    models = [query(rows) for rows in cases]
    measured = []
    for i, left in enumerate(cases):
        for j, right in enumerate(cases):
            result = phmt.compare_pharmacophores(
                models[i], models[j], distance_tolerance=".25 nm"
            )
            check_report(result, left, right, 0.25)
            measured.append(
                [
                    i,
                    j,
                    oracle(left, right, 0.25),
                    result["n_matches"],
                    result["similarity"],
                ]
            )
    assert len(cases) ** 2 == 1296
    print(
        json.dumps(
            dict(
                experiment="two_site_positive_center_family@1",
                models=cases,
                tolerance_nm=0.25,
                columns=[
                    "first",
                    "second",
                    "expected_matches",
                    "observed_matches",
                    "similarity",
                ],
                measured=measured,
            ),
            sort_keys=True,
        )
    )


def test_rectangular_alternative_tied_permutations_and_swaps_have_invariant_count():
    left = [
        (0, ["hb donor", "hb acceptor"]),
        (0.2, ["hb donor"]),
        (0.4, ["hydrophobicity"]),
    ]
    right = [(0.1, ["hb donor"]), (0.4, ["hydrophobicity"])]
    expected = oracle(left, right, 0.15)
    for a in itertools.permutations(left):
        for b in itertools.permutations(right):
            for first, second in [(a, b), (b, a)]:
                result = phmt.compare_pharmacophores(query(first), query(second))
                check_report(result, first, second, 0.15)
                assert result["n_matches"] == expected == 2


@pytest.mark.parametrize(
    "left,right",
    [
        ([], []),
        ([], [(0, ["hb donor"])]),
        ([(0, ["hb donor"])], []),
        ([(0, ["hb donor"])], [(0, ["hydrophobicity"])]),
    ],
)
def test_empty_and_no_edges_complete_without_reaching_assignment(
    left, right, monkeypatch
):
    import scipy.optimize

    def forbidden(*args, **kwargs):
        pytest.fail("No edges must not execute assignment")

    monkeypatch.setattr(scipy.optimize, "linear_sum_assignment", forbidden)
    result = phmt.compare_pharmacophores(query(left), query(right))
    check_report(result, left, right, 0.15)
    assert result["work"]["assignment_calls"] == 0


def test_occurrences_count_independently_and_weights_do_not_change_overlap():
    left = query([(0, ["hydrophobicity"])], sphere=True)
    left.interaction_sites[0].weight = 0
    left.interaction_sites[0].essential = False
    left.add_interaction_site(left.interaction_sites[0])
    result = phmt.compare_pharmacophores(left, query([(0, ["hydrophobicity"])]))
    assert result["n_matches"] == 1 and result["similarity"] == pytest.approx(2 / 3)
    assert result["inputs"]["pharmacophore"]["sites"][0]["weight"] == 0
    assert result["inputs"]["pharmacophore"]["sites"][0]["essential"] is False


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_inclusive_boundary_zero_and_finite_extremes(unit):
    with puw.context(standard_units=[unit, "ps", "radians"]):
        first = query([(0, ["hydrophobicity"])])
        for separation, expected in [
            (1, 1),
            (1 + 4 * np.finfo(float).eps, 1),
            (1 + 32 * np.finfo(float).eps, 0),
            (1 + 1e-12, 0),
        ]:
            assert (
                phmt.compare_pharmacophores(
                    first,
                    query([(separation, ["hydrophobicity"])]),
                    distance_tolerance="1 nm",
                )["n_matches"]
                == expected
            )
        assert (
            phmt.compare_pharmacophores(first, first, distance_tolerance="0 nm")[
                "n_matches"
            ]
            == 1
        )
        assert (
            phmt.compare_pharmacophores(
                first, query([(1e-200, ["hydrophobicity"])]), distance_tolerance="0 nm"
            )["n_matches"]
            == 0
        )
        assert (
            phmt.compare_pharmacophores(
                first,
                query([(1e200, ["hydrophobicity"])]),
                distance_tolerance=puw.quantity(2e200, "nm"),
            )["n_matches"]
            == 1
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "shape",
    [
        Cylinder("[0,0,0] nm", "[1,0,0] nm", ".1 nm"),
        Disk("[0,0,0] nm", [0, 0, 1], ".1 nm"),
        GaussianKernel("[0,0,0] nm", ".1 nm"),
        SphereAndVector("[0,0,0] nm", ".1 nm", [1, 0, 0]),
    ],
)
def test_unsupported_shapes_are_refused_even_with_bypass(shape, skip):
    left = query([])
    left.add_interaction_site(InteractionSite(shape, "hydrophobicity"))
    with pytest.raises(ArgumentError):
        phmt.compare_pharmacophores(left, query([]), skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("feature", ["excluded volume", "included volume"])
def test_volumes_are_not_silently_interpreted_as_positive_sites(feature, skip):
    with pytest.raises(ArgumentError):
        phmt.compare_pharmacophores(
            query([(0, [feature])]), query([]), skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "option,value",
    [
        ("distance_tolerance", 0),
        ("distance_tolerance", "-1 nm"),
        ("distance_tolerance", "nan nm"),
        ("distance_tolerance", "1 ps"),
        ("max_sites", 0),
        ("max_sites", True),
        ("max_matrix_entries", -1),
        ("max_matrix_entries", 1.5),
    ],
)
def test_native_argument_contracts_survive_bypass(skip, option, value):
    with pytest.raises(ArgumentError):
        phmt.compare_pharmacophores(
            query([]), query([]), skip_digestion=skip, **{option: value}
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("option,value", [("max_sites", 1), ("max_matrix_entries", 3)])
def test_quotas_refuse_before_axis_processing_or_allocation(
    skip, option, value, monkeypatch
):
    import pharmacophoremt.comparison as owner

    left = query([(0, ["hydrophobicity"]), (1, ["hydrophobicity"])])

    def forbidden(*args, **kwargs):
        pytest.fail("Quota must precede geometry and matrix allocation")

    monkeypatch.setattr(owner, "_axis", forbidden)
    with pytest.raises(ComparisonLimitError) as caught:
        phmt.compare_pharmacophores(left, left, skip_digestion=skip, **{option: value})
    assert (
        caught.value.code == "PHMT-E111"
        and caught.value.extra["observed"] > caught.value.extra["limit"]
    )
    rebuilt = type(caught.value)(*caught.value.args)
    assert rebuilt.args == caught.value.args
    assert rebuilt.code == caught.value.code
    assert str(rebuilt) == str(caught.value)


@pytest.mark.parametrize("value", [None, 0, 1, "true"])
def test_nonboolean_controls_and_unknown_method_are_refused(value):
    left = query([])
    with pytest.raises(ArgumentError):
        phmt.compare_pharmacophores(left, left, skip_digestion=value)
    with pytest.raises(ArgumentError):
        left.similarity(left, method="unknown", skip_digestion=True)
    with pytest.raises(TypeError):
        phmt.compare_pharmacophores(left, left, unknown=True)


@pytest.mark.parametrize("skip", [False, True])
def test_scalar_facade_uses_public_tool_without_blind_forwarding(skip, monkeypatch):
    import pharmacophoremt.comparison as owner

    calls = []
    original = owner.compare_pharmacophores

    def observed(*args, **kwargs):
        calls.append(kwargs)
        return original(*args, **kwargs)

    monkeypatch.setattr(owner, "compare_pharmacophores", observed)

    class ApplicationModel(phmt.Pharmacophore):
        pass

    left = ApplicationModel()
    assert left.similarity(left, method="maximum_cardinality", skip_digestion=skip) == 0
    assert len(calls) == 1 and "skip_digestion" not in calls[0]
