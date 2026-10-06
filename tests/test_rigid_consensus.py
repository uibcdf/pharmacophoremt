"""Prepared rigid consensus controls, not biological or performance validation."""

import json
from itertools import permutations

import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError, CliqueLimitError
from pharmacophoremt.io.phmt import load_json, to_json
from pharmacophoremt.modeler import from_rigid_ligands, get_features
from pharmacophoremt.screening import get_rigid_feature_correspondences
from tests.test_aligned_consensus import inventory
from tests.test_pose_evaluation import system
from tests.test_rigid_search import COORDINATES, FAMILIES, SMILES, moved


def inputs(third=False):
    source = system(SMILES, COORDINATES)
    displaced = moved(source)
    ligands = [
        dict(ligand_id="a", molecular_system=source),
        dict(ligand_id="b", molecular_system=displaced),
    ]
    if third:
        ligands.append(
            dict(ligand_id="no-features", molecular_system=system("[Na+]", [[0, 0, 0]]))
        )
    return ligands


def consensus(ligands, **kwargs):
    options = dict(
        features=FAMILIES, distance_tolerance="0.02 nm", min_matches=5, min_sites=5
    )
    options.update(kwargs)
    return from_rigid_ligands(ligands, **options)


@pytest.mark.parametrize("strategy", ["association_cliques", "triplet_seeds"])
def test_rigid_motion_recovery_uses_provider_and_keeps_sources_and_support(
    strategy, monkeypatch
):
    ligands = inputs(third=True)
    before = [
        puw.get_value(
            msm.get(ligand["molecular_system"], coordinates=True), to_unit="nm"
        ).copy()
        for ligand in ligands
    ]
    calls = []
    provider = msm.structure.least_rmsd_fit

    def recorded(*args, **kwargs):
        calls.append(kwargs)
        return provider(*args, **kwargs)

    monkeypatch.setattr(msm.structure, "least_rmsd_fit", recorded)
    result = consensus(ligands, correspondence_strategy=strategy)
    assert result["complete"] and result["models"]
    report = result["report"]
    assert report["criteria"]["reference_ligand_id"] == "a"
    assert [r["status"] for r in report["source_alignments"]] == [
        "pivot",
        "placed",
        "unplaced",
    ]
    assert calls and all(
        c["precision"] == "double" and c["use_gpu"] is False for c in calls
    )
    assert report["n_fits"] == len(calls)
    assert report["n_layouts"] == len(
        report["source_alignments"][1]["accepted_placements"]
    )
    for model in result["models"]:
        assert model.n_interaction_sites == 5
        assert model.metadata["hypothesis"]["joint_ligand_ids"] == ["a", "b"]
        assert model.metadata["hypothesis"]["joint_support_fraction"] == pytest.approx(
            2 / 3
        )
        assert model.metadata["layout"]["unplaced_ligand_ids"] == ["no-features"]
        alignment = model.metadata["placements"][1]["alignment"]
        fitted = puw.QuantityRecord.from_dict(
            alignment["aligned_atom_coordinates"]
        ).to_quantity(unit="nm", dimensionality={"[L]": 1})
        np.testing.assert_allclose(
            puw.get_value(fitted, to_unit="nm")[0], COORDINATES, atol=1e-12
        )
        assert alignment["provider"] == "molsysmt.structure.least_rmsd_fit"
        json.dumps(model.metadata, allow_nan=False)
    json.dumps(report, allow_nan=False)
    for ligand, original in zip(ligands, before):
        np.testing.assert_array_equal(
            puw.get_value(
                msm.get(ligand["molecular_system"], coordinates=True), to_unit="nm"
            ),
            original,
        )


