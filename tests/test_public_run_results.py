"""Public saved-run formats, provider-free reading and bounded scalar command."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from pharmacophoremt_results import (
    ScreeningRunError,
    ScreeningRunStore,
    ScreeningRunView,
    canonical_json,
)

ROOT = Path(__file__).resolve().parents[1]
CRITERION = "checked_pose_coverage@1"
FRESH_GUARD = """
import sys
sys.path.insert(0, sys.argv.pop(1))
blocked = {'pharmacophoremt', 'molsysmt', 'numpy', 'scipy', 'rdkit',
           'pyunitwizard', 'ackredit', 'phmt_test_support'}
class Guard:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in blocked:
            raise AssertionError('unexpected scientific import: '+fullname)
sys.meta_path.insert(0, Guard())
"""


class TestPublicRunResults(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="phmt-public-run-results-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.path = self.root / "public run #1?.sqlite3"
        self.manifest = self.root / "work.jsonl"
        self.mapping = [
            {
                "work_key": key,
                "source_key": "source:repeated" if index < 2 else f"source:{index}",
                "occurrence_key": f"occurrence:{index}",
            }
            for index, key in enumerate(["alpha", "beta", "gamma", "delta", "epsilon"])
        ]
        self.write_manifest()
        self.query = b'{"original":"private saved query geometry"}\n'
        self.context = {
            "execution": {"score_method": "checked_pose_coverage"},
            "producer": {"version": "original-producer-0.1"},
        }

    def write_manifest(self):
        self.manifest.write_text(
            "".join(json.dumps(row) + "\n" for row in self.mapping), encoding="utf-8"
        )

    def create(self, **overrides):
        arguments = {
            "run_id": "run:public",
            "parent_run_id": "run:ancestor",
            "query_bytes": self.query,
            "context": self.context,
            "manifest_path": self.manifest,
        }
        arguments.update(overrides)
        return ScreeningRunStore.create(self.path, **arguments)

    def reopen(self):
        return ScreeningRunStore.open(
            self.path,
            query_bytes=self.query,
            context=self.context,
            manifest_path=self.manifest,
        )

    def outcome(self, key, *, score=0.75, status="matched"):
        mapping = next(row for row in self.mapping if row["work_key"] == key)
        return {
            **mapping,
            "native_result": {
                "pose_id": key,
                "status": status,
                "fit_value": score,
                "producer": {"version": "original-native-0.1"},
                "attribution": {
                    "status": "original-record",
                    "references": {"items": []},
                },
                "geometry": "private native geometry",
            },
            "ranking_score": score,
            "score_method": CRITERION,
        }

    def publish(self, ledger, key, **settings):
        attempt = ledger.begin(key)
        ledger.stage(attempt, self.outcome(key, **settings))
        self.assertTrue(ledger.publish(attempt))
        return attempt

    def create_partial(self):
        with self.create() as ledger:
            self.publish(ledger, "beta")
            self.publish(ledger, "alpha")
            self.publish(ledger, "gamma", score=0, status="not_matched")
            self.publish(ledger, "delta", score=None, status="failed")
            staged = ledger.begin("epsilon")
            ledger.stage(staged, self.outcome("epsilon", score=1))

    def test_public_seeded_scores_are_binary_and_agree_with_native_status(self):
        context = {"execution": {"score_method": "seeded_hit"}}
        with self.create(context=context) as ledger:
            for score, status in (
                (0.5, "matched"),
                (0, "matched"),
                (1, "not_matched"),
                (0.25, "not_matched"),
            ):
                with self.subTest(score=score, status=status):
                    attempt = ledger.begin("alpha")
                    outcome = self.outcome("alpha", score=score, status=status)
                    outcome["score_method"] = "seeded_hit@1"
                    with self.assertRaises(ScreeningRunError) as caught:
                        ledger.stage(attempt, outcome)
                    self.assertIn("binary score", str(caught.exception.__cause__))
                    self.assertIsNone(ledger.committed("alpha"))
            for key, score, status in (
                ("alpha", 1, "matched"),
                ("beta", 0, "not_matched"),
                ("gamma", None, "failed"),
            ):
                outcome = self.outcome(key, score=score, status=status)
                outcome["score_method"] = "seeded_hit@1"
                attempt = ledger.begin(key)
                ledger.stage(attempt, outcome)
                ledger.publish(attempt)
            self.assertEqual(
                [row["ranking_score"] for row in ledger.results()], [1, 0, None]
            )

    def test_checksum_valid_seeded_conflict_is_refused_without_rewriting_legacy(self):
        context = {"execution": {"score_method": "seeded_hit"}}
        outcome = self.outcome("alpha", score=1)
        outcome["score_method"] = "seeded_hit@1"
        with self.create(context=context) as ledger:
            attempt = ledger.begin("alpha")
            ledger.stage(attempt, outcome)
            ledger.publish(attempt)
        outcome["ranking_score"] = 0.5
        outcome["native_result"]["fit_value"] = 0.5
        payload = canonical_json(outcome)
        digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        with closing(sqlite3.connect(self.path)) as connection, connection:
            connection.execute(
                "UPDATE attempts SET payload=?, digest=? WHERE attempt_id=?",
                (payload, digest, attempt),
            )
        before = self.directory_bytes()
        with self.assertRaises(ScreeningRunError) as caught:
            ScreeningRunView.open(self.path)
        self.assertIn("binary score", str(caught.exception.__cause__))
        self.assertEqual(self.directory_bytes(), before)

        legacy = self.root / "fractional-legacy.sqlite3"
        with self.legacy().create(
            legacy,
            run_id="run:legacy-fractional",
            query_bytes=self.query,
            context=context,
            manifest_path=self.manifest,
        ) as ledger:
            attempt = ledger.begin("alpha")
            ledger.stage(attempt, outcome)
            ledger.publish(attempt)
        before = legacy.read_bytes()
        with ScreeningRunView.open(legacy, allow_legacy=True) as view:
            self.assertEqual(list(view.results()), [outcome])
        self.assertEqual(legacy.read_bytes(), before)

    def directory_bytes(self):
        return {
            path.name: path.read_bytes()
            for path in self.root.iterdir()
            if path.is_file()
        }

    def legacy(self):
        spec = importlib.util.spec_from_file_location(
            "public_result_legacy_fixture",
            ROOT / "phmt_test_support/reference_run_store.py",
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.ReferenceLedger

    def create_legacy(self):
        with self.legacy().create(
            self.path,
            run_id="run:legacy",
            query_bytes=self.query,
            context=self.context,
            manifest_path=self.manifest,
        ) as ledger:
            self.publish(ledger, "alpha")

    def fresh(self, source, *arguments):
        return subprocess.run(
            [
                sys.executable,
                "-I",
                "-B",
                "-c",
                FRESH_GUARD + source,
                str(ROOT),
                *map(str, arguments),
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def command(self, *arguments):
        return self.fresh(
            "\nimport runpy\nsys.argv[0] = 'pharmacophoremt_results'\n"
            "runpy.run_module('pharmacophoremt_results', run_name='__main__')\n",
            *arguments,
        )

    def test_new_writer_format_and_complete_original_results_are_detached(self):
        self.create_partial()
        before = self.directory_bytes()
        with ScreeningRunView.open(self.path) as view:
            self.assertEqual(
                view.configuration["format"], "pharmacophoremt.screening-run@1"
            )
            self.assertEqual(view.query_bytes, self.query)
            configuration = view.configuration
            configuration["context"]["producer"]["version"] = "changed by caller"
            self.assertEqual(view.configuration["context"], self.context)
            original = list(view.results())
            self.assertEqual(
                [row["work_key"] for row in original],
                ["alpha", "beta", "gamma", "delta"],
            )
            self.assertEqual(
                [row["ranking_score"] for row in original], [0.75, 0.75, 0, None]
            )
            original[0]["native_result"]["producer"]["version"] = "changed by caller"
            self.assertEqual(
                next(view.results())["native_result"]["producer"]["version"],
                "original-native-0.1",
            )
        self.assertEqual(self.directory_bytes(), before)

    def test_summary_keeps_failed_scored_and_pending_work_separate(self):
        self.create_partial()
        with ScreeningRunView.open(self.path) as view:
            summary = view.summary(score_method=CRITERION)
        self.assertEqual(
            summary["counts"],
            {
                "declared_work": 5,
                "committed_work": 4,
                "scored_work": 3,
                "matched_work": 2,
                "not_matched_work": 1,
                "failed_work": 1,
                "pending_work": 1,
            },
        )
        self.assertEqual(
            summary["attempts"], {"started": 5, "staged": 5, "committed": 4}
        )
        self.assertFalse(summary["manifest_work_complete"])
        self.assertEqual(summary["ranking_scope"], "observed_scored_work_only")

    def test_ranking_uses_observed_scores_and_manifest_order_including_valid_zero(self):
        self.create_partial()
        with ScreeningRunView.open(self.path) as view:
            ranked = view.top_results(score_method=CRITERION, limit=10)
            self.assertEqual(
                [row["manifest_ordinal"] for row in ranked["records"]], [0, 1, 2]
            )
            self.assertEqual(
                [row["outcome"]["work_key"] for row in ranked["records"]],
                ["alpha", "beta", "gamma"],
            )
            self.assertEqual(
                view.top_results(score_method=CRITERION, limit=0)["records"], []
            )
            self.assertEqual(ranked["summary"]["counts"]["pending_work"], 1)

    def test_legacy_read_requires_explicit_opt_in_and_never_migrates_bytes(self):
        self.create_legacy()
        before = self.directory_bytes()
        with self.assertRaises(ValueError):
            ScreeningRunView.open(self.path)
        with ScreeningRunView.open(self.path, allow_legacy=True) as view:
            self.assertEqual(
                view.configuration["format"], "pharmacophoremt.reference-ledger@1"
            )
            self.assertEqual(list(view.results()), [self.outcome("alpha")])
        self.assertEqual(self.directory_bytes(), before)

    def test_new_writer_cannot_resume_legacy_even_with_identical_query_and_manifest(
        self,
    ):
        self.create_legacy()
        before = self.directory_bytes()
        with self.assertRaises(ValueError):
            self.reopen()
        self.assertEqual(self.directory_bytes(), before)

    def test_confirmed_failure_stays_unscored_and_requires_a_new_run_for_retry(self):
        with self.create() as ledger:
            attempt = self.publish(ledger, "alpha", score=None, status="failed")
        with self.reopen() as ledger:
            self.assertEqual(
                ledger.committed("alpha"),
                self.outcome("alpha", score=None, status="failed"),
            )
            with self.assertRaises(ValueError):
                ledger.begin("alpha")
            self.assertEqual(list(ledger.attempts("alpha"))[0]["attempt_id"], attempt)

    def test_staged_outcome_is_pending_and_recomputation_keeps_both_attempts(self):
        with self.create() as ledger:
            staged = ledger.begin("alpha")
            ledger.stage(staged, self.outcome("alpha"))
        with ScreeningRunView.open(self.path) as view:
            self.assertEqual(list(view.results()), [])
            self.assertEqual(
                view.summary(score_method=CRITERION)["counts"]["pending_work"], 5
            )
        with self.reopen() as ledger:
            self.assertIsNone(ledger.committed("alpha"))
            confirmed = self.publish(ledger, "alpha")
            self.assertNotEqual(staged, confirmed)
            self.assertEqual(
                [row["committed"] for row in ledger.attempts("alpha")], [False, True]
            )

    def test_corruption_outside_requested_top_result_and_staged_attempt_is_refused(
        self,
    ):
        for index, key in enumerate(["gamma", "epsilon"]):
            with self.subTest(key=key):
                self.path = self.root / f"corrupt-{index}.sqlite3"
                self.create_partial()
                with closing(sqlite3.connect(self.path)) as connection, connection:
                    connection.execute(
                        "UPDATE attempts SET payload=payload || ' ' WHERE work_key=?",
                        (key,),
                    )
                before = self.directory_bytes()
                with self.assertRaises(ValueError):
                    ScreeningRunView.open(self.path)
                self.assertEqual(self.directory_bytes(), before)

    def test_empty_manifest_is_work_complete_without_scored_or_failed_work(self):
        self.mapping = []
        self.write_manifest()
        with self.create():
            pass
        with ScreeningRunView.open(self.path) as view:
            summary = view.summary(score_method=CRITERION)
            self.assertTrue(summary["manifest_work_complete"])
            self.assertEqual(set(summary["counts"].values()), {0})
            self.assertEqual(
                view.top_results(score_method=CRITERION, limit=5)["records"], []
            )

    def test_missing_or_unknown_version_is_refused_without_file_creation_or_repair(
        self,
    ):
        with self.assertRaises((OSError, sqlite3.Error, ValueError)) as refused:
            ScreeningRunView.open(self.path)
        if isinstance(refused.exception, ValueError):
            self.assertIsInstance(refused.exception.__cause__, (OSError, sqlite3.Error))
        self.assertFalse(self.path.exists())
        with self.create():
            pass
        with closing(sqlite3.connect(self.path)) as connection, connection:
            connection.execute("PRAGMA user_version=999")
        before = self.directory_bytes()
        with self.assertRaises(ValueError):
            ScreeningRunView.open(self.path)
        self.assertEqual(self.directory_bytes(), before)

    def test_invalid_limits_criteria_and_unknown_keywords_preserve_saved_bytes(self):
        self.create_partial()
        before = self.directory_bytes()
        with ScreeningRunView.open(self.path) as view:
            for limit in [-1, True, 0.5]:
                with self.subTest(limit=limit), self.assertRaises(ValueError):
                    view.top_results(score_method=CRITERION, limit=limit)
            with self.assertRaises(ValueError):
                view.summary(score_method="seeded_hit@1")
            for extra in [
                {"skip_digestion": True},
                {"skip_digestion": False},
                {"typo": True},
            ]:
                with self.subTest(extra=extra), self.assertRaises(TypeError):
                    view.summary(score_method=CRITERION, **extra)
        self.assertEqual(self.directory_bytes(), before)

    def test_storage_refusal_has_a_catalog_code_and_retains_the_sqlite_cause(self):
        with self.assertRaises(ScreeningRunError) as refused:
            ScreeningRunView.open(self.path)
        self.assertEqual(refused.exception.code, "PHMT-E201")
        self.assertIsInstance(refused.exception.__cause__, sqlite3.Error)
        self.assertFalse(self.path.exists())

    def test_invalid_legacy_admission_is_refused_before_opening_a_missing_file(self):
        for flag in ["yes", 1, None]:
            with (
                self.subTest(flag=flag),
                self.assertRaises(ScreeningRunError) as refused,
            ):
                ScreeningRunView.open(self.path, allow_legacy=flag)
            self.assertEqual(refused.exception.code, "PHMT-E201")
            self.assertIsNone(refused.exception.__cause__)
        self.assertFalse(self.path.exists())

    def test_closed_view_cannot_read_and_writer_ownership_is_released(self):
        self.create_partial()
        view = ScreeningRunView.open(self.path)
        with self.assertRaises((sqlite3.Error, ValueError)) as refused:
            self.reopen()
        if isinstance(refused.exception, ValueError):
            self.assertIsInstance(refused.exception.__cause__, sqlite3.Error)
        view.close()
        view.close()
        with self.assertRaises(ValueError):
            view.summary(score_method=CRITERION)
        with self.assertRaises(ValueError):
            list(view.results())
        with self.reopen() as ledger:
            self.assertEqual(len(list(ledger.results())), 4)

    def test_fresh_public_reader_needs_no_molecular_or_attribution_providers(self):
        self.create_partial()
        self.manifest.unlink()
        before = self.directory_bytes()
        result = self.fresh(
            """
