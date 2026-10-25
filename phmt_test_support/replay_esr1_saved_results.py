"""Derive native summaries from immutable #64 evidence, without molecular work.

Run from the checkout with python -m phmt_test_support.replay_esr1_saved_results
--output /new/path.json. This is a new derived verification, not a rerun or a
replacement of the original evaluation. Source acquisition/search is never run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

from phmt_test_support.evidence_archive import read_archived_evidence

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "devguide/evidence/esr1_paired_evaluation_20261024_summary.json"


def replay(summary_path=SOURCE):
    """Return detached new statistics plus explicit assertions against #64."""
    import pharmacophoremt as phmt
    from pharmacophoremt.validation import compare_screening_results

    envelope, source = read_archived_evidence(summary_path)
    source_before = json.dumps(source, sort_keys=True, allow_nan=False)
    cohort = [
        {
            "input_index": r["cohort_index"],
            "label": r["label"],
            "cid": r["cid"],
            "sid": r["sid"],
        }
        for r in source["records"]
    ]
    arms = {}
    for name in ("baseline", "consensus"):
        native = source["arms"][name]["native_prepared_input_report"]
        arms[name] = {
            "evaluations": native["evaluations"],
            "input_mapping": [
                {
                    "native_input_index": r["arms"][name]["native_input_index"],
                    "input_index": r["cohort_index"],
                }
                for r in source["records"]
                if r["arms"][name]["native_evaluation"] is not None
            ],
            "score_method": "seeded_hit",
            "unscored": [
                {
                    "input_index": r["cohort_index"],
                    "stage": r["arms"][name]["stage"],
                    "reason": r["preparation"]["message"],
                    "acquisition": r["acquisition"],
                }
                for r in source["records"]
                if r["arms"][name]["native_evaluation"] is None
            ],
            "source_metadata": {
                "producer": source["producer"],
                "attribution": source["attribution"],
                "query": source["queries"][name],
                "archive": envelope["full_evidence"],
            },
        }
    with phmt.attribution():
        result = compare_screening_results(
            cohort, arms["baseline"], arms["consensus"], ef_fractions=(0.1,)
        )
    checks = {}
    compact = {}
    for name, native_name in (("baseline", "baseline"), ("consensus", "comparison")):
        derived, original = result["arms"][native_name], source["arms"][name]["study"]
        checks[name] = {
            "original_counts": derived["n_total"] == original["n_total"] == 64,
            "evaluated_counts": derived["n_evaluated"] == original["n_evaluated"] == 45,
            "unscored_counts": derived["n_unscored"] == original["n_unscored"] == 19,
            "unscored_causes": derived["unscored_by_stage"]
            == original["unscored_by_stage"],
            "original_indices": derived["evaluated_indices"]
            == original["evaluated_cohort_indices"],
            "labels_scores": derived["labels"] == original["labels"]
            and derived["scores"] == original["scores"],
            "metrics": all(
                abs(derived["metrics"][key] - original[key]) < 1e-14
                for key in ("AUC", "BEDROC", "EF@10%")
            ),
            "binary_sensitivity": derived["missing_binary_score_AUC_sensitivity"]
            == original["missing_binary_score_AUC_sensitivity"],
            "source_metadata": derived["source_metadata"]
            == arms[name]["source_metadata"],
            "native_records": all(
                r["native_evaluation"]
                == source["records"][r["input_index"]]["arms"][name][
                    "native_evaluation"
                ]
                for r in derived["records"]
            ),
        }
        compact[name] = {
            key: value
            for key, value in derived.items()
            if key not in {"records", "source_metadata"}
        }
    checks["paired"] = {
        "common_indices": result["common_subset"]["input_indices"]
        == source["common_subset"]["cohort_indices"],
        "AUC_delta": abs(
            result["common_subset"]["delta_comparison_minus_baseline"]["AUC"]
            - source["common_subset"]["delta_AUC_consensus_minus_baseline"]
        )
        < 1e-14,
        "source_unchanged": source_before
        == json.dumps(source, sort_keys=True, allow_nan=False),
    }
    if not all(value for section in checks.values() for value in section.values()):
        raise RuntimeError(f"Saved-result verification failed: {checks}")
    runtime_files = [
        "pharmacophoremt/validation/saved_results.py",
        "pharmacophoremt/validation/metrics.py",
        "pharmacophoremt/screening/scoring.py",
        "pharmacophoremt/_ackredit.py",
        "pharmacophoremt/_private/arg_digestion/argument/_contracts.py",
        "phmt_test_support/replay_esr1_saved_results.py",
        "phmt_test_support/evidence_archive.py",
    ]
    return {
        "schema": "pharmacophoremt.esr1_saved_summary_replay@1",
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "source_summary": str(Path(summary_path).relative_to(ROOT)),
        "source_summary_sha256": hashlib.sha256(
            Path(summary_path).read_bytes()
        ).hexdigest(),
        "source_archive": envelope["full_evidence"],
        "source_producer": source["producer"],
        "producer": {
            "git_head": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "git_status": subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=ROOT, text=True
            ),
            "python": sys.version,
            "executable": sys.executable,
            "versions": {
                name: metadata.version(name)
                for name in (
                    "pharmacophoremt",
                    "numpy",
                    "argdigest",
                    "smonitor",
                    "ackredit",
                    "molsysmt",
                    "pyunitwizard",
                    "depdigest",
                )
            },
            "module_origins": {
                name: str(getattr(sys.modules.get(name), "__file__", None))
                for name in (
                    "pharmacophoremt",
                    "numpy",
                    "argdigest",
                    "smonitor",
                    "ackredit",
                    "molsysmt",
                    "pyunitwizard",
                    "depdigest",
                )
            },
            "runtime_files": {
                name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                for name in runtime_files
            },
        },
        "verification": checks,
        "arms": compact,
        "common_subset": result["common_subset"],
        "attribution": result["attribution"],
        "scope": "New descriptive metrics from unchanged saved evidence; no molecular preparation/search, new activity observations or public delivery.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = replay()
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    print(
        json.dumps({"output": str(args.output), "verification": result["verification"]})
    )


if __name__ == "__main__":
    main()
