"""Frozen analytical stage controls; no production pmapper adapter or index."""

import hashlib
import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parents[1] / "tests/data/pmapper_controls"


def load_declaration():
    data = json.loads((DIRECTORY / "declaration.json").read_text())
    if data["schema"] != "pharmacophoremt.pmapper-controls@1":
        raise ValueError("Unsupported analytical declaration")
    if data["unit"] != "angstrom" or len(data["cases"]) != 8:
        raise ValueError("Expected eight fixed angstrom point cases")
    return data


def squared_distance(first, second):
    """Exact rational squared distance of the original binary operands."""
    return sum((Fraction(a) - Fraction(b)) ** 2 for a, b in zip(first, second))


def rational_oracles(declaration):
    """Independent physical witnesses; no backend fit, norm or cache formula."""
    cases = {row["key"]: row for row in declaration["cases"]}
    impossible = cases["same-bin-impossible"]
    q = impossible["query"][1][1][0]
    s = impossible["source"][1][1][0]
    gap = Fraction(s) - Fraction(q)
    assert gap == Fraction(1, 2) > 2 * Fraction(impossible["position_tolerance"])
    # Every distinct-label triangle fixes the correspondence independently.
    feasible = cases["cross-bin-feasible"]
    shift = feasible["witness_translation"]
    squares = [
        squared_distance(q[1], [Fraction(x) + Fraction(t) for x, t in zip(s[1], shift)])
        for q, s in zip(feasible["query"], feasible["source"])
    ]
    assert squares == [Fraction(1, 256)] * 3
    assert all(x < Fraction(feasible["position_tolerance"]) ** 2 for x in squares)
    # Actual floor bins on the x-axis differ despite this strict interior witness.
    assert int(Fraction(feasible["query"][1][1][0])) == 1
    assert int(Fraction(feasible["source"][1][1][0])) == 2
    reference = cases["identity"]["query"]
    moved = cases["proper-motion"]["source"]
    for (_, point), (_, actual) in zip(reference, moved):
        assert actual == [8 - point[1], point[0] - 4, point[2] + 2]
    tetra = cases["noncoplanar-reflection"]
    assert tetra["source"] == [
        [label, [-xyz[0], xyz[1], xyz[2]]] for label, xyz in tetra["query"]
    ]
    determinant = Fraction(5, 4) * Fraction(13, 4) * Fraction(21, 4)
    assert determinant > 0
    return {
        "same_bin_pair_gap_angstrom": str(gap),
        "cross_bin_squared_deviations_angstrom2": [str(v) for v in squares],
        "reflection_reference_determinant_angstrom3": str(determinant),
        "reflection_source_determinant_angstrom3": str(-determinant),
        "physical_witnesses_are_not_backend_outputs": True,
    }


def _points(rows):
    return [(label, tuple(xyz)) for label, xyz in rows]


def _inventory(rows):
    from pharmacophoremt import pyunitwizard as puw
    from phmt_test_support.absence_inputs import inventory

    labels = load_declaration()["label_map"]
    centers = puw.get_value(
        puw.quantity([xyz for _, xyz in rows], "angstrom"), to_unit="nm"
    )
    return inventory(centers, [labels[label] for label, _ in rows])


