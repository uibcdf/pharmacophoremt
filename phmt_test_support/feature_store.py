"""Bounded POSIX feature-store study; unshipped, with no persisted lookup index.

The caller owns a trusted local directory. Cooperating writers hold one flock;
readers detach one verified generation. No hostile-filesystem, power-loss,
network-filesystem, molecular-authentication or public-format guarantee is made.
"""

import base64
import fcntl
import hashlib
import json
import os
import re
import stat
import tempfile
import uuid
from pathlib import Path

from phmt_test_support.feature_snapshot import MAX_BYTES, FeatureSnapshotStudy

SCHEMA = "pharmacophoremt.feature-store-study@1"
MAX_BUNDLE = 4 * 1024 * 1024
MAX_RECORDS = 12
MAX_ATTEMPTS = 64
STATES = {"ready", "failed", "partial", "unsupported", "unattempted"}
MARKER = {"schema": SCHEMA, "profile": "local-posix-detached@1"}


def _encode(value):
    from pharmacophoremt_results import canonical_json

    return canonical_json(value).encode("utf-8")


def _json(raw):
    value = json.loads(raw)
    if _encode(value) != raw:
        raise ValueError("Noncanonical store document")
    return value


def _hash(raw):
    return hashlib.sha256(raw).hexdigest()


def _digest(value):
    if type(value) is not str or not re.fullmatch("[a-f0-9]{64}", value):
        raise ValueError("Expected a literal SHA-256 generation/payload name")
    return value


def _text(value, maximum=512):
    if type(value) is not str or not value or len(value.encode()) > maximum:
        raise ValueError("Expected bounded nonempty literal text")


def _directory(path):
    if not stat.S_ISDIR(path.lstat().st_mode):
        raise ValueError("Store directories must be real directories")


def _read(path, maximum):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= maximum:
            raise ValueError("Expected a bounded nonempty regular store file")
        raw = stream.read(maximum + 1)
    if len(raw) != info.st_size or len(raw) > maximum:
        raise ValueError("Store file size changed or exceeded its bound")
    return raw


def _install(path, raw, replace=False):
    # Same-directory staging. Exclusive link never overwrites a sealed generation.
    fd, name = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
        if replace:
            os.replace(temporary, path)
        else:
            try:
                os.link(temporary, path)
            except FileExistsError:
                if _read(path, len(raw)) != raw:
                    raise ValueError(
                        "Existing immutable store file conflicts"
                    ) from None
    finally:
        temporary.unlink(missing_ok=True)


def _record(row):
    base = {"work_key", "source_key", "occurrence_key", "status"}
    if (
        type(row) is not dict
        or type(row.get("status")) is not str
        or row["status"] not in STATES
    ):
        raise ValueError("Declare an explicit extraction status")
    extra = {"snapshot_sha256"} if row["status"] == "ready" else {"cause"}
    if set(row) != base | extra:
        raise ValueError("Unsupported manifest record fields")
    for name in ("work_key", "source_key", "occurrence_key"):
        _text(row[name])
    if row["status"] == "ready":
        _digest(row["snapshot_sha256"])
    else:
        if type(row["cause"]) is not dict or set(row["cause"]) != {"type", "reason"}:
            raise ValueError("Preserve the explicit incomplete extraction cause")
        for value in row["cause"].values():
            _text(value, 2048)


