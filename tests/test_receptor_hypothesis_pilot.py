"""Independent raw-coordinate oracles for the fixed receptor hypothesis pilot."""

import hashlib
import json
from copy import deepcopy

import ackredit
import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import Pharmacophore, attribution
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import get_features
from pharmacophoremt.screening import evaluate_feature_correspondence
from phmt_test_support.prepared_receptor_workflow import load_input
from phmt_test_support.receptor_hypothesis_pilot import PLAN, generate, run_case
from phmt_test_support.saved_model_reader import native_record


def original_geometry(plan, output):
    # Independent test-only arithmetic over frozen original coordinates.
    coordinates = np.asarray(output["inputs_before"]["coordinates_nm"])[0]
    donor, hydrogen = coordinates[plan["donor_atoms"]]
    direction = hydrogen - donor
    direction /= np.linalg.norm(direction)
    ring = coordinates[plan["ring_atoms"]]
    center = ring.mean(axis=0)
    normal = np.linalg.svd(ring - center)[2][-1]
    return donor, direction, center, normal


def cloud(acceptor, center, normal, *, wrong_kind=False):
    return dict(
        definition="classical_atomic_formal@1",
        structure_index=0,
        chemical_state="reference",
        selected_atom_indices=list(range(7)),
        recognition={"origin": "analytical feature cloud, no molecular system"},
        features=[
            dict(
                kind="positive charge" if wrong_kind else "hb acceptor",
                atom_indices=[0],
                center=puw.quantity(acceptor, "nm"),
                direction=None,
                normal=None,
                charge=puw.quantity(1, "e") if wrong_kind else None,
            ),
            dict(
                kind="aromatic ring",
                atom_indices=list(range(1, 7)),
                center=puw.quantity(center, "nm"),
                direction=None,
                normal=puw.quantity(normal, "dimensionless"),
                charge=None,
            ),
        ],
    )


def pair_checks(plan, output):
    donor, direction, center, normal = original_geometry(plan, output)
    acceptor = donor + plan["oracle_donor_distance_nm"] * direction
    orthogonal = np.cross(normal, np.eye(3)[np.argmin(np.abs(normal))])
    orthogonal /= np.linalg.norm(orthogonal)
    checks = []
    for sign in [1, -1]:
        target = center + sign * plan["oracle_ring_distance_nm"] * normal
        for row in output["runs"][0]["hypotheses"]:
            first, second = row["model"]["interaction_sites"]
            reference = cloud(
                first["shape"]["center"],
                second["shape"]["center"],
                second["shape"]["normal"],
            )
            for label, axis, wrong_kind in [
                ("positive", normal, False),
                ("axis_reversed", -normal, False),
                ("orthogonal", orthogonal, False),
                ("wrong_kind", normal, True),
            ]:
                result = evaluate_feature_correspondence(
                    reference,
                    cloud(acceptor, target, axis, wrong_kind=wrong_kind),
                    [[0, 0], [1, 1]],
                    distance_tolerance=puw.quantity(
                        plan["pair_distance_tolerance_nm"], "nm"
                    ),
                    direction_tolerance=puw.quantity(
                        plan["pair_direction_tolerance_degrees"], "degrees"
                    ),
                )
                checks.append(
                    dict(
                        face=sign,
                        hypothesis_id=row["hypothesis_id"],
                        control=label,
                        result=result,
                    )
                )
    return checks


@pytest.fixture(scope="module")
def measured(tmp_path_factory):
    directory = tmp_path_factory.mktemp("receptor-hypothesis-pilot")
    plan = json.loads(PLAN.read_text())
    outputs, controls = [], []
    for index, policy in enumerate(plan["policies"]):
        output = run_case(policy, directory / str(index))
        with (
            attribution(),
            ackredit.capture("independent feature-pair controls") as cap,
        ):
            checks = pair_checks(plan, output)
        holder = Pharmacophore()
        holder.metadata = dict(checks=checks)
        output["independent_pair_checks"] = native_record(
            holder, directory, f"pair-checks-{index}"
        )
        output["independent_pair_attribution"] = cap.attribution.to_dict()
        outputs.append(output)
        controls.append(checks)
    (directory / "full_results.json").write_text(
        json.dumps(outputs, indent=2, allow_nan=False) + "\n"
    )
    return plan, outputs, controls, directory


