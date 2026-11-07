"""Unshipped, stdlib-only outcome ledger for the prepared reference (#108).

This single-owner SQLite experiment checks declared identities and stored bytes.
It authenticates no molecular object and promises neither power-loss/platform
qualification, distributed execution nor exactly-once external result delivery.
"""

import hashlib
import heapq
import json
import math
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

_VERSION = 1
_APPLICATION_ID = 0x50484D54
_FORMAT = "pharmacophoremt.reference-ledger@1"
_MAX_LINE_BYTES = 64 * 1024
_MAPPING_KEYS = {"work_key", "source_key", "occurrence_key"}
_OUTCOME_KEYS = _MAPPING_KEYS | {"native_result", "ranking_score", "score_method"}
_CONFIG_KEYS = {
    "format",
    "run_id",
    "parent_run_id",
    "query_sha256",
    "context",
    "manifest_sha256",
    "work_sha256",
    "work_count",
}
_SCHEMA = {
    "metadata": "CREATE TABLE metadata (key TEXT PRIMARY KEY, value BLOB NOT NULL)",
    "work": """CREATE TABLE work (
        ordinal INTEGER NOT NULL UNIQUE CHECK (typeof(ordinal) = 'integer' AND ordinal >= 0),
        work_key TEXT PRIMARY KEY,
        source_key TEXT NOT NULL,
        occurrence_key TEXT NOT NULL
    )""",
    "attempts": """CREATE TABLE attempts (
        attempt_id INTEGER PRIMARY KEY,
        work_key TEXT NOT NULL REFERENCES work(work_key),
        payload TEXT,
        digest TEXT,
        committed INTEGER NOT NULL DEFAULT 0 CHECK (committed IN (0, 1)),
        CHECK ((payload IS NULL) = (digest IS NULL)),
        CHECK (committed = 0 OR payload IS NOT NULL)
    )""",
    "outcomes": """CREATE TABLE outcomes (
        work_key TEXT PRIMARY KEY REFERENCES work(work_key),
        attempt_id INTEGER NOT NULL UNIQUE REFERENCES attempts(attempt_id)
    )""",
}


def canonical_json(value):
    """Encode finite plain JSON values, refusing implicit key/type conversion."""

    def check(item):
        if type(item) is dict:
            for key, child in item.items():
                if type(key) is not str:
                    raise ValueError("JSON object keys must be strings")
                check(child)
        elif type(item) is list:
            for child in item:
                check(child)
        elif type(item) is float:
            if not math.isfinite(item):
                raise ValueError("JSON numbers must be finite")
        elif type(item) not in (str, int, bool, type(None)):
            raise ValueError("expected plain JSON values")

    try:
        check(value)
    except RecursionError as error:
        raise ValueError("JSON data is cyclic or too deeply nested") from error
    text = json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    text.encode("utf-8")
    return text


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _json_load(text):
    value = json.loads(text, object_pairs_hook=_unique_object)
    canonical_json(value)
    return value


def _digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _key(value, name):
    if type(value) is not str or not value.strip():
        raise ValueError(f"{name} must be a nonempty string")
    return value


def _mapping(value):
    if type(value) is not dict or set(value) != _MAPPING_KEYS:
        raise ValueError("manifest entries require exactly the three mapping keys")
    return {
        name: _key(value[name], name)
        for name in ("work_key", "source_key", "occurrence_key")
    }


def _manifest_rows(path):
    """Read one bounded original JSONL record at a time; do not own its source."""
    with Path(path).open("rb") as source:
        ordinal = 0
        while raw := source.readline(_MAX_LINE_BYTES + 1):
            if len(raw) > _MAX_LINE_BYTES:
                raise ValueError("manifest line exceeds 64 KiB")
            yield ordinal, _mapping(_json_load(raw.decode("utf-8"))), raw
            ordinal += 1


def _manifest_identity(path, connection=None):
    raw_hash = hashlib.sha256()
    mapping_hash = hashlib.sha256()
    count = 0
    for ordinal, mapping, raw in _manifest_rows(path):
        raw_hash.update(raw)
        mapping_hash.update(canonical_json(mapping).encode("utf-8") + b"\n")
        if connection is not None:
            connection.execute(
                "INSERT INTO work VALUES (?, ?, ?, ?)",
                (
                    ordinal,
                    mapping["work_key"],
                    mapping["source_key"],
                    mapping["occurrence_key"],
                ),
            )
        count += 1
    return raw_hash.hexdigest(), mapping_hash.hexdigest(), count


