"""Explicit frozen #93 receiving experiment and independent geometric oracles."""

import copy
import hashlib
import json
import os
import subprocess
import sys
import warnings
from pathlib import Path

import numpy as np
import pytest

import phmt_test_support.carbonyl_acceptor_receiving as driver
from pharmacophoremt import _ackredit
from pharmacophoremt import pyunitwizard as puw

PLAN = driver.load_plan()


@pytest.fixture(scope="module")
def measured(tmp_path_factory):
    retained = os.environ.get("PHMT_CARBONYL_RECEIVING_RESULT")
    if retained:
        path = Path(retained)
        receipt = json.loads(path.with_suffix(".receipt.json").read_text())
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == receipt["results_sha256"]
        assert (
            hashlib.sha256(Path(driver.__file__).read_bytes()).hexdigest()
            == receipt["driver_sha256"]
        )
        assert receipt["plan_sha256"] == driver.PLAN_SHA256
        data = json.loads(raw)
        assert data["plan_sha256"] == driver.PLAN_SHA256
        data["_cli_exit_code"] = receipt["cli_exit_code"]
        return data
    work = tmp_path_factory.mktemp("carbonyl-receiving-cli")
    path = work / "full_results.json"
    command = [
        sys.executable,
        "-B",
        "-m",
        "phmt_test_support.carbonyl_acceptor_receiving",
        "--output",
        str(path),
    ]
    (work / "command.json").write_text(json.dumps(command, indent=2) + "\n")
    with (work / "cli.log").open("w") as log:
        child = subprocess.run(
            command, env=os.environ.copy(), stdout=log, stderr=subprocess.STDOUT
        )
    assert path.is_file(), (work / "cli.log").read_text()
    raw = path.read_bytes()
    path.with_suffix(".receipt.json").write_text(
        json.dumps(
            dict(
                results_sha256=hashlib.sha256(raw).hexdigest(),
                driver_sha256=hashlib.sha256(
                    Path(driver.__file__).read_bytes()
                ).hexdigest(),
                plan_sha256=driver.PLAN_SHA256,
                cli_exit_code=child.returncode,
            ),
            indent=2,
        )
        + "\n"
    )
    data = json.loads(raw)
    data["_cli_exit_code"] = child.returncode
    return data


def quantity(record, unit):
    return puw.get_value(
        puw.QuantityRecord.from_dict(record).to_quantity(), to_unit=unit
    )


def carbonyl_oracle(frame):
    # Test-only, from literal original atoms; never a case/runtime molecular kernel.
    substituent, carbon, oxygen = np.asarray(
        PLAN["source"]["coordinates"]["values"][frame]
    )
    bond = carbon - oxygen
    bond /= np.linalg.norm(bond)
    side = substituent - carbon
    side -= np.dot(side, bond) * bond
    side /= np.linalg.norm(side)
    directions = np.array(
        [-bond / 2 + np.sqrt(3) * side / 2, -bond / 2 - np.sqrt(3) * side / 2]
    )
    return oxygen, directions


def native_payload(measured):
    record = measured["policies"][0]["provider"]
    payload = copy.deepcopy(record["payload"])
    for key, layout in record["array_layouts"].items():
        if key != "origins":
            payload[key] = np.asarray(payload[key], dtype=layout["dtype"]).reshape(
                layout["shape"]
            )
    payload["origins"] = puw.QuantityRecord.from_dict(payload["origins"]).to_quantity()
    return payload


def receive(payload):
    return driver._receive_payload(
        payload, n_atoms=3, selection=[2], structures=[0, 1, 0]
    )


def test_full_workload_and_actual_software_model_credit(measured):
    assert measured["_cli_exit_code"] == 0
    assert measured["execution_status"] == "completed" and measured["failures"] == []
    assert measured["actual_counts"] == PLAN["planned_counts"]
    assert measured["attribution"]["status"] == "captured"
    text = json.dumps(measured["attribution"])
    assert "from_receptor_projections" in text and "PoseEvaluator.evaluate" in text
    assert "prepared-eralpha" not in text
    for context in measured["policies"]:
        payload = context["provider"]["payload"]
        assert payload["method"] == "ideal_local_geometry"
        assert any(
            item["roles"] == ["geometric_inspiration"]
            for item in payload["attribution"]["items"]
        )


