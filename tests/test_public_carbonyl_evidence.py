"""Cheap public-profile original-evidence and scientific-scope integrity."""

import hashlib
import json
import unittest
from pathlib import Path

SUMMARY = (
    Path(__file__).resolve().parents[1]
    / "devguide/evidence/public_cached_carbonyl_20261105_summary.json"
)


class TestPublicCarbonylEvidence(unittest.TestCase):
    def test_original_workload_and_source_scope(self):
        data = json.loads(SUMMARY.read_text())
        self.assertEqual(data["unique_selected_controls_passed"], 295)
        self.assertEqual(data["final_selected_controls_passed"], 114)
        self.assertEqual(
            data["actual_counts"],
            dict(
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
        self.assertEqual(data["molecular_operations_owner"], "molsysmt")
        self.assertFalse(data["new_tag_or_package_published"])

    def test_both_original_archives_keep_exact_bytes(self):
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
