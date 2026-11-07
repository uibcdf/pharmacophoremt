"""Independent boundary and custody controls for the prospective BRD4 capacity case."""

from __future__ import annotations

import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from devtools import brd4_label_capacity as capacity
from devtools.brd4_label_capacity import CsvLayout, classify_ic50, project_csv

HEADER = (
    "PUBCHEM_RESULT_TAG",
    "PUBCHEM_SID",
    "PUBCHEM_CID",
    "Standard Type",
    "Standard Relation",
    "PubChem Standard Value",
    "PUBCHEM_ACTIVITY_OUTCOME",
    "IC50",
)
LAYOUT = CsvLayout(
    HEADER,
    {"sid": 1, "cid": 2, "type": 3, "relation": 4, "value": 5},
)


def source_rows():
    # Synthetic distinct source IDs do not purport to be independent molecules.
    rows = []
    for sid in range(1, 500):
        value = "0.5" if sid <= 50 else "6" if sid <= 100 else "1"
        rows.append(
            [
                str(sid),
                str(sid),
                str((sid - 1) % 494 + 1),
                "IC50",
                "=",
                value,
                "Inactive",
                "999",
            ]
        )
    return rows


def csv_text(rows, *, header=HEADER, metadata_rows=()):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(header)
    writer.writerows(metadata_rows)
    writer.writerows(rows)
    return stream.getvalue()