def compare_stage(case, limits):
    """Execute real public graph/hash and PHMT proposal operations separately."""
    import numpy as np
    from pmapper.pharmacophore import Pharmacophore as P

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.screening import (
        evaluate_feature_correspondence,
        get_rigid_feature_correspondences,
    )

    reference, source = P(bin_step=case["bin_step"]), P(bin_step=case["bin_step"])
    reference.load_from_feature_coords(_points(case["query"]))
    source.load_from_feature_coords(_points(case["source"]))
    original = (reference.get_feature_coords(), source.get_feature_coords())
    matched = source.fit_model(reference)
    first, second = _inventory(case["query"]), _inventory(case["source"])
    tolerance = puw.quantity(case["position_tolerance"], "angstrom")
    proposals = get_rigid_feature_correspondences(
        first,
        second,
        distance_tolerance=tolerance,
        min_matches=len(case["query"]),
        max_graph_nodes=limits["max_graph_nodes"],
        max_cliques=limits["max_cliques"],
    )
    assert proposals["complete"]
    result = {
        "key": case["key"],
        "pmapper_match": matched is not None,
        "pmapper_source_to_model": None
        if matched is None
        else sorted([int(a), int(b)] for a, b in matched.items()),
        "pmapper_query_hash": reference.get_signature_md5(),
        "pmapper_source_hash": source.get_signature_md5(),
        "pmapper_retained_source_features": len(source.get_feature_coords()),
        "PHMT_proposals": len(proposals["correspondences"]),
        "PHMT_correspondences": proposals["correspondences"],
        "PHMT_finite_family_complete": proposals["complete"],
        "original_source_occurrences": len(case["source"]),
    }
    if case["key"] in ("identity", "proper-motion", "permuted-motion"):
        mapping, matrix, rms = source.fit_model(
            reference, get_transform_matrix=True, get_rms=True
        )
        errors = []
        for source_id, model_id in mapping.items():
            point = np.asarray(source.get_feature_coords()[source_id][1])
            placed = np.asarray(matrix)[:3, :3] @ point + np.asarray(matrix)[:3, 3]
            target = np.asarray(reference.get_feature_coords()[model_id][1])
            errors.append(float(np.linalg.norm(placed - target)))
        assert max(errors) < 1e-10 and float(rms) < 1e-10
        result["external_point_fit"] = {
            "RMS_angstrom": float(rms),
            "max_corresponding_error_angstrom": max(errors),
            "matrix": np.asarray(matrix).tolist(),
        }
    if "witness_translation" in case:
        placed = deepcopy(case["source"])
        for _, xyz in placed:
            for axis, delta in enumerate(case["witness_translation"]):
                xyz[axis] += delta
        witness = evaluate_feature_correspondence(
            first,
            _inventory(placed),
            [[i, i] for i in range(len(placed))],
            distance_tolerance=tolerance,
        )
        assert witness["all_pairs_valid"]
        result["PHMT_supplied_witness_all_pairs_valid"] = True
    assert original == (reference.get_feature_coords(), source.get_feature_coords())
    result["expected_observations_match"] = all(
        result[name] == expected for name, expected in case["expected"].items()
    )
    return result


def cache_controls(declaration):
    """Observe mutable-object equivalence separately from scientific matches."""
    import random

    from pmapper.pharmacophore import Pharmacophore as P

    points = _points(declaration["cases"][0]["query"])

    def make(rows, step=1, cached=False):
        p = P(bin_step=step, cached=cached)
        p.load_from_feature_coords(rows)
        return p

    fresh = make(points)
    cached = make(points, cached=True)
    immutable = cached.get_signature_md5() == fresh.get_signature_md5()
    original_hash = cached.get_signature_md5()
    cached.update(bin_step=0.5)
    changed_hash = cached.get_signature_md5()
    changed_fresh = make(points, step=0.5).get_signature_md5()
    uncached = make(points)
    uncached.get_signature_md5()
    uncached.update(bin_step=0.5)
    uncached_equal = uncached.get_signature_md5() == changed_fresh
    reloaded = make(points, cached=True)
    reloaded_original = reloaded.get_signature_md5()
    replacement = [(label, tuple(2 * x for x in xyz)) for label, xyz in points]
    reloaded.load_from_feature_coords(replacement)
    reload_hash = reloaded.get_signature_md5()
    reload_fresh = make(replacement).get_signature_md5()
    cached.add_feature("A", (0, 0, 5.25))
    after_add_subset = cached.get_signature_md5(ids=[0, 1, 2])
    initial_rng = random.getstate()
    try:
        random.seed(12345)
        before = random.getstate()
        bits = fresh.get_fp(min_features=3, max_features=3, nbits=128)
        after = random.getstate()
    finally:
        random.setstate(initial_rng)
    observed = {
        "immutable_cached": immutable,
        "warm_bin_change_equals_fresh": changed_hash == changed_fresh,
        "uncached_bin_change_equals_fresh": uncached_equal,
        "warm_coordinate_reload_equals_fresh": reload_hash == reload_fresh,
        "add_feature_clears_stale_subset": after_add_subset == changed_fresh,
        "fingerprint_changes_global_rng": before != after,
    }
    return {
        "observed": observed,
        "expected_observations_match": observed == declaration["extra_controls"],
        "bin_change": {
            "original": original_hash,
            "warm_changed": changed_hash,
            "fresh_changed": changed_fresh,
            "cache_equivalence_passed": changed_hash == changed_fresh,
        },
        "coordinate_reload": {
            "original": reloaded_original,
            "warm_reloaded": reload_hash,
            "fresh_reloaded": reload_fresh,
            "cache_equivalence_passed": reload_hash == reload_fresh,
        },
        "fingerprint_bits": sorted(bits),
        "RNG_restored_after_observation": random.getstate() == initial_rng,
        "digest_authenticates_source_or_molecules": False,
    }


def file_identity(path):
    with Path(path).open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"bytes": Path(path).stat().st_size, "sha256": digest}
