"""Bounded composition of original native snapshots and existing study postings."""

import hashlib
import json
from copy import deepcopy
from pathlib import Path

from phmt_test_support.feature_snapshot import FeatureSnapshotStudy
from phmt_test_support.retrieval_controls import StudyIndex

DIRECTORY = Path(__file__).resolve().parents[1] / "tests/data/snapshot_retrieval"
LABELS = {
    "positive charge": "P",
    "negative charge": "N",
    "hydrophobicity": "H",
    "hb acceptor": "A",
    "hb donor": "D",
    "aromatic ring": "R",
}


def declaration():
    result = json.loads((DIRECTORY / "declaration.json").read_text())
    if result["schema"] != "pharmacophoremt.snapshot-retrieval-case@1":
        raise ValueError("Unknown snapshot retrieval case")
    return result


def load_entries(context):
    if context not in ("source", "installed"):
        raise ValueError("Choose an original snapshot context explicitly")
    manifest = json.loads((DIRECTORY / "originals.json").read_text())
    identities = {r["file"]: r for r in manifest["snapshots"]}
    result = []
    for work in declaration()["work"]:
        name = context + "/" + work["snapshot"]
        raw = (DIRECTORY / name).read_bytes()
        identity = identities[name]
        if (
            len(raw) != identity["bytes"]
            or hashlib.sha256(raw).hexdigest() != identity["sha256"]
        ):
            raise ValueError("Original snapshot byte identity mismatch")
        result.append({"work_key": work["work_key"], "snapshot": raw})
    return result


def _entries(entries):
    if type(entries) is not list or len(entries) > 12:
        raise ValueError("Study requires an ordered list of up to twelve entries")
    keys, saved, manifest = set(), [], []
    for ordinal, entry in enumerate(entries):
        if type(entry) is not dict or set(entry) != {"work_key", "snapshot"}:
            raise ValueError("Declare complete work key and original snapshot bytes")
        key = entry["work_key"]
        if type(key) is not str or not key or key in keys:
            raise ValueError("Original work keys must be distinct nonempty text")
        keys.add(key)
        snapshot = FeatureSnapshotStudy(entry["snapshot"])
        saved.append(snapshot)
        manifest.append(
            {
                "work_ordinal": ordinal,
                "work_key": key,
                "snapshot_sha256": hashlib.sha256(snapshot.to_bytes()).hexdigest(),
                **snapshot.describe(),
            }
        )
    return saved, manifest


def _digest(manifest):
    from pharmacophoremt_results import canonical_json

    return hashlib.sha256(canonical_json(manifest).encode()).hexdigest()


def project(inventory):
    from pharmacophoremt import pyunitwizard as puw

    rows = []
    for feature in inventory["features"]:
        if feature["kind"] not in LABELS:
            raise ValueError("Feature kind is outside the bounded point index")
        rows.append(
            [
                LABELS[feature["kind"]],
                puw.get_value(feature["center"], to_unit="angstrom").tolist(),
            ]
        )
    return rows


