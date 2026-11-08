"""Exact work detail, confirmed evidence and explicitly pending saved inputs."""

import io
import json
import sqlite3
import threading
import unittest
from contextlib import closing, redirect_stderr, redirect_stdout
from unittest.mock import patch

import test_public_run_results as fixtures

from pharmacophoremt_results import ScreeningRunError, ScreeningRunView, main


class TestPublicWorkItem(unittest.TestCase):
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

    def test_original_outcomes_and_pending_work_remain_distinct(self):
        f = self.fixture
        f.mapping.append(
            dict(work_key="zeta", source_key="source:never", occurrence_key="none")
        )
        f.write_manifest()
        f.create_partial()
        before = f.directory_bytes()
        expected = [
            ("matched", f.outcome("alpha"), 1, 1, 1),
            ("matched", f.outcome("beta"), 1, 1, 1),
            ("not_matched", f.outcome("gamma", score=0, status="not_matched"), 1, 1, 1),
            ("failed", f.outcome("delta", score=None, status="failed"), 1, 1, 1),
            ("pending", None, 1, 1, 0),
            ("pending", None, 0, 0, 0),
        ]
        with ScreeningRunView.open(f.path) as view:
            work_hash = view.configuration["work_sha256"]
            for ordinal, (mapping, values) in enumerate(
                zip(f.mapping, expected, strict=True)
            ):
                status, outcome, started, staged, committed = values
                with self.subTest(key=mapping["work_key"]):
                    self.assertEqual(
                        view.work_item(mapping["work_key"]),
                        {
                            "format": "pharmacophoremt.screening-work-item@1",
                            "run_id": "run:public",
                            "run_format": "pharmacophoremt.screening-run@1",
                            "work_sha256": work_hash,
                            "work_item": {"manifest_ordinal": ordinal, **mapping},
                            "confirmed": outcome is not None,
                            "status": status,
                            "attempts": dict(
                                started=started, staged=staged, committed=committed
                            ),
                            "outcome": outcome,
                        },
                    )
        self.assertEqual(f.directory_bytes(), before)

    def test_saved_failure_keeps_its_original_error_without_emitting_it_again(self):
        f = self.fixture
        outcome = f.outcome("delta", score=None, status="failed")
        outcome["native_result"]["error"] = {
            "stage": "source",
            "code": "ORIGINAL-NATIVE-017",
            "message": "original source unavailable",
        }
        with f.create() as store:
            attempt = store.begin("delta")
            store.stage(attempt, outcome)
            store.publish(attempt)
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            expected = view.work_item("delta")
        self.assertEqual(expected["outcome"], outcome)
        result = f.command(f.path, "--work-key", "delta")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), expected)
        self.assertNotIn("ORIGINAL-NATIVE-017", result.stderr)
        self.assertNotIn("original source unavailable", result.stderr)
        self.assertEqual(f.directory_bytes(), before)

    def test_unpublished_attempts_never_disclose_a_draft_as_an_outcome(self):
        f = self.fixture
        f.create_partial()
        with f.reopen() as store:
            store.begin("epsilon")
            attempt = store.begin("epsilon")
            draft = f.outcome("epsilon")
            draft["native_result"]["private_draft"] = "do not publish this attempt"
            store.stage(attempt, draft)
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            result = view.work_item("epsilon")
        self.assertEqual(result["status"], "pending")
        self.assertIs(result["confirmed"], False)
        self.assertIsNone(result["outcome"])
        self.assertEqual(result["attempts"], dict(started=3, staged=2, committed=0))
        self.assertNotIn("do not publish", json.dumps(result))
        self.assertEqual(f.directory_bytes(), before)

    def test_abandoned_attempt_counts_preserve_only_the_confirmed_evidence(self):
        f = self.fixture
        with f.create() as store:
            store.begin("alpha")
            attempt = store.begin("alpha")
            store.stage(attempt, f.outcome("alpha", score=0.25))
            f.publish(store, "alpha")
        with ScreeningRunView.open(f.path) as view:
            result = view.work_item("alpha")
        self.assertEqual(result["attempts"], dict(started=3, staged=2, committed=1))
        self.assertEqual(result["outcome"], f.outcome("alpha"))
        self.assertIs(result["confirmed"], True)

    def test_detail_is_detached_and_retains_opaque_units_and_attribution(self):
        f = self.fixture
        outcome = f.outcome("alpha")
        outcome["native_result"]["reported_distance"] = {
            "value": 1.25,
            "unit": "nanometer",
        }
        with f.create() as store:
            attempt = store.begin("alpha")
            store.stage(attempt, outcome)
            store.publish(attempt)
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            original = view.work_item("alpha")
            changed = view.work_item("alpha")
            changed["work_item"].clear()
            changed["attempts"].clear()
            changed["outcome"]["native_result"]["reported_distance"]["unit"] = "changed"
            changed["outcome"]["native_result"]["attribution"].clear()
            self.assertEqual(view.work_item("alpha"), original)
        self.assertEqual(original["outcome"], outcome)
        self.assertEqual(f.directory_bytes(), before)

    def test_exact_opaque_keys_roundtrip_in_api_and_fresh_command(self):
        f = self.fixture
        key = " alpha'β?/\n "
        f.mapping[0]["work_key"] = key
        f.write_manifest()
        with f.create() as store:
            f.publish(store, key)
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            expected = view.work_item(key)
            self.assertEqual(expected["work_item"]["work_key"], key)
            for unknown in [key.strip(), "source:repeated", "occurrence:0"]:
                with self.subTest(key=unknown), self.assertRaises(ScreeningRunError):
                    view.work_item(unknown)
        result = f.command(f.path, "--work-key", key)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), expected)
        self.assertEqual(f.directory_bytes(), before)

    def test_definition_owned_key_and_call_shape_contracts(self):
        f = self.fixture
        f.create_partial()
        with ScreeningRunView.open(f.path) as view:
            for key in [None, 0, True, b"alpha", "", " \t", [], {}]:
                with self.subTest(key=key), self.assertRaises(ScreeningRunError):
                    view.work_item(key)
            for extra in [
                {"unknown": 1},
                {"skip_digestion": True},
                {"skip_digestion": False},
            ]:
                with self.subTest(extra=extra), self.assertRaises(TypeError):
                    view.work_item("alpha", **extra)
            with self.assertRaises(TypeError):
                view.work_item()

    def test_closed_and_foreign_thread_reads_keep_structured_storage_errors(self):
        f = self.fixture
        f.create_partial()
        errors = []
        with ScreeningRunView.open(f.path) as view:

            def read_foreign():
                try:
                    view.work_item("alpha")
                except Exception as error:
                    errors.append(error)

            thread = threading.Thread(target=read_foreign)
            thread.start()
            thread.join(timeout=5)
            self.assertFalse(thread.is_alive())
            self.assertEqual(len(errors), 1)
            self.assertIsInstance(errors[0], ScreeningRunError)
            self.assertIsInstance(errors[0].__cause__, sqlite3.ProgrammingError)
        with self.assertRaises(ScreeningRunError):
            view.work_item("alpha")

    def test_legacy_detail_needs_explicit_admission_and_preserves_original_bytes(self):
        f = self.fixture
        f.create_legacy()
        before = f.directory_bytes()
        with self.assertRaises(ScreeningRunError):
            ScreeningRunView.open(f.path)
        with ScreeningRunView.open(f.path, allow_legacy=True) as view:
            expected = view.work_item("alpha")
            self.assertEqual(
                expected["run_format"], "pharmacophoremt.reference-ledger@1"
            )
            self.assertEqual(expected["run_id"], "run:legacy")
            self.assertEqual(expected["outcome"], f.outcome("alpha"))
        denied = f.command(f.path, "--work-key", "alpha")
        self.assertEqual(denied.returncode, 2)
        self.assertEqual(denied.stdout, "")
        allowed = f.command(f.path, "--work-key", "alpha", "--allow-legacy")
        self.assertEqual(allowed.returncode, 0, allowed.stderr)
        self.assertEqual(json.loads(allowed.stdout), expected)
        self.assertEqual(f.directory_bytes(), before)

    def test_fresh_detail_command_matches_api_for_hit_zero_failure_and_pending(self):
        f = self.fixture
        f.create_partial()
        before = f.directory_bytes()
        with ScreeningRunView.open(f.path) as view:
            for key in ["alpha", "gamma", "delta", "epsilon"]:
                expected = view.work_item(key)
                result = f.command(f.path, "--work-key", key)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), expected)
        self.assertEqual(f.directory_bytes(), before)

    def test_detail_conflicts_and_blank_cli_keys_refuse_before_database_io(self):
        f = self.fixture
        for extra in [
            ["--summary"],
            ["--work-items"],
            ["--to-jsonl", f.root / "new.jsonl"],
            ["--to-csv", f.root / "new.csv"],
            ["--score-method", fixtures.CRITERION],
            ["--limit", 0],
            ["--limit", 1],
            ["--offset", 0],
        ]:
            with (
                self.subTest(extra=extra),
                patch.object(ScreeningRunView, "open") as opened,
            ):
                code, stdout, stderr = self.invoke(
                    f.path, "--work-key", "alpha", *extra
                )
                self.assertEqual(code, 2)
                self.assertEqual(stdout, "")
                self.assertTrue(stderr)
                opened.assert_not_called()
        for key in ["", " \t"]:
            with (
                self.subTest(key=key),
                patch.object(ScreeningRunView, "open") as opened,
            ):
                code, stdout, stderr = self.invoke(f.path, "--work-key", key)
                self.assertEqual(code, 2)
                self.assertEqual(stdout, "")
                self.assertTrue(stderr)
                opened.assert_not_called()
        self.assertFalse(f.path.exists())
        self.assertFalse(
            (f.root / "new.jsonl").exists() or (f.root / "new.csv").exists()
        )

    def test_unknown_key_refuses_with_no_success_json_or_database_change(self):
        f = self.fixture
        f.create_partial()
        before = f.directory_bytes()
        result = f.command(f.path, "--work-key", "unknown")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("unknown work key", result.stderr)
        self.assertEqual(f.directory_bytes(), before)

    def test_detail_and_close_failures_leave_stdout_empty(self):
        f = self.fixture
        f.create_partial()
        with patch.object(
            ScreeningRunView,
            "work_item",
            side_effect=ScreeningRunError(
                operation="inspect work", reason="detail unavailable"
            ),
        ):
            code, stdout, stderr = self.invoke(f.path, "--work-key", "alpha")
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("detail unavailable", stderr)
        original = ScreeningRunView.close

        def failing(view):
            original(view)
            raise ScreeningRunError(operation="close evidence", reason="close refused")

        with patch.object(ScreeningRunView, "close", failing):
            code, stdout, stderr = self.invoke(f.path, "--work-key", "alpha")
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("close refused", stderr)

    def test_complete_verification_is_not_bypassed_for_an_unselected_input(self):
        f = self.fixture
        f.create_partial()
        with closing(sqlite3.connect(f.path)) as connection, connection:
            connection.execute("UPDATE work SET source_key='changed' WHERE ordinal=4")
        before = f.directory_bytes()
        result = f.command(f.path, "--work-key", "alpha")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertTrue(result.stderr)
        self.assertEqual(f.directory_bytes(), before)

    def test_missing_and_invalid_databases_leave_no_success_json_or_new_file(self):
        f = self.fixture
        for raw in [None, b"invalid database"]:
            if raw is not None:
                f.path.write_bytes(raw)
            before = f.directory_bytes()
            result = f.command(f.path, "--work-key", "alpha")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertTrue(result.stderr)
            self.assertEqual(f.directory_bytes(), before)

    def test_help_discloses_full_confirmed_evidence_without_opening_a_run(self):
        result = self.fixture.command("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--work-key", result.stdout)
        self.assertIn("geometry", result.stdout)
        self.assertFalse(self.fixture.path.exists())
