"""Independent prepared-geometry oracles for the prespecified #85 experiment."""

import hashlib
import json
import math

import numpy as np
import pytest

from pharmacophoremt import pyunitwizard as puw
from phmt_test_support.prepared_receptor_sensitivity import PLAN, run_case


@pytest.fixture(scope="module")
def measured(tmp_path_factory):
    directory = tmp_path_factory.mktemp("prepared-sensitivity")
    plan = json.loads(PLAN.read_text())
    outputs = [
        run_case(policy, directory / str(index))
        for index, policy in enumerate(plan["policies"])
    ]
    (directory / "full_results.json").write_text(
        json.dumps(outputs, indent=2, allow_nan=False) + "\n"
    )
    return plan, outputs


def family(measured, policy, name):
    return [row for row in measured[1][policy]["rows"] if row["family"] == name]


def coordinates(measured, policy):
    return np.asarray(measured[1][policy]["inputs_before"]["coordinates_nm"])[0]


def original_plane(measured, policy):
    # Independent test-only oracle, never used by the executable case recorder.
    points = coordinates(measured, policy)[measured[0]["ring_atoms"]]
    center = points.mean(axis=0)
    return center, np.linalg.svd(points - center)[2][-1]


def value(record, unit="nm"):
    return puw.get_value(
        puw.QuantityRecord.from_dict(record).to_quantity(), to_unit=unit
    )


@pytest.mark.parametrize("policy", [0, 1])
@pytest.mark.parametrize("face_index", [0, 1])
@pytest.mark.parametrize("radius_index", [0, 1, 2])
def test_predeclared_placement_bands_and_separate_opposite_face(
    measured, policy, face_index, radius_index
):
    plan = measured[0]
    rows = family(measured, policy, "placement")[
        9 * face_index + 3 * radius_index : 9 * face_index + 3 * (radius_index + 1)
    ]
    expected = (
        plan["expected_positive_face_matches_by_radius"][radius_index]
        if face_index == 0
        else [False] * 3
    )
    assert [row["result"]["status"] == "matched" for row in rows] == expected
    center, normal = original_plane(measured, policy)
    for row, distance, hit in zip(rows, plan["distance_nm"], expected, strict=True):
        result, site = row["result"], row["model"]["interaction_sites"][0]
        assert result["fit_value"] == int(hit)
        assert result["missing_essential_sites"] == ([] if hit else [0])
        assert site["metadata"]["atom_indices"] == plan["ring_atoms"]
        assert site["features"] == ["aromatic ring"]
        np.testing.assert_allclose(
            site["shape"]["center"],
            center + [0, 0, plan["face_signs"][face_index] * distance],
            rtol=0,
            atol=1e-12,
        )
        assert abs(np.dot(site["shape"]["normal"], normal)) == pytest.approx(
            1, abs=1e-12
        )
        if hit:
            assert result["assignments"][0]["atom_indices"] == plan["ring_atoms"]
            assert value(result["assignments"][0]["distance"]) == pytest.approx(
                abs(0.35 - distance), abs=1e-12
            )


@pytest.mark.parametrize("policy", [0, 1])
@pytest.mark.parametrize("radius_index", [0, 1, 2])
def test_every_steric_veto_matches_independent_original_coordinate_oracle(
    measured, policy, radius_index
):
    plan = measured[0]
    row = family(measured, policy, "exclusion")[radius_index]
    original = coordinates(measured, policy)
    moved = original + plan["translation_nm"]
    radius = plan["exclusion_radius_nm"][radius_index]
    expected = [
        {"site_index": 1 + site, "atom_index": atom}
        for site, excluded in enumerate(plan["heavy_atoms"])
        for atom in plan["heavy_atoms"]
        if math.dist(moved[atom], original[excluded]) < radius
    ]
    result = row["result"]
    assert result["excluded_volume_clashes"] == expected
    assert result["fit_value"] == 1
    assert result["status"] == ("not_matched" if expected else "matched")
    assert len(row["model"]["interaction_sites"]) == 12
    if radius_index == 0:
        assert expected == []
    if radius_index == 2:
        assert len(expected) >= 11


@pytest.mark.parametrize("policy", [0, 1])
@pytest.mark.parametrize("axis_index", [0, 1])
@pytest.mark.parametrize("tolerance_index", [0, 1, 2, 3])
def test_rotated_candidate_obeys_independent_plane_axis_angle(
    measured, policy, axis_index, tolerance_index
):
    plan = measured[0]
    _, normal = original_plane(measured, policy)
    transformed_normal = np.asarray(plan["rotation"]) @ normal
    angle = math.degrees(
        math.acos(min(1, abs(float(np.dot(normal, transformed_normal)))))
    )
    row = family(measured, policy, "orientation")[4 * axis_index + tolerance_index]
    hit = angle <= plan["direction_tolerance_degrees"][tolerance_index]
    assert row["result"]["status"] == ("matched" if hit else "not_matched")
    assert row["result"]["fit_value"] == int(hit)
    assert row["result"]["criteria"]["aromatic_normal"] == "unoriented_axis"
    if hit:
        assert value(row["result"]["assignments"][0]["distance"]) == pytest.approx(
            0, abs=1e-12
        )


