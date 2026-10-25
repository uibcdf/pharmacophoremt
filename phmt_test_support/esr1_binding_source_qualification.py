"""Apply #66's committed study thresholds to saved source activity tables.

This case consumer uses only tabular source records. It neither interprets
molecular structures nor acquires another source after the fixed pool stops.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tests/data/esr1_binding_evaluation/source_qualification_20261024"
PROTOCOL_COMMIT = "acfbe85b812eb6bd32f9682ac2fd86824ebeaff9"
ASSAYS = (("CHEMBL3382763", "CHEMBL3352633"), ("CHEMBL3705057", "CHEMBL3638543"))
ENDPOINTS = ("Ki", "Kd", "IC50")
spec = importlib.util.spec_from_file_location(
    "binding_source_readiness", Path(__file__).with_name("esr1_binding_readiness.py")
)
readiness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(readiness)


def classify(row):
    """Return this study's class/reasons, retaining unresolved evidence explicitly."""
    reasons = []
    quality = ("standard_flag", "potential_duplicate", "data_validity_comment")
    if not all(key in row for key in quality):
        reasons.append("missing_quality_fields")
    if type(row.get("standard_flag")) is not int or row["standard_flag"] != 1:
        reasons.append("not_standardized")
    if (
        type(row.get("potential_duplicate")) is not int
        or row["potential_duplicate"] != 0
    ):
        reasons.append("duplicate_or_unknown_duplicate_status")
    if row.get("data_validity_comment") not in (None, ""):
        reasons.append("data_validity_comment")
    if row.get("standard_type") not in ENDPOINTS:
        reasons.append("unsupported_endpoint")
    if row.get("standard_units") != "nM":
        reasons.append("unsupported_or_missing_units")
    try:
        value = Decimal(str(row.get("standard_value")))
        if not value.is_finite() or value <= 0:
            raise InvalidOperation
    except InvalidOperation:
        value = None
        reasons.append("missing_or_invalid_value")
    relation = row.get("standard_relation")
    if relation not in ("=", "<", "<=", ">", ">="):
        reasons.append("unsupported_or_missing_relation")
    if reasons:
        return None, reasons
    if relation in ("=", "<", "<=") and value <= 1000:
        return 1, []
    if relation in ("=", ">", ">=") and value >= 10000:
        return 0, []
    return None, ["intermediate_or_insufficient_bound"]


def assess_rows(rows):
    """Keep all rows and classify source identifiers separately per endpoint."""
    ledger, groups = [], defaultdict(list)
    activity_ids = set()
    for row in rows:
        identifier, activity_id = row.get("molecule_chembl_id"), row.get("activity_id")
        if (
            not isinstance(identifier, str)
            or not identifier
            or type(activity_id) is not int
            or activity_id in activity_ids
        ):
            raise ValueError(
                "missing source identifier or duplicate/invalid activity ID"
            )
        activity_ids.add(activity_id)
        label, reasons = classify(row)
        entry = {"source": deepcopy(row), "label": label, "reasons": reasons}
        ledger.append(entry)
        groups[(row.get("standard_type"), identifier)].append(entry)
    endpoints = {}
    for endpoint in ENDPOINTS:
        records = []
        for (kind, identifier), observations in groups.items():
            if kind != endpoint:
                continue
            labels = {entry["label"] for entry in observations}
            resolved = len(labels) == 1 and None not in labels
            records.append(
                {
                    "source_identifier": identifier,
                    "activity_ids": [
                        entry["source"]["activity_id"] for entry in observations
                    ],
                    "label": next(iter(labels)) if resolved else None,
                    "reason": None
                    if resolved
                    else "conflicting_or_unresolved_relevant_observation",
                }
            )
        counts = Counter(r["label"] for r in records)
        endpoints[endpoint] = {
            "source_identifiers": records,
            "n_identifiers": len(records),
            "n_positive_identifiers": counts[1],
            "n_weak_identifiers": counts[0],
            "n_unclassified_identifiers": counts[None],
            "population_upper_bound_passes": counts[1] >= 20 and counts[0] >= 20,
            "scope": "literal source identifiers before molecular equivalence, old-CID exclusions or scaffold audit",
        }
    return {"n_rows": len(rows), "ledger": ledger, "endpoints": endpoints}


def execute():
    acquisition_path = DATA / "activity_acquisition.json"
    acquisition = json.loads(acquisition_path.read_text())
    if acquisition["protocol_source"] != PROTOCOL_COMMIT:
        raise ValueError("activity acquisition predates the declared protocol")
    requests = {row["file"]: row for row in acquisition["requests"]}
    if len(requests) != 2 or len(acquisition["requests"]) != 2:
        raise ValueError("expected exactly the two complete saved assay pages")
    assessments = {}
    for assay, document in ASSAYS:
        name = f"{assay}.activities.page0.json"
        raw = (DATA / name).read_bytes()
        item = requests[name]
        if readiness.identity(DATA / name) != {
            key: item[key] for key in ("sha256", "byte_count")
        }:
            raise ValueError("activity source bytes changed")
        obj = json.loads(raw)
        page, rows = obj["page_meta"], obj["activities"]
        if (
            page["offset"] != 0
            or page["next"] is not None
            or page["previous"] is not None
            or len(rows) != page["total_count"]
        ):
            raise ValueError("incomplete activity acquisition")
        if any(
            r.get("assay_chembl_id") != assay
            or r.get("document_chembl_id") != document
            or r.get("target_chembl_id") != "CHEMBL206"
            for r in rows
        ):
            raise ValueError("wrong assay/document/target in source table")
        assessments[assay] = assess_rows(rows)
    any_population = any(
        e["population_upper_bound_passes"]
        for a in assessments.values()
        for e in a["endpoints"].values()
    )
    return {
        "schema": "pharmacophoremt.esr1_binding_source_qualification@1",
        "issue": 66,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "protocol_source": PROTOCOL_COMMIT,
        "producer": {
            "git_head": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "git_status": subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=ROOT, text=True
            ),
            "python": sys.version,
            "executable": sys.executable,
            "driver": readiness.identity(Path(__file__)),
        },
        "acquisition": {
            "path": str(acquisition_path.relative_to(ROOT)),
            **readiness.identity(acquisition_path),
        },
        "assessments": assessments,
        "new_exposed_source_identifiers": sorted(
            {
                row["source"]["molecule_chembl_id"]
                for assessment in assessments.values()
                for row in assessment["ledger"]
            }
        ),
        "exposure_scope": "literal ChEMBL identifiers; aliases and molecular equivalence remain provider-owned",
        "readiness": "needs_remaining_gates" if any_population else "stopped",
        "terminal_stop": not any_population,
        "stop_reason": None
        if any_population
        else "predeclared_source_pool_exhausted_insufficient_class_counts",
        "evaluation_cohort": None,
        "new_molecular_inputs_acquired": False,
        "new_scores_computed": False,
        "scope": "source/label feasibility only; no molecular identity or independence inferred; no scoring route",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    report = execute()
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(report, handle, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "readiness": report["readiness"],
                "terminal_stop": report["terminal_stop"],
            }
        )
    )


if __name__ == "__main__":
    main()
