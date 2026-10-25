"""Original-source controls for a fresh, not-yet-acquired binding challenge."""

import csv
import importlib.util
import io
import json
import tarfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "binding_readiness_driver", ROOT / "phmt_test_support/esr1_binding_readiness.py"
)
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)


class TestEsr1BindingReadiness(unittest.TestCase):
    def test_clean_metadata_receipt_preserves_nonready_gates_and_measured_counts(self):
        summary, run = driver.reader.read_archived_evidence(
            ROOT
            / "devguide/evidence/esr1_binding_metadata_review_20261024_summary.json"
        )
        self.assertEqual(
            run["producer"]["git_head"], "507ca37d8f21815bb29c0a34f8ccf3b020edbacf"
        )
        self.assertEqual(run["producer"]["git_status"], "")
        self.assertEqual(run["historical_exclusions"], driver.historical_exclusions())
        inventory = json.loads(driver.INVENTORY.read_text())
        self.assertEqual(len(inventory["responses"]), 9)
        self.assertEqual(
            run["source_inventory"]["sha256"],
            driver.identity(driver.INVENTORY)["sha256"],
        )
        self.assertEqual(run["readiness"], "not_ready")
        self.assertIsNone(run["evaluation_cohort"])
        self.assertFalse(run["new_individual_activities_acquired"])
        self.assertFalse(run["new_molecular_inputs_acquired"])
        self.assertFalse(run["new_scores_computed"])
        self.assertFalse(run["raw_metadata_portable"])
        self.assertEqual(run["chembl"]["discovery_records"], 1485)
        self.assertEqual(run["chembl"]["discovery_pages"], 2)
        self.assertTrue(run["chembl"]["complete_pagination"])
        self.assertEqual(run["chembl"]["status"]["chembl_db_version"], "ChEMBL_37")
        self.assertEqual(
            [r["assay_chembl_id"] for r in run["chembl"]["nominees"]],
            ["CHEMBL3382763", "CHEMBL3705057"],
        )
        by_aid = {r["AID"]: r for r in run["pubchem_metadata"]}
        self.assertEqual(
            (by_aid[1223]["CIDCountActive"], by_aid[1223]["CIDCountInactive"]), (17, 46)
        )
        self.assertEqual(by_aid[625258]["CIDCountInactive"], 0)
        self.assertGreater(
            by_aid[625258]["CIDCountActive"] + by_aid[625258]["CIDCountUnspecified"],
            by_aid[625258]["CIDCountAll"],
        )
        self.assertEqual(
            by_aid[2051711]["CIDCountAll"], by_aid[2051711]["CIDCountUnspecified"]
        )
        self.assertEqual(summary["producer"], run["producer"])

    def test_exclusions_cover_entire_read_source_and_failed_requested_inputs(self):
        observed = driver.historical_exclusions()
        manifest = json.loads(
            (ROOT / "tests/data/esr1_activity_pilot/manifest.json").read_text()
        )
        _, raw = driver.reader.read_archived_bytes(
            ROOT / "devguide/evidence/esr1_activity_pilot_inputs_20261023_summary.json"
        )
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
            rows = list(
                csv.DictReader(
                    io.TextIOWrapper(archive.extractfile(manifest["assay"]["file"]))
                )
            )
        expected = {row["CID"] for row in rows if row["CID"]}
        self.assertEqual(set(observed["cids"]), expected)
        self.assertEqual(observed["cids"], sorted(expected, key=int))
        self.assertEqual(len(rows), 10486)
        self.assertEqual(len(expected), 8099)
        self.assertEqual(observed["bath_distinct_cids"], 4402)
        self.assertNotIn("", observed["cids"])
        self.assertEqual(observed["assay_blank_cid_rows"], 149)
        self.assertEqual(
            observed["unresolved_source_rows"],
            [
                {"row_index": index, "sid": row["SID"]}
                for index, row in enumerate(rows)
                if not row["CID"]
            ],
        )
        # Both known upstream 404s and unselected/ambiguous historical outcomes
        # stay excluded; a new cohort cannot silently reuse them as unseen data.
        self.assertIn("24633", observed["cids"])
        self.assertTrue(
            {
                row["CID"]
                for row in rows
                if row["CID"] and row["Activity Outcome"] == "Inconclusive"
            }
            <= set(observed["cids"])
        )
        for item in observed["prior_requests"].values():
            original = json.loads((ROOT / item["path"]).read_text())
            self.assertTrue({r["cid"] for r in original["cohort"]} <= expected)
