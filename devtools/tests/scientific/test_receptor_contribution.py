"""Independent original-coordinate oracles for every frozen #90 result."""

import hashlib
import itertools
import json
import math
import os
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
import pytest

import phmt_test_support.receptor_contribution as study_driver
from pharmacophoremt import _ackredit
from pharmacophoremt import pyunitwizard as puw
from phmt_test_support.receptor_contribution import aggregate, load_plan, run_study

PLAN = load_plan()
PAIRS = list(itertools.product(["337", "367", "404"], ["nm", "pm"]))
SCIENCE_FIELDS = [
    "status",
    "fit_value",
    "assignments",
    "missing_essential_sites",
    "excluded_volume_clashes",
    "selected_atom_indices",
    "chemical_state",
    "structure_index",
]


@pytest.fixture(scope="module")
def measured(tmp_path_factory):
    retained = os.environ.get("PHMT_RECEPTOR_CONTRIBUTION_RESULT")
    if retained:
        path = Path(retained)
        receipt = json.loads(path.with_suffix(".receipt.json").read_text())
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == receipt["results_sha256"]
        assert (
            hashlib.sha256(Path(study_driver.__file__).read_bytes()).hexdigest()
            == receipt["driver_sha256"]
        )
        assert receipt["plan_sha256"] == study_driver.PLAN_SHA256
        output = json.loads(raw)
        assert output["plan_sha256"] == receipt["plan_sha256"]
        output["_cli_exit_code"] = receipt["cli_exit_code"]
        return output
    work = tmp_path_factory.mktemp("receptor-contribution-cli")
    result = work / "full_results.json"
    command = [
        sys.executable,
        "-B",
        "-m",
        "phmt_test_support.receptor_contribution",
        "--output",
        str(result),
    ]
    with (work / "cli.log").open("w") as log:
        child = subprocess.run(
            command, env=os.environ.copy(), stdout=log, stderr=subprocess.STDOUT
        )
    assert result.is_file(), (work / "cli.log").read_text()
    output = json.loads(result.read_text())
    output["_cli_exit_code"] = child.returncode
    output["_cli_command"] = command
    return output


def region_data(output, group, policy):
    return next(
        r
        for r in output["regions"]
        if r["group_id"] == group and r["policy_id"] == policy
    )


def raw_geometry(output, group, policy):
    region = next(r for r in PLAN["regions"] if r["group_id"] == group)
    coordinates = np.asarray(output["source_before"]["coordinates_nm"])[0]
    donor, hydrogen = coordinates[region["donor_atoms"]]
    direction = hydrogen - donor
    direction /= np.linalg.norm(direction)
    ring = coordinates[region["ring_atoms"]]
    center = ring.mean(axis=0)
    axis = np.linalg.svd(ring - center)[2][-1]
    record = region_data(output, group, policy)["inventories"]["ring"]["features"][0][
        "normal"
    ]
    cached = puw.get_value(
        puw.QuantityRecord.from_dict(record).to_quantity(), to_unit="dimensionless"
    )
    assert abs(np.dot(axis, cached)) == pytest.approx(1, abs=1e-12)
    axis *= 1 if np.dot(axis, cached) >= 0 else -1
    return region, coordinates, donor, direction, ring, center, axis


def original_candidate_oracle(output, group, policy):
    region, coordinates, donor, direction, ring, center, axis = raw_geometry(
        output, group, policy
    )
    oxygen = donor + 0.35 * direction
    ring = ring + 0.35 * axis
    shift = np.array([1.0, 0, 0])
    rotation = np.asarray(
        PLAN["candidate_definition"]["rotation"]["matrices"][
            int(np.argmin(np.abs(axis)))
        ]
    )
    ring_center = center + 0.35 * axis
    return {
        "intact": np.vstack([oxygen, ring]),
        "donor_displaced": np.vstack([oxygen + shift, ring]),
        "ring_displaced": np.vstack([oxygen, ring + shift]),
        "both_displaced": np.vstack([oxygen + shift, ring + shift]),
        "ring_rotated": np.vstack(
            [oxygen, (ring - ring_center) @ rotation.T + ring_center]
        ),
    }


def expected_choices(row):
    ds = [0.28, 0.35] if row["variant"] != "ring" else [None]
    rs = (
        [(0.35, 1), (0.35, -1), (0.45, 1), (0.45, -1)]
        if row["variant"] != "donor"
        else [(None, None)]
    )
    return list(itertools.product(ds, rs))[: row["expected_returned"]]


def test_complete_cli_workload_retains_every_attempt_and_unscored_slot(measured):
    assert measured["_cli_exit_code"] == 0
    assert measured["execution_status"] == "completed" and measured["failures"] == []
    assert len(measured["regions"]) == 6
    assert measured["actual_counts"] == dict(
        generation_cells=60,
        returned_models=342,
        primary_evaluations=1710,
        successful_primary_evaluations=1710,
        recovery_evaluations=108,
        unevaluated_candidate_slots=30,
    )
    assert {r["cell_id"] for r in measured["cells"]} == {
        r["id"] for r in PLAN["matrix"]
    }


