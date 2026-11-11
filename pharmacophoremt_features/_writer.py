"""Explicit local writer; scientific validation is activated only for originals."""

import base64
import hashlib
import os
import re
import stat
import tempfile
import threading
import uuid
import weakref
from contextlib import contextmanager
from pathlib import Path

from argdigest import arg_digest
from smonitor import signal

from . import _schema, _storage
from . import _writer_schema as spec
from ._api import FeatureAssetView
from ._diagnostics import FeatureAssetError, fail
from ._writer_digestion import config


@contextmanager
def _io():
    try:
        yield
    except OSError as error:
        raise FeatureAssetError(code="PHMT-E327") from error


def _platform():
    if os.name != "posix" or not all(
        hasattr(os, n) for n in ("O_NOFOLLOW", "O_NONBLOCK")
    ):
        fail(307)
    import fcntl

    return fcntl


def _install(path, raw, *, replace=False):
    """Same-directory atomic replacement or immutable exclusive installation."""
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
                if _storage._read(path, len(raw)) != raw:
                    fail(302)
    finally:
        temporary.unlink(missing_ok=True)


def _descriptor(root):
    marker = _storage.layout(root)
    try:
        if not stat.S_ISDIR((root / "attempts").lstat().st_mode):
            fail(328)
        raw = _storage._read(root / "WRITER.json", 4096)
    except FileNotFoundError as error:
        raise FeatureAssetError(code="PHMT-E328") from error
    value = _schema.json_document(raw)
    if type(value) is not dict or value.get("payload_profile") not in (
        _schema.SNAPSHOT_PROFILE,
        _schema.NATIVE_PAYLOAD_PROFILE,
    ):
        fail(328)
    expected = spec.descriptor(value["payload_profile"])
    if _schema.encoded(value) != _schema.encoded(expected):
        fail(328)
    if marker != _schema.marker(value["payload_profile"]):
        fail(336)
    return value


def _receipt(condition):
    if not condition:
        fail(325)


def _software():
    """Observe writer identity separately from original extraction producers."""
    from importlib.metadata import PackageNotFoundError, version

    try:
        observed = version("pharmacophoremt")
    except PackageNotFoundError:
        observed = None
    try:
        digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    except OSError:
        digest = None
    return {
        "distribution": "pharmacophoremt",
        "distribution_version": observed,
        "observed_writer_sha256": digest,
    }


