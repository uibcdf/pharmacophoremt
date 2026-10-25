"""Offline identity and numerical checks of the new #65 derived verification."""

import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "saved_result_archive_reader", ROOT / "phmt_test_support/evidence_archive.py"
)
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


class TestSavedResultsReplay(unittest.TestCase):
    def test_clean_native_replay_preserves_original_counts_metrics_and_provenance(self):
        summary, run = reader.read_archived_evidence(
            ROOT / "devguide/evidence/esr1_saved_summary_replay_20261024_summary.json"
        )
        self.assertEqual(run["producer"]["git_status"], "")
        self.assertEqual(
            run["producer"]["git_head"], "e32c80e0cbc9837e8badcda2b7c93f22d30f1ddc"
        )
        self.assertEqual(
            summary["producer"],
            {k: v for k, v in run["producer"].items() if k != "runtime_files"},
        )
        source_path = ROOT / run["source_summary"]
        self.assertEqual(
            hashlib.sha256(source_path.read_bytes()).hexdigest(),
            run["source_summary_sha256"],
        )
        source_summary, source = reader.read_archived_evidence(source_path)
        self.assertEqual(run["source_archive"], source_summary["full_evidence"])
        self.assertEqual(run["source_producer"], source["producer"])
        self.assertEqual(
            run["source_producer"]["git_head"],
            "012544472e8eca27d1646a6e8065ee22872d4368",
        )
        self.assertTrue(
            all(
                v is True
                for section in run["verification"].values()
                for v in section.values()
            )
        )
        for name in ("baseline", "consensus"):
            arm, original = run["arms"][name], source["arms"][name]["study"]
            with self.subTest(arm=name):
                self.assertEqual(
                    (arm["n_total"], arm["n_actives"], arm["n_inactives"]), (64, 16, 48)
                )
                self.assertEqual(
                    (
                        arm["n_evaluated"],
                        arm["n_actives_evaluated"],
                        arm["n_inactives_evaluated"],
                    ),
                    (45, 12, 33),
                )
                self.assertEqual(
                    (
                        arm["n_unscored"],
                        arm["n_actives_unscored"],
                        arm["n_inactives_unscored"],
                    ),
                    (19, 4, 15),
                )
                self.assertEqual(
                    (arm["n_native_failed"], arm["n_upstream_unscored"]), (0, 19)
                )
                self.assertEqual(arm["unscored_by_stage"], {"acquisition": 19})
                self.assertEqual(
                    arm["n_actives_found"], {"baseline": 0, "consensus": 2}[name]
                )
                self.assertEqual(
                    arm["n_inactives_found"], {"baseline": 1, "consensus": 2}[name]
                )
                self.assertEqual(
                    arm["evaluated_indices"], original["evaluated_cohort_indices"]
                )
                self.assertEqual(arm["labels"], original["labels"])
                self.assertEqual(arm["scores"], original["scores"])
                self.assertEqual(
                    arm["missing_binary_score_AUC_sensitivity"],
                    original["missing_binary_score_AUC_sensitivity"],
                )
                for key in ("AUC", "BEDROC", "EF@10%"):
                    self.assertAlmostEqual(
                        arm["metrics"][key], original[key], places=13
                    )
        self.assertEqual(
            run["common_subset"]["input_indices"],
            source["common_subset"]["cohort_indices"],
        )
        self.assertAlmostEqual(
            run["common_subset"]["delta_comparison_minus_baseline"]["AUC"],
            source["common_subset"]["delta_AUC_consensus_minus_baseline"],
            places=14,
        )
        self.assertEqual(run["attribution"]["status"], "captured")
        credit = json.dumps(run["attribution"])
        self.assertIn("validation.saved_results.compare_screening_results", credit)
        self.assertIn("validation.metrics.bedroc", credit)
        self.assertNotIn("modeler.features.get_features", credit)
        self.assertNotIn("molsysmt.structure.least_rmsd_fit", credit)