from pharmacophoremt_results import ScreeningRunView
with ScreeningRunView.open(sys.argv[1]) as view:
    assert view.configuration['context']['producer']['version'] == 'original-producer-0.1'
    assert view.query_bytes == b'{"original":"private saved query geometry"}\\n'
    assert view.summary(score_method='checked_pose_coverage@1')['counts']['scored_work'] == 3
    saved = list(view.results())
    assert saved[0]['native_result']['producer']['version'] == 'original-native-0.1'
    assert len(saved) == 4
assert not any(name.split('.')[0] in blocked for name in sys.modules)
""",
            self.path,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.directory_bytes(), before)

    def test_public_module_command_emits_only_bounded_scalar_observations(self):
        self.create_partial()
        before = self.directory_bytes()
        result = self.command(self.path, "--score-method", CRITERION, "--limit", "2")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(
            [row["work_key"] for row in output["records"]], ["alpha", "beta"]
        )
        self.assertEqual(
            output["summary"]["ranking_scope"], "observed_scored_work_only"
        )
        self.assertEqual(output["summary"]["counts"]["pending_work"], 1)
        self.assertTrue(
            all(
                set(row)
                == {
                    "manifest_ordinal",
                    "work_key",
                    "source_key",
                    "occurrence_key",
                    "ranking_score",
                    "score_method",
                    "status",
                }
                for row in output["records"]
            )
        )
        self.assertNotIn("private saved query geometry", result.stdout)
        self.assertNotIn("private native geometry", result.stdout)
        self.assertEqual(self.directory_bytes(), before)

    def test_public_module_command_refuses_legacy_until_explicitly_requested(self):
        self.create_legacy()
        before = self.directory_bytes()
        denied = self.command(self.path, "--score-method", CRITERION)
        self.assertNotEqual(denied.returncode, 0)
        self.assertEqual(denied.stdout, "")
        allowed = self.command(self.path, "--score-method", CRITERION, "--allow-legacy")
        self.assertEqual(allowed.returncode, 0, allowed.stdout + allowed.stderr)
        self.assertEqual(json.loads(allowed.stdout)["records"][0]["work_key"], "alpha")
        self.assertEqual(self.directory_bytes(), before)

    def test_public_module_help_needs_no_run_or_molecular_provider(self):
        result = self.command("--help")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("--allow-legacy", result.stdout)
        self.assertIn("--score-method", result.stdout)
        self.assertFalse(self.path.exists())

    def test_public_module_command_bad_requests_produce_no_partial_output(self):
        self.create_partial()
        before = self.directory_bytes()
        for options in [["--limit", "-1"], ["--score-method", "unknown@1"]]:
            with self.subTest(options=options):
                result = self.command(self.path, "--score-method", CRITERION, *options)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr)
        self.assertEqual(self.directory_bytes(), before)


if __name__ == "__main__":
    unittest.main()
