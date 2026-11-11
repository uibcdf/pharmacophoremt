"""Detached, immutable native record inputs; no scientific validation passport."""

import hashlib

from argdigest import arg_digest
from smonitor import signal

from . import _native_archive_schema as spec
from . import _schema
from ._diagnostics import fail
from ._payload import FeatureInventoryPayload
from ._record_digestion import config


class FeatureAssetRecord:
    """Caller-owned native record bytes and declared original archive lineage."""

    __slots__ = ("_row_bytes", "_payload_bytes")

    def __init__(self):
        raise TypeError("Use FeatureAssetRecord.from_payload, from_view or incomplete")

    @classmethod
    def _attach(cls, row, raw):
        spec.validate_record(row, raw)
        result = cls.__new__(cls)
        result._row_bytes, result._payload_bytes = _schema.encoded(row), raw
        return result

    @classmethod
    @signal(tags=["feature-asset", "record", "new"])
    @arg_digest(config=config("from_payload"), type_check=False)
    def from_payload(cls, work_key, payload):
        """Assign new work explicitly; preserve native original bytes/producers."""
        raw = payload.to_bytes()
        metadata = FeatureInventoryPayload.from_bytes(
            raw, payload_profile=_schema.NATIVE_PAYLOAD_PROFILE
        ).describe()
        return cls._attach(
            {
                "work_key": work_key,
                "source_key": metadata["parent"]["source_key"],
                "occurrence_key": metadata["parent"]["occurrence_key"],
                "status": "ready",
                "payload_sha256": metadata["payload_sha256"],
                "extraction": metadata,
                "lineage": [],
            },
            raw,
        )

    @classmethod
    @signal(tags=["feature-asset", "record", "borrow"])
    @arg_digest(config=config("from_view"), type_check=False)
    def from_view(cls, view, ordinal, *, expected_generation):
        """Copy one native-v2 occurrence and retain its exact original binding."""
        if view.generation != expected_generation:
            fail(308)
        if view.summary()["schema"] != _schema.NATIVE_GENERATION_SCHEMA:
            fail(336)
        page = view.work_items(offset=ordinal, limit=1)["records"]
        if not page:
            fail(301, argument="ordinal")
        row = page[0]
        returned_ordinal = row.pop("work_ordinal", None)
        if type(returned_ordinal) is not int or returned_ordinal != ordinal:
            fail(335)
        raw = view.snapshot_bytes(ordinal) if row["status"] == "ready" else None
        spec.validate_record(row, raw)
        anchor = {
            "generation": expected_generation,
            "work_ordinal": ordinal,
            "record_sha256": hashlib.sha256(_schema.encoded(row)).hexdigest(),
            **{k: row[k] for k in spec.KEYS},
        }
        row["lineage"].append(anchor)
        if view.generation != expected_generation:
            fail(308)
        return cls._attach(row, raw)

    @classmethod
    @signal(tags=["feature-asset", "record", "incomplete"])
    @arg_digest(config=config("incomplete"), type_check=False)
    def incomplete(cls, work_key, source_key, occurrence_key, *, status, cause):
        """Keep failed/partial/unsupported/unattempted evidence distinct from empty."""
        return cls._attach(
            {
                "work_key": work_key,
                "source_key": source_key,
                "occurrence_key": occurrence_key,
                "status": status,
                "cause": cause,
                "lineage": [],
            },
            None,
        )

    @signal(tags=["feature-asset", "record", "metadata"])
    @arg_digest(config=config("describe"), type_check=False)
    def describe(self):
        """Return a fresh detached structurally checked row, with no new ordinal."""
        row = _schema.json_document(self._row_bytes)
        spec.validate_record(row, self._payload_bytes)
        return row

    @signal(tags=["feature-asset", "record", "bytes"])
    @arg_digest(config=config("payload_bytes"), type_check=False)
    def payload_bytes(self):
        """Original native bytes, or None for incomplete evidence; no decoding."""
        return self._payload_bytes


FeatureAssetRecord.__module__ = "pharmacophoremt_features"