@pytest.mark.parametrize("group,policy", PAIRS)
def test_original_geometry_defines_all_candidates_and_generated_models(
    measured, group, policy
):
    region, coordinates, donor, direction, ring, center, axis = raw_geometry(
        measured, group, policy
    )
    actual = region_data(measured, group, policy)
    for control, expected in original_candidate_oracle(measured, group, policy).items():
        preflight = actual["preflight"]["candidates"][control]
        np.testing.assert_allclose(
            preflight["custody"]["coordinates_nm"], [expected], atol=1e-12, rtol=0
        )
        kinds = preflight["inventory"]["features"]
        assert [f["atom_indices"] for f in kinds if f["kind"] == "hb acceptor"] == [[0]]
        assert [f["atom_indices"] for f in kinds if f["kind"] == "aromatic ring"] == [
            list(range(1, 7))
        ]
    for declared in PLAN["matrix"]:
        if declared["group_id"] != group or declared["policy_id"] != policy:
            continue
        cell = next(r for r in measured["cells"] if r["cell_id"] == declared["id"])
        assert cell["status"] == "returned"
        assert len(cell["models"]) == declared["expected_returned"]
        for model, (distance, (ring_distance, face)) in zip(
            cell["models"], expected_choices(declared), strict=True
        ):
            sites = model["native"]["interaction_sites"]
            npositive = 1 if declared["variant"] in ["donor", "ring"] else 2
            expected_centers, expected_atoms = [], []
            if distance is not None:
                expected_centers.append(donor + distance * direction)
                expected_atoms.append(region["donor_atoms"])
            if ring_distance is not None:
                expected_centers.append(center + face * ring_distance * axis)
                expected_atoms.append(region["ring_atoms"])
            for index, (point, atoms) in enumerate(
                zip(expected_centers, expected_atoms, strict=True)
            ):
                site = sites[index]
                np.testing.assert_allclose(
                    site["shape"]["center"], point, atol=1e-12, rtol=0
                )
                assert site["metadata"]["atom_indices"] == atoms
                assert site["essential"] and site["weight"] == 1
                assert site["shape"]["radius"] == pytest.approx(
                    declared["query_radius_nm"], abs=1e-12
                )
                if site["shape"]["type"] == "disk":
                    assert abs(np.dot(site["shape"]["normal"], axis)) == pytest.approx(
                        1, abs=1e-12
                    )
            if declared["exclusion_radius_nm"] is None:
                assert len(sites) == npositive
            else:
                assert len(sites) == npositive + 11
                assert model["native"]["metadata"]["excluded_volumes"][
                    "global_site_indices"
                ] == list(range(npositive, npositive + 11))
                for site, atom in zip(
                    sites[npositive:], region["heavy_atom_indices"], strict=True
                ):
                    assert site["weight"] == 0 and site["features"] == [
                        "excluded volume"
                    ]
                    np.testing.assert_allclose(
                        site["shape"]["center"], coordinates[atom], atol=1e-12, rtol=0
                    )


@pytest.mark.parametrize("group,policy", PAIRS)
def test_every_fit_assignment_and_strict_inside_pair_matches_independent_oracles(
    measured, group, policy
):
    region, coordinates, *_ = raw_geometry(measured, group, policy)
    candidates = original_candidate_oracle(measured, group, policy)
    for declared in PLAN["matrix"]:
        if declared["group_id"] != group or declared["policy_id"] != policy:
            continue
        cell = next(r for r in measured["cells"] if r["cell_id"] == declared["id"])
        npositive = 1 if declared["variant"] in ["donor", "ring"] else 2
        for control, values in declared["expected_positive_fit_values"].items():
            for outcome, fit in zip(cell["outcomes"][control], values, strict=True):
                assert outcome["status"] == "returned"
                result = outcome["result"]
                pairs = (
                    []
                    if declared["exclusion_radius_nm"] is None
                    else [
                        dict(site_index=npositive + local, atom_index=atom)
                        for local, source_atom in enumerate(
                            region["heavy_atom_indices"]
                        )
                        for atom, position in enumerate(candidates[control])
                        if math.dist(position, coordinates[source_atom])
                        < declared["exclusion_radius_nm"]
                    ]
                )
                assert result["fit_value"] == fit
                assert result["excluded_volume_clashes"] == pairs
                assert result["status"] == (
                    "matched" if fit == 1 and not pairs else "not_matched"
                )
                assert len(result["missing_essential_sites"]) == npositive - round(
                    fit * npositive
                )
                for assignment in result["assignments"]:
                    assert assignment["atom_indices"] in [[0], list(range(1, 7))]
                if (
                    control == "intact"
                    and fit == 1
                    and declared["exclusion_radius_nm"] == 0.4
                ):
                    assert len(pairs) >= 7
                assert "model_metadata" not in result
                assert cell["models"][outcome["model_index"]][
                    "evaluation_model_metadata"
                ]


