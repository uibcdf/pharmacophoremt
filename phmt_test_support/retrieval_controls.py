"""Case-specific finite retrieval prototype; not a public index or collection."""

import hashlib
import json
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, permutations
from math import isfinite, isqrt
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parents[1] / "tests/data/retrieval_controls"


def load_declaration():
    data = json.loads((DIRECTORY / "declaration.json").read_text())
    if data["schema"] != "pharmacophoremt.retrieval-controls@1":
        raise ValueError("Unsupported retrieval case declaration")
    if (
        data["unit"] != "angstrom"
        or len(data["records"]) != 12
        or len(data["queries"]) != 9
    ):
        raise ValueError("Expected the fixed twelve-record/nine-query angstrom case")
    return data


def binding(declaration, width):
    return {
        **deepcopy(declaration["metadata"]),
        "unit": declaration["unit"],
        "bin_width": width,
        "anchor_feature_indices": declaration["anchor_feature_indices"],
        "numerical_guard_bins": declaration["numerical_guard_bins"],
    }


def _digest(records, settings):
    payload = json.dumps([records, settings], sort_keys=True, allow_nan=False).encode()
    return hashlib.sha256(payload).hexdigest()


def _validate_features(features):
    if not 3 <= len(features) <= 4:
        raise ValueError("Study requires three or four feature occurrences")
    for kind, xyz in features:
        if kind not in {"P", "N", "H", "A", "D", "R"} or len(xyz) != 3:
            raise ValueError("Unsupported typed point")
        if any(
            type(x) not in (int, float) or not isfinite(x) or abs(x) > 16 for x in xyz
        ):
            raise ValueError(
                "Study coordinates must be finite and bounded by16angstrom"
            )


def _square(first, second):
    return sum((Fraction(a) - Fraction(b)) ** 2 for a, b in zip(first, second))


