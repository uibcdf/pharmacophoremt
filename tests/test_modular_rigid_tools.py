"""Standalone tool contracts and scientific assembly controls."""

import json
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError, CliqueLimitError
from pharmacophoremt.modeler import (
    from_feature_inventory,
    from_ligand,
    from_rigid_ligands,
    get_features,
)
from pharmacophoremt.screening import (
    get_rigid_feature_correspondences,
    get_rigid_feature_placements,
)
from pharmacophoremt.validation import summarize_rigid_consensus
from tests.test_rigid_consensus import FAMILIES, inputs


def test_cached_inventory_construction_requires_no_molecular_provider_access(
    monkeypatch,
):
    source = inputs()[0]["molecular_system"]
    inventory = get_features(source, features=FAMILIES)
    expected = from_ligand(source, features=FAMILIES, radius="0.02 nm")

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "cached inventory construction must not read a molecular system"
        )

    monkeypatch.setattr(msm, "get", forbidden)
    query = from_feature_inventory(inventory, radius="0.02 nm")
    assert query.molecular_system is None
    assert query.n_interaction_sites == expected.n_interaction_sites == 5
    for site, original in zip(query.interaction_sites, expected.interaction_sites):
        assert site.features == original.features
        assert site.shape.shape_name == original.shape.shape_name
        np.testing.assert_allclose(
            puw.get_value(site.center, to_unit="nm"),
            puw.get_value(original.center, to_unit="nm"),
        )
    before = deepcopy(query.metadata)
    inventory["features"].clear()
    assert query.metadata == before


def test_inventory_orientation_contract_and_included_volume():
    source = inputs()[0]["molecular_system"]
    inventory = get_features(source, features=["hb donor"])
    inventory["features"][0]["direction"] = None
    with pytest.raises(ArgumentError, match="orientation"):
        from_feature_inventory(inventory)
    included = get_features(source, features=["included volume"])
    query = from_feature_inventory(included)
    assert query.n_interaction_sites == len(included["features"])
    assert all(site.features == ["included volume"] for site in query.interaction_sites)


def test_explicit_mapping_placement_is_standalone_detached_and_source_preserving():
    ligands = inputs()
    first, second = [
        get_features(ligand["molecular_system"], features=FAMILIES)
        for ligand in ligands
    ]
    source = ligands[1]["molecular_system"]
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    proposals = get_rigid_feature_correspondences(
        first, second, distance_tolerance="0.02 nm", min_matches=5
    )
    mappings = proposals["correspondences"][:1]
    placed = get_rigid_feature_placements(
        source,
        first,
        mappings,
        features=FAMILIES,
        feature_inventory=second,
        distance_tolerance="0.02 nm",
        min_matches=5,
    )
    assert placed["complete"] and len(placed["placements"]) == 1
    copy = placed["placements"][0]["molecular_system"]
    assert copy is not source
    query = from_feature_inventory(first, radius="0.02 nm")
    assert phmt.screening.PoseEvaluator(query).evaluate(copy)["status"] == "matched"
    json.dumps(placed["report"], allow_nan=False)
    report = deepcopy(placed["report"])
    placed["placements"][0]["inventory"]["features"].clear()
    assert placed["report"] == report
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )


def test_placement_budget_preflight_and_invalid_injective_mapping_never_fit(
    monkeypatch,
):
    ligands = inputs()
    first, second = [
        get_features(ligand["molecular_system"], features=FAMILIES)
        for ligand in ligands
    ]
    mapping = [[0, 0], [1, 1], [2, 2]]

    def forbidden(*args, **kwargs):
        raise AssertionError("should fail before fitting")

    monkeypatch.setattr(msm.structure, "least_rmsd_fit", forbidden)
    with pytest.raises(CliqueLimitError):
        get_rigid_feature_placements(
            ligands[1]["molecular_system"],
            first,
            [mapping, mapping],
            feature_inventory=second,
            features=FAMILIES,
            max_fits=1,
        )
    with pytest.raises(ArgumentError, match="unique"):
        get_rigid_feature_placements(
            ligands[1]["molecular_system"],
            first,
            [[[0, 0], [1, 1], [1, 2]]],
            feature_inventory=second,
            features=FAMILIES,
        )
    empty = get_rigid_feature_placements(
        ligands[1]["molecular_system"],
        first,
        [],
        feature_inventory=second,
        features=FAMILIES,
    )
    assert (
        empty["complete"]
        and empty["placements"] == []
        and empty["report"]["n_fits"] == 0
    )


def test_modeler_calls_public_placement_tool_for_each_nonpivot_source(monkeypatch):
    from pharmacophoremt.screening import rigid_placements

    original = rigid_placements.get_rigid_feature_placements
    calls = []

    def observed(*args, **kwargs):
        calls.append(len(args[2]))
        return original(*args, **kwargs)

    monkeypatch.setattr(rigid_placements, "get_rigid_feature_placements", observed)
    result = from_rigid_ligands(
        inputs(third=True),
        features=FAMILIES,
        min_matches=5,
        distance_tolerance="0.02 nm",
    )
    assert result["models"] and calls == [1, 0]


def test_saved_report_summary_preserves_support_counts_and_never_credits_reading():
    import ackredit

    result = from_rigid_ligands(
        inputs(third=True),
        features=FAMILIES,
        min_matches=5,
        min_sites=5,
        distance_tolerance="0.02 nm",
    )
    saved = json.loads(json.dumps(result["report"], allow_nan=False))
    with ackredit.session("report-reading"), phmt.attribution():
        before = ackredit.get_attribution().to_dict()
        summary = summarize_rigid_consensus(saved)
        assert ackredit.get_attribution().to_dict() == before
    assert summary["n_ligands"] == 3
    assert summary["n_fits"] == 1 and summary["max_joint_sites"] == 5
    assert summary["n_models"] == len(result["models"])
    assert summary["hypotheses"][0]["joint_support_fraction"] == pytest.approx(2 / 3)
    assert summary["sources"][2]["status"] == "unplaced"
    assert summary["sources"][2]["n_features"] == 1
    before = deepcopy(summary)
    saved["layouts"].clear()
    assert summary == before


@pytest.mark.parametrize(
    "mutate",
    [
        lambda report: report.update(complete=False),
        lambda report: report.update(n_fits=999),
        lambda report: report["layouts"][0]["consensus"].update(complete=False),
        lambda report: report["source_alignments"].reverse(),
    ],
)
def test_invalid_or_incomplete_report_is_never_summarized_as_a_negative(mutate):
    result = from_rigid_ligands(
        inputs(),
        features=FAMILIES,
        min_matches=5,
        min_sites=5,
        distance_tolerance="0.02 nm",
    )
    mutate(result["report"])
    with pytest.raises(ArgumentError):
        summarize_rigid_consensus(result["report"])
