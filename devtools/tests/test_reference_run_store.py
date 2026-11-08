"""Offline transaction/replay controls for the unshipped reference run store."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
STORE = ROOT / "phmt_test_support/reference_run_store.py"
# Administrative discovery must not register the scientific support namespace.
_spec = importlib.util.spec_from_file_location("reference_store_guard", STORE)
_store = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_store)
ReferenceLedger = _store.ReferenceLedger


class TestReferenceRunStore(unittest.TestCase):
    def test_corruption_fixtures_close_every_owned_sqlite_connection(self):
        from devtools.tests.test_reference_run_inspection import (
            TestReferenceRunInspection,
        )

        class ObservedConnection(sqlite3.Connection):
            explicitly_closed = False

            def close(self):
                super().close()
                self.explicitly_closed = True

        original_connect = sqlite3.connect
        connections = []

        def connect(*args, **kwargs):
            connection = original_connect(*args, **kwargs, factory=ObservedConnection)
            connections.append(connection)
            return connection

        fixtures = [
            TestReferenceRunStore(
                "test_corrupt_staged_or_confirmed_payload_is_refused_on_open"
            ),
            TestReferenceRunStore(
                "test_changed_work_mapping_or_committing_attempt_is_refused"
            ),
            TestReferenceRunStore(
                "test_query_metadata_checksums_and_schema_identity_are_verified"
            ),
            TestReferenceRunInspection(
                "test_corruption_outside_top_results_and_in_unpublished_attempts_is_refused"
            ),
            TestReferenceRunInspection(
                "test_query_checksum_is_checked_without_external_query_artifact"
            ),
        ]
        try:
            with patch.object(sqlite3, "connect", connect):
                result = unittest.TestResult()
                unittest.TestSuite(fixtures).run(result)
            self.assertTrue(result.wasSuccessful(), result.errors + result.failures)
            self.assertTrue(connections)
            self.assertTrue(
                all(connection.explicitly_closed for connection in connections),
                "corruption fixtures must close owned handles after commit/rollback",
            )
        finally:
            for connection in connections:
                if not connection.explicitly_closed:
                    connection.close()

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="phmt-reference-ledger-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.path = self.root / "run.sqlite3"
        self.manifest = self.root / "work.jsonl"
        self.mapping = [
            {
                "work_key": "alpha",
                "source_key": "source:shared",
                "occurrence_key": "row:0",
            },
            {
                "work_key": "beta",
                "source_key": "source:shared",
                "occurrence_key": "row:1",
            },
        ]
        self.write_manifest(self.mapping)
        self.query = b'{"schema":"controlled-query-bytes"}\n'
        self.context = {
            "execution": {"score_method": "checked_pose_coverage"},
            "numerical": {"version": "controlled-test"},
        }

    def write_manifest(self, records):
        self.manifest.write_text(
            "".join(json.dumps(record) + "\n" for record in records),
            encoding="utf-8",
        )

    def create(self, *, path=None, **overrides):
        options = {
            "run_id": "run:original",
            "query_bytes": self.query,
            "context": self.context,
            "manifest_path": self.manifest,
        }
        options.update(overrides)
        return ReferenceLedger.create(path or self.path, **options)

    def reopen(self, *, path=None, **overrides):
        options = {
            "query_bytes": self.query,
            "context": self.context,
            "manifest_path": self.manifest,
        }
        options.update(overrides)
        return ReferenceLedger.open(path or self.path, **options)

    def outcome(self, key="alpha", *, status="matched"):
        mapping = next(record for record in self.mapping if record["work_key"] == key)
        score = None if status == "failed" else float(status == "matched")
        return {
            **mapping,
            "native_result": {"pose_id": key, "status": status, "fit_value": score},
            "ranking_score": score,
            "score_method": "checked_pose_coverage@1",
        }

    def publish(self, ledger, key="alpha", *, status="matched"):
        attempt = ledger.begin(key)
        ledger.stage(attempt, self.outcome(key, status=status))
        self.assertTrue(ledger.publish(attempt))
        return attempt

    def test_start_and_stage_remain_unpublished_across_reopen(self):
        with self.create() as ledger:
            original_attempt = ledger.begin("alpha")
            self.assertIsNone(ledger.committed("alpha"))
            ledger.stage(original_attempt, self.outcome())
            self.assertIsNone(ledger.committed("alpha"))
            self.assertEqual(list(ledger.results()), [])
        with self.reopen() as ledger:
            attempts = list(ledger.attempts("alpha"))
            self.assertEqual(len(attempts), 1)
            self.assertEqual(attempts[0]["attempt_id"], original_attempt)
            self.assertTrue(attempts[0]["staged"])
            self.assertFalse(attempts[0]["committed"])
            recovered_attempt = self.publish(ledger)
            self.assertNotEqual(recovered_attempt, original_attempt)
            self.assertEqual(list(ledger.results()), [self.outcome()])
            self.assertEqual(
                [a["committed"] for a in ledger.attempts("alpha")], [False, True]
            )

    def test_terminal_failure_stays_authoritative_and_retry_uses_linked_run(self):
        with self.create() as ledger:
            self.publish(ledger, status="failed")
            with self.assertRaises(ValueError):
                ledger.begin("alpha")
            self.assertIsNone(ledger.committed("alpha")["ranking_score"])
        retry_path = self.root / "retry.sqlite3"
        with self.create(
            path=retry_path, run_id="run:retry", parent_run_id="run:original"
        ) as ledger:
            self.assertEqual(ledger.parent_run_id, "run:original")
            self.assertEqual(ledger.expected(0), self.mapping[0])
            self.publish(ledger)
            self.assertEqual(ledger.committed("alpha")["ranking_score"], 1)
        with self.reopen() as ledger:
            self.assertEqual(ledger.run_id, "run:original")
            self.assertEqual(ledger.committed("alpha"), self.outcome(status="failed"))

    def test_identical_publication_is_idempotent_and_conflicts_preserve_original(self):
        with self.create() as ledger:
            first, repeated, conflict = [ledger.begin("alpha") for _ in range(3)]
            ledger.stage(first, self.outcome())
            ledger.stage(repeated, deepcopy(self.outcome()))
            ledger.stage(conflict, self.outcome(status="not_matched"))
            self.assertTrue(ledger.publish(first))
            self.assertFalse(ledger.publish(first))
            self.assertFalse(ledger.publish(repeated))
            with self.assertRaises(ValueError):
                ledger.publish(conflict)
            self.assertEqual(ledger.committed("alpha"), self.outcome())
            self.assertEqual(
                [a["attempt_id"] for a in ledger.attempts("alpha") if a["committed"]],
                [first],
            )

    def test_replay_follows_manifest_order_instead_of_commit_order(self):
        with self.create() as ledger:
            self.publish(ledger, "beta", status="not_matched")
            self.publish(ledger, "alpha")
            self.assertEqual(ledger.expected(0), self.mapping[0])
            self.assertEqual(ledger.expected(1), self.mapping[1])
            self.assertIsNone(ledger.expected(2))
            self.assertEqual(
                [record["work_key"] for record in ledger.results()], ["alpha", "beta"]
            )

    def test_existing_run_file_is_never_overwritten(self):
        with self.create() as ledger:
            self.publish(ledger)
        original = self.path.read_bytes()
        with self.assertRaises(FileExistsError):
            self.create()
        self.assertEqual(self.path.read_bytes(), original)
        with self.reopen() as ledger:
            self.assertEqual(ledger.committed("alpha"), self.outcome())

    def test_missing_run_is_not_created_by_resume(self):
        with self.assertRaises((FileNotFoundError, sqlite3.DatabaseError)):
            with self.reopen():
                pass
        self.assertFalse(self.path.exists())

    def test_unknown_work_or_unstaged_attempt_cannot_publish(self):
        with self.create() as ledger:
            with self.assertRaises((ValueError, sqlite3.DatabaseError)):
                ledger.begin("unknown")
            attempt = ledger.begin("alpha")
            with self.assertRaises(ValueError):
                ledger.publish(attempt)
            self.assertEqual(list(ledger.results()), [])

    def test_invalid_outcome_mapping_and_failed_scores_are_refused(self):
        changes = [
            {"work_key": "beta"},
            {"source_key": "source:substitution"},
            {"occurrence_key": "row:substitution"},
            {
                "native_result": {
                    "pose_id": "wrong",
                    "status": "matched",
                    "fit_value": 1,
                }
            },
            {
                "native_result": {
                    "pose_id": "alpha",
                    "status": "unknown",
                    "fit_value": 1,
                }
            },
            {
                "native_result": {
                    "pose_id": "alpha",
                    "status": "failed",
                    "fit_value": None,
                }
            },
            {"ranking_score": float("nan")},
            {"ranking_score": None},
            {"score_method": "seeded_hit@1"},
            {"extra": "unrecognized envelope field"},
        ]
        with self.create() as ledger:
            for change in changes:
                with self.subTest(change=change):
                    outcome = self.outcome()
                    outcome.update(change)
                    attempt = ledger.begin("alpha")
                    with self.assertRaises((ValueError, TypeError)):
                        ledger.stage(attempt, outcome)
            self.assertEqual(list(ledger.results()), [])

    def test_duplicate_unknown_or_malformed_manifest_keys_are_refused(self):
        records = [
            [self.mapping[0], self.mapping[0]],
            [{**self.mapping[0], "work_key": ""}],
            [{**self.mapping[0], "source_key": 4}],
            [{**self.mapping[0], "occurrence_key": None}],
            [{**self.mapping[0], "extra": "not a mapping field"}],
        ]
        for index, rows in enumerate(records):
            with self.subTest(rows=rows):
                self.write_manifest(rows)
                with self.assertRaises((ValueError, sqlite3.DatabaseError)):
                    with self.create(path=self.root / f"invalid-{index}.sqlite3"):
                        pass
        self.manifest.write_text(
            '{"work_key":"first","work_key":"last",'
            '"source_key":"source","occurrence_key":"row"}\n',
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            with self.create(path=self.root / "duplicate-json-field.sqlite3"):
                pass

    def test_manifest_line_bound_is_checked_before_unbounded_decoding(self):
        self.manifest.write_text(
            json.dumps({**self.mapping[0], "source_key": "x" * (70 * 1024)}) + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(ValueError):
            with self.create():
                pass

    def test_canonical_json_refuses_nonfinite_or_nonjson_context(self):
        invalid = [
            {"number": float("nan")},
            {"number": float("inf")},
            {"number": -float("inf")},
            {1: "coerced key"},
            {"value": object()},
        ]
        for value in invalid:
            with self.subTest(value=value):
                with self.assertRaises((ValueError, TypeError)):
                    _store.canonical_json(value)
        self.assertEqual(
            _store.canonical_json({"b": 1, "a": [True, None]}),
            _store.canonical_json({"a": [True, None], "b": 1}),
        )

    def test_changed_query_context_or_manifest_rejects_resume(self):
        with self.create() as ledger:
            self.publish(ledger)
        changed_context = deepcopy(self.context)
        changed_context["numerical"]["version"] = "different"
        for overrides in [
            {"query_bytes": self.query + b" "},
            {"context": changed_context},
        ]:
            with self.subTest(overrides=overrides):
                with self.assertRaises(ValueError):
                    with self.reopen(**overrides):
                        pass
        self.write_manifest([self.mapping[1], self.mapping[0]])
        with self.assertRaises(ValueError):
            with self.reopen():
                pass

    def test_storage_relocation_preserves_compatibility_and_detached_results(self):
        with self.create() as ledger:
            self.publish(ledger)
            context = ledger.context
            context["numerical"]["version"] = "caller mutation"
            self.assertEqual(ledger.context, self.context)
            detached = ledger.committed("alpha")
            detached["native_result"]["status"] = "failed"
            self.assertEqual(ledger.committed("alpha"), self.outcome())
        moved_database = self.root / "relocated.sqlite3"
        moved_manifest = self.root / "relocated-manifest.jsonl"
        shutil.copyfile(self.path, moved_database)
        shutil.copyfile(self.manifest, moved_manifest)
        with self.reopen(path=moved_database, manifest_path=moved_manifest) as ledger:
            self.assertEqual(ledger.query_bytes, self.query)
            self.assertEqual(list(ledger.results()), [self.outcome()])

    def test_exclusive_owner_is_released_on_close(self):
        with self.create() as ledger:
            for name, expected in (
                ("foreign_keys", 1),
                ("synchronous", 2),
                ("journal_mode", "delete"),
                ("locking_mode", "exclusive"),
            ):
                self.assertEqual(
                    ledger._connection.execute(f"PRAGMA {name}").fetchone(), (expected,)
                )
            with self.assertRaises(sqlite3.OperationalError):
                with self.reopen():
                    pass
        with self.reopen() as ledger:
            self.assertEqual(ledger.expected(0), self.mapping[0])

    def test_failed_publication_statement_rolls_back_visibility_and_winner(self):
        with self.create() as ledger:
            attempt = ledger.begin("alpha")
            ledger.stage(attempt, self.outcome())
            ledger._connection.execute(
                "CREATE TEMP TRIGGER reject_winner BEFORE UPDATE OF committed ON attempts "
                "BEGIN SELECT RAISE(ABORT, 'controlled publication interruption'); END"
            )
            with self.assertRaises(sqlite3.IntegrityError):
                ledger.publish(attempt)
            self.assertEqual(list(ledger.results()), [])
            self.assertFalse(list(ledger.attempts("alpha"))[0]["committed"])
            ledger._connection.execute("DROP TRIGGER reject_winner")
            self.assertTrue(ledger.publish(attempt))
        with self.reopen() as ledger:
            self.assertEqual(list(ledger.results()), [self.outcome()])

    def test_corrupt_staged_or_confirmed_payload_is_refused_on_open(self):
        for phase in ("staged", "committed"):
            source_path = self.root / f"{phase}-source.sqlite3"
            with self.create(path=source_path) as ledger:
                attempt = ledger.begin("alpha")
                ledger.stage(attempt, self.outcome())
                if phase == "committed":
                    ledger.publish(attempt)
            wrong_id = self.outcome()
            wrong_id["native_result"]["pose_id"] = "another-work-item"
            rehashed = _store.canonical_json(wrong_id)
            changes = [
                ("payload", "UPDATE attempts SET payload = ?", ["{}"]),
                ("checksum", "UPDATE attempts SET digest = ?", ["0" * 64]),
                (
                    "rehashed-mapping",
                    "UPDATE attempts SET payload = ?, digest = ?",
                    [rehashed, hashlib.sha256(rehashed.encode("utf-8")).hexdigest()],
                ),
            ]
            for label, sql, parameters in changes:
                with self.subTest(phase=phase, corruption=label):
                    target = self.root / f"{phase}-{label}.sqlite3"
                    shutil.copyfile(source_path, target)
                    with closing(sqlite3.connect(target)) as connection, connection:
                        connection.execute(sql, parameters)
                    with self.assertRaises((ValueError, sqlite3.DatabaseError)):
                        with self.reopen(path=target):
                            pass

    def test_changed_work_mapping_or_committing_attempt_is_refused(self):
        with self.create() as ledger:
            self.publish(ledger, "alpha")
            other_attempt = ledger.begin("beta")
            ledger.stage(other_attempt, self.outcome("beta"))
        changes = [
            (
                "source-mapping",
                "UPDATE work SET source_key = ? WHERE work_key = 'alpha'",
                ["source:substitution"],
            ),
            (
                "wrong-winning-attempt",
                "UPDATE outcomes SET attempt_id = ? WHERE work_key = 'alpha'",
                [other_attempt],
            ),
        ]
        for label, sql, parameters in changes:
            with self.subTest(corruption=label):
                target = self.root / f"{label}.sqlite3"
                shutil.copyfile(self.path, target)
                with closing(sqlite3.connect(target)) as connection, connection:
                    connection.execute(sql, parameters)
                with self.assertRaises((ValueError, sqlite3.DatabaseError)):
                    with self.reopen(path=target):
                        pass

    def test_query_metadata_checksums_and_schema_identity_are_verified(self):
        with self.create() as ledger:
            self.publish(ledger)
        changes = [
            (
                "query-bytes",
                "UPDATE metadata SET value = ? WHERE key = 'query'",
                [self.query + b"changed"],
            ),
            (
                "configuration-checksum",
                "UPDATE metadata SET value = ? WHERE key = 'configuration_sha256'",
                ["0" * 64],
            ),
            ("schema-version", "PRAGMA user_version = 999", []),
            ("application-identity", "PRAGMA application_id = 0", []),
        ]
        for label, sql, parameters in changes:
            with self.subTest(corruption=label):
                target = self.root / f"{label}.sqlite3"
                shutil.copyfile(self.path, target)
                with closing(sqlite3.connect(target)) as connection, connection:
                    connection.execute(sql, parameters)
                with self.assertRaises((ValueError, sqlite3.DatabaseError)):
                    with self.reopen(path=target):
                        pass

    def child(self, source, *arguments):
        return subprocess.run(
            [
                sys.executable,
                "-I",
                "-B",
                "-c",
                source,
                str(STORE),
                *map(str, arguments),
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )

    def interruption(self, phase):
        with self.create():
            pass
        source = """
