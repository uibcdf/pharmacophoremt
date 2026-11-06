"""Independent #97 workload/oracle guards; never run the timing campaign in CI."""

import warnings
from copy import deepcopy

import pytest

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_receptor_features
from phmt_test_support.benchmark_cached_generation import inputs, load_plan, oracle

PLAN = load_plan()


@pytest.mark.parametrize(
    "case_id",
    ["size_1_1", "size_2_2", "budget_0", "budget_1", "budget_64", "exclusions_16"],
)
@pytest.mark.parametrize("policy", [["nm", "ps", "radians"], ["pm", "fs", "degrees"]])
def test_independent_oracle_and_exact_coverage_with_other_unit_policy(case_id, policy):
    case = next(c for c in PLAN["cases"] if c["id"] == case_id)
    source, options = inputs(case, PLAN)
    with puw.context(standard_units=policy), warnings.catch_warnings():
        warnings.simplefilter("error")
        result = from_receptor_features(source, **options)
        measured = oracle(result, case, PLAN, source)
    assert measured["returned"] == min(
        case["budget"], 2 ** case["donors"] * 4 ** case["rings"]
    )
    assert (
        measured["sites_per_model"]
        == case["donors"] + case["rings"] + case["exclusions"]
    )


@pytest.mark.parametrize(
    "corruption",
    [
        "center",
        "normal",
        "radius",
        "source",
        "count",
        "complete",
        "choice",
        "weight",
        "essential",
        "exclusion",
    ],
)
def test_oracle_detects_wrong_geometry_decisions_and_false_coverage(corruption):
    case = next(c for c in PLAN["cases"] if c["id"] == "exclusions_16")
    source, options = inputs(case, PLAN)
    result = from_receptor_features(source, **options)
    model = result["models"][0]
    if corruption == "center":
        model.interaction_sites[0].shape.center = puw.quantity([9, 0, 0], "nm")
    elif corruption == "normal":
        model.interaction_sites[2].shape.normal = puw.quantity(
            [1, 0, 0], "dimensionless"
        )
    elif corruption == "radius":
        model.interaction_sites[0].shape.radius = puw.quantity(0.2, "nm")
    elif corruption == "source":
        result["report"]["source_inventory"]["structure_index"] = 999
    elif corruption == "count":
        result["report"]["enumeration"]["total_possible"] = 8
    elif corruption == "complete":
        result["complete"] = True
    elif corruption == "choice":
        model.metadata["generation"]["choices"][0]["distance_index"] = 1
    elif corruption == "weight":
        model.interaction_sites[0].weight = 0
    elif corruption == "essential":
        model.interaction_sites[0].essential = False
    else:
        model.interaction_sites[-1].metadata["atom_indices"] = [999]
    with pytest.raises(AssertionError):
        oracle(result, case, PLAN, source)


def test_plan_has_independent_size_budget_and_exclusion_axes():
    assert len(PLAN["cases"]) == 10
    sizes = [c for c in PLAN["cases"] if c["id"].startswith("size_")]
    assert [(c["donors"], c["rings"], c["budget"]) for c in sizes] == [
        (n, n, 8) for n in [1, 2, 4, 8]
    ]
    original = deepcopy(PLAN)
    source, options = inputs(sizes[-1], PLAN)
    result = from_receptor_features(source, **options)
    assert oracle(result, sizes[-1], PLAN, source)["total_possible"] == 16777216
    assert PLAN == original


def test_cached_workload_does_not_request_molecular_operations(monkeypatch):
    import molsysmt as msm

    def forbidden(*args, **kwargs):
        pytest.fail("cached generation requested a molecular operation")

    for name in ("get", "set", "convert", "select", "extract", "copy"):
        monkeypatch.setattr(msm, name, forbidden, raising=False)
    monkeypatch.setattr(msm.structure, "get_vectors", forbidden, raising=False)
    case = next(c for c in PLAN["cases"] if c["id"] == "exclusions_16")
    source, options = inputs(case, PLAN)
    result = from_receptor_features(source, **options)
    assert oracle(result, case, PLAN, source)["returned"] == 8
