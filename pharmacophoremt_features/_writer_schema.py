"""Declaration-only metadata for the first writer-owned archive profile."""

import re

from depdigest import dep_digest

from . import _schema
from ._diagnostics import fail

WRITER_SCHEMA = "pharmacophoremt.feature-archive-writer@1"
ATTEMPT_SCHEMA = "pharmacophoremt.feature-archive-attempt@1"
MAX_RECORDS = 64
MAX_REPEATED_BYTES = 8 * 1024 * 1024
MAX_ATTEMPTS = 64
DESCRIPTOR = {
    "schema": WRITER_SCHEMA,
    "profile": "local-posix-bounded@1",
    "payload_profile": _schema.SNAPSHOT_PROFILE,
    "limits": {
        "records": MAX_RECORDS,
        "repeated_original_bytes": MAX_REPEATED_BYTES,
        "attempts": MAX_ATTEMPTS,
    },
}


def attempt_id(value, *, argument=False):
    if type(value) is not str or not re.fullmatch("[a-f0-9]{32}", value):
        fail(301 if argument else 325, argument="attempt" if argument else None)
    return value


def limits(value, originals):
    if len(value["records"]) > MAX_RECORDS:
        fail(313)
    total = sum(
        len(originals[r["payload_sha256"]])
        for r in value["records"]
        if r["status"] == "ready"
    )
    if total > MAX_REPEATED_BYTES:
        fail(313)


def validate_native(value, originals, *, complete=False):
    """Activate only the existing scientific owner, never a study decoder."""
    limits(value, originals)
    if complete and any(r["status"] != "ready" for r in value["records"]):
        fail(326)
    for row in value["records"]:
        if row["status"] == "ready":
            _decode(originals[row["payload_sha256"]], row["extraction"])


@dep_digest("pyunitwizard")
def _decode(raw, extraction):
    from pharmacophoremt._private.feature_snapshot_v1 import decode_snapshot

    return decode_snapshot(raw, extraction)
