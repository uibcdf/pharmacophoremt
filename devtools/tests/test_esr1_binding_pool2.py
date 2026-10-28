"""Pool-2 capacity gates select before class values and reject unknown totals."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "binding_pool2", ROOT / "phmt_test_support/esr1_binding_pool2.py"
)
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)


def page(total):
    return {
        "page_meta": {
            "total_count": total,
            "offset": 0,
            "previous": None,
            "next": "/next" if total > 1 else None,
        },
        "activities": [{"activity_id": 123}] if total else [],
    }


class TestBindingPool2(unittest.TestCase):
    def test_pool3_original_census_and_clean_receipt_retain_pending_survivors(self):
        declaration_path = (
            ROOT / "tests/data/esr1_binding_evaluation/pool3_declaration_20261028.json"
        )
        summary, archived = driver.source.readiness.reader.read_archived_evidence(
            ROOT / "devguide/evidence/esr1_binding_pool3_20261028_summary.json"
        )
        directory = ROOT / summary["original_inputs"]
        journal = json.loads((directory / "acquisition.json").read_text())
        current = driver.summarize(directory, declaration_path=declaration_path)
        self.assertEqual(len(journal["requests"]), 476)
        self.assertTrue(all(r["status"] == "completed" for r in journal["requests"]))
        self.assertFalse(any(r["phase"] == "details" for r in journal["requests"]))
        self.assertEqual(journal["producer"], archived["producer"])
        self.assertEqual(archived["producer"]["git_status"], "")
        self.assertEqual(
            archived["producer"]["git_head"], "751f7f4208186db401c6de373f826abf439ff695"
        )
        for key in archived.keys() - {"producer", "recorded_at"}:
            self.assertEqual(current[key], archived[key], key)
        self.assertEqual(len(archived["capacity_totals"]), 475)
        eligible = sorted(
            (a for a, n in archived["capacity_totals"].items() if n >= 40),
            key=lambda a: (-archived["capacity_totals"][a], int(a[6:])),
        )
        self.assertEqual(len(eligible), 15)
        self.assertEqual(archived["deferred_capacity_survivors"], eligible)
        self.assertEqual(archived["capacity_totals"][eligible[0]], 439)
        self.assertEqual(archived["capacity_totals"][eligible[-1]], 40)
        self.assertEqual(archived["selected"], [])
        self.assertEqual(archived["assessments"], {})
        self.assertEqual(archived["numerical_survivors"], [])
        self.assertEqual(archived["newly_inspected_chembl_identifiers"], [])
        self.assertEqual(len(archived["previously_exposed_chembl_identifiers"]), 25)
        self.assertEqual(
            archived["readiness"], "capacity_survivors_require_source_review"
        )
        self.assertFalse(archived["terminal_stop"])
        self.assertFalse(archived["new_molecular_inputs_acquired"])
        self.assertFalse(archived["new_scores_computed"])
        self.assertIsNone(archived["evaluation_cohort"])
        self.assertEqual(summary["producer"], archived["producer"])

    def test_capacity_only_survivors_are_pending_and_never_fetch_detail_values(self):
        declaration = json.loads(driver.DECLARATION.read_text())
        declaration["nominees"] = [{"assay_chembl_id": "CHEMBL9"}]
        declaration["detailed_selection"]["maximum_assays"] = 0
        declaration["acquisition_schema"] = "capacity-only-acquisition"
        declaration["review_schema"] = "capacity-only-review"
        calls = []

        def fetch(url, path):
            calls.append(url)
            payload = (
                {"chembl_db_version": "ChEMBL_37", "activities": 1000000}
                if "status.json" in url
                else page(40)
            )
            path.write_text(json.dumps(payload))
            return path.read_bytes()

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            declared = root / "declaration.json"
            declared.write_text(json.dumps(declaration))
            with patch.object(driver.pilot, "fetch", fetch):
                journal = driver.acquire(root / "inputs", declaration_path=declared)
            report = driver.summarize(root / "inputs", declaration_path=declared)
            self.assertEqual(journal["schema"], "capacity-only-acquisition")
            self.assertEqual(report["schema"], "capacity-only-review")
            self.assertEqual(journal["phase"], "completed")
            self.assertEqual(len(calls), 2)
            self.assertIn("only=activity_id", calls[1])
            self.assertIn("limit=1", calls[1])
            self.assertEqual(report["deferred_capacity_survivors"], ["CHEMBL9"])
            self.assertEqual(report["selected"], [])
            self.assertEqual(report["assessments"], {})
            self.assertEqual(report["newly_inspected_chembl_identifiers"], [])
            self.assertEqual(
                report["readiness"], "capacity_survivors_require_source_review"
            )
            self.assertFalse(report["terminal_stop"])
            declared.write_text(declared.read_text() + "\n")
            with self.assertRaisesRegex(ValueError, "different declaration"):
                driver.summarize(root / "inputs", declaration_path=declared)

    def test_pool3_declares_all_remaining_single_protein_assays_without_text_filter(
        self,
    ):
        path = (
            ROOT / "tests/data/esr1_binding_evaluation/pool3_declaration_20261028.json"
        )
        declaration = json.loads(path.read_text())
        rows = declaration["nominees"]
        ids = [r["assay_chembl_id"] for r in rows]
        previous = json.loads(driver.DECLARATION.read_text())
        excluded = {r["assay_chembl_id"] for r in previous["nominees"]} | {
            "CHEMBL3382763",
            "CHEMBL3705057",
            "CHEMBL5474416",
        }
        self.assertEqual(len(ids), 475)
        self.assertEqual(len(set(ids)), 475)
        self.assertEqual(ids, sorted(ids, key=lambda x: int(x[6:])))
        self.assertFalse(set(ids) & excluded)
        self.assertEqual(
            set(declaration["nomination_rule"]["excluded_assays"]), excluded
        )
        self.assertEqual(declaration["metadata_sources"], previous["metadata_sources"])
        self.assertTrue(all(r["bao_format"] == "BAO_0000357" for r in rows))
        self.assertEqual(declaration["detailed_selection"]["maximum_assays"], 0)
        self.assertEqual(declaration["capacity"]["minimum_total_records"], 40)
        self.assertEqual(declaration["classification"], previous["classification"])
        self.assertTrue(declaration["no_molecular_inputs_or_scoring"])
        # Known misleading recruitment metadata and single-concentration wording
        # remain candidates for capacity, explicitly not qualified endpoints.
        self.assertIn("CHEMBL4233993", ids)
        self.assertTrue(any(" at " in r["description"].lower() for r in rows))

    def test_clean_replay_keeps_original_acquisition_and_no_new_compound_exposure(self):
        summary, run = driver.source.readiness.reader.read_archived_evidence(
            ROOT / "devguide/evidence/esr1_binding_pool2_20261026_summary.json"
        )
        self.assertEqual(
            run["producer"]["git_head"], "992df4e31131e2435821b73c5cf6901f6913e407"
        )
        self.assertEqual(run["producer"]["git_status"], "")
        directory = ROOT / summary["original_inputs"]
        original = json.loads((directory / "acquisition.json").read_text())
        self.assertEqual(
            original["producer"]["git_head"], "eef3fa82abcf3e22ca0c1974948fc577a3f1b42c"
        )
        self.assertEqual(original["producer"]["git_status"], "")
        self.assertEqual(
            run["declaration"], driver.source.readiness.identity(driver.DECLARATION)
        )
        self.assertEqual(
            run["acquisition"],
            driver.source.readiness.identity(directory / "acquisition.json"),
        )
        current = driver.summarize(directory)
        for key in (
            "capacity_totals",
            "selected",
            "invalid_capacity",
            "assessments",
            "readiness",
            "newly_inspected_chembl_identifiers",
            "previously_exposed_chembl_identifiers",
        ):
            self.assertEqual(run[key], current[key])
        self.assertEqual(len(run["previously_exposed_chembl_identifiers"]), 25)
        self.assertTrue(run["terminal_stop"])
        self.assertFalse(run["new_scores_computed"])
        self.assertFalse(run["new_molecular_inputs_acquired"])
        self.assertEqual(summary["producer"], run["producer"])

    def test_original_capacity_responses_stop_before_values_and_global_status_is_not_a_table(
        self,
    ):
        directory = ROOT / "tests/data/esr1_binding_evaluation/pool2_capacity_20261026"
        report = driver.summarize(directory)
        journal = json.loads((directory / "acquisition.json").read_text())
        self.assertEqual(len(journal["requests"]), 43)
        self.assertEqual(journal["producer"]["git_status"], "")
        self.assertTrue(all(r["status"] == "completed" for r in journal["requests"]))
        self.assertEqual(len(report["capacity_totals"]), 42)
        self.assertEqual(max(report["capacity_totals"].values()), 26)
        self.assertEqual(report["capacity_totals"]["CHEMBL3776150"], 26)
        self.assertEqual(report["selected"], [])
        self.assertEqual(report["deferred_capacity_survivors"], [])
        self.assertEqual(report["assessments"], {})
        self.assertEqual(report["newly_inspected_chembl_identifiers"], [])
        self.assertEqual(report["invalid_capacity"], {})
        self.assertEqual(report["readiness"], "capacity_pool_stopped")
        self.assertTrue(report["terminal_stop"])
        self.assertIsNone(report["evaluation_cohort"])
        self.assertFalse(any(r["phase"] == "details" for r in journal["requests"]))
        # ChEMBL status has a global integer 'activities' counter. It is valid
        # status provenance, never an iterable of individual activity records.
        self.assertIsInstance(
            json.loads((directory / "status.json").read_text())["activities"], int
        )
        for request in journal["requests"]:
            if request["phase"] == "capacity":
                payload = json.loads((directory / request["file"]).read_text())
                self.assertTrue(
                    all(set(r) == {"activity_id"} for r in payload["activities"])
                )

    def test_capacity_projection_has_no_labels_and_zero_is_observed_not_missing(self):
        for total in (0, 1, 39, 40, 100):
            self.assertEqual(driver.capacity_total(page(total)), total)
        for mutation in ("value", "missing_row", "wrong_total", "missing_next"):
            with self.subTest(mutation=mutation):
                payload = page(40)
                if mutation == "value":
                    payload["activities"][0]["standard_value"] = "500"
                elif mutation == "missing_row":
                    payload["activities"] = []
                elif mutation == "wrong_total":
                    payload["page_meta"]["total_count"] = True
                else:
                    payload["page_meta"]["next"] = None
                with self.assertRaises(ValueError):
                    driver.capacity_total(payload)

    def test_complete_capacity_and_numeric_tie_order_are_required_before_selection(
        self,
    ):
        declaration = {
            "nominees": [
                {"assay_chembl_id": f"CHEMBL{i}"} for i in (9, 10, 11, 12, 13)
            ],
            "capacity": {"minimum_total_records": 40},
            "detailed_selection": {"maximum_assays": 3},
        }
        totals = {
            "CHEMBL9": 40,
            "CHEMBL10": 90,
            "CHEMBL11": 90,
            "CHEMBL12": 39,
            "CHEMBL13": 70,
        }
        selected, deferred = driver.select_details(totals, declaration)
        self.assertEqual(selected, ["CHEMBL10", "CHEMBL11", "CHEMBL13"])
        self.assertEqual(deferred, ["CHEMBL9"])
        for value in (None, False, -1):
            with self.subTest(value=value), self.assertRaises(ValueError):
                driver.select_details({**totals, "CHEMBL12": value}, declaration)
        del totals["CHEMBL12"]
        with self.assertRaises(ValueError):
            driver.select_details(totals, declaration)

    def test_declaration_preserves_original_numeric_and_no_molecular_contract(self):
        declaration = json.loads(driver.DECLARATION.read_text())
        ids = [row["assay_chembl_id"] for row in declaration["nominees"]]
        self.assertEqual(len(ids), 42)
        self.assertEqual(len(set(ids)), 42)
        self.assertNotIn("CHEMBL3382763", ids)
        self.assertNotIn("CHEMBL3705057", ids)
        self.assertNotIn("CHEMBL5474416", ids)
        self.assertEqual(declaration["classification"]["minimum_per_class"], 20)
        self.assertEqual(declaration["classification"]["positive_nM_at_most"], 1000)
        self.assertEqual(declaration["classification"]["weak_nM_at_least"], 10000)
        self.assertEqual(declaration["capacity"]["projection"], ["activity_id"])
        self.assertTrue(declaration["no_molecular_inputs_or_scoring"])