class SnapshotRetrievalStudy:
    """Preserve original work positions and byte bindings around StudyIndex."""

    def __init__(self, entries, width):
        self._snapshots, self._manifest = _entries(entries)
        self.manifest_sha256 = _digest(self._manifest)
        records, self._eligible = [], []
        for ordinal, (snapshot, row) in enumerate(zip(self._snapshots, self._manifest)):
            inventory = snapshot.decode_inventory()
            n = len(inventory["features"])
            row["indexing"] = (
                "fewer-than-three-in-full-query-profile" if n < 3 else "indexed"
            )
            row["original_feature_maps"] = [
                {
                    "feature_index": i,
                    **{
                        k: feature[k]
                        for k in ("kind", "atom_indices", "geometry_atom_indices")
                    },
                }
                for i, feature in enumerate(inventory["features"])
            ]
            if n < 3:
                continue
            records.append(
                {
                    "source_key": row["parent"]["source_key"],
                    # Index occurrence means the original work occurrence, not the
                    # distinct recorded parent occurrence kept in the binding.
                    "occurrence_key": row["work_key"],
                    "features": project(inventory),
                    "snapshot_binding": deepcopy(row),
                }
            )
            self._eligible.append(ordinal)
        self._records = records
        self._settings = {
            "unit": "angstrom",
            "bin_width": width,
            "anchor_feature_indices": [0, 1],
            "numerical_guard_bins": 1,
            "original_manifest_sha256": self.manifest_sha256,
            "profile": "classical-three-four-point-snapshot-study@2",
            "feature_labels": list(LABELS.values()),
        }
        self._index = StudyIndex(records, self._settings)
        self.identity = self._index.identity

    def describe(self):
        return {
            "manifest_sha256": self.manifest_sha256,
            "asset_identity": self.identity,
            "settings": deepcopy(self._settings),
            "original_occurrences": deepcopy(self._manifest),
            "eligible_original_ordinals": list(self._eligible),
            "pair_entries": self._index.pair_entries,
            "molecular_origin_authenticated": False,
            "final_pose_or_activity_acceptance": False,
        }

    def original_inventory(self, ordinal):
        if type(ordinal) is not int or not 0 <= ordinal < len(self._snapshots):
            raise ValueError("Use an original work ordinal")
        return self._snapshots[ordinal].decode_inventory()

    def original_bytes(self, ordinal):
        if type(ordinal) is not int or not 0 <= ordinal < len(self._snapshots):
            raise ValueError("Use an original work ordinal")
        return self._snapshots[ordinal].to_bytes()

    def lookup(self, query, *, current_entries, **limits):
        _, current = _entries(current_entries)
        if _digest(current) != self.manifest_sha256:
            raise ValueError(
                "Original snapshot/work bindings changed; refuse stale reuse"
            )
        result = self._index.lookup(
            query,
            current_records=self._records,
            current_binding=self._settings,
            **limits,
        )
        compact = result["candidate_ordinals"]
        pending = result["pending_candidate_ordinals"]
        return {
            **result,
            "index_candidate_ordinals": compact,
            "candidate_ordinals": [self._eligible[i] for i in compact],
            "pending_candidate_ordinals": [self._eligible[i] for i in pending],
            "not_indexed_original_ordinals": [
                i for i in range(len(self._snapshots)) if i not in self._eligible
            ],
            "manifest_sha256": self.manifest_sha256,
        }


def query_inventory(query):
    """Build a declared mathematical query; D/R geometry must be explicit."""
    from pharmacophoremt import pyunitwizard as puw
    from phmt_test_support.absence_inputs import inventory as mathematical_inventory
    from phmt_test_support.retrieval_controls import _validate_features

    _validate_features(query["features"])
    n = len(query["features"])
    directions = query.get("directions", [None] * n)
    normals = query.get("normals", [None] * n)
    if any(
        not isinstance(value, (list, tuple)) or len(value) != n
        for value in (directions, normals)
    ):
        raise ValueError("Declare one optional direction/normal per query feature")
    for i, (kind, _) in enumerate(query["features"]):
        if (directions[i] is not None) != (kind == "D") or (normals[i] is not None) != (
            kind == "R"
        ):
            raise ValueError(
                "Explicit donor direction/aromatic normal presence mismatch"
            )
    centers = puw.get_value(
        puw.quantity([xyz for _, xyz in query["features"]], "angstrom"), to_unit="nm"
    )
    kinds = {label: kind for kind, label in LABELS.items()}
    return mathematical_inventory(
        centers,
        [kinds[label] for label, _ in query["features"]],
        directions=directions,
        normals=normals,
    )


def reference_proposals(query, native_inventory):
    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.screening import get_rigid_feature_correspondences

    result = get_rigid_feature_correspondences(
        query_inventory(query),
        native_inventory,
        distance_tolerance=puw.quantity(query["tolerance"], "angstrom"),
        min_matches=len(query["features"]),
        max_graph_nodes=32,
        max_cliques=32,
    )
    if not result["complete"]:
        raise ValueError("The native proposal operation did not complete")
    return result["correspondences"]


