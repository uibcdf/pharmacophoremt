"""Offline independent checks of the prospective carbonyl receiving design."""

import hashlib
import itertools
import json
import math
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data/carbonyl_acceptor_receiving"
PLAN = json.loads((DATA / "plan.json").read_text())


def product(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector, strict=True)) for row in matrix]


class TestCarbonylAcceptorPlan(unittest.TestCase):
    def test_frozen_identity_and_zero_execution(self):
        self.assertEqual(
            hashlib.sha256((DATA / "plan.json").read_bytes()).hexdigest(),
            "b0af26640c0b7ff6cadde2c7f7e499141921adc29fd2ec7f4c1666218be92340",
        )
        self.assertEqual(
            hashlib.sha256((DATA / "provider_review.json").read_bytes()).hexdigest(),
            PLAN["provider_review_sha256"],
        )
        review = json.loads((DATA / "provider_review.json").read_text())
        self.assertEqual(review["provider_commit"], PLAN["provider_commit"])
        self.assertEqual(
            review["source_contract"]["stability"].split(",")[0], "experimental"
        )
        self.assertEqual(review["new_models"], 0)
        self.assertEqual(review["new_pose_evaluations"], 0)
        self.assertEqual(review["provider_tests_executed_in_this_stage"], 0)
        self.assertIsNone(PLAN["measured_results"])
        self.assertEqual(PLAN["measured_models"], 0)
        self.assertEqual(PLAN["measured_pose_evaluations"], 0)
        self.assertFalse(PLAN["holdout_access"])

    def test_paired_workload_and_separate_recovery_denominators(self):
        rows = PLAN["matrix"]
        self.assertEqual(len(rows), len({r["id"] for r in rows}))
        self.assertEqual(
            {(r["policy_id"], r["structure_position"]) for r in rows},
            set(itertools.product(["nm", "pm"], range(3))),
        )
        self.assertEqual(sum(r["expected_returned_models"] for r in rows), 12)
        self.assertEqual(sum(r["expected_primary_evaluations"] for r in rows), 72)
        self.assertEqual(sum(r["expected_recovery_evaluations"] for r in rows), 24)
        self.assertTrue(
            all(
                r["source_structure_index"] == [0, 1, 0][r["structure_position"]]
                for r in rows
            )
        )
        counts = PLAN["planned_counts"]
        self.assertEqual(counts["positive_provider_direction_calls"], 2)
        self.assertEqual(counts["negative_provider_direction_calls"], 4)
        self.assertEqual(counts["negative_pose_evaluations"], 0)
        supplemental = PLAN["supplemental_optional_attribution"]
        self.assertTrue(supplemental["separate_from_primary_denominators"])
        self.assertEqual(supplemental["each_primary_evaluations"], 12)

    def test_declared_analytic_angles_and_sparse_repeated_source_maps(self):
        source = PLAN["source"]
        directions = source["directions"]["values"]
        h = math.sqrt(3) / 2
        self.assertEqual(directions[:2], [[0.5, h, 0], [0.5, -h, 0]])
        for direction in directions:
            self.assertAlmostEqual(sum(x * x for x in direction), 1, places=14)
        self.assertEqual(source["selection"], [2])
        self.assertEqual(source["support_atom_indices"], [2, 1, 0])
        self.assertEqual(source["support_atom_offsets"], [0, 3])
        self.assertEqual(source["site_models"], [2])
        self.assertEqual(source["site_roles"], [1])
        self.assertEqual(source["direction_structure_indices"], [0, 0, 1, 1, 0, 0])
        self.assertEqual(source["direction_structure_positions"], [0, 0, 1, 1, 2, 2])
        self.assertEqual(source["direction_indices"], [0, 1] * 3)
        self.assertEqual(source["status"], [[1], [1], [1]])
        self.assertEqual(source["expected_image_offsets"], list(range(0, 19, 3)))
        self.assertEqual(source["expected_image_vectors"], [[0, 0, 0]] * 18)

    def test_proper_rotation_and_declared_frames_are_independent_oracles(self):
        source = PLAN["source"]
        base, moved = source["coordinates"]["values"]
        transform = source["frame_transforms"][1]
        matrix = transform["rotation"]
        for first, second in zip(base, moved, strict=True):
            expected = [
                a + b
                for a, b in zip(
                    product(matrix, first),
                    transform["translation"]["values"],
                    strict=True,
                )
            ]
            self.assertLess(math.dist(expected, second), 1e-14)
        for first, second in zip(
            source["directions"]["values"][:2],
            source["directions"]["values"][2:4],
            strict=True,
        ):
            self.assertLess(math.dist(product(matrix, first), second), 1e-14)
        rotations = [
            matrix,
            *PLAN["candidate"]["rotations_from_x_to_target"],
            PLAN["candidate"]["reversed_axis_rotation"],
        ]
        for r in rotations:
            for i, j in itertools.product(range(3), repeat=2):
                self.assertAlmostEqual(
                    sum(a * b for a, b in zip(r[i], r[j], strict=True)),
                    int(i == j),
                    places=14,
                )
            determinant = sum(
                r[0][i]
                * (
                    r[1][(i + 1) % 3] * r[2][(i + 2) % 3]
                    - r[1][(i + 2) % 3] * r[2][(i + 1) % 3]
                )
                for i in range(3)
            )
            self.assertAlmostEqual(determinant, 1, places=14)

    def test_lobes_are_alternatives_with_declared_donor_orientation(self):
        query = PLAN["query"]
        self.assertEqual(query["sites_per_model"], 1)
        self.assertEqual(query["choices_per_source_feature"], 2)
        self.assertEqual(query["target_feature_kind"], "hb donor")
        self.assertTrue(query["essential"])
        self.assertEqual(query["weight"], 1)
        self.assertIn(
            "Explicit pharmacophoric choice -u", query["target_direction_rule"]
        )
        for matrix, direction in zip(
            PLAN["candidate"]["rotations_from_x_to_target"],
            PLAN["source"]["directions"]["values"][:2],
            strict=True,
        ):
            self.assertLess(
                math.dist(product(matrix, [1, 0, 0]), [-v for v in direction]), 1e-14
            )
        u, v = PLAN["source"]["directions"]["values"][:2]
        self.assertGreater(0.35 * math.dist(u, v), 2 * 0.02)

    def test_all_unfavorable_controls_remain_valid_negative_predictions(self):
        controls = PLAN["controls"]
        self.assertEqual(len(controls), 6)
        self.assertEqual(
            {c["id"] for c in controls},
            {
                f"lobe{i}_{kind}"
                for i, kind in itertools.product(
                    range(2), ["aligned", "reversed", "displaced"]
                )
            },
        )
        for c in controls:
            aligned = c["id"].endswith("_aligned")
            self.assertEqual(
                c["expected_fits"],
                [int(aligned and i == c["source_lobe"]) for i in range(2)],
            )
            if c["id"].endswith("_displaced"):
                self.assertGreater(
                    math.dist(c["displacement"]["values"], [0, 0, 0]), 0.02
                )
            if c["id"].endswith("_reversed"):
                self.assertEqual(c["donor_axis_sign"], 1)

    def test_unsupported_acceptor_cannot_borrow_observed_donor_direction(self):
        water, undefined = PLAN["negative_sources"]
        self.assertEqual(water["site_roles"], [0, 1])
        self.assertEqual(water["status"], [[1, 0]])
        self.assertEqual(water["donor_direction_records"], 1)
        self.assertEqual(water["acceptor_status"], 0)
        self.assertEqual(undefined["site_models"], [2])
        self.assertEqual(undefined["acceptor_status"], 2)
        for source in [water, undefined]:
            self.assertEqual(source["acceptor_direction_records"], 0)
            self.assertEqual(source["expected_models"], 0)
            self.assertEqual(source["expected_pose_evaluations"], 0)
            self.assertIsNone(source["score"])

    def test_units_ownership_and_scientific_scope_are_explicit(self):
        self.assertEqual(PLAN["molecular_operations_owner"], "molsysmt")
        self.assertFalse(PLAN["pbc"])
        self.assertEqual(PLAN["chemical_state"], "reference")
        self.assertEqual(PLAN["source"]["coordinates"]["unit"], "nm")
        self.assertEqual(PLAN["source"]["directions"]["unit"], "dimensionless")
        self.assertEqual(
            PLAN["query"]["direction_tolerance"], {"unit": "degrees", "values": 1}
        )
        self.assertEqual(PLAN["phase"], "prespecified_not_executed")
        self.assertIn("New public/default acceptor profile", PLAN["exclusions"])


if __name__ == "__main__":
    unittest.main()
