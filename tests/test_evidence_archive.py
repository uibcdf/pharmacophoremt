"""Archive integrity controls that require only the Python standard library."""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from devtools.evidence_archive import read_archived_evidence

ROOT = Path(__file__).resolve().parents[1]
CCD_SUMMARY = ROOT / "devguide/evidence/prepared_ccd_py314_summary.json"


class TestEvidenceArchive(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.original = {
            "schema": "local.result@1",
            "records": [{"status": "failed", "fit_value": None, "error": "budget"}],
            "unknown_producer_field": {"chemical_state": "original"},
        }
        raw = (json.dumps(self.original) + "\n").encode()
        self.compressed = gzip.compress(raw, mtime=0)
        self.archive = self.directory / "report.json.gz"
        self.archive.write_bytes(self.compressed)
        self.summary_path = self.directory / "summary.json"
        self.summary = {
            "schema": "local.summary@1",
            "full_evidence": {
                "path": self.archive.name,
                "compressed_sha256": hashlib.sha256(self.compressed).hexdigest(),
                "uncompressed_sha256": hashlib.sha256(raw).hexdigest(),
                "compressed_bytes": len(self.compressed),
                "uncompressed_bytes": len(raw),
            },
        }
        self.write_summary()

    def write_summary(self):
        self.summary_path.write_text(json.dumps(self.summary))

    def test_failed_and_unknown_fields_remain_original_and_files_are_unchanged(self):
        before = self.summary_path.read_bytes(), self.archive.read_bytes()
        summary, report = read_archived_evidence(self.summary_path)
        self.assertEqual(summary, self.summary)
        self.assertEqual(report, self.original)
        self.assertEqual(
            before, (self.summary_path.read_bytes(), self.archive.read_bytes())
        )

    def test_corrupted_compressed_archive_is_refused_before_decompression(self):
        self.archive.write_bytes(b"corrupted")
        with self.assertRaisesRegex(ValueError, "Compressed SHA-256 mismatch"):
            read_archived_evidence(self.summary_path)

    def test_repacked_altered_payload_cannot_pass_original_uncompressed_identity(self):
        altered = gzip.compress(b'{"records": []}', mtime=0)
        self.archive.write_bytes(altered)
        identity = self.summary["full_evidence"]
        identity["compressed_sha256"] = hashlib.sha256(altered).hexdigest()
        identity["compressed_bytes"] = len(altered)
        self.write_summary()
        with self.assertRaisesRegex(ValueError, "Uncompressed SHA-256 mismatch"):
            read_archived_evidence(self.summary_path)

    def test_missing_and_malformed_checksums_are_refused(self):
        for value in (None, "", "not-a-digest", True):
            with self.subTest(value=value):
                self.summary["full_evidence"]["compressed_sha256"] = value
                self.write_summary()
                with self.assertRaisesRegex(ValueError, "invalid compressed SHA-256"):
                    read_archived_evidence(self.summary_path)

    def test_recorded_byte_count_mismatch_is_refused(self):
        for key in ("compressed_bytes", "uncompressed_bytes"):
            original = self.summary["full_evidence"][key]
            for value in (original + 1, None, True, float(original)):
                with self.subTest(key=key, value=value):
                    self.summary["full_evidence"][key] = value
                    self.write_summary()
                    with self.assertRaisesRegex(ValueError, "byte count mismatch"):
                        read_archived_evidence(self.summary_path)
            self.summary["full_evidence"][key] = original

    def test_absolute_parent_and_escaping_symlink_paths_are_refused(self):
        for value in (
            "../report.json.gz",
            str(self.archive),
            "",
            "..",
            "sub/report.gz",
        ):
            with self.subTest(value=value):
                self.summary["full_evidence"]["path"] = value
                self.write_summary()
                with self.assertRaisesRegex(ValueError, "sibling file"):
                    read_archived_evidence(self.summary_path)
        with tempfile.TemporaryDirectory() as outside:
            target = Path(outside) / "report.json.gz"
            target.write_bytes(self.compressed)
            link = self.directory / "outside.json.gz"
            link.symlink_to(target)
            self.summary["full_evidence"]["path"] = link.name
            self.write_summary()
            with self.assertRaisesRegex(ValueError, "escapes summary directory"):
                read_archived_evidence(self.summary_path)

    def test_historical_file_spelling_and_explicit_identity_key_are_supported(self):
        identity = self.summary.pop("full_evidence")
        identity["file"] = identity.pop("path")
        identity.pop("compressed_bytes")
        identity.pop("uncompressed_bytes")
        self.summary["evidence"] = identity
        self.write_summary()
        self.assertEqual(
            read_archived_evidence(self.summary_path, identity_key="evidence")[1],
            self.original,
        )
        with self.assertRaisesRegex(ValueError, "Missing archive identity"):
            read_archived_evidence(self.summary_path)

    def test_original_ccd_demonstrator_has_twelve_controls_and_detached_references(
        self,
    ):
        summary, report = read_archived_evidence(CCD_SUMMARY)
        self.assertEqual(summary["environment"], report["environment"])
        self.assertEqual(len(report["records"]), 12)
        self.assertTrue(all(r["expectation_passed"] for r in report["records"]))
        self.assertTrue(all(r["scientific_outputs_stable"] for r in report["records"]))
        self.assertEqual(report["attribution"]["schema"], "ackredit.attribution@1")
        self.assertEqual(len(report["attribution"]["items"]), 21)
        self.assertEqual(len(report["attribution"]["uses"]), 99)
        datasets = [r for r in report["attribution"]["items"] if r["type"] == "dataset"]
        self.assertEqual(len(datasets), 2)
        manifest = json.loads(
            (ROOT / "tests/data/prepared_ccd/manifest.json").read_text()
        )
        self.assertEqual(report["manifest"], manifest)
        for case in manifest["cases"]:
            path = ROOT / "tests/data/prepared_ccd" / case["file"]
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(), case["sha256"]
            )

    def test_prepared_workflow_preserves_failed_inputs_and_execution_identity(self):
        summary, report = read_archived_evidence(
            ROOT / "devguide/evidence/prepared_workflow_py314_summary.json"
        )
        self.assertEqual(report["schema"], "pharmacophoremt.prepared_workflow@1")
        self.assertEqual(summary["environment"], report["environment"])
        self.assertTrue(report["scientific_outputs_stable"])
        self.assertTrue(report["source_hashes_unchanged"])
        self.assertTrue(report["input_hashes_unchanged"])
        for name, content in report["executed_source_overlay"].items():
            self.assertEqual(
                hashlib.sha256(content.encode()).hexdigest(),
                report["input_sha256"][name],
            )
        for run in report["records"]:
            self.assertTrue(run["expectations_passed"])
            self.assertEqual(len(run["result"]["results"]), 9)
            self.assertEqual(run["result"]["fresh_reader"]["attribution"]["uses"], [])
            for record in run["result"]["results"].values():
                evaluations = record["screening"]["evaluations"]
                self.assertEqual(len(evaluations), 5)
                self.assertEqual(evaluations[2]["status"], "not_matched")
                self.assertEqual(evaluations[2]["fit_value"], 0)
                self.assertEqual(evaluations[3]["status"], "failed")
                self.assertIsNone(evaluations[3]["fit_value"])
        tracked = report["records"][1]
        datasets = [
            item
            for item in tracked["attribution"]["items"]
            if item["type"] == "dataset"
        ]
        self.assertEqual(len(datasets), 1)
        self.assertIn("ccd:EST:", datasets[0]["id"])
        self.assertTrue(
            any(
                use["item_id"] == datasets[0]["id"] and use["roles"] == ["input_data"]
                for use in tracked["attribution"]["uses"]
            )
        )

    def test_cli_reads_real_archive_without_site_packages(self):
        result = subprocess.run(
            [sys.executable, "-S", "-m", "devtools.evidence_archive", str(CCD_SUMMARY)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["archive_bytes_verified"])


if __name__ == "__main__":
    unittest.main()
