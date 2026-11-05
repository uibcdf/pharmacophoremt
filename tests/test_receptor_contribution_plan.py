"""Offline scientific-declaration guards; no molecular experiment runs here."""

import hashlib
import itertools
import json
import unittest
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data/receptor_contribution"
PLAN = json.loads((DATA / "plan.json").read_text())
LEDGER = json.loads((DATA / "eligibility.json").read_text())


def rows(block, variant=None, radius=None, budget=None):
    return [
        row
        for row in PLAN["matrix"]
        if row["block"] == block
        and (variant is None or row["variant"] == variant)
        and (radius is None or row["query_radius_nm"] == radius)
        and (budget is None or row["max_hypotheses"] == budget)
    ]


class TestReceptorContributionPlan(unittest.TestCase):
    def test_frozen_identity_and_outcome_independent_region_selection(self):
        self.assertEqual(
            hashlib.sha256((DATA / "plan.json").read_bytes()).hexdigest(),
            "4358f73bf84aa334bf1b69822558860bc1f7cc6c0c071c1ad0dcc58978923981",
        )
        for file_name, key in [
            ("eligibility.json", "eligibility_ledger_sha256"),
            ("eligibility_rule.json", "eligibility_rule_sha256"),
        ]:
            self.assertEqual(
                hashlib.sha256((DATA / file_name).read_bytes()).hexdigest(), PLAN[key]
            )
        self.assertEqual(
            PLAN["native_sha256"],
            "a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a",
        )
        candidates = LEDGER["rows"]
        self.assertEqual(
            [r["group_id"] for r in candidates],
            ["337", "367", "404", "425", "435", "445", "461"],
        )
        self.assertTrue(all(r["status"] == "eligible" for r in candidates))
        others = [r for r in candidates if r["group_id"] != "404"][:2]
        anchor = next(r for r in candidates if r["group_id"] == "404")
        chosen = sorted([anchor, *others], key=lambda r: r["source_group_order"])
        self.assertEqual([r["group_id"] for r in chosen], ["337", "367", "404"])
        self.assertEqual(PLAN["regions"], chosen)
        for region in chosen:
            heavy = set(region["heavy_atom_indices"])
            self.assertEqual(len(heavy), 11)
            self.assertEqual(len(region["ring_atoms"]), 6)
            self.assertEqual(len(region["donor_atoms"]), 2)
            self.assertTrue(set(region["ring_atoms"]) <= heavy)
            self.assertIn(region["donor_atoms"][0], heavy)

    def test_each_paired_factor_cell_occurs_once(self):
        matrix = PLAN["matrix"]
        self.assertEqual(len(matrix), 60)
        self.assertEqual(len({r["id"] for r in matrix}), 60)
        self.assertEqual(
            Counter(r["block"] for r in matrix),
            dict(baseline=36, tolerance=12, budget=12),
        )
        groups = ["337", "367", "404"]
        policies = ["nm", "pm"]
        variants = [
            "donor",
            "ring",
            "joint",
            "joint_ex01",
            "joint_ex20",
            "joint_ex40",
        ]
        self.assertEqual(
            {(r["group_id"], r["policy_id"], r["variant"]) for r in rows("baseline")},
            set(itertools.product(groups, policies, variants)),
        )
        self.assertEqual(
            {
                (r["group_id"], r["policy_id"], r["query_radius_nm"])
                for r in rows("tolerance")
            },
            set(itertools.product(groups, policies, [0.08, 0.12])),
        )
        self.assertEqual(
            {
                (r["group_id"], r["policy_id"], r["max_hypotheses"])
                for r in rows("budget")
            },
            set(itertools.product(groups, policies, [3, 0])),
        )

    def test_scheduled_workload_has_correct_denominators_and_no_imputed_scores(self):
        totals = {}
        for block in ["baseline", "tolerance", "budget"]:
            selected = rows(block)
            returned = sum(r["expected_returned"] for r in selected)
            totals[block] = (len(selected), returned, returned * 5)
        self.assertEqual(
            totals,
            dict(
                baseline=(36, 228, 1140), tolerance=(12, 96, 480), budget=(12, 18, 90)
            ),
        )
        self.assertEqual(PLAN["counts"]["planned_returned_models"], 342)
        self.assertEqual(PLAN["counts"]["planned_primary_pose_evaluations"], 1710)
        self.assertEqual(PLAN["counts"]["zero_budget_unevaluated_candidate_slots"], 30)
        self.assertEqual(PLAN["counts"]["native_representative_models"], 54)
        self.assertEqual(PLAN["counts"]["native_roundtrips"], 108)
        self.assertEqual(PLAN["counts"]["planned_post_recovery_pose_evaluations"], 108)
        for row in PLAN["matrix"]:
            self.assertEqual(
                set(row["expected_positive_fit_values"]), set(PLAN["controls"])
            )
            for values in row["expected_positive_fit_values"].values():
                self.assertEqual(len(values), row["expected_returned"])
            self.assertEqual(
                row["expected_returned"] + row["expected_remaining"],
                row["expected_total_hypotheses"],
            )

    def test_baseline_component_removal_has_analytically_known_answers(self):
        expected = {
            "donor": {
                "intact": {0: 1, 1: 1},
                "donor_displaced": {0: 2},
                "ring_displaced": {0: 1, 1: 1},
                "both_displaced": {0: 2},
                "ring_rotated": {0: 1, 1: 1},
            },
            "ring": {
                "intact": {0: 3, 1: 1},
                "donor_displaced": {0: 3, 1: 1},
                "ring_displaced": {0: 4},
                "both_displaced": {0: 4},
                "ring_rotated": {0: 4},
            },
            "joint": {
                "intact": {0: 3, 0.5: 4, 1: 1},
                "donor_displaced": {0: 6, 0.5: 2},
                "ring_displaced": {0: 4, 0.5: 4},
                "both_displaced": {0: 8},
                "ring_rotated": {0: 4, 0.5: 4},
            },
        }
        for variant, answers in expected.items():
            for row in rows("baseline", variant):
                for control, histogram in answers.items():
                    self.assertEqual(
                        Counter(row["expected_positive_fit_values"][control]), histogram
                    )
                self.assertTrue(row["expected_complete"])

    def test_radius_sensitivity_is_declared_separately_from_exclusions(self):
        for radius, histogram in [(0.08, {0.5: 6, 1: 2}), (0.12, {0.5: 4, 1: 4})]:
            selected = rows("tolerance", radius=radius)
            self.assertEqual(len(selected), 6)
            for row in selected:
                self.assertEqual(row["variant"], "joint")
                self.assertIsNone(row["exclusion_radius_nm"])
                self.assertEqual(
                    Counter(row["expected_positive_fit_values"]["intact"]), histogram
                )

    def test_truncated_prefix_and_zero_budget_do_not_claim_exhausted_negatives(self):
        for row in rows("baseline", "joint"):
            self.assertEqual(row["expected_positive_fit_values"]["intact"][4], 1)
        for row in rows("budget"):
            self.assertFalse(row["expected_complete"])
            self.assertEqual(row["expected_total_hypotheses"], 8)
            values = row["expected_positive_fit_values"]["intact"]
            self.assertNotIn(1, values)
            if row["max_hypotheses"] == 3:
                self.assertEqual(values, [0.5, 0, 0])
                self.assertEqual(row["expected_remaining"], 5)
            else:
                self.assertEqual(values, [])
                self.assertEqual(row["expected_remaining"], 8)

    def test_exclusions_preserve_positive_fits_and_require_independent_clash_oracle(
        self,
    ):
        for row in rows("baseline"):
            if row["exclusion_radius_nm"] is None:
                continue
            base = next(
                b
                for b in rows("baseline", "joint")
                if b["group_id"] == row["group_id"]
                and b["policy_id"] == row["policy_id"]
            )
            self.assertEqual(
                row["expected_positive_fit_values"],
                base["expected_positive_fit_values"],
            )
            self.assertEqual(row["expected_returned"], 8)
            self.assertEqual(
                row["expected_acceptance_rule"],
                "all_positive_sites_matched_and_no_strict_inside_clashes",
            )
            self.assertEqual(
                row["minimum_guaranteed_intact_reference_clash_pairs"],
                7 if row["exclusion_radius_nm"] == 0.4 else None,
            )

    def test_candidate_rotations_and_scope_preserve_the_declared_scientific_limits(
        self,
    ):
        for matrix in PLAN["candidate_definition"]["rotation"]["matrices"]:
            for i in range(3):
                for j in range(3):
                    self.assertEqual(
                        sum(matrix[i][k] * matrix[j][k] for k in range(3)), int(i == j)
                    )
            a, b, c = matrix
            self.assertEqual(
                a[0] * (b[1] * c[2] - b[2] * c[1])
                - a[1] * (b[0] * c[2] - b[2] * c[0])
                + a[2] * (b[0] * c[1] - b[1] * c[0]),
                1,
            )
        self.assertEqual(PLAN["phase"], "prespecified_not_executed")
        self.assertEqual(PLAN["actual_pose_evaluations"], 0)
        self.assertEqual(LEDGER["model_pose_evaluations"], 0)
        self.assertIsNone(PLAN["measured_comparison_results"])
        self.assertFalse(PLAN["holdout_access"])
        self.assertEqual(PLAN["molecular_operations_owner"], "molsysmt")
        self.assertEqual(PLAN["population"]["independent_biological_ligands"], 0)
        self.assertEqual(PLAN["population"]["prepared_input_artifacts"], 1)


if __name__ == "__main__":
    unittest.main()
