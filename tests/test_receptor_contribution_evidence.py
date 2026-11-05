"""Cheap original-evidence integrity/accounting, without molecular execution."""

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "devguide/evidence/receptor_contribution_20261105_summary.json"


class TestReceptorContributionEvidence(unittest.TestCase):
    def test_measured_counts_remain_distinct_from_unscored_and_supplemental_slots(self):
        data = json.loads(SUMMARY.read_text())
        self.assertEqual(
            data["actual_counts"],
            dict(
                generation_cells=60,
                returned_models=342,
                primary_evaluations=1710,
                successful_primary_evaluations=1710,
                recovery_evaluations=108,
                unevaluated_candidate_slots=30,
            ),
        )
        self.assertEqual(
            data["plan_sha256"],
            "4358f73bf84aa334bf1b69822558860bc1f7cc6c0c071c1ad0dcc58978923981",
        )
        self.assertEqual(
            data["input_sha256"],
            "a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a",
        )
        self.assertTrue(data["production_runtime_unchanged"])
        self.assertEqual(data["molecular_operations_owner"], "molsysmt")

    def test_both_original_archives_keep_their_exact_compressed_bytes(self):
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
