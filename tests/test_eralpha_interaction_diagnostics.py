"""Independent real-input geometry guards for the bounded diagnostic recipe."""

import json

import molsysmt as msm
import numpy as np
import pytest

from devtools.diagnose_eralpha_interface import DIAGNOSTICS, diagnose, valid
from devtools.prepare_eralpha_interface import prepare_interface
from pharmacophoremt import pyunitwizard as puw


@pytest.fixture(scope="module")
def diagnostic():
    case = prepare_interface()
    return case, diagnose(case)


def test_recognition_and_empty_observations_are_distinct(diagnostic):
    case, run = diagnostic
    assert valid(run)
    assert run["original_input_and_cached_analyses_unchanged"]
    assert {key: value.n_interactions for key, value in case["analyses"].items()} == {
        "hydrophobic": 12,
        "hbonds": 0,
        "pi_pi": 0,
    }
    sites = run["hbond_sites"]
    assert [4006, 4025] in sites["donor_hydrogen_pairs"]
    assert [4021, 4043] in sites["donor_hydrogen_pairs"]
    assert {4006, 4021, 378, 379, 1754} <= set(sites["acceptor_atom_indices"])
    assert len(run["hbond_candidates"]) == 8
    assert all(
        row["kind"] == "recognized_geometric_candidate_not_observation"
        for row in run["hbond_candidates"]
    )
    assert (
        run["biological_validation"]
        == run["environmental_refinement"]
        == "not_performed"
    )


def test_candidate_distances_and_angles_have_independent_coordinate_oracles(diagnostic):
    case, run = diagnostic
    xyz = puw.get_value(
        msm.get(case["molecular_system"], coordinates=True), to_unit="nm"
    )[0]
    frozen = json.loads(DIAGNOSTICS.read_text())["expected_near_hbond_triplets"]
    for row, (d, h, a) in zip(run["hbond_candidates"], frozen, strict=True):
        assert [
            row[key]["prepared_index"] for key in ("donor", "hydrogen", "acceptor")
        ] == [d, h, a]
        assert row["hydrogen"]["source_index"] == -1
        assert (
            row["donor"]["source_index"] >= 0 and row["acceptor"]["source_index"] >= 0
        )
        distance = np.linalg.norm(xyz[d] - xyz[a])
        u, v = xyz[d] - xyz[h], xyz[a] - xyz[h]
        angle = np.degrees(
            np.arccos(
                np.clip(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)), -1, 1)
            )
        )
        assert row["donor_acceptor_distance"]["unit"] == "nm"
        assert row["donor_hydrogen_acceptor_angle"]["unit"] == "degrees"
        assert row["donor_acceptor_distance"]["value"] == pytest.approx(
            distance, abs=1e-12
        )
        assert row["donor_hydrogen_acceptor_angle"]["value"] == pytest.approx(
            angle, abs=1e-10
        )
    indexed = {
        (row["donor"]["prepared_index"], row["acceptor"]["prepared_index"]): row
        for row in run["hbond_candidates"]
    }
    for pair, expected_angle in [
        ((4006, 379), 51.55929633111298),
        ((4021, 1754), 30.379399929981165),
        ((721, 4006), 83.50688755231846),
    ]:
        row = indexed[pair]
        assert row["passes_declared_distance"] and not row["passes_declared_angle"]
        assert row["donor_hydrogen_acceptor_angle"]["value"] == pytest.approx(
            expected_angle
        )


