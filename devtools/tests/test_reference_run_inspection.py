"""Offline inspection of saved work, coverage and deterministic observed ranks."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STORE = ROOT / "phmt_test_support/reference_run_store.py"
_spec = importlib.util.spec_from_file_location("reference_inspection_guard", STORE)
_store = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_store)
ReferenceLedger = _store.ReferenceLedger
ReferenceRunView = _store.ReferenceRunView
CRITERION = "checked_pose_coverage@1"


class TestReferenceRunInspection(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="phmt-reference-view-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        # SQLite URI quoting must retain these literal filename characters.
        self.path = self.root / "saved run #1?.sqlite3"
        self.manifest = self.root / "work.jsonl"
        self.mapping = [
            {
                "work_key": key,
                "source_key": "source:shared" if index < 2 else f"source:{index}",
                "occurrence_key": f"row:{index}",
            }
            for index, key in enumerate(
                ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta"]
            )
        ]
        self.write_manifest()
        self.query = b'{"original":"saved query bytes"}\n'
        self.context = {
            "execution": {"score_method": "checked_pose_coverage"},
            "producer": {"version": "historical-provider"},
        }

    def write_manifest(self):
        self.manifest.write_text(
            "".join(json.dumps(record) + "\n" for record in self.mapping),
            encoding="utf-8",
        )

    def create(self, **overrides):
        options = {
            "run_id": "run:inspection",
            "parent_run_id": "run:parent",
            "query_bytes": self.query,
            "context": self.context,
            "manifest_path": self.manifest,
        }
        options.update(overrides)
        return ReferenceLedger.create(self.path, **options)

    def reopen_writer(self):
        return ReferenceLedger.open(
            self.path,
            query_bytes=self.query,
            context=self.context,
            manifest_path=self.manifest,
        )

    def outcome(self, key, *, score=0.75, status="matched", criterion=CRITERION):
        mapping = next(row for row in self.mapping if row["work_key"] == key)
        return {
            **mapping,
            "native_result": {
                "pose_id": key,
                "status": status,
                "fit_value": score,
                "producer": {"version": "original-native-version"},
                "diagnostics": [{"reason": "retained observation"}],
            },
            "ranking_score": score,
            "score_method": criterion,
        }

    def publish(self, ledger, key, **settings):
        attempt = ledger.begin(key)
        ledger.stage(attempt, self.outcome(key, **settings))
        ledger.publish(attempt)
        return attempt

    def create_partial(self):
        with self.create() as ledger:
            # Completion order differs from manifest order, including tied scores.
            self.publish(ledger, "beta")
            self.publish(ledger, "gamma", score=0.0, status="not_matched")
            self.publish(ledger, "alpha")
            self.publish(ledger, "delta", score=None, status="failed")
            staged = ledger.begin("epsilon")
            ledger.stage(staged, self.outcome("epsilon", score=1.0))
            ledger.begin("zeta")

    def directory_bytes(self):
        return {
            path.name: path.read_bytes()
            for path in self.root.iterdir()
            if path.is_file()
        }

    def test_partial_summary_keeps_terminal_failures_and_unpublished_work_distinct(
        self,
    ):
        self.create_partial()
        with ReferenceRunView.open(self.path) as view:
            summary = view.summary(score_method=CRITERION)
        self.assertEqual(summary["run_id"], "run:inspection")
        self.assertEqual(summary["parent_run_id"], "run:parent")
        self.assertEqual(summary["score_method"], CRITERION)
        self.assertEqual(
            summary["counts"],
            {
                "declared_work": 7,
                "committed_work": 4,
                "scored_work": 3,
                "matched_work": 2,
                "not_matched_work": 1,
                "failed_work": 1,
                "pending_work": 3,
            },
        )
        self.assertEqual(
            summary["attempts"], {"started": 6, "staged": 5, "committed": 4}
        )
        self.assertFalse(summary["manifest_work_complete"])
        self.assertEqual(summary["ranking_scope"], "observed_scored_work_only")

    def test_observed_top_results_use_manifest_ties_and_include_valid_zero(self):
        self.create_partial()
        with ReferenceRunView.open(self.path) as view:
            ranked = view.top_results(score_method=CRITERION, limit=20)
            self.assertEqual(ranked["summary"], view.summary(score_method=CRITERION))
            first_two = view.top_results(score_method=CRITERION, limit=2)
        self.assertEqual(ranked["limit"], 20)
        self.assertEqual(
            [row["manifest_ordinal"] for row in ranked["records"]], [0, 1, 2]
        )
        self.assertEqual(
            [row["outcome"]["work_key"] for row in ranked["records"]],
            ["alpha", "beta", "gamma"],
        )
        self.assertEqual(ranked["records"][-1]["outcome"]["ranking_score"], 0.0)
        self.assertEqual(
            ranked["records"][-1]["outcome"]["native_result"]["status"], "not_matched"
        )
        self.assertEqual(first_two["records"], ranked["records"][:2])

    def test_zero_limit_retains_coverage_without_publishing_a_ranked_record(self):
        self.create_partial()
        with ReferenceRunView.open(self.path) as view:
            result = view.top_results(score_method=CRITERION, limit=0)
        self.assertEqual(result["limit"], 0)
        self.assertEqual(result["records"], [])
        self.assertEqual(result["summary"]["counts"]["committed_work"], 4)

    def test_later_higher_scores_replace_selected_results_and_keep_earliest_tie(self):
        with self.create() as ledger:
            for key, score in [
                ("alpha", 0.1),
                ("beta", 0.2),
                ("gamma", 0.9),
                ("delta", 0.9),
            ]:
                self.publish(ledger, key, score=score)
        with ReferenceRunView.open(self.path) as view:
            best = view.top_results(score_method=CRITERION, limit=1)
            pair = view.top_results(score_method=CRITERION, limit=2)
        self.assertEqual(best["records"][0]["outcome"]["work_key"], "gamma")
        self.assertEqual(
            [record["outcome"]["work_key"] for record in pair["records"]],
            ["gamma", "delta"],
        )
        self.assertEqual(pair["summary"]["counts"]["scored_work"], 4)

    def test_streamed_results_retain_full_evidence_and_original_multiplicity(self):
        self.create_partial()
        expected = [
            self.outcome("alpha"),
            self.outcome("beta"),
            self.outcome("gamma", score=0.0, status="not_matched"),
            self.outcome("delta", score=None, status="failed"),
        ]
        with ReferenceRunView.open(self.path) as view:
            self.assertEqual(list(view.results()), expected)
        self.assertEqual(expected[0]["source_key"], expected[1]["source_key"])
        self.assertNotEqual(
            expected[0]["occurrence_key"], expected[1]["occurrence_key"]
        )

    def test_inspection_needs_no_external_manifest_or_current_provider(self):
        self.create_partial()
        self.manifest.unlink()
        before = self.directory_bytes()
        with ReferenceRunView.open(self.path) as view:
            self.assertEqual(view.query_bytes, self.query)
            self.assertEqual(view.configuration["context"], self.context)
            self.assertEqual(view.configuration["work_count"], 7)
            self.assertEqual(
                view.summary(score_method=CRITERION)["counts"]["scored_work"], 3
            )
        self.assertEqual(self.directory_bytes(), before)

    def test_configuration_results_and_ranking_are_detached(self):
        self.create_partial()
        with ReferenceRunView.open(self.path) as view:
            configuration = view.configuration
            configuration["context"]["producer"]["version"] = "caller mutation"
            records = list(view.results())
            records[0]["native_result"]["diagnostics"][0]["reason"] = "caller mutation"
            ranked = view.top_results(score_method=CRITERION, limit=1)
            ranked["records"][0]["outcome"]["native_result"]["producer"]["version"] = (
                "caller mutation"
            )
            self.assertEqual(view.configuration["context"], self.context)
            self.assertEqual(list(view.results())[0], self.outcome("alpha"))
            self.assertEqual(
                view.top_results(score_method=CRITERION, limit=1)["records"][0][
                    "outcome"
                ],
                self.outcome("alpha"),
            )

    def test_inspection_preserves_database_bytes_and_creates_no_sidecar(self):
        self.create_partial()
        before = self.directory_bytes()
        with ReferenceRunView.open(self.path) as view:
            view.summary(score_method=CRITERION)
            view.top_results(score_method=CRITERION, limit=1)
            list(view.results())
        self.assertEqual(self.directory_bytes(), before)

    def test_missing_database_is_not_created(self):
        with self.assertRaises((FileNotFoundError, sqlite3.DatabaseError)):
            with ReferenceRunView.open(self.path):
                pass
        self.assertFalse(self.path.exists())

    def test_reader_and_writer_ownership_are_released_on_close(self):
        with self.create():
            with self.assertRaises(sqlite3.OperationalError):
                with ReferenceRunView.open(self.path):
                    pass
        with ReferenceRunView.open(self.path) as view:
            self.assertEqual(list(view.results()), [])
            with self.assertRaises(sqlite3.OperationalError):
                with self.reopen_writer():
                    pass
        with self.reopen_writer() as ledger:
            self.publish(ledger, "alpha")
        with ReferenceRunView.open(self.path) as view:
            self.assertEqual(list(view.results()), [self.outcome("alpha")])

    def test_invalid_limits_and_criteria_are_refused_without_file_changes(self):
        self.create_partial()
        before = self.directory_bytes()
        with ReferenceRunView.open(self.path) as view:
            for limit in [-1, True, False, 1.0, "1", None]:
                with self.subTest(limit=limit):
                    with self.assertRaises(ValueError):
                        view.top_results(score_method=CRITERION, limit=limit)
            for criterion in [
                None,
                "",
                "checked_pose_coverage",
                "unknown@1",
                "seeded_hit@1",
            ]:
                with self.subTest(criterion=criterion):
                    with self.assertRaises(ValueError):
                        view.summary(score_method=criterion)
                    with self.assertRaises(ValueError):
                        view.top_results(score_method=criterion, limit=0)
        self.assertEqual(self.directory_bytes(), before)

    def test_empty_work_still_checks_the_declared_score_criterion(self):
        self.mapping = []
        self.write_manifest()
        with self.create():
            pass
        with ReferenceRunView.open(self.path) as view:
            summary = view.summary(score_method=CRITERION)
            self.assertTrue(summary["manifest_work_complete"])
            self.assertTrue(all(value == 0 for value in summary["counts"].values()))
            self.assertEqual(
                view.top_results(score_method=CRITERION, limit=3)["records"], []
            )
            with self.assertRaises(ValueError):
                view.summary(score_method="seeded_hit@1")

    def test_complete_manifest_with_failures_does_not_turn_failures_into_scores(self):
        with self.create() as ledger:
            for index, row in enumerate(self.mapping):
                if index == 0:
                    self.publish(ledger, row["work_key"], score=None, status="failed")
                else:
                    self.publish(
                        ledger, row["work_key"], score=0.0, status="not_matched"
                    )
        with ReferenceRunView.open(self.path) as view:
            ranked = view.top_results(score_method=CRITERION, limit=20)
        self.assertTrue(ranked["summary"]["manifest_work_complete"])
        self.assertEqual(ranked["summary"]["counts"]["failed_work"], 1)
        self.assertEqual(ranked["summary"]["counts"]["scored_work"], 6)
        self.assertEqual(
            ranked["summary"]["ranking_scope"], "observed_scored_work_only"
        )
        self.assertEqual(len(ranked["records"]), 6)

    def test_mixed_saved_criteria_cannot_form_one_ranking_even_with_zero_limit(self):
        self.context = {"execution": {}, "producer": {"version": "historical"}}
        with self.create() as ledger:
            self.publish(ledger, "alpha")
            self.publish(ledger, "beta", score=1.0, criterion="seeded_hit@1")
        with ReferenceRunView.open(self.path) as view:
            self.assertEqual(len(list(view.results())), 2)
            for criterion in [CRITERION, "seeded_hit@1"]:
                with self.subTest(criterion=criterion):
                    with self.assertRaises(ValueError):
                        view.summary(score_method=criterion)
                    with self.assertRaises(ValueError):
                        view.top_results(score_method=criterion, limit=0)

    def test_corruption_outside_top_results_and_in_unpublished_attempts_is_refused(
        self,
    ):
        self.create_partial()
        for key in ["gamma", "epsilon"]:
            with self.subTest(key=key):
                target = self.root / f"corrupt-{key}.sqlite3"
                shutil.copyfile(self.path, target)
                with closing(sqlite3.connect(target)) as connection, connection:
                    connection.execute(
                        "UPDATE attempts SET digest = ? WHERE work_key = ?",
                        ("0" * 64, key),
                    )
                with self.assertRaises((ValueError, sqlite3.DatabaseError)):
                    with ReferenceRunView.open(target):
                        pass

    def test_query_checksum_is_checked_without_external_query_artifact(self):
        self.create_partial()
        with closing(sqlite3.connect(self.path)) as connection, connection:
            connection.execute(
                "UPDATE metadata SET value = ? WHERE key = 'query'",
                (self.query + b"changed",),
            )
        with self.assertRaises(ValueError):
            with ReferenceRunView.open(self.path):
                pass

    def test_closed_view_cannot_resume_result_inspection(self):
        self.create_partial()
        view = ReferenceRunView.open(self.path)
        view.close()
        view.close()
        with self.assertRaises(ValueError):
            view.summary(score_method=CRITERION)
        with self.assertRaises(ValueError):
            view.top_results(score_method=CRITERION, limit=2)
        with self.assertRaises(ValueError):
            list(view.results())

    def test_fresh_reader_imports_no_scientific_or_support_namespace(self):
        self.create_partial()
        source = """
