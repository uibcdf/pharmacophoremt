"""Offline prospective cardinality and source-selection guards."""

import hashlib
import itertools
import json
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data/tyr_cardinality"
PLAN = json.loads((DATA / "plan.json").read_text())


class TestTyrCardinalityPlan(unittest.TestCase):
    def test_frozen_input_and_outcome_independent_cohort(self):
        self.assertEqual(
            hashlib.sha256((DATA / "plan.json").read_bytes()).hexdigest(),
            "29b62982967e19855c0429716815a2c39f645cea7fd2042be0f86567925aac81",
        )
        for name, key in [
            ("eligibility.json", "eligibility_sha256"),
            ("eligibility_rule.json", "eligibility_rule_sha256"),
        ]:
            self.assertEqual(
                hashlib.sha256((DATA / name).read_bytes()).hexdigest(), PLAN[key]
            )
        ledger = json.loads((DATA / "eligibility.json").read_text())
        eligible = [r for r in ledger["rows"] if r["status"] == "eligible"]
        self.assertEqual([r["group_id"] for r in eligible[:2]], ["328", "331"])
        self.assertEqual(PLAN["regions"], eligible[:2])
        self.assertEqual(ledger["model_pose_evaluations"], 0)
        for row in PLAN["regions"]:
            self.assertEqual(set(row["donor_pairs_by_element"]), {"N", "O"})
            self.assertEqual(len(row["ring_atoms"]), 6)

    def test_complete_paired_matrix_and_planned_denominators(self):
        rows = PLAN["matrix"]
        self.assertEqual(len(rows), len({r["id"] for r in rows}))
        self.assertEqual(
            {(r["group_id"], r["policy_id"], r["variant"]) for r in rows},
            set(
                itertools.product(
                    ["328", "331"], ["nm", "pm"], ["donor", "ring", "joint"]
                )
            ),
        )
        self.assertEqual(sum(r["expected_returned"] for r in rows), 20)
        self.assertEqual(
            sum(r["expected_returned"] * len(PLAN["controls"]) for r in rows), 100
        )
        self.assertEqual(len(rows) * 2, 24)
        self.assertTrue(all(r["expected_complete"] for r in rows))

    def test_one_native_record_cannot_fill_both_essential_acceptor_slots(self):
        for row in PLAN["matrix"]:
            fits = row["expected_positive_fit_values"]
            if row["variant"] == "donor":
                self.assertEqual(fits["intact"], [1])
                self.assertEqual(fits["nitrogen_target_only"], [0.5])
                self.assertEqual(fits["oxygen_target_only"], [0.5])
            if row["variant"] == "joint":
                self.assertEqual(fits["intact"], [1, 2 / 3])
                self.assertEqual(fits["nitrogen_target_only"], [2 / 3, 1 / 3])
                self.assertEqual(fits["ring_only"], [1 / 3, 0])
                self.assertNotIn(1, fits["ring_rotated"])

    def test_no_comparison_outcome_or_biological_claim_is_prespecified_as_measured(
        self,
    ):
        self.assertEqual(PLAN["phase"], "prespecified_not_executed")
        self.assertIsNone(PLAN["measured_comparison_results"])
        self.assertFalse(PLAN["holdout_access"])
        self.assertEqual(PLAN["molecular_operations_owner"], "molsysmt")


if __name__ == "__main__":
    unittest.main()
