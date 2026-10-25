"""Offline guards for fixed paired-study transport and input accounting."""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import math
import tempfile
import unittest
import urllib.error
from collections import Counter
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "paired_evaluation_driver", ROOT / "phmt_test_support/esr1_consensus_evaluation.py"
)
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)


def independent_metrics(rows, arm, hypothetical=None):
    """Pairwise AUC, boundary-tie EF and explicit exponential positional sums."""
    pairs = []
    for row in rows:
        score = row["arms"][arm]["ranking_score"]
        if score is None:
            if hypothetical is None:
                raise ValueError(
                    "exclude unscored inputs or request a hypothetical scenario"
                )
            score = row["label"] if hypothetical else 1 - row["label"]
        pairs.append((row["label"], score))
    positives = [score for label, score in pairs if label]
    negatives = [score for label, score in pairs if not label]
    auc = sum((p > n) + 0.5 * (p == n) for p in positives for n in negatives) / (
        len(positives) * len(negatives)
    )
    ranked = sorted(pairs, key=lambda p: -p[1])
    n, active = len(pairs), len(positives)
    top = math.ceil(0.10 * n)
    threshold = ranked[top - 1][1]
    above = [p for p in pairs if p[1] > threshold]
    tied = [p for p in pairs if p[1] == threshold]
    ef = (
        (
            sum(p[0] for p in above)
            + (top - len(above)) * sum(p[0] for p in tied) / len(tied)
        )
        / top
        / (active / n)
    )
    weights = [math.exp(-20 * (i + 1) / n) for i in range(n)]
    observed, start = 0, 0
    while start < n:
        end = start + 1
        while end < n and ranked[end][1] == ranked[start][1]:
            end += 1
        observed += (
            sum(p[0] for p in ranked[start:end])
            * sum(weights[start:end])
            / (end - start)
        )
        start = end
    bedroc = (observed - sum(weights[-active:])) / (
        sum(weights[:active]) - sum(weights[-active:])
    )
    return dict(AUC=auc, BEDROC=bedroc, **{"EF@10%": ef})


