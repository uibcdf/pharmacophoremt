"""Offline integrity/count checks; no scientific execution or imports."""

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "devguide/evidence/carbonyl_acceptor_receiving_20261105_summary.json"


class TestCarbonylAcceptorEvidence(unittest.TestCase):
    def test_executed_counts_and_frozen_scope(self):
        data = json.loads(SUMMARY.read_text())
        self.assertEqual(
            data["actual_counts"],
            dict(
                positive_provider_direction_calls=2,
                negative_provider_direction_calls=4,
                source_position_policy_blocks=6,
                returned_models=12,
                primary_evaluations=72,
                recovery_evaluations=24,
                negative_queries=4,
                negative_pose_evaluations=0,
            ),
        )
        self.assertEqual(
            data["plan_sha256"],
            "b0af26640c0b7ff6cadde2c7f7e499141921adc29fd2ec7f4c1666218be92340",
        )
        self.assertTrue(data["production_runtime_unchanged"])
        self.assertEqual(data["molecular_operations_owner"], "molsysmt")
        self.assertTrue(data["measured_analysis"]["unit_and_repeated_frame_fits_agree"])
        self.assertEqual(data["scientific_controls_passed"], 29)

    def test_original_scientific_and_source_archive_compressed_hashes(self):
        data = json.loads(SUMMARY.read_text())
        for key in ["scientific_results", "full_evidence"]:
            record = data[key]
            raw = SUMMARY.with_name(record["path"]).read_bytes()
            self.assertEqual(len(raw), record["compressed_bytes"])
            self.assertEqual(
                hashlib.sha256(raw).hexdigest(), record["compressed_sha256"]
            )


if __name__ == "__main__":
    unittest.main()