class FeatureAssetStore:
    """One process-bound cooperating writer over explicitly selected profiles.

    Use explicit create/open, then stage and publish separately. Metadata/receipt
    inspection stays scientifically cold. Ready originals activate their selected
    native/compatibility validator on every stage/publication, without extraction
    credit. Native-v2 records support explicit assembly and retained source lineage.
    Trusted local POSIX filesystems only; no fsync/power-loss or hostile-directory
    guarantee. The caller owns this lease and any detached source/returned views.
    """

    def __init__(self):
        raise TypeError("Use FeatureAssetStore.create(path, ...) or .open(path)")

    @classmethod
    @signal(tags=["feature-asset", "writer", "create"])
    @arg_digest(config=config("create"), type_check=False)
    def create(cls, path, *, payload_profile):
        """Create a new writer-owned archive; refuse even an existing empty path."""
        fcntl = _platform()
        root = path.absolute()
        with _io():
            try:
                root.mkdir(mode=0o700)
            except FileExistsError as error:
                raise FeatureAssetError(code="PHMT-E329") from error
            for name in ("generations", "attempts"):
                (root / name).mkdir(mode=0o700)
            fd = os.open(root / ".lock", os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                _install(
                    root / "WRITER.json",
                    _schema.encoded(spec.descriptor(payload_profile)),
                )
                _install(
                    root / "STORE.json",
                    _schema.encoded(_schema.marker(payload_profile)),
                )
                return cls._attach(root, fd, payload_profile)
            except BaseException:
                os.close(fd)
                raise

    @classmethod
    @signal(tags=["feature-asset", "writer", "open"])
    @arg_digest(config=config("open"), type_check=False)
    def open(cls, path):
        """Acquire an existing writer-owned archive without native decoding."""
        fcntl = _platform()
        root = path.absolute()
        with _io():
            descriptor = _descriptor(root)
            fd = os.open(root / ".lock", os.O_RDWR | os.O_NOFOLLOW | os.O_NONBLOCK)
            try:
                if not stat.S_ISREG(os.fstat(fd).st_mode):
                    fail(328)
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError as error:
                    raise FeatureAssetError(code="PHMT-E320") from error
                return cls._attach(root, fd, descriptor["payload_profile"])
            except BaseException:
                os.close(fd)
                raise

    @classmethod
    def _attach(cls, root, fd, payload_profile):
        result = cls.__new__(cls)
        result._root, result._fd = root, fd
        result._payload_profile = payload_profile
        result._marker = _schema.marker(payload_profile)
        result._pid, result._lock = os.getpid(), threading.RLock()
        result._current()
        result._attempts()
        result._finalizer = weakref.finalize(result, os.close, fd)
        return result

    def _open(self):
        if self._fd is None or os.getpid() != self._pid:
            fail(321)

    @contextmanager
    def _use(self):
        self._open()  # Refuse inherited handles before touching an inherited lock.
        with self._lock, _io():
            self._open()
            yield

    def _current(self):
        try:
            raw = _storage._read(self._root / "CURRENT", 4096)
        except FileNotFoundError:
            return None
        pointer = _schema.json_document(raw)
        if (
            type(pointer) is not dict
            or set(pointer) != {"schema", "generation", "bytes"}
            or pointer["schema"] != self._marker["schema"]
        ):
            fail(302)
        generation = _schema.digest(pointer["generation"])
        _, _, _, size = _storage.read_generation(self._root, generation)
        if type(pointer["bytes"]) is not int or pointer["bytes"] != size:
            fail(302)
        return generation

    @signal(tags=["feature-asset", "writer", "current"])
    @arg_digest(config=config("current"), type_check=False)
    def current(self):
        """Return verified current metadata identity, or None before publication."""
        with self._use():
            return self._current()

    @signal(tags=["feature-asset", "writer", "view"])
    @arg_digest(config=config("view"), type_check=False)
    def view(self, *, generation=None):
        """Return an independent pinned public metadata view, without decoding."""
        with self._use():
            return FeatureAssetView.open(self._root, generation=generation)

    def _attempts(self):
        records, scanned = {}, 0
        with os.scandir(self._root / "attempts") as entries:
            for entry in entries:
                scanned += 1
                if scanned > 4 * spec.MAX_ATTEMPTS:
                    fail(325)
                if entry.name.startswith(".pending-"):
                    continue
                match = re.fullmatch(
                    r"([a-f0-9]{32})\.(started|terminal)\.json", entry.name
                )
                if match is None:
                    fail(325)
                token, phase = match.groups()
                value = _schema.json_document(
                    _storage._read(self._root / "attempts" / entry.name, 8192)
                )
                _receipt(type(value) is dict and value.get("attempt") == token)
                records.setdefault(token, {})[phase] = value
        _receipt(len(records) <= spec.MAX_ATTEMPTS)
        rows = []
        for token, phases in records.items():
            _receipt("started" in phases)
            start = phases["started"]
            common = {
                "schema",
                "attempt",
                "ordinal",
                "operation",
                "retry_of",
                "software",
            }
            operation = start.get("operation")
            allowed = {"stage", "publish"}
            if self._payload_profile == _schema.NATIVE_PAYLOAD_PROFILE:
                allowed.add("stage_records")
            _receipt(type(operation) is str and operation in allowed)
            keys = (
                {"source_generation"}
                if operation == "stage"
                else {"candidate", "record_count", "ordinal_policy"}
                if operation == "stage_records"
                else {"candidate", "expected_current"}
            )
            _receipt(
                set(start) == common | keys
                and start["schema"] == spec.attempt_schema(self._payload_profile)
            )
            _receipt(
                type(start["ordinal"]) is int
                and 0 <= start["ordinal"] < spec.MAX_ATTEMPTS
            )
            software = start["software"]
            _receipt(
                type(software) is dict
                and set(software)
                == {"distribution", "distribution_version", "observed_writer_sha256"}
            )
            _receipt(software["distribution"] == "pharmacophoremt")
            if software["distribution_version"] is not None:
                _schema.text(software["distribution_version"], 128)
            if software["observed_writer_sha256"] is not None:
                _schema.digest(software["observed_writer_sha256"])
            retry = start["retry_of"]
            if retry is not None:
                spec.attempt_id(retry)
                _receipt(operation == "publish")
            if operation == "stage":
                _schema.digest(start["source_generation"])
            elif operation == "stage_records":
                from ._native_archive_schema import ORDINAL_POLICIES

                _schema.digest(start["candidate"])
                _receipt(
                    type(start["record_count"]) is int
                    and 0 <= start["record_count"] <= spec.MAX_RECORDS
                )
                _receipt(
                    type(start["ordinal_policy"]) is str
                    and start["ordinal_policy"] in ORDINAL_POLICIES
                )
            else:
                _schema.digest(start["candidate"])
                if start["expected_current"] is not None:
                    _schema.digest(start["expected_current"])
            state = "unknown"
            terminal = phases.get("terminal")
            if terminal is not None:
                state = terminal.get("state")
                _receipt(type(state) is str and state in {"completed", "raised"})
                extra = (
                    {"result"}
                    if state == "completed"
                    else {"category", "exception_type"}
                )
                _receipt(set(terminal) == set(start) | {"state"} | extra)
                _receipt(
                    _schema.encoded({k: terminal[k] for k in start})
                    == _schema.encoded(start)
                )
                if state == "completed":
                    _schema.digest(terminal["result"])
                    _receipt(
                        operation == "stage" or terminal["result"] == start["candidate"]
                    )
                else:
                    for key in extra:
                        _schema.text(terminal[key], 128)
            rows.append(
                {
                    "attempt": token,
                    "state": state,
                    "started": start,
                    **({"terminal": terminal} if terminal is not None else {}),
                }
            )
        rows.sort(key=lambda r: r["started"]["ordinal"])
        _receipt([r["started"]["ordinal"] for r in rows] == list(range(len(rows))))
        prior = {}
        for row in rows:
            start = row["started"]
            retry = start["retry_of"]
            if retry is not None:
                _receipt(retry in prior)
                original = prior[retry]
                _receipt(
                    original["started"]["operation"] == "publish"
                    and original["state"] != "completed"
                )
                _receipt(
                    all(
                        start[k] == original["started"][k]
                        for k in ("candidate", "expected_current")
                    )
                )
            prior[row["attempt"]] = row
        return rows

    @signal(tags=["feature-asset", "writer", "attempts"])
    @arg_digest(config=config("attempts"), type_check=False)
    def attempts(self):
        """Return bounded validated detached history; missing terminals stay unknown."""
        with self._use():
            return self._attempts()

    def _attempt(self, operation, context, retry_of, action):
        previous = self._attempts()
        if len(previous) >= spec.MAX_ATTEMPTS:
            fail(323)
        token = uuid.uuid4().hex
        start = {
            "schema": spec.attempt_schema(self._payload_profile),
            "attempt": token,
            "ordinal": len(previous),
            "operation": operation,
            "retry_of": retry_of,
            "software": _software(),
            **context,
        }
        directory = self._root / "attempts"
        _install(directory / (token + ".started.json"), _schema.encoded(start))
        try:
            result = action()
        except BaseException as error:
            category = (
                error.code if isinstance(error, FeatureAssetError) else "unclassified"
            )
            terminal = {
                **start,
                "state": "raised",
                "category": category,
                "exception_type": type(error).__name__[:128],
            }
            try:
                _install(
                    directory / (token + ".terminal.json"), _schema.encoded(terminal)
                )
            except Exception:
                error.add_note("The terminal operation receipt could not be retained.")
            raise
        _install(
            directory / (token + ".terminal.json"),
            _schema.encoded({**start, "state": "completed", "result": result}),
        )
        return result

    @signal(tags=["feature-asset", "writer", "stage"])
    @arg_digest(config=config("stage"), type_check=False)
    def stage(self, view, *, expected_generation):
        """Copy a whole borrowed view, validate originals and install a candidate."""
        with self._use():
            if view.generation != expected_generation:
                fail(308)
            summary = view.summary()
            if summary["profile"] != self._marker["profile"]:
                fail(336)
            if view.work_items(limit=0)["selected_count"] > spec.MAX_RECORDS:
                fail(313)

            def action():
                rows, payloads, total = [], {}, 0
                for row in view.work_items(limit=spec.MAX_RECORDS)["records"]:
                    ordinal = row.pop("work_ordinal")
                    if row["status"] == "ready":
                        raw = view.snapshot_bytes(ordinal)
                        total += len(raw)
                        if total > spec.MAX_REPEATED_BYTES:
                            fail(313)
                        info = view.payload_info(ordinal)
                        digest = hashlib.sha256(raw).hexdigest()
                        if (
                            digest != row["payload_sha256"]
                            or info["generation"] != expected_generation
                        ):
                            fail(310)
                        payloads[digest] = {
                            "format": info["format"],
                            "data": base64.b64encode(raw).decode("ascii"),
                        }
                    rows.append(row)
                if view.generation != expected_generation:
                    fail(308)
                generation_schema = summary["schema"]
                value = {
                    "schema": generation_schema,
                    "profile": summary["profile"],
                    "origin": {
                        "format": generation_schema,
                        "generation": expected_generation,
                        "policy": "explicit-original-generation-copy@1",
                    },
                    "records": rows,
                    "payloads": payloads,
                }
                raw = _schema.encoded(value)
                if len(raw) > _schema.MAX_DOCUMENT_BYTES:
                    fail(313)
                value, originals = _schema.generation(raw)
                spec.validate_native(value, originals)
                generation = hashlib.sha256(raw).hexdigest()
                _install(self._root / "generations" / (generation + ".json"), raw)
                return generation

            return self._attempt(
                "stage", {"source_generation": expected_generation}, None, action
            )

    @signal(tags=["feature-asset", "writer", "stage-records"])
    @arg_digest(config=config("stage_records"), type_check=False)
    def stage_records(self, records, *, ordinal_policy="preserve-original@1"):
        """Stage an explicit native record sequence, preserving or explicitly rebasing ordinals.

        Borrowed records retain their original source/global-ordinal anchors.
        Default preservation refuses a moved source position. Reordering/subsets
        require explicit-rebase@1; original lineage is never replaced or trimmed.
        All ready originals validate afresh before immutable installation.
        """
        with self._use():
            if self._payload_profile != _schema.NATIVE_PAYLOAD_PROFILE:
                fail(336)
            from ._native_archive_schema import ASSEMBLY_POLICY
            from ._payload_schema import SCHEMA as PAYLOAD_SCHEMA

            rows, payloads, total, unique = [], {}, 0, 0
            for record in records:
                row = record.describe()
                if row["status"] == "ready":
                    raw = record.payload_bytes()
                    total += len(raw)
                    if total > spec.MAX_REPEATED_BYTES:
                        fail(313)
                    digest = row["payload_sha256"]
                    if digest not in payloads:
                        unique += len(raw)
                        if unique > _schema.MAX_UNIQUE_PAYLOAD_BYTES:
                            fail(313)
                        payloads[digest] = {
                            "format": PAYLOAD_SCHEMA,
                            "data": base64.b64encode(raw).decode("ascii"),
                        }
                rows.append(row)
            raw = _schema.encoded(
                {
                    "schema": _schema.NATIVE_GENERATION_SCHEMA,
                    "profile": _schema.NATIVE_PROFILE,
                    "origin": {
                        "policy": ASSEMBLY_POLICY,
                        "ordinal_policy": ordinal_policy,
                    },
                    "records": rows,
                    "payloads": payloads,
                }
            )
            if len(raw) > _schema.MAX_DOCUMENT_BYTES:
                fail(313)
            candidate = hashlib.sha256(raw).hexdigest()

            def action():
                value, originals = _schema.generation(raw)
                spec.validate_native(value, originals)
                _install(self._root / "generations" / (candidate + ".json"), raw)
                return candidate

            return self._attempt(
                "stage_records",
                {
                    "candidate": candidate,
                    "record_count": len(rows),
                    "ordinal_policy": ordinal_policy,
                },
                None,
                action,
            )

    def _recovery(self, attempt):
        rows = self._attempts()
        by_id = {r["attempt"]: r for r in rows}
        if attempt not in by_id or by_id[attempt]["started"]["operation"] != "publish":
            fail(324)
        original = by_id[attempt]
        start = original["started"]
        current = self._current()
        confirmed_links = []
        for row in rows:
            if row["state"] != "completed":
                continue
            token = row["started"]["retry_of"]
            while token is not None:
                if token == attempt:
                    confirmed_links.append(row["attempt"])
                    break
                token = by_id[token]["started"]["retry_of"]
        if current == start["candidate"]:
            decision = "already_current"
        elif original["state"] == "completed" or confirmed_links:
            decision = "completed_attempt"
        elif current != start["expected_current"]:
            decision = "publication_changed"
        else:
            decision = "retry_available"
        return {
            "attempt": attempt,
            "receipt_state": original["state"],
            "candidate": start["candidate"],
            "expected_current": start["expected_current"],
            "current": current,
            "confirmed_linked_attempts": confirmed_links,
            "candidate_native_validation_performed": False,
            "decision": {"action": decision},
        }

    @signal(tags=["feature-asset", "writer", "recovery"])
    @arg_digest(config=config("inspect_recovery"), type_check=False)
    def inspect_recovery(self, attempt):
        """Inspect actual visibility/receipt state without validation or retry."""
        with self._use():
            return self._recovery(attempt)

    @signal(tags=["feature-asset", "writer", "publish"])
    @arg_digest(config=config("publish"), type_check=False)
    def publish(self, generation, *, expected_current, retry_of=None):
        """Revalidate a complete candidate, then atomically compare and publish."""
        with self._use():
            if retry_of is not None:
                prior = self._recovery(retry_of)
                if (
                    prior["decision"]["action"] != "retry_available"
                    or prior["candidate"] != generation
                    or prior["expected_current"] != expected_current
                ):
                    fail(324)

            def action():
                current = self._current()
                if current != expected_current:
                    fail(322)
                if current == generation:
                    fail(324)
                _, value, originals, size = _storage.read_generation(
                    self._root, generation
                )
                spec.validate_native(value, originals, complete=True)
                if self._current() != expected_current:
                    fail(322)
                pointer = {
                    "schema": self._marker["schema"],
                    "generation": generation,
                    "bytes": size,
                }
                _install(self._root / "CURRENT", _schema.encoded(pointer), replace=True)
                return generation

            return self._attempt(
                "publish",
                {"candidate": generation, "expected_current": expected_current},
                retry_of,
                action,
            )

    @signal(tags=["feature-asset", "writer", "retry"])
    @arg_digest(config=config("retry_publication"), type_check=False)
    def retry_publication(self, attempt):
        """Explicitly link an eligible old publication and revalidate it afresh."""
        with self._use():
            report = self._recovery(attempt)
            if report["decision"]["action"] != "retry_available":
                fail(324)
            return self.publish(
                report["candidate"],
                expected_current=report["expected_current"],
                retry_of=attempt,
            )

    @signal(tags=["feature-asset", "writer", "close"])
    @arg_digest(config=config("close"), type_check=False)
    def close(self):
        """Idempotently close only this descriptor; never unlock a parent's lease."""
        if self._fd is None:
            return
        if os.getpid() != self._pid:
            self._fd = None
            self._finalizer()
            return
        with self._lock, _io():
            if self._fd is not None:
                self._fd = None
                self._finalizer()

    def __enter__(self):
        self._open()
        return self

    def __exit__(self, *args):
        self.close()
