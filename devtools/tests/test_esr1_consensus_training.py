"""Study-specific training transport and frozen model-choice guards."""

from __future__ import annotations

import hashlib
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
    def test_readiness_acquisition_reuses_three_originals_and_never_requests_evaluation(
        self,
    ):
        path = ROOT / "tests/data/esr1_consensus_comparison/readiness_declaration.json"
        protocol = driver.declaration(path)
        prior_ids = {"31477", "24633", "6293"}
        expected_urls = [
            e["url"]
            for e in driver.training_entries(protocol)
            if e["cid"] not in prior_ids
        ]
        calls = []

        def fetch(url, target):
            calls.append(url)
            target.write_bytes(b"new opaque training response")

        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp) / "pool"
            with (
                patch.object(driver.pilot, "fetch", side_effect=fetch),
                patch.object(driver.time, "sleep"),
            ):
                receipt = driver.acquire_training(directory, path)
            self.assertEqual(calls, expected_urls)
            self.assertEqual(len(calls), 9)
            self.assertEqual(len(receipt["records"]), 12)
            self.assertEqual(receipt["records"][1]["acquisition"]["http_status"], 404)
            self.assertFalse((directory / "CID24633.sdf").exists())
            self.assertEqual(driver.validate_acquisition(directory, protocol), receipt)
            receipt["records"][1]["acquisition"]["http_status"] = 503
            (directory / "acquisition.json").write_text(json.dumps(receipt))
            with self.assertRaises(ValueError):
                driver.validate_acquisition(directory, protocol)
        records = [
            dict(cid="a", preparation=dict(status="failed")),
            dict(cid="b", preparation=dict(status="completed", feature_counts={})),
            dict(
                cid="c",
                preparation=dict(
                    status="completed", feature_counts={"aromatic ring": 1}
                ),
            ),
            dict(cid="d", preparation=dict(status="completed", feature_counts={})),
            dict(
                cid="e",
                preparation=dict(
                    status="completed", feature_counts={"aromatic ring": 99}
                ),
            ),
        ]
        self.assertEqual(driver.choose_training_ids(records), ["b", "c", "d"])
        self.assertEqual(driver.choose_training_ids(records[:2]), ["b"])

    def test_archived_stop_preserves_sources_without_consensus_or_evaluation(self):
        spec = importlib.util.spec_from_file_location(
            "training_evidence_reader", ROOT / "phmt_test_support/evidence_archive.py"
        )
        reader = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(reader)
        path = ROOT / "devguide/evidence/esr1_consensus_training_20261024_summary.json"
        summary, run = reader.read_archived_evidence(path)
        self.assertEqual(
            run["producer"]["git_head"], "5242ca63eb239aaecb95ae782304dbeca7b53135"
        )
        self.assertEqual(run["producer"]["dirty"], "")
        self.assertTrue(run["producer_stable"])
        self.assertEqual(run["producer"]["versions"]["molsysmt"], "0.23.0")
        self.assertEqual(len(run["producer"]["conda_records"]), 325)
        self.assertEqual(run["declaration"]["sha256"], driver.DECLARATION_SHA256)
        self.assertEqual(run["outcome"]["status"], "stopped")
        self.assertEqual(run["outcome"]["stage"], "preparation")
        self.assertFalse(run["outcome"]["evaluation_opened"])
        self.assertIsNone(run["consensus"])
        self.assertIsNone(run["selected"])
        self.assertEqual(run["training_readiness"], [])
        inputs = ROOT / summary["original_inputs"]
        acquired = json.loads((inputs / "acquisition.json").read_text())
        self.assertEqual(
            hashlib.sha256((inputs / "acquisition.json").read_bytes()).hexdigest(),
            run["acquisition"]["sha256"],
        )
        expected = [
            e for e in driver.declaration()["cohort"] if e["role"] == "training"
        ]
        self.assertEqual(
            [r["cid"] for r in run["records"]], [e["cid"] for e in expected]
        )
        self.assertEqual(
            [r["cid"] for r in acquired["records"]], [e["cid"] for e in expected]
        )
        self.assertFalse(acquired["evaluation_acquired"])
        for record in acquired["records"]:
            acquisition = record["acquisition"]
            identity = (
                acquisition
                if acquisition["status"] == "completed"
                else acquisition["response"]
            )
            self.assertEqual(
                driver.pilot.identity(inputs / identity["file"]),
                {k: identity[k] for k in ("file", "sha256", "byte_count")},
            )
        records = {r["cid"]: r for r in run["records"]}
        for cid, counts, features in (
            ("31477", (49, 49), {"hb donor": 2, "hb acceptor": 5, "aromatic ring": 1}),
            ("6293", (26, 28), {"hb donor": 2, "hb acceptor": 4, "aromatic ring": 2}),
        ):
            prepared = records[cid]["preparation"]
            self.assertEqual(prepared["status"], "completed")
            self.assertTrue(all(prepared["checks"].values()))
            self.assertEqual(
                (prepared["counts"]["n_atoms"], prepared["counts"]["n_bonds"]), counts
            )
            self.assertEqual(prepared["counts"]["n_structures"], 1)
            self.assertEqual(prepared["feature_counts"], features)
            self.assertLess(prepared["coordinate_rmsd_nm"], 1e-12)
        failed = records["24633"]
        self.assertEqual(failed["acquisition"]["http_status"], 404)
        self.assertEqual(failed["preparation"]["status"], "failed")
        self.assertIn("acquisition failed", failed["preparation"]["message"])
        self.assertFalse((inputs / "CID24633.sdf").exists())
        self.assertEqual(len(run["attribution"]["items"]), 12)
        self.assertEqual(len(run["attribution"]["uses"]), 14)
        ids = {i["id"] for i in run["attribution"]["items"]}
        self.assertTrue(
            {"phmt:dataset:pubchem-3d:31477", "phmt:dataset:pubchem-3d:6293"} <= ids
        )
        self.assertNotIn("phmt:dataset:pubchem-3d:24633", ids)
        self.assertTrue(all("10.1107/S0567739476001873" not in i for i in ids))
        for key in (
            "execution_log",
            "acquisition_log",
            "cleanup_evidence",
            "environment_creation_evidence",
        ):
            reader.read_archived_bytes(path, identity_key=key)
        _, qualification = reader.read_archived_evidence(
            path, identity_key="qualification_evidence"
        )
        self.assertEqual(qualification["source_commit"], run["producer"]["git_head"])

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
