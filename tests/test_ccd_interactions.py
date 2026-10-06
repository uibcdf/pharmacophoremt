"""Native collection controls with traceable complete real chemical components."""

import json
from pathlib import Path

import ackredit as ack
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from devtools.ccd_interaction_cases import build_case, observe_case
from devtools.prepared_ccd_ligands import credit_source
from devtools.validate_aromatic_interactions import _fingerprint
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.io import load_json, to_json
from pharmacophoremt.modeler import (
    compose_pharmacophores,
    from_interaction_collection,
    get_excluded_volume_sites,
    get_features,
)
from pharmacophoremt.pharmacophore import Pharmacophore
from pharmacophoremt.screening import PoseEvaluator

MANIFEST = Path(__file__).parent / "data/ccd_interaction_cases.json"
CASES = json.loads(MANIFEST.read_text())["cases"]


@pytest.fixture(
    scope="module",
    params=CASES,
    ids=lambda case: case["case_id"] + "_" + case["placement"],
)
def prepared(request):
    expected = request.param
    case = build_case(expected["case_id"], expected["placement"])
    case["analyses"] = observe_case(case)
    case["expected"] = expected
    return case


def test_public_merge_preserves_complete_components_and_original_sources(prepared):
    report = prepared["report"]
    source_expected = report["source"]["expected"]
    assert (
        report["component_chemistry_preserved"]
        and report["component_atom_identity_preserved"]
    )
    assert (
        report["ligand_coordinates_preserved"]
        and report["partner_translation_preserved"]
    )
    assert report["prepared_source_before"] == report["prepared_source_after"]
    assert report["input_bytes_unchanged"]
    assert report["merged_counts"] == dict(
        n_atoms=2 * source_expected["n_atoms"],
        n_bonds=2 * source_expected["n_bonds"],
        n_structures=1,
    )
    assert report["element_counts"]["H"] == 2 * source_expected["n_hydrogens"]
    assert set(report["merged_formal_charges"]) == {0}
    for role in ("ligand", "partner"):
        assert report["component_counts"][role] == dict(
            n_atoms=source_expected["n_atoms"], n_bonds=source_expected["n_bonds"]
        )
        assert (
            report["component_states"][role]["states"][0]["connectivity_completeness"]
            == "complete"
        )
    json.dumps(report, allow_nan=False)


@pytest.mark.parametrize("role", ["ligand", "partner"])
def test_complete_molecule_roles_reuse_ring_evidence_and_preserve_neutral_empty_families(
    prepared, role
):
    source, analyses, expected = (
        prepared["source"],
        prepared["analyses"],
        prepared["expected"],
    )
    before = _fingerprint(source)
    assert {
        label: observed.n_interactions for label, observed in analyses.items()
    } == expected["observations"]
    query = from_interaction_collection(
        source, analyses, prepared[role], radius=".02 nm"
    )
    assert query.n_interaction_sites == expected["n_sites"]
    assert (
        sum(row["action"] == "reused" for row in query.metadata["site_map"])
        == expected["n_duplicate_rings"]
    )
    for label in ("ionic", "cation_pi"):
        component = next(
            row for row in query.metadata["components"] if row["label"] == label
        )
        assert component["n_sites"] == 0 and component["metadata"][
            "evaluated_structure_indices"
        ] == [0]
        assert component["metadata"]["parameters"]["chemical_state_index"] == 0
    for site in query.interaction_sites:
        assert all(atom in prepared[role] for atom in site.metadata["atom_indices"])
        if site.feature_name == "aromatic ring":
            assert {row["component"] for row in site.metadata["observations"]} == {
                "pi_prolif",
                "pi_molstar",
            }
    evaluator = PoseEvaluator(query)
    assert evaluator.evaluate(source, selection=prepared[role])["fit_value"] == 1
    moved = msm.structure.translate(
        source, selection=prepared[role], translation="[3,0,0] nm", in_place=False
    )
    negative = evaluator.evaluate(moved, selection=prepared[role])
    assert negative["status"] == "not_matched" and negative["fit_value"] == 0
    kept = from_interaction_collection(
        source, analyses, prepared[role], radius=".02 nm", duplicate_policy="keep"
    )
    assert (
        kept.n_interaction_sites == expected["n_sites"] + expected["n_duplicate_rings"]
    )
    result = PoseEvaluator(kept).evaluate(source, selection=prepared[role])
    assert result["status"] == "not_matched" and result["fit_value"] == pytest.approx(
        expected["n_sites"] / kept.n_interaction_sites
    )
    assert len(result["missing_essential_sites"]) == expected["n_duplicate_rings"]
    assert _fingerprint(source) == before


def test_independent_steric_hypothesis_retains_actual_veto_instead_of_changing_radius(
    prepared,
):
    source, expected = prepared["source"], prepared["expected"]
    positive = from_interaction_collection(
        source, prepared["analyses"], prepared["ligand"], radius=".02 nm"
    )
    excluded = Pharmacophore(ref_struct=0)
    inventory = get_features(
        source, selection=prepared["partner"], features=["included volume"]
    )
    spheres = get_excluded_volume_sites(inventory, radius=".05 nm")
    for site in spheres["interaction_sites"]:
        excluded.add_interaction_site(site)
    joint = compose_pharmacophores({"positive": positive, "excluded": excluded})
    result = PoseEvaluator(joint).evaluate(source, selection=prepared["ligand"])
    assert result["fit_value"] == 1
    assert len(result["excluded_volume_clashes"]) == expected["n_steric_clashes"]
    assert result["status"] == (
        "not_matched" if expected["n_steric_clashes"] else "matched"
    )
    assert (
        excluded.n_interaction_sites
        == prepared["report"]["source"]["expected"]["n_atoms"]
        - prepared["report"]["source"]["expected"]["n_hydrogens"]
    )


