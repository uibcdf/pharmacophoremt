"""Analytical objective counterexample and frozen comparison expectations."""

import numpy as np
import pytest

from devtools.benchmark_rigid_consensus import _matches_expectation
from devtools.rigid_consensus_cases import build_case, load_cases
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import CliqueLimitError
from pharmacophoremt.modeler import (
    from_feature_inventory,
    from_rigid_ligands,
    get_features,
)
from pharmacophoremt.modeler.aligned_consensus import get_aligned_feature_matches
from pharmacophoremt.screening import (
    align_to_pharmacophore,
    get_rigid_feature_correspondences,
    get_rigid_feature_placements,
)
from pharmacophoremt.validation import summarize_rigid_consensus


def test_minimum_rmsd_loses_tolerance_valid_coverage_to_triplet_placements():
    case = next(case for case in load_cases() if case["case_id"] == "warped_square")
    ligands = build_case(case)
    parameters = case["parameters"]
    target, source = [
        get_features(ligand["molecular_system"], features=parameters["features"])
        for ligand in ligands
    ]
    query = from_feature_inventory(target, radius=parameters["distance_tolerance"])
    full = align_to_pharmacophore(
        ligands[1]["molecular_system"],
        query,
        [[i, i] for i in range(4)],
        feature_inventory=source,
    )
    full_inventory = get_features(
        full["molecular_system"], features=parameters["features"]
    )
    assert (
        get_aligned_feature_matches(
            target, full_inventory, distance_tolerance=parameters["distance_tolerance"]
        )["matches"]
        == []
    )
    proposals = get_rigid_feature_correspondences(
        target,
        source,
        correspondence_strategy="triplet_seeds",
        distance_tolerance=parameters["distance_tolerance"],
    )
    alternative = get_rigid_feature_placements(
        ligands[1]["molecular_system"],
        target,
        proposals["correspondences"][:1],
        feature_inventory=source,
        features=parameters["features"],
        distance_tolerance=parameters["distance_tolerance"],
    )
    assert len(alternative["placements"][0]["matches"]["matches"]) == 3
    # Compare RMSD over the SAME four feature pairs, not the seed's three pairs.
    all_centers = [
        [puw.get_value(r["center"], to_unit="nm") for r in inventory["features"]]
        for inventory in (target, alternative["placements"][0]["inventory"])
    ]
    alternative_full_rmsd = np.sqrt(
        np.mean(np.sum((np.array(all_centers[0]) - all_centers[1]) ** 2, axis=1))
    )
    minimum_rmsd = puw.get_value(
        puw.QuantityRecord.from_dict(full["alignment"]["rmsd"]).to_quantity(
            unit="nm", dimensionality={"[L]": 1}
        ),
        to_unit="nm",
    )[0]
    assert minimum_rmsd == pytest.approx(0.11) and alternative_full_rmsd > minimum_rmsd


@pytest.mark.parametrize("case", load_cases(), ids=lambda case: case["case_id"])
@pytest.mark.parametrize("strategy", ["association_cliques", "triplet_seeds"])
def test_frozen_analytical_case_expectations(case, strategy):
    ligands = build_case(case)
    expected = case["expected"][strategy]
    if expected["status"] == "failed":
        with pytest.raises(CliqueLimitError) as caught:
            from_rigid_ligands(
                ligands, correspondence_strategy=strategy, **case["parameters"]
            )
        assert caught.value.code == expected["error_code"]
        assert not _matches_expectation(dict(status="completed_empty"), expected)
    else:
        result = from_rigid_ligands(
            ligands, correspondence_strategy=strategy, **case["parameters"]
        )
        summary = summarize_rigid_consensus(result["report"])
        outcome = dict(
            status="completed" if result["models"] else "completed_empty",
            summary=summary,
        )
        assert _matches_expectation(outcome, expected)
        assert summary["n_models"] == len(result["models"])
        assert not _matches_expectation(
            dict(status="failed", error_code="PHMT-E107"), expected
        )