def distance_bin(first, second, width):
    """Exact floor(sqrt(squared_distance)/width) of the binary operands."""
    width = Fraction(width)
    if width <= 0:
        raise ValueError("Positive bin width required")
    ratio = _square(first, second) / width**2
    return isqrt(ratio.numerator // ratio.denominator)


def _noncollinear(features):
    origin = features[0][1]
    vectors = [
        [Fraction(x) - Fraction(o) for x, o in zip(xyz, origin)]
        for _, xyz in features[1:]
    ]
    return any(
        a[1] * b[2] != a[2] * b[1]
        or a[2] * b[0] != a[0] * b[2]
        or a[0] * b[1] != a[1] * b[0]
        for a, b in combinations(vectors, 2)
    )


def exact_mapping_oracle(query, record):
    """Brute-force exact-distance witness, independent of bins and backend norms."""
    first, second = query["features"], record["features"]
    if not _noncollinear(first):
        raise ValueError("Reference must be noncollinear")
    tolerance_squared = (2 * Fraction(query["tolerance"])) ** 2
    result = []
    for columns in permutations(range(len(second)), len(first)):
        if any(a[0] != second[j][0] for a, j in zip(first, columns)):
            continue
        if not _noncollinear([second[j] for j in columns]):
            continue
        for i, k in combinations(range(len(first)), 2):
            a = _square(first[i][1], first[k][1])
            b = _square(second[columns[i]][1], second[columns[k]][1])
            excess = a + b - tolerance_squared
            if excess > 0 and excess**2 > 4 * a * b:
                break
        else:
            result.append([[i, j] for i, j in enumerate(columns)])
    return sorted(result)


class StudyIndex:
    """Detached twelve-record typed-pair postings for this analytical case only."""

    def __init__(self, records, settings):
        if len(records) > 12 or settings["unit"] != "angstrom":
            raise ValueError("Unsupported study size/unit")
        if (
            type(settings["bin_width"]) not in (int, float)
            or settings["bin_width"] not in (0.125, 0.5, 1.0)
            or type(settings["numerical_guard_bins"]) is not int
            or settings["numerical_guard_bins"] != 1
        ):
            raise ValueError("Unsupported study bin settings")
        if settings["anchor_feature_indices"] != [0, 1]:
            raise ValueError("Unsupported study anchor")
        keys = [(r["source_key"], r["occurrence_key"]) for r in records]
        if len(set(keys)) != len(keys) or any(
            not isinstance(x, str) or not x for key in keys for x in key
        ):
            raise ValueError(
                "Original source/occurrence pairs must be distinct nonempty strings"
            )
        self._records, self._settings = deepcopy(records), deepcopy(settings)
        self.identity = _digest(self._records, self._settings)
        self._postings = {}
        self.pair_entries = 0
        for ordinal, record in enumerate(self._records):
            features = record["features"]
            _validate_features(features)
            for (kind_a, first), (kind_b, second) in combinations(features, 2):
                key = (
                    *sorted((kind_a, kind_b)),
                    distance_bin(first, second, settings["bin_width"]),
                )
                self._postings.setdefault(key, set()).add(ordinal)
                self.pair_entries += 1

    def stored_records(self):
        return deepcopy(self._records)

    def lookup(
        self,
        query,
        *,
        current_records,
        current_binding,
        max_lookup_bins=64,
        max_candidates=12,
        exact_bin=False,
    ):
        if _digest(current_records, current_binding) != self.identity:
            raise ValueError(
                "Study asset is incompatible with current records/settings"
            )
        if type(max_lookup_bins) is not int or not 1 <= max_lookup_bins <= 64:
            raise ValueError("Study lookup bin budget must be in1..64")
        if type(max_candidates) is not int or not 0 <= max_candidates <= 12:
            raise ValueError("Study candidate budget must be in0..12")
        _validate_features(query["features"])
        radius = query["tolerance"]
        if (
            type(radius) not in (int, float)
            or not isfinite(radius)
            or not 0 <= radius <= 1.25
        ):
            raise ValueError("Unsupported study positional tolerance")
        first, second = query["features"][:2]
        width = Fraction(self._settings["bin_width"])
        center = distance_bin(first[1], second[1], width)
        ratio = 2 * Fraction(radius) / width
        span = 0 if exact_bin else -(-ratio.numerator // ratio.denominator) + 1
        start, stop = max(0, center - span), center + span + 1
        searched = list(range(start, min(stop, start + max_lookup_bins)))
        types = sorted((first[0], second[0]))
        candidates = sorted(
            set().union(*(self._postings.get((*types, b), set()) for b in searched))
        )
        pending = candidates[max_candidates:]
        return {
            "candidate_ordinals": candidates[:max_candidates],
            "pending_candidate_ordinals": pending,
            "planned_bin_interval": [start, stop - 1],
            "searched_bins": searched,
            "unsearched_bin_interval": None
            if start + len(searched) == stop
            else [start + len(searched), stop - 1],
            "complete": start + len(searched) == stop and not pending,
            "unseen_outcomes_are_unknown": start + len(searched) != stop
            or bool(pending),
            "asset_identity": self.identity,
            "numerical_guard_bins": 0 if exact_bin else 1,
        }


def reference_proposals(query, record):
    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.screening import get_rigid_feature_correspondences
    from phmt_test_support.pmapper_controls import _inventory

    result = get_rigid_feature_correspondences(
        _inventory(query["features"]),
        _inventory(record["features"]),
        distance_tolerance=puw.quantity(query["tolerance"], "angstrom"),
        min_matches=len(query["features"]),
        max_graph_nodes=32,
        max_cliques=32,
    )
    assert result["complete"]
    return result["correspondences"]


def compare_retrieval(declaration, progress=None):
    records = declaration["records"]
    reference = {}
    calls = {"exhaustive": 0, "retrieved": 0}
    oracle_comparisons = 0
    rows, build = [], []
    state = {
        "rows": rows,
        "build": build,
        "reference_full_mappings": reference,
        "reference_calls": calls,
        "complete": False,
    }
    if progress is not None:
        progress(state)
    for query in declaration["queries"]:
        reference_rows = []
        reference[query["key"]] = reference_rows
        for record in records:
            state["current_operation"] = {
                "phase": "exhaustive",
                "query": query["key"],
                "source_key": record["source_key"],
                "occurrence_key": record["occurrence_key"],
            }
            actual = reference_proposals(query, record)
            calls["exhaustive"] += 1
            if query["oracle"] == "exact-interior":
                assert actual == exact_mapping_oracle(query, record), (
                    query["key"],
                    record["occurrence_key"],
                )
                oracle_comparisons += 1
            reference_rows.append(actual)
        if progress is not None:
            progress(state)
    for width in declaration["bin_widths"]:
        settings = binding(declaration, width)
        index = StudyIndex(records, settings)
        build.append(
            {
                "width": width,
                "original_records": len(records),
                "pair_entries": index.pair_entries,
                "asset_identity": index.identity,
            }
        )
        for query in declaration["queries"]:
            state["current_operation"] = {
                "phase": "retrieval",
                "query": query["key"],
                "width": width,
            }
            lookup = index.lookup(
                query, current_records=records, current_binding=settings
            )
            assert lookup["complete"]
            actual = [[] for _ in records]
            for ordinal in lookup["candidate_ordinals"]:
                actual[ordinal] = reference_proposals(query, records[ordinal])
                calls["retrieved"] += 1
            assert actual == reference[query["key"]], (query["key"], width)
            exact = index.lookup(
                query, current_records=records, current_binding=settings, exact_bin=True
            )
            misses = [
                i
                for i, mappings in enumerate(reference[query["key"]])
                if mappings and i not in exact["candidate_ordinals"]
            ]
            rows.append(
                {
                    "query": query["key"],
                    "width": width,
                    "lookup": lookup,
                    "exact_bin_lookup": exact,
                    "exact_bin_missing_positive_ordinals": misses,
                    "original_full_mappings": actual,
                    "equal_exhaustive": True,
                }
            )
            if progress is not None:
                progress(state)
    cross = next(
        r for r in rows if r["query"] == "cross-bin-feasible" and r["width"] == 1
    )
    cross_id = next(
        i
        for i, r in enumerate(records)
        if r["occurrence_key"] == "source:cross-bin-feasible"
    )
    assert cross_id in cross["exact_bin_missing_positive_ordinals"]
    ordinary = next(r for r in rows if r["query"] == "identity" and r["width"] == 1)
    impossible_id = next(
        i
        for i, r in enumerate(records)
        if r["occurrence_key"] == "source:same-bin-impossible"
    )
    assert (
        impossible_id in ordinary["lookup"]["candidate_ordinals"]
        and not ordinary["original_full_mappings"][impossible_id]
    )
    state.update(
        complete=True, independent_exact_mapping_comparisons=oracle_comparisons
    )
    return {
        **state,
        "rows": rows,
        "build": build,
        "original_source_occurrence_keys": [
            [r["source_key"], r["occurrence_key"]] for r in records
        ],
        "reference_full_mappings": reference,
        "reference_calls": calls,
        "independent_exact_mapping_comparisons": oracle_comparisons,
        "all_conservative_mappings_equal_exhaustive": True,
        "original_occurrences_and_mappings_preserved": True,
        "exact_bin_negative_control_misses": True,
        "same_bin_false_positive_is_filtered_by_reference": True,
        "molecular_inputs": 0,
        "final_pose_or_activity_acceptance": False,
        "performance_measured": False,
    }
