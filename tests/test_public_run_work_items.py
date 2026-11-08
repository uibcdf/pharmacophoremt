"""Public saved-manifest reading includes unconfirmed work without science."""

import unittest
from concurrent.futures import ThreadPoolExecutor

import test_public_run_results as fixtures

from pharmacophoremt_results import ScreeningRunError, ScreeningRunView


class TestPublicRunWorkItems(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.TestPublicRunResults()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def test_partial_manifest_is_ordered_complete_detached_and_unchanged(self):
        f = self.fixture
        f.create_partial()
        before = f.directory_bytes()
        expected = [dict(manifest_ordinal=i, **row) for i, row in enumerate(f.mapping)]
        with ScreeningRunView.open(f.path) as view:
            rows = list(view.work_items())
            self.assertEqual(rows, expected)
            rows[0].clear()
            self.assertEqual(list(view.work_items()), expected)
            self.assertEqual(len(list(view.results())), 4)
        self.assertEqual(f.directory_bytes(), before)

    def test_empty_manifest_is_empty(self):
        f = self.fixture
        f.mapping = []
        f.write_manifest()
        with f.create():
            pass
        with ScreeningRunView.open(f.path) as view:
            self.assertEqual(list(view.work_items()), [])

    def test_explicit_legacy_admission_preserves_original_manifest(self):
        f = self.fixture
        f.create_legacy()
        before = f.directory_bytes()
        with self.assertRaises(ScreeningRunError):
            ScreeningRunView.open(f.path)
        with ScreeningRunView.open(f.path, allow_legacy=True) as view:
            self.assertEqual(
                list(view.work_items()),
                [dict(manifest_ordinal=i, **row) for i, row in enumerate(f.mapping)],
            )
        self.assertEqual(f.directory_bytes(), before)

    def test_iterator_is_lazy_and_refuses_a_closed_connection(self):
        f = self.fixture
        f.create_partial()
        with ScreeningRunView.open(f.path) as view:
            iterator = view.work_items()
        with self.assertRaises(ScreeningRunError):
            next(iterator)

    def test_partial_iteration_refuses_close_before_the_next_pull(self):
        f = self.fixture
        f.create_partial()
        with ScreeningRunView.open(f.path) as view:
            iterator = view.work_items()
            self.assertEqual(next(iterator)["work_key"], "alpha")
        with self.assertRaises(ScreeningRunError):
            next(iterator)

    def test_wrong_thread_refuses_iteration(self):
        f = self.fixture
        f.create_partial()
        with ScreeningRunView.open(f.path) as view:
            with ThreadPoolExecutor(max_workers=1) as worker:
                future = worker.submit(lambda: list(view.work_items()))
                with self.assertRaises(ScreeningRunError):
                    future.result()

    def test_closed_signature_refuses_unknown_options(self):
        from argdigest import UnknownArgumentError

        f = self.fixture
        f.create_partial()
        with ScreeningRunView.open(f.path) as view:
            with self.assertRaises(UnknownArgumentError):
                view.work_items(unknown=True)

    def test_fresh_guarded_manifest_reader_imports_no_scientific_package(self):
        f = self.fixture
        f.create_partial()
        before = f.directory_bytes()
        result = f.fresh(
            "\nfrom pharmacophoremt_results import ScreeningRunView\n"
            "with ScreeningRunView.open(sys.argv[1]) as view:\n"
            "    rows = list(view.work_items())\n"
            "assert [r['manifest_ordinal'] for r in rows] == list(range(5))\n"
            "assert rows[-1]['work_key'] == 'epsilon'\n",
            f.path,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(f.directory_bytes(), before)
