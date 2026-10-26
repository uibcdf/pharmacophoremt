"""Bounded #66 pool-2 acquisition and offline source-population review."""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import urllib.error
import urllib.parse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECLARATION = (
    ROOT / "tests/data/esr1_binding_evaluation/pool2_declaration_20261026.json"
)
FIELDS = "activity_id,assay_chembl_id,molecule_chembl_id,standard_type,standard_relation,standard_value,standard_units,standard_flag,data_validity_comment,potential_duplicate,document_chembl_id,target_chembl_id,activity_comment"


def _module(name, filename):
    spec = importlib.util.spec_from_file_location(
        name, Path(__file__).with_name(filename)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


source = _module("pool2_source_classifier", "esr1_binding_source_qualification.py")
pilot = _module("pool2_existing_fetch", "esr1_activity_pilot.py")


def capacity_total(payload):
    """Validate the declared ID-only projection; unknown is never a zero total."""
    page, rows = payload["page_meta"], payload["activities"]
    total = page["total_count"]
    if (
        type(total) is not int
        or total < 0
        or page["offset"] != 0
        or page["previous"] is not None
        or len(rows) != min(total, 1)
        or bool(page["next"]) != (total > 1)
        or any(
            set(r) != {"activity_id"}
            or type(r["activity_id"]) is not int
            or r["activity_id"] < 1
            for r in rows
        )
    ):
        raise ValueError(
            "invalid capacity metadata or unexpected activity-value exposure"
        )
    return total


def select_details(totals, declaration):
    """Choose by complete raw capacity before observing any class values."""
    expected = {r["assay_chembl_id"] for r in declaration["nominees"]}
    if set(totals) != expected or any(
        type(v) is not int or v < 0 for v in totals.values()
    ):
        raise ValueError("every declared capacity must resolve before ranking")
    eligible = sorted(
        (
            key
            for key, total in totals.items()
            if total >= declaration["capacity"]["minimum_total_records"]
        ),
        key=lambda key: (-totals[key], int(key[6:])),
    )
    count = declaration["detailed_selection"]["maximum_assays"]
    return eligible[:count], eligible[count:]


def _producer():
    return {
        "git_head": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "git_status": subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=ROOT, text=True
        ),
        "python": sys.version,
        "driver": source.readiness.identity(Path(__file__)),
    }


def _url(assay, capacity):
    return (
        "https://www.ebi.ac.uk/chembl/api/data/activity.json?"
        + urllib.parse.urlencode(
            {
                "assay_chembl_id": assay,
                "limit": 1 if capacity else 1000,
                "order_by": "activity_id",
                "only": "activity_id" if capacity else FIELDS,
            }
        )
    )


