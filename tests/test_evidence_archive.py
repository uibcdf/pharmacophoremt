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

from devtools.evidence_archive import read_archived_bytes, read_archived_evidence

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

    def test_binary_payload_is_verified_without_decoding_or_mutating_files(self):
        raw = b"\x89HDF\r\n\x1a\n\x00\xffnative fixture bytes"
        packed = gzip.compress(raw, mtime=0)
        self.archive.write_bytes(packed)
        self.summary["native_evidence"] = dict(
            path=self.archive.name,
            compressed_sha256=hashlib.sha256(packed).hexdigest(),
            uncompressed_sha256=hashlib.sha256(raw).hexdigest(),
            compressed_bytes=len(packed),
            uncompressed_bytes=len(raw),
        )
        self.write_summary()
        before = self.archive.read_bytes(), self.summary_path.read_bytes()
        summary, payload = read_archived_bytes(
            self.summary_path, identity_key="native_evidence"
        )
        self.assertEqual(summary, self.summary)
        self.assertEqual(payload, raw)
        self.assertEqual(
            before, (self.archive.read_bytes(), self.summary_path.read_bytes())
        )
        with self.assertRaises(ValueError):
            read_archived_evidence(self.summary_path, identity_key="native_evidence")
        self.summary["native_evidence"]["uncompressed_bytes"] += 1
        self.write_summary()
        with self.assertRaisesRegex(ValueError, "byte count mismatch"):
            read_archived_bytes(self.summary_path, identity_key="native_evidence")

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

    def test_prepared_search_keeps_budget_failure_and_incomplete_resolved_ensemble(
        self,
    ):
        summary, report = read_archived_evidence(
            ROOT / "devguide/evidence/prepared_search_workflow_py314_summary.json"
        )
        self.assertEqual(report["schema"], "pharmacophoremt.prepared_search_workflow@1")
        self.assertEqual(summary["environment"], report["environment"])
        self.assertTrue(report["scientific_outputs_stable"])
        self.assertTrue(report["source_hashes_unchanged"])
        self.assertTrue(report["input_hashes_unchanged"])
        for name, content in report["executed_source_overlay"].items():
            self.assertEqual(
                hashlib.sha256(content.encode()).hexdigest(),
                report["input_sha256"][name],
            )
        self.assertEqual(len(report["original_archives_unchanged"]), 29)
        for run in report["records"]:
            self.assertTrue(run["expectations_passed"])
            self.assertEqual(len(run["result"]["results"]), 3)
            self.assertEqual(run["result"]["fresh_reader"]["attribution"]["uses"], [])
            for result in run["result"]["results"].values():
                controls = result["controls"]
                self.assertEqual(controls["budget_failure"]["status"], "failed")
                self.assertIsNone(controls["budget_failure"]["fit_value"])
                self.assertEqual(controls["selected_negative"]["status"], "not_matched")
                self.assertTrue(
                    controls["selected_negative"]["search"]["enumeration_complete"]
                )
                for order in ([1, 0], [0, 1]):
                    partial = controls["ensembles"][f"1:{order}"]
                    self.assertFalse(partial["ensemble"]["complete"])
                    self.assertTrue(partial["ensemble"]["score_resolved"])
                    self.assertEqual(partial["ensemble"]["n_failed"], 1)
                    self.assertEqual(partial["best_conformer_index"], 0)
                    self.assertEqual(partial["fit_value"], 1)

    def test_prepared_distinct_consensus_keeps_support_maps_empty_and_failed_rebuild(
        self,
    ):
        summary, report = read_archived_evidence(
            ROOT / "devguide/evidence/prepared_consensus_workflow_py314_summary.json"
        )
        self.assertEqual(
            report["schema"], "pharmacophoremt.prepared_consensus_workflow@1"
        )
        self.assertEqual(summary["environment"], report["environment"])
        self.assertTrue(report["scientific_outputs_stable"])
        self.assertTrue(report["source_hashes_unchanged"])
        self.assertTrue(report["input_hashes_unchanged"])
        for name, content in report["executed_source_overlay"].items():
            self.assertEqual(
                hashlib.sha256(content.encode()).hexdigest(),
                report["input_sha256"][name],
            )
        self.assertEqual(len(report["original_archives_unchanged"]), 30)
        for run in report["records"]:
            self.assertTrue(run["expectations_passed"])
            result = run["result"]
            self.assertEqual(result["empty"]["models"], [])
            self.assertTrue(result["empty"]["complete"])
            self.assertEqual(result["budget_failure"]["code"], "PHMT-E107")
            self.assertIsNone(result["budget_failure"]["result"])
            self.assertIsNone(result["budget_failure"]["report"])
            self.assertEqual(result["fresh_reader"]["attribution"]["uses"], [])
            for model in [
                result["model"],
                *result["results"].values(),
                *result["fresh_reader"]["models"].values(),
            ]:
                metadata = model["metadata"]
                self.assertEqual(
                    metadata["hypothesis"]["joint_ligand_ids"], ["DES", "EST"]
                )
                self.assertEqual(metadata["consensus"]["n_ligands"], 2)
                for key in ("EST", "DES"):
                    members = [
                        m
                        for site in metadata["consensus"]["sites"]
                        for m in site["members"]
                        if m["ligand_id"] == key
                    ]
                    self.assertEqual([m["feature_index"] for m in members], [0, 1, 2])
                    for member in members:
                        self.assertEqual(
                            member["atom_indices"],
                            result["oracle"]["original_atom_domains"][key][
                                member["feature_index"]
                            ],
                        )
        tracked = report["records"][1]["attribution"]
        datasets = [item for item in tracked["items"] if item["type"] == "dataset"]
        self.assertEqual(len(datasets), 2)
        for dataset in datasets:
            self.assertTrue(
                any(
                    use["item_id"] == dataset["id"] and use["roles"] == ["input_data"]
                    for use in tracked["uses"]
                )
            )

    def test_cached_receptor_archive_keeps_original_input_empty_veto_and_failures(self):
        summary, report = read_archived_evidence(
            ROOT / "devguide/evidence/prepared_receptor_workflow_py314_summary.json"
        )
        self.assertEqual(
            report["schema"], "pharmacophoremt.prepared_receptor_workflow@1"
        )
        self.assertEqual(summary["environment"], report["environment"])
        for name in (
            "scientific_outputs_stable",
            "source_hashes_unchanged",
            "input_hashes_unchanged",
        ):
            self.assertTrue(report[name])
        for name, content in report["executed_source_overlay"].items():
            self.assertEqual(
                hashlib.sha256(content.encode()).hexdigest(),
                report["input_sha256"][name],
            )
        self.assertEqual(len(report["original_archives_unchanged"]), 31)
        self.assertFalse(summary["focused_tests"]["initial_total_selection_passed"])
        self.assertIn("133 passed", report["verification"]["guards.log"])
        self.assertIn("7 passed", report["verification"]["final-guards.log"])
        for run in report["records"]:
            self.assertTrue(run["expectations_passed"])
            result = run["result"]
            self.assertEqual(result["inputs_before"], result["inputs_after"])
            self.assertEqual(result["empty"]["interaction_sites"], [])
            self.assertEqual(len(result["results"]), 12)
            self.assertEqual(len(result["fresh_reader"]["models"]), 12)
            self.assertEqual(result["fresh_reader"]["attribution"]["uses"], [])
            self.assertEqual(
                result["failed_rebuilds"]["complex"]["code"], "MSM-ERR-ARG-001"
            )
            for failed in result["failed_rebuilds"].values():
                self.assertTrue(failed["result_is_none"])
            for codec in ("json", "yaml", "sdf"):
                positive = result["results"]["projected." + codec]["outcomes"][
                    "translated"
                ]
                veto = result["results"]["collision." + codec]["outcomes"]["translated"]
                self.assertEqual(
                    (positive["status"], positive["fit_value"]), ("matched", 1)
                )
                self.assertEqual(
                    (veto["status"], veto["fit_value"]), ("not_matched", 1)
                )
                native = result["results"]["projected." + codec]["native"]
                self.assertEqual(
                    native["interaction_sites"][0]["metadata"]["atom_indices"],
                    [796, 797, 798, 799, 800, 801],
                )
                observed = result["results"]["observed." + codec]["native"]
                self.assertEqual(
                    {
                        x["label"]: x["n_observations"]
                        for x in observed["metadata"]["interaction_collection"][
                            "analyses"
                        ]
                    },
                    {"hydrophobic": 12, "hbonds": 0, "pi_pi": 0},
                )
        attribution = report["records"][1]["attribution"]
        datasets = [item for item in attribution["items"] if item["type"] == "dataset"]
        self.assertEqual(len(datasets), 1)
        self.assertIn("prepared-eralpha:a42ef986", datasets[0]["id"])
        self.assertTrue(
            any(
                use["item_id"] == datasets[0]["id"] and use["roles"] == ["input_data"]
                for use in attribution["uses"]
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
