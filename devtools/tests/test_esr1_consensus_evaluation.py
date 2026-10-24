"""Offline guards for fixed paired-study transport and input accounting."""

from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "paired_evaluation_driver", ROOT / "phmt_test_support/esr1_consensus_evaluation.py"
)
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)


class TestEsr1ConsensusEvaluation(unittest.TestCase):
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
