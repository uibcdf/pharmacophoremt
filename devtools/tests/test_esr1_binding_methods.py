"""Keep reviewed source limits and incidental exposure out of accepted cohorts."""

import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "methods_archive_reader", ROOT / "phmt_test_support/evidence_archive.py"
)
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


class TestBindingMethods(unittest.TestCase):
    def setUp(self):
        self.summary, self.review = reader.read_archived_evidence(
            ROOT / "devguide/evidence/esr1_binding_pool3_methods_20261028_summary.json"
        )

    def test_original_metadata_matches_declared_order_and_retains_access_limits(self):
        declaration = self.review["declaration"]
        path = ROOT / declaration["path"]
        self.assertEqual(
            hashlib.sha256(path.read_bytes()).hexdigest(), declaration["sha256"]
        )
        declared = json.loads(path.read_text())["candidates"]
        self.assertEqual(
            [r["assay"] for r in self.review["candidates"]],
            [r["assay_chembl_id"] for r in declared],
        )
        inventory = self.review["source_inventory"]
        path = ROOT / inventory["path"]
        self.assertEqual(
            hashlib.sha256(path.read_bytes()).hexdigest(), inventory["sha256"]
        )
        sources = json.loads(path.read_text())
        original = [r for r in sources["requests"] if r["portable"]]
        self.assertEqual(len(original), 12)
        for row in original:
            raw = (path.parent / row["file"]).read_bytes()
            self.assertEqual(len(raw), row["bytes"])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), row["sha256"])
        self.assertEqual(sum(r["status"] == "failed" for r in sources["requests"]), 4)
        for row in self.review["publisher_receiving"]:
            self.assertEqual(row["http_status"], 200)
            self.assertTrue(row["coredata_present"])
            self.assertFalse(row["originalText_present"])
            self.assertFalse(row["sections_present"])
            self.assertFalse(row["full_method_text_observed"])
        self.assertEqual(sources["producer"]["git_status"], "")
        self.assertEqual(self.review["producer"]["kind"], "manual_document_review")
        self.assertIn(
            "pool3_methods_20261028", self.review["producer"]["context_git_status"]
        )

    def test_primary_panel_positions_cannot_become_independent_database_records(self):
        source = self.review["candidates"][0]
        self.assertEqual(source["assay"], "CHEMBL5730671")
        expected = {
            "Table 1": list("ABCDEFG") + ["1", "2", "3", "4"],
            "Table 2": list("HIJKL") + ["5", "6", "7"],
            "Table 3": list("MNO") + ["8"],
        }
        self.assertEqual(source["source_table_entry_labels"], expected)
        positions = sum(len(rows) for rows in expected.values())
        self.assertEqual(positions, 23)
        self.assertEqual(source["reported_alpha_positions_upper_bound"], positions)
        self.assertLess(positions, source["required_groups_total"])
        self.assertEqual(source["capacity_total"], 69)
        self.assertEqual(source["disposition"], "stopped_reported_panel_capacity")
        self.assertFalse(source["accepted_for_detailed_activity_acquisition"])
        self.assertIsNone(source["activity_class_counts"])

    def test_unresolved_methods_and_newly_seen_identifiers_do_not_become_unseen_data(
        self,
    ):
        r = self.review
        self.assertEqual(r["accepted_sources"], [])
        self.assertEqual(len(r["candidates"]), 6)
        self.assertEqual(
            sum(
                c["disposition"] == "unresolved_original_methods"
                for c in r["candidates"]
            ),
            4,
        )
        self.assertFalse(
            any(
                c["accepted_for_detailed_activity_acquisition"] for c in r["candidates"]
            )
        )
        self.assertEqual(r["activity_resource_requests"], 0)
        self.assertTrue(r["new_document_activity_information_observed"])
        self.assertFalse(r["activity_class_counts_computed"])
        self.assertFalse(r["digital_molecular_system_inputs_acquired"])
        self.assertFalse(r["new_scores_computed"])
        self.assertIsNone(r["evaluation_cohort"])
        _, prior = reader.read_archived_evidence(
            ROOT
            / "devguide/evidence/esr1_binding_metadata_review_20261024_summary.json"
        )
        old = set(prior["historical_exclusions"]["cids"])
        self.assertEqual(len(old), 8099)
        seen = r["new_review_exposure"]["literal_cids_seen"]
        self.assertEqual({x["cid"] for x in seen}, {"5870", "10399473"})
        for observation in seen:
            self.assertEqual(
                observation["already_in_original_8099"], observation["cid"] in old
            )
        self.assertNotIn("10399473", old)
        self.assertEqual(
            len(r["new_review_exposure"]["potentially_exposed_full_documents"]), 3
        )
