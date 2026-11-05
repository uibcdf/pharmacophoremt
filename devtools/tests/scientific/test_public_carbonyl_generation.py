"""Public generator replay on the unchanged #93 analytical source/control matrix."""

import json
import os
import subprocess
import sys

import numpy as np
import pytest

from devtools.tests.scientific.test_carbonyl_acceptor_receiving import (
    carbonyl_oracle,
    quantity,
)
from phmt_test_support.carbonyl_acceptor_receiving import load_plan

PLAN = load_plan()


@pytest.fixture(scope="module")
def measured(tmp_path_factory):
    work = tmp_path_factory.mktemp("public-carbonyl-cli")
    path = work / "full_results.json"
    command = [
        sys.executable,
        "-B",
        "-m",
        "phmt_test_support.public_carbonyl_generation",
        "--output",
        str(path),
    ]
    (work / "command.json").write_text(json.dumps(command, indent=2) + "\n")
    with (work / "cli.log").open("w") as log:
        r = subprocess.run(
            command, env=os.environ.copy(), stdout=log, stderr=subprocess.STDOUT
        )
    assert path.is_file(), (work / "cli.log").read_text()
    data = json.loads(path.read_text())
    data["_cli_exit_code"] = r.returncode
    return data


def test_full_public_workload_and_actual_credit(measured):
    assert (
        measured["_cli_exit_code"] == 0 and measured["execution_status"] == "completed"
    )
    assert measured["actual_counts"] == dict(
        source_position_policy_blocks=6,
        returned_models=12,
        primary_evaluations=72,
        recovery_evaluations=24,
        negative_queries=4,
        negative_pose_evaluations=0,
    )
    assert measured["attribution"]["status"] == "captured"
    assert "from_receptor_features" in json.dumps(measured["attribution"])


@pytest.mark.parametrize(
    "declared", PLAN["matrix"], ids=[r["id"] for r in PLAN["matrix"]]
)
def test_public_geometry_matches_independent_original_oracles(measured, declared):
    cell = next(c for c in measured["cells"] if c["cell_id"] == declared["id"])
    assert (
        cell["status"] == "returned" and cell["complete"] and len(cell["models"]) == 2
    )
    assert cell["generation_report"]["enumeration"]["total_possible"] == 2
    origin, axes = carbonyl_oracle(declared["source_structure_index"])
    for index, row in enumerate(cell["models"]):
        sites = row["native"]["interaction_sites"]
        assert len(sites) == 1
        site = sites[0]
        assert (
            site["features"] == ["hb donor"]
            and site["essential"]
            and site["weight"] == 1
        )
        np.testing.assert_allclose(
            site["shape"]["center"], origin + 0.35 * axes[index], atol=1e-12, rtol=0
        )
        np.testing.assert_allclose(
            site["shape"]["direction"], -axes[index], atol=1e-12, rtol=0
        )
        context = site["metadata"]["projection"]["evidence"]["provider_geometry"][
            "context"
        ]
        assert context["source_structure_position"] == declared["structure_position"]
        assert context["support_atom_indices"] == [2, 1, 0]
        assert site["metadata"]["atom_indices"] == [2]
        for control in PLAN["controls"]:
            name = control["id"]
            point = (
                origin
                + 0.35 * axes[control["source_lobe"]]
                + control["displacement"]["values"]
            )
            axis = control["donor_axis_sign"] * axes[control["source_lobe"]]
            np.testing.assert_allclose(
                cell["candidates_before"][name]["coordinates_nm"],
                [[point + 0.1 * axis, point]],
                atol=1e-12,
                rtol=0,
            )
            value = cell["outcomes"][name][index]
            assert value["status"] == "returned"
            result = value["result"]
            assert result["fit_value"] == control["expected_fits"][index]
            assert result["status"] == (
                "matched" if control["expected_fits"][index] else "not_matched"
            )
            assert result["missing_essential_sites"] == (
                [] if control["expected_fits"][index] else [0]
            )
            if result["fit_value"]:
                assert result["assignments"][0]["atom_indices"] == [1, 0]


def test_public_empty_omissions_custody_and_every_roundtrip(measured):
    assert (
        measured["source_before"] == measured["source_after"]
        and measured["application_policy_restored"]
    )
    for policy in measured["policies"]:
        assert policy["provider"] == policy["provider_after"]
        for negative, reason in zip(
            policy["negative_queries"],
            ["unsupported_acceptor_geometry", "undefined_acceptor_geometry"],
            strict=True,
        ):
            assert (
                "failure" not in negative
                and negative["returned_models"] == 0
                and negative["score"] is None
            )
            assert negative["report"]["status"] == "no_supported_features"
            assert negative["report"]["omitted"][0]["reason"] == reason
            assert negative["source_before"] == negative["source_after"]
    for cell in measured["cells"]:
        assert (
            cell["inventory_before"] == cell["inventory_after"]
            and cell["candidates_before"] == cell["candidates_after"]
        )
        assert len(cell["recovery"]) == 4
        for record in cell["recovery"]:
            assert record["native_equivalent"]
            original = cell["outcomes"][record["candidate"]][record["model_index"]][
                "result"
            ]
            restored = record["result"]
            for key in [
                "status",
                "fit_value",
                "missing_essential_sites",
                "excluded_volume_clashes",
                "structure_index",
                "selected_atom_indices",
            ]:
                assert original[key] == restored[key]
            for first, second in zip(
                original["assignments"], restored["assignments"], strict=True
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
