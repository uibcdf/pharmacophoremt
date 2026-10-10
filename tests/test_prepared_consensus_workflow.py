"""Distinct-source support and independent frozen-geometry consensus controls."""

import numpy as np
import pytest

from devtools.prepared_consensus_workflow import ATOMS, expectations_passed, run_case
from devtools.prepared_workflow import models_equivalent
from devtools.validate_prepared_ccd_ligands import scientific_projection
from pharmacophoremt import pyunitwizard as puw


@pytest.fixture(scope="module")
def workflow(tmp_path_factory):
    return run_case(tmp_path_factory.mktemp("prepared-consensus"), fresh_reader=True)


def values(record, unit="nm"):
    return puw.get_value(
        puw.QuantityRecord.from_dict(record).to_quantity(), to_unit=unit
    )


def test_inputs_are_two_distinct_ctabs_with_one_declared_frame_each(workflow):
    before = workflow["inputs_before"]
    assert before == workflow["inputs_after"]
    est = np.array(before["EST"]["coordinates_nm"])
    des = np.array(before["DES"]["coordinates_nm"])
    assert est.shape == (1, 44, 3) and des.shape == (2, 40, 3)
    np.testing.assert_allclose(est[0, 3], [0.0249, 0.0518, -0.5772], rtol=0, atol=1e-12)
    np.testing.assert_allclose(
        des[1],
        des[0] @ np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]).T + [2, 1, 3],
        rtol=0,
        atol=1e-12,
    )
    sources = workflow["report"]["sources"]
    assert [s["ligand_id"] for s in sources] == ["EST", "DES"]
    assert [s["structure_index"] for s in sources] == [0, 1]
    for source, n in zip(sources, [44, 40]):
        assert source["selected_atom_indices"] == list(range(n))
        assert source["chemical_state"] == "reference"
        assert [f["atom_indices"] for f in source["features"]] == ATOMS[
            source["ligand_id"]
        ]
        assert all(f["direction"] is None for f in source["features"])
        coords = np.array(before[source["ligand_id"]]["coordinates_nm"])[
            source["structure_index"]
        ]
        for f in source["features"]:
            np.testing.assert_allclose(
                values(f["center"]),
                coords[f["atom_indices"]].mean(axis=0),
                rtol=0,
                atol=1e-12,
            )
    assert "distinct" in workflow["repeated_raw_rejection"]["message"]


def test_joint_support_is_set_intersection_of_disjoint_original_occurrences(workflow):
    meta = workflow["model"]["metadata"]
    sites = meta["consensus"]["sites"]
    sets = [{m["ligand_id"] for m in site["members"]} for site in sites]
    assert set.intersection(*sets) == {"EST", "DES"}
    assert meta["hypothesis"]["joint_support_count"] == 2
    assert meta["hypothesis"]["joint_support_fraction"] == 1
    assert (
        meta["consensus"]["n_ligands"] == 2
    )  # Frames/proposals never enlarge denominator.
    assert len(sites) == 3
    for key in ATOMS:
        members = [m for s in sites for m in s["members"] if m["ligand_id"] == key]
        occurrences = [m["feature_index"] for m in members]
        assert occurrences == [0, 1, 2] and len(set(occurrences)) == 3
        for m in members:
            assert m["atom_indices"] == ATOMS[key][m["feature_index"]]
            assert m["geometry"]["geometry_atom_indices"] == m["atom_indices"]
            assert m["structure_index"] == (0 if key == "EST" else 1)
            assert m["chemical_state"] == "reference"
    # DES's second ring cannot create a fourth jointly supported site by reusing EST's ring.
    assert all(
        m["feature_index"] != 3
        for s in sites
        for m in s["members"]
        if m["ligand_id"] == "DES"
    )


