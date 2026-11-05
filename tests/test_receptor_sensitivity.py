"""Prespecified analytical receptor choices, with real molecular providers.

Literal transition tables were declared before case execution. The recorder
uses settings only; these tests independently compare its full native answers.
"""

import hashlib
import json

import numpy as np
import pytest

from pharmacophoremt import Pharmacophore
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Point, Sphere
from pharmacophoremt.screening import PoseEvaluator
from phmt_test_support.absence_inputs import system
from phmt_test_support.receptor_sensitivity import PLAN, run_case


@pytest.fixture(scope="module")
def measured(tmp_path_factory):
    directory = tmp_path_factory.mktemp("receptor-sensitivity")
    plan = json.loads(PLAN.read_text())
    results = [
        run_case(policy, directory / str(index))
        for index, policy in enumerate([plan["policy"], plan["alternate_policy"]])
    ]
    (directory / "full_results.json").write_text(
        json.dumps(results, indent=2, allow_nan=False) + "\n"
    )
    return plan, results


def family(measured, policy, name):
    return [row for row in measured[1][policy]["rows"] if row["family"] == name]


def length_value(record):
    return puw.get_value(
        puw.QuantityRecord.from_dict(record).to_quantity(), to_unit="nm"
    )


@pytest.mark.parametrize("policy", [0, 1])
@pytest.mark.parametrize("radius_index", [0, 1, 2])
def test_projection_distance_and_radius_have_declared_acceptance_bands(
    measured, policy, radius_index
):
    plan = measured[0]
    rows = family(measured, policy, "placement")[
        5 * radius_index : 5 * (radius_index + 1)
    ]
    expected = plan["expected_distance_matches_by_radius"][radius_index]
    assert [row["result"]["status"] == "matched" for row in rows] == expected
    for row, hit, distance in zip(rows, expected, plan["distance_nm"]):
        result = row["result"]
        assert result["fit_value"] == int(hit)
        assert result["missing_essential_sites"] == ([] if hit else [0])
        site = row["model"]["interaction_sites"][0]
        assert site["features"] == ["negative charge"]
        np.testing.assert_allclose(
            site["shape"]["center"], [distance, 0, 0], atol=1e-12, rtol=0
        )
        if hit:
            assert result["assignments"][0]["atom_indices"] == [2]
            assert length_value(result["assignments"][0]["distance"]) == pytest.approx(
                abs(0.5 - distance), abs=1e-12
            )


@pytest.mark.parametrize("policy", [0, 1])
@pytest.mark.parametrize("distance_index", [0, 1])
def test_point_tolerance_does_not_widen_receptor_sphere(
    measured, policy, distance_index
):
    rows = family(measured, policy, "point_contrast")[
        3 * distance_index : 3 * (distance_index + 1)
    ]
    expected = measured[0]["expected_point_contrast_matches"][distance_index]
    assert [row["result"]["status"] == "matched" for row in rows] == [expected] * 3
    assert [
        length_value(row["result"]["criteria"]["point_tolerance"]) for row in rows
    ] == pytest.approx(measured[0]["point_tolerance_nm"])
    assert all(
        row["model"]["interaction_sites"][0]["shape"]["radius"] == pytest.approx(0.125)
        for row in rows
    )


@pytest.mark.parametrize("policy", [0, 1])
def test_exclusion_sensitivity_changes_veto_without_changing_positive_coverage(
    measured, policy
):
    rows = family(measured, policy, "exclusion")
    assert [len(row["result"]["excluded_volume_clashes"]) for row in rows] == measured[
        0
    ]["expected_exclusion_clashes"]
    assert [row["result"]["status"] for row in rows] == [
        "matched",
        "matched",
        "not_matched",
    ]
    assert all(row["result"]["fit_value"] == 1 for row in rows)
    assert rows[-1]["result"]["excluded_volume_clashes"] == [
        {"site_index": 1, "atom_index": 2}
    ]


@pytest.mark.parametrize("policy", [0, 1])
@pytest.mark.parametrize("variant_index", range(7))
def test_constraint_ablation_distinguishes_requirement_weight_and_denominator(
    measured, policy, variant_index
):
    expected = measured[0]["constraint_variants"][variant_index]
    row = family(measured, policy, "constraint")[variant_index]
    result = row["result"]
    assert row["cell_id"] == "constraint-" + expected["id"]
    assert result["status"] == expected["status"]
    assert result["fit_value"] == expected["fit_value"]
    assert result["missing_essential_sites"] == expected["missing"]
    assert result["excluded_volume_clashes"] == []
    if expected["operation"] != "baseline":
        assert row["model"]["metadata"]["reason"].startswith(
            "prespecified analytical ablation:"
        )


