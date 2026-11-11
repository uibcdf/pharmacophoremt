"""Public read-only view of declared feature evidence and original opaque bytes."""

from collections import Counter

from argdigest import arg_digest
from smonitor import signal

from . import _schema, _storage
from ._diagnostics import fail
from ._digestion import config


class FeatureAssetView:
    """A detached, pinned metadata archive; quantities and payloads are uninterpreted.

    The supported bounded local profile verifies metadata structure and original
    byte integrity. Counts are producer declarations, not recalculated features,
    source authentication, query admission or biological negative evidence.
    """

    def __init__(self):
        raise TypeError("Use FeatureAssetView.open(path)")

    @classmethod
    @signal(tags=["feature-asset", "open"])
    @arg_digest(config=config("open"), type_check=False)
    def open(cls, path, *, generation=None):
        """Read an existing public archive, resolving current once unless pinned.

        No creation, migration, payload decoding or molecular access occurs.
        The caller owns a trusted local directory; hostile ancestors, network
        filesystems, distributed atomicity and power-loss durability are not
        guaranteed by this reader. Raw study stores are not accepted.
        """
        identity, metadata, originals, size = _storage.read_generation(path, generation)
        result = cls.__new__(cls)
        result._identity, result._metadata, result._originals, result._size = (
            identity,
            metadata,
            originals,
            size,
        )
        return result

    def _open(self):
        if self._metadata is None:
            fail(304)

    def _selected(self, work_keys):
        self._open()
        rows = self._metadata["records"]
        selected = None if work_keys is None else set(work_keys)
        if selected is not None and selected - {r["work_key"] for r in rows}:
            fail(305)
        return [
            (i, row)
            for i, row in enumerate(rows)
            if selected is None or row["work_key"] in selected
        ]

    @property
    @signal(tags=["feature-asset", "identity"])
    @arg_digest(config=config("generation"), type_check=False)
    def generation(self):
        """The immutable generation pinned by this open view."""
        self._open()
        return self._identity

    @signal(tags=["feature-asset", "summary"])
    @arg_digest(config=config("summary"), type_check=False)
    def summary(self):
        """Return detached counts and explicit metadata/payload validation scope."""
        self._open()
        counts = Counter(r["status"] for r in self._metadata["records"])
        return {
            "schema": _schema.GENERATION_SCHEMA,
            "profile": _schema.PROFILE,
            "generation": self._identity,
            "origin": _schema.detached(self._metadata["origin"]),
            "record_count": len(self._metadata["records"]),
            "status_counts": {k: counts[k] for k in _schema.STATES},
            "complete": counts["ready"] == len(self._metadata["records"]),
            "unique_payload_count": len(self._originals),
            "archive_bytes": self._size,
            "coverage_authority": "producer-declared extraction metadata",
            "original_payloads_interpreted": False,
            "quantity_semantics_checked": False,
            "molecular_origin_authenticated": False,
            "query_admitted": None,
            "match_outcome": None,
            "persisted_lookup_index": False,
        }

    @signal(tags=["feature-asset", "page"])
    @arg_digest(config=config("work_items"), type_check=False)
    def work_items(self, *, work_keys=None, offset=0, limit=100):
        """Page selected metadata, preserving global ordinals and full counts.

        Keys are exact and selection follows original manifest order. None
        selects all; [] selects none. Unknown keys refuse. Offset is relative to
        the selection, not the original manifest. A zero limit is count-only:
        it has no next_offset and never claims an empty selected corpus.
        """
        selected = self._selected(work_keys)
        page = selected[offset : offset + limit]
        end = offset + len(page)
        return {
            "generation": self._identity,
            "selected_count": len(selected),
            "returned_count": len(page),
            "offset": offset,
            "limit": limit,
            "has_more": end < len(selected),
            "next_offset": end if limit and end < len(selected) else None,
            "records": [
                {"work_ordinal": i, **_schema.detached(row)} for i, row in page
            ],
        }

    @signal(tags=["feature-asset", "original"])
    @arg_digest(config=config("snapshot_bytes"), type_check=False)
    def snapshot_bytes(self, ordinal):
        """Return completed original opaque bytes at one global manifest ordinal.

        This checks byte integrity and metadata availability, not the original
        format's semantics or quantities. Treat originals as caller-controlled
        data; they may contain geometry and private producer information.
        """
        self._open()
        if ordinal >= len(self._metadata["records"]):
            fail(301, argument="ordinal")
        row = self._metadata["records"][ordinal]
        if row["status"] != "ready":
            fail(306)
        return self._originals[row["payload_sha256"]]

    @signal(tags=["feature-asset", "coverage"])
    @arg_digest(config=config("inspect"), type_check=False)
    def inspect(self, required_families, *, work_keys=None):
        """Inspect declared family evaluation; do not interpret original payloads."""
        selected = self._selected(work_keys)
        rows = []
        for ordinal, row in selected:
            item = {"work_ordinal": ordinal, **_schema.detached(row)}
            if row["status"] == "ready":
                coverage = row["extraction"]["coverage"]
                item["declared_counts"] = {
                    k: coverage[k]["count"] for k in required_families if k in coverage
                }
                item["unobserved_families"] = [
                    k for k in required_families if k not in coverage
                ]
            rows.append(item)
        if any(r["status"] != "ready" for r in rows):
            action, message = (
                "resolve_incomplete_extraction",
                "Inspect the original incomplete extraction causes before requesting new work.",
            )
        elif any(r["unobserved_families"] for r in rows):
            action, message = (
                "evaluate_missing_families",
                "Request the missing family evaluation explicitly; it is not a negative result.",
            )
        elif rows:
            action, message = (
                "payload_validation_required",
                "Use a qualified decoder to validate original quantities and geometry before scientific reuse.",
            )
        else:
            action, message = (
                "empty_selection",
                "This explicit selection has no occurrences; no source-level negative follows.",
            )
        return {
            "generation": self._identity,
            "scope": "captured-inventory-only",
            "coverage_authority": "producer-declared extraction metadata",
            "manifest_complete": all(
                r["status"] == "ready" for r in self._metadata["records"]
            ),
            "required_families": list(required_families),
            "selected_count": len(rows),
            "selection_ordinals": [r["work_ordinal"] for r in rows],
            "records": rows,
            "decision": {"action": action, "message": message},
            "original_payloads_interpreted": False,
            "quantity_semantics_checked": False,
            "molecular_origin_authenticated": False,
            "query_admitted": None,
            "match_outcome": None,
        }

    @signal(tags=["feature-asset", "close"])
    @arg_digest(config=config("close"), type_check=False)
    def close(self):
        """Drop owned detached data; repeated close is safe."""
        self._metadata = self._originals = None

    def __enter__(self):
        self._open()
        return self

    def __exit__(self, *args):
        self.close()