def acquire(directory):
    """Reuse the existing fetch helper; journal original successes and failures."""
    declaration = json.loads(DECLARATION.read_text())
    directory.mkdir(parents=True, exist_ok=False)
    journal = {
        "schema": "pharmacophoremt.esr1_binding_pool2_acquisition@1",
        "declaration": source.readiness.identity(DECLARATION),
        "producer": _producer(),
        "requests": [],
        "phase": "capacity",
    }

    def save():
        (directory / "acquisition.json").write_text(
            json.dumps(journal, indent=2, sort_keys=True) + "\n"
        )

    def request(url, filename, phase, assay=None):
        record = {
            "url": url,
            "file": filename,
            "phase": phase,
            "assay": assay,
            "started_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            raw = pilot.fetch(url, directory / filename)
            record.update(
                status="completed", **source.readiness.identity(directory / filename)
            )
            return json.loads(raw)
        except Exception as error:
            record.update(
                status="failed", error_type=type(error).__name__, message=str(error)
            )
            if isinstance(error, urllib.error.HTTPError):
                error_path = directory / (filename + ".http-error")
                error_path.write_bytes(error.read())
                record["http_error"] = {
                    "code": error.code,
                    "file": error_path.name,
                    **source.readiness.identity(error_path),
                }
            raise
        finally:
            record["finished_at"] = datetime.now(timezone.utc).isoformat()
            journal["requests"].append(record)
            save()

    save()
    try:
        status = request(
            "https://www.ebi.ac.uk/chembl/api/data/status.json", "status.json", "status"
        )
        if status["chembl_db_version"] != "ChEMBL_37":
            raise ValueError("source version changed; declare a new discovery snapshot")
        totals = {}
        for row in declaration["nominees"]:
            assay = row["assay_chembl_id"]
            totals[assay] = capacity_total(
                request(_url(assay, True), f"{assay}.capacity.json", "capacity", assay)
            )
        selected, deferred = select_details(totals, declaration)
        journal.update(
            totals=totals, selected=selected, deferred=deferred, phase="details"
        )
        save()
        for assay in selected:
            if (
                totals[assay]
                > declaration["detailed_selection"]["maximum_records_per_assay"]
            ):
                raise ValueError(
                    "selected source exceeds declared budget; no replacement"
                )
            url, offset, page_index = _url(assay, False), 0, 0
            while url:
                obj = request(
                    url, f"{assay}.activities.{page_index}.json", "details", assay
                )
                page = obj["page_meta"]
                if (
                    page["total_count"] != totals[assay]
                    or page["offset"] != offset
                    or not obj["activities"]
                ):
                    raise ValueError("incomplete or changed selected source")
                offset += len(obj["activities"])
                next_url = page["next"]
                if next_url and not next_url.startswith(
                    "/chembl/api/data/activity.json?"
                ):
                    raise ValueError("unexpected pagination URL")
                url = "https://www.ebi.ac.uk" + next_url if next_url else None
                page_index += 1
                if page_index > 5:
                    raise ValueError("selected source exceeded page budget")
            if offset != totals[assay]:
                raise ValueError("selected source lacks complete rows")
        journal["phase"] = "completed"
    except Exception as error:
        journal.update(
            phase="stopped_acquisition",
            error_type=type(error).__name__,
            message=str(error),
        )
    save()
    return journal


def summarize(directory):
    """Revalidate saved responses and reuse the unchanged source classifier."""
    declaration = json.loads(DECLARATION.read_text())
    journal = json.loads((directory / "acquisition.json").read_text())
    if journal["declaration"] != source.readiness.identity(DECLARATION):
        raise ValueError("acquisition used a different declaration")
    payloads = {}
    for row in journal["requests"]:
        if row["status"] == "completed":
            if source.readiness.identity(directory / row["file"]) != {
                k: row[k] for k in ("sha256", "byte_count")
            }:
                raise ValueError("saved source bytes changed")
            payloads[row["file"]] = json.loads((directory / row["file"]).read_bytes())
    totals, invalid_capacity = {}, {}
    exposed = set()
    for row in journal["requests"]:
        if row["status"] != "completed":
            continue
        for activity in payloads[row["file"]].get("activities", []):
            identifier = activity.get("molecule_chembl_id")
            if isinstance(identifier, str):
                exposed.add(identifier)
        if row["phase"] == "capacity":
            try:
                totals[row["assay"]] = capacity_total(payloads[row["file"]])
            except (KeyError, TypeError, ValueError) as error:
                invalid_capacity[row["file"]] = str(error)
    selected, deferred = (
        select_details(totals, declaration)
        if journal["phase"] == "completed"
        else ([], [])
    )
    _, prior = source.readiness.reader.read_archived_evidence(
        ROOT
        / "devguide/evidence/esr1_binding_source_qualification_20261024_summary.json"
    )
    excluded = set(prior["new_exposed_source_identifiers"])
    assessments = {}
    for assay in selected:
        rows = [
            r
            for request in journal["requests"]
            if request["phase"] == "details" and request["assay"] == assay
            for r in payloads[request["file"]]["activities"]
        ]
        document = next(
            r["document_chembl_id"]
            for r in declaration["nominees"]
            if r["assay_chembl_id"] == assay
        )
        if len(rows) != totals[assay] or any(
            r.get("assay_chembl_id") != assay
            or r.get("document_chembl_id") != document
            or r.get("target_chembl_id") != "CHEMBL206"
            for r in rows
        ):
            raise ValueError("selected rows disagree with source scope/completeness")
        assessment = source.assess_rows(rows)
        for endpoint in assessment["endpoints"].values():
            records = endpoint["source_identifiers"]
            labels = Counter(
                r["label"] for r in records if r["source_identifier"] not in excluded
            )
            endpoint["prior_exposed_identifiers"] = [
                r["source_identifier"]
                for r in records
                if r["source_identifier"] in excluded
            ]
            endpoint["new_identifier_upper_bound"] = {
                "positive": labels[1],
                "weak": labels[0],
                "unclassified": labels[None],
                "passes": labels[1] >= 20 and labels[0] >= 20,
            }
        assessments[assay] = assessment
        exposed.update(r["molecule_chembl_id"] for r in rows)
    numerical = [
        assay
        for assay in selected
        if any(
            e["new_identifier_upper_bound"]["passes"]
            for e in assessments[assay]["endpoints"].values()
        )
    ]
    return {
        "schema": "pharmacophoremt.esr1_binding_pool2_review@1",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "producer": _producer(),
        "declaration": source.readiness.identity(DECLARATION),
        "acquisition": source.readiness.identity(directory / "acquisition.json"),
        "acquisition_phase": journal["phase"],
        "capacity_totals": totals,
        "invalid_capacity": invalid_capacity,
        "selected": selected,
        "deferred_capacity_survivors": deferred,
        "assessments": assessments,
        "numerical_survivors": numerical,
        "newly_inspected_chembl_identifiers": sorted(exposed),
        "previously_exposed_chembl_identifiers": sorted(excluded),
        "readiness": "acquisition_unresolved"
        if journal["phase"] != "completed"
        else "requires_experimental_and_molecular_gates"
        if numerical
        else "selected_detail_pool_stopped",
        "evaluation_cohort": None,
        "new_molecular_inputs_acquired": False,
        "new_scores_computed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--acquire", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and args.output.exists():
        raise FileExistsError(args.output)
    if args.acquire:
        journal = acquire(args.data_dir)
        print(
            json.dumps(
                {
                    "phase": journal["phase"],
                    "requests": len(journal["requests"]),
                    "message": journal.get("message"),
                }
            )
        )
    if args.output:
        report = summarize(args.data_dir)
        with args.output.open("x") as output:
            json.dump(report, output, indent=2, sort_keys=True, allow_nan=False)
            output.write("\n")
        print(
            json.dumps(
                {
                    "readiness": report["readiness"],
                    "selected": report["selected"],
                    "numerical_survivors": report["numerical_survivors"],
                }
            )
        )


if __name__ == "__main__":
    main()
