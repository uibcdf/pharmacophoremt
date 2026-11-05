"""Explicit native TYR experiment and independent injective-assignment oracles."""

import hashlib
import itertools
import json
import os
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
import pytest

import phmt_test_support.tyr_cardinality as study_driver
from pharmacophoremt import _ackredit
from pharmacophoremt import pyunitwizard as puw
from phmt_test_support.tyr_cardinality import load_plan, run_study

PLAN = load_plan()
PAIRS = list(itertools.product(["328", "331"], ["nm", "pm"]))


@pytest.fixture(scope="module")
def measured(tmp_path_factory):
    retained = os.environ.get("PHMT_TYR_CARDINALITY_RESULT")
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
        data = json.loads(raw)
        assert data["plan_sha256"] == receipt["plan_sha256"]
        data["_cli_exit_code"] = receipt["cli_exit_code"]
        return data
    work = tmp_path_factory.mktemp("tyr-cardinality-cli")
    path = work / "full_results.json"
    command = [
        sys.executable,
        "-B",
        "-m",
        "phmt_test_support.tyr_cardinality",
        "--output",
        str(path),
    ]
    (work / "command.json").write_text(json.dumps(command, indent=2) + "\n")
    with (work / "cli.log").open("w") as log:
        child = subprocess.run(
            command, env=os.environ.copy(), stdout=log, stderr=subprocess.STDOUT
        )
    assert path.is_file(), (work / "cli.log").read_text()
    data = json.loads(path.read_text())
    data["_cli_exit_code"] = child.returncode
    return data


def context(data, group, policy):
    region = next(r for r in PLAN["regions"] if r["group_id"] == group)
    actual = next(
        r
        for r in data["regions"]
        if r["group_id"] == group and r["policy_id"] == policy
    )
    xyz = np.asarray(data["source_before"]["coordinates_nm"])[0]
    targets = {}
    for element, pair in region["donor_pairs_by_element"].items():
        donor, hydrogen = xyz[pair]
        vector = hydrogen - donor
        targets[element] = donor + 0.35 * vector / np.linalg.norm(vector)
    ring = xyz[region["ring_atoms"]]
    center = ring.mean(axis=0)
    normal = np.linalg.svd(ring - center)[2][-1]
    record = actual["inventories"]["ring"]["features"][0]["normal"]
    cached = puw.get_value(
        puw.QuantityRecord.from_dict(record).to_quantity(), to_unit="dimensionless"
    )
    assert abs(np.dot(normal, cached)) == pytest.approx(1, abs=1e-12)
    normal *= 1 if np.dot(normal, cached) >= 0 else -1
    return region, actual, targets, ring, center, normal


def candidate_oracles(data, group, policy):
    region, actual, targets, ring, center, normal = context(data, group, policy)
    moved_ring = ring + 0.35 * normal
    axis = int(np.argmin(np.abs(normal)))
    matrix = np.asarray(PLAN["rotation_matrices"][axis])
    pivot = center + 0.35 * normal
    rotated = (moved_ring - pivot) @ matrix.T + pivot
    return {
        "intact": (np.vstack([targets["N"], targets["O"], moved_ring]), 2, normal),
        "nitrogen_target_only": (np.vstack([targets["N"], moved_ring]), 1, normal),
        "oxygen_target_only": (np.vstack([targets["O"], moved_ring]), 1, normal),
        "ring_only": (moved_ring, 0, normal),
        "ring_rotated": (
            np.vstack([targets["N"], targets["O"], rotated]),
            2,
            matrix @ normal,
        ),
    }


def optimal_assignments(
    sites, feature_points, kinds, feature_atoms, normal, tolerance=0.02
):
    # Tiny exhaustive oracle: no SciPy/Hungarian code or runtime matcher reuse.
    edges = []
    for site in sites:
        compatible = []
        for index, point in enumerate(feature_points):
            same_kind = site["features"] == [kinds[index]]
            close = (
                np.linalg.norm(np.asarray(site["shape"]["center"]) - point) <= tolerance
            )
            if not same_kind or not close:
                continue
            oriented = kinds[index] != "aromatic ring" or abs(
                np.dot(site["shape"]["normal"], normal)
            ) >= np.cos(np.deg2rad(1))
            if oriented:
                compatible.append(index)
        edges.append([None, *compatible])
    options = []
    for selected in itertools.product(*edges):
        used = [v for v in selected if v is not None]
        if len(set(used)) == len(used):
            options.append(
                frozenset(
                    (site, tuple(feature_atoms[v]))
                    for site, v in enumerate(selected)
                    if v is not None
                )
            )
    maximum = max(map(len, options))
    return maximum, {v for v in options if len(v) == maximum}


def test_full_frozen_workload_and_actual_credit(measured):
    assert (
        measured["_cli_exit_code"] == 0 and measured["execution_status"] == "completed"
    )
    assert measured["failures"] == []
    assert measured["actual_counts"] == dict(
        generation_cells=12,
        returned_models=20,
        primary_evaluations=100,
        recovery_evaluations=24,
    )
    assert measured["input_credit_status"] == "captured"
    assert measured["attribution"]["status"] == "captured"
    payload = json.dumps(measured["attribution"])
    assert (
        "pharmacophoremt:dataset:prepared-eralpha:" + PLAN["native_sha256"] in payload
    )
    assert "PoseEvaluator.evaluate" in payload and "from_receptor_features" in payload


