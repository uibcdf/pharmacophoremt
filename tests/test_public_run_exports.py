"""Complete saved exports, source evidence and filesystem failure semantics."""

import csv
import hashlib
import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

import test_public_run_results as fixtures

from pharmacophoremt_results import (
    ScreeningRunError,
    ScreeningRunView,
    _exports,
    canonical_json,
)


class TestPublicRunExports(unittest.TestCase):
    def setUp(self):
        # Reuse the original writer/legacy fixtures without collecting their tests.
        self.fixture = fixtures.TestPublicRunResults()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root
        self.path = self.fixture.path

    def assert_receipt(self, receipt, path, configuration, *, count, pending):
        raw = path.read_bytes()
        self.assertEqual(receipt["format"], "pharmacophoremt.screening-export@1")
        self.assertEqual(receipt["path"], str(path.absolute()))
        self.assertEqual(receipt["encoding"], "utf-8")
        self.assertEqual(receipt["bytes"], len(raw))
        self.assertEqual(receipt["sha256"], hashlib.sha256(raw).hexdigest())
        self.assertEqual(receipt["configuration"], configuration)
        self.assertEqual(
            receipt["configuration_sha256"],
            hashlib.sha256(canonical_json(configuration).encode()).hexdigest(),
        )
        self.assertEqual(receipt["exported_records"], count)
        self.assertEqual(receipt["pending_work"], pending)
        self.assertIs(receipt["published"], True)
        self.assertEqual(json.loads(canonical_json(receipt)), receipt)

    def test_complete_jsonl_and_csv_preserve_original_rows_and_coverage(self):
        self.fixture.create_partial()
        before = self.path.read_bytes()
        with ScreeningRunView.open(self.path) as view:
            original = list(view.results())
            configuration = view.configuration
            jsonl = self.root / "complete.jsonl"
            table = self.root / "complete.csv"
            native_receipt = view.to_jsonl(jsonl)
            scalar_receipt = view.to_csv(table)
            self.assertEqual(
                [json.loads(line) for line in jsonl.read_text().splitlines()], original
            )
            self.assertEqual(
                jsonl.read_text(),
                "".join(canonical_json(row) + "\n" for row in original),
            )
            with table.open(newline="") as source:
                reader = csv.DictReader(source)
                self.assertEqual(
                    reader.fieldnames,
                    [
                        "work_key",
                        "source_key",
                        "occurrence_key",
                        "status",
                        "ranking_score",
                        "score_method",
                    ],
                )
                rows = list(reader)
            self.assertEqual(
                [row["work_key"] for row in rows], ["alpha", "beta", "gamma", "delta"]
            )
            self.assertEqual(
                [row["ranking_score"] for row in rows], ["0.75", "0.75", "0", ""]
            )
            self.assertEqual(
                [row["status"] for row in rows],
                ["matched", "matched", "not_matched", "failed"],
            )
            self.assertEqual(rows[0]["source_key"], rows[1]["source_key"])
            for receipt, path, file_format in (
                (native_receipt, jsonl, "jsonl"),
                (scalar_receipt, table, "csv"),
            ):
                self.assertEqual(receipt["file_format"], file_format)
                self.assert_receipt(receipt, path, configuration, count=4, pending=1)
                receipt["configuration"]["context"]["producer"]["version"] = "caller"
                self.assertEqual(view.configuration, configuration)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.root.glob(".phmt-export-*")), [])

    def test_opaque_ids_and_native_units_are_not_interpreted_or_rewritten(self):
        f = self.fixture
        f.mapping = [
            {
                "work_key": 'κλειδί,"\n1',
                "source_key": '=literal,"\nα',
                "occurrence_key": "répété\n2",
            }
        ]
        f.write_manifest()
        outcome = f.outcome(f.mapping[0]["work_key"], score=0, status="not_matched")
        outcome["native_result"]["distance"] = {"value": 0.35, "unit": "nanometer"}
        with f.create() as store:
            attempt = store.begin(outcome["work_key"])
            store.stage(attempt, outcome)
            store.publish(attempt)
        with ScreeningRunView.open(self.path) as view:
            view.to_jsonl(self.root / "native.jsonl")
            view.to_csv(self.root / "scalar.csv")
        self.assertEqual(json.loads((self.root / "native.jsonl").read_text()), outcome)
        with (self.root / "scalar.csv").open(newline="") as stream:
            (row,) = csv.DictReader(stream)
        self.assertEqual({key: row[key] for key in f.mapping[0]}, f.mapping[0])
        self.assertEqual(row["ranking_score"], "0")

    def test_empty_run_writes_header_only_csv_and_empty_jsonl(self):
        f = self.fixture
        f.mapping = []
        f.write_manifest()
        with f.create():
            pass
        with ScreeningRunView.open(self.path) as view:
            for file_format in ("jsonl", "csv"):
                path = self.root / ("empty." + file_format)
                receipt = getattr(view, "to_" + file_format)(path)
                self.assert_receipt(
                    receipt, path, view.configuration, count=0, pending=0
                )
        self.assertEqual((self.root / "empty.jsonl").read_bytes(), b"")
        self.assertEqual(
            (self.root / "empty.csv").read_text(),
            "work_key,source_key,occurrence_key,status,ranking_score,score_method\n",
        )

    def test_legacy_export_preserves_fractional_score_and_original_format(self):
        f = self.fixture
        f.create_legacy()
        before = f.directory_bytes()
        with self.assertRaises(ScreeningRunError):
            ScreeningRunView.open(self.path)
        with ScreeningRunView.open(self.path, allow_legacy=True) as view:
            path = self.root / "legacy.jsonl"
            receipt = view.to_jsonl(path)
            self.assertEqual(json.loads(path.read_text()), f.outcome("alpha"))
            self.assertEqual(
                receipt["configuration"]["format"], "pharmacophoremt.reference-ledger@1"
            )
            self.assertEqual(receipt["pending_work"], 4)
        self.assertTrue(
            all((self.root / name).read_bytes() == raw for name, raw in before.items())
        )

    def test_existing_files_directories_and_symlinks_are_never_touched(self):
        self.fixture.create_partial()
        existing = self.root / "existing"
        existing.write_bytes(b"caller-owned")
        directory = self.root / "directory"
        directory.mkdir()
        symlink = self.root / "symlink"
        symlink.symlink_to(existing)
        broken = self.root / "broken"
        broken.symlink_to(self.root / "absent")
        with (
            ScreeningRunView.open(self.path) as view,
            patch.object(view, "results") as read,
        ):
            for path in (existing, directory, symlink, broken, self.path):
                for method in (view.to_jsonl, view.to_csv):
                    with self.subTest(path=path, method=method.__name__):
                        with self.assertRaises(ScreeningRunError) as caught:
                            method(path)
                        self.assertIsInstance(
                            caught.exception.__cause__, FileExistsError
                        )
            read.assert_not_called()
        self.assertEqual(existing.read_bytes(), b"caller-owned")
        self.assertTrue(symlink.is_symlink() and broken.is_symlink())
        self.assertEqual(list(self.root.glob(".phmt-export-*")), [])

    def test_concurrent_destination_wins_without_replacement(self):
        self.fixture.create_partial()
        path = self.root / "concurrent.jsonl"
        real_link = os.link

        def competing_link(source, destination):
            Path(destination).write_bytes(b"another owner")
            real_link(source, destination)

        with (
            ScreeningRunView.open(self.path) as view,
            patch.object(_exports.os, "link", side_effect=competing_link),
            self.assertRaises(ScreeningRunError) as caught,
        ):
            view.to_jsonl(path)
        self.assertIsInstance(caught.exception.__cause__, FileExistsError)
        self.assertEqual(path.read_bytes(), b"another owner")
        self.assertEqual(list(self.root.glob(".phmt-export-*")), [])

    def test_closed_view_and_invalid_options_have_no_filesystem_effects(self):
        self.fixture.create_partial()
        before = self.fixture.directory_bytes()
        with ScreeningRunView.open(self.path) as view:
            for method in (view.to_jsonl, view.to_csv):
                for extra in (
                    {"typo": True},
                    {"skip_digestion": True},
                    {"skip_digestion": False},
                ):
                    with self.assertRaises(TypeError):
                        method(self.root / "new", **extra)
                for bad_path in (True, None, b"bytes", ""):
                    with self.assertRaises(ScreeningRunError):
                        method(bad_path)
        for method in (view.to_jsonl, view.to_csv):
            with self.assertRaises(ScreeningRunError):
                method(self.root / "new")
        self.assertEqual(self.fixture.directory_bytes(), before)

    def test_missing_parent_is_refused_without_creating_directories(self):
        self.fixture.create_partial()
        with (
            ScreeningRunView.open(self.path) as view,
            self.assertRaises(ScreeningRunError),
        ):
            view.to_csv(self.root / "absent" / "new.csv")
        self.assertFalse((self.root / "absent").exists())

    def test_midstream_failure_closes_iterator_and_leaves_no_new_destination(self):
        self.fixture.create_partial()
        before = self.fixture.directory_bytes()
        closed = []
        error = ValueError("retained read failure")

        def failing_rows():
            try:
                yield self.fixture.outcome("alpha")
                raise error
            finally:
                closed.append(True)

        with (
            ScreeningRunView.open(self.path) as view,
            patch.object(view, "results", side_effect=failing_rows),
            self.assertRaises(ScreeningRunError) as caught,
        ):
            view.to_jsonl(self.root / "new.jsonl")
        self.assertIs(caught.exception.__cause__, error)
        self.assertEqual(closed, [True])
        self.assertEqual(self.fixture.directory_bytes(), before)

    def test_write_hash_and_link_failures_leave_no_published_file(self):
        self.fixture.create_partial()
        before = self.fixture.directory_bytes()
        error = OSError("injected disk or filesystem refusal")

        def incomplete_write(view, output, file_format):
            output.write("incomplete staging bytes")
            raise error

        with ScreeningRunView.open(self.path) as view:
            for target, replacement in (
                ("_write", incomplete_write),
                ("_identity", error),
                ("os.link", error),
            ):
                with (
                    patch(
                        "pharmacophoremt_results._exports." + target,
                        side_effect=replacement,
                    ),
                    self.assertRaises(ScreeningRunError) as caught,
                ):
                    view.to_csv(self.root / "new.csv")
                self.assertIs(caught.exception.__cause__, error)
                self.assertEqual(caught.exception.code, "PHMT-E201")
                self.assertEqual(self.fixture.directory_bytes(), before)

    def test_interruption_preserves_interrupt_and_removes_staging_file(self):
        self.fixture.create_partial()
        before = self.fixture.directory_bytes()
        with (
            ScreeningRunView.open(self.path) as view,
            patch.object(_exports, "_write", side_effect=KeyboardInterrupt),
            self.assertRaises(KeyboardInterrupt),
        ):
            view.to_jsonl(self.root / "interrupted.jsonl")
        self.assertEqual(self.fixture.directory_bytes(), before)

    def test_failed_stream_open_closes_descriptor_and_removes_staging_file(self):
        self.fixture.create_partial()
        before = self.fixture.directory_bytes()
        descriptor = []
        error = OSError("stream open refused")

        def refused_open(fd, *args, **kwargs):
            descriptor.append(fd)
            raise error

        with (
            ScreeningRunView.open(self.path) as view,
            patch.object(_exports.os, "fdopen", side_effect=refused_open),
            self.assertRaises(ScreeningRunError) as caught,
        ):
            view.to_jsonl(self.root / "new.jsonl")
        self.assertIs(caught.exception.__cause__, error)
        self.assertEqual(len(descriptor), 1)
        with self.assertRaises(OSError):
            os.fstat(descriptor[0])
        self.assertEqual(self.fixture.directory_bytes(), before)

    def test_failed_cleanup_before_publication_retains_primary_cause_and_path(self):
        self.fixture.create_partial()
        error = OSError("primary write failure")
        real_unlink = Path.unlink

        def failed_unlink(path, *args, **kwargs):
            if path.name.startswith(".phmt-export-"):
                raise PermissionError("cleanup denied")
            return real_unlink(path, *args, **kwargs)

        with (
            ScreeningRunView.open(self.path) as view,
            patch.object(_exports, "_write", side_effect=error),
            patch.object(Path, "unlink", failed_unlink),
            self.assertRaises(ScreeningRunError) as caught,
        ):
            view.to_jsonl(self.root / "new.jsonl")
        self.assertIs(caught.exception.__cause__, error)
        self.assertFalse((self.root / "new.jsonl").exists())
        (temporary,) = self.root.glob(".phmt-export-*")
        self.assertIn(str(temporary), error.__notes__[0])
        temporary.unlink()

    def test_cleanup_after_publication_reports_complete_destination_and_receipt(self):
        self.fixture.create_partial()
        error = PermissionError("cleanup denied")
        with (
            ScreeningRunView.open(self.path) as view,
            patch.object(Path, "unlink", side_effect=error),
            self.assertRaises(ScreeningRunError) as caught,
        ):
            view.to_jsonl(self.root / "new.jsonl")
        failure = caught.exception
        self.assertIs(failure.__cause__, error)
        self.assertIs(failure.extra["published"], True)
        receipt = failure.extra["receipt"]
        with ScreeningRunView.open(self.path) as view:
            self.assert_receipt(
                receipt, self.root / "new.jsonl", view.configuration, count=4, pending=1
            )
            self.assertEqual(
                [
                    json.loads(line)
                    for line in (self.root / "new.jsonl").read_text().splitlines()
                ],
                list(view.results()),
            )
        temporary = Path(failure.extra["temporary_path"])
        self.assertEqual(temporary.read_bytes(), (self.root / "new.jsonl").read_bytes())
        temporary.unlink()

    def test_fresh_reader_exports_without_original_manifest_or_scientific_imports(self):
        self.fixture.create_partial()
        self.fixture.manifest.unlink()
        result = self.fixture.fresh(
            """
import json
from pathlib import Path
from pharmacophoremt_results import ScreeningRunView
with ScreeningRunView.open(sys.argv[1]) as view:
    for file_format in ['csv', 'jsonl']:
        receipt = getattr(view, 'to_' + file_format)(Path(sys.argv[2]) / ('fresh.' + file_format))
        assert receipt['exported_records'] == 4 and receipt['pending_work'] == 1
        assert receipt['configuration']['context']['producer']['version'] == 'original-producer-0.1'
assert not any(name.split('.')[0] in blocked for name in sys.modules)
""",
            self.path,
            self.root,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