def test_common_frame_rigid_motion_preserves_detected_membership_and_query_geometry(
    prepared,
):
    source = prepared["source"]
    rotation = np.array([[0.0, -1, 0], [1, 0, 0], [0, 0, 1]])
    translation = np.array([2.0, 1, -3])
    moved = msm.structure.rotate(
        source, rotation=rotation, rotation_center="[0,0,0] nm", in_place=False
    )
    moved = msm.structure.translate(
        moved, translation=puw.quantity(translation, "nm"), in_place=False
    )
    moved_case = dict(prepared, source=moved)
    fresh = observe_case(moved_case)
    assert {
        label: observed.n_interactions for label, observed in fresh.items()
    } == prepared["expected"]["observations"]
    original_query = from_interaction_collection(
        source, prepared["analyses"], prepared["ligand"], radius=".02 nm"
    )
    moved_query = from_interaction_collection(
        moved, fresh, prepared["ligand"], radius=".02 nm"
    )
    assert (
        PoseEvaluator(moved_query).evaluate(moved, selection=prepared["ligand"])[
            "status"
        ]
        == "matched"
    )
    for original, transformed in zip(
        original_query.interaction_sites, moved_query.interaction_sites, strict=True
    ):
        assert original.metadata["atom_indices"] == transformed.metadata["atom_indices"]
        np.testing.assert_allclose(
            puw.get_value(transformed.center, to_unit="nm"),
            puw.get_value(original.center, to_unit="nm") @ rotation.T + translation,
            atol=1e-14,
        )


def test_json_under_nondefault_policy_preserves_real_input_and_original_detector_evidence(
    prepared, tmp_path
):
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        model = from_interaction_collection(
            prepared["source"], prepared["analyses"], prepared["ligand"], radius="20 pm"
        )
        path = tmp_path / "ccd_joint.json"
        to_json(model, path)
        restored = load_json(path)
        assert restored.metadata == model.metadata
        assert [site.metadata for site in restored.interaction_sites] == [
            site.metadata for site in model.interaction_sites
        ]
        assert (
            PoseEvaluator(restored).evaluate(
                prepared["source"], selection=prepared["ligand"]
            )["status"]
            == "matched"
        )


@pytest.mark.parametrize("case_id", ["EST", "DES"])
def test_directional_negative_rejects_a_moved_hydrogen_but_retains_acceptor_role(
    case_id,
):
    case = build_case(case_id, "donor_contact")
    analyses = observe_case(case)
    ligand = from_interaction_collection(
        case["source"], analyses, case["ligand"], radius=".02 nm"
    )
    partner = from_interaction_collection(
        case["source"], analyses, case["partner"], radius=".02 nm"
    )
    donor = next(
        site for site in ligand.interaction_sites if site.feature_name == "hb donor"
    )
    hydrogen = donor.metadata["atom_indices"][1]
    shift = -0.2 * puw.get_value(donor.direction, to_unit="dimensionless")
    candidate = msm.structure.translate(
        case["source"],
        selection=[hydrogen],
        translation=puw.quantity(shift, "nm"),
        in_place=False,
    )
    negative = PoseEvaluator(ligand).evaluate(candidate, selection=case["ligand"])
    assert negative["status"] == "not_matched" and negative[
        "fit_value"
    ] == pytest.approx((ligand.n_interaction_sites - 1) / ligand.n_interaction_sites)
    # Partner-role acceptors have no invented lone-pair direction or dependency
    # on the donor H outside the candidate selection.
    assert (
        PoseEvaluator(partner).evaluate(candidate, selection=case["partner"])["status"]
        == "matched"
    )


def test_actual_resource_and_detector_capture_reuses_data_without_crediting_a_cached_detection(
    prepared, tmp_path
):
    with ack.session("CCD interactions"):
        for _ in range(2):
            with ack.capture("complete CCD input and detection") as run:
                credit_source(prepared["expected"]["case_id"])
                with phmt.attribution():
                    fresh = observe_case(prepared)
                    result = from_interaction_collection(
                        prepared["source"], fresh, prepared["ligand"]
                    )
                    assert (
                        PoseEvaluator(result).evaluate(
                            prepared["source"], selection=prepared["ligand"]
                        )["status"]
                        == "matched"
                    )
            references = run.attribution.to_dict()
            assert any(
                item.get("doi") == "10.1093/bioinformatics/btu789"
                for item in references["items"]
            )
            assert any(
                item.get("doi") == "10.1186/s13321-021-00548-6"
                for item in references["items"]
            )
            assert any(
                "get_pi_pi_interactions" in use["used_by"] for use in references["uses"]
            )
            with ack.capture("cached conversion") as cached:
                with phmt.attribution():
                    from_interaction_collection(
                        prepared["source"], fresh, prepared["ligand"]
                    )
            assert not any(
                "get_pi_pi_interactions" in use["used_by"]
                for use in cached.attribution.to_dict()["uses"]
            )
        before = ack.get_attribution().to_dict()
        path = tmp_path / "credited.json"
        to_json(result, path)
        assert load_json(path).metadata == result.metadata
        assert ack.get_attribution().to_dict() == before
