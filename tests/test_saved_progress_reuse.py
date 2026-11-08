"""Snapshot progress reuse preserves public accounting and connection semantics."""

import sqlite3
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

import test_public_run_results as fixtures

from pharmacophoremt_results import ScreeningRunError, ScreeningRunView


class TestSavedProgressReuse(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.TestPublicRunResults()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def assert_reused(self, view, expected):
        statements = []
        connection = view._view._ledger._db()
        connection.set_trace_callback(statements.append)
        try:
            for _ in range(3):
                self.assertEqual(view.progress(), expected)
        finally:
            connection.set_trace_callback(None)
        self.assertTrue(statements, "connection/thread checks must still execute")
        for statement in statements:
            self.assertFalse(
                any(
                    name in statement.lower().split()
                    for name in ("work", "attempts", "outcomes")
                ),
                statement,
            )

    def test_partial_snapshot_reuses_counts_without_reading_saved_payloads(self):
        f = self.fixture
        f.create_partial()
        original = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            expected = view.progress()
            self.assertEqual(
                expected["counts"],
                dict(
                    declared_work=5,
                    committed_work=4,
                    scored_work=3,
                    matched_work=2,
                    not_matched_work=1,
                    failed_work=1,
                    pending_work=1,
                ),
            )
            self.assertEqual(
                expected["attempts"], dict(started=5, staged=5, committed=4)
            )
            self.assertFalse(expected["manifest_work_complete"])
            self.assert_reused(view, expected)
        self.assertEqual(f.directory_bytes(), original)

    def test_each_return_detaches_nested_values_and_preserves_key_order(self):
        f = self.fixture
        f.create_partial()
        with ScreeningRunView.open(f.path) as view:
            expected = view.progress()
            modified = view.progress()
            modified["counts"].clear()
            modified["attempts"]["started"] = -1
            modified["run_id"] = "caller-modified"
            result = view.progress()
            self.assertEqual(result, expected)
            for key in ("counts", "attempts"):
                self.assertIsNot(result[key], expected[key])
                self.assertEqual(list(result[key]), list(expected[key]))
            self.assertEqual(list(result), list(expected))

    def test_failed_first_scan_is_retried_before_reuse(self):
        f = self.fixture
        f.create_partial()
        with ScreeningRunView.open(f.path) as view:
            with patch.object(
                view._view._ledger, "_outcome", side_effect=ValueError("read failed")
            ):
                with self.assertRaises(ScreeningRunError) as caught:
                    view.progress()
                self.assertEqual(str(caught.exception.__cause__), "read failed")
            expected = view.progress()
            self.assertEqual(expected["counts"]["committed_work"], 4)
            self.assert_reused(view, expected)

    def test_closed_snapshot_refuses_progress_after_priming(self):
        f = self.fixture
        f.create_partial()
        with ScreeningRunView.open(f.path) as view:
            view.progress()
        with self.assertRaises(ScreeningRunError) as caught:
            view.progress()
        self.assertEqual(str(caught.exception.__cause__), "ledger is closed")

    def test_native_connection_close_refuses_progress_after_priming(self):
        f = self.fixture
        f.create_partial()
        with ScreeningRunView.open(f.path) as view:
            view.progress()
            view._view._ledger._db().close()
            with self.assertRaises(ScreeningRunError) as caught:
                view.progress()
            self.assertIsInstance(caught.exception.__cause__, sqlite3.ProgrammingError)

    def test_wrong_thread_refuses_progress_after_priming_without_poisoning_owner(self):
        f = self.fixture
        f.create_partial()
        with ScreeningRunView.open(f.path) as view:
            expected = view.progress()
            with ThreadPoolExecutor(max_workers=1) as worker:
                future = worker.submit(view.progress)
                with self.assertRaises(ScreeningRunError) as caught:
                    future.result()
            self.assertIsInstance(caught.exception.__cause__, sqlite3.ProgrammingError)
            self.assertEqual(view.progress(), expected)

    def test_writer_counts_remain_fresh_between_each_publication_step(self):
        f = self.fixture
        with f.create() as store:
            original = store.progress()
            self.assertEqual(
                original["attempts"], dict(started=0, staged=0, committed=0)
            )
            attempt = store.begin("alpha")
            self.assertEqual(
                store.progress()["attempts"], dict(started=1, staged=0, committed=0)
            )
            store.stage(attempt, f.outcome("alpha"))
            self.assertEqual(
                store.progress()["attempts"], dict(started=1, staged=1, committed=0)
            )
            self.assertEqual(store.progress()["counts"]["committed_work"], 0)
            store.publish(attempt)
            result = store.progress()
            self.assertEqual(result["attempts"], dict(started=1, staged=1, committed=1))
            self.assertEqual(result["counts"]["matched_work"], 1)
            self.assertEqual(original["counts"]["committed_work"], 0)

    def test_empty_snapshot_reuses_zero_counts(self):
        f = self.fixture
        f.mapping = []
        f.write_manifest()
        with f.create():
            pass
        with ScreeningRunView.open(f.path) as view:
            expected = view.progress()
            self.assertTrue(expected["manifest_work_complete"])
            self.assertEqual(set(expected["counts"].values()), {0})
            self.assert_reused(view, expected)

    def test_complete_snapshot_reuses_counts_and_reopened_snapshot_sees_changes(self):
        f = self.fixture
        f.create_partial()
        with ScreeningRunView.open(f.path) as view:
            previous = view.progress()
        with f.reopen() as store:
            f.publish(store, "epsilon", score=None, status="failed")
        with ScreeningRunView.open(f.path) as view:
            expected = view.progress()
            self.assertTrue(expected["manifest_work_complete"])
            self.assertEqual(expected["counts"]["committed_work"], 5)
            self.assertEqual(expected["counts"]["failed_work"], 2)
            self.assertEqual(previous["counts"]["committed_work"], 4)
            self.assert_reused(view, expected)

    def test_explicit_legacy_snapshot_reuses_counts_without_merging_score_criteria(
        self,
    ):
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
        with self.assertRaises(ScreeningRunError):
            ScreeningRunView.open(f.path)
        original = f.directory_bytes()
        with ScreeningRunView.open(f.path, allow_legacy=True) as view:
            expected = view.progress()
            self.assertEqual(expected["counts"]["scored_work"], 2)
            self.assert_reused(view, expected)
            for criterion in (fixtures.CRITERION, "seeded_hit@1"):
                with self.assertRaises(ScreeningRunError):
                    view.summary(score_method=criterion)
            self.assert_reused(view, expected)
        self.assertEqual(f.directory_bytes(), original)