@pytest.mark.parametrize("policy", [0, 1])
def test_source_custody_and_provider_transforms_keep_the_frozen_input(measured, policy):
    plan, outputs = measured
    output = outputs[policy]
    assert (
        output["input_identity"]["native_evidence"]["uncompressed_sha256"]
        == plan["native_sha256"]
    )
    assert output["inputs_before"] == output["inputs_after"]
    assert output["inventories_before"] == output["inventories_after"]
    assert output["selection"] == [*range(791, 802), *range(2772, 2781)]
    assert "NaN" in output["inputs_before"]["chemical_state_json"]
    original = coordinates(measured, policy)
    assert original.shape == (4047, 3)
    center, _ = original_plane(measured, policy)
    np.testing.assert_allclose(
        center, [10.3282, 1.9207666666666665, 2.0210166666666667], atol=1e-12, rtol=0
    )
    np.testing.assert_allclose(
        output["candidate_coordinates_nm"]["translated"],
        [original + plan["translation_nm"]],
        atol=1e-12,
        rtol=0,
    )
    expected = (
        (original - center) @ np.asarray(plan["rotation"]).T
        + center
        + plan["translation_nm"]
    )
    np.testing.assert_allclose(
        output["candidate_coordinates_nm"]["rotated_translated"],
        [expected],
        atol=1e-12,
        rtol=0,
    )


@pytest.mark.parametrize("policy", [0, 1])
def test_exclusion_removal_records_a_hypothesis_change_without_modifying_source(
    measured, policy
):
    output = measured[1][policy]
    (row,) = family(measured, policy, "curation")
    assert row["result"]["status"] == "matched" and row["result"]["fit_value"] == 1
    assert row["result"]["excluded_volume_clashes"] == []
    assert output["wide_before"] == output["wide_after"]
    assert len(row["model"]["interaction_sites"]) == 1
    metadata = row["model"]["metadata"]
    assert metadata["reason"] == "prespecified removal of PHE404 exclusion vetoes"
    assert metadata["site_map"] == [{"source_site_index": 0, "site_index": 0}]
    # Internal curation snapshots retain the legacy envelope; the public writer
    # adds the top-level wire schema. All model data must still match exactly.
    saved_source = dict(metadata["source_model"])
    saved_source.setdefault("schema", output["wide_before"]["schema"])
    assert saved_source == output["wide_before"]


@pytest.mark.parametrize("policy", [0, 1])
def test_original_negative_and_real_failed_frame_remain_distinct(measured, policy):
    (row,) = family(measured, policy, "original")
    assert row["result"]["status"] == "not_matched" and row["result"]["fit_value"] == 0
    (failed,) = family(measured, policy, "failure")
    result = failed["result"]
    assert result["status"] == "failed" and result["fit_value"] is None
    assert result["error"]["stage"] == "source" and result["error"]["cause"]
    assert "assignments" not in result


@pytest.mark.parametrize("policy", [0, 1])
def test_complete_prespecified_ledger_unit_policy_and_actual_input_credit(
    measured, policy
):
    plan, outputs = measured
    output = outputs[policy]
    assert output["plan_sha256"] == hashlib.sha256(PLAN.read_bytes()).hexdigest()
    assert (
        len(output["rows"])
        == plan["valid_cells_per_policy"] + plan["failed_cells_per_policy"]
    )
    assert len({row["cell_id"] for row in output["rows"]}) == 32
    assert sum(row["result"]["status"] == "failed" for row in output["rows"]) == 1
    assert output["application_policy_restored"] and output["search_budget"] == 0
    assert output["holdout_access"] is False
    assert "pharmacophoremt:dataset:prepared-eralpha:" + plan[
        "native_sha256"
    ] in json.dumps(output["workflow_attribution"])
    assert (
        sum(
            row["result"].get("attribution", {}).get("status") == "captured"
            for row in output["rows"]
        )
        == 31
    )


def test_each_physical_answer_is_preserved_across_application_units(measured):
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
        aa, bb = a["result"].get("assignments", []), b["result"].get("assignments", [])
        assert [(x["site_index"], x["atom_indices"]) for x in aa] == [
            (x["site_index"], x["atom_indices"]) for x in bb
        ]
        np.testing.assert_allclose(
            [value(x["distance"]) for x in aa],
            [value(x["distance"]) for x in bb],
            atol=1e-12,
            rtol=0,
        )