def compare_retrieval(entries, spec, progress=None):
    from phmt_test_support.retrieval_controls import exact_mapping_oracle

    study = SnapshotRetrievalStudy(entries, spec["bin_widths"][0])
    original = study.describe()
    if original["eligible_original_ordinals"] != spec["eligible_original_ordinals"]:
        raise ValueError("Original eligible work positions differ from the case")
    if [r["feature_count"] for r in original["original_occurrences"]] != spec[
        "expected_counts"
    ]:
        raise ValueError("Original feature counts differ from the case")
    reference, rows, build = {}, [], []
    calls = {"exhaustive": 0, "retrieved": 0}
    state = {
        "complete": False,
        "rows": rows,
        "build": build,
        "reference_full_mappings": reference,
        "reference_calls": calls,
        "independent_rational_mapping_comparisons": 0,
        "original_manifest": original,
        "original_snapshots": [
            FeatureSnapshotStudy(entry["snapshot"]).to_dict() for entry in entries
        ],
    }

    def retain():
        if progress is not None:
            progress(state)

    retain()
    for query in spec["queries"]:
        answer = reference[query["key"]] = []
        for ordinal in range(len(entries)):
            state["current_operation"] = {
                "phase": "exhaustive",
                "query": query["key"],
                "work_ordinal": ordinal,
            }
            native = study.original_inventory(ordinal)
            actual = reference_proposals(query, native)
            calls["exhaustive"] += 1
            oracle = exact_mapping_oracle(query, {"features": project(native)})
            expected = (
                query["expected_mappings_per_eligible"]
                if ordinal in study._eligible
                else []
            )
            assert actual == oracle == expected, (query["key"], ordinal, actual, oracle)
            state["independent_rational_mapping_comparisons"] += 1
            answer.append(actual)
            retain()
    for width in spec["bin_widths"]:
        index = SnapshotRetrievalStudy(entries, width)
        build.append(
            {
                "width": width,
                "identity": index.identity,
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
                actual[ordinal] = reference_proposals(
                    query, index.original_inventory(ordinal)
                )
                calls["retrieved"] += 1
                retain()
            assert actual == reference[query["key"]], (query["key"], width)
            exact = index.lookup(query, current_entries=entries, exact_bin=True)
            misses = [
                i
                for i, mappings in enumerate(reference[query["key"]])
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
                            "payload_sha256": occurrence["payload_sha256"],
                            "parent": occurrence["parent"],
                            "pairs": pairs,
                            "matched_original_feature_maps": [
                                occurrence["original_feature_maps"][j] for _, j in pairs
                            ],
                        }
                    )
            rows.append(
                {
                    "query": query["key"],
                    "width": width,
                    "lookup": lookup,
                    "exact_bin_lookup": exact,
                    "exact_bin_missing_positive_ordinals": misses,
                    "original_full_mappings": actual,
                    "joined_mappings": joined,
                    "equal_exhaustive": True,
                }
            )
            retain()
    cross = next(
        r for r in rows if r["query"] == "cross-bin-feasible" and r["width"] == 1
    )
    assert (
        cross["exact_bin_missing_positive_ordinals"]
        == spec["negative_control_width_1_expected_missing"]
    )
    narrow = next(
        r for r in rows if r["query"] == "cross-bin-feasible" and r["width"] == 0.125
    )
    assert (
        narrow["exact_bin_missing_positive_ordinals"]
        == spec["negative_control_width_0_125_expected_missing"]
    )
    false_positive = next(
        r for r in rows if r["query"] == "same-anchor-impossible" and r["width"] == 1
    )
    assert false_positive["lookup"]["candidate_ordinals"] == spec[
        "eligible_original_ordinals"
    ] and not any(false_positive["original_full_mappings"])
    prefix = study.lookup(spec["queries"][0], current_entries=entries, max_candidates=1)
    assert (
        prefix["candidate_ordinals"] == [1]
        and prefix["pending_candidate_ordinals"] == [4, 5]
        and not prefix["complete"]
        and prefix["unseen_outcomes_are_unknown"]
    )
    limited_bins = study.lookup(
        spec["queries"][0], current_entries=entries, max_lookup_bins=1
    )
    assert not limited_bins["complete"] and limited_bins["unseen_outcomes_are_unknown"]
    state.update(
        complete=True,
        prefix_lookup=prefix,
        limited_bin_lookup=limited_bins,
        all_original_mappings_equal_exhaustive=True,
        all_original_mappings_equal_rational_oracle=True,
        exact_bin_negative_control_misses=True,
        false_positive_filtered_by_native_reference=True,
        molecular_operations=0,
        final_pose_or_activity_acceptance=False,
        performance_measured=False,
    )
    retain()
    return state