def test_site_geometry_agrees_with_original_atoms_and_pairwise_criteria(workflow):
    meta = workflow["model"]["metadata"]
    placement = meta["placements"][1]
    fit = placement["alignment"]
    assert fit["provider"] == "molsysmt.structure.least_rmsd_fit"
    assert fit["structure_index"] == 1 and fit["selected_atom_indices"] == list(
        range(40)
    )
    coords = {
        "EST": np.array(workflow["inputs_before"]["EST"]["coordinates_nm"])[0],
        "DES": values(fit["aligned_atom_coordinates"])[0],
    }
    for emitted, site in zip(
        workflow["model"]["interaction_sites"], meta["consensus"]["sites"]
    ):
        centers = np.array(
            [
                coords[m["ligand_id"]][m["atom_indices"]].mean(axis=0)
                for m in site["members"]
            ]
        )
        np.testing.assert_allclose(
            values(site["center"]), centers.mean(axis=0), rtol=0, atol=1e-12
        )
        np.testing.assert_allclose(
            emitted["shape"]["center"], centers.mean(axis=0), rtol=0, atol=1e-12
        )
        pair_distance = np.linalg.norm(centers[0] - centers[1])
        assert pair_distance <= 0.20
        assert values(site["position_rmsd"]) == pytest.approx(
            pair_distance / 2, abs=1e-12
        )
        assert site["support_count"] == 2 and site["support_fraction"] == 1
        assert emitted["essential"] and emitted["weight"] == 1
        if site["kind"] == "aromatic ring":
            normals = []
            for m in site["members"]:
                points = coords[m["ligand_id"]][m["atom_indices"]]
                # Test-only plane oracle; production molecular geometry stays in MolSysMT.
                normal = np.linalg.svd(points - points.mean(axis=0))[2][-1]
                assert abs(
                    np.dot(normal, values(m["geometry"]["normal"], "dimensionless"))
                ) == pytest.approx(1, abs=1e-12)
                normals.append(normal)
            angle = np.degrees(np.arccos(np.clip(abs(np.dot(*normals)), -1, 1)))
            assert angle <= 30
            assert values(
                site["maximum_orientation_deviation"], "degrees"
            ) == pytest.approx(angle, abs=1e-10)
        else:
            assert site["normal"] is None and site["direction"] is None


def test_finite_layout_accounting_does_not_invent_support(workflow):
    report = workflow["report"]
    assert workflow["complete"] and report["complete"]
    assert report["n_fits"] == 2 and report["n_layouts"] == 1
    assert [a["status"] for a in report["source_alignments"]] == ["pivot", "placed"]
    assert len(report["source_alignments"][1]["accepted_placements"]) == 1
    assert workflow["model"]["metadata"]["layout"] == dict(
        layout_id="layout_00000", placement_indices=[0, 0], unplaced_ligand_ids=[]
    )
    assert report["criteria"]["n_seeds"] == 4
    assert (
        report["criteria"]["completion_scope"]
        == "declared_pivot_proposals_and_maximal_aligned_hypotheses"
    )


def test_impossible_site_count_is_complete_empty_and_failed_rebuild_clears_state(
    workflow,
):
    empty = workflow["empty"]
    assert empty["complete"] and empty["report"]["complete"]
    assert empty["models"] == [] and empty["report"]["criteria"]["min_sites"] == 4
    assert empty["report"]["criteria"]["min_support"] == 2
    assert len(empty["report"]["sources"][0]["features"]) == 3
    assert empty["report"]["n_fits"] == 2 and empty["report"]["n_layouts"] == 1
    assert all(
        layout["consensus"]["hypotheses"] == [] for layout in empty["report"]["layouts"]
    )
    failed = workflow["budget_failure"]
    assert failed["status"] == "failed" and failed["code"] == "PHMT-E107"
    assert failed["result"] is None and failed["report"] is None
    assert "scheduled fits" in failed["message"]
    success = workflow["facade_success"]
    assert success["return_is_native_list"] and success["complete"]

    def projection(value):
        return scientific_projection(
            value, attribution_keys=("attribution", "source_attribution")
        )

    assert models_equivalent(
        projection(success["models"][0]), projection(workflow["model"])
    )


@pytest.mark.parametrize("codec", ["json", "yaml", "sdf"])
def test_saved_unit_contexts_and_fresh_readers_preserve_complete_maps(workflow, codec):
    assert models_equivalent(workflow["results"][codec], workflow["model"])
    fresh = workflow["fresh_reader"]
    assert fresh["attribution"]["uses"] == []
    assert models_equivalent(fresh["models"]["consensus." + codec], workflow["model"])
    assert workflow["model"]["score"] is None
    assert expectations_passed(workflow)