class TestEsr1ConsensusEvaluation(unittest.TestCase):
    def test_original_paired_result_has_independent_oracles_and_complete_failure_accounting(
        self,
    ):
        path = ROOT / "devguide/evidence/esr1_paired_evaluation_20261024_summary.json"
        summary, run = driver.reader.read_archived_evidence(path)
        self.assertEqual(
            run["producer"]["git_head"], "012544472e8eca27d1646a6e8065ee22872d4368"
        )
        self.assertEqual(run["producer"]["dirty"], "")
        self.assertTrue(run["producer_stable"])
        self.assertTrue(run["product_provider_files_match_training"])
        self.assertEqual(len(run["producer"]["conda_records"]), 325)
        records = run["records"]
        protocol = driver.training.declaration(driver.DECLARATION)
        expected = driver.evaluation_entries(protocol)
        self.assertEqual(
            [(r["cid"], r["sid"], r["label"]) for r in records],
            [(e["cid"], e["sid"], e["label"]) for e in expected],
        )
        self.assertEqual(Counter(r["label"] for r in records), {1: 16, 0: 48})
        prepared = [r for r in records if r["preparation"]["status"] == "completed"]
        missing = [r for r in records if r["preparation"]["status"] != "completed"]
        self.assertEqual(Counter(r["label"] for r in prepared), {1: 12, 0: 33})
        self.assertEqual(Counter(r["label"] for r in missing), {1: 4, 0: 15})
        self.assertTrue(all(all(r["preparation"]["checks"].values()) for r in prepared))
        self.assertTrue(
            all(
                r["acquisition"]["http_status"] == 404
                and r["preparation"]["stage"] == "acquisition"
                for r in missing
            )
        )
        mapping = run["prepared_cohort_indices"]
        self.assertEqual(mapping, [r["cohort_index"] for r in prepared])
        self.assertEqual(run["common_subset"]["cohort_indices"], mapping)
        oracles = {}
        for arm in ("baseline", "consensus"):
            report = run["arms"][arm]
            native = report["native_prepared_input_report"]
            self.assertEqual(
                (
                    native["n_actives"],
                    native["n_decoys"],
                    native["n_evaluated"],
                    native["n_failed"],
                ),
                (12, 33, 45, 0),
            )
            self.assertEqual(
                (report["study"]["n_total"], report["study"]["n_unscored"]), (64, 19)
            )
            self.assertEqual(report["study"]["unscored_by_stage"], {"acquisition": 19})
            for dense_index, index in enumerate(mapping):
                self.assertEqual(
                    records[index]["arms"][arm]["native_input_index"], dense_index
                )
                self.assertEqual(
                    records[index]["arms"][arm]["native_evaluation"],
                    native["evaluations"][dense_index],
                )
            for row in missing:
                self.assertIsNone(row["arms"][arm]["ranking_score"])
                self.assertIsNone(row["arms"][arm]["native_evaluation"])
            oracles[arm] = independent_metrics(prepared, arm)
            for key, value in oracles[arm].items():
                for observed in (
                    native[key],
                    report["study"][key],
                    run["common_subset"]["arms"][arm][key],
                ):
                    self.assertAlmostEqual(value, observed, places=13)
            for key, optimistic in (
                ("pessimistic_hypothetical", False),
                ("optimistic_hypothetical", True),
            ):
                self.assertAlmostEqual(
                    independent_metrics(records, arm, hypothetical=optimistic)["AUC"],
                    report["study"]["missing_binary_score_AUC_sensitivity"][key],
                    places=13,
                )
        self.assertEqual(
            [r["cid"] for r in prepared if r["arms"]["baseline"]["ranking_score"] == 1],
            ["33255"],
        )
        self.assertEqual(
            [
                (r["cid"], r["label"])
                for r in prepared
                if r["arms"]["consensus"]["ranking_score"] == 1
            ],
            [("87250", 1), ("5280961", 1), ("70425", 0), ("11193251", 0)],
        )
        self.assertAlmostEqual(
            run["common_subset"]["delta_AUC_consensus_minus_baseline"],
            oracles["consensus"]["AUC"] - oracles["baseline"]["AUC"],
            places=14,
        )
        self.assertEqual(
            run["input_integrity"]["before"], run["input_integrity"]["after_baseline"]
        )
        self.assertEqual(
            run["input_integrity"]["before"], run["input_integrity"]["after_consensus"]
        )
        inputs = ROOT / summary["original_inputs"]
        self.assertEqual(
            hashlib.sha256((inputs / "acquisition.json").read_bytes()).hexdigest(),
            run["acquisition"]["sha256"],
        )
        acquired = json.loads((inputs / "acquisition.json").read_text())
        for row in acquired["records"]:
            a = row["acquisition"]
            identity = a if a["status"] == "completed" else a["response"]
            self.assertEqual(
                driver.pilot.identity(inputs / identity["file"]),
                {k: identity[k] for k in ("file", "sha256", "byte_count")},
            )
        for arm, expected_sha in driver.QUERY_HASHES.items():
            self.assertEqual(
                driver.pilot.digest((inputs / f"{arm}.query.json").read_bytes()),
                expected_sha,
            )
            self.assertEqual(run["queries"][arm]["sha256"], expected_sha)
        self.assertEqual(
            (len(run["attribution"]["items"]), len(run["attribution"]["uses"])),
            (60, 89),
        )
        for key in (
            "preparation_evidence",
            "baseline_evidence",
            "consensus_evidence",
            "execution_log",
            "acquisition_log",
            "qualification_evidence",
            "cleanup_evidence",
        ):
            driver.reader.read_archived_bytes(path, identity_key=key)

    def test_acquisition_uses_all_reserved_ids_and_exact_queries_without_replacement(
        self,
    ):
        protocol, trained, queries = driver.frozen_context()
        self.assertEqual(trained["outcome"]["status"], "ready")
        expected = driver.evaluation_entries(protocol)
        self.assertEqual(len(expected), 64)
        self.assertEqual(sum(e["label"] for e in expected), 16)
        self.assertFalse(
            {e["cid"] for e in expected}
            & {e["cid"] for e in driver.training.training_entries(protocol)}
        )
        calls = []

        def fetch(url, path):
            calls.append(url)
            if len(calls) in (2, 60):
                raise urllib.error.HTTPError(
                    url, 404, "Not Found", {}, io.BytesIO(b"original response")
                )
            path.write_bytes(b"opaque source SDF response")

        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "inputs"
            with (
                patch.object(driver.pilot, "fetch", side_effect=fetch),
                patch.object(driver.time, "sleep"),
            ):
                receipt = driver.acquire(directory)
            self.assertEqual(calls, [e["url"] for e in expected])
            self.assertEqual(len(receipt["records"]), 64)
            self.assertEqual(
                driver.validate_acquisition(directory, protocol, queries), receipt
            )
            for arm, raw in queries.items():
                self.assertEqual((directory / f"{arm}.query.json").read_bytes(), raw)
            failed = receipt["records"][1]
            self.assertEqual(failed["acquisition"]["http_status"], 404)
            self.assertEqual(
                (directory / failed["acquisition"]["response"]["file"]).read_bytes(),
                b"original response",
            )
            self.assertFalse((directory / f"CID{failed['cid']}.sdf").exists())
            with self.assertRaises(FileExistsError):
                driver.acquire(directory)
            (directory / "baseline.query.json").write_bytes(queries["baseline"] + b"\n")
            with self.assertRaises(ValueError):
                driver.validate_acquisition(directory, protocol, queries)
            (directory / "baseline.query.json").write_bytes(queries["baseline"])
            receipt["records"][0]["cohort_index"] = 63
            (directory / "acquisition.json").write_text(json.dumps(receipt))
            with self.assertRaises(ValueError):
                driver.validate_acquisition(directory, protocol, queries)

    def test_prepared_native_indices_keep_failed_originals_and_class_order_distinct(
        self,
    ):
        records = [
            dict(cohort_index=i, label=label, preparation=dict(status=status))
            for i, (label, status) in enumerate(
                (
                    (0, "completed"),
                    (1, "unavailable"),
                    (1, "completed"),
                    (0, "failed"),
                    (0, "completed"),
                )
            )
        ]
        self.assertEqual(driver.prepared_mapping(records), [2, 0, 4])
        self.assertEqual(len(records), 5)
        self.assertEqual(
            [
                r["cohort_index"]
                for r in records
                if r["preparation"]["status"] != "completed"
            ],
            [1, 3],
        )
        self.assertEqual(driver.prepared_mapping([]), [])


if __name__ == "__main__":
    unittest.main()
