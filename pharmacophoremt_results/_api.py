"""Public screening-run storage and read-only evidence orchestration."""

import argparse
import json
import sqlite3
from pathlib import Path

from argdigest import arg_digest
from smonitor import signal

from . import _store
from ._diagnostics import ScreeningRunError
from ._digestion import config


def _invoke(operation, function, *args, **kwargs):
    try:
        return function(*args, **kwargs)
    except ScreeningRunError:
        raise
    except (OSError, ValueError, sqlite3.Error) as error:
        raise ScreeningRunError(operation=operation, reason=str(error)) from error


def _iterate(operation, source):
    try:
        yield from source
    except ScreeningRunError:
        raise
    except (OSError, ValueError, sqlite3.Error) as error:
        raise ScreeningRunError(operation=operation, reason=str(error)) from error
    finally:
        source.close()


@signal(tags=["results", "json", "encode"])
@arg_digest(config=config("canonical_json"))
def canonical_json(value):
    """Encode finite plain JSON data without changing key types or units.

    Objects must have string keys; values are plain dict/list/string/bool/int,
    finite float or None. Cycles, duplicate keys on reading, nonfinite values
    and implicit conversion of arbitrary Python objects are refused. This codec
    does not interpret a scientific schema or authenticate its declared values.
    """
    return _invoke("encode JSON", _store.canonical_json, value)