import importlib.util, json, os, sys
spec = importlib.util.spec_from_file_location('isolated_store', sys.argv[1])
store = importlib.util.module_from_spec(spec)
spec.loader.exec_module(store)
ledger = store.ReferenceLedger.open(
    sys.argv[2], query_bytes=bytes.fromhex(sys.argv[4]),
    context=json.loads(sys.argv[5]), manifest_path=sys.argv[3],
)
attempt = ledger.begin('alpha')
ledger.stage(attempt, json.loads(sys.argv[6]))
if sys.argv[7] == 'committed':
    ledger.publish(attempt)
os._exit(73)
"""
        result = self.child(
            source,
            self.path,
            self.manifest,
            self.query.hex(),
            json.dumps(self.context),
            json.dumps(self.outcome()),
            phase,
        )
        self.assertEqual(result.returncode, 73, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_process_exit_after_stage_leaves_recomputable_attempt(self):
        self.interruption("staged")
        with self.reopen() as ledger:
            self.assertIsNone(ledger.committed("alpha"))
            previous = list(ledger.attempts("alpha"))
            self.assertEqual(len(previous), 1)
            self.assertTrue(previous[0]["staged"])
            self.assertFalse(previous[0]["committed"])
            self.publish(ledger)
            self.assertEqual(len(list(ledger.attempts("alpha"))), 2)
            self.assertEqual(list(ledger.results()), [self.outcome()])

    def test_process_exit_after_commit_preserves_undelivered_outcome_once(self):
        self.interruption("committed")
        with self.reopen() as ledger:
            self.assertEqual(list(ledger.results()), [self.outcome()])
            self.assertEqual(len(list(ledger.attempts("alpha"))), 1)
            with self.assertRaises(ValueError):
                ledger.begin("alpha")

    def test_saved_replay_works_with_scientific_imports_forbidden(self):
        with self.create() as ledger:
            self.publish(ledger)
        source = """
import importlib.util, json, sys
blocked = {'pharmacophoremt', 'molsysmt', 'numpy', 'scipy', 'rdkit', 'ackredit'}
class DenyScience:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in blocked:
            raise AssertionError('scientific import: ' + fullname)
sys.meta_path.insert(0, DenyScience())
spec = importlib.util.spec_from_file_location('isolated_store', sys.argv[1])
store = importlib.util.module_from_spec(spec)
spec.loader.exec_module(store)
with store.ReferenceLedger.open(
    sys.argv[2], query_bytes=bytes.fromhex(sys.argv[4]),
    context=json.loads(sys.argv[5]), manifest_path=sys.argv[3],
) as ledger:
    print(json.dumps(list(ledger.results()), allow_nan=False))
assert not any(name.split('.')[0] in blocked for name in sys.modules)
"""
        result = self.child(
            source,
            self.path,
            self.manifest,
            self.query.hex(),
            json.dumps(self.context),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [self.outcome()])


if __name__ == "__main__":
    unittest.main()