@pytest.mark.parametrize("policy", ["nm", "pm"])
def test_native_sparse_correspondence_and_original_coordinate_oracles(measured, policy):
    record = next(p for p in measured["policies"] if p["policy_id"] == policy)[
        "provider"
    ]
    actual = record["payload"]
    source = PLAN["source"]
    assert actual["selected_atom_indices"] == [2]
    assert actual["site_atom_indices"] == [2]
    for key in [
        "site_roles",
        "site_models",
        "support_atom_indices",
        "support_atom_offsets",
        "status",
        "direction_site_indices",
        "direction_structure_indices",
        "direction_structure_positions",
        "direction_indices",
    ]:
        assert actual[key] == source[key]
    assert actual["evaluated_structure_indices"] == [0, 1, 0]
    assert actual["image_offsets"] == source["expected_image_offsets"]
    assert actual["image_vectors"] == source["expected_image_vectors"]
    expected_directions, origins = [], []
    for frame in [0, 1, 0]:
        origin, directions = carbonyl_oracle(frame)
        expected_directions.extend(directions)
        origins.extend([origin, origin])
    np.testing.assert_allclose(
        actual["directions"], expected_directions, atol=1e-12, rtol=0
    )
    np.testing.assert_allclose(
        quantity(actual["origins"], "nm"), origins, atol=1e-12, rtol=0
    )
    assert record["array_layouts"]["status"] == dict(shape=[3, 1], dtype="uint8")
    assert record["array_layouts"]["direction_structure_positions"] == dict(
        shape=[6], dtype="int64"
    )
    assert actual["software"]["molsysmt"] == driver.msm.__version__


@pytest.mark.parametrize(
    "declared", PLAN["matrix"], ids=[r["id"] for r in PLAN["matrix"]]
)
def test_every_query_candidate_orientation_and_assignment(measured, declared):
    cell = next(c for c in measured["cells"] if c["cell_id"] == declared["id"])
    assert cell["status"] == "returned" and len(cell["models"]) == 2
    context = next(
        p for p in measured["policies"] if p["policy_id"] == declared["policy_id"]
    )
    origin, directions = carbonyl_oracle(declared["source_structure_index"])
    assert len(cell["inventory_before"]["features"]) == 1
    assert cell["inventory_before"]["features"][0]["direction"] is None
    for index, model in enumerate(cell["models"]):
        assert len(model["native"]["interaction_sites"]) == 1
        site = model["native"]["interaction_sites"][0]
        target = origin + 0.35 * directions[index]
        assert (
            site["features"] == ["hb donor"]
            and site["essential"]
            and site["weight"] == 1
        )
        assert site["shape"]["type"] == "sphere and vector"
        assert site["shape"]["radius"] == pytest.approx(0.02, abs=1e-12)
        np.testing.assert_allclose(site["shape"]["center"], target, atol=1e-12, rtol=0)
        np.testing.assert_allclose(
            site["shape"]["direction"], -directions[index], atol=1e-12, rtol=0
        )
        assert site["metadata"]["atom_indices"] == [2]
        evidence = site["metadata"]["projection"]["evidence"]
        assert evidence["source_support"] == [2, 1, 0]
        assert evidence["source_structure_position"] == declared["structure_position"]
        assert evidence["source_structure_index"] == declared["source_structure_index"]
        assert evidence["provider_local_direction"] == index
        assert evidence["provider_result_sha256"] == context["provider"]["sha256"]
        for control in PLAN["controls"]:
            name = control["id"]
            point = (
                origin
                + 0.35 * directions[control["source_lobe"]]
                + control["displacement"]["values"]
            )
            axis = control["donor_axis_sign"] * directions[control["source_lobe"]]
            expected = np.array([point + 0.1 * axis, point])
            np.testing.assert_allclose(
                cell["candidates_before"][name]["coordinates_nm"],
                [expected],
                atol=1e-12,
                rtol=0,
            )
            inventory = cell["candidate_inventories"][name]["features"]
            assert len(inventory) == 1 and inventory[0]["atom_indices"] == [1, 0]
            np.testing.assert_allclose(
                quantity(inventory[0]["direction"], "dimensionless"),
                axis,
                atol=1e-12,
                rtol=0,
            )
            outcome = cell["outcomes"][name][index]
            assert outcome["status"] == "returned"
            result = outcome["result"]
            fits = int(
                np.linalg.norm(point - target) <= 0.02
                and np.dot(axis, -directions[index]) >= np.cos(np.deg2rad(1))
            )
            assert result["fit_value"] == fits == control["expected_fits"][index]
            assert result["status"] == ("matched" if fits else "not_matched")
            assert result["missing_essential_sites"] == ([] if fits else [0])
            assert result["excluded_volume_clashes"] == []
            assert result["structure_index"] == 0 and result[
                "selected_atom_indices"
            ] == [0, 1]
            assert len(result["assignments"]) == fits
            if fits:
                assert result["assignments"][0]["site_index"] == 0
                assert result["assignments"][0]["atom_indices"] == [1, 0]