def test_fixed_cutoff_sensitivity_does_not_reclassify_original_analyses(diagnostic):
    case, run = diagnostic
    assert [
        (row["name"], row["n_interactions"]) for row in run["hbond_comparisons"]
    ] == [
        ("declared", 0),
        ("distance_only_control", 6),
        ("loose_angle_control", 2),
        ("120_degree_control", 0),
        ("extended_distance_control", 1),
    ]
    for comparison in run["hbond_comparisons"]:
        payload = comparison["analysis"]
        assert payload["evaluated_structure_indices"] == [0]
        assert payload["parameters"]["profile"] == "smarts_donor_acceptor"
        distance_limit = payload["parameters"]["distance_threshold"]["value"]
        angle_limit = np.degrees(payload["parameters"]["angle_threshold"]["value"])
        independently_accepted = sum(
            row["donor_acceptor_distance"]["value"] <= distance_limit
            and row["donor_hydrogen_acceptor_angle"]["value"] >= angle_limit
            for row in run["hbond_candidates"]
        )
        assert comparison["n_interactions"] == independently_accepted
    extended = run["hbond_comparisons"][-1]["analysis"]
    assert extended["participant_atoms"] == [4006, 4025, 657]
    assert case["analyses"]["hbonds"].n_interactions == 0


def test_phe404_is_recognized_and_profile_comparison_retains_its_definition(diagnostic):
    case, run = diagnostic
    assert run["n_smarts_rings"] == 29
    assert len(run["ring_pairs"]) == 28
    nearest, next_nearest = run["ring_pairs"][:2]
    assert nearest["receptor_members"][0]["group_name"] == "PHE"
    assert nearest["receptor_members"][0]["group_id"] == "404"
    assert (
        sorted(row["source_index"] for row in nearest["receptor_members"])
        == run["declaration"]["expected_source_ring_memberships"]["PHE404"]
    )
    assert (
        sorted(row["source_index"] for row in nearest["ligand_members"])
        == run["declaration"]["expected_source_ring_memberships"]["EST"]
    )
    assert nearest["centroid_distance"]["value"] == pytest.approx(
        0.4999674389397774, abs=1e-12
    )
    assert next_nearest["centroid_distance"]["value"] > 0.65
    assert [(row["name"], row["n_interactions"]) for row in run["pi_comparisons"]] == [
        ("declared", 0),
        ("aromatic_cycle_control", 0),
        ("least_squares_control", 1),
    ]
    custom = run["pi_comparisons"][-1]["analysis"]
    assert custom["parameters"]["profile"] == "least_squares"
    assert custom["parameters"]["plane_method"] == "unweighted_orthogonal_least_squares"
    assert custom["measure_units"]["plane_angle"] == "radians"
    assert np.degrees(custom["measurements"]["plane_angle"][0]) == pytest.approx(
        69.6408780519349
    )
    # Independent plane fit and projection on the observed ligand coordinates.
    xyz = puw.get_value(
        msm.get(case["molecular_system"], coordinates=True), to_unit="nm"
    )[0]
    receptor_xyz = xyz[[row["prepared_index"] for row in nearest["receptor_members"]]]
    ligand_xyz = xyz[[row["prepared_index"] for row in nearest["ligand_members"]]]
    delta = ligand_xyz.mean(axis=0) - receptor_xyz.mean(axis=0)
    normal = np.linalg.svd(ligand_xyz - ligand_xyz.mean(axis=0))[2][-1]
    offset = np.linalg.norm(delta - np.dot(delta, normal) * normal)
    assert custom["measurements"]["offset_b"][0] == pytest.approx(offset, abs=1e-12)
    assert case["analyses"]["pi_pi"].n_interactions == 0


