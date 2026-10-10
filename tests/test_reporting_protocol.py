"""Exercise the issue-backed reporting guard without scientific dependencies."""

from __future__ import annotations

import importlib
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "devtools"))
devguide_reports = importlib.import_module("devguide_reports")


class TestReportingProtocol(unittest.TestCase):
    def test_existing_reports_have_valid_metadata_and_generated_indexes(self):
        reports, errors = devguide_reports.validate_all()
        self.assertEqual(errors, [])
        self.assertEqual(
            {report.fields["issue"] for report in reports},
            {
                "uibcdf/pharmacophoremt#2",
                "uibcdf/pharmacophoremt#10",
                "uibcdf/pharmacophoremt#12",
                "uibcdf/pharmacophoremt#13",
                "uibcdf/pharmacophoremt#14",
                "uibcdf/pharmacophoremt#15",
                "uibcdf/pharmacophoremt#16",
                "uibcdf/pharmacophoremt#17",
                "uibcdf/pharmacophoremt#18",
                "uibcdf/pharmacophoremt#19",
                "uibcdf/pharmacophoremt#20",
                "uibcdf/pharmacophoremt#21",
                "uibcdf/pharmacophoremt#22",
                "uibcdf/pharmacophoremt#23",
                "uibcdf/pharmacophoremt#24",
                "uibcdf/pharmacophoremt#25",
                "uibcdf/pharmacophoremt#26",
                "uibcdf/pharmacophoremt#27",
                "uibcdf/pharmacophoremt#28",
                "uibcdf/pharmacophoremt#29",
                "uibcdf/pharmacophoremt#30",
                "uibcdf/pharmacophoremt#31",
                "uibcdf/pharmacophoremt#32",
                "uibcdf/pharmacophoremt#33",
                "uibcdf/pharmacophoremt#34",
                "uibcdf/pharmacophoremt#35",
                "uibcdf/pharmacophoremt#36",
                "uibcdf/pharmacophoremt#37",
                "uibcdf/pharmacophoremt#38",
                "uibcdf/pharmacophoremt#39",
                "uibcdf/pharmacophoremt#41",
                "uibcdf/pharmacophoremt#42",
                "uibcdf/pharmacophoremt#44",
                "uibcdf/pharmacophoremt#45",
                "uibcdf/pharmacophoremt#46",
                "uibcdf/pharmacophoremt#47",
                "uibcdf/pharmacophoremt#48",
                "uibcdf/pharmacophoremt#49",
                "uibcdf/pharmacophoremt#50",
                "uibcdf/pharmacophoremt#51",
                "uibcdf/pharmacophoremt#52",
                "uibcdf/pharmacophoremt#53",
                "uibcdf/pharmacophoremt#54",
                "uibcdf/pharmacophoremt#55",
                "uibcdf/pharmacophoremt#5",
                "uibcdf/pharmacophoremt#6",
                "uibcdf/pharmacophoremt#8",
                "uibcdf/pharmacophoremt#9",
            },
        )
        result = subprocess.run(
            [sys.executable, "devtools/devguide_index.py", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_issue_and_false_closure_are_rejected(self):
        reports, _ = devguide_reports.validate_all()
        pending = next(
            report
            for report in reports
            if report.fields["issue"] == "uibcdf/pharmacophoremt#6"
        )
        fields = dict(pending.fields)
        fields["issue"] = ""
        fields["status"] = "resolved"
        fields["closed"] = ""
        fields["guard"] = ""
        fields["normative"] = ""
        invalid = devguide_reports.Report(
            pending.path, fields, pending.kind, pending.archived
        )
        errors = devguide_reports.validate_report(invalid)
        self.assertTrue(any("issue must be" in error for error in errors))
        self.assertTrue(any("closed reports belong" in error for error in errors))
        self.assertTrue(any("requires an ISO closed date" in error for error in errors))
        self.assertTrue(any("requires guard or normative" in error for error in errors))

    def test_guard_selectors_are_addressable(self):
        self.assertEqual(
            devguide_reports.validate_guard(
                "tests/test_validation_eralpha.py::test_eralpha_pharmacophore_extraction_requires_native_observations"
            ),
            [],
        )
        self.assertTrue(
            devguide_reports.validate_guard("tests/test_import.py::test_missing")
        )
        self.assertTrue(devguide_reports.validate_guard("python arbitrary_command.py"))


if __name__ == "__main__":
    unittest.main()
