"""Study-specific training transport and frozen model-choice guards."""

from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "esr1_training_driver", ROOT / "phmt_test_support/esr1_consensus_training.py"
)
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)


class TestEsr1ConsensusTraining(unittest.TestCase):
    def test_only_three_frozen_training_requests_and_original_failure_are_retained(
        self,
    ):
        protocol = driver.declaration()
        expected = [e for e in protocol["cohort"] if e["role"] == "training"]
        calls = []

        def fetch(url, path):
            calls.append(url)
            if len(calls) == 2:
                raise urllib.error.HTTPError(
                    url, 404, "Not Found", {}, io.BytesIO(b"original error")
                )
            path.write_bytes(b"opaque source response")

        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "inputs"
            with (
                patch.object(driver.pilot, "fetch", side_effect=fetch),
                patch.object(driver.time, "sleep"),
            ):
                receipt = driver.acquire_training(directory)
            self.assertEqual(calls, [e["url"] for e in expected])
            self.assertFalse(receipt["evaluation_acquired"])
            self.assertEqual(
                [e["cid"] for e in receipt["records"]], [e["cid"] for e in expected]
            )
            failed = receipt["records"][1]["acquisition"]
            self.assertEqual(failed["http_status"], 404)
            self.assertEqual(
                (directory / failed["response"]["file"]).read_bytes(), b"original error"
            )
            self.assertEqual(driver.validate_acquisition(directory, protocol), receipt)
            with self.assertRaises(FileExistsError):
                driver.acquire_training(directory)
            first = directory / receipt["records"][0]["acquisition"]["file"]
            first.write_bytes(b"substitution")
            with self.assertRaises(ValueError):
                driver.validate_acquisition(directory, protocol)
            changed = Path(tmp) / "declaration.json"
            changed.write_bytes(driver.DECLARATION.read_bytes() + b"\n")
            with self.assertRaises(ValueError):
                driver.acquire_training(Path(tmp) / "changed", changed)
            self.assertFalse((Path(tmp) / "changed").exists())

    def test_model_choice_uses_sites_support_and_identifiers_without_scores(self):
        def model(sites, support, layout, hypothesis):
            return SimpleNamespace(
                n_interaction_sites=sites,
                metadata=dict(
                    hypothesis=dict(
                        joint_support_count=support, hypothesis_id=hypothesis
                    ),
                    layout=dict(layout_id=layout),
                ),
            )

        models = [
            model(3, 3, "layout_0", "a"),
            model(4, 2, "layout_2", "a"),
            model(4, 3, "layout_1", "b"),
            model(4, 3, "layout_1", "a"),
        ]
        index, ranking = driver.choose_model(models)
        self.assertEqual(index, 3)
        self.assertEqual(ranking, [3, 2, 1, 0])
        with self.assertRaises(ValueError):
            driver.choose_model([])
        # A changed cohort identity is rejected even before molecular imports.
        protocol = json.loads(driver.DECLARATION.read_text())
        self.assertEqual(sum(e["role"] == "training" for e in protocol["cohort"]), 3)


if __name__ == "__main__":
    unittest.main()