def test_prefixes_and_zero_budgets_keep_actual_completion_and_denominators(measured):
    for declared in PLAN["matrix"]:
        cell = next(r for r in measured["cells"] if r["cell_id"] == declared["id"])
        enumeration = cell["generation_report"]["enumeration"]
        assert enumeration["returned"] == declared["expected_returned"]
        assert enumeration["remaining"] == declared["expected_remaining"]
        assert cell["complete"] == declared["expected_complete"]
        for summary in cell["aggregates"].values():
            assert summary["failed"] == 0
            assert summary["enumeration_complete"] == declared["expected_complete"]
            if declared["max_hypotheses"] == 0:
                assert summary["status"] == "unevaluated"
                assert summary["best_positive_fit"] is summary["any_accepted"] is None
        if declared["block"] == "budget":
            assert not cell["aggregates"]["intact"]["any_accepted"]
            assert not cell["complete"]


def test_all_native_recoveries_preserve_geometry_and_scientific_outcomes(measured):
    count = 0
    for cell in measured["cells"]:
        assert len(cell["recovery"]) == (2 if cell["models"] else 0)
        for recovered in cell["recovery"]:
            assert recovered["native_equivalent"]
            original = cell["outcomes"]["intact"][recovered["model_index"]]["result"]
            for key in SCIENCE_FIELDS:
                if key != "assignments":
                    assert original[key] == recovered["result"][key], (
                        cell["cell_id"],
                        key,
                    )
            before = original["assignments"]
            after = recovered["result"]["assignments"]
            assert len(before) == len(after)
            for first, second in zip(before, after, strict=True):
                assert {k: v for k, v in first.items() if k != "distance"} == {
                    k: v for k, v in second.items() if k != "distance"
                }
                distances = [
                    float(
                        puw.get_value(
                            puw.QuantityRecord.from_dict(
                                item["distance"]
                            ).to_quantity(),
                            to_unit="nm",
                        )
                    )
                    for item in [first, second]
                ]
                assert abs(distances[0] - distances[1]) <= PLAN["geometry_tolerance_nm"]
            count += 1
    assert count == 108


def test_original_source_candidates_inventories_and_application_policy_are_unchanged(
    measured,
):
    assert measured["source_before"] == measured["source_after"]
    assert measured["application_policy_restored"]
    for region in measured["regions"]:
        assert region["inventories"] == region["inventories_after"]
        for name, after in region["candidate_custody_after"].items():
            assert after == region["preflight"]["candidates"][name]["custody"]
    for group in ["337", "367", "404"]:
        first, second = (
            region_data(measured, group, "nm"),
            region_data(measured, group, "pm"),
        )
        for name in PLAN["controls"]:
            a = first["preflight"]["candidates"][name]["custody"]["coordinates_nm"]
            b = second["preflight"]["candidates"][name]["custody"]["coordinates_nm"]
            np.testing.assert_allclose(a, b, rtol=0, atol=1e-12)


def test_actual_credit_names_loaded_input_and_reached_operations(measured):
    assert measured["workflow_attribution"]["status"] == "captured"
    payload = json.dumps(measured["workflow_attribution"])
    assert (
        "pharmacophoremt:dataset:prepared-eralpha:" + PLAN["native_sha256"] in payload
    )
    assert "PoseEvaluator.evaluate" in payload and "from_receptor_features" in payload
    assert "get_excluded_volume_sites" in payload


@pytest.mark.parametrize("fail", [False, True])
def test_optional_tracking_absence_or_failure_preserves_the_frozen_subset(
    tmp_path, monkeypatch, fail
):
    def backend():
        if fail:
            raise RuntimeError("controlled optional tracking failure")
        return None

    monkeypatch.setattr(_ackredit, "backend", backend)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("error")
        output = run_study(
            tmp_path, cell_ids=["phe404-nm-baseline-joint_ex40-r0.02-b8"]
        )
    (tmp_path / "optional_results.json").write_text(
        json.dumps(output, indent=2, allow_nan=False) + "\n"
    )
    assert output["execution_status"] == "completed"
    cell = output["cells"][0]
    declared = next(r for r in PLAN["matrix"] if r["id"] == cell["cell_id"])
    for control, fits in declared["expected_positive_fit_values"].items():
        assert [v["result"]["fit_value"] for v in cell["outcomes"][control]] == fits
    assert cell["aggregates"]["intact"]["full_positive_vetoed"] == 1
    assert output["workflow_attribution"]["status"] != "captured"


def test_failed_attempt_is_not_a_valid_negative_or_unscored_zero():
    result = aggregate(dict(complete=False), [dict(status="failed", error={})])
    assert result["status"] == "partial_failure"
    assert result["failed"] == 1 and result["evaluated"] == 0
    assert result["best_positive_fit"] is result["any_accepted"] is None
