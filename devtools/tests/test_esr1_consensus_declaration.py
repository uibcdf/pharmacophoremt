"""Offline pre-score protocol guards; no molecular or network execution."""

from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tarfile
import tempfile
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_file(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


driver = load_file(
    "esr1_declaration_driver", "phmt_test_support/esr1_consensus_declaration.py"
)
reader = load_file("esr1_declaration_reader", "phmt_test_support/evidence_archive.py")


class TestEsr1ConsensusDeclaration(unittest.TestCase):
    def test_frozen_declaration_reconstructs_original_sources_and_excludes_exposed_cids(
        self,
    ):
        path = (
            ROOT / "devguide/evidence/esr1_activity_pilot_inputs_20261023_summary.json"
        )
        _, raw = reader.read_archived_bytes(path)
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
                for name in (
                    "ESR1ago.tar.gz",
                    "aid743075_concise.csv",
                    "aid743075_description.json",
                ):
                    (directory / name).write_bytes(archive.extractfile(name).read())
            declaration = driver.build_declaration(directory)
            self.assertEqual(declaration, json.loads(driver.OUTPUT.read_text()))
            cohort = declaration["cohort"]
            self.assertEqual(len({e["cid"] for e in cohort}), 67)
            self.assertEqual(
                Counter((e["role"], e["label"]) for e in cohort),
                {
                    ("training", 1): 3,
                    ("evaluation", 1): 16,
                    ("evaluation", 0): 48,
                },
            )
            old = json.loads(driver.MANIFEST.read_text())
            self.assertFalse(
                {e["cid"] for e in cohort} & {e["cid"] for e in old["cohort"]}
            )
            self.assertEqual(
                [(e["cid"], e["sid"]) for e in cohort[:3]],
                [
                    ("31477", "144205272"),
                    ("24633", "144209427"),
                    ("6293", "144205039"),
                ],
            )
            self.assertEqual(declaration["selection"]["all_ambiguous_cids"], 370)
            self.assertEqual(declaration["selection"]["excluded_bath_cids"], 4402)
            self.assertEqual(
                declaration["selection"]["eligible_counts"],
                {"Active": 338, "Inactive": 2749},
            )
            self.assertEqual(
                declaration["baseline"]["query_sha256"],
                "c165f3755e1a76603a69f7fd1c24259e8f4706c20407eb3fdf653a4b5f7804f3",
            )
            output = directory / "declaration.json"
            command = [
                sys.executable,
                "-I",
                str(ROOT / "phmt_test_support/esr1_consensus_declaration.py"),
                "--source-dir",
                str(directory),
                "--output",
                str(output),
            ]
            completed = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            before = output.read_bytes()
            repeated = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(repeated.returncode, 0)
            self.assertIn("FileExistsError", repeated.stderr)
            self.assertEqual(before, output.read_bytes())
            (directory / "aid743075_concise.csv").write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "source identity"):
                driver.build_declaration(directory)

    def test_conflicting_or_inconclusive_cids_and_row_order_cannot_leak_into_split(
        self,
    ):
        rows = [
            dict(CID=str(i), SID=str(i + 10000), **{"Activity Outcome": "Active"})
            for i in range(100, 150)
        ]
        rows += [
            dict(CID=str(i), SID=str(i + 10000), **{"Activity Outcome": "Inactive"})
            for i in range(200, 280)
        ]
        rows += [
            dict(CID="100", SID="1", **{"Activity Outcome": "Inconclusive"}),
            dict(CID="101", SID="2", **{"Activity Outcome": "Inactive"}),
            dict(CID="102", SID="3", **{"Activity Outcome": "Active"}),
        ]
        forward = driver.select_cohort(rows, {"103", "200"})
        backward = driver.select_cohort(list(reversed(rows)), {"103", "200"})
        self.assertEqual(forward, backward)
        selected = {e["cid"]: e for e in forward["cohort"]}
        self.assertFalse({"100", "101", "103", "200"} & selected.keys())
        minimal = [r for r in rows if int(r["CID"]) < 123 or int(r["CID"]) >= 200]
        minimal_result = driver.select_cohort(minimal, {"103", "122"})
        self.assertEqual(
            next(e["sid"] for e in minimal_result["cohort"] if e["cid"] == "102"), "3"
        )
        with self.assertRaises(ValueError):
            driver.select_cohort(rows[:10], set())


if __name__ == "__main__":
    unittest.main()
