"""Metadata-only #66 review; no activity, structure or molecular calculation route."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "tests/data/esr1_binding_evaluation/source_inventory.json"
spec = importlib.util.spec_from_file_location(
    "binding_readiness_archive_reader", Path(__file__).with_name("evidence_archive.py")
)
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


def identity(path):
    raw = path.read_bytes()
    return {"sha256": hashlib.sha256(raw).hexdigest(), "byte_count": len(raw)}


def historical_exclusions():
    """Collect literal IDs from complete historical source tables, without chemistry."""
    manifest_path = ROOT / "tests/data/esr1_activity_pilot/manifest.json"
    manifest = json.loads(manifest_path.read_text())
    snapshot_path = (
        ROOT / "devguide/evidence/esr1_activity_pilot_inputs_20261023_summary.json"
    )
    summary, raw = reader.read_archived_bytes(snapshot_path)
    if identity(manifest_path)["sha256"] != summary["input_manifest_sha256"]:
        raise ValueError("historical manifest identity changed")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as outer:
        payloads = {
            key: outer.extractfile(manifest[key]["file"]).read()
            for key in ("source", "assay")
        }
    for key, data in payloads.items():
        if hashlib.sha256(data).hexdigest() != manifest[key]["sha256"]:
            raise ValueError("historical source bytes changed")
    with tarfile.open(fileobj=io.BytesIO(payloads["source"])) as bath:
        bath_rows = list(
            csv.DictReader(
                io.TextIOWrapper(bath.extractfile("ESR1ago/ESR1ago_data_full.csv"))
            )
        )
    assay_rows = list(csv.DictReader(io.StringIO(payloads["assay"].decode())))
    bath_ids = {r["PUBCHEM_CID"] for r in bath_rows if r["PUBCHEM_CID"]}
    assay_ids = {r["CID"] for r in assay_rows if r["CID"]}
    cids = bath_ids | assay_ids
    if any(not cid.isdecimal() or int(cid) < 1 for cid in cids):
        raise ValueError("historical source has an unsupported nonempty CID")
    prior = {}
    for name, relative in (
        ("pilot", "tests/data/esr1_activity_pilot/manifest.json"),
        (
            "original_comparison",
            "tests/data/esr1_consensus_comparison/declaration.json",
        ),
        (
            "readiness_comparison",
            "tests/data/esr1_consensus_comparison/readiness_declaration.json",
        ),
    ):
        path = ROOT / relative
        requested = {row["cid"] for row in json.loads(path.read_text())["cohort"]}
        if not requested <= cids:
            raise ValueError(
                "prior requested inputs escaped the historical source universe"
            )
        prior[name] = {
            "path": relative,
            **identity(path),
            "distinct_requested_cids": len(requested),
        }
    return {
        "scope": "literal external CID exclusion only; no molecular equivalence or scaffold inference",
        "snapshot": {
            "path": str(snapshot_path.relative_to(ROOT)),
            **identity(snapshot_path),
        },
        "source_archive": summary["full_evidence"],
        "bath_rows": len(bath_rows),
        "bath_distinct_cids": len(bath_ids),
        "assay_rows": len(assay_rows),
        "assay_distinct_valid_cids": len(assay_ids),
        "assay_blank_cid_rows": sum(not r["CID"] for r in assay_rows),
        "unresolved_source_rows": [
            {"row_index": index, "sid": row["SID"]}
            for index, row in enumerate(assay_rows)
            if not row["CID"]
        ],
        "n_excluded_cids": len(cids),
        "cids": sorted(cids, key=int),
        "prior_requests": prior,
    }


def review(metadata_dir):
    """Verify frozen responses and report source readiness without acquiring data."""
    inventory = json.loads(INVENTORY.read_text())
    responses = {}
    for item in inventory["responses"]:
        path = metadata_dir / item["file"]
        if identity(path) != {k: item[k] for k in ("sha256", "byte_count")}:
            raise ValueError(f"metadata changed: {item['file']}")
        responses[item["file"]] = json.loads(path.read_bytes())
    pages = [
        responses[name]
        for name in (
            "chembl_human_binding_assays.json",
            "chembl_human_binding_assays_page2.json",
        )
    ]
    rows = [row for page in pages for row in page["assays"]]
    if (
        pages[0]["page_meta"]["offset"] != 0
        or pages[1]["page_meta"]["offset"] != len(pages[0]["assays"])
        or not pages[0]["page_meta"]["next"]
        or pages[1]["page_meta"]["next"] is not None
        or any(p["page_meta"]["total_count"] != len(rows) for p in pages)
        or len({r["assay_chembl_id"] for r in rows}) != len(rows)
    ):
        raise ValueError("incomplete or duplicate ChEMBL discovery metadata")
    if any(
        r["assay_type"] != "B"
        or r["confidence_score"] != 9
        or r["assay_organism"] != "Homo sapiens"
        for r in rows
    ):
        raise ValueError("metadata disagrees with the declared source filter")
    projections = []
    for row in responses["assay_summaries.json"]["AssaySummaries"]["AssaySummary"]:
        projections.append(
            {
                key: value
                for key, value in row.items()
                if key.startswith(("CIDCount", "SIDCount"))
                or key
                in {
                    "AID",
                    "Version",
                    "Revision",
                    "LastDataChange",
                    "SourceName",
                    "SourceID",
                }
            }
        )
    nominees = [
        responses[f"{name}.assay.json"] for name in ("CHEMBL3382763", "CHEMBL3705057")
    ]
    plan_path = ROOT / "devguide/esr1_binding_evaluation_plan.md"
    return {
        "schema": "pharmacophoremt.esr1_binding_metadata_review@1",
        "issue": 66,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "producer": {
            "git_head": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "git_status": subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=ROOT, text=True
            ),
            "python": sys.version,
            "executable": sys.executable,
            "driver": identity(Path(__file__)),
        },
        "source_inventory": {
            "path": str(INVENTORY.relative_to(ROOT)),
            **identity(INVENTORY),
        },
        "protocol": {"path": str(plan_path.relative_to(ROOT)), **identity(plan_path)},
        "raw_metadata_retained_at": str(metadata_dir.resolve()),
        "raw_metadata_portable": False,
        "pubchem_metadata": projections,
        "chembl": {
            "status": responses["chembl_status.json"],
            "discovery_records": len(rows),
            "discovery_pages": len(pages),
            "complete_pagination": True,
            "nominees": [
                {
                    key: r[key]
                    for key in (
                        "assay_chembl_id",
                        "description",
                        "assay_type",
                        "assay_organism",
                        "confidence_score",
                        "bao_format",
                        "document_chembl_id",
                        "target_chembl_id",
                        "variant_sequence",
                    )
                }
                for r in nominees
            ],
        },
        "historical_exclusions": historical_exclusions(),
        "stage": "metadata_review_only",
        "evaluation_cohort": None,
        "new_individual_activities_acquired": False,
        "new_molecular_inputs_acquired": False,
        "new_scores_computed": False,
        "readiness": "not_ready",
        "remaining_gates": [
            "experimental endpoint and activity-schema qualification",
            "provider-owned identity/scaffold and source-ID correspondence",
            "source rights and exact cohort declaration",
            "molecular coordinate/state readiness before scoring",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = review(args.metadata_dir)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, sort_keys=True, indent=2, allow_nan=False)
        handle.write("\n")
    print(
        json.dumps(
            {
                "output": str(args.output),
                "readiness": result["readiness"],
                "excluded_cids": result["historical_exclusions"]["n_excluded_cids"],
            }
        )
    )


if __name__ == "__main__":
    main()