@pytest.mark.parametrize("policy", [0, 1])
@pytest.mark.parametrize("index", range(8))
def test_every_separate_hypothesis_matches_raw_coordinate_oracle(
    measured, policy, index
):
    plan, outputs, _, _ = measured
    output = outputs[policy]
    donor, direction, center, normal = original_geometry(plan, output)
    row = output["runs"][0]["hypotheses"][index]
    first, second = row["model"]["interaction_sites"]
    choices = row["choices"]
    assert first["features"] == ["hb acceptor"]
    assert second["features"] == ["aromatic ring"]
    np.testing.assert_allclose(
        first["shape"]["center"],
        donor + choices["donor_distance_nm"] * direction,
        atol=1e-12,
        rtol=0,
    )
    # Plane sign is arbitrary; the two face centers must span the oracle axis.
    displacement = np.asarray(second["shape"]["center"]) - center
    assert abs(np.dot(displacement, normal)) == pytest.approx(
        choices["ring_distance_nm"], abs=1e-12
    )
    np.testing.assert_allclose(
        np.cross(displacement, normal), [0, 0, 0], atol=1e-12, rtol=0
    )
    assert abs(np.dot(second["shape"]["normal"], normal)) == pytest.approx(1, abs=1e-12)
    for site, atoms in [(first, plan["donor_atoms"]), (second, plan["ring_atoms"])]:
        assert site["metadata"]["atom_indices"] == atoms
        assert site["shape"]["radius"] == plan["radius_nm"]
        assert site["essential"] and site["weight"] == 1


@pytest.mark.parametrize("policy", [0, 1])
@pytest.mark.parametrize("budget_index", [0, 1, 2])
def test_exhaustion_is_separate_from_budget_limited_empty_output(
    measured, policy, budget_index
):
    report = measured[1][policy]["runs"][budget_index]
    budget = measured[0]["budgets"][budget_index]
    assert report["status"] == "enumerated"
    assert report["total_possible"] == 8
    assert report["visited"] == report["returned"] == budget
    assert report["remaining"] == 8 - budget
    assert report["complete"] is (budget == 8)
    ids = [row["hypothesis_id"] for row in report["hypotheses"]]
    assert (
        ids
        == [f"d{d}-r{r}-f{f}" for d in [0, 1] for r in [0, 1] for f in [0, 1]][:budget]
    )
    assert report["omitted"] == [
        dict(
            feature_index=1,
            atom_indices=[794],
            kind="hb acceptor",
            reason="ideal_acceptor_profile_not_adopted",
        )
    ]


@pytest.mark.parametrize("policy", [0, 1])
@pytest.mark.parametrize("face", [1, -1])
def test_independent_pair_controls_preserve_alternatives_and_axis_semantics(
    measured, policy, face
):
    checks = [row for row in measured[2][policy] if row["face"] == face]
    valid = {}
    for label in ["positive", "axis_reversed", "orthogonal", "wrong_kind"]:
        selected = [row for row in checks if row["control"] == label]
        assert len(selected) == 8
        assert all(row["result"]["complete"] for row in selected)
        valid[label] = {
            row["hypothesis_id"] for row in selected if row["result"]["all_pairs_valid"]
        }
    assert len(valid["positive"]) == 1
    assert valid["positive"] == valid["axis_reversed"]
    assert not valid["orthogonal"] and not valid["wrong_kind"]
    assert valid["positive"] <= {"d1-r0-f0", "d1-r0-f1"}


