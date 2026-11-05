"""Offline original-evidence checks; no molecular rerun or scientific imports."""

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "devguide/evidence/tyr_cardinality_20261105_summary.json"


class TestTyrCardinalityEvidence(unittest.TestCase):
    def test_frozen_identity_counts_and_scope(self):
        data = json.loads(SUMMARY.read_text())
        self.assertEqual(
            data["actual_counts"],
            dict(
                generation_cells=12,
                returned_models=20,
                primary_evaluations=100,
                recovery_evaluations=24,
            ),
        )
        self.assertEqual(
            data["plan_sha256"],
            "29b62982967e19855c0429716815a2c39f645cea7fd2042be0f86567925aac81",
        )
        self.assertEqual(
            data["input_sha256"],
            "a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a",
        )
        self.assertTrue(data["production_runtime_unchanged"])
        self.assertEqual(data["molecular_operations_owner"], "molsysmt")
        self.assertTrue(data["measured_analysis"]["unit_policy_answers_identical"])
        self.assertFalse(data["overlapping_site_reuse_isolated"])

    def test_both_original_archives_keep_exact_compressed_bytes(self):
        data = json.loads(SUMMARY.read_text())
        for key in ["full_evidence", "scientific_results"]:
            descriptor = data[key]
            raw = SUMMARY.with_name(descriptor["path"]).read_bytes()
            self.assertEqual(len(raw), descriptor["compressed_bytes"])
            self.assertEqual(
                hashlib.sha256(raw).hexdigest(), descriptor["compressed_sha256"]
            )


if __name__ == "__main__":
    unittest.main()
