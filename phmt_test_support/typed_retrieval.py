"""Six-family analytical case composition; no molecular collection or public index."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

from phmt_test_support.snapshot_retrieval import SnapshotRetrievalStudy, project

DIRECTORY = Path(__file__).resolve().parents[1] / "tests/data/typed_retrieval"


def declaration():
    result = json.loads((DIRECTORY / "declaration.json").read_text())
    if result["schema"] != "pharmacophoremt.typed-retrieval-case@1":
        raise ValueError("Unknown typed retrieval case")
    return result


def identity(path):
    with Path(path).open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"bytes": Path(path).stat().st_size, "sha256": digest}


def load_parent(key):
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    case = next(c for c in declaration()["parents"] if c["key"] == key)
    manifest = json.loads((DIRECTORY / "parents.json").read_text())
    row = next(r for r in manifest["parents"] if r["key"] == key)
    path = DIRECTORY / row["file"]
    assert identity(path) == {k: row[k] for k in ("bytes", "sha256")}
    source = msm.h5msm.read(str(path))
    assert msm.get(source, element="atom", atom_type=True) == case["atom_types"]
    assert msm.get(source, formal_charge=True) == case["formal_charges"]
    assert source.chemical_states.get(n_bonds=True) == case["n_bonds"]
    assert msm.get(source, n_structures=True) == 1
    np.testing.assert_allclose(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm")[0],
        case["coordinates_nm"],
        rtol=0,
        atol=declaration()["coordinate_tolerance_nm"],
    )
    return source, {
        "source_key": "nm" if key == "donors4" else key,
        "occurrence_key": "1 nm" if key == "donors4" else key + ":0",
        "artifact_sha256": row["sha256"],
        "artifact_bytes": row["bytes"],
        "n_atoms": row["n_atoms"],
        "structure_index": 0,
        "chemical_state": 0,
        "trust": "caller-verified-artifact/unchanged-source",
        "preparation": row["preparation"],
    }


def check_native(case, inventory):
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    points = project(inventory)
    assert [r[0] for r in points] == case["expected_types"]
    assert [r["atom_indices"] for r in inventory["features"]] == case[
        "expected_atom_maps"
    ]
    assert [r["geometry_atom_indices"] for r in inventory["features"]] == case[
        "expected_atom_maps"
    ]
    np.testing.assert_allclose(
        [r[1] for r in points], case["expected_centers_angstrom"], rtol=0, atol=1e-11
    )
    for i, row in enumerate(inventory["features"]):
        if row["kind"] == "hb donor":
            np.testing.assert_allclose(
                puw.get_value(row["direction"], to_unit="dimensionless"),
                case["expected_directions"][i],
                rtol=0,
                atol=1e-12,
            )
        if row["kind"] == "aromatic ring":
            np.testing.assert_allclose(
                np.abs(puw.get_value(row["normal"], to_unit="dimensionless")),
                case["expected_normal_axis"],
                rtol=0,
                atol=1e-12,
            )
        if row["kind"] in ("positive charge", "negative charge"):
            assert puw.get_value(row["charge"], to_unit="e") == (
                1 if row["kind"] == "positive charge" else -1
            )


def load_entries(context):
    if context not in ("source", "installed"):
        raise ValueError("Choose an explicit original capture context")
    manifest = json.loads((DIRECTORY / "originals.json").read_text())
    files = {r["file"]: r for r in manifest["snapshots"]}
    result = []
    for work in declaration()["work"]:
        name = context + "/" + work["origin"] + "/" + work["file"]
        path = DIRECTORY / name
        if identity(path) != {k: files[name][k] for k in ("bytes", "sha256")}:
            raise ValueError("Original captured snapshot identity mismatch")
        result.append({"work_key": work["work_key"], "snapshot": path.read_bytes()})
    return result


def compare_domain(entries, spec, progress=None):
    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.screening import evaluate_feature_correspondence
    from phmt_test_support.feature_snapshot_case import projection as native_projection
    from phmt_test_support.retrieval_controls import exact_mapping_oracle
    from phmt_test_support.snapshot_retrieval import (
        query_inventory,
        reference_proposals,
    )

    initial = SnapshotRetrievalStudy(entries, spec["bin_widths"][0])
    original = initial.describe()
    assert original["eligible_original_ordinals"] == spec["eligible_original_ordinals"]
    assert [r["feature_count"] for r in original["original_occurrences"]] == spec[
        "expected_counts"
    ]
    native = [initial.original_inventory(i) for i in range(len(entries))]
    before = [native_projection(inv) for inv in native]
    points = [{"features": project(inv)} for inv in native]
    references, rational, rows, build = {}, {}, [], []
    counts = {"exhaustive": 0, "retrieved": 0}
    state = {
        "complete": False,
        "original_manifest": original,
        "reference_full_mappings": references,
        "rational_full_mappings": rational,
        "reference_calls": counts,
        "strict_oracle_comparisons": 0,
        "candidate_band_observations": [],
        "rows": rows,
        "build": build,
        "orientation_checks": [],
    }

    def retain():
        if progress is not None:
            progress(state)

    retain()
    for query in spec["queries"]:
        actual_rows = references[query["key"]] = []
        rational_rows = rational[query["key"]] = []
        for ordinal, inventory in enumerate(native):
            state["current_operation"] = {
                "phase": "exhaustive",
                "query": query["key"],
                "work_ordinal": ordinal,
            }
            actual = reference_proposals(query, inventory)
            counts["exhaustive"] += 1
            assert all(len(pairs) == len(query["features"]) for pairs in actual)
            oracle = exact_mapping_oracle(query, points[ordinal])
            if query["classification"] == "strict-interior":
                assert actual == oracle, (query["key"], ordinal, actual, oracle)
                state["strict_oracle_comparisons"] += 1
            else:
                state["candidate_band_observations"].append(
                    {
                        "query": query["key"],
                        "work_ordinal": ordinal,
                        "native": actual,
                        "rational": oracle,
                        "equal": actual == oracle,
                    }
                )
            actual_rows.append(actual)
            rational_rows.append(oracle)
            retain()
        assert [i for i, mappings in enumerate(actual_rows) if mappings] == query[
            "expected_native_positive_ordinals"
        ], query["key"]
    for width in spec["bin_widths"]:
        index = SnapshotRetrievalStudy(entries, width)
        build.append(
            {
                "width": width,
                "asset_identity": index.identity,
                "pair_entries": index.describe()["pair_entries"],
            }
        )
        for query in spec["queries"]:
            state["current_operation"] = {
                "phase": "retrieval",
                "query": query["key"],
                "width": width,
            }
            lookup = index.lookup(query, current_entries=entries)
            assert lookup["complete"]
            actual = [[] for _ in entries]
            for ordinal in lookup["candidate_ordinals"]:
                state["current_operation"]["work_ordinal"] = ordinal
                actual[ordinal] = reference_proposals(query, native[ordinal])
                counts["retrieved"] += 1
            assert actual == references[query["key"]], (query["key"], width)
            exact = index.lookup(query, current_entries=entries, exact_bin=True)
            misses = [
                i
                for i, mappings in enumerate(references[query["key"]])
                if mappings and i not in exact["candidate_ordinals"]
            ]
            joined = []
            for ordinal, mappings in enumerate(actual):
                occurrence = original["original_occurrences"][ordinal]
                for pairs in mappings:
                    joined.append(
                        {
                            "work_ordinal": ordinal,
                            "work_key": occurrence["work_key"],
                            "snapshot_sha256": occurrence["snapshot_sha256"],
                            "pairs": pairs,
                            "matched_original_feature_maps": [
                                occurrence["original_feature_maps"][j] for _, j in pairs
                            ],
                        }
                    )
            rows.append(
                {
                    "query": query["key"],
                    "classification": query["classification"],
                    "width": width,
                    "lookup": lookup,
                    "exact_bin_lookup": exact,
                    "exact_bin_missing_native_positive_ordinals": misses,
                    "original_full_mappings": actual,
                    "joined_mappings": joined,
                    "equal_native_exhaustive": True,
                }
            )
            retain()
    for key in ("donor-four", "aromatic-three"):
        query = next(q for q in spec["queries"] if q["key"] == key)
        for ordinal in query["expected_native_positive_ordinals"]:
            checks = []
            for pairs in references[key][ordinal]:
                checked = evaluate_feature_correspondence(
                    query_inventory(query),
                    native[ordinal],
                    pairs,
                    distance_tolerance=puw.quantity(query["tolerance"], "angstrom"),
                )
                checks.append({"pairs": pairs, "evaluation": checked})
            if key == "donor-four":
                assert (
                    len(checks) == 2
                    and sum(c["evaluation"]["all_pairs_valid"] for c in checks) == 1
                )
                assert all(c["evaluation"]["all_positions_valid"] for c in checks)
            else:
                assert len(checks) == 1 and checks[0]["evaluation"]["all_pairs_valid"]
                opposite = deepcopy(query)
                opposite["normals"][0] = [-x for x in query["normals"][0]]
                checked = evaluate_feature_correspondence(
                    query_inventory(opposite),
                    native[ordinal],
                    checks[0]["pairs"],
                    distance_tolerance=puw.quantity(query["tolerance"], "angstrom"),
                )
                assert checked["all_pairs_valid"]
                checks.append(
                    {
                        "query_axis_reversed": True,
                        "pairs": checks[0]["pairs"],
                        "evaluation": checked,
                    }
                )
            state["orientation_checks"].append(
                {"query": key, "work_ordinal": ordinal, "checks": checks}
            )
            retain()
    assert [native_projection(inv) for inv in native] == before
    prefix = initial.lookup(
        spec["queries"][0], current_entries=entries, max_candidates=1
    )
    assert (
        prefix["candidate_ordinals"] == [1]
        and prefix["pending_candidate_ordinals"] == [6, 10]
        and not prefix["complete"]
        and prefix["unseen_outcomes_are_unknown"]
    )
    state.update(
        complete=True,
        prefix_lookup=prefix,
        all_native_full_query_mappings_preserved=True,
        native_inputs_unchanged=True,
        strict_native_rational_equal=True,
        candidate_band_native_rational_equal=all(
            r["equal"] for r in state["candidate_band_observations"]
        ),
        molecular_operations=0,
        final_pose_or_activity_acceptance=False,
        performance_measured=False,
    )
    retain()
    return state