@pytest.mark.parametrize("policy", [0, 1])
def test_native_custody_persistence_real_failure_and_actual_credit(measured, policy):
    plan, outputs, _, _ = measured
    output = outputs[policy]
    assert output["plan_sha256"] == hashlib.sha256(PLAN.read_bytes()).hexdigest()
    assert (
        output["input_identity"]["native_evidence"]["uncompressed_sha256"]
        == (plan["native_sha256"])
    )
    assert output["inputs_before"] == output["inputs_after"]
    assert output["inventories_before"] == output["inventories_after"]
    assert output["selection"] == [*range(791, 802), *range(2772, 2781)]
    assert "NaN" in output["inputs_before"]["chemical_state_json"]
    assert len(output["persistence"]) == 8
    assert all(row["json"] and row["yaml"] for row in output["persistence"])
    assert output["application_policy_restored"] and not output["holdout_access"]
    failure = output["failed_inventory"]
    assert failure["status"] == "failed" and failure["stage"] == "inventory"
    assert failure["structure_index"] == 1 and failure["traceback"]
    assert "fit_value" not in failure and "hypotheses" not in failure
    actual = json.dumps(output["workflow_attribution"])
    assert "pharmacophoremt:dataset:prepared-eralpha:" + plan["native_sha256"] in actual
    assert "from_receptor_projections" in actual and "software:molsysmt:" in actual
    route = output["inventories_before"]["metadata"]["inventory"]["recognition"][
        "hydrogen_bond_route"
    ]
    assert route["donor_geometry"] == "molsysmt.structure.get_vectors"


def test_physical_hypotheses_and_pair_answers_agree_across_unit_policies(measured):
    first, second = measured[1]
    for a, b in zip(
        first["runs"][0]["hypotheses"], second["runs"][0]["hypotheses"], strict=True
    ):
        assert a["hypothesis_id"] == b["hypothesis_id"]
        for x, y in zip(
            a["model"]["interaction_sites"],
            b["model"]["interaction_sites"],
            strict=True,
        ):
            np.testing.assert_allclose(
                x["shape"]["center"], y["shape"]["center"], atol=1e-12, rtol=0
            )
    assert [row["result"]["all_pairs_valid"] for row in measured[2][0]] == [
        row["result"]["all_pairs_valid"] for row in measured[2][1]
    ]


@pytest.fixture(scope="module")
def native_inventory(measured):
    # Serialized metadata retain QuantityRecords, not a hydrated native cache.
    # Obtain the native inventory once through its actual public producer.
    directory = measured[3] / "native-cache-replay"
    directory.mkdir()
    source, _ = load_input(directory)
    return get_features(
        source,
        selection=msm.select(source, selection=measured[0]["selection"]),
        features=measured[0]["features"],
    )


def test_cached_generation_has_no_molecular_access_and_results_are_independent(
    measured, native_inventory, monkeypatch
):
    inventory = deepcopy(native_inventory)
    original = deepcopy(inventory["features"])

    def forbidden(*args, **kwargs):
        pytest.fail("cached hypothesis generation must not inspect molecular systems")

    for name in ["get", "select", "convert", "copy", "extract", "set"]:
        monkeypatch.setattr(msm, name, forbidden)
    monkeypatch.setattr(msm.structure, "get_vectors", forbidden)
    monkeypatch.setattr(msm.structure, "get_least_squares_plane", forbidden)
    monkeypatch.setattr(msm.interactions.hbonds, "get_hbond_sites", forbidden)
    report = generate(inventory, measured[0], 8)
    first, second = report["hypotheses"][:2]
    first["model"].metadata["source_inventory"]["features"][0]["atom_indices"].append(
        999
    )
    first["model"].metadata["generation"]["omitted"][0]["atom_indices"].append(998)
    assert inventory["features"][0]["atom_indices"] == original[0]["atom_indices"]
    assert (
        second["model"].metadata["source_inventory"]["features"][0]["atom_indices"]
        == original[0]["atom_indices"]
    )
    assert second["model"].metadata["generation"]["omitted"][0]["atom_indices"] == [794]
    assert report["omitted"][0]["atom_indices"] == [794]


@pytest.mark.parametrize("field,index", [("direction", 0), ("normal", 2)])
def test_missing_required_cached_geometry_is_a_failure_not_an_invented_axis(
    measured, native_inventory, field, index
):
    inventory = deepcopy(native_inventory)
    inventory["features"][index][field] = None
    with pytest.raises(ValueError, match="missing cached"):
        generate(inventory, measured[0], 8)


@pytest.mark.parametrize("empty", [False, True])
def test_missing_profile_family_is_not_applicable_not_inactivity(
    measured, native_inventory, empty
):
    inventory = deepcopy(native_inventory)
    inventory["features"] = [] if empty else inventory["features"][:2]
    report = generate(inventory, measured[0], 8)
    assert report["status"] == "not_applicable" and report["complete"]
    assert report["returned"] == report["total_possible"] == 0
    assert "aromatic ring" in report["missing_families"]
    assert "fit_value" not in report
