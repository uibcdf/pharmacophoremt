"""Analytical bounds and primary-table oracles for the stopped #66 source pool."""

import importlib.util
import json
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "binding_source_qualification",
    ROOT / "phmt_test_support/esr1_binding_source_qualification.py",
)
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)


def observation(value, relation="=", **patch):
    row = dict(
        activity_id=1,
        molecule_chembl_id="source-A",
        standard_type="IC50",
        standard_flag=1,
        potential_duplicate=0,
        data_validity_comment=None,
        standard_units="nM",
        standard_value=value,
        standard_relation=relation,
    )
    row.update(patch)
    return row


class TestBindingSourceQualification(unittest.TestCase):
    def test_exact_and_censored_bounds_do_not_invent_weak_labels(self):
        for value, relation, expected in (
            ("1000", "=", 1),
            ("10000", "=", 0),
            ("1000", "<", 1),
            ("1000", "<=", 1),
            ("10000", ">", 0),
            ("10000", ">=", 0),
            ("1000", ">", None),
            ("10000", "<", None),
            ("1500", "=", None),
            (None, "=", None),
            ("NaN", "=", None),
            ("Infinity", "=", None),
            ("0", "=", None),
            ("-1", "=", None),
            ("100", "~", None),
        ):
            with self.subTest(value=value, relation=relation):
                self.assertEqual(
                    driver.classify(observation(value, relation))[0], expected
                )

    def test_quality_missing_numeric_values_and_units_remain_unclassified(self):
        for patch in (
            {"potential_duplicate": 1},
            {"potential_duplicate": None},
            {"data_validity_comment": "outside typical range"},
            {"standard_flag": 0},
            {"standard_flag": True},
            {"standard_units": "uM"},
            {"standard_type": "Relative binding affinity"},
            {"standard_value": None, "activity_comment": "Inactive"},
        ):
            with self.subTest(patch=patch):
                label, reasons = driver.classify(observation("20", **patch))
                self.assertIsNone(label)
                self.assertTrue(reasons)
        row = observation("20")
        del row["data_validity_comment"]
        self.assertIsNone(driver.classify(row)[0])

    def test_all_relevant_replicates_count_and_endpoints_are_not_pooled(self):
        rows = [observation("20"), observation("20000", activity_id=2)]
        before = deepcopy(rows)
        report = driver.assess_rows(rows)
        self.assertEqual(rows, before)
        endpoint = report["endpoints"]["IC50"]
        self.assertEqual(endpoint["n_identifiers"], 1)
        self.assertEqual(endpoint["n_unclassified_identifiers"], 1)
        rows[1]["standard_value"] = "1500"
        self.assertEqual(
            driver.assess_rows(rows)["endpoints"]["IC50"]["n_unclassified_identifiers"],
            1,
        )
        rows[1].update(standard_type="Ki", standard_value="20000")
        report = driver.assess_rows(rows)
        self.assertEqual(report["endpoints"]["IC50"]["n_positive_identifiers"], 1)
        self.assertEqual(report["endpoints"]["Ki"]["n_weak_identifiers"], 1)
        with self.assertRaises(ValueError):
            driver.assess_rows([rows[0], rows[0]])

    def test_original_activity_tables_match_primary_receptor_column_oracles(self):
        report = driver.execute()
        self.assertEqual(report["readiness"], "stopped")
        self.assertTrue(report["terminal_stop"])
        self.assertIsNone(report["evaluation_cohort"])
        self.assertFalse(report["new_scores_computed"])
        self.assertFalse(report["new_molecular_inputs_acquired"])
        self.assertEqual(len(report["new_exposed_source_identifiers"]), 25)
        expected = {
            "CHEMBL3382763": ("IC50", 15, 6, 2, 7),
            "CHEMBL3705057": ("Ki", 10, 10, 0, 0),
        }
        for assay, (kind, total, positives, weak, unclassified) in expected.items():
            current = report["assessments"][assay]
            counts = current["endpoints"][kind]
            self.assertEqual(current["n_rows"], total)
            self.assertEqual(
                (
                    counts["n_positive_identifiers"],
                    counts["n_weak_identifiers"],
                    counts["n_unclassified_identifiers"],
                ),
                (positives, weak, unclassified),
            )
            self.assertFalse(counts["population_upper_bound_passes"])
        # Independently transcribed from Table 1's ERalpha column in the author
        # manuscript (uM -> nM), and Example 6/Table 2's ERalpha Ki column.
        numeric_oracles = {
            "CHEMBL3382763": [230, 1100, 140, 150, 40, 1470, 18000, 8, 5.7, 61, 13000],
            "CHEMBL3705057": [3.75, 3.81, 21.7, 7.13, 9, 6.06, 13, 14.79, 15, 15.12],
        }
        for assay, expected_values in numeric_oracles.items():
            source = json.loads(
                (driver.DATA / f"{assay}.activities.page0.json").read_text()
            )["activities"]
            self.assertEqual(
                sorted(
                    float(r["standard_value"])
                    for r in source
                    if r["standard_value"] is not None
                ),
                sorted(expected_values),
            )
        first = report["assessments"]["CHEMBL3382763"]["ledger"]
        duplicate = next(
            r for r in first if r["source"]["molecule_chembl_id"] == "CHEMBL135"
        )
        self.assertIsNone(duplicate["label"])
        self.assertEqual(sum(r["source"]["standard_value"] is None for r in first), 4)