def test_reference_intersection_rejects_frozen_phe404_pair(diagnostic):
    """Independent fixed-case oracle; no consumer production geometry engine.

    Use the reviewed ordered SMARTS participants, not least-squares planes.
    Project via the second normal's in-plane component; the provider uses a
    three-equation solve. This independently checks the asymmetric reference
    ring-A projection and the geometric gate behind the evaluated-empty result.
    """
    case, run = diagnostic
    xyz = puw.get_value(
        msm.get(case["molecular_system"], coordinates=True), to_unit="nm"
    )[0]
    order = run["declaration"]["reference_ring_order"]
    memberships = {
        tuple(row)
        for matrix in run["aromatic_recognition"]["matches"]
        for row in matrix
    }
    assert tuple(order["PHE404"]) in memberships and tuple(order["EST"]) in memberships
    a, b = xyz[order["PHE404"]], xyz[order["EST"]]
    ca, cb = a.mean(axis=0), b.mean(axis=0)
    na, nb = np.cross(a[0] - ca, a[1] - ca), np.cross(b[0] - cb, b[1] - cb)
    na, nb = na / np.linalg.norm(na), nb / np.linalg.norm(nb)
    delta, distance = cb - ca, np.linalg.norm(cb - ca)
    plane_angle = np.degrees(np.arccos(abs(np.dot(na, nb))))
    normal_angles = np.degrees(
        np.arccos([abs(np.dot(n, delta)) / distance for n in (na, nb)])
    )
    assert distance < 0.65 and 50 < plane_angle < 90 and min(normal_angles) < 30
    assert plane_angle == pytest.approx(69.78276676849039)
    projected_normal = nb - np.dot(nb, na) * na
    point = (
        ca
        + np.dot(delta, nb)
        / np.dot(projected_normal, projected_normal)
        * projected_normal
    )
    assert np.dot(point - ca, na) == pytest.approx(0, abs=1e-12)
    assert np.dot(point - cb, nb) == pytest.approx(0, abs=1e-12)
    intersection_distance = min(np.linalg.norm(point - ca), np.linalg.norm(point - cb))
    assert intersection_distance == pytest.approx(0.2643939338459814, abs=1e-12)
    threshold = run["pi_comparisons"][0]["analysis"]["parameters"][
        "intersection_radius"
    ]
    assert threshold == {"value": 0.15, "unit": "nm"}
    assert intersection_distance > threshold["value"]
    assert (
        run["unavailable_rejected_reference_geometry"]["provider_issue"]
        == "uibcdf/molsysmt#350"
    )


def test_nondefault_unit_policy_preserves_diagnosis_and_explicit_records(diagnostic):
    case, reference = diagnostic
    with puw.context(
        standard_units=["pm", "fs", "coulomb", "radians", "dimensionless"]
    ):
        altered = diagnose(case)
    assert valid(altered)
    assert altered["n_smarts_rings"] == reference["n_smarts_rings"]
    for actual, expected in zip(
        altered["hbond_candidates"], reference["hbond_candidates"], strict=True
    ):
        for key in (
            "donor",
            "hydrogen",
            "acceptor",
            "passes_declared_distance",
            "passes_declared_angle",
            "kind",
        ):
            assert actual[key] == expected[key]
        for key, tolerance in (
            ("donor_acceptor_distance", 1e-12),
            ("donor_hydrogen_acceptor_angle", 1e-10),
        ):
            assert actual[key]["unit"] == expected[key]["unit"]
            assert actual[key]["value"] == pytest.approx(
                expected[key]["value"], abs=tolerance
            )
    for actual, expected in zip(
        altered["ring_pairs"], reference["ring_pairs"], strict=True
    ):
        assert actual["receptor_members"] == expected["receptor_members"]
        assert actual["ligand_members"] == expected["ligand_members"]
        assert (
            actual["centroid_distance"]["unit"]
            == expected["centroid_distance"]["unit"]
            == "nm"
        )
        assert actual["centroid_distance"]["value"] == pytest.approx(
            expected["centroid_distance"]["value"], abs=1e-12
        )
    for key in ("hbond_comparisons", "pi_comparisons"):
        assert [row["n_interactions"] for row in altered[key]] == [
            row["n_interactions"] for row in reference[key]
        ]
    original = puw.QuantityRecord.from_dict(
        reference["diagnostic_planes"]["centers"]
    ).to_quantity()
    shifted = puw.QuantityRecord.from_dict(
        altered["diagnostic_planes"]["centers"]
    ).to_quantity()
    np.testing.assert_allclose(
        puw.get_value(original, to_unit="nm"),
        puw.get_value(shifted, to_unit="nm"),
        atol=1e-12,
        rtol=0,
    )