class TestBrd4LabelCapacity(unittest.TestCase):
    def test_cli_refuses_oversized_source_without_an_unbounded_read(self):
        limit = 2 * 1024 * 1024
        calls = []

        class BoundedSource(io.BytesIO):
            def read(self, size=-1):
                if not 0 < size <= limit + 1:
                    raise AssertionError("private source read was not bounded")
                calls.append(size)
                return super().read(size)

        with tempfile.TemporaryDirectory() as directory:
            csv_path = Path(directory) / "oversized.csv"
            original_open = Path.open

            def guarded_open(path, *args, **kwargs):
                if path == csv_path:
                    return BoundedSource(b"x" * (limit + 1))
                return original_open(path, *args, **kwargs)

            with patch.object(Path, "open", guarded_open):
                with self.assertRaisesRegex(ValueError, "two-MiB"):
                    capacity.main([str(csv_path), str(Path(directory) / "layout.json")])
        self.assertEqual(calls, [limit + 1])

    def test_cli_checks_frozen_plan_before_opening_the_private_source(self):
        with tempfile.TemporaryDirectory() as directory:
            changed_plan = Path(directory) / "changed-plan.json"
            changed_plan.write_text("{}", encoding="utf-8")
            with patch.object(capacity, "PLAN_PATH", changed_plan):
                with self.assertRaisesRegex(ValueError, "immutable.*plan has changed"):
                    capacity.main(
                        [
                            str(Path(directory) / "unavailable-private.csv"),
                            str(Path(directory) / "unavailable-layout.json"),
                        ]
                    )

    def test_interval_boundaries_do_not_impute_censored_values(self):
        cases = {
            ("=", "0.5"): "strong",
            ("<=", "0.5"): "strong",
            ("<", "0.5"): "strong",
            ("=", "0.5000000000000000000000000000000001"): "intermediate",
            ("<=", "0.5000000000000000000000000000000001"): "class_ambiguous",
            ("=", "5"): "intermediate",
            (">", "5"): "weak",
            (">=", "5"): "class_ambiguous",
            (">", "0.5"): "class_ambiguous",
            ("<", "5"): "class_ambiguous",
            (">=", "5.000000000000000000000000000000001"): "weak",
            ("=", "5e-1"): "strong",
        }
        for (relation, value), expected in cases.items():
            with self.subTest(relation=relation, value=value):
                self.assertEqual(classify_ic50("IC50", relation, value), expected)

    def test_missing_invalid_and_unsupported_are_not_weak_labels(self):
        for value in ("0", "-1", "NaN", "Infinity", "1_0", "0.5 uM", "--1"):
            with self.subTest(value=value):
                self.assertEqual(classify_ic50("IC50", "=", value), "invalid")
        self.assertEqual(classify_ic50("IC50", "=", " "), "missing")
        self.assertEqual(classify_ic50("IC50", "", "5"), "missing")
        self.assertEqual(classify_ic50("KD", "=", "10"), "unsupported_type")
        self.assertEqual(classify_ic50("IC50", "~", "10"), "unsupported_relation")

    def test_complete_capacity_ignores_upstream_flags_and_raw_other_values(self):
        result = project_csv(csv_text(source_rows()), LAYOUT)
        self.assertEqual(
            result["eligible_sid_upper_bounds"], {"strong": 50, "weak": 50}
        )
        self.assertEqual(result["row_status_counts"]["intermediate"], 399)
        self.assertEqual(result["rows"], 499)
        self.assertEqual(result["distinct_cids"], 494)
        self.assertEqual(result["decision"], "capacity_permits_further_admission")
        self.assertFalse(result["independent_groups_qualified"])
        serialized = json.dumps(result)
        self.assertNotIn("PUBCHEM_SID", serialized)
        self.assertNotIn("Inactive", serialized)

    def test_duplicate_rows_do_not_increase_capacity_and_conflicts_stop(self):
        rows = source_rows()
        rows.append(list(rows[0]))
        conflicting = list(rows[50])
        conflicting[5] = "0.2"
        rows.append(conflicting)
        result = project_csv(csv_text(rows), LAYOUT)
        self.assertEqual(result["rows"], 501)
        self.assertEqual(result["duplicate_sids"], 2)
        self.assertEqual(result["extra_duplicate_rows"], 2)
        self.assertEqual(result["conflicting_label_sids"], 1)
        self.assertEqual(
            result["eligible_sid_upper_bounds"], {"strong": 50, "weak": 49}
        )
        self.assertEqual(result["decision"], "stop_insufficient_raw_capacity")

    def test_mixed_unknowns_and_inconsistent_source_mapping_are_not_promoted(self):
        rows = source_rows()
        unresolved = list(rows[0])
        unresolved[5] = ""
        rows.append(unresolved)
        inconsistent = list(rows[1])
        inconsistent[2] = "400"
        rows.append(inconsistent)
        result = project_csv(csv_text(rows), LAYOUT)
        self.assertEqual(result["eligible_sid_upper_bounds"]["strong"], 48)
        self.assertEqual(result["mixed_status_sids"], 1)
        self.assertEqual(result["conflicting_cid_sids"], 1)
        self.assertEqual(result["row_status_counts"]["missing"], 1)

    def test_missing_cid_remains_counted_but_not_eligible(self):
        rows = source_rows()
        # CID1 is also present in SID495, so the source count stays494.
        rows[0][2] = ""
        result = project_csv(csv_text(rows), LAYOUT)
        self.assertEqual(result["missing_cid_rows"], 1)
        self.assertEqual(result["eligible_sid_upper_bounds"]["strong"], 49)

    def test_unreviewed_metadata_or_header_schema_is_not_silently_skipped(self):
        metadata = (("RESULT_TYPE", "", "", "STRING", "STRING", "FLOAT", "", ""),)
        payload = csv_text(source_rows(), metadata_rows=metadata)
        with self.assertRaisesRegex(ValueError, "identifier"):
            project_csv(payload, LAYOUT)
        explicit = CsvLayout(HEADER, dict(LAYOUT.columns), metadata)
        self.assertEqual(project_csv(payload, explicit)["rows"], 499)
        with self.assertRaisesRegex(ValueError, "metadata"):
            project_csv(csv_text(source_rows()), explicit)
        altered = list(HEADER)
        altered[5] = "IC50 Raw"
        with self.assertRaisesRegex(ValueError, "header differs"):
            project_csv(csv_text(source_rows(), header=altered), LAYOUT)
        with self.assertRaisesRegex(ValueError, "unique"):
            CsvLayout((*HEADER, "PUBCHEM_SID"), dict(LAYOUT.columns))
        with self.assertRaisesRegex(ValueError, "declared value"):
            CsvLayout(HEADER, {**LAYOUT.columns, "value": 7})

    def test_complete_coverage_and_each_row_width_are_required(self):
        with self.assertRaisesRegex(ValueError, "coverage"):
            project_csv(csv_text(source_rows()[:-1]), LAYOUT)
        rows = source_rows()
        rows[-1][2] = "99999"
        with self.assertRaisesRegex(ValueError, "coverage"):
            project_csv(csv_text(rows), LAYOUT)
        rows = source_rows()
        rows[-1].append("unexpected")
        with self.assertRaisesRegex(ValueError, "row width"):
            project_csv(csv_text(rows), LAYOUT)


if __name__ == "__main__":
    unittest.main()
