"""Cold native-v2 record identity, bounded lineage and payload metadata binding."""

import hashlib

from . import _schema
from ._diagnostics import FeatureAssetError, fail

MAX_LINEAGE = 16
ORDINAL_POLICIES = ("preserve-original@1", "explicit-rebase@1")
ASSEMBLY_POLICY = "explicit-native-record-assembly@1"
COPY_POLICY = "explicit-original-generation-copy@1"
KEYS = ("work_key", "source_key", "occurrence_key")


def require(condition):
    if not condition:
        fail(335)


def _text(value, maximum=512):
    try:
        _schema.text(value, maximum)
    except (FeatureAssetError, UnicodeError) as error:
        raise FeatureAssetError(code="PHMT-E335") from error


def _digest(value):
    try:
        return _schema.digest(value)
    except FeatureAssetError as error:
        raise FeatureAssetError(code="PHMT-E335") from error


def validate_record(row, raw, *, metadata=None):
    """Recheck a whole native record; sealed quantities remain uninterpreted."""
    require(
        type(row) is dict
        and type(row.get("status")) is str
        and row["status"] in _schema.STATES
    )
    ready = row["status"] == "ready"
    extra = {"payload_sha256", "extraction"} if ready else {"cause"}
    require(set(row) == set(KEYS) | {"status", "lineage"} | extra)
    for key in KEYS:
        _text(row[key])
    lineage = row["lineage"]
    require(type(lineage) is list)
    if len(lineage) > MAX_LINEAGE:
        fail(338)
    seen = set()
    for anchor in lineage:
        require(
            type(anchor) is dict
            and set(anchor)
            == set(KEYS) | {"generation", "work_ordinal", "record_sha256"}
        )
        _digest(anchor["generation"])
        _digest(anchor["record_sha256"])
        require(
            type(anchor["work_ordinal"]) is int
            and 0 <= anchor["work_ordinal"] < _schema.MAX_NATIVE_RECORDS
        )
        require(all(type(anchor[k]) is str and anchor[k] == row[k] for k in KEYS))
        identity = (anchor["generation"], anchor["work_ordinal"])
        require(identity not in seen)
        seen.add(identity)
    if ready:
        require(type(raw) is bytes and bool(raw))
        digest = _digest(row["payload_sha256"])
        require(hashlib.sha256(raw).hexdigest() == digest)
        if metadata is None:
            from ._payload import FeatureInventoryPayload

            metadata = FeatureInventoryPayload.from_bytes(
                raw, payload_profile=_schema.NATIVE_PAYLOAD_PROFILE
            ).describe()
        require(_schema.encoded(row["extraction"]) == _schema.encoded(metadata))
        require(
            all(
                row[k] == metadata["parent"][k]
                for k in ("source_key", "occurrence_key")
            )
        )
    else:
        require(raw is None)
        cause = row["cause"]
        require(type(cause) is dict and set(cause) == {"type", "reason"})
        for value in cause.values():
            _text(value, 2048)


def generation(value):
    require(set(value) == {"schema", "profile", "origin", "records", "payloads"})
    if (
        value["schema"] != _schema.NATIVE_GENERATION_SCHEMA
        or value["profile"] != _schema.NATIVE_PROFILE
    ):
        fail(307)
    origin = value["origin"]
    require(type(origin) is dict)
    if origin.get("policy") == ASSEMBLY_POLICY:
        require(set(origin) == {"policy", "ordinal_policy"})
        require(
            type(origin["ordinal_policy"]) is str
            and origin["ordinal_policy"] in ORDINAL_POLICIES
        )
        preserve = origin["ordinal_policy"] == ORDINAL_POLICIES[0]
    else:
        require(set(origin) == {"policy", "format", "generation"})
        require(
            origin["policy"] == COPY_POLICY
            and origin["format"] == _schema.NATIVE_GENERATION_SCHEMA
        )
        _digest(origin["generation"])
        preserve = False  # Whole-copy origin retains every existing ordinal.
    rows = value["records"]
    require(type(rows) is list)
    if len(rows) > _schema.MAX_NATIVE_RECORDS:
        fail(313)
    require(type(value["payloads"]) is dict)
    if len(value["payloads"]) > _schema.MAX_NATIVE_RECORDS:
        fail(313)
    originals = _schema.decode_originals(value["payloads"])
    repeated = 0
    for row in rows:
        require(type(row) is dict)
        if row.get("status") == "ready":
            digest = _digest(row.get("payload_sha256"))
            require(digest in originals)
            repeated += len(originals[digest])
            if repeated > _schema.MAX_NATIVE_REPEATED_BYTES:
                fail(313)
    from ._payload import FeatureInventoryPayload
    from ._payload_schema import SCHEMA as PAYLOAD_SCHEMA

    metadata = {}
    for digest, raw in originals.items():
        if value["payloads"][digest]["format"] != PAYLOAD_SCHEMA:
            fail(336)
        metadata[digest] = FeatureInventoryPayload.from_bytes(
            raw, payload_profile=_schema.NATIVE_PAYLOAD_PROFILE
        ).describe()
    used, keys = set(), set()
    for ordinal, row in enumerate(rows):
        require(type(row) is dict)
        digest = row.get("payload_sha256")
        if row.get("status") == "ready":
            _digest(digest)
            require(digest in originals)
            used.add(digest)
        validate_record(
            row,
            originals[digest] if row.get("status") == "ready" else None,
            metadata=metadata[digest] if row.get("status") == "ready" else None,
        )
        require(row["work_key"] not in keys)
        keys.add(row["work_key"])
        if (
            preserve
            and row["lineage"]
            and row["lineage"][-1]["work_ordinal"] != ordinal
        ):
            fail(337)
    require(used == set(originals))
    return value, originals
