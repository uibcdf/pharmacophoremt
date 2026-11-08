"""Bounded original-manifest inspection through the independent saved-run CLI."""

import io
import json
import sqlite3
import unittest
from contextlib import closing, redirect_stderr, redirect_stdout
from unittest.mock import patch

import test_public_run_results as fixtures

from pharmacophoremt_results import ScreeningRunError, ScreeningRunView, main


class TestPublicWorkCLI(unittest.TestCase):
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

    def expected_records(self):
        return [
            {"manifest_ordinal": ordinal, **mapping}
            for ordinal, mapping in enumerate(self.fixture.mapping)
        ]

    def page(self, *arguments):
        result = self.fixture.command(self.fixture.path, "--work-items", *arguments)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_pages_preserve_all_original_work_including_unconfirmed_entries(self):
        f = self.fixture
        f.create_partial()
        with f.reopen() as store:
            config = store.configuration
        before = f.directory_bytes()
        received = []
        for offset, next_offset in [(0, 2), (2, 4), (4, None)]:
            page = self.page("--limit", 2, "--offset", offset)
            self.assertEqual(
                page,
                {
                    "format": "pharmacophoremt.screening-work-page@1",
                    "run_id": "run:public",
                    "run_format": "pharmacophoremt.screening-run@1",
                    "work_sha256": config["work_sha256"],
                    "declared_work": 5,
                    "offset": offset,
                    "limit": 2,
                    "next_offset": next_offset,
                    "records": self.expected_records()[offset : offset + 2],
                },
            )
            received.extend(page["records"])
        self.assertEqual(received, self.expected_records())
        self.assertEqual(received[-1]["work_key"], "epsilon")
        self.assertEqual(received[0]["source_key"], received[1]["source_key"])
        self.assertEqual(f.directory_bytes(), before)

    def test_default_page_is_ten_and_never_started_work_is_retained(self):
        f = self.fixture
        f.mapping.extend(
            {"work_key": f"new:{i}", "source_key": "shared", "occurrence_key": "same"}
            for i in range(8)
        )
        f.write_manifest()
        f.create_partial()
        first = self.page()
        self.assertEqual(first["limit"], 10)
        self.assertEqual(first["next_offset"], 10)
        self.assertEqual(first["records"], self.expected_records()[:10])
        last = self.page("--offset", first["next_offset"])
        self.assertEqual(last["records"], self.expected_records()[10:])
        self.assertIsNone(last["next_offset"])
        self.assertEqual(last["declared_work"], 13)

    def test_full_run_unicode_identifiers_and_no_payload_disclosure(self):
        f = self.fixture
        f.mapping[0]["source_key"] = "library:á/β\nsecond line"
        f.mapping[1]["occurrence_key"] = "same occurrence:α"
        f.write_manifest()
        f.create_partial()
        with f.reopen() as store:
            f.publish(store, "epsilon", score=1)
        before = f.directory_bytes()
        page = self.page()
        self.assertEqual(page["records"], self.expected_records())
        self.assertIsNone(page["next_offset"])
        text = json.dumps(page)
        for forbidden in [
            "geometry",
            "native_result",
            "producer",
            "context",
            "ranking_score",
        ]:
            self.assertNotIn(forbidden, text)
        self.assertEqual(f.directory_bytes(), before)

    def test_empty_beyond_end_and_arbitrary_precision_windows(self):
        f = self.fixture
        f.create_partial()
        for offset in [5, 6, 10**30]:
            with self.subTest(offset=offset):
                page = self.page("--offset", offset)
                self.assertEqual(page["records"], [])
                self.assertEqual(page["offset"], offset)
                self.assertIsNone(page["next_offset"])
        page = self.page("--offset", 1, "--limit", 10**30)
        self.assertEqual(page["limit"], 10**30)
        self.assertEqual(page["records"], self.expected_records()[1:])
        self.assertIsNone(page["next_offset"])
        f.path = f.root / "empty.sqlite3"
        f.mapping = []
        f.write_manifest()
        with f.create():
            pass
        page = self.page()
        self.assertEqual(page["declared_work"], 0)
        self.assertEqual(page["records"], [])
        self.assertIsNone(page["next_offset"])

    def test_legacy_requires_explicit_admission_without_rewriting_identities(self):
        f = self.fixture
        f.create_legacy()
        before = f.directory_bytes()
        denied = f.command(f.path, "--work-items")
        self.assertEqual(denied.returncode, 2)
        self.assertEqual(denied.stdout, "")
        page = self.page("--allow-legacy")
        self.assertEqual(page["run_id"], "run:legacy")
        self.assertEqual(page["run_format"], "pharmacophoremt.reference-ledger@1")
        self.assertEqual(page["records"], self.expected_records())
        self.assertEqual(f.directory_bytes(), before)

    def test_argument_conflicts_and_invalid_windows_refuse_before_open(self):
        f = self.fixture
        for arguments in [
            ["--work-items", "--summary"],
            ["--work-items", "--to-jsonl", f.root / "out.jsonl"],
            ["--work-items", "--to-csv", f.root / "out.csv"],
            ["--work-items", "--score-method", fixtures.CRITERION],
            ["--work-items", "--limit", 0],
            ["--work-items", "--limit", -1],
            ["--work-items", "--limit", "1.5"],
            ["--work-items", "--offset", -1],
            ["--work-items", "--offset", "one"],
            ["--summary", "--offset", 0],
            ["--to-jsonl", f.root / "out.jsonl", "--offset", 0],
            ["--score-method", fixtures.CRITERION, "--offset", 0],
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
        self.assertFalse((f.root / "out.jsonl").exists())
        self.assertFalse((f.root / "out.csv").exists())

    def test_selected_window_closes_iterator_without_consuming_later_records(self):
        f = self.fixture
        f.create_partial()
        original = ScreeningRunView.work_items
        consumed, closed = [], []

        def traced(view):
            with closing(original(view)) as source:
                try:
                    for record in source:
                        consumed.append(record["manifest_ordinal"])
                        yield record
                finally:
                    closed.append(True)

        with patch.object(ScreeningRunView, "work_items", traced):
            code, stdout, stderr = self.invoke(
                f.path, "--work-items", "--offset", 1, "--limit", 2
            )
        self.assertEqual(code, 0, stderr)
        self.assertEqual(json.loads(stdout)["records"], self.expected_records()[1:3])
        self.assertEqual(consumed, [0, 1, 2])
        self.assertEqual(closed, [True])

    def test_iteration_failure_closes_source_and_emits_no_success_json(self):
        f = self.fixture
        f.create_partial()
        closed = []

        def failing(view):
            try:
                yield self.expected_records()[0]
                raise ScreeningRunError(
                    operation="read declared work", reason="reader failed"
                )
            finally:
                closed.append(True)

        before = f.directory_bytes()
        with patch.object(ScreeningRunView, "work_items", failing):
            code, stdout, stderr = self.invoke(f.path, "--work-items")
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("reader failed", stderr)
        self.assertEqual(closed, [True])
        self.assertEqual(f.directory_bytes(), before)

    def test_close_failure_emits_no_success_json(self):
        f = self.fixture
        f.create_partial()
        original = ScreeningRunView.close

        def failing(view):
            original(view)
            raise ScreeningRunError(
                operation="close saved evidence", reason="close failed"
            )

        with patch.object(ScreeningRunView, "close", failing):
            code, stdout, stderr = self.invoke(f.path, "--work-items")
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("close failed", stderr)

    def test_full_verification_is_not_bypassed_beyond_the_page(self):
        f = self.fixture
        f.create_partial()
        with closing(sqlite3.connect(f.path)) as connection, connection:
            connection.execute("UPDATE work SET source_key='changed' WHERE ordinal=4")
        before = f.directory_bytes()
        result = f.command(f.path, "--work-items", "--limit", 1)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr)
        self.assertEqual(f.directory_bytes(), before)

    def test_missing_or_invalid_run_has_no_success_json_or_filesystem_mutation(self):
        f = self.fixture
        for raw in [None, b"invalid database"]:
            if raw is not None:
                f.path.write_bytes(raw)
            before = f.directory_bytes()
            result = f.command(f.path, "--work-items")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertTrue(result.stderr)
            self.assertEqual(f.directory_bytes(), before)

    def test_help_explains_work_pages_without_opening_a_run(self):
        result = self.fixture.command("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        for option in ["--work-items", "--offset", "--limit", "--allow-legacy"]:
            self.assertIn(option, result.stdout)
        self.assertFalse(self.fixture.path.exists())
