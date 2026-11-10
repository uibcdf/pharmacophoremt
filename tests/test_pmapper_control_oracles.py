"""Independent exact input witnesses, with no pmapper or scientific imports."""

import json
import unittest
from fractions import Fraction

from phmt_test_support.pmapper_controls import (
    DIRECTORY,
    load_declaration,
    rational_oracles,
    squared_distance,
)


class TestPmapperOracles(unittest.TestCase):
    def test_frozen_input_identity_and_explicit_unit(self):
        data = load_declaration()
        self.assertEqual(
            (data["case_id"], data["unit"]), ("pmapper-stage-controls-v1", "angstrom")
        )
        self.assertEqual(len({r["key"] for r in data["cases"]}), 8)
        self.assertEqual(json.loads((DIRECTORY / "declaration.json").read_text()), data)

    def test_same_bin_gap_proves_no_placement_with_the_declared_radius(self):
        result = rational_oracles(load_declaration())
        self.assertEqual(Fraction(result["same_bin_pair_gap_angstrom"]), Fraction(1, 2))
        self.assertGreater(Fraction(1, 2), 2 * Fraction(1, 16))

    def test_cross_bin_placement_is_strictly_inside_every_radius(self):
        result = rational_oracles(load_declaration())
        for value in result["cross_bin_squared_deviations_angstrom2"]:
            self.assertEqual(Fraction(value), Fraction(1, 256))
            self.assertLess(Fraction(value), Fraction(1, 8) ** 2)

    def test_reflection_preserves_all_distances_and_changes_handedness(self):
        case = next(
            r
            for r in load_declaration()["cases"]
            if r["key"] == "noncoplanar-reflection"
        )
        for i in range(4):
            for j in range(i):
                self.assertEqual(
                    squared_distance(case["query"][i][1], case["query"][j][1]),
                    squared_distance(case["source"][i][1], case["source"][j][1]),
                )
        result = rational_oracles(load_declaration())
        self.assertEqual(
            Fraction(result["reflection_reference_determinant_angstrom3"]),
            -Fraction(result["reflection_source_determinant_angstrom3"]),
        )

    def test_permutation_preserves_literal_feature_occurrences(self):
        data = load_declaration()
        proper = next(r for r in data["cases"] if r["key"] == "proper-motion")
        permuted = next(r for r in data["cases"] if r["key"] == "permuted-motion")
        self.assertEqual(permuted["source"], [proper["source"][i] for i in (2, 0, 1)])
        duplicate = next(r for r in data["cases"] if r["key"] == "duplicate-occurrence")
        self.assertEqual(duplicate["source"][0], duplicate["source"][-1])
        self.assertEqual(len(duplicate["source"]), 4)
