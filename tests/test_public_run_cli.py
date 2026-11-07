"""Command receiving for complete saved exports and retained ranked inspection."""

import csv
import hashlib
import io
import json
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import test_public_run_results as fixtures

from pharmacophoremt_results import ScreeningRunError, ScreeningRunView, _exports, main


class TestPublicRunCLI(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.TestPublicRunResults()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root

    def invoke(self, *arguments):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                code = main(list(map(str, arguments)))
            except SystemExit as exit_error:
                code = exit_error.code
        return code, stdout.getvalue(), stderr.getvalue()

    def check_receipt(self, result, output, count, pending):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["format"], "pharmacophoremt.screening-export@1")
        self.assertEqual(receipt["exported_records"], count)
        self.assertEqual(receipt["pending_work"], pending)
        self.assertIs(receipt["published"], True)
        raw = output.read_bytes()
        self.assertEqual(receipt["bytes"], len(raw))
        self.assertEqual(receipt["sha256"], hashlib.sha256(raw).hexdigest())
        with ScreeningRunView.open(self.fixture.path, allow_legacy=True) as view:
            self.assertEqual(receipt["configuration"], view.configuration)
        return receipt

    def test_jsonl_exports_all_confirmations_in_manifest_order_without_a_criterion(
        self,
    ):
        f = self.fixture
        f.create_partial()
        with f.reopen() as store:
            f.publish(store, "epsilon", score=1)
        before = f.path.read_bytes()
        output = self.root / "all original.jsonl"
        result = f.command(f.path, "--to-jsonl", output)
        receipt = self.check_receipt(result, output, 5, 0)
        self.assertEqual(receipt["file_format"], "jsonl")
        with ScreeningRunView.open(f.path) as view:
            self.assertEqual(
                [json.loads(line) for line in output.read_text().splitlines()],
                list(view.results()),
            )
        self.assertEqual(
            [json.loads(line)["work_key"] for line in output.read_text().splitlines()],
            ["alpha", "beta", "gamma", "delta", "epsilon"],
        )
        self.assertNotIn("private native geometry", result.stdout)
        self.assertEqual(f.path.read_bytes(), before)

    def test_csv_exports_partial_zero_negatives_and_failures_without_ranking(self):
        f = self.fixture
        f.create_partial()
        before = f.path.read_bytes()
        output = self.root / "all confirmed.csv"
        result = f.command(f.path, "--to-csv", output)
        receipt = self.check_receipt(result, output, 4, 1)
        self.assertEqual(receipt["file_format"], "csv")
        with output.open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(
            [row["ranking_score"] for row in rows], ["0.75", "0.75", "0", ""]
        )
        self.assertEqual(
            [row["status"] for row in rows],
            ["matched", "matched", "not_matched", "failed"],
        )
        self.assertEqual(rows[0]["source_key"], rows[1]["source_key"])
        self.assertEqual(f.path.read_bytes(), before)

    def test_empty_exports_keep_header_and_explicit_zero_counts(self):
        f = self.fixture
        f.mapping = []
        f.write_manifest()
        with f.create():
            pass
        for file_format in ["jsonl", "csv"]:
            output = self.root / ("empty." + file_format)
            self.check_receipt(
                f.command(f.path, "--to-" + file_format, output), output, 0, 0
            )
        self.assertEqual((self.root / "empty.jsonl").read_bytes(), b"")
        self.assertEqual(
            (self.root / "empty.csv").read_text(),
            "work_key,source_key,occurrence_key,status,ranking_score,score_method\n",
        )

    def test_legacy_exports_require_explicit_admission_and_keep_original_values(self):
        f = self.fixture
        f.create_legacy()
        before = f.path.read_bytes()
        for file_format in ["jsonl", "csv"]:
            output = self.root / ("legacy." + file_format)
            denied = f.command(f.path, "--to-" + file_format, output)
            self.assertEqual(denied.returncode, 2)
            self.assertEqual(denied.stdout, "")
            self.assertFalse(output.exists())
            allowed = f.command(f.path, "--to-" + file_format, output, "--allow-legacy")
            receipt = self.check_receipt(allowed, output, 1, 4)
            self.assertEqual(
                receipt["configuration"]["format"], "pharmacophoremt.reference-ledger@1"
            )
        self.assertEqual(
            json.loads((self.root / "legacy.jsonl").read_text()), f.outcome("alpha")
        )
        self.assertEqual(f.path.read_bytes(), before)

    def test_conflicting_options_are_refused_before_database_or_output_io(self):
        f = self.fixture
        output = self.root / "new.jsonl"
        for extra in [
            ["--to-jsonl", output, "--to-csv", self.root / "new.csv"],
            ["--to-jsonl", output, "--score-method", fixtures.CRITERION],
            ["--to-csv", output, "--limit", "0"],
            ["--to-jsonl", output, "--limit", "-1"],
            ["--unknown-option", "anything"],
            [],
        ]:
            with (
                self.subTest(extra=extra),
                patch.object(ScreeningRunView, "open") as opened,
            ):
                code, stdout, stderr = self.invoke(f.path, *extra)
                self.assertEqual(code, 2)
                self.assertEqual(stdout, "")
                self.assertTrue(stderr)
                opened.assert_not_called()
        self.assertFalse(
            f.path.exists() or output.exists() or (self.root / "new.csv").exists()
        )

    def test_help_explains_export_and_inspection_without_opening_a_run(self):
        f = self.fixture
        result = f.command("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        for option in [
            "--to-csv",
            "--to-jsonl",
            "--score-method",
            "--limit",
            "--allow-legacy",
        ]:
            self.assertIn(option, result.stdout)
        self.assertIn("without rerunning science", " ".join(result.stdout.split()))
        self.assertFalse(f.path.exists())

    def test_existing_ranked_inspection_defaults_and_literal_export_filename_remain_valid(
        self,
    ):
        f = self.fixture
        f.path = self.root / "export"
        f.create_partial()
        before = f.path.read_bytes()
        result = f.command(f.path, "--score-method", fixtures.CRITERION)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        received = json.loads(result.stdout)
        with ScreeningRunView.open(f.path) as view:
            expected = view.top_results(score_method=fixtures.CRITERION, limit=10)
        self.assertEqual(received["summary"], expected["summary"])
        self.assertEqual(
            [row["work_key"] for row in received["records"]], ["alpha", "beta", "gamma"]
        )
        self.assertNotIn("native_result", received["records"][0])
        self.assertEqual(f.path.read_bytes(), before)

    def test_missing_and_corrupt_databases_leave_no_success_json_or_destination(self):
        f = self.fixture
        for contents in [None, b"not a screening database"]:
            if contents is not None:
                f.path.write_bytes(contents)
            for file_format in ["jsonl", "csv"]:
                output = self.root / ("new." + file_format)
                result = f.command(f.path, "--to-" + file_format, output)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr)
                self.assertFalse(output.exists())
            if contents is None:
                self.assertFalse(f.path.exists())
            else:
                self.assertEqual(f.path.read_bytes(), contents)

    def test_existing_outputs_and_the_source_database_are_never_overwritten(self):
        f = self.fixture
        f.create_partial()
        output = self.root / "caller-owned"
        output.write_bytes(b"original output")
        before = f.directory_bytes()
        for path in [output, f.path]:
            for file_format in ["csv", "jsonl"]:
                result = f.command(f.path, "--to-" + file_format, path)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
        self.assertEqual(f.directory_bytes(), before)

    def test_prepublication_failure_has_no_success_response_or_partial_output(self):
        f = self.fixture
        f.create_partial()
        before = f.directory_bytes()
        with patch.object(
            _exports.os, "link", side_effect=OSError("publication refused")
        ):
            code, stdout, stderr = self.invoke(
                f.path, "--to-csv", self.root / "new.csv"
            )
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("publication refused", stderr)
        self.assertNotIn('"published": true', stderr)
        self.assertEqual(f.directory_bytes(), before)

    def test_postpublication_cleanup_failure_retains_coded_receipt_on_stderr(self):
        f = self.fixture
        f.create_partial()
        output = self.root / "complete.jsonl"
        with patch.object(
            Path, "unlink", side_effect=PermissionError("cleanup denied")
        ):
            code, stdout, stderr = self.invoke(f.path, "--to-jsonl", output)
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        (detail,) = [
            json.loads(line) for line in stderr.splitlines() if line.startswith("{")
        ]
        self.assertEqual(detail["code"], "PHMT-E201")
        self.assertIs(detail["published"], True)
        self.assertEqual(
            detail["receipt"]["sha256"], hashlib.sha256(output.read_bytes()).hexdigest()
        )
        self.assertEqual(detail["receipt"]["exported_records"], 4)
        temporary = Path(detail["temporary_path"])
        self.assertEqual(temporary.read_bytes(), output.read_bytes())
        temporary.unlink()
        with ScreeningRunView.open(f.path) as view:
            self.assertEqual(
                [json.loads(line) for line in output.read_text().splitlines()],
                list(view.results()),
            )

    def test_close_failure_after_successful_export_retains_the_completed_receipt(self):
        f = self.fixture
        f.create_partial()
        output = self.root / "complete.csv"
        real_close = ScreeningRunView.close

        def failed_close(view):
            real_close(view)
            raise ScreeningRunError(
                operation="close saved evidence", reason="close refused"
            )

        with patch.object(ScreeningRunView, "close", failed_close):
            code, stdout, stderr = self.invoke(f.path, "--to-csv", output)
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        (detail,) = [
            json.loads(line) for line in stderr.splitlines() if line.startswith("{")
        ]
        self.assertIs(detail["published"], True)
        self.assertEqual(detail["code"], "PHMT-E201")
        self.assertIsNone(detail["temporary_path"])
        self.assertEqual(
            detail["receipt"]["sha256"], hashlib.sha256(output.read_bytes()).hexdigest()
        )
        self.assertEqual(list(self.root.glob(".phmt-export-*")), [])


if __name__ == "__main__":
    unittest.main()
