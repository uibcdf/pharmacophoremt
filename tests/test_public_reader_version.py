"""Independent reader distribution identity without a saved run or science."""

import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from importlib.metadata import PackageNotFoundError
from unittest.mock import patch

import test_public_run_results as fixtures

from pharmacophoremt_results import ScreeningRunView, main


class TestPublicReaderVersion(unittest.TestCase):
    def invoke(self, *arguments):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                code = main(list(arguments))
            except SystemExit as error:
                code = error.code
        return code, stdout.getvalue(), stderr.getvalue()

    def test_version_needs_no_ledger_and_identifies_requested_distribution(self):
        with (
            patch("importlib.metadata.version", return_value="0.4.0+123.gabcd") as read,
            patch.object(ScreeningRunView, "open") as opened,
        ):
            self.assertEqual(
                self.invoke("--version"),
                (0, "PharmacophoreMT distribution 0.4.0+123.gabcd\n", ""),
            )
        read.assert_called_once_with("pharmacophoremt")
        opened.assert_not_called()

    def test_missing_or_invalid_metadata_refuses_without_success_or_run_io(self):
        for value in (PackageNotFoundError("pharmacophoremt"), None, ""):
            with self.subTest(value=repr(value)):
                options = (
                    {"side_effect": value}
                    if isinstance(value, Exception)
                    else {"return_value": value}
                )
                with (
                    patch("importlib.metadata.version", **options),
                    patch.object(ScreeningRunView, "open") as opened,
                ):
                    code, stdout, stderr = self.invoke("--version")
                self.assertEqual((code, stdout), (2, ""))
                self.assertIn("distribution metadata", stderr)
                self.assertNotIn("Traceback", stderr)
                opened.assert_not_called()

    def test_help_lists_option_without_distribution_lookup(self):
        with patch("importlib.metadata.version") as read:
            code, stdout, stderr = self.invoke("--help")
        self.assertEqual((code, stderr), (0, ""))
        self.assertIn("--version", stdout)
        read.assert_not_called()

    def test_ordinary_summary_does_not_query_distribution_metadata(self):
        f = fixtures.TestPublicRunResults()
        f.setUp()
        self.addCleanup(f.doCleanups)
        f.create_partial()
        with patch("importlib.metadata.version") as read:
            code, stdout, stderr = self.invoke(str(f.path), "--summary")
        self.assertEqual((code, stderr), (0, ""))
        self.assertIn('"declared_work": 5', stdout)
        read.assert_not_called()

    def test_fresh_version_agrees_with_actual_distribution_without_science(self):
        f = fixtures.TestPublicRunResults()
        f.setUp()
        self.addCleanup(f.doCleanups)
        result = f.fresh(
            """
from importlib.metadata import version
from contextlib import redirect_stdout
import io
from pharmacophoremt_results import main
expected = version('pharmacophoremt')
output = io.StringIO()
with redirect_stdout(output):
    try:
        main(['--version'])
    except SystemExit as error:
        assert error.code == 0
assert output.getvalue() == 'PharmacophoreMT distribution ' + expected + '\\n'
assert blocked.isdisjoint(sys.modules)
"""
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