class ScreeningRunStore:
    """An exclusively owned writer for ``pharmacophoremt.screening-run@1``.

    Construct with :meth:`create` or :meth:`open`, then close or use a context
    manager. Creation never replaces a destination. Reopening requires exact
    query, context and original ordered manifest identities. Neither operation
    loads molecular providers, validates molecular preparation or runs a query.

    Begin, stage and publish are separate retained transactions. Only publication
    confirms a terminal outcome. Confirmed failures stay unscored and immutable;
    retry or changed settings require a new run, optionally linked by parent ID.
    Interruptions can cause recomputation before confirmation or prevent external
    delivery after confirmation. Read ``results()`` for the authoritative view.

    Checksums and supplied compatibility metadata establish consistency, not
    authentication, biological independence or complete provider qualification.
    The single-owner local SQLite contract makes no power-loss, network-filesystem
    or multiwriter guarantee. Close this writer before opening a read-only view.
    """

    def __init__(self, ledger):
        if not isinstance(ledger, _store.ScreeningLedger):
            raise ScreeningRunError(
                operation="construct a writer",
                reason="use ScreeningRunStore.create or ScreeningRunStore.open",
            )
        self._ledger = ledger

    @classmethod
    @signal(tags=["results", "run", "create"])
    @arg_digest(config=config("ScreeningRunStore.create"))
    def create(
        cls,
        path,
        *,
        run_id,
        query_bytes,
        context,
        manifest_path,
        parent_run_id=None,
    ):
        """Create a fresh run from exact query bytes and a three-key JSONL manifest.

        ``context`` is detached finite JSON. Each manifest record has exactly
        ``work_key``, ``source_key`` and ``occurrence_key``. Work keys are unique;
        repeated source/occurrence keys preserve original multiplicity. No
        molecular/chemical equivalence or independent-assay count is inferred.
        A failed creation retains its new file for inspection; never reuse that
        file as a valid run without successful opening and verification.
        """
        ledger = _invoke(
            "create a run",
            _store.ScreeningLedger.create,
            path,
            run_id=run_id,
            query_bytes=query_bytes,
            context=context,
            manifest_path=manifest_path,
            parent_run_id=parent_run_id,
        )
        return cls(ledger)

    @classmethod
    @signal(tags=["results", "run", "reopen"])
    @arg_digest(config=config("ScreeningRunStore.open"))
    def open(cls, path, *, query_bytes, context, manifest_path):
        """Reopen the same public-format run, checking bindings before mutation.

        Legacy experimental files cannot be resumed through this writer. Their
        explicit read-only admission in :class:`ScreeningRunView` is a separate
        operation and performs no migration or rewriting.
        """
        ledger = _invoke(
            "reopen a run",
            _store.ScreeningLedger.open,
            path,
            query_bytes=query_bytes,
            context=context,
            manifest_path=manifest_path,
        )
        return cls(ledger)

    @property
    def run_id(self):
        return self._ledger.run_id

    @property
    def parent_run_id(self):
        return self._ledger.parent_run_id

    @property
    def query_bytes(self):
        """Original immutable saved bytes, including any original geometry."""
        return self._ledger.query_bytes

    @property
    def context(self):
        """Detach the original execution and producer declarations."""
        return _invoke("read run context", lambda: self._ledger.context)

    @property
    def configuration(self):
        """Detach complete saved configuration while this connection is open."""
        return _invoke(
            "read run configuration",
            lambda: _store.ReferenceRunView(self._ledger).configuration,
        )

    @arg_digest(config=config("ScreeningRunStore.expected"))
    def expected(self, ordinal):
        """Return one ordered three-key mapping, or None after declared work."""
        return _invoke("read declared work", self._ledger.expected, ordinal)

    @arg_digest(config=config("ScreeningRunStore.begin"))
    def begin(self, work_key):
        """Retain a new unpublished attempt for a known unconfirmed work key."""
        return _invoke("begin an attempt", self._ledger.begin, work_key)

    @arg_digest(config=config("ScreeningRunStore.stage"))
    def stage(self, attempt_id, outcome):
        """Stage detached canonical evidence without confirming its visibility."""
        return _invoke("stage an outcome", self._ledger.stage, attempt_id, outcome)

    @signal(tags=["results", "run", "confirm"])
    @arg_digest(config=config("ScreeningRunStore.publish"))
    def publish(self, attempt_id):
        """Confirm one outcome atomically; identical republication returns False."""
        return _invoke("confirm an outcome", self._ledger.publish, attempt_id)

    @arg_digest(config=config("ScreeningRunStore.committed"))
    def committed(self, work_key):
        """Detach a confirmed outcome, or None while that work is pending."""
        return _invoke("read a confirmed outcome", self._ledger.committed, work_key)

    @arg_digest(config=config("ScreeningRunStore.results"))
    def results(self):
        """Iterate all confirmed original outcomes in declared manifest order."""
        return _iterate("read saved outcomes", self._ledger.results())

    @arg_digest(config=config("ScreeningRunStore.attempts"))
    def attempts(self, work_key):
        """Iterate retained attempt states for one known work key."""
        return _iterate("read retained attempts", self._ledger.attempts(work_key))

    @signal(tags=["results", "run", "summary"])
    @arg_digest(config=config("ScreeningRunStore.summary"))
    def summary(self, *, score_method):
        """Inspect work coverage between writes using the caller-owned connection."""
        return _invoke(
            "summarize saved work",
            _store.ReferenceRunView(self._ledger).summary,
            score_method=score_method,
        )

    @signal(tags=["results", "run", "rank"])
    @arg_digest(config=config("ScreeningRunStore.top_results"))
    def top_results(self, *, score_method, limit):
        """Inspect observed ranks between writes, retaining at most limit payloads."""
        return _invoke(
            "rank observed work",
            _store.ReferenceRunView(self._ledger).top_results,
            score_method=score_method,
            limit=limit,
        )

    def close(self):
        """Release this connection; existing saved evidence remains unchanged."""
        return _invoke("close a run", self._ledger.close)

    def __enter__(self):
        _invoke("enter a run", self._ledger.__enter__)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class ScreeningRunView:
    """A verified read-only snapshot of saved screening evidence.

    Opening verifies configuration, query bytes, every mapping and every attempt,
    including unpublished records and work outside a requested ranking. Close
    any exclusive writer before opening, and close this view before resuming.
    The view remains fixed until closure and never executes stored code, loads
    molecular/citation providers, recomputes scores or creates attribution.

    Counts describe declared work, not independent compounds. Top results cover
    observed scored work only; valid zero negatives remain scored and failures
    remain unscored. Selection scans outcomes and retains at most K payloads;
    opening verifies the whole file. This is neither an index nor a global
    top-K proof for incomplete work. Original full bodies can contain geometry.
    """

    def __init__(self, view):
        if not isinstance(view, _store.ScreeningRunViewCore):
            raise ScreeningRunError(
                operation="construct a view",
                reason="use ScreeningRunView.open",
            )
        self._view = view

    @classmethod
    @signal(tags=["results", "read", "open"])
    @arg_digest(config=config("ScreeningRunView.open"))
    def open(cls, path, *, allow_legacy=False):
        """Read public v1 files, optionally admitting the old reference format.

        ``allow_legacy=True`` permits read-only inspection of
        ``pharmacophoremt.reference-ledger@1``. It leaves the original format,
        producer context and file bytes unchanged, authorizing no migration or
        resumption under the current scientific software.
        """
        view = _invoke(
            "open saved evidence",
            _store.ScreeningRunViewCore.open,
            path,
            allow_legacy=allow_legacy,
        )
        return cls(view)

    @property
    def configuration(self):
        """Detach original versions, identities and exact execution declarations."""
        return _invoke("read original configuration", lambda: self._view.configuration)

    @property
    def query_bytes(self):
        """Return exact original saved query bytes, without loading its producer."""
        return _invoke("read original query", lambda: self._view.query_bytes)

    @signal(tags=["results", "read", "summary"])
    @arg_digest(config=config("ScreeningRunView.summary"))
    def summary(self, *, score_method):
        """Count confirmed/failed/pending work and retained attempts separately."""
        return _invoke(
            "summarize saved work", self._view.summary, score_method=score_method
        )

    @signal(tags=["results", "read", "rank"])
    @arg_digest(config=config("ScreeningRunView.top_results"))
    def top_results(self, *, score_method, limit):
        """Select observed scores descending, with original manifest order for ties."""
        return _invoke(
            "rank observed work",
            self._view.top_results,
            score_method=score_method,
            limit=limit,
        )

    @arg_digest(config=config("ScreeningRunView.results"))
    def results(self):
        """Iterate detached full confirmed outcomes in manifest order."""
        return _iterate("read original outcomes", self._view.results())

    def close(self):
        """Release this read snapshot without changing saved evidence."""
        return _invoke("close saved evidence", self._view.close)

    def __enter__(self):
        _invoke("enter saved evidence", self._view.__enter__)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def main(argv=None):
    """Print bounded scalar saved results; errors produce no partial JSON stdout."""
    parser = argparse.ArgumentParser(description=ScreeningRunView.__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument(
        "--score-method",
        required=True,
        choices=("seeded_hit@1", "checked_pose_coverage@1"),
    )
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--allow-legacy", action="store_true")
    arguments = parser.parse_args(argv)
    try:
        with ScreeningRunView.open(
            arguments.ledger, allow_legacy=arguments.allow_legacy
        ) as view:
            result = view.top_results(
                score_method=arguments.score_method, limit=arguments.limit
            )
        result["records"] = [
            {
                "manifest_ordinal": record["manifest_ordinal"],
                **{
                    name: record["outcome"][name]
                    for name in (
                        "work_key",
                        "source_key",
                        "occurrence_key",
                        "ranking_score",
                        "score_method",
                    )
                },
                "status": record["outcome"]["native_result"]["status"],
            }
            for record in result["records"]
        ]
        encoded = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)
    except (ScreeningRunError, OSError, ValueError, sqlite3.Error) as error:
        parser.error(str(error))
    print(encoded)
    return 0
