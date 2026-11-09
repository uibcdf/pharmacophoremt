"""Original saved status selection without scoring, draft disclosure or regrouping."""

import io
import json
import sqlite3
import threading
import unittest
from contextlib import closing, redirect_stderr, redirect_stdout
from unittest.mock import patch

import test_public_run_results as fixtures

from pharmacophoremt_results import ScreeningRunError, ScreeningRunView, _store, main


class TestPublicWorkSelection(unittest.TestCase):
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

    def records(self, *ordinals):
        return [{"manifest_ordinal": n, **self.fixture.mapping[n]} for n in ordinals]

    def page(self, status, *arguments):
        f = self.fixture
        result = f.command(f.path, "--work-items", "--status", status, *arguments)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_status_selection_preserves_original_positions_and_distinctions(self):
        f = self.fixture
        f.mapping.extend(
            [
                dict(
                    work_key="never",
                    source_key="source:repeated",
                    occurrence_key="same",
                ),
                dict(
                    work_key="matched-zero",
                    source_key="source:repeated",
                    occurrence_key="same",
                ),
            ]
        )
        f.write_manifest()
        f.create_partial()
        with f.reopen() as store:
            f.publish(store, "matched-zero", score=0)
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            expected = {
                "matched": [0, 1, 6],
                "not_matched": [2],
                "failed": [3],
                "pending": [4, 5],
            }
            for status, ordinals in expected.items():
                with self.subTest(status=status):
                    self.assertEqual(
                        list(view.work_items(status=status)), self.records(*ordinals)
                    )
            self.assertEqual(list(view.work_items()), self.records(*range(7)))
            self.assertEqual(
                list(view.work_items(status=None)), self.records(*range(7))
            )
        self.assertEqual(f.directory_bytes(), before)

    def test_pending_uses_publication_membership_without_draft_or_native_output(self):
        f = self.fixture
        f.create_partial()
        with f.reopen() as store:
            attempt = store.begin("epsilon")
            draft = f.outcome("epsilon", score=None, status="failed")
            draft["native_result"]["secret"] = "unpublished detail"
            store.stage(attempt, draft)
        with ScreeningRunView.open(f.path) as view:
            self.assertEqual(list(view.work_items(status="failed")), self.records(3))
            with patch.object(
                _store.ReferenceLedger,
                "_outcome",
                side_effect=AssertionError("no extra outcome decoding"),
            ):
                records = list(view.work_items(status="pending"))
            self.assertEqual(records, self.records(4))
            self.assertNotIn("secret", json.dumps(records))
        page = self.page("pending")
        self.assertEqual(page["records"], self.records(4))
        self.assertNotIn("native_result", json.dumps(page))

    def test_confirmed_selection_is_lazy_and_early_close_releases_its_iterator(self):
        f = self.fixture
        f.create_partial()
        decoded = []
        original = _store.ReferenceLedger._outcome

        def tracked(ledger, key, *arguments):
            decoded.append(key)
            return original(ledger, key, *arguments)

        with ScreeningRunView.open(f.path) as view:
            with patch.object(_store.ReferenceLedger, "_outcome", tracked):
                source = view.work_items(status="matched")
                self.assertEqual(decoded, [])
                self.assertEqual(next(source), self.records(0)[0])
                self.assertEqual(decoded, ["alpha"])
                source.close()
                self.assertEqual(decoded, ["alpha"])
            self.assertEqual(view.work_item("gamma")["status"], "not_matched")

    def test_status_and_call_shape_admission_are_closed(self):
        f = self.fixture
        f.create_partial()
        with ScreeningRunView.open(f.path) as view:
            for status in [
                "",
                "FAILED",
                "all",
                "staged",
                "unknown",
                0,
                False,
                b"failed",
                [],
                {},
            ]:
                with self.subTest(status=status), self.assertRaises(ScreeningRunError):
                    list(view.work_items(status=status))
            with self.assertRaises(TypeError):
                view.work_items("failed")
            for options in [
                {"unknown": 1},
                {"skip_digestion": True},
                {"skip_digestion": False},
            ]:
                with self.subTest(options=options), self.assertRaises(TypeError):
                    view.work_items(**options)

    def test_filtered_records_are_detached_and_keep_closed_thread_errors(self):
        f = self.fixture
        f.create_partial()
        errors = []
        with ScreeningRunView.open(f.path) as view:
            result = list(view.work_items(status="failed"))
            result[0].clear()
            self.assertEqual(list(view.work_items(status="failed")), self.records(3))

            def foreign():
                try:
                    list(view.work_items(status="pending"))
                except Exception as error:
                    errors.append(error)

            thread = threading.Thread(target=foreign)
            thread.start()
            thread.join(timeout=5)
            self.assertFalse(thread.is_alive())
            self.assertEqual(len(errors), 1)
            self.assertIsInstance(errors[0], ScreeningRunError)
            iterator = view.work_items(status="failed")
        with self.assertRaises(ScreeningRunError):
            next(iterator)

    def test_deferred_decoder_failure_remains_structured(self):
        f = self.fixture
        f.create_partial()
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            with patch.object(
                _store.ReferenceLedger,
                "_outcome",
                side_effect=ValueError("original read failed"),
            ):
                with self.assertRaises(ScreeningRunError) as caught:
                    list(view.work_items(status="matched"))
            self.assertIn("original read failed", str(caught.exception))
        self.assertEqual(f.directory_bytes(), before)

    def test_selection_pages_use_selected_offsets_and_original_global_ordinals(self):
        f = self.fixture
        f.mapping.extend(
            dict(work_key=f"never:{i}", source_key="repeat:β", occurrence_key="same")
            for i in range(4)
        )
        f.write_manifest()
        f.create_partial()
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            work_hash = view.configuration["work_sha256"]
        for offset, ordinals, following in [
            (0, [4, 5], 2),
            (2, [6, 7], 4),
            (4, [8], None),
        ]:
            page = self.page("pending", "--limit", 2, "--offset", offset)
            self.assertEqual(
                page,
                {
                    "format": "pharmacophoremt.screening-work-selection@1",
                    "run_id": "run:public",
                    "run_format": "pharmacophoremt.screening-run@1",
                    "work_sha256": work_hash,
                    "declared_work": 9,
                    "selected_work": 5,
                    "status": "pending",
                    "offset": offset,
                    "limit": 2,
                    "next_offset": following,
                    "records": self.records(*ordinals),
                },
            )
        self.assertEqual(f.directory_bytes(), before)

    def test_all_status_counts_and_fresh_commands_match_independent_original_records(
        self,
    ):
        f = self.fixture
        f.create_partial()
        before = f.directory_bytes()
        for status, ordinals in [
            ("matched", [0, 1]),
            ("not_matched", [2]),
            ("failed", [3]),
            ("pending", [4]),
        ]:
            with self.subTest(status=status):
                page = self.page(status)
                self.assertEqual(page["records"], self.records(*ordinals))
                self.assertEqual(page["selected_work"], len(ordinals))
                self.assertEqual(page["declared_work"], 5)
                self.assertIsNone(page["next_offset"])
                self.assertEqual(page["status"], status)
        self.assertEqual(f.directory_bytes(), before)

    def test_empty_absent_and_arbitrary_precision_selection_windows(self):
        f = self.fixture
        f.create_partial()
        for offset in [1, 2, 10**30]:
            page = self.page("failed", "--offset", offset)
            self.assertEqual(page["selected_work"], 1)
            self.assertEqual(page["records"], [])
            self.assertIsNone(page["next_offset"])
        page = self.page("failed", "--limit", 10**30)
        self.assertEqual(page["limit"], 10**30)
        self.assertEqual(page["records"], self.records(3))
        with f.reopen() as store:
            f.publish(store, "epsilon", score=1)
        absent = self.page("pending")
        self.assertEqual(absent["selected_work"], 0)
        self.assertEqual(absent["records"], [])
        f.path = f.root / "empty.sqlite3"
        f.mapping = []
        f.write_manifest()
        with f.create():
            pass
        for status in ["failed", "pending", "matched", "not_matched"]:
            page = self.page(status)
            self.assertEqual(page["selected_work"], 0)
            self.assertEqual(page["declared_work"], 0)
            self.assertIsNone(page["next_offset"])

    def test_legacy_mixed_criteria_need_explicit_admission_without_combining_scores(
        self,
    ):
        f = self.fixture
        with f.legacy().create(
            f.path,
            run_id="mixed:legacy",
            query_bytes=f.query,
            context={"execution": {}},
            manifest_path=f.manifest,
        ) as store:
            f.publish(store, "alpha")
            beta = f.outcome("beta", score=1)
            beta["score_method"] = "seeded_hit@1"
            attempt = store.begin("beta")
            store.stage(attempt, beta)
            store.publish(attempt)
            f.publish(store, "delta", score=None, status="failed")
        before = f.directory_bytes()
        denied = f.command(f.path, "--work-items", "--status", "failed")
        self.assertEqual(denied.returncode, 2)
        self.assertEqual(denied.stdout, "")
        with ScreeningRunView.open(f.path, allow_legacy=True) as view:
            self.assertEqual(
                list(view.work_items(status="matched")), self.records(0, 1)
            )
            self.assertEqual(
                list(view.work_items(status="pending")), self.records(2, 4)
            )
        page = self.page("failed", "--allow-legacy")
        self.assertEqual(page["run_format"], "pharmacophoremt.reference-ledger@1")
        self.assertEqual(page["records"], self.records(3))
        self.assertEqual(f.directory_bytes(), before)

    def test_status_conflicts_and_invalid_syntax_refuse_before_database_io(self):
        f = self.fixture
        for arguments in [
            ["--status", "failed"],
            ["--summary", "--status", "failed"],
            ["--work-key", "alpha", "--status", "failed"],
            ["--to-jsonl", f.root / "new.jsonl", "--status", "failed"],
            ["--score-method", fixtures.CRITERION, "--status", "failed"],
            ["--work-items", "--status", "unknown"],
            ["--work-items", "--status", "FAILED"],
            ["--work-items", "--status", "failed", "--limit", 0],
            ["--work-items", "--status", "pending", "--offset", -1],
            [
                "--work-items",
                "--status",
                "failed",
                "--score-method",
                fixtures.CRITERION,
            ],
        ]:
            with (
                self.subTest(arguments=arguments),
                patch.object(ScreeningRunView, "open") as opened,
            ):
                code, stdout, stderr = self.invoke(f.path, *arguments)
                self.assertEqual(code, 2)
                self.assertEqual(stdout, "")
                self.assertTrue(stderr)
                opened.assert_not_called()
        self.assertFalse(f.path.exists() or (f.root / "new.jsonl").exists())

    def test_selection_count_iteration_and_close_failures_leave_stdout_empty(self):
        f = self.fixture
        f.create_partial()
        with patch.object(
            ScreeningRunView,
            "progress",
            side_effect=ScreeningRunError(
                operation="count work", reason="count unavailable"
            ),
        ):
            code, stdout, stderr = self.invoke(
                f.path, "--work-items", "--status", "failed"
            )
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("count unavailable", stderr)
        closed = []

        def failing(view, *, status=None):
            try:
                yield self.records(0)[0]
                raise ScreeningRunError(
                    operation="select work", reason="selection unavailable"
                )
            finally:
                closed.append(True)

        with patch.object(ScreeningRunView, "work_items", failing):
            code, stdout, stderr = self.invoke(
                f.path, "--work-items", "--status", "matched", "--limit", 2
            )
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("selection unavailable", stderr)
        self.assertEqual(closed, [True])
        original = ScreeningRunView.close

        def fail_close(view):
            original(view)
            raise ScreeningRunError(operation="close work", reason="close unavailable")

        with patch.object(ScreeningRunView, "close", fail_close):
            code, stdout, stderr = self.invoke(
                f.path, "--work-items", "--status", "failed"
            )
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("close unavailable", stderr)

    def test_complete_file_admission_is_not_bypassed_by_a_status_filter(self):
        f = self.fixture
        f.create_partial()
        with closing(sqlite3.connect(f.path)) as connection, connection:
            connection.execute("UPDATE work SET source_key='changed' WHERE ordinal=0")
        before = f.directory_bytes()
        result = f.command(f.path, "--work-items", "--status", "pending")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr)
        self.assertEqual(f.directory_bytes(), before)

    def test_help_documents_the_filter_without_opening_a_file(self):
        result = self.fixture.command("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--status", result.stdout)
        self.assertIn("pending", result.stdout)
        self.assertFalse(self.fixture.path.exists())