def test_association_graph_matches_independent_injective_mapping_oracle():
    centers = np.array([[0, 0, 0], [0.2, 0, 0], [0, 0.5, 0], [0.1, 0.2, 0.7]])
    target = centers[[2, 0, 3, 1]] @ np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]) + [
        5,
        3,
        2,
    ]
    first, second = inventory(centers), inventory(target)
    result = get_rigid_feature_correspondences(
        first, second, distance_tolerance="0.0001 nm", min_matches=4
    )
    oracle = []
    for columns in permutations(range(4)):
        if all(
            abs(
                np.linalg.norm(centers[i] - centers[j])
                - np.linalg.norm(target[columns[i]] - target[columns[j]])
            )
            <= 0.0002
            for i in range(4)
            for j in range(i)
        ):
            oracle.append([[i, column] for i, column in enumerate(columns)])
    assert result["correspondences"] == sorted(oracle)
    assert len(oracle) == 1 and result["complete"]
    assert result["n_graph_nodes"] == 16


@pytest.mark.parametrize("strategy", ["association_cliques", "triplet_seeds"])
def test_reflection_passes_invariant_filter_but_cannot_support_full_consensus(strategy):
    ligands = inputs()
    ligands[1]["molecular_system"] = system(SMILES, COORDINATES * [1, 1, -1])
    result = consensus(ligands, correspondence_strategy=strategy)
    assert result["models"] == [] and result["complete"]
    placements = result["report"]["source_alignments"][1]
    assert placements["proposals"]["correspondences"]
    assert placements["status"] == "unplaced" and placements["rejected_placements"]


def test_distorted_source_and_missing_direct_pivot_placement_do_not_claim_no_chemistry():
    ligands = inputs()
    changed = COORDINATES.copy()
    changed[-1] += [0, 0, 2]
    ligands[1]["molecular_system"] = system(SMILES, changed)
    result = consensus(ligands)
    assert result["complete"] and result["models"] == []
    assert result["report"]["source_alignments"][1]["status"] == "unplaced"
    assert len(result["report"]["sources"][1]["features"]) == 5


def symmetric_inputs():
    centers = np.array([[0, 0, 0], [0.4, 0, 0], [0.2, np.sqrt(3) * 0.2, 0]])
    coordinates = np.vstack(
        [
            center + delta
            for center in centers
            for delta in ([-0.1, 0, 0], [0, 0, 0], [0.1, 0, 0])
        ]
    )
    source = system("COC.COC.COC", coordinates)
    return [
        dict(ligand_id="left", molecular_system=source),
        dict(ligand_id="right", molecular_system=moved(source)),
    ]


@pytest.mark.parametrize("strategy", ["association_cliques", "triplet_seeds"])
def test_ambiguous_mappings_are_retained_without_coverage_early_stop(strategy):
    result = from_rigid_ligands(
        symmetric_inputs(),
        features=["hb acceptor"],
        correspondence_strategy=strategy,
        distance_tolerance="0.01 nm",
        min_sites=3,
    )
    assert result["report"]["n_fits"] == result["report"]["n_layouts"] == 6
    assert len(result["models"]) == 6
    mappings = {
        tuple(
            map(tuple, model.metadata["placements"][1]["alignment"]["correspondence"])
        )
        for model in result["models"]
    }
    assert len(mappings) == 6
    assert (
        len({model.metadata["layout"]["layout_id"] for model in result["models"]}) == 6
    )


@pytest.mark.parametrize(
    "options,stage",
    [
        ({"max_graph_nodes": 1}, "association_graph"),
        (
            {"correspondence_strategy": "triplet_seeds", "max_trials": 1},
            "triplet_proposals",
        ),
        (
            {"correspondence_strategy": "triplet_seeds", "max_fits": 1},
            "rigid_alignment",
        ),
        ({"max_cliques": 1}, "association_cliques"),
        ({"max_layouts": 1}, "alignment_layouts"),
        ({"max_combinations": 1}, "hypothesis_combinations"),
    ],
)
def test_exhausted_resource_is_failure_never_an_empty_consensus(options, stage):
    with pytest.raises(CliqueLimitError) as caught:
        from_rigid_ligands(
            symmetric_inputs(),
            features=["hb acceptor"],
            distance_tolerance="0.01 nm",
            **options,
        )
    assert caught.value.extra["stage"] == stage
    assert caught.value.extra["complete"] is False