@pytest.mark.parametrize("policy", [0, 1])
@pytest.mark.parametrize("tolerance_index", [0, 1])
def test_aromatic_sensitivity_uses_an_unoriented_axis(
    measured, policy, tolerance_index
):
    rows = family(measured, policy, "aromatic")[
        7 * tolerance_index : 7 * (tolerance_index + 1)
    ]
    assert [row["result"]["status"] == "matched" for row in rows] == measured[0][
        "expected_aromatic_matches_by_tolerance"
    ][tolerance_index]
    assert all(
        row["result"]["criteria"]["aromatic_normal"] == "unoriented_axis"
        for row in rows
    )
    assert rows[0]["result"]["fit_value"] == rows[-1]["result"]["fit_value"] == 1


@pytest.mark.parametrize("policy", [0, 1])
def test_invalid_frame_is_unscored_instead_of_a_valid_negative(measured, policy):
    (row,) = family(measured, policy, "failure")
    result = row["result"]
    assert result["status"] == "failed" and result["fit_value"] is None
    assert result["error"]["stage"] == "source"
    assert result["error"]["cause"]
    assert "assignments" not in result


@pytest.mark.parametrize("policy", [0, 1])
def test_complete_fixed_matrix_and_unchanged_source_custody(measured, policy):
    plan, outputs = measured
    output = outputs[policy]
    assert output["plan_sha256"] == hashlib.sha256(PLAN.read_bytes()).hexdigest()
    assert (
        len(output["rows"])
        == plan["valid_cells_per_policy"] + plan["failed_cells_per_policy"]
    )
    assert len({row["cell_id"] for row in output["rows"]}) == 46
    assert (
        output["source_coordinates_before_nm"] == output["source_coordinates_after_nm"]
    )
    assert output["inventories_before"] == output["inventories_after"]
    assert output["constraint_source_before"] == output["constraint_source_after"]
    assert output["application_policy_restored"]
    assert output["search_budget"] == 0 and output["holdout_access"] is False
    assert sum(row["result"]["status"] == "failed" for row in output["rows"]) == 1


def test_application_units_preserve_each_physical_answer(measured):
    first, second = measured[1]
    for a, b in zip(first["rows"], second["rows"], strict=True):
        assert a["cell_id"] == b["cell_id"] and a["settings"] == b["settings"]
        for key in [
            "status",
            "fit_value",
            "missing_essential_sites",
            "excluded_volume_clashes",
        ]:
            assert a["result"].get(key) == b["result"].get(key)
        if a["result"]["status"] != "failed":
            aa, bb = a["result"]["assignments"], b["result"]["assignments"]
            assert [(x["site_index"], x["atom_indices"]) for x in aa] == [
                (x["site_index"], x["atom_indices"]) for x in bb
            ]
            np.testing.assert_allclose(
                [length_value(x["distance"]) for x in aa],
                [length_value(x["distance"]) for x in bb],
                atol=1e-12,
                rtol=0,
            )


@pytest.mark.parametrize("policy", [["nm", "ps", "radians"], ["pm", "fs", "degrees"]])
@pytest.mark.parametrize("shape", ["point", "sphere"])
@pytest.mark.parametrize("offset", [-1, 0, 1])
def test_numerical_boundary_policy_keeps_resolved_inside_and_outside_poses(
    policy, shape, offset
):
    # Supplementary #84 guard: the margin is vastly above conversion roundoff.
    with puw.context(standard_units=policy):
        query = Pharmacophore()
        geometry = (
            Point("[0,0,0] nm") if shape == "point" else Sphere("[0,0,0] nm", ".125 nm")
        )
        query.add_interaction_site(InteractionSite(geometry, "negative charge"))
        source = system("[Cl-]", [[0.125 + offset * 2**-30, 0, 0]])
        result = PoseEvaluator(query, point_tolerance=".125 nm").evaluate(source)
        assert result["status"] == ("matched" if offset <= 0 else "not_matched")
        assert result["fit_value"] == int(offset <= 0)


@pytest.mark.parametrize("policy", [0, 1])
def test_positive_site_numerical_allowance_is_explicit_in_criteria(measured, policy):
    row = family(measured, policy, "placement")[0]
    assert (
        row["result"]["criteria"]["position_comparison_relative_slack"]
        == 8 * np.finfo(np.float64).eps
    )