import importlib.util, sys
blocked={'pharmacophoremt','molsysmt','numpy','scipy','rdkit','ackredit','phmt_test_support'}
class Guard:
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in blocked:
            raise AssertionError('unexpected scientific import: '+fullname)
sys.meta_path.insert(0,Guard())
spec=importlib.util.spec_from_file_location('isolated_inspection',sys.argv[1])
store=importlib.util.module_from_spec(spec)
spec.loader.exec_module(store)
with store.ReferenceRunView.open(sys.argv[2]) as view:
    assert view.summary(score_method='checked_pose_coverage@1')['counts']['scored_work']==3
    assert len(view.top_results(score_method='checked_pose_coverage@1',limit=2)['records'])==2
assert not any(name.split('.')[0] in blocked for name in sys.modules)
"""
        result = subprocess.run(
            [sys.executable, "-I", "-B", "-c", source, str(STORE), str(self.path)],
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_standalone_command_prints_only_scalar_observed_results(self):
        self.create_partial()
        before = self.directory_bytes()
        result = subprocess.run(
            [
                sys.executable,
                "-I",
                "-B",
                "-S",
                str(STORE),
                str(self.path),
                "--score-method",
                CRITERION,
                "--limit",
                "2",
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertFalse(data["summary"]["manifest_work_complete"])
        self.assertEqual(
            [row["work_key"] for row in data["records"]], ["alpha", "beta"]
        )
        for row in data["records"]:
            self.assertEqual(
                set(row),
                {
                    "manifest_ordinal",
                    "work_key",
                    "source_key",
                    "occurrence_key",
                    "ranking_score",
                    "score_method",
                    "status",
                },
            )
        self.assertEqual(self.directory_bytes(), before)

    def test_standalone_command_refuses_bad_requests_without_partial_output(self):
        self.create_partial()
        before = self.directory_bytes()
        for path, criterion, limit in [
            (self.path, CRITERION, "-1"),
            (self.path, "seeded_hit@1", "1"),
            (self.root / "missing.sqlite3", CRITERION, "1"),
        ]:
            with self.subTest(path=path, criterion=criterion, limit=limit):
                result = subprocess.run(
                    [
                        sys.executable,
                        "-I",
                        "-B",
                        "-S",
                        str(STORE),
                        str(path),
                        "--score-method",
                        criterion,
                        "--limit",
                        limit,
                    ],
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                    timeout=20,
                    check=False,
                )
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(result.stdout, "")
        self.assertEqual(self.directory_bytes(), before)


if __name__ == "__main__":
    unittest.main()
