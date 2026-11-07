"""Criterion-independent saved progress, actual CLI and original evidence."""

import io
import json
import sqlite3
import unittest
from contextlib import closing, redirect_stderr, redirect_stdout
from unittest.mock import patch

import test_public_run_results as fixtures

from pharmacophoremt_results import ScreeningRunError, ScreeningRunView, main


class TestPublicRunProgress(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.TestPublicRunResults()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def invoke(self, *arguments):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                code = main(list(map(str, arguments)))
            except SystemExit as error:
                code = error.code
        return code, stdout.getvalue(), stderr.getvalue()

    def test_writer_and_reader_separate_work_statuses_from_repeated_attempts(self):
        f = self.fixture
        f.create_partial()
        expected = {
            "run_id": "run:public",
            "parent_run_id": "run:ancestor",
            "counts": {
                "declared_work": 5,
                "committed_work": 4,
                "scored_work": 3,
                "matched_work": 2,
                "not_matched_work": 1,
                "failed_work": 1,
                "pending_work": 1,
            },
            "attempts": {"started": 6, "staged": 5, "committed": 4},
            "manifest_work_complete": False,
        }
        with f.reopen() as store:
            store.begin("epsilon")
            self.assertEqual(store.progress(), expected)
            summary = store.summary(score_method=fixtures.CRITERION)
            self.assertEqual(store.progress()["counts"], summary["counts"])
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            self.assertEqual(view.progress(), expected)
        self.assertEqual(f.directory_bytes(), before)
        with f.reopen() as store:
            f.publish(store, "epsilon", score=None, status="failed")
            progress = store.progress()
            self.assertEqual(
                progress["attempts"], {"started": 7, "staged": 6, "committed": 5}
            )
            self.assertEqual(progress["counts"]["failed_work"], 2)
            self.assertEqual(progress["counts"]["pending_work"], 0)
            self.assertIs(progress["manifest_work_complete"], True)
        with ScreeningRunView.open(f.path) as view:
            self.assertEqual(view.progress(), progress)

    def test_empty_declared_work_is_complete_with_no_attempts(self):
        f = self.fixture
        f.mapping = []
        f.write_manifest()
        with f.create() as store:
            progress = store.progress()
            self.assertTrue(progress["manifest_work_complete"])
            self.assertEqual(set(progress["counts"].values()), {0})
            self.assertEqual(
                progress["attempts"], dict(started=0, staged=0, committed=0)
            )
        result = f.command(f.path, "--summary")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), progress)

    def test_progress_is_detached_and_closed_connections_refuse_inspection(self):
        f = self.fixture
        f.create_partial()
        with f.reopen() as store:
            expected = store.progress()
            changed = store.progress()
            changed["counts"]["committed_work"] = 1000
            changed["attempts"].clear()
            self.assertEqual(store.progress(), expected)
        with self.assertRaises(ScreeningRunError):
            store.progress()
        with ScreeningRunView.open(f.path) as view:
            changed = view.progress()
            changed["counts"].clear()
            changed["attempts"].clear()
            self.assertEqual(view.progress(), expected)
            with self.assertRaises(ScreeningRunError):
                view.summary(score_method=None)
        with self.assertRaises(ScreeningRunError):
            view.progress()

    def test_explicit_legacy_mixed_criteria_are_counted_without_combining_scores(self):
        f = self.fixture
        with f.legacy().create(
            f.path,
            run_id="run:mixed",
            query_bytes=f.query,
            context={"execution": {}},
            manifest_path=f.manifest,
        ) as store:
            f.publish(store, "alpha")
            outcome = f.outcome("beta", score=1)
            outcome["score_method"] = "seeded_hit@1"
            attempt = store.begin("beta")
            store.stage(attempt, outcome)
            store.publish(attempt)
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path, allow_legacy=True) as view:
            progress = view.progress()
            self.assertEqual(progress["counts"]["scored_work"], 2)
            self.assertEqual(progress["counts"]["pending_work"], 3)
            for criterion in [fixtures.CRITERION, "seeded_hit@1"]:
                with self.assertRaises(ScreeningRunError):
                    view.summary(score_method=criterion)
        denied = f.command(f.path, "--summary")
        self.assertEqual(denied.returncode, 2)
        self.assertEqual(denied.stdout, "")
        allowed = f.command(f.path, "--summary", "--allow-legacy")
        self.assertEqual(allowed.returncode, 0, allowed.stderr)
        self.assertEqual(json.loads(allowed.stdout), progress)
        self.assertEqual(f.directory_bytes(), before)

    def test_fresh_guarded_command_matches_api_without_native_or_query_payloads(self):
        f = self.fixture
        f.create_partial()
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            expected = view.progress()
        result = f.command(f.path, "--summary")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), expected)
        for field in [
            "score_method",
            "ranking_scope",
            "records",
            "context",
            "geometry",
        ]:
            self.assertNotIn(field, result.stdout)
        self.assertEqual(f.directory_bytes(), before)

    def test_summary_option_conflicts_fail_before_opening_a_database(self):
        f = self.fixture
        for options in [
            ["--summary", "--to-csv", f.root / "new.csv"],
            ["--summary", "--to-jsonl", f.root / "new.jsonl"],
            ["--summary", "--score-method", fixtures.CRITERION],
            ["--summary", "--limit", "0"],
            ["--summary", "--limit", "-1"],
        ]:
            with (
                self.subTest(options=options),
                patch.object(ScreeningRunView, "open") as opened,
            ):
                code, stdout, stderr = self.invoke(f.path, *options)
                self.assertEqual(code, 2)
                self.assertEqual(stdout, "")
                self.assertTrue(stderr)
                opened.assert_not_called()
        self.assertEqual(set(f.directory_bytes()), {f.manifest.name})

    def test_missing_and_corrupt_database_commands_produce_no_success_response(self):
        f = self.fixture
        for contents in [None, b"not a database"]:
            if contents is not None:
                f.path.write_bytes(contents)
            result = f.command(f.path, "--summary")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertTrue(result.stderr)
            if contents is None:
                self.assertFalse(f.path.exists())
            else:
                self.assertEqual(f.path.read_bytes(), contents)

    def test_corrupt_unpublished_evidence_is_verified_before_progress(self):
        f = self.fixture
        f.create_partial()
        with closing(sqlite3.connect(f.path)) as connection, connection:
            connection.execute("UPDATE attempts SET digest='invalid' WHERE committed=0")
        before = f.directory_bytes()
        with self.assertRaises(ScreeningRunError):
            ScreeningRunView.open(f.path)
        result = f.command(f.path, "--summary")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(f.directory_bytes(), before)

    def test_help_describes_summary_without_loading_a_saved_run(self):
        f = self.fixture
        result = f.command("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--summary", result.stdout)
        self.assertIn(
            "without selecting a ranking criterion", " ".join(result.stdout.split())
        )
        self.assertFalse(f.path.exists())


if __name__ == "__main__":
    unittest.main()