def test_selection_frame_unit_policy_and_explicit_pivot_are_preserved():
    source = system(SMILES + ".[Na+]", np.vstack((COORDINATES, [[4, 5, 6]])))
    source.structures.append(
        coordinates=puw.quantity([np.vstack((COORDINATES, [[4, 5, 6]]))], "nm")
    )
    displaced = msm.structure.translate(
        source,
        selection=list(range(8)),
        structure_indices=[1],
        translation=puw.quantity([[[2, 1, 3]]], "nm"),
        in_place=False,
    )
    before = puw.get_value(msm.get(displaced, coordinates=True), to_unit="nm").copy()
    ligands = [
        dict(
            ligand_id="b",
            molecular_system=displaced,
            selection=list(range(8)),
            structure_index=1,
        ),
        dict(
            ligand_id="a",
            molecular_system=source,
            selection=list(range(8)),
            structure_index=0,
        ),
    ]
    with puw.context(standard_units=["angstrom", "ps", "degrees"]):
        result = consensus(ligands, reference_index=1, direction_tolerance="0 degrees")
    assert result["models"] and result["report"]["criteria"]["reference_index"] == 1
    assert result["report"]["sources"][0]["structure_index"] == 1
    assert (
        result["models"][0].metadata["placements"][0]["alignment"]["structure_index"]
        == 1
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(displaced, coordinates=True), to_unit="nm"), before
    )


def test_provider_failure_propagates_without_local_geometry_fallback(monkeypatch):
    def broken(*args, **kwargs):
        raise RuntimeError("provider failed")

    monkeypatch.setattr(msm.structure, "least_rmsd_fit", broken)
    with pytest.raises(RuntimeError, match="provider failed"):
        consensus(inputs())


@pytest.mark.parametrize(
    "options",
    [
        {"reference_index": 99},
        {"min_matches": 2},
        {"min_matches": True},
        {"correspondence_strategy": "unknown"},
        {"max_fits": 0},
        {"max_layouts": False},
    ],
)
def test_public_contract_rejects_invalid_options(options):
    with pytest.raises(ArgumentError):
        consensus(inputs(), **options)


def test_collinear_pivot_is_rejected_and_empty_candidate_is_completed():
    with pytest.raises(ArgumentError, match="non-collinear"):
        get_rigid_feature_correspondences(
            inventory([[0, 0, 0], [1, 0, 0], [2, 0, 0]]), inventory([])
        )
    result = get_rigid_feature_correspondences(
        inventory([[0, 0, 0], [1, 0, 0], [0, 1, 0]]), inventory([])
    )
    assert result["complete"] and result["correspondences"] == []


def test_real_ackredit_captures_solver_branches_and_native_model_roundtrip(tmp_path):
    import ackredit

    with ackredit.session("rigid-modeling"), phmt.attribution():
        result = consensus(inputs())
    payload = result["attribution"]
    assert payload["status"] == "captured"
    titles = [item["title"] for item in payload["references"]["items"]]
    assert any("cliques of an undirected graph" in title for title in titles)
    assert any("rectangular assignment" in title for title in titles)
    assert "MolSysMT" in titles
    model = result["models"][0]
    assert model.metadata["attribution"] == payload
    filename = tmp_path / "rigid.json"
    to_json(model, filename)
    loaded = load_json(filename)
    assert loaded.metadata["attribution"] == payload
    assert loaded.metadata["placements"] == model.metadata["placements"]
    bibliography = phmt.attribution_report(
        loaded.metadata["attribution"], format="bibtex"
    )
    assert "10.1145/362342.362367" in bibliography
    assert "10.1107/S0567739476001873" in bibliography


def test_triplet_proposal_attribution_does_not_claim_unexecuted_clique_solver():
    import ackredit

    ligands = inputs()
    first, second = [
        get_features(ligand["molecular_system"], features=FAMILIES)
        for ligand in ligands
    ]
    with ackredit.session("triplet-only"), phmt.attribution():
        proposals = get_rigid_feature_correspondences(
            first, second, correspondence_strategy="triplet_seeds"
        )
    assert proposals["attribution"]["status"] == "captured"
    titles = [item["title"] for item in proposals["attribution"]["references"]["items"]]
    assert not any("cliques" in title for title in titles)