def test_unsupported_undefined_and_full_source_candidate_cache_custody(measured):
    assert measured["application_policy_restored"]
    assert measured["source_before"] == measured["source_after"]
    np.testing.assert_array_equal(
        measured["source_before"]["coordinates_nm"],
        PLAN["source"]["coordinates"]["values"],
    )
    for context in measured["policies"]:
        assert context["provider"] == context["provider_after"]
        assert len(context["negative_queries"]) == 2
        for declared, record in zip(
            PLAN["negative_sources"], context["negative_queries"], strict=True
        ):
            assert record["source_before"] == record["source_after"]
            assert (
                record["admitted_records"] == []
                and record["models"] == []
                and record["score"] is None
            )
            payload = record["provider"]["payload"]
            for key in ["site_roles", "site_models", "status"]:
                assert payload[key] == declared[key]
            sites = payload["direction_site_indices"]
            assert sum(payload["site_roles"][i] == 1 for i in sites) == 0
            assert (
                sum(payload["site_roles"][i] == 0 for i in sites)
                == declared["donor_direction_records"]
            )
    for cell in measured["cells"]:
        assert cell["inventory_before"] == cell["inventory_after"]
        assert cell["candidates_before"] == cell["candidates_after"]


def test_every_native_roundtrip_keeps_geometry_provenance_and_results(measured):
    for cell in measured["cells"]:
        assert len(cell["recovery"]) == 4
        for record in cell["recovery"]:
            assert record["native_equivalent"]
            original = cell["outcomes"][record["candidate"]][record["model_index"]][
                "result"
            ]
            recovered = record["result"]
            for key in [
                "fit_value",
                "status",
                "missing_essential_sites",
                "excluded_volume_clashes",
                "structure_index",
                "selected_atom_indices",
            ]:
                assert original[key] == recovered[key]
            for first, second in zip(
                original["assignments"], recovered["assignments"], strict=True
            ):
                assert {k: v for k, v in first.items() if k != "distance"} == {
                    k: v for k, v in second.items() if k != "distance"
                }
                assert (
                    abs(
                        float(quantity(first["distance"], "nm"))
                        - float(quantity(second["distance"], "nm"))
                    )
                    <= 1e-12
                )


@pytest.mark.parametrize(
    "field",
    [
        "schema",
        "method",
        "state",
        "selection",
        "producer",
        "role",
        "model",
        "status",
        "codes",
        "positions",
        "multiplicity",
        "zero_vector",
        "direction_unit",
        "origin_unit",
        "images",
    ],
)
def test_malformed_cached_provider_output_is_refused_without_repair(measured, field):
    payload = native_payload(measured)
    assert receive(payload) == list(range(6))
    if field == "schema":
        payload["schema"] = "unknown@2"
    elif field == "method":
        payload["method"] = "first_neighbor"
    elif field == "state":
        payload["chemical_state_index"] = 1
    elif field == "selection":
        payload["selected_atom_indices"] = np.array([1])
    elif field == "producer":
        payload["software"]["molsysmt"] = "wrong producer"
    elif field == "role":
        payload["site_roles"][0] = 0
    elif field == "model":
        payload["site_models"][0] = 9
    elif field == "status":
        payload["status"][0, 0] = 0
    elif field == "codes":
        payload["codes"]["status"]["2"] = "unsupported"
    elif field == "positions":
        payload["direction_structure_positions"][4:] = 0
    elif field == "multiplicity":
        payload["direction_indices"][1] = 0
    elif field == "zero_vector":
        payload["directions"][0] = 0
    elif field == "direction_unit":
        payload["units"]["directions"] = "nm"
    elif field == "origin_unit":
        payload["origins"] = puw.quantity(np.zeros((6, 3)), "ps")
    elif field == "images":
        payload["image_vectors"][0, 0] = 1
    with pytest.raises(Exception):
        receive(payload)


def test_operational_provider_error_keeps_its_identity_and_has_no_fallback(monkeypatch):
    error = RuntimeError("controlled provider operation failure")
    calls = []

    def unavailable(source, **kwargs):
        calls.append(kwargs)
        raise error

    monkeypatch.setattr(
        driver.msm.interactions.hbonds, "get_hbond_site_directions", unavailable
    )
    with pytest.raises(RuntimeError) as caught:
        driver._directions(None, PLAN["source"], PLAN)
    assert caught.value is error and len(calls) == 1
    assert calls[0]["method"] == "ideal_local_geometry" and calls[0]["pbc"] is False


@pytest.mark.parametrize("failed", [False, True])
def test_optional_attribution_absence_or_failure_preserves_the_fixed_subset(
    tmp_path, monkeypatch, failed
):
    def backend():
        if failed:
            raise RuntimeError("controlled optional tracking failure")
        return None

    monkeypatch.setattr(_ackredit, "backend", backend)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("error")
        result = driver.run_study(tmp_path, cell_ids=["carbonyl-nm-position0"])
    (tmp_path / "optional_results.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n"
    )
    assert (
        result["execution_status"] == "completed"
        and result["attribution"]["status"] != "captured"
    )
    assert result["actual_counts"]["returned_models"] == 2
    assert result["actual_counts"]["primary_evaluations"] == 12
    assert result["actual_counts"]["recovery_evaluations"] == 4
    for control in PLAN["controls"]:
        assert [
            o["result"]["fit_value"]
            for o in result["cells"][0]["outcomes"][control["id"]]
        ] == control["expected_fits"]
