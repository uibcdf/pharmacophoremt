"""Public screening-run storage and read-only evidence orchestration."""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from argdigest import arg_digest
from smonitor import signal

from . import _exports, _store
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

    @signal(tags=["results", "run", "progress"])
    @arg_digest(config=config("ScreeningRunStore.progress"))
    def progress(self):
        """Count confirmed/pending work and attempts between writes, without ranking.

        Use this owned writer connection; a separate read view requires closing
        the writer first. Semantics match :meth:`ScreeningRunView.progress`.
        """
        return _invoke(
            "inspect saved progress", _store.ReferenceRunView(self._ledger).progress
        )

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

    @signal(tags=["results", "read", "progress"])
    @arg_digest(config=config("ScreeningRunView.progress"))
    def progress(self):
        """Inspect saved work and attempts without choosing a ranking criterion.

        Returns detached run/parent IDs, ``counts``, ``attempts`` and
        ``manifest_work_complete``. Work counts separate declared, committed,
        scored, matched, not-matched, failed and pending items. Attempts separate
        started, staged and committed records; unpublished stages remain pending.
        No native payload, query, score criterion or ranking is returned.

        Complete declared work may include failures. Counts describe work items,
        not independent compounds or biological validity. Empty work is complete.
        Opening fully verifies saved evidence. The first call scans confirmed
        outcomes; later calls reuse detached counts within that same read-only
        snapshot. Close and reopen to inspect a later writer state. No scientific
        computation is performed.

        >>> with ScreeningRunView.open('run.sqlite3') as view:
        ...     pending = view.progress()['counts']['pending_work']
        """
        return _invoke("inspect saved progress", self._view.progress)

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

    @signal(tags=["results", "export", "jsonl"])
    @arg_digest(config=config("ScreeningRunView.to_jsonl"))
    def to_jsonl(self, path):
        """Export every confirmed original outcome to a fresh UTF-8 JSONL file.

        Parameters
        ----------
        path : str or os.PathLike
            New destination in an existing directory. Existing destinations,
            including symlinks, are never replaced.

        Returns
        -------
        dict
            Detached ``pharmacophoremt.screening-export@1`` receipt containing
            original configuration, output byte count/SHA-256, exported record
            count and pending work count. Full native evidence is retained.

        Notes
        -----
        Streams all confirmations, including negatives and failures, in manifest
        order. A private same-directory file is closed and hashed before exclusive
        hard-link publication; unsupported filesystems fail. Prepublication errors
        attempt cleanup without exposing a partial destination. Postpublication
        cleanup errors carry ``published=True``, ``receipt`` and ``temporary_path``
        in ``ScreeningRunError.extra``. Separate exports are not one transaction.
        Saved query bytes and attempts remain in the authoritative database.
        No science or attribution is executed. Full results can contain geometry;
        callers own their disclosure. This does not qualify power-loss durability.

        Examples
        --------
        >>> with ScreeningRunView.open('run.sqlite3') as view:
        ...     receipt = view.to_jsonl('outcomes.jsonl')
        """
        return _invoke("export JSONL", _exports.export, self, path, "jsonl")

    @signal(tags=["results", "export", "csv"])
    @arg_digest(config=config("ScreeningRunView.to_csv"))
    def to_csv(self, path):
        """Export a complete scalar result table to a fresh UTF-8 CSV file.

        Parameters
        ----------
        path : str or os.PathLike
            New destination in an existing directory. Existing destinations,
            including symlinks, are never replaced.

        Returns
        -------
        dict
            Detached ``pharmacophoremt.screening-export@1`` receipt with original
            configuration, output identity and explicit confirmed/pending counts.

        Notes
        -----
        Columns are ``work_key,source_key,occurrence_key,status,ranking_score,
        score_method``. Manifest order, literal identifiers and zero scores are
        preserved; unscored failures have empty score cells. Native geometry,
        units and attribution remain available through ``results()``/``to_jsonl``.
        Publication, cleanup and data-authority semantics match ``to_jsonl``.
        An empty run writes only the header; pending work is not exported.

        Examples
        --------
        >>> with ScreeningRunView.open('run.sqlite3') as view:
        ...     receipt = view.to_csv('outcomes.csv')
        """
        return _invoke("export CSV", _exports.export, self, path, "csv")

    def close(self):
        """Release this read snapshot without changing saved evidence."""
        return _invoke("close saved evidence", self._view.close)

    def __enter__(self):
        _invoke("enter saved evidence", self._view.__enter__)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def main(argv=None):
    """Inspect saved progress/ranks or export evidence through the public view.

    Successful inspection prints bounded scalar JSON; export prints the original
    API receipt. Handled failures exit2 without a success response. Publication
    followed by cleanup/close failure retains a coded JSON receipt on stderr.
    """
    parser = argparse.ArgumentParser(
        description="Inspect or export a saved PharmacophoreMT screening run without rerunning science."
    )
    parser.add_argument("ledger", type=Path, help="Saved screening-run database.")
    exports = parser.add_mutually_exclusive_group()
    exports.add_argument(
        "--summary",
        action="store_true",
        help="Show saved work/attempt counts without selecting a ranking criterion.",
    )
    exports.add_argument(
        "--to-jsonl",
        type=Path,
        metavar="FILE",
        help="Export all confirmed original outcomes to a new JSONL file.",
    )
    exports.add_argument(
        "--to-csv",
        type=Path,
        metavar="FILE",
        help="Export all confirmed outcomes to a new scalar CSV file.",
    )
    parser.add_argument(
        "--score-method",
        choices=("seeded_hit@1", "checked_pose_coverage@1"),
        help="Required for ranked inspection; cannot be combined with summary/export.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Ranked inspection only; defaults to 10. Summary/export has no limit.",
    )
    parser.add_argument(
        "--allow-legacy",
        action="store_true",
        help="Explicitly admit read-only legacy reference-ledger@1 files.",
    )
    arguments = parser.parse_args(argv)
    exporting = arguments.to_jsonl is not None or arguments.to_csv is not None
    ranked = not (exporting or arguments.summary)
    if not ranked and (
        arguments.score_method is not None or arguments.limit is not None
    ):
        parser.error("--score-method and --limit are only valid for ranked inspection")
    if ranked and arguments.score_method is None:
        parser.error("--score-method is required for ranked inspection")
    receipt = None
    try:
        with ScreeningRunView.open(
            arguments.ledger, allow_legacy=arguments.allow_legacy
        ) as view:
            if arguments.summary:
                result = view.progress()
            elif arguments.to_jsonl is not None:
                result = receipt = view.to_jsonl(arguments.to_jsonl)
            elif arguments.to_csv is not None:
                result = receipt = view.to_csv(arguments.to_csv)
            else:
                result = view.top_results(
                    score_method=arguments.score_method,
                    limit=10 if arguments.limit is None else arguments.limit,
                )
        if ranked:
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
        context = getattr(error, "extra", {})
        if context.get("published") is True:
            receipt = context["receipt"]
        if receipt is not None:
            print(
                json.dumps(
                    {
                        "code": getattr(error, "code", None),
                        "error": str(error),
                        "published": True,
                        "receipt": receipt,
                        "temporary_path": context.get("temporary_path"),
                    },
                    ensure_ascii=False,
                    allow_nan=False,
                ),
                file=sys.stderr,
            )
        parser.error(str(error))
    print(encoded)
    return 0