@pytest.mark.parametrize("group,policy", PAIRS)
def test_native_geometries_maps_and_all_injective_assignments(measured, group, policy):
    region, actual, targets, ring, center, normal = context(measured, group, policy)
    candidates = candidate_oracles(measured, group, policy)
    for control, (xyz, n, axis) in candidates.items():
        np.testing.assert_allclose(
            actual["preflight"]["candidates"][control]["custody"]["coordinates_nm"],
            [xyz],
            atol=1e-12,
            rtol=0,
        )
    for declared in PLAN["matrix"]:
        if declared["group_id"] != group or declared["policy_id"] != policy:
            continue
        cell = next(c for c in measured["cells"] if c["cell_id"] == declared["id"])
        assert cell["status"] == "returned" and cell["complete"]
        assert len(cell["models"]) == declared["expected_returned"]
        for index, model in enumerate(cell["models"]):
            sites = model["native"]["interaction_sites"]
            expected_pairs = set()
            for site in sites:
                assert site["essential"] and site["weight"] == 1
                assert site["shape"]["radius"] == pytest.approx(0.02, abs=1e-12)
                if site["features"] == ["hb acceptor"]:
                    pair = site["metadata"]["atom_indices"]
                    element = next(
                        e
                        for e, p in region["donor_pairs_by_element"].items()
                        if p == pair
                    )
                    point = targets[element]
                    expected_pairs.add(element)
                else:
                    assert site["features"] == ["aromatic ring"]
                    assert site["metadata"]["atom_indices"] == region["ring_atoms"]
                    point = center + (1 if index == 0 else -1) * 0.35 * normal
                    assert abs(
                        np.dot(site["shape"]["normal"], normal)
                    ) == pytest.approx(1, abs=1e-12)
                np.testing.assert_allclose(
                    site["shape"]["center"], point, atol=1e-12, rtol=0
                )
            assert expected_pairs == (
                set() if declared["variant"] == "ring" else {"N", "O"}
            )
            for control, (xyz, n, axis) in candidates.items():
                outcome = cell["outcomes"][control][index]
                assert outcome["status"] == "returned"
                result = outcome["result"]
                atoms = [[i] for i in range(n)] + [list(range(n, n + 6))]
                points = [*xyz[:n], xyz[n:].mean(axis=0)]
                maximum, alternatives = optimal_assignments(
                    sites, points, ["hb acceptor"] * n + ["aromatic ring"], atoms, axis
                )
                assigned = frozenset(
                    (r["site_index"], tuple(r["atom_indices"]))
                    for r in result["assignments"]
                )
                assert assigned in alternatives
                assert (
                    result["fit_value"]
                    == maximum / len(sites)
                    == declared["expected_positive_fit_values"][control][index]
                )
                assert result["status"] == (
                    "matched" if maximum == len(sites) else "not_matched"
                )
                assert len(result["missing_essential_sites"]) == len(sites) - maximum
                assert result["excluded_volume_clashes"] == []


def test_every_native_recovery_and_source_custody(measured):
    assert (
        measured["source_before"] == measured["source_after"]
        and measured["application_policy_restored"]
    )
    for region in measured["regions"]:
        assert region["inventories"] == region["inventories_after"]
        for name, after in region["candidate_custody_after"].items():
            assert after == region["preflight"]["candidates"][name]["custody"]
    for cell in measured["cells"]:
        assert len(cell["recovery"]) == 2
        for recovered in cell["recovery"]:
            assert recovered["native_equivalent"]
            original = cell["outcomes"]["intact"][recovered["model_index"]]["result"]
            result = recovered["result"]
            for key in [
                "status",
                "fit_value",
                "missing_essential_sites",
                "excluded_volume_clashes",
            ]:
                assert original[key] == result[key]
            for first, second in zip(
                original["assignments"], result["assignments"], strict=True
            ):
                assert {k: v for k, v in first.items() if k != "distance"} == {
                    k: v for k, v in second.items() if k != "distance"
                }
                values = [
                    float(
                        puw.get_value(
                            puw.QuantityRecord.from_dict(v["distance"]).to_quantity(),
                            to_unit="nm",
                        )
                    )
                    for v in [first, second]
                ]
                assert abs(values[0] - values[1]) <= 1e-12


@pytest.mark.parametrize("failed", [False, True])
def test_optional_absence_or_failure_keeps_native_cardinality(
    tmp_path, monkeypatch, failed
):
    def backend():
        if failed:
            raise RuntimeError("controlled optional tracking failure")
        return None

    monkeypatch.setattr(_ackredit, "backend", backend)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("error")
        result = run_study(tmp_path, cell_ids=["tyr328-nm-joint"])
    (tmp_path / "optional_results.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n"
    )
    assert (
        result["execution_status"] == "completed"
        and result["attribution"]["status"] != "captured"
    )
    expected = next(r for r in PLAN["matrix"] if r["id"] == "tyr328-nm-joint")
    for control, fits in expected["expected_positive_fit_values"].items():
        assert [
            o["result"]["fit_value"] for o in result["cells"][0]["outcomes"][control]
        ] == fits
