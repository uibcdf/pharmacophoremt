"""Offline guards for the frozen assay case; no molecular/network execution."""

from __future__ import annotations

import csv
import gzip
import hashlib
import importlib.util
import io
import json
import math
import tarfile
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "tests/data/esr1_activity_pilot/manifest.json"
SUMMARY = ROOT / "devguide/evidence/esr1_activity_pilot_20261023_summary.json"
# Reuse the canonical standalone reader without registering the unshipped test
# namespace: other administrative tests exercise its genuinely clean staging.
_spec = importlib.util.spec_from_file_location(
    "esr1_archive_reader", ROOT / "phmt_test_support/evidence_archive.py"
)
_reader = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_reader)
read_archived_bytes = _reader.read_archived_bytes
read_archived_evidence = _reader.read_archived_evidence


class TestEsr1ActivityPilot(unittest.TestCase):
    def test_original_inputs_restore_offline_with_source_labels_and_failures(self):
        spec = importlib.util.spec_from_file_location(
            "esr1_snapshot_driver", ROOT / "phmt_test_support/esr1_activity_pilot.py"
        )
        driver = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver)
        manifest = json.loads(MANIFEST.read_text())
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "originals"
            with patch.object(
                driver.urllib.request, "urlopen", side_effect=AssertionError("network")
            ):
                receipt = driver.restore_archived_inputs(target)
            self.assertEqual(
                receipt,
                dict(original_input_files=35, saved_queries=1, network_used=False),
            )
            self.assertEqual(len(list(target.iterdir())), 36)
            with tarfile.open(target / "ESR1ago.tar.gz") as archive:
                with archive.extractfile("ESR1ago/ESR1ago_data_full.csv") as stream:
                    rows = list(csv.DictReader(io.TextIOWrapper(stream)))
            selected = driver.frozen_cohort(rows)
            self.assertEqual(
                [(r["cid"], r["sid"], r["label"], r["role"]) for r in selected],
                [
                    (r["cid"], r["sid"], r["label"], r["role"])
                    for r in manifest["cohort"]
                ],
            )
            with (target / "aid743075_concise.csv").open() as stream:
                assay = {r["SID"]: r for r in csv.DictReader(stream)}
            for entry in manifest["cohort"]:
                self.assertEqual(assay[entry["sid"]]["CID"], entry["cid"])
                self.assertEqual(
                    assay[entry["sid"]]["Activity Outcome"], entry["assay_outcome"]
                )
                record = entry["acquisition"]
                if record["status"] == "failed":
                    self.assertFalse((target / f"CID{entry['cid']}.sdf").exists())
                    record = record["response"]
                payload = (target / record["file"]).read_bytes()
                self.assertEqual(hashlib.sha256(payload).hexdigest(), record["sha256"])
            _, query = read_archived_bytes(SUMMARY, identity_key="saved_query_archive")
            self.assertEqual((target / "run-01.query.json").read_bytes(), query)
            with self.assertRaises(FileExistsError):
                driver.restore_archived_inputs(target)
            # Scientific workflows may now read these exact bytes via MolSysMT;
            # this transport test does not import molecular providers.

    def test_snapshot_rejects_rehashed_member_or_manifest_substitution_before_writes(
        self,
    ):
        spec = importlib.util.spec_from_file_location(
            "esr1_snapshot_driver", ROOT / "phmt_test_support/esr1_activity_pilot.py"
        )
        driver = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver)
        summary, original_tar = read_archived_bytes(driver.INPUT_SNAPSHOT)
        with tarfile.open(fileobj=io.BytesIO(original_tar)) as archive:
            members = [
                (m.name, archive.extractfile(m).read()) for m in archive.getmembers()
            ]
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            for change in ("bytes", "duplicate", "traversal", "symlink", "missing"):
                with self.subTest(change=change):
                    buffer = io.BytesIO()
                    with tarfile.open(fileobj=buffer, mode="w") as archive:
                        altered = members[:-1] if change == "missing" else members
                        for index, (name, payload) in enumerate(altered):
                            if index == 0 and change == "bytes":
                                payload += b"changed"
                            info = tarfile.TarInfo(
                                "../escape"
                                if index == 0 and change == "traversal"
                                else name
                            )
                            info.size = len(payload)
                            if index == 0 and change == "symlink":
                                info.type, info.linkname, info.size = (
                                    tarfile.SYMTYPE,
                                    "../escape",
                                    0,
                                )
                            archive.addfile(info, io.BytesIO(payload))
                        if change == "duplicate":
                            info = tarfile.TarInfo(members[0][0])
                            archive.addfile(info, io.BytesIO())
                    raw = buffer.getvalue()
                    compressed = gzip.compress(raw, mtime=0)
                    (tmp / "snapshot.tar.gz").write_bytes(compressed)
                    changed = dict(
                        summary,
                        full_evidence=dict(
                            path="snapshot.tar.gz",
                            compressed_sha256=hashlib.sha256(compressed).hexdigest(),
                            compressed_bytes=len(compressed),
                            uncompressed_sha256=hashlib.sha256(raw).hexdigest(),
                            uncompressed_bytes=len(raw),
                        ),
                    )
                    path = tmp / "snapshot.json"
                    path.write_text(json.dumps(changed))
                    target = tmp / "inputs"
                    with self.assertRaises(ValueError):
                        driver.restore_archived_inputs(target, summary_path=path)
                    self.assertFalse(target.exists())
                    self.assertFalse((tmp / "escape").exists())
            changed_manifest = tmp / "manifest.json"
            changed_manifest.write_bytes(MANIFEST.read_bytes() + b"\n")
            # Even a corresponding rehash cannot replace the archived producer's
            # manifest identity. Original compressed bytes are used in this case.
            changed = dict(
                summary,
                input_manifest_sha256=hashlib.sha256(
                    changed_manifest.read_bytes()
                ).hexdigest(),
            )
            changed["full_evidence"] = dict(
                summary["full_evidence"], path="snapshot.tar.gz"
            )
            (tmp / "snapshot.tar.gz").write_bytes(
                (
                    driver.INPUT_SNAPSHOT.parent / summary["full_evidence"]["path"]
                ).read_bytes()
            )
            path.write_text(json.dumps(changed))
            with self.assertRaises(ValueError):
                driver.restore_archived_inputs(tmp / "inputs", changed_manifest, path)
            self.assertFalse((tmp / "inputs").exists())

    def test_seeded_replay_keeps_frozen_inputs_and_uses_binary_oracles(self):
        path = ROOT / "devguide/evidence/esr1_seeded_hit_replay_20261024_summary.json"
        summary, run = read_archived_evidence(path)
        _, original = read_archived_evidence(SUMMARY)
        declaration = (
            ROOT / "tests/data/esr1_activity_pilot/seeded_replay_declaration.json"
        )
        self.assertEqual(
            run["producer"]["git_head"], "c80325c5c3851691bcc0a993d1e73eaf294654f6"
        )
        self.assertEqual(run["producer"]["dirty"], "")
        self.assertEqual(
            run["saved_query"]["sha256"], original["saved_query"]["sha256"]
        )
        self.assertEqual(run["manifest"]["sha256"], original["manifest"]["sha256"])
        self.assertEqual(
            run["replay_declaration"]["sha256"],
            hashlib.sha256(declaration.read_bytes()).hexdigest(),
        )
        self.assertEqual(
            [r["cid"] for r in run["records"]], [r["cid"] for r in original["records"]]
        )
        for new, old in zip(run["records"], original["records"], strict=True):
            self.assertEqual(new["preparation"]["status"], old["preparation"]["status"])
            if new["preparation"]["status"] == "completed":
                self.assertEqual(
                    new["preparation"]["counts"], old["preparation"]["counts"]
                )
                self.assertEqual(
                    new["preparation"]["feature_counts"],
                    old["preparation"]["feature_counts"],
                )
                self.assertTrue(all(new["preparation"]["checks"].values()))
        records = run["records"][1:]
        valid = [r for r in records if r["evaluation"]["status"] != "failed"]
        failed = [r for r in records if r["evaluation"]["status"] == "failed"]
        self.assertEqual(Counter(r["label"] for r in valid), {1: 6, 0: 19})
        self.assertEqual(Counter(r["label"] for r in failed), {1: 1, 0: 5})
        self.assertTrue(all(r["evaluation"]["fit_value"] is None for r in failed))
        scores = [r["evaluation"]["ranking_score"] for r in valid]
        labels = [r["label"] for r in valid]
        self.assertEqual(Counter(scores), {0: 24, 1: 1})
        self.assertEqual(run["retrospective"]["scores"], scores)
        self.assertEqual(run["retrospective"]["score_method"], "seeded_hit@1")
        self.assertEqual(
            sum(r["evaluation"]["pose_evaluated"] is False for r in valid), 23
        )
        self.assertTrue(
            all(not r["evaluation"]["search"]["identity_pose_tested"] for r in valid)
        )
        self.assertEqual(
            [
                (r["cid"], r["label"])
                for r in valid
                if r["evaluation"]["status"] == "matched"
            ],
            [("24964624", 1)],
        )
        positives = [s for s, label in zip(scores, labels) if label]
        negatives = [s for s, label in zip(scores, labels) if not label]
        auc = sum((p > n) + 0.5 * (p == n) for p in positives for n in negatives) / (
            len(positives) * len(negatives)
        )
        self.assertAlmostEqual(auc, run["retrospective"]["AUC"], places=14)
        # Three top positions: one hit plus two fractional selections from the
        # 24 zero-score inputs, of which five are active.
        ef = ((1 + 2 * 5 / 24) / 3) / (6 / 25)
        self.assertAlmostEqual(ef, run["retrospective"]["EF@10%"], places=14)
        _, qualified = read_archived_evidence(
            path, identity_key="qualification_evidence"
        )
        self.assertEqual(qualified["source_commit"], run["producer"]["git_head"])
        self.assertEqual(qualified["checks"]["full_source"]["result"], "949 passed")
        self.assertIn(
            "pharmacophoremt/screening/scoring.py", qualified["source_content"]
        )
        self.assertIn("source", summary["source_availability"])

    def test_seeded_replay_requires_original_query_and_inputs_even_with_rehashed_declaration(
        self,
    ):
        spec = importlib.util.spec_from_file_location(
            "esr1_replay_driver", ROOT / "phmt_test_support/esr1_activity_pilot.py"
        )
        driver = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver)
        declared = (
            ROOT / "tests/data/esr1_activity_pilot/seeded_replay_declaration.json"
        )
        _, query_bytes = read_archived_bytes(
            SUMMARY, identity_key="saved_query_archive"
        )
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            query_path = directory / "query.json"
            query_path.write_bytes(query_bytes)
            driver.validate_replay_declaration(MANIFEST, declared, query_path)
            with self.assertRaises(ValueError):
                driver.validate_replay_declaration(MANIFEST, declared, None)
            changed = json.loads(declared.read_text())
            query_path.write_bytes(query_bytes + b"\n")
            changed["frozen_query_sha256"] = hashlib.sha256(
                query_path.read_bytes()
            ).hexdigest()
            declaration_path = directory / "changed.json"
            declaration_path.write_text(json.dumps(changed))
            with self.assertRaises(ValueError):
                driver.validate_replay_declaration(
                    MANIFEST, declaration_path, query_path
                )
            query_path.write_bytes(query_bytes)
            changed = json.loads(declared.read_text())
            manifest_path = directory / "inputs.json"
            manifest_path.write_bytes(MANIFEST.read_bytes() + b"\n")
            changed["input_manifest_sha256"] = hashlib.sha256(
                manifest_path.read_bytes()
            ).hexdigest()
            declaration_path.write_text(json.dumps(changed))
            with self.assertRaises(ValueError):
                driver.validate_replay_declaration(
                    manifest_path, declaration_path, query_path
                )

    def test_original_accounting_and_metrics_have_independent_oracles(self):
        summary, run = read_archived_evidence(SUMMARY)
        manifest = json.loads(MANIFEST.read_text())
        records = run["records"]
        self.assertEqual(
            [r["cid"] for r in records], [r["cid"] for r in manifest["cohort"]]
        )
        held_out = records[1:]
        self.assertEqual(len(held_out), 31)
        failed = [r for r in held_out if r["evaluation"]["status"] == "failed"]
        self.assertEqual(Counter(r["label"] for r in failed), {1: 1, 0: 5})
        self.assertTrue(all(r["evaluation"]["fit_value"] is None for r in failed))
        self.assertTrue(all(r["preparation"]["status"] == "failed" for r in failed))
        self.assertIn(
            "stereo",
            next(r for r in failed if r["cid"] == "6842999")["preparation"]["message"],
        )
        valid = [r for r in held_out if r["evaluation"]["status"] != "failed"]
        labels = [r["label"] for r in valid]
        scores = [r["evaluation"]["fit_value"] for r in valid]
        report = run["retrospective"]
        self.assertEqual(report["scores"], scores)
        self.assertEqual(report["labels"], labels)
        self.assertEqual(
            report["evaluated_indices"],
            [i for i, r in enumerate(held_out) if r not in failed],
        )
        self.assertEqual((report["n_evaluated"], report["n_failed"]), (25, 6))
        self.assertEqual((sum(labels), len(labels) - sum(labels)), (6, 19))
        self.assertEqual(scores.count(0), 23)
        self.assertEqual(
            [
                (r["cid"], r["label"])
                for r in valid
                if r["evaluation"]["status"] == "matched"
            ],
            [("24964624", 1)],
        )

        # Pairwise probability and boundary-tie arithmetic are independent of
        # the executed NumPy metric implementations and input tie ordering.
        def auc(rows, optimistic=None):
            positives, negatives = [], []
            for row in rows:
                score = row["evaluation"]["fit_value"]
                if score is None:
                    self.assertIsNotNone(optimistic)
                    score = row["label"] if optimistic else 1 - row["label"]
                (positives if row["label"] else negatives).append(score)
            return sum(
                (p > n) + 0.5 * (p == n) for p in positives for n in negatives
            ) / (len(positives) * len(negatives))

        self.assertAlmostEqual(auc(valid), report["AUC"], places=14)
        top_n = math.ceil(0.10 * len(valid))
        threshold = sorted(scores, reverse=True)[top_n - 1]
        strict = [r for r in valid if r["evaluation"]["fit_value"] > threshold]
        tied = [r for r in valid if r["evaluation"]["fit_value"] == threshold]
        expected_actives = sum(r["label"] for r in strict) + (
            top_n - len(strict)
        ) * sum(r["label"] for r in tied) / len(tied)
        self.assertAlmostEqual(
            (expected_actives / top_n) / (sum(labels) / len(labels)),
            report["EF@10%"],
            places=14,
        )
        for optimistic, key in [
            (False, "pessimistic_hypothetical_scores"),
            (True, "optimistic_hypothetical_scores"),
        ]:
            self.assertAlmostEqual(
                auc(held_out, optimistic),
                summary["failure_sensitivity_AUC"][key],
                places=14,
            )
        for record in valid:
            self.assertTrue(record["evaluation"]["search"]["enumeration_complete"])
            self.assertLessEqual(record["evaluation"]["search"]["n_trials"], 10000)
        for record in records:
            if record["preparation"]["status"] == "completed":
                self.assertTrue(all(record["preparation"]["checks"].values()))

    def test_original_installed_runtime_query_and_source_identities(self):
        summary, run = read_archived_evidence(SUMMARY)
        self.assertEqual(run["producer"]["dirty"], "")
        self.assertEqual(
            run["producer"]["git_head"], "ee064102f3701a280297e01ec0c549207f10bfd3"
        )
        self.assertEqual(run["producer"]["versions"]["pharmacophoremt"], "0.4.0")
        self.assertEqual(run["producer"]["versions"]["molsysmt"], "0.23.0")
        for origin in run["producer"]["runtime_origins"].values():
            self.assertIn("/environment/lib/python3.14/site-packages/", origin)
        self.assertEqual(len(run["producer"]["conda_records"]), 311)
        self.assertIn("_rust.abi3.so", run["producer"]["runtime_files"]["molsysmt"])
        self.assertEqual(
            hashlib.sha256(MANIFEST.read_bytes()).hexdigest(), run["manifest"]["sha256"]
        )
        _, query_raw = read_archived_bytes(SUMMARY, identity_key="saved_query_archive")
        self.assertEqual(
            hashlib.sha256(query_raw).hexdigest(), run["saved_query"]["sha256"]
        )
        _, journal = read_archived_evidence(SUMMARY, identity_key="preparation_archive")
        self.assertEqual(
            [r["preparation"] for r in run["records"]],
            [r["preparation"] for r in journal["records"]],
        )
        self.assertEqual(run["reference_self_evaluation"]["fit_value"], 1)
        self.assertEqual(
            run["records"][0]["preparation"]["feature_counts"],
            {"hb acceptor": 2, "aromatic ring": 1},
        )
        self.assertEqual(
            summary["attribution"]["portable_items"],
            len(run["data_attribution"]["items"]),
        )

    def test_frozen_split_excludes_ambiguous_compounds_and_reference_leakage(self):
        manifest = json.loads(MANIFEST.read_text())
        rows = manifest["cohort"]
        self.assertEqual(len(rows), 32)
        self.assertEqual(len({r["cid"] for r in rows}), 32)
        self.assertEqual(len({r["sid"] for r in rows}), 32)
        self.assertEqual(
            Counter((r["role"], r["label"]) for r in rows),
            {("reference", 1): 1, ("held_out", 1): 7, ("held_out", 0): 24},
        )
        self.assertEqual(rows[0]["cid"], "9821849")
        ambiguous = manifest["selection"]["ambiguous_source_rows"]
        self.assertEqual(len(ambiguous), 8)
        ambiguous_ids = {r["PUBCHEM_CID"] for r in ambiguous}
        self.assertEqual(ambiguous_ids, {"2662", "5361202", "6128", "17113"})
        self.assertFalse(ambiguous_ids & {r["cid"] for r in rows})
        for cid in ambiguous_ids:
            self.assertEqual(
                {
                    r["PUBCHEM_ACTIVITY_OUTCOME"]
                    for r in ambiguous
                    if r["PUBCHEM_CID"] == cid
                },
                {"Active", "Inactive"},
            )
        for row in rows:
            self.assertEqual(
                row["assay_outcome"], "Active" if row["label"] else "Inactive"
            )
            self.assertEqual(
                row["selection_hash"],
                hashlib.sha256(
                    ("phmt-esr1ago-pilot-v1:" + row["cid"]).encode()
                ).hexdigest(),
            )
        unavailable = [r for r in rows if r["acquisition"]["status"] == "failed"]
        self.assertEqual(
            {r["cid"] for r in unavailable},
            {"154256", "9576185", "9984487", "21124389", "92151"},
        )
        self.assertTrue(
            all(r["acquisition"]["http_status"] == 404 for r in unavailable)
        )


if __name__ == "__main__":
    unittest.main()
