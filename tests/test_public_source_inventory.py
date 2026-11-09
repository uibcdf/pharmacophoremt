"""Original declared-source browsing without chemical grouping or payload access."""

import io
import json
import sqlite3
import threading
import unittest
from contextlib import closing, redirect_stderr, redirect_stdout
from unittest.mock import patch

import test_public_run_results as fixtures

from pharmacophoremt_results import ScreeningRunError, ScreeningRunView, _store, main


class TestPublicSourceInventory(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.TestPublicRunResults()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def records(self, *rows):
        return [
            dict(source_key=key, first_manifest_ordinal=first, declared_work=count)
            for key, first, count in rows
        ]

    def mixed(self):
        f = self.fixture
        for n, key in enumerate(
            ("source:z", "source:a", "source:z", "β:other", "source:z")
        ):
            f.mapping[n].update(source_key=key, occurrence_key="same")
        f.mapping.append(dict(work_key="never", source_key="0", occurrence_key="same"))
        f.write_manifest()
        f.create_partial()
        return self.records(
            ("source:z", 0, 3), ("source:a", 1, 1), ("β:other", 3, 1), ("0", 5, 1)
        )

    def page(self, *arguments):
        f = self.fixture
        result = f.command(f.path, "--sources", *arguments)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def invoke(self, *arguments):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                code = main(list(map(str, arguments)))
            except SystemExit as error:
                code = error.code
        return code, stdout.getvalue(), stderr.getvalue()

    def test_original_first_encounter_order_counts_all_work_and_repetitions(self):
        expected = self.mixed()
        f = self.fixture
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            self.assertEqual(list(view.source_items()), expected)
            self.assertEqual(sum(r["declared_work"] for r in expected), 6)
            self.assertEqual(view.progress()["counts"]["pending_work"], 2)
        self.assertEqual(f.directory_bytes(), before)

    def test_opaque_keys_keep_whitespace_case_unicode_zero_and_embedded_nul(self):
        f = self.fixture
        keys = [
            " 0 ",
            "0",
            "z",
            "A",
            "a",
            "β' OR 1=1 --",
            "nul\0key",
            "--source α",
            "z",
            " 0 ",
        ]
        f.mapping = [
            dict(work_key=str(n), source_key=key, occurrence_key="same")
            for n, key in enumerate(keys)
        ]
        f.write_manifest()
        with f.create():
            pass
        expected = self.records(
            (" 0 ", 0, 2),
            ("0", 1, 1),
            ("z", 2, 2),
            ("A", 3, 1),
            ("a", 4, 1),
            ("β' OR 1=1 --", 5, 1),
            ("nul\0key", 6, 1),
            ("--source α", 7, 1),
        )
        with ScreeningRunView.open(f.path) as view:
            self.assertEqual(list(view.source_items()), expected)
        self.assertEqual(self.page()["records"], expected)

    def test_publication_does_not_change_the_immutable_manifest_inventory(self):
        expected = self.mixed()
        f = self.fixture
        with ScreeningRunView.open(f.path) as view:
            self.assertEqual(list(view.source_items()), expected)
            before_hash = view.configuration["work_sha256"]
        with f.reopen() as store:
            f.publish(store, "epsilon", score=1)
            f.publish(store, "never", score=None, status="failed")
        with ScreeningRunView.open(f.path) as view:
            self.assertEqual(list(view.source_items()), expected)
            self.assertEqual(view.configuration["work_sha256"], before_hash)
            self.assertEqual(view.progress()["counts"]["pending_work"], 0)

    def test_empty_and_explicit_legacy_admission_preserve_originals(self):
        f = self.fixture
        f.create_legacy()
        before = f.directory_bytes()
        denied = f.command(f.path, "--sources")
        self.assertEqual(denied.returncode, 2)
        self.assertEqual(denied.stdout, "")
        expected = self.records(
            ("source:repeated", 0, 2),
            ("source:2", 2, 1),
            ("source:3", 3, 1),
            ("source:4", 4, 1),
        )
        with ScreeningRunView.open(f.path, allow_legacy=True) as view:
            self.assertEqual(list(view.source_items()), expected)
        self.assertEqual(self.page("--allow-legacy")["records"], expected)
        self.assertEqual(f.directory_bytes(), before)
        f.path = f.root / "empty.sqlite3"
        f.mapping = []
        f.write_manifest()
        with f.create():
            pass
        page = self.page()
        self.assertEqual(
            (page["declared_sources"], page["declared_work"], page["records"]),
            (0, 0, []),
        )
        self.assertIsNone(page["next_offset"])

    def test_inventory_needs_no_outcome_decoding_after_complete_admission(self):
        expected = self.mixed()
        with ScreeningRunView.open(self.fixture.path) as view:
            with patch.object(
                _store.ReferenceLedger,
                "_outcome",
                side_effect=AssertionError("no extra payload decode"),
            ):
                self.assertEqual(list(view.source_items()), expected)
        self.assertEqual(
            set(expected[0]), {"source_key", "first_manifest_ordinal", "declared_work"}
        )

    def test_definition_owned_inheritance_and_call_shape_are_closed(self):
        expected = self.mixed()

        class DerivedView(ScreeningRunView):
            pass

        with DerivedView.open(self.fixture.path) as view:
            self.assertEqual(list(view.source_items()), expected)
            with self.assertRaises(TypeError):
                view.source_items("source:z")
            for options in (
                {"status": "failed"},
                {"source_key": "source:z"},
                {"skip_digestion": True},
                {"unknown": 1},
            ):
                with self.subTest(options=options), self.assertRaises(TypeError):
                    view.source_items(**options)

    def test_lazy_detached_early_close_foreign_thread_and_closed_view_boundaries(self):
        expected = self.mixed()
        errors = []
        with ScreeningRunView.open(self.fixture.path) as view:
            rows = list(view.source_items())
            rows[0].clear()
            source = view.source_items()
            self.assertEqual(next(source), expected[0])
            source.close()
            self.assertIsNone(source.gi_frame)
            self.assertEqual(list(view.source_items()), expected)

            def foreign():
                try:
                    list(view.source_items())
                except Exception as error:
                    errors.append(error)

            thread = threading.Thread(target=foreign)
            thread.start()
            thread.join(timeout=5)
            self.assertFalse(thread.is_alive())
            self.assertEqual(len(errors), 1)
            self.assertIsInstance(errors[0], ScreeningRunError)
            future = view.source_items()
        with self.assertRaises(ScreeningRunError):
            next(future)

    def test_late_core_read_failure_remains_a_structured_reader_error(self):
        expected = self.mixed()

        def broken(core):
            yield expected[0]
            raise sqlite3.DatabaseError("original inventory unavailable")

        with ScreeningRunView.open(self.fixture.path) as view:
            with patch.object(_store.ReferenceRunView, "source_items", broken):
                source = view.source_items()
                self.assertEqual(next(source), expected[0])
                with self.assertRaises(ScreeningRunError) as caught:
                    next(source)
                self.assertIn("original inventory unavailable", str(caught.exception))

    def test_cli_pages_have_exact_totals_identities_and_first_global_ordinals(self):
        expected = self.mixed()
        f = self.fixture
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            work_hash = view.configuration["work_sha256"]
        for offset, records, following in [
            (0, expected[:2], 2),
            (2, expected[2:], None),
        ]:
            self.assertEqual(
                self.page("--offset", offset, "--limit", 2),
                dict(
                    format="pharmacophoremt.screening-source-page@1",
                    run_id="run:public",
                    run_format="pharmacophoremt.screening-run@1",
                    work_sha256=work_hash,
                    declared_work=6,
                    declared_sources=4,
                    offset=offset,
                    limit=2,
                    next_offset=following,
                    records=records,
                ),
            )
        self.assertEqual(f.directory_bytes(), before)

    def test_cli_arbitrary_precision_windows_and_complete_single_stream_count(self):
        expected = self.mixed()
        for offset in (4, 5, 10**30):
            page = self.page("--offset", offset)
            self.assertEqual(page["records"], [])
            self.assertEqual(page["declared_sources"], 4)
            self.assertIsNone(page["next_offset"])
        self.assertEqual(self.page("--limit", 10**30)["records"], expected)
        original = ScreeningRunView.source_items
        calls = []

        def tracked(view):
            calls.append(True)
            return original(view)

        with (
            patch.object(ScreeningRunView, "source_items", tracked),
            patch.object(
                ScreeningRunView,
                "progress",
                side_effect=AssertionError("no unrelated global count"),
            ),
        ):
            code, stdout, stderr = self.invoke(
                self.fixture.path, "--sources", "--limit=1"
            )
        self.assertEqual(code, 0, stderr)
        self.assertEqual(json.loads(stdout)["declared_sources"], 4)
        self.assertEqual(calls, [True])

    def test_cli_invalid_modes_filters_and_windows_refuse_before_file_access(self):
        f = self.fixture
        for args in [
            ("--sources", "--summary"),
            ("--sources", "--work-items"),
            ("--sources", "--work-key=alpha"),
            ("--sources", "--to-jsonl", f.root / "new.jsonl"),
            ("--sources", "--status=failed"),
            ("--sources", "--source-key=source:z"),
            ("--sources", "--score-method", fixtures.CRITERION),
            ("--sources", "--limit=0"),
            ("--sources", "--offset=-1"),
        ]:
            with (
                self.subTest(args=args),
                patch.object(ScreeningRunView, "open") as opened,
            ):
                code, stdout, stderr = self.invoke(f.path, *args)
                self.assertEqual(code, 2)
                self.assertEqual(stdout, "")
                self.assertTrue(stderr)
                opened.assert_not_called()
        self.assertFalse(f.path.exists())

    def test_late_count_and_view_close_failures_leave_no_success_json(self):
        expected = self.mixed()
        closed = []

        def broken(view):
            try:
                yield expected[0]
                raise ScreeningRunError(
                    operation="count sources", reason="late source count failed"
                )
            finally:
                closed.append(True)

        with patch.object(ScreeningRunView, "source_items", broken):
            code, stdout, stderr = self.invoke(
                self.fixture.path, "--sources", "--limit=1"
            )
        self.assertEqual((code, stdout), (2, ""))
        self.assertIn("late source count failed", stderr)
        self.assertEqual(closed, [True])
        original = ScreeningRunView.close

        def broken_close(view):
            original(view)
            raise ScreeningRunError(
                operation="close source page", reason="source close failed"
            )

        with patch.object(ScreeningRunView, "close", broken_close):
            code, stdout, stderr = self.invoke(self.fixture.path, "--sources")
        self.assertEqual((code, stdout), (2, ""))
        self.assertIn("source close failed", stderr)

    def test_complete_file_verification_includes_work_outside_the_displayed_prefix(
        self,
    ):
        self.mixed()
        f = self.fixture
        with closing(sqlite3.connect(f.path)) as db, db:
            db.execute("UPDATE work SET source_key='changed' WHERE work_key='never'")
        before = f.directory_bytes()
        result = f.command(f.path, "--sources", "--limit=1")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertEqual(f.directory_bytes(), before)

    def test_fresh_reader_and_help_need_no_scientific_provider_or_file(self):
        expected = self.mixed()
        result = self.fixture.fresh(
            "import json\nfrom pharmacophoremt_results import ScreeningRunView\nwith ScreeningRunView.open(sys.argv[1]) as view:\n print(json.dumps(list(view.source_items()), ensure_ascii=False))",
            self.fixture.path,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), expected)
        help_text = self.fixture.command("--help")
        self.assertEqual(help_text.returncode, 0, help_text.stderr)
        self.assertIn("--sources", help_text.stdout)
