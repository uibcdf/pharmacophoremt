"""Frozen P1 case orchestration; not a shipped external-engine adapter."""

import json
from copy import deepcopy
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parents[1] / "tests/data/pharmer_p1"


def load_declaration(directory=DIRECTORY):
    """Load original synthetic declarations without importing science providers."""
    directory = Path(directory)
    data = json.loads((directory / "declaration.json").read_text())
    if data.get("schema") != "pharmacophoremt.pharmer-p1@1":
        raise ValueError("unsupported P1 declaration")
    query = json.loads((directory / data["query"]).read_text())
    return data, query


def qualify_case(case, *, max_trials=None):
    """Receive one PHMT arm with real public recognition, fitting and evaluation.

    The complete proposal set is retained, then every surviving mapping is fit.
    Budget exhaustion raises rather than becoming a geometric negative. The
    caller owns interpretation of an empty complete set and the independent
    oracle. Original fixture expectations are never used to manufacture output.
    """
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt._private.molsysmt import detached
    from pharmacophoremt.io.pharmer import from_pharmer
    from pharmacophoremt.modeler import get_features
    from pharmacophoremt.screening import (
        PoseEvaluator,
        align_to_pharmacophore,
        get_correspondences,
    )
    from phmt_test_support.absence_inputs import system

    declaration, raw_query = load_declaration()
    original = deepcopy((declaration, raw_query, case))
    query = from_pharmer(raw_query)
    query_before = detached(
        query.get(get_center=True, get_radius=True, get_features=True)
    )
    source = system(
        declaration["smiles"], case["centers"], unit=declaration["source_unit"]
    )
    options = {
        name: declaration[name]
        for name in ("selection", "structure_index", "chemical_state")
    }
    coordinates_before = puw.get_value(
        msm.get(source, coordinates=True), to_unit="nm"
    ).copy()
    inventory = get_features(source, features=declaration["features"], **options)
    records = inventory["features"]
    if len(records) != 3 or [row["atom_indices"] for row in records] != [[0], [1], [2]]:
        raise ValueError("P1 requires three original single-atom feature identities")
    if any(row["kind"] != "positive charge" for row in records):
        raise ValueError("P1 requires only positive-charge features")
    inventory_before = detached(inventory)
    proposals = get_correspondences(
        query,
        inventory,
        max_trials=declaration["max_trials"] if max_trials is None else max_trials,
    )
    if not proposals["complete"]:
        raise RuntimeError("P1 candidate enumeration is incomplete; no answer accepted")
    placements = []
    for pairs in proposals["correspondences"]:
        fitted = align_to_pharmacophore(
            source, query, pairs, feature_inventory=inventory, **options
        )
        final = PoseEvaluator(query).evaluate(fitted["molecular_system"], **options)
        placed = puw.get_value(
            msm.get(fitted["molecular_system"], coordinates=True), to_unit="nm"
        )[0]
        placements.append(
            dict(
                correspondence=pairs,
                alignment=fitted["alignment"],
                final=final,
                aligned_coordinates_nm=placed.tolist(),
            )
        )
    np.testing.assert_array_equal(
        coordinates_before,
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"),
    )
    # Compare portable public quantities and the original cached feature record.
    assert detached(inventory) == inventory_before
    assert (
        detached(query.get(get_center=True, get_radius=True, get_features=True))
        == query_before
    )
    assert (declaration, raw_query, case) == original
    return dict(
        key=case["key"],
        proposals=proposals,
        placements=placements,
        recognition=inventory["recognition"],
        original_atom_indices=[row["atom_indices"] for row in records],
        input_coordinates_unchanged=True,
        input_inventory_unchanged=True,
        query_unchanged=True,
        external_state="not_executed",
    )


def expectation_passed(case, result):
    """Compare the actual PHMT record with the frozen independent expectations."""
    import numpy as np

    declaration, _ = load_declaration()
    expected = case["expected"]
    scientific_fields = ("correspondences", "n_trials", "n_pruned", "complete")
    if {key: result["proposals"][key] for key in scientific_fields} != {
        key: expected[key] for key in scientific_fields
    }:
        return False
    if len(result["placements"]) != expected["matched_placements"]:
        return False
    for row in result["placements"]:
        if row["final"]["status"] != "matched" or row["final"]["fit_value"] != 1:
            return False
        placed = np.asarray(row["aligned_coordinates_nm"])
        reference = np.asarray(declaration["reference_centers_nm"])
        for site, atom in row["correspondence"]:
            if (
                np.linalg.norm(placed[atom] - reference[site])
                > declaration["position_error_limit_nm"]
            ):
                return False
    return True
