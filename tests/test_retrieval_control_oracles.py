"""Independent finite geometry, identity, invalidation and incomplete-work guards."""

import unittest
from copy import deepcopy
from fractions import Fraction

from phmt_test_support.retrieval_controls import (
    StudyIndex,
    binding,
    distance_bin,
    exact_mapping_oracle,
    load_declaration,
)


class TestRetrievalControls(unittest.TestCase):
    def setUp(self):
        self.data = load_declaration()
        self.records = self.data["records"]
        self.settings = binding(self.data, 1.0)
        self.index = StudyIndex(self.records, self.settings)
        self.query = self.data["queries"][0]

    def lookup(self, query=None, **kwargs):
        return self.index.lookup(
            query or self.query,
            current_records=self.records,
            current_binding=self.settings,
            **kwargs,
        )

    def test_exact_rational_bins_include_irrational_lengths_without_float_sqrt(self):
        self.assertEqual(distance_bin([0, 0, 0], [3, 4, 0], 0.5), 10)
        self.assertLess(Fraction(11, 8) ** 2, 2)
        self.assertGreater(Fraction(12, 8) ** 2, 2)
        self.assertEqual(distance_bin([0, 0, 0], [1, 1, 0], 0.125), 11)

    def test_independent_pair_neighborhood_contains_exact_axis_witnesses(self):
        for width in self.data["bin_widths"]:
            for first in range(33):
                for second in range(33):
                    a, b = Fraction(first, 16), Fraction(second, 16)
                    if abs(a - b) <= Fraction(1, 4):
                        difference = abs(
                            distance_bin([0, 0, 0], [a, 0, 0], width)
                            - distance_bin([0, 0, 0], [b, 0, 0], width)
                        )
                        self.assertLessEqual(
                            difference, 2
                        )  # widest required ceil((1/4)/(1/8))
                        span = -(
                            -(Fraction(1, 4) / Fraction(width)).numerator
                            // (Fraction(1, 4) / Fraction(width)).denominator
                        )
                        self.assertLessEqual(difference, span)

    def test_cross_bin_physical_witness_survives_conservative_lookup(self):
        query = next(
            q for q in self.data["queries"] if q["key"] == "cross-bin-feasible"
        )
        ordinal = next(
            i
            for i, r in enumerate(self.records)
            if r["occurrence_key"] == "source:cross-bin-feasible"
        )
        self.assertEqual(
            exact_mapping_oracle(query, self.records[ordinal]),
            [[[0, 0], [1, 1], [2, 2]]],
        )
        self.assertIn(ordinal, self.lookup(query)["candidate_ordinals"])
        self.assertNotIn(
            ordinal, self.lookup(query, exact_bin=True)["candidate_ordinals"]
        )

    def test_same_bin_impossibility_is_a_prefilter_false_positive(self):
        ordinal = next(
            i
            for i, r in enumerate(self.records)
            if r["occurrence_key"] == "source:same-bin-impossible"
        )
        self.assertIn(ordinal, self.lookup()["candidate_ordinals"])
        self.assertEqual(exact_mapping_oracle(self.query, self.records[ordinal]), [])
        self.assertGreater(Fraction(1, 2), 2 * Fraction(self.query["tolerance"]))

    def test_duplicate_feature_occurrences_preserve_both_literal_mappings(self):
        record = next(
            r
            for r in self.records
            if r["occurrence_key"] == "source:duplicate-occurrence"
        )
        self.assertEqual(
            exact_mapping_oracle(self.query, record),
            [[[0, 0], [1, 1], [2, 2]], [[0, 3], [1, 1], [2, 2]]],
        )
        keys = [
            (r["source_key"], r["occurrence_key"]) for r in self.index.stored_records()
        ]
        self.assertIn(("same/source", "repeat=α"), keys)
        self.assertEqual(len(set(keys)), 12)

    def test_reflection_is_a_distance_proposal_with_original_feature_ids(self):
        query = next(
            q for q in self.data["queries"] if q["key"] == "noncoplanar-reflection"
        )
        record = next(
            r
            for r in self.records
            if r["occurrence_key"] == "source:noncoplanar-reflection"
        )
        self.assertEqual(
            exact_mapping_oracle(query, record), [[[i, i] for i in range(4)]]
        )

    def test_empty_library_is_completed_empty_without_an_activity_claim(self):
        index = StudyIndex([], self.settings)
        result = index.lookup(
            self.query, current_records=[], current_binding=self.settings
        )
        self.assertTrue(result["complete"])
        self.assertFalse(result["unseen_outcomes_are_unknown"])
        self.assertEqual(result["candidate_ordinals"], [])

    def test_stored_data_and_binding_are_detached_from_the_caller(self):
        before = self.index.stored_records()
        returned = self.index.stored_records()
        returned[0]["features"][0][1][0] = 5
        self.assertEqual(before, self.index.stored_records())
        self.records[0]["features"][0][1][0] = 0.5
        with self.assertRaises(ValueError):
            self.lookup()
        self.assertEqual(before, self.index.stored_records())

    def test_coordinate_label_and_occurrence_changes_refuse_stale_reuse(self):
        for kind in ("coordinate", "label", "occurrence", "order"):
            changed = deepcopy(self.records)
            if kind == "coordinate":
                changed[0]["features"][1][1][0] = 2.25
            elif kind == "label":
                changed[0]["features"][0][0] = "A"
            elif kind == "occurrence":
                changed[0]["occurrence_key"] = "other"
            else:
                changed.reverse()
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                self.index.lookup(
                    self.query, current_records=changed, current_binding=self.settings
                )
            fresh = StudyIndex(changed, self.settings)
            self.assertTrue(
                fresh.lookup(
                    self.query, current_records=changed, current_binding=self.settings
                )["complete"]
            )

    def test_units_frames_definitions_snapshots_and_settings_invalidate_reuse(self):
        for key, new in (
            ("unit", "nm"),
            ("frame", "changed"),
            ("feature_definition", "other@1"),
            ("prepared_snapshot", "other"),
            ("representation", "other"),
            ("producer", "other"),
            ("bin_width", 0.5),
            ("numerical_guard_bins", 2),
            ("anchor_feature_indices", [1, 2]),
        ):
            changed = deepcopy(self.settings)
            changed[key] = new
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.index.lookup(
                    self.query, current_records=self.records, current_binding=changed
                )

    def test_lookup_budget_exposes_unknown_bins_instead_of_an_empty_negative(self):
        result = self.lookup(max_lookup_bins=1)
        self.assertFalse(result["complete"])
        self.assertTrue(result["unseen_outcomes_are_unknown"])
        self.assertIsNotNone(result["unsearched_bin_interval"])
        self.assertEqual(len(result["searched_bins"]), 1)

    def test_candidate_budget_retains_known_pending_original_ordinals(self):
        complete = self.lookup()
        partial = self.lookup(max_candidates=1)
        self.assertFalse(partial["complete"])
        self.assertTrue(partial["unseen_outcomes_are_unknown"])
        self.assertEqual(
            partial["candidate_ordinals"] + partial["pending_candidate_ordinals"],
            complete["candidate_ordinals"],
        )
        self.assertEqual(partial["unsearched_bin_interval"], None)

    def test_unsupported_sizes_nonfinite_points_and_duplicate_keys_are_refused(self):
        for records in (
            self.records + [deepcopy(self.records[0])],
            [self.records[0], self.records[0]],
        ):
            with self.assertRaises(ValueError):
                StudyIndex(records, self.settings)
        for invalid in (float("nan"), float("inf"), 17, True):
            changed = deepcopy(self.records)
            changed[0]["features"][0][1][0] = invalid
            with self.assertRaises(ValueError):
                StudyIndex(changed, self.settings)
        with self.assertRaises(ValueError):
            self.lookup(max_lookup_bins=65)