def _connect(path):
    connection = sqlite3.connect(
        Path(path).resolve().as_uri() + "?mode=rw",
        uri=True,
        timeout=0,
        isolation_level=None,
    )
    try:
        if connection.execute("PRAGMA journal_mode").fetchone()[0] != "delete":
            raise ValueError("reference ledgers require DELETE journal mode")
        connection.execute("PRAGMA foreign_keys=ON")
        connection.execute("PRAGMA synchronous=FULL")
        if connection.execute("PRAGMA foreign_keys").fetchone() != (
            1,
        ) or connection.execute("PRAGMA synchronous").fetchone() != (2,):
            raise ValueError("required ledger consistency settings are unavailable")
        if (
            connection.execute("PRAGMA locking_mode=EXCLUSIVE").fetchone()[0]
            != "exclusive"
        ):
            raise ValueError("exclusive ledger ownership is unavailable")
        connection.execute("BEGIN EXCLUSIVE")
    except BaseException:
        connection.close()
        raise
    return connection


class ReferenceLedger:
    """An owned connection; close it before relocation, another writer or reopen.

    Started attempts, staged payloads and terminal publication use separate
    transactions. Confirmed failures have the same immutability as other results.
    Failed creation retains the newly created database for caller inspection.
    Caller manifests/query artifacts remain caller-owned. Their checksums express
    consistency, not authenticity or proof that live molecular inputs match them.
    """

    def __init__(self, connection, configuration, query_bytes):
        self._connection = connection
        self._configuration = configuration
        self._context_json = canonical_json(configuration["context"])
        self._query_bytes = query_bytes

    @classmethod
    def create(
        cls, path, *, run_id, query_bytes, context, manifest_path, parent_run_id=None
    ):
        _key(run_id, "run_id")
        if parent_run_id is not None:
            _key(parent_run_id, "parent_run_id")
            if parent_run_id == run_id:
                raise ValueError("a run cannot be its own parent")
        context_text = cls._arguments(query_bytes, context)
        descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        os.close(descriptor)
        connection = _connect(path)
        try:
            for statement in _SCHEMA.values():
                connection.execute(statement)
            connection.execute(f"PRAGMA application_id={_APPLICATION_ID}")
            connection.execute(f"PRAGMA user_version={_VERSION}")
            raw_hash, work_hash, count = _manifest_identity(manifest_path, connection)
            configuration = dict(
                format=_FORMAT,
                run_id=run_id,
                parent_run_id=parent_run_id,
                query_sha256=_digest(query_bytes),
                context=_json_load(context_text),
                manifest_sha256=raw_hash,
                work_sha256=work_hash,
                work_count=count,
            )
            encoded = canonical_json(configuration).encode("utf-8")
            connection.executemany(
                "INSERT INTO metadata VALUES (?, ?)",
                [
                    ("configuration", encoded),
                    ("configuration_sha256", _digest(encoded).encode("ascii")),
                    ("query", query_bytes),
                ],
            )
            connection.commit()
            return cls(connection, configuration, query_bytes)
        except BaseException:
            connection.close()
            raise

    @classmethod
    def open(cls, path, *, query_bytes, context, manifest_path):
        context_text = cls._arguments(query_bytes, context)
        connection = _connect(path)
        try:
            configuration, saved_query = cls._read_configuration(connection)
            if (
                saved_query != query_bytes
                or canonical_json(configuration["context"]) != context_text
            ):
                raise ValueError(
                    "query or execution context is incompatible with this run"
                )
            actual = _manifest_identity(manifest_path)
            expected = tuple(
                configuration[name]
                for name in ("manifest_sha256", "work_sha256", "work_count")
            )
            if actual != expected:
                raise ValueError("manifest is incompatible with this run")
            ledger = cls(connection, configuration, saved_query)
            ledger._verify_records()
            connection.commit()
            return ledger
        except BaseException:
            connection.close()
            raise

    @staticmethod
    def _arguments(query_bytes, context):
        if type(query_bytes) is not bytes or type(context) is not dict:
            raise ValueError("expected exact query bytes and a JSON context object")
        return canonical_json(context)

    @staticmethod
    def _read_configuration(connection):
        if (
            connection.execute("PRAGMA application_id").fetchone()[0] != _APPLICATION_ID
            or connection.execute("PRAGMA user_version").fetchone()[0] != _VERSION
        ):
            raise ValueError("unrecognized ledger format/version")
        if connection.execute("PRAGMA quick_check(1)").fetchone()[0] != "ok":
            raise ValueError("SQLite ledger integrity check failed")
        seen = set()
        for name, kind, statement in connection.execute(
            "SELECT name, type, sql FROM sqlite_master WHERE type IN ('table', 'view', 'trigger')"
        ):
            if kind != "table" or name not in _SCHEMA or statement != _SCHEMA[name]:
                raise ValueError("unrecognized ledger schema")
            seen.add(name)
        if seen != set(_SCHEMA):
            raise ValueError("incomplete ledger schema")
        metadata = {}
        for key, value in connection.execute("SELECT key, value FROM metadata"):
            if (
                key not in {"configuration", "configuration_sha256", "query"}
                or type(value) is not bytes
            ):
                raise ValueError("invalid ledger metadata")
            metadata[key] = value
        if set(metadata) != {"configuration", "configuration_sha256", "query"}:
            raise ValueError("incomplete ledger metadata")
        encoded = metadata["configuration"]
        if _digest(encoded).encode("ascii") != metadata["configuration_sha256"]:
            raise ValueError("configuration checksum mismatch")
        configuration = _json_load(encoded.decode("utf-8"))
        if (
            canonical_json(configuration).encode("utf-8") != encoded
            or type(configuration) is not dict
            or set(configuration) != _CONFIG_KEYS
        ):
            raise ValueError("invalid canonical configuration")
        _key(configuration["run_id"], "run_id")
        parent = configuration["parent_run_id"]
        if parent is not None:
            _key(parent, "parent_run_id")
            if parent == configuration["run_id"]:
                raise ValueError("a run cannot be its own parent")
        if (
            configuration["format"] != _FORMAT
            or type(configuration["context"]) is not dict
            or type(configuration["work_count"]) is not int
            or configuration["work_count"] < 0
        ):
            raise ValueError("invalid ledger configuration")
        if configuration["query_sha256"] != _digest(metadata["query"]):
            raise ValueError("query checksum mismatch")
        return configuration, metadata["query"]

    @property
    def run_id(self):
        return self._configuration["run_id"]

    @property
    def parent_run_id(self):
        return self._configuration["parent_run_id"]

    @property
    def query_bytes(self):
        return self._query_bytes

    @property
    def context(self):
        return _json_load(self._context_json)

    def _db(self):
        if self._connection is None:
            raise ValueError("ledger is closed")
        return self._connection

    @contextmanager
    def _transaction(self):
        connection = self._db()
        connection.execute("BEGIN EXCLUSIVE")
        try:
            yield connection
            connection.commit()
        except BaseException:
            if connection.in_transaction:
                connection.rollback()
            raise

    def expected(self, ordinal):
        if type(ordinal) is not int or ordinal < 0:
            raise ValueError("ordinal must be a nonnegative integer")
        row = (
            self._db()
            .execute(
                "SELECT work_key, source_key, occurrence_key FROM work WHERE ordinal=?",
                (ordinal,),
            )
            .fetchone()
        )
        return (
            None
            if row is None
            else dict(
                zip(("work_key", "source_key", "occurrence_key"), row, strict=True)
            )
        )

    def _work(self, work_key):
        _key(work_key, "work_key")
        row = (
            self._db()
            .execute(
                "SELECT work_key, source_key, occurrence_key FROM work WHERE work_key=?",
                (work_key,),
            )
            .fetchone()
        )
        if row is None:
            raise ValueError("unknown work key")
        return _mapping(
            dict(zip(("work_key", "source_key", "occurrence_key"), row, strict=True))
        )

    def _outcome(self, work_key, payload, digest):
        if (
            type(payload) is not str
            or type(digest) is not str
            or _digest(payload.encode("utf-8")) != digest
        ):
            raise ValueError("staged payload checksum mismatch")
        value = _json_load(payload)
        if (
            canonical_json(value) != payload
            or type(value) is not dict
            or set(value) != _OUTCOME_KEYS
        ):
            raise ValueError("invalid canonical outcome envelope")
        expected = self._work(work_key)
        if any(value[name] != expected[name] for name in _MAPPING_KEYS):
            raise ValueError("outcome source/work mapping mismatch")
        native = value["native_result"]
        if (
            type(native) is not dict
            or native.get("pose_id") != work_key
            or type(native.get("status")) is not str
            or native["status"] not in {"matched", "not_matched", "failed"}
        ):
            raise ValueError("invalid native outcome identity/status")
        score = value["ranking_score"]
        if score is not None and type(score) not in (int, float):
            raise ValueError("ranking score must be finite numeric evidence or None")
        if native["status"] == "failed" and score is not None:
            raise ValueError("failed outcomes must remain unscored")
        if native["status"] != "failed" and (score is None or not 0 <= score <= 1):
            raise ValueError("native nonfailures require a score in [0, 1]")
        _key(value["score_method"], "score_method")
        execution = self._configuration["context"].get("execution", {})
        if type(execution) is not dict:
            raise ValueError("execution context must be a mapping")
        method = execution.get("score_method")
        if (
            method is not None
            and value["score_method"] != _key(method, "score_method") + "@1"
        ):
            raise ValueError("outcome score criterion differs from saved execution")
        return value

    def begin(self, work_key):
        self._work(work_key)
        with self._transaction() as connection:
            if connection.execute(
                "SELECT 1 FROM outcomes WHERE work_key=?", (work_key,)
            ).fetchone():
                raise ValueError("work already has a committed terminal outcome")
            return int(
                connection.execute(
                    "INSERT INTO attempts (work_key) VALUES (?)", (work_key,)
                ).lastrowid
            )

    def _attempt(self, attempt_id):
        if type(attempt_id) is not int or attempt_id < 1:
            raise ValueError("attempt_id must be a positive integer")
        row = (
            self._db()
            .execute(
                "SELECT work_key, payload, digest FROM attempts WHERE attempt_id=?",
                (attempt_id,),
            )
            .fetchone()
        )
        if row is None:
            raise ValueError("unknown attempt")
        return row

    def stage(self, attempt_id, outcome):
        payload = canonical_json(outcome)
        digest = _digest(payload.encode("utf-8"))
        with self._transaction() as connection:
            work_key, previous, previous_digest = self._attempt(attempt_id)
            self._outcome(work_key, payload, digest)
            if previous is not None:
                self._outcome(work_key, previous, previous_digest)
                if (payload, digest) != (previous, previous_digest):
                    raise ValueError("attempt already has a different staged payload")
            else:
                connection.execute(
                    "UPDATE attempts SET payload=?, digest=? WHERE attempt_id=?",
                    (payload, digest, attempt_id),
                )

    def publish(self, attempt_id):
        with self._transaction() as connection:
            work_key, payload, digest = self._attempt(attempt_id)
            self._outcome(work_key, payload, digest)
            previous = connection.execute(
                "SELECT a.payload, a.digest FROM outcomes o JOIN attempts a ON a.attempt_id=o.attempt_id WHERE o.work_key=?",
                (work_key,),
            ).fetchone()
            if previous is not None:
                self._outcome(work_key, *previous)
                if previous != (payload, digest):
                    raise ValueError("conflicting committed outcome")
                return False
            connection.execute(
                "INSERT INTO outcomes VALUES (?, ?)", (work_key, attempt_id)
            )
            connection.execute(
                "UPDATE attempts SET committed=1 WHERE attempt_id=?", (attempt_id,)
            )
            return True

    def committed(self, work_key):
        self._work(work_key)
        row = (
            self._db()
            .execute(
                "SELECT a.payload, a.digest FROM outcomes o JOIN attempts a ON a.attempt_id=o.attempt_id WHERE o.work_key=?",
                (work_key,),
            )
            .fetchone()
        )
        return None if row is None else self._outcome(work_key, *row)

    def results(self):
        cursor = self._db().execute(
            "SELECT o.work_key, a.payload, a.digest FROM work w JOIN outcomes o ON o.work_key=w.work_key JOIN attempts a ON a.attempt_id=o.attempt_id ORDER BY w.ordinal"
        )
        for work_key, payload, digest in cursor:
            yield self._outcome(work_key, payload, digest)

    def attempts(self, work_key):
        self._work(work_key)
        for attempt_id, payload, committed in self._db().execute(
            "SELECT attempt_id, payload, committed FROM attempts WHERE work_key=? ORDER BY attempt_id",
            (work_key,),
        ):
            yield dict(
                attempt_id=attempt_id,
                work_key=work_key,
                staged=payload is not None,
                committed=bool(committed),
            )

    def _verify_records(self):
        connection = self._db()
        if connection.execute("PRAGMA foreign_key_check").fetchone() is not None:
            raise ValueError("ledger contains invalid references")
        work_hash = hashlib.sha256()
        count = 0
        for ordinal, work_key, source_key, occurrence_key in connection.execute(
            "SELECT ordinal, work_key, source_key, occurrence_key FROM work ORDER BY ordinal"
        ):
            if type(ordinal) is not int or ordinal != count:
                raise ValueError("invalid manifest ordinal sequence")
            mapping = _mapping(
                dict(
                    work_key=work_key,
                    source_key=source_key,
                    occurrence_key=occurrence_key,
                )
            )
            work_hash.update(canonical_json(mapping).encode("utf-8") + b"\n")
            count += 1
        if (
            count != self._configuration["work_count"]
            or work_hash.hexdigest() != self._configuration["work_sha256"]
        ):
            raise ValueError("stored work mapping checksum mismatch")
        for (
            attempt_id,
            work_key,
            payload,
            digest,
            committed,
            published_key,
        ) in connection.execute(
            "SELECT a.attempt_id, a.work_key, a.payload, a.digest, a.committed, o.work_key FROM attempts a LEFT JOIN outcomes o ON o.attempt_id=a.attempt_id"
        ):
            if (
                type(attempt_id) is not int
                or attempt_id < 1
                or type(committed) is not int
                or committed not in (0, 1)
            ):
                raise ValueError("invalid attempt metadata")
            self._work(work_key)
            if (
                (payload is None) != (digest is None)
                or bool(committed) != (published_key is not None)
                or (published_key is not None and published_key != work_key)
            ):
                raise ValueError("inconsistent attempt/publication metadata")
            if payload is not None:
                self._outcome(work_key, payload, digest)
        for work_key, payload, digest in connection.execute(
            "SELECT o.work_key, a.payload, a.digest FROM outcomes o JOIN attempts a ON a.attempt_id=o.attempt_id"
        ):
            self._outcome(work_key, payload, digest)

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def __enter__(self):
        self._db()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class ReferenceRunView:
    """Read historical reference evidence without resuming or recalculating it.

    The reader owns a read-only SQLite snapshot until closed. Close the ledger's
    exclusive writer before opening a view, and close the view before resuming.
    Opening verifies every stored record and attempt, including unpublished work.
    Ranking scans committed outcomes and retains at most ``limit`` payloads;
    this is not an index or a constant-time progress operation.
    """

    def __init__(self, ledger):
        self._ledger = ledger

    @classmethod
    def open(cls, path):
        connection = sqlite3.connect(
            Path(path).resolve().as_uri() + "?mode=ro",
            uri=True,
            timeout=0,
            isolation_level=None,
        )
        try:
            connection.execute("PRAGMA query_only=ON")
            if connection.execute("PRAGMA query_only").fetchone() != (1,):
                raise ValueError("read-only ledger inspection is unavailable")
            if connection.execute("PRAGMA journal_mode").fetchone() != ("delete",):
                raise ValueError("reference ledgers require DELETE journal mode")
            connection.execute("BEGIN")
            configuration, query_bytes = ReferenceLedger._read_configuration(connection)
            ledger = ReferenceLedger(connection, configuration, query_bytes)
            ledger._verify_records()
            return cls(ledger)
        except BaseException:
            connection.close()
            raise

    @property
    def configuration(self):
        """Detach original producer context; do not compare current providers."""
        self._ledger._db()
        return _json_load(canonical_json(self._ledger._configuration))

    @property
    def query_bytes(self):
        self._ledger._db()
        return self._ledger.query_bytes

    def results(self):
        """Yield full saved terminal outcomes in manifest order, including failures."""
        yield from self._ledger.results()

    def summary(self, *, score_method):
        """Count declared work and publication coverage under one saved criterion."""
        return self._inspect(score_method, limit=0)["summary"]

    def top_results(self, *, score_method, limit):
        """Select observed scored work, retaining negatives and stable ordinal ties."""
        if type(limit) is not int or limit < 0:
            raise ValueError("limit must be a nonnegative integer")
        return self._inspect(score_method, limit=limit)

    def _inspect(self, score_method, *, limit):
        if type(score_method) is not str or score_method not in {
            "seeded_hit@1",
            "checked_pose_coverage@1",
        }:
            raise ValueError("choose an explicit supported versioned score criterion")
        connection = self._ledger._db()
        configuration = self._ledger._configuration
        execution = configuration["context"].get("execution", {})
        if type(execution) is not dict:
            raise ValueError("execution context must be a mapping")
        declared = execution.get("score_method")
        if (
            declared is not None
            and score_method != _key(declared, "score_method") + "@1"
        ):
            raise ValueError("requested score criterion differs from saved execution")
        counts = dict.fromkeys(
            (
                "committed_work",
                "scored_work",
                "matched_work",
                "not_matched_work",
                "failed_work",
            ),
            0,
        )
        counts["declared_work"] = configuration["work_count"]
        heap = []
        for ordinal, work_key, payload, digest in connection.execute(
            "SELECT w.ordinal, o.work_key, a.payload, a.digest FROM work w "
            "JOIN outcomes o ON o.work_key=w.work_key "
            "JOIN attempts a ON a.attempt_id=o.attempt_id ORDER BY w.ordinal"
        ):
            outcome = self._ledger._outcome(work_key, payload, digest)
            if outcome["score_method"] != score_method:
                raise ValueError("saved outcomes use a different score criterion")
            counts["committed_work"] += 1
            counts[outcome["native_result"]["status"] + "_work"] += 1
            score = outcome["ranking_score"]
            if score is not None:
                counts["scored_work"] += 1
                if limit:
                    # A later ordinal loses a tie; unique ordinals avoid comparing dicts.
                    candidate = (score, -ordinal, outcome)
                    if len(heap) < limit:
                        heapq.heappush(heap, candidate)
                    elif candidate[:2] > heap[0][:2]:
                        heapq.heapreplace(heap, candidate)
        counts["pending_work"] = counts["declared_work"] - counts["committed_work"]
        started, staged, committed = connection.execute(
            "SELECT COUNT(*), COALESCE(SUM(payload IS NOT NULL), 0), "
            "COALESCE(SUM(committed), 0) FROM attempts"
        ).fetchone()
        summary = dict(
            run_id=configuration["run_id"],
            parent_run_id=configuration["parent_run_id"],
            score_method=score_method,
            counts=counts,
            attempts=dict(started=started, staged=staged, committed=committed),
            manifest_work_complete=counts["pending_work"] == 0,
            ranking_scope="observed_scored_work_only",
        )
        return dict(
            summary=summary,
            limit=limit,
            records=[
                dict(manifest_ordinal=-ordinal, outcome=outcome)
                for _, ordinal, outcome in sorted(
                    heap, key=lambda item: (-item[0], -item[1])
                )
            ],
        )

    def close(self):
        self._ledger.close()

    def __enter__(self):
        self._ledger._db()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def main(argv=None):
    """Print a bounded scalar development view; never execute saved code/science."""
    import argparse

    parser = argparse.ArgumentParser(description=ReferenceRunView.__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument(
        "--score-method",
        required=True,
        choices=("seeded_hit@1", "checked_pose_coverage@1"),
    )
    parser.add_argument("--limit", type=int, default=10)
    arguments = parser.parse_args(argv)
    try:
        with ReferenceRunView.open(arguments.ledger) as view:
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
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    except (OSError, ValueError, sqlite3.Error) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
