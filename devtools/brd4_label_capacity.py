"""Offline, case-specific capacity projection for the declared BRD4 assay plan.

The caller owns HTTP receiving and before/after descriptor checks. This tool
requires an explicitly reviewed CSV layout rather than inferring metadata rows
or endpoint aliases. It returns aggregate facts only; original assay rows remain
in the caller's private receiving capsule. No molecular identity is inferred.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

PLAN_SHA256 = "079f2b6652f17c292ca41e7eba04b3e9c2404e9c4a2f067b4ddd92669d95d718"
PLAN_PATH = (
    Path(__file__).resolve().parents[1]
    / "devguide/evidence/brd4_activity_capacity_plan_20261106.json"
)
EXPECTED_SIDS = 499
EXPECTED_CIDS = 494
MINIMUM_PER_CLASS = 50
EXPECTED_COLUMNS = {
    "sid": "PUBCHEM_SID",
    "cid": "PUBCHEM_CID",
    "type": "Standard Type",
    "relation": "Standard Relation",
    "value": "PubChem Standard Value",
}
CLASSES = ("strong", "intermediate", "weak")
STATUSES = (
    *CLASSES,
    "class_ambiguous",
    "missing",
    "invalid",
    "unsupported_type",
    "unsupported_relation",
)
NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
IDENTIFIER = re.compile(r"[1-9][0-9]*")


def classify_ic50(standard_type: str, relation: str, value: str) -> str:
    """Classify one complete positive IC50 interval, in declared micromolar.

    Decimal parsing and comparisons retain exact reported boundaries. Missing,
    invalid or unsupported fields never become a biological negative. Values
    must be source strings; there is no float conversion or bound imputation.
    """
    if any(field is None or field == "" for field in (standard_type, relation, value)):
        return "missing"
    if not all(isinstance(field, str) for field in (standard_type, relation, value)):
        return "invalid"
    standard_type, relation, value = (
        field.strip() for field in (standard_type, relation, value)
    )
    if not all((standard_type, relation, value)):
        return "missing"
    if standard_type != "IC50":
        return "unsupported_type"
    if relation not in {"=", "<", "<=", ">", ">="}:
        return "unsupported_relation"
    if not NUMBER.fullmatch(value):
        return "invalid"
    try:
        potency = Decimal(value)
    except InvalidOperation:
        return "invalid"
    if not potency.is_finite() or potency <= 0:
        return "invalid"
    strong_max, weak_min = Decimal("0.5"), Decimal("5")
    if relation == "=":
        if potency <= strong_max:
            return "strong"
        return "weak" if potency > weak_min else "intermediate"
    if relation in {"<", "<="}:
        return "strong" if potency <= strong_max else "class_ambiguous"
    if relation == ">":
        return "weak" if potency >= weak_min else "class_ambiguous"
    return "weak" if potency > weak_min else "class_ambiguous"


@dataclass(frozen=True)
class CsvLayout:
    """Exact observed header/preamble and explicit semantic column indices.

    Construct this only after the receiving caller has reviewed descriptor
    semantics and the complete CSV header/preamble. No metadata row is guessed
    or silently skipped. All column indices refer to the same source header.
    """

    header: tuple[str, ...]
    columns: dict[str, int]
    metadata_rows: tuple[tuple[str, ...], ...] = ()

    def __post_init__(self):
        if (
            not self.header
            or not all(isinstance(name, str) and name for name in self.header)
            or len(set(self.header)) != len(self.header)
        ):
            raise ValueError("CSV layout requires nonempty unique header names")
        if set(self.columns) != set(EXPECTED_COLUMNS):
            raise ValueError(
                "CSV layout requires exactly the five declared column roles"
            )
        for role, expected_name in EXPECTED_COLUMNS.items():
            index = self.columns[role]
            if (
                type(index) is not int
                or index < 0
                or index >= len(self.header)
                or self.header[index] != expected_name
            ):
                raise ValueError(
                    f"CSV column mapping does not identify declared {role}"
                )
        if any(
            len(row) != len(self.header)
            or not all(isinstance(value, str) for value in row)
            for row in self.metadata_rows
        ):
            raise ValueError(
                "CSV layout metadata rows must have the exact header width"
            )

    @classmethod
    def from_dict(cls, payload: dict) -> CsvLayout:
        if not isinstance(payload, dict) or set(payload) != {
            "header",
            "columns",
            "metadata_rows",
        }:
            raise ValueError("CSV layout needs header, columns and metadata_rows only")
        if not isinstance(payload["header"], list) or not isinstance(
            payload["columns"], dict
        ):
            raise ValueError("CSV layout header/columns have invalid types")
        if not isinstance(payload["metadata_rows"], list) or any(
            not isinstance(row, list) for row in payload["metadata_rows"]
        ):
            raise ValueError(
                "CSV layout metadata_rows must be an explicit list of rows"
            )
        return cls(
            tuple(payload["header"]),
            dict(payload["columns"]),
            tuple(tuple(row) for row in payload["metadata_rows"]),
        )


def _identifier(value: str, *, allow_missing: bool = False) -> str | None:
    if value == "" and allow_missing:
        return None
    if not IDENTIFIER.fullmatch(value):
        raise ValueError("CSV data has a missing or malformed source identifier")
    return value


def project_csv(text: str, layout: CsvLayout) -> dict:
    """Return the fixed plan's complete-coverage, aggregate-only projection.

    Every data row is retained in the accounting. A SID contributes at most
    once, and only when all its rows have the same definite strong/weak label
    and the same CID. Mixed labels/statuses remain excluded and counted. This
    conservative eligibility rule makes no choice of a favorable duplicate.

    Exact source totals are a gate, not proof of row provenance or molecular
    independence. A successful capacity projection permits further admission;
    it accepts neither a cohort nor a predictive scientific result.
    """
    # Revalidate the explicit mapping if its caller-owned dictionary was edited.
    layout.__post_init__()
    reader = csv.reader(io.StringIO(text, newline=""), strict=True)
    if tuple(next(reader, ())) != layout.header:
        raise ValueError("CSV header differs from the explicitly reviewed layout")
    for expected in layout.metadata_rows:
        if tuple(next(reader, ())) != expected:
            raise ValueError("CSV metadata differs from the explicitly reviewed layout")
    statuses = Counter({name: 0 for name in STATUSES})
    groups = defaultdict(list)
    cids = set()
    missing_cid_rows = 0
    for row in reader:
        if len(row) != len(layout.header):
            raise ValueError("CSV data row width differs from the reviewed header")
        sid = _identifier(row[layout.columns["sid"]])
        cid = _identifier(row[layout.columns["cid"]], allow_missing=True)
        if cid is None:
            missing_cid_rows += 1
        else:
            cids.add(cid)
        status = classify_ic50(
            row[layout.columns["type"]],
            row[layout.columns["relation"]],
            row[layout.columns["value"]],
        )
        statuses[status] += 1
        groups[sid].append((cid, status))
    if len(groups) != EXPECTED_SIDS or len(cids) != EXPECTED_CIDS:
        raise ValueError("CSV coverage differs from the declared 499 SIDs/494 CIDs")
    bounds = {"strong": 0, "weak": 0}
    sid_statuses = Counter({name: 0 for name in STATUSES})
    conflicting_labels = conflicting_cids = mixed_statuses = duplicate_sids = 0
    for observations in groups.values():
        labels = {status for _, status in observations}
        identifiers = {cid for cid, _ in observations}
        duplicate_sids += len(observations) > 1
        conflicting_labels += len(labels.intersection(CLASSES)) > 1
        conflicting_cids += len(identifiers) > 1
        mixed_statuses += len(labels) > 1
        if len(labels) == 1:
            label = next(iter(labels))
            sid_statuses[label] += 1
            if label in bounds and len(identifiers) == 1 and None not in identifiers:
                bounds[label] += 1
    passes = all(count >= MINIMUM_PER_CLASS for count in bounds.values())
    return {
        "schema": "pharmacophoremt.brd4-label-capacity-projection@1",
        "plan_sha256": PLAN_SHA256,
        "source_aid": 1805333,
        "scope": "Necessary raw label capacity only; no cohort or molecular admission",
        "rows": sum(statuses.values()),
        "distinct_sids": len(groups),
        "distinct_cids": len(cids),
        "missing_cid_rows": missing_cid_rows,
        "row_status_counts": dict(statuses),
        "uniform_sid_status_counts": dict(sid_statuses),
        "duplicate_sids": duplicate_sids,
        "extra_duplicate_rows": sum(len(rows) - 1 for rows in groups.values()),
        "conflicting_label_sids": conflicting_labels,
        "conflicting_cid_sids": conflicting_cids,
        "mixed_status_sids": mixed_statuses,
        "eligible_sid_upper_bounds": bounds,
        "minimum_per_class": MINIMUM_PER_CLASS,
        "duplicate_rule": (
            "Contribute once only when every row has the same definite class and CID; "
            "exclude mixed, unresolved or conflicting observations"
        ),
        "decision": (
            "capacity_permits_further_admission"
            if passes
            else "stop_insufficient_raw_capacity"
        ),
        "independent_groups_qualified": False,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path, help="Private received CSV; never printed")
    parser.add_argument("layout", type=Path, help="Explicitly reviewed CSV layout JSON")
    args = parser.parse_args(argv)
    if hashlib.sha256(PLAN_PATH.read_bytes()).hexdigest() != PLAN_SHA256:
        raise ValueError("The case's immutable activity-capacity plan has changed")
    source_limit = 2 * 1024 * 1024
    with args.csv.open("rb") as source:
        raw = source.read(source_limit + 1)
    if len(raw) > source_limit:
        raise ValueError("CSV exceeds the declared two-MiB source-response limit")
    layout_bytes = args.layout.read_bytes()
    layout = CsvLayout.from_dict(json.loads(layout_bytes))
    result = project_csv(raw.decode("utf-8-sig"), layout)
    result["csv_sha256"] = hashlib.sha256(raw).hexdigest()
    result["layout_sha256"] = hashlib.sha256(layout_bytes).hexdigest()
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
