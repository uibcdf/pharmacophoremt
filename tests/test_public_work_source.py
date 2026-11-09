"""Exact original source selection without chemical grouping or new execution."""

import io
import json
import sqlite3
import threading
import unittest
from contextlib import closing, redirect_stderr, redirect_stdout
from unittest.mock import patch

import test_public_run_results as fixtures

from pharmacophoremt_results import ScreeningRunError, ScreeningRunView, _store, main


class TestPublicWorkSource(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.TestPublicRunResults()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def records(self, *ordinals):
        return [{"manifest_ordinal": n, **self.fixture.mapping[n]} for n in ordinals]

    def invoke(self, *arguments):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                code = main(list(map(str, arguments)))
            except SystemExit as error:
                code = error.code
        return code, stdout.getvalue(), stderr.getvalue()

    def mixed(self):
        f = self.fixture
        for n in (0, 2, 3, 4):
            f.mapping[n]["source_key"] = "repeat:β"
            f.mapping[n]["occurrence_key"] = "same"
        f.mapping.append(
            dict(work_key="never", source_key="repeat:β", occurrence_key="same")
        )
        f.mapping.append(
            dict(work_key="zero", source_key="repeat:β", occurrence_key="same")
        )
        f.write_manifest()
        f.create_partial()
        with f.reopen() as store:
            f.publish(store, "zero", score=0)

    def page(self, source, *arguments):
        f = self.fixture
        result = f.command(f.path, "--work-items", "--source-key=" + source, *arguments)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_exact_source_and_status_intersections_keep_original_repeated_work(self):
        self.mixed()
        f = self.fixture
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            self.assertEqual(
                list(view.work_items(source_key="repeat:β")),
                self.records(0, 2, 3, 4, 5, 6),
            )
            for status, ordinals in [
                ("matched", (0, 6)),
                ("not_matched", (2,)),
                ("failed", (3,)),
                ("pending", (4, 5)),
            ]:
                self.assertEqual(
                    list(view.work_items(status=status, source_key="repeat:β")),
                    self.records(*ordinals),
                )
            self.assertEqual(
                list(view.work_items(source_key=None)), self.records(*range(7))
            )
            self.assertEqual(
                list(view.work_items(status="matched", source_key=None)),
                self.records(0, 1, 6),
            )
            self.assertEqual(list(view.work_items(source_key="absent")), [])
        self.assertEqual(f.directory_bytes(), before)

    def test_opaque_keys_are_literal_and_parameterized(self):
        f = self.fixture
        keys = ["0", " x ", "x", "β' OR 1=1 --", "--literal value", "nul\0key", "X"]
        f.mapping = [
            dict(work_key=str(n), source_key=key, occurrence_key="same")
            for n, key in enumerate(keys)
        ]
        f.write_manifest()
        with f.create():
            pass
        with ScreeningRunView.open(f.path) as view:
            for n, key in enumerate(keys):
                self.assertEqual(list(view.work_items(source_key=key)), self.records(n))
                self.assertEqual(
                    list(view.work_items(source_key=key, status="pending")),
                    self.records(n),
                )
            self.assertEqual(list(view.work_items(source_key="β")), [])
        for n in (0, 1, 3, 4):
            self.assertEqual(self.page(keys[n])["records"], self.records(n))

    def test_invalid_source_values_and_call_shape_refuse(self):
        f = self.fixture
        f.create_partial()
        with ScreeningRunView.open(f.path) as view:
            for value in ("", " \t\n", 0, False, b"source:repeated", [], {}):
                with self.subTest(value=value), self.assertRaises(ScreeningRunError):
                    list(view.work_items(source_key=value))
            with self.assertRaises(TypeError):
                view.work_items("source:repeated")
            with self.assertRaises(TypeError):
                view.work_items(source="source:repeated")

    def test_selection_is_lazy_and_does_not_decode_unrelated_sources(self):
        self.mixed()
        f = self.fixture
        decoded = []
        original = _store.ReferenceLedger._outcome

        def tracked(ledger, key, *args):
            self.assertNotEqual(key, "beta")
            decoded.append(key)
            return original(ledger, key, *args)

        with ScreeningRunView.open(f.path) as view:
            with patch.object(_store.ReferenceLedger, "_outcome", tracked):
                source = view.work_items(source_key="repeat:β", status="matched")
                self.assertEqual(decoded, [])
                self.assertEqual(next(source), self.records(0)[0])
                source.close()
                self.assertEqual(decoded, ["alpha"])
                self.assertEqual(
                    list(view.work_items(source_key="repeat:β", status="matched")),
                    self.records(0, 6),
                )
            with patch.object(
                _store.ReferenceLedger,
                "_outcome",
                side_effect=AssertionError("draft decoding"),
            ):
                rows = list(view.work_items(source_key="repeat:β", status="pending"))
                self.assertEqual(rows, self.records(4, 5))
                self.assertNotIn("native_result", json.dumps(rows))

    def test_detachment_closed_thread_and_late_errors_remain_structured(self):
        self.mixed()
        f = self.fixture
        errors = []
        with ScreeningRunView.open(f.path) as view:
            rows = list(view.work_items(source_key="repeat:β"))
            rows[0].clear()
            self.assertEqual(
                list(view.work_items(source_key="repeat:β"))[0], self.records(0)[0]
            )

            def foreign():
                try:
                    list(view.work_items(source_key="repeat:β"))
                except Exception as error:
                    errors.append(error)

            thread = threading.Thread(target=foreign)
            thread.start()
            thread.join(timeout=5)
            self.assertFalse(thread.is_alive())
            self.assertEqual(len(errors), 1)
            self.assertIsInstance(errors[0], ScreeningRunError)
            with patch.object(
                _store.ReferenceLedger,
                "_outcome",
                side_effect=ValueError("late source failure"),
            ):
                with self.assertRaises(ScreeningRunError) as caught:
                    list(view.work_items(source_key="repeat:β", status="matched"))
                self.assertIn("late source failure", str(caught.exception))
            source = view.work_items(source_key="repeat:β")
        with self.assertRaises(ScreeningRunError):
            next(source)

    def test_cli_pages_count_the_intersection_and_keep_global_ordinals(self):
        self.mixed()
        f = self.fixture
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            work_hash = view.configuration["work_sha256"]
        for offset, ordinals, following in [
            (0, (0, 2), 2),
            (2, (3, 4), 4),
            (4, (5, 6), None),
        ]:
            self.assertEqual(
                self.page("repeat:β", "--offset", offset, "--limit", 2),
                dict(
                    format="pharmacophoremt.screening-work-selection@2",
                    run_id="run:public",
                    run_format="pharmacophoremt.screening-run@1",
                    work_sha256=work_hash,
                    declared_work=7,
                    selected_work=6,
                    source_key="repeat:β",
                    status=None,
                    offset=offset,
                    limit=2,
                    next_offset=following,
                    records=self.records(*ordinals),
                ),
            )
        for status, ordinals in [
            ("matched", (0, 6)),
            ("not_matched", (2,)),
            ("failed", (3,)),
            ("pending", (4, 5)),
        ]:
            page = self.page("repeat:β", "--status", status)
            self.assertEqual(page["selected_work"], len(ordinals))
            self.assertEqual(page["status"], status)
            self.assertEqual(page["records"], self.records(*ordinals))
        self.assertEqual(f.directory_bytes(), before)

    def test_empty_unknown_and_arbitrary_precision_windows(self):
        self.mixed()
        for offset in (6, 7, 10**30):
            page = self.page("repeat:β", "--offset", offset)
            self.assertEqual(page["records"], [])
            self.assertEqual(page["selected_work"], 6)
            self.assertIsNone(page["next_offset"])
        self.assertEqual(
            self.page("repeat:β", "--limit", 10**30)["records"],
            self.records(0, 2, 3, 4, 5, 6),
        )
        self.assertEqual(self.page("absent")["selected_work"], 0)
        f = self.fixture
        f.path = f.root / "empty.sqlite3"
        f.mapping = []
        f.write_manifest()
        with f.create():
            pass
        page = self.page("absent", "--status", "pending")
        self.assertEqual(
            (page["selected_work"], page["declared_work"], page["records"]), (0, 0, [])
        )

    def test_cli_invalid_modes_keys_and_dash_ambiguity_refuse_before_io(self):
        f = self.fixture
        for arguments in [
            ("--source-key=x",),
            ("--summary", "--source-key=x"),
            ("--work-key=alpha", "--source-key=x"),
            ("--to-jsonl", f.root / "new.jsonl", "--source-key=x"),
            ("--score-method", fixtures.CRITERION, "--source-key=x"),
            ("--work-items", "--source-key="),
            ("--work-items", "--source-key= \t"),
            ("--work-items", "--source-key", "--literal"),
            ("--work-items", "--source-key=x", "--limit", 0),
            ("--work-items", "--source-key=x", "--offset", -1),
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
        self.assertFalse(f.path.exists())

    def test_cli_finishes_count_after_page_and_closes_before_success(self):
        self.mixed()
        f = self.fixture
        closed = []

        def failing(view, *, source_key=None, status=None):
            try:
                yield self.records(0)[0]
                raise ScreeningRunError(
                    operation="count source", reason="late count failure"
                )
            finally:
                closed.append(True)

        with patch.object(ScreeningRunView, "work_items", failing):
            code, stdout, stderr = self.invoke(
                f.path, "--work-items", "--source-key=repeat:β", "--limit", 1
            )
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("late count failure", stderr)
        self.assertEqual(closed, [True])
        original = ScreeningRunView.close

        def fail_close(view):
            original(view)
            raise ScreeningRunError(
                operation="close source", reason="source close failure"
            )

        with patch.object(ScreeningRunView, "close", fail_close):
            code, stdout, stderr = self.invoke(
                f.path, "--work-items", "--source-key=repeat:β"
            )
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("source close failure", stderr)

    def test_one_selected_stream_in_one_verified_snapshot_without_progress_count(self):
        self.mixed()
        calls = []
        original = ScreeningRunView.work_items

        def tracked(view, **options):
            calls.append(options)
            return original(view, **options)

        with (
            patch.object(ScreeningRunView, "work_items", tracked),
            patch.object(
                ScreeningRunView,
                "progress",
                side_effect=AssertionError("unrelated global status count"),
            ),
        ):
            code, stdout, stderr = self.invoke(
                self.fixture.path,
                "--work-items",
                "--source-key=repeat:β",
                "--status=pending",
                "--limit=1",
            )
        self.assertEqual(code, 0, stderr)
        self.assertEqual(json.loads(stdout)["selected_work"], 2)
        self.assertEqual(calls, [dict(source_key="repeat:β", status="pending")])

    def test_full_verification_rejects_corruption_outside_selected_source(self):
        self.mixed()
        f = self.fixture
        with closing(sqlite3.connect(f.path)) as connection, connection:
            connection.execute(
                "UPDATE work SET source_key='changed' WHERE work_key='beta'"
            )
        before = f.directory_bytes()
        result = f.command(
            f.path, "--work-items", "--source-key=repeat:β", "--status=pending"
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr)
        self.assertEqual(f.directory_bytes(), before)

    def test_explicit_legacy_source_selection_preserves_mixed_criteria(self):
        f = self.fixture
        with f.legacy().create(
            f.path,
            run_id="legacy",
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
        before = f.directory_bytes()
        refused = f.command(f.path, "--work-items", "--source-key=source:repeated")
        self.assertEqual(refused.returncode, 2)
        self.assertEqual(refused.stdout, "")
        with ScreeningRunView.open(f.path, allow_legacy=True) as view:
            self.assertEqual(
                list(view.work_items(source_key="source:repeated", status="matched")),
                self.records(0, 1),
            )
        self.assertEqual(
            self.page("source:repeated", "--allow-legacy", "--status=matched")[
                "records"
            ],
            self.records(0, 1),
        )
        self.assertEqual(f.directory_bytes(), before)

    def test_help_exposes_exact_source_selection_without_file_access(self):
        result = self.fixture.command("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--source-key", result.stdout)
        self.assertIn("exact original source", result.stdout)
        self.assertFalse(self.fixture.path.exists())