def _bundle(raw, quantities=False):
    if type(raw) is not bytes or not 0 < len(raw) <= MAX_BUNDLE:
        raise ValueError("Feature bundle exceeds its finite bound")
    value = _json(raw)
    if (
        type(value) is not dict
        or set(value) != {"schema", "records", "payloads"}
        or value["schema"] != SCHEMA
        or type(value["records"]) is not list
        or len(value["records"]) > MAX_RECORDS
        or type(value["payloads"]) is not dict
        or len(value["payloads"]) > MAX_RECORDS
    ):
        raise ValueError("Unsupported bounded feature bundle")
    payloads = {}
    for digest, encoded in value["payloads"].items():
        _digest(digest)
        if type(encoded) is not str or len(encoded) > 4 * ((MAX_BYTES + 2) // 3):
            raise ValueError("Invalid bounded base64 payload")
        original = base64.b64decode(encoded, validate=True)
        if (
            base64.b64encode(original).decode("ascii") != encoded
            or _hash(original) != digest
        ):
            raise ValueError("Original payload hash/encoding mismatch")
        snapshot = FeatureSnapshotStudy(original)
        if quantities:
            snapshot.decode_inventory()
        payloads[digest] = original
    keys, used, total = set(), set(), 0
    for row in value["records"]:
        _record(row)
        if row["work_key"] in keys:
            raise ValueError("Work keys must remain unique; occurrences may repeat")
        keys.add(row["work_key"])
        if row["status"] != "ready":
            continue
        digest = row["snapshot_sha256"]
        if digest not in payloads:
            raise ValueError("Manifest payload is missing")
        original = payloads[digest]
        parent = FeatureSnapshotStudy(original).describe()["parent"]
        if any(row[k] != parent[k] for k in ("source_key", "occurrence_key")):
            raise ValueError("Manifest must retain sealed parent bindings")
        used.add(digest)
        total += len(original)
    if used != set(payloads) or total > MAX_BYTES:
        raise ValueError("Unused payload or aggregate original bytes exceed 2 MiB")
    return value, payloads


def _layout(root):
    _directory(root)
    for name in ("generations", "attempts"):
        _directory(root / name)
    if _json(_read(root / "STORE.json", 4096)) != MARKER:
        raise ValueError("Unsupported store marker")


def _current(root):
    try:
        value = _json(_read(root / "CURRENT", 4096))
    except FileNotFoundError:
        return None
    if (
        type(value) is not dict
        or set(value) != {"schema", "generation", "bytes"}
        or value["schema"] != SCHEMA
        or type(value["bytes"]) is not int
        or not 0 < value["bytes"] <= MAX_BUNDLE
    ):
        raise ValueError("Unsupported current-generation pointer")
    _digest(value["generation"])
    return value


def _load(root, generation):
    raw = _read(root / "generations" / (_digest(generation) + ".json"), MAX_BUNDLE)
    if _hash(raw) != generation:
        raise ValueError("Generation checksum mismatch")
    return raw


class FeatureStoreReaderStudy:
    """Detached immutable view; opening checks bytes, not quantity semantics."""

    def __init__(self, root, generation=None):
        root = Path(root).absolute()
        _layout(root)
        pointer = _current(root) if generation is None else None
        if generation is None:
            if pointer is None:
                raise ValueError("Store has no published generation")
            generation = pointer["generation"]
        raw = _load(root, generation)
        if pointer is not None and pointer["bytes"] != len(raw):
            raise ValueError("Published generation byte count mismatch")
        value, payloads = _bundle(raw)
        self._value, self._payloads = value, payloads
        self._generation, self._bytes = generation, len(raw)

    def _open(self):
        if self._value is None:
            raise ValueError("Feature-store reader is closed")

    def describe(self):
        self._open()
        return {
            "schema": SCHEMA,
            "generation": self._generation,
            "bundle_bytes": self._bytes,
            "records": json.loads(_encode(self._value["records"])),
            "unique_payloads": len(self._payloads),
            "complete": all(r["status"] == "ready" for r in self._value["records"]),
            "quantity_semantics_validated_by_open": False,
            "molecular_origin_authenticated": False,
            "persisted_lookup_index": False,
            "scope": "captured-inventory-only",
        }

    def snapshot(self, ordinal):
        self._open()
        if type(ordinal) is not int or not 0 <= ordinal < len(self._value["records"]):
            raise ValueError("Expected an original manifest ordinal")
        row = self._value["records"][ordinal]
        if row["status"] != "ready":
            raise ValueError("Occurrence has no completed feature snapshot")
        return self._payloads[row["snapshot_sha256"]]

    def inventory(self, ordinal):
        # Every call performs the public QuantityRecord handshake afresh.
        return FeatureSnapshotStudy(self.snapshot(ordinal)).decode_inventory()

    def entries(self):
        self._open()
        return self._entries()

    def _entries(self):
        ordinal = 0
        while True:
            self._open()
            if ordinal == len(self._value["records"]):
                return
            row = self._value["records"][ordinal]
            result = json.loads(_encode(row))
            if row["status"] == "ready":
                result["snapshot"] = self.snapshot(ordinal)
            ordinal += 1
            yield result

    def close(self):
        self._value = self._payloads = None

    def __enter__(self):
        self._open()
        return self

    def __exit__(self, *args):
        self.close()


class FeatureStoreStudy:
    """One cooperating writer, finite immutable bundles, separate publication."""

    def __init__(self, root, *, create=False):
        if type(create) is not bool:
            raise ValueError("create must be explicit boolean")
        self._root = Path(root).absolute()
        self._fd = None
        if create:
            self._root.mkdir()  # Refuses even an existing empty directory.
            for name in ("generations", "attempts"):
                (self._root / name).mkdir()
            fd = os.open(
                self._root / ".lock", os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600
            )
            os.close(fd)
            _install(self._root / "STORE.json", _encode(MARKER))
        _layout(self._root)
        fd = os.open(self._root / ".lock", os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            if not stat.S_ISREG(os.fstat(fd).st_mode):
                raise ValueError("Writer lease must be a regular file")
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self._fd = fd
            pointer = _current(self._root)
            if pointer is not None:
                with FeatureStoreReaderStudy(self._root):
                    pass
        except BaseException:
            os.close(fd)
            self._fd = None
            raise

    def _open(self):
        if self._fd is None:
            raise ValueError("Feature-store writer is closed")

    def current(self):
        self._open()
        pointer = _current(self._root)
        return None if pointer is None else pointer["generation"]

    def attempts(self):
        self._open()
        names = []
        with os.scandir(self._root / "attempts") as scan:
            for entry in scan:
                if entry.name.startswith(".pending-"):
                    continue
                if not re.fullmatch(
                    "[a-f0-9]{32}\\.(started|terminal)\\.json", entry.name
                ):
                    raise ValueError("Unknown operation receipt")
                names.append(entry.name)
                if len(names) > 2 * MAX_ATTEMPTS:
                    raise ValueError("Operation receipt bound exceeded")
        rows = {}
        for name in sorted(names):
            token, phase, _ = name.split(".")
            record = _json(_read(self._root / "attempts" / name, 8192))
            if type(record) is not dict or record.get("attempt") != token:
                raise ValueError("Operation receipt identity mismatch")
            rows.setdefault(token, {})[phase] = record
        for phases in rows.values():
            if "started" not in phases:
                raise ValueError("Terminal receipt has no started attempt")
        return [
            {
                "attempt": token,
                "state": phases.get("terminal", {}).get("state", "unknown"),
                **phases,
            }
            for token, phases in sorted(rows.items())
        ]

    def _attempt(self, operation, context, retry_of, action):
        self._open()
        previous = self.attempts()
        if len(previous) >= MAX_ATTEMPTS:
            raise ValueError("Study operation limit reached; retain this store")
        if retry_of is not None and retry_of not in {r["attempt"] for r in previous}:
            raise ValueError("retry_of must identify a retained operation attempt")
        token = uuid.uuid4().hex
        base = {
            "schema": SCHEMA,
            "attempt": token,
            "operation": operation,
            "retry_of": retry_of,
            **context,
        }
        directory = self._root / "attempts"
        _install(directory / (token + ".started.json"), _encode(base))
        try:
            result = action()
        except BaseException as error:
            reason = str(error)
            bounded_reason = reason.encode("utf-8")[:2048].decode(
                "utf-8", errors="ignore"
            )
            terminal = {
                **base,
                "state": "raised",
                "exception_type": type(error).__name__,
                "reason": bounded_reason,
                "reason_truncated": len(reason.encode("utf-8")) > 2048,
            }
            try:
                _install(directory / (token + ".terminal.json"), _encode(terminal))
            except Exception as receipt_error:
                error.add_note(
                    "Operation receipt could not be retained: "
                    + type(receipt_error).__name__
                )
            raise
        _install(
            directory / (token + ".terminal.json"),
            _encode({**base, "state": "completed", "result": result}),
        )
        return result

    def seal(self, records, *, retry_of=None):
        self._open()
        if type(records) is not list or len(records) > MAX_RECORDS:
            raise ValueError("Declare at most twelve ordered records as a list")

        def action():
            manifest, payloads, total = [], {}, 0
            for row in records:
                if type(row) is not dict:
                    raise ValueError("Expected a declared manifest record")
                row = dict(row)
                if row.get("status") == "ready":
                    if "snapshot_sha256" in row:
                        raise ValueError(
                            "Pass original bytes, not a claimed payload identity"
                        )
                    original = row.pop("snapshot", None)
                    if (
                        type(original) is not bytes
                        or not 0 < len(original) <= MAX_BYTES
                    ):
                        raise ValueError(
                            "Ready record needs bounded original snapshot bytes"
                        )
                    total += len(original)
                    if total > MAX_BYTES:
                        raise ValueError("Aggregate original bytes exceed 2 MiB")
                    digest = _hash(original)
                    row["snapshot_sha256"] = digest
                    payloads[digest] = base64.b64encode(original).decode("ascii")
                _record(row)
                manifest.append(row)
            raw = _encode({"schema": SCHEMA, "records": manifest, "payloads": payloads})
            _bundle(raw, quantities=True)
            generation = _hash(raw)
            _install(self._root / "generations" / (generation + ".json"), raw)
            return generation

        return self._attempt("seal", {}, retry_of, action)

    def publish(self, generation, *, expected_current, retry_of=None):
        self._open()
        _digest(generation)
        if expected_current is not None:
            _digest(expected_current)

        def action():
            if self.current() != expected_current:
                raise ValueError("Stale expected current generation")
            raw = _load(self._root, generation)
            value, _ = _bundle(raw, quantities=True)
            if any(r["status"] != "ready" for r in value["records"]):
                raise ValueError(
                    "Incomplete manifest cannot replace published generation"
                )
            if self.current() != expected_current:
                raise ValueError("Current generation changed before publication")
            _install(
                self._root / "CURRENT",
                _encode(
                    {"schema": SCHEMA, "generation": generation, "bytes": len(raw)}
                ),
                replace=True,
            )
            return generation

        return self._attempt(
            "publish",
            {"candidate": generation, "expected_current": expected_current},
            retry_of,
            action,
        )

    def close(self):
        if self._fd is not None:
            fd, self._fd = self._fd, None
            os.close(fd)

    def __enter__(self):
        self._open()
        return self

    def __exit__(self, *args):
        self.close()
