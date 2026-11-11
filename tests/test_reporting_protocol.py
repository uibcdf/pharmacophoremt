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
                "uibcdf/pharmacophoremt#4",
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
                "uibcdf/pharmacophoremt#56",
                "uibcdf/pharmacophoremt#57",
                "uibcdf/pharmacophoremt#58",
                "uibcdf/pharmacophoremt#59",
                "uibcdf/pharmacophoremt#60",
                "uibcdf/pharmacophoremt#61",
                "uibcdf/pharmacophoremt#62",
                "uibcdf/pharmacophoremt#63",
                "uibcdf/pharmacophoremt#64",
                "uibcdf/pharmacophoremt#65",
                "uibcdf/pharmacophoremt#66",
                "uibcdf/pharmacophoremt#69",
                "uibcdf/pharmacophoremt#73",
                "uibcdf/pharmacophoremt#74",
                "uibcdf/pharmacophoremt#75",
                "uibcdf/pharmacophoremt#76",
                "uibcdf/pharmacophoremt#77",
                "uibcdf/pharmacophoremt#78",
                "uibcdf/pharmacophoremt#79",
                "uibcdf/pharmacophoremt#80",
                "uibcdf/pharmacophoremt#81",
                "uibcdf/pharmacophoremt#82",
                "uibcdf/pharmacophoremt#83",
                "uibcdf/pharmacophoremt#84",
                "uibcdf/pharmacophoremt#85",
                "uibcdf/pharmacophoremt#86",
                "uibcdf/pharmacophoremt#87",
                "uibcdf/pharmacophoremt#88",
                "uibcdf/pharmacophoremt#89",
                "uibcdf/pharmacophoremt#90",
                "uibcdf/pharmacophoremt#91",
                "uibcdf/pharmacophoremt#92",
                "uibcdf/pharmacophoremt#93",
                "uibcdf/pharmacophoremt#94",
                "uibcdf/pharmacophoremt#96",
                "uibcdf/pharmacophoremt#97",
                "uibcdf/pharmacophoremt#98",
                "uibcdf/pharmacophoremt#99",
                "uibcdf/pharmacophoremt#100",
                "uibcdf/pharmacophoremt#101",
                "uibcdf/pharmacophoremt#102",
                "uibcdf/pharmacophoremt#103",
                "uibcdf/pharmacophoremt#104",
                "uibcdf/pharmacophoremt#105",
                "uibcdf/pharmacophoremt#106",
                "uibcdf/pharmacophoremt#107",
                "uibcdf/pharmacophoremt#108",
                "uibcdf/pharmacophoremt#128",
                "uibcdf/pharmacophoremt#140",
                "uibcdf/pharmacophoremt#141",
                "uibcdf/pharmacophoremt#142",
                "uibcdf/pharmacophoremt#143",
                "uibcdf/pharmacophoremt#144",
                "uibcdf/pharmacophoremt#145",
                "uibcdf/pharmacophoremt#146",
                "uibcdf/pharmacophoremt#147",
                "uibcdf/pharmacophoremt#148",
                "uibcdf/pharmacophoremt#149",
                "uibcdf/pharmacophoremt#150",
                "uibcdf/pharmacophoremt#151",
                "uibcdf/pharmacophoremt#152",
                "uibcdf/pharmacophoremt#153",
                "uibcdf/pharmacophoremt#154",
                "uibcdf/pharmacophoremt#155",
                "uibcdf/pharmacophoremt#156",
                "uibcdf/pharmacophoremt#157",
                "uibcdf/pharmacophoremt#158",
                "uibcdf/pharmacophoremt#159",
                "uibcdf/pharmacophoremt#160",
                "uibcdf/pharmacophoremt#161",
                "uibcdf/pharmacophoremt#162",
                "uibcdf/pharmacophoremt#163",
                "uibcdf/pharmacophoremt#164",
                "uibcdf/pharmacophoremt#165",
                "uibcdf/pharmacophoremt#166",
                "uibcdf/pharmacophoremt#167",
                "uibcdf/pharmacophoremt#168",
                "uibcdf/pharmacophoremt#169",
                "uibcdf/pharmacophoremt#170",
                "uibcdf/pharmacophoremt#171",
                "uibcdf/pharmacophoremt#172",
                "uibcdf/pharmacophoremt#173",
                "uibcdf/pharmacophoremt#174",
                "uibcdf/pharmacophoremt#175",
                "uibcdf/pharmacophoremt#177",
                "uibcdf/pharmacophoremt#178",
                "uibcdf/pharmacophoremt#179",
                "uibcdf/pharmacophoremt#180",
                "uibcdf/pharmacophoremt#181",
                "uibcdf/pharmacophoremt#182",
                "uibcdf/pharmacophoremt#183",
                "uibcdf/pharmacophoremt#184",
                "uibcdf/pharmacophoremt#185",
                "uibcdf/pharmacophoremt#186",
                "uibcdf/pharmacophoremt#187",
                "uibcdf/pharmacophoremt#188",
                "uibcdf/pharmacophoremt#189",
                "uibcdf/pharmacophoremt#190",
                "uibcdf/pharmacophoremt#191",
                "uibcdf/pharmacophoremt#192",
                "uibcdf/pharmacophoremt#193",
                "uibcdf/pharmacophoremt#194",
                "uibcdf/pharmacophoremt#195",
                "uibcdf/pharmacophoremt#196",
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
