"""Declaration-only metadata for the first writer-owned archive profile."""

import re

from depdigest import dep_digest

from . import _schema
from ._diagnostics import fail

WRITER_SCHEMA = "pharmacophoremt.feature-archive-writer@1"
ATTEMPT_SCHEMA = "pharmacophoremt.feature-archive-attempt@1"
MAX_RECORDS = _schema.MAX_NATIVE_RECORDS
MAX_REPEATED_BYTES = _schema.MAX_NATIVE_REPEATED_BYTES
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


def descriptor(payload_profile):
    value = _schema.detached(DESCRIPTOR)
    if payload_profile == _schema.NATIVE_PAYLOAD_PROFILE:
        value["schema"] = "pharmacophoremt.feature-archive-writer@2"
        value["payload_profile"] = payload_profile
    elif payload_profile != _schema.SNAPSHOT_PROFILE:
        fail(336)
    return value


def attempt_schema(payload_profile):
    return (
        "pharmacophoremt.feature-archive-attempt@2"
        if payload_profile == _schema.NATIVE_PAYLOAD_PROFILE
        else ATTEMPT_SCHEMA
    )


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
            _decode(
                originals[row["payload_sha256"]],
                row["extraction"],
                native=value["schema"] == _schema.NATIVE_GENERATION_SCHEMA,
            )


@dep_digest("pyunitwizard")
def _decode(raw, extraction, *, native=False):
    if native:
        from ._payload import FeatureInventoryPayload

        payload = FeatureInventoryPayload.from_bytes(
            raw, payload_profile=_schema.NATIVE_PAYLOAD_PROFILE
        )
        if _schema.encoded(payload.describe()) != _schema.encoded(extraction):
            fail(310)
        return payload.to_inventory(required_families=extraction["evaluated_families"])
    from pharmacophoremt._private.feature_snapshot_v1 import decode_snapshot

    return decode_snapshot(raw, extraction)
