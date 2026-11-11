"""Owned native payload bytes with cold metadata and explicit scientific use."""

import hashlib

from argdigest import arg_digest
from depdigest import dep_digest
from smonitor import signal

from . import _payload_schema as spec
from ._diagnostics import fail
from ._payload_digestion import config


class FeatureInventoryPayload:
    """A complete captured native inventory, with independently checked readers.

    Parsing and metadata inspection check structure/bytes only. Native reads
    validate every quantity/feature afresh; no mutable flag grants admission.
    This object owns bytes, no file handles or molecular sources.
    """

    __slots__ = ("_raw",)

    def __init__(self):
        raise TypeError("Use FeatureInventoryPayload.from_inventory or from_bytes")

    @classmethod
    @signal(tags=["feature-payload", "encode"])
    @arg_digest(config=config("from_inventory"), type_check=False)
    @dep_digest("pyunitwizard")
    def from_inventory(
        cls,
        inventory,
        evaluated_families,
        *,
        parent,
        extraction_producer,
        payload_profile,
    ):
        """Encode a complete captured inventory with explicit evaluation/source declarations.

        ``native-classical-v1`` is required. Original extraction producer may
        explicitly be None (unknown). No extraction or attribution registration
        runs. The result is reconstructed through the native validator before
        returning; caller objects are never mutated.
        """
        from pharmacophoremt._private.native_feature_payload import encode

        result = cls.__new__(cls)
        result._raw = encode(inventory, evaluated_families, parent, extraction_producer)
        return result

    @classmethod
    @signal(tags=["feature-payload", "read"])
    @arg_digest(config=config("from_bytes"), type_check=False)
    def from_bytes(cls, raw, *, payload_profile):
        """Verify new-profile structure/byte integrity; leave quantities uninterpreted."""
        spec.document(raw)
        result = cls.__new__(cls)
        result._raw = raw
        return result

    @signal(tags=["feature-payload", "bytes"])
    @arg_digest(config=config("to_bytes"), type_check=False)
    def to_bytes(self):
        """Return original immutable bytes for caller-owned storage or transport."""
        return self._raw

    @signal(tags=["feature-payload", "metadata"])
    @arg_digest(config=config("describe"), type_check=False)
    def describe(self):
        """Return detached cold metadata; never a scientific validation passport."""
        payload = spec.document(self._raw)
        return {
            "schema": spec.SCHEMA,
            "payload_profile": spec.PAYLOAD_PROFILE,
            "payload_sha256": hashlib.sha256(self._raw).hexdigest(),
            "payload_bytes": len(self._raw),
            **{
                key: payload[key]
                for key in (
                    "parent",
                    "evaluated_families",
                    "coverage",
                    "extraction_producer",
                    "serialization",
                )
            },
            "definition": payload["inventory"]["definition"],
            "selected_atom_indices": payload["inventory"]["selected_atom_indices"],
            "structure_index": payload["inventory"]["structure_index"],
            "chemical_state": payload["inventory"]["chemical_state"],
            "coverage_authority": "caller-declared evaluation; counts checked against stored features",
            "quantity_semantics_checked": False,
            "molecular_origin_authenticated": False,
            "query_admitted": None,
            "match_outcome": None,
        }

    @signal(tags=["feature-payload", "native-read"])
    @arg_digest(config=config("to_inventory"), type_check=False)
    @dep_digest("pyunitwizard")
    def to_inventory(self, *, required_families):
        """Reconstruct every feature afresh; refuse families without evaluation evidence."""
        payload = spec.document(self._raw)
        if not set(required_families) <= set(payload["evaluated_families"]):
            fail(334)
        from pharmacophoremt._private.native_feature_payload import decode

        return decode(payload)


FeatureInventoryPayload.__module__ = "pharmacophoremt_features"
