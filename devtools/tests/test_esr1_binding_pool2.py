"""Pool-2 capacity gates select before class values and reject unknown totals."""

import importlib.util
import json
import unittest
from pathlib import Path

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
