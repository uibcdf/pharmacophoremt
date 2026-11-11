"""Read one bounded local POSIX archive; no writer, lock or format migration."""

import hashlib
import os
import stat

from . import _schema
from ._diagnostics import FeatureAssetError, fail


def _read(path, maximum):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, "rb") as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= maximum:
            fail(302)
        raw = stream.read(maximum + 1)
    if len(raw) != info.st_size or len(raw) > maximum:
        fail(302)
    return raw


def read_generation(root, expected):
    if not all(hasattr(os, name) for name in ("O_NOFOLLOW", "O_NONBLOCK")):
        fail(307)
    try:
        if not stat.S_ISDIR(root.lstat().st_mode) or not stat.S_ISDIR(
            (root / "generations").lstat().st_mode
        ):
            fail(302)
        marker = _schema.json_document(_read(root / "STORE.json", 4096))
        if marker != _schema.MARKER:
            fail(307)
        pointer = None
        if expected is None:
            pointer = _schema.json_document(_read(root / "CURRENT", 4096))
            if (
                type(pointer) is not dict
                or set(pointer) != {"schema", "generation", "bytes"}
                or pointer["schema"] != _schema.STORE_SCHEMA
            ):
                fail(302)
            _schema.digest(pointer["generation"])
            if (
                type(pointer["bytes"]) is not int
                or not 0 < pointer["bytes"] <= _schema.MAX_DOCUMENT_BYTES
            ):
                fail(302)
            expected = pointer["generation"]
        raw = _read(
            root / "generations" / (expected + ".json"), _schema.MAX_DOCUMENT_BYTES
        )
        if hashlib.sha256(raw).hexdigest() != expected or (
            pointer is not None and pointer["bytes"] != len(raw)
        ):
            fail(302)
        value, originals = _schema.generation(raw)
        return expected, value, originals, len(raw)
    except FeatureAssetError:
        raise
    except OSError as error:
        raise FeatureAssetError(code="PHMT-E303") from error
    except (ValueError, RecursionError) as error:
        raise FeatureAssetError(code="PHMT-E302") from error
