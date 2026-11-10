"""Bounded native capture/inspection study; no supported public snapshot API."""

import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass

SCHEMA = "pharmacophoremt.feature-snapshot-study@1"
PROFILE = "native-classical-single-frame@1"
MAX_BYTES = 2 * 1024 * 1024
FAMILIES = (
    "hydrophobicity",
    "hb donor",
    "hb acceptor",
    "aromatic ring",
    "positive charge",
    "negative charge",
)
PARENT_KEYS = {
    "source_key",
    "occurrence_key",
    "artifact_sha256",
    "artifact_bytes",
    "n_atoms",
    "structure_index",
    "chemical_state",
    "trust",
    "preparation",
}
INVENTORY_KEYS = {
    "definition",
    "features",
    "recognition",
    "selected_atom_indices",
    "structure_index",
    "chemical_state",
}
FEATURE_KEYS = {
    "kind",
    "atom_indices",
    "geometry_atom_indices",
    "center",
    "direction",
    "normal",
    "charge",
}


def _canonical(value):
    # Reuse the supported finite-JSON owner; inspection imports no main PHMT.
    from pharmacophoremt_results import canonical_json

    return canonical_json(value)


def _parent(value):
    if type(value) is not dict or set(value) != PARENT_KEYS:
        raise ValueError("Declare the complete single-artifact parent")
    for key in ("source_key", "occurrence_key", "preparation"):
        if type(value[key]) is not str or not value[key]:
            raise ValueError("Parent text keys must be nonempty literal strings")
    if type(value["artifact_sha256"]) is not str or not re.fullmatch(
        "[a-f0-9]{64}", value["artifact_sha256"]
    ):
        raise ValueError("Declare the original artifact SHA-256")
    if type(value["artifact_bytes"]) is not int or value["artifact_bytes"] <= 0:
        raise ValueError("Declare positive artifact bytes")
    if type(value["n_atoms"]) is not int or not 1 <= value["n_atoms"] <= 256:
        raise ValueError("Study atom count must be in 1..256")
    if any(
        type(value[k]) is not int or value[k] != 0
        for k in ("structure_index", "chemical_state")
    ):
        raise ValueError("Study requires frame 0/state 0")
    if value["trust"] != "caller-verified-artifact/unchanged-source":
        raise ValueError("This profile requires its explicit caller trust precondition")


def _request(features):
    if (
        not isinstance(features, (tuple, list))
        or not features
        or any(type(x) is not str or x not in FAMILIES for x in features)
    ):
        raise ValueError("Explicit nonempty classical family request required")
    return [x for x in FAMILIES if x in features]


def _producer(producer):
    if (
        type(producer) is not dict
        or set(producer) != {"scope", "admission_sha256", "runtime_version", "versions"}
        or producer["scope"] != "selected-case-context"
    ):
        raise ValueError("Explicit selected producer context required")
    if type(producer["admission_sha256"]) is not str or not re.fullmatch(
        "[a-f0-9]{64}", producer["admission_sha256"]
    ):
        raise ValueError("Producer context needs its frozen admission identity")
    if (
        type(producer["runtime_version"]) is not str
        or not producer["runtime_version"]
        or type(producer["versions"]) is not dict
        or not producer["versions"]
        or any(
            type(k) is not str or type(v) is not str or not v
            for k, v in producer["versions"].items()
        )
    ):
        raise ValueError("Record actual producer versions")


def _validate(payload):
    if (
        type(payload) is not dict
        or set(payload)
        != {"profile", "parent", "request", "coverage", "inventory", "producer"}
        or payload["profile"] != PROFILE
    ):
        raise ValueError("Unsupported study snapshot payload/profile")
    parent, request, inventory = (
        payload["parent"],
        payload["request"],
        payload["inventory"],
    )
    _parent(parent)
    if type(request) is not dict or set(request) != {
        "definition",
        "features",
        "selection",
        "structure_index",
        "chemical_state",
        "coordinate_policy",
    }:
        raise ValueError("Unsupported extraction request")
    if (
        request["definition"] != "classical_atomic_formal@1"
        or request["features"] != _request(request["features"])
        or request["selection"] != "all"
        or request["coordinate_policy"] != "cartesian-no-imaging"
    ):
        raise ValueError("Unsupported effective extraction request")
    for key in ("structure_index", "chemical_state"):
        if type(request[key]) is not int or request[key] != parent[key]:
            raise ValueError("Request must retain the original parent frame/state")
    if (
        type(inventory) is not dict
        or not INVENTORY_KEYS <= set(inventory)
        or set(inventory) - INVENTORY_KEYS - {"attribution"}
    ):
        raise ValueError("Expected the native inventory layout, not a partial result")
    if (
        inventory["definition"] != request["definition"]
        or type(inventory["recognition"]) is not dict
    ):
        raise ValueError("Inventory definition/recognition mismatch")
    for key in ("structure_index", "chemical_state"):
        if type(inventory[key]) is not int or inventory[key] != request[key]:
            raise ValueError("Inventory frame/state mismatch")
    selected = list(range(parent["n_atoms"]))
    if inventory["selected_atom_indices"] != selected or any(
        type(i) is not int for i in inventory["selected_atom_indices"]
    ):
        raise ValueError("Study inventory must retain the complete parent atom axis")
    records = inventory["features"]
    if type(records) is not list or len(records) > 64:
        raise ValueError("Study feature count exceeds 64")
    for row in records:
        if (
            type(row) is not dict
            or set(row) != FEATURE_KEYS
            or row["kind"] not in request["features"]
        ):
            raise ValueError("Unknown feature layout or unrequested family")
        for key in ("atom_indices", "geometry_atom_indices"):
            indices = row[key]
            if (
                type(indices) is not list
                or not indices
                or any(type(i) is not int or i not in selected for i in indices)
                or len(set(indices)) != len(indices)
            ):
                raise ValueError(
                    "Original participant/geometry maps must lie in the parent"
                )
        if type(row["center"]) is not dict:
            raise ValueError("Center needs its sealed quantity record")
        for key, required in (
            ("direction", row["kind"] == "hb donor"),
            ("normal", row["kind"] == "aromatic ring"),
            ("charge", row["kind"] in {"positive charge", "negative charge"}),
        ):
            if (type(row[key]) is dict) != required or (
                not required and row[key] is not None
            ):
                raise ValueError("Feature geometry/charge presence mismatch")
    counts = Counter(row["kind"] for row in records)
    expected = {
        kind: {
            "count": counts[kind],
            "status": "completed" if counts[kind] else "evaluated_empty",
        }
        for kind in request["features"]
    }
    if (
        type(payload["coverage"]) is not dict
        or any(
            type(v) is not dict
            or set(v) != {"count", "status"}
            or type(v["count"]) is not int
            for v in payload["coverage"].values()
        )
        or payload["coverage"] != expected
    ):
        raise ValueError("Coverage must retain the complete successful family request")
    _producer(payload["producer"])


def _unpack(raw):
    if type(raw) is not bytes or not 0 < len(raw) <= MAX_BYTES:
        raise ValueError("Expected immutable study bytes up to 2 MiB")
    try:
        text = raw.decode("utf-8")
        envelope = json.loads(text)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise ValueError("Invalid study JSON bytes") from error
    if (
        _canonical(envelope) != text
        or type(envelope) is not dict
        or set(envelope) != {"schema", "payload", "payload_sha256"}
        or envelope["schema"] != SCHEMA
    ):
        raise ValueError("Unknown/noncanonical study snapshot envelope")
    if (
        envelope["payload_sha256"]
        != hashlib.sha256(_canonical(envelope["payload"]).encode()).hexdigest()
    ):
        raise ValueError("Snapshot payload checksum mismatch")
    _validate(envelope["payload"])
    return envelope


@dataclass(frozen=True, repr=False)
class FeatureSnapshotStudy:
    """Immutable bounded bytes; structural inspection is not source authentication."""

    encoded: bytes

    def __post_init__(self):
        _unpack(self.encoded)

    def __repr__(self):
        info = self.describe()
        return f"FeatureSnapshotStudy(features={info['feature_count']}, bytes={len(self.encoded)}, sha256={info['payload_sha256']!r})"

    def to_bytes(self):
        return self.encoded

    def to_dict(self):
        return _unpack(self.encoded)

    def describe(self):
        record = self.to_dict()
        payload = record["payload"]
        return {
            "schema": SCHEMA,
            "profile": PROFILE,
            "payload_sha256": record["payload_sha256"],
            "encoded_bytes": len(self.encoded),
            "feature_count": len(payload["inventory"]["features"]),
            **{k: payload[k] for k in ("parent", "request", "coverage", "producer")},
            "validation": "structural-and-content-integrity-only",
            "molecular_origin_authenticated": False,
            "quantity_semantics_validated_by_inspection": False,
        }

    def decode_inventory(self):
        import numpy as np

        from pharmacophoremt import pyunitwizard as puw
        from pharmacophoremt.modeler.aligned_consensus import _records

        inventory = self.to_dict()["payload"]["inventory"]
        for index, row in enumerate(inventory["features"]):
            for field, unit, dimension in (
                ("center", "nm", {"[L]": 1}),
                ("direction", "dimensionless", {}),
                ("normal", "dimensionless", {}),
                ("charge", "e", None),
            ):
                if row[field] is not None:
                    row[field] = puw.QuantityRecord.from_dict(row[field]).to_quantity(
                        field=f"features[{index}].{field}",
                        unit=unit,
                        dimensionality=dimension,
                    )
            if row["charge"] is not None:
                value = puw.get_value(row["charge"], to_unit="e")
                if (
                    np.shape(value) != ()
                    or not np.isfinite(value)
                    or (value > 0) != (row["kind"] == "positive charge")
                    or value == 0
                ):
                    raise ValueError("Expected a finite signed native formal charge")
        _records(inventory)
        return inventory


def capture_feature_snapshot(molecular_system, *, parent, features, producer):
    """Capture one actual native request under the declared unchanged-source trust."""
    _parent(parent)
    requested = _request(features)
    _producer(producer)
    _canonical(producer)
    import molsysmt as msm

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt._private.molsysmt import detached
    from pharmacophoremt.modeler import get_features
    from pharmacophoremt.modeler.aligned_consensus import _records
    from pharmacophoremt.modeler.features import CLASSICAL_FEATURES, DEFINITION

    if (
        tuple(CLASSICAL_FEATURES) != FAMILIES
        or DEFINITION != "classical_atomic_formal@1"
    ):
        raise ValueError(
            "Native feature definition differs from this frozen study profile"
        )
    if (
        msm.get(molecular_system, n_atoms=True) != parent["n_atoms"]
        or msm.get(molecular_system, n_structures=True) != 1
    ):
        raise ValueError("Prepared source atom/frame axis differs from its declaration")
    inventory = get_features(
        molecular_system,
        selection="all",
        structure_index=0,
        chemical_state=0,
        features=requested,
    )
    _records(inventory)
    sealed = detached(inventory)
    for index, row in enumerate(inventory["features"]):
        for field in ("center", "direction", "normal", "charge"):
            if row[field] is not None:
                sealed["features"][index][field] = puw.QuantityRecord.from_quantity(
                    row[field], field=f"features[{index}].{field}"
                ).to_dict()
    counts = Counter(row["kind"] for row in inventory["features"])
    payload = {
        "profile": PROFILE,
        "parent": parent,
        "request": {
            "definition": inventory["definition"],
            "features": requested,
            "selection": "all",
            "structure_index": 0,
            "chemical_state": 0,
            "coordinate_policy": "cartesian-no-imaging",
        },
        "coverage": {
            kind: {
                "count": counts[kind],
                "status": "completed" if counts[kind] else "evaluated_empty",
            }
            for kind in requested
        },
        "inventory": sealed,
        "producer": producer,
    }
    _validate(payload)
    return FeatureSnapshotStudy(
        _canonical(
            {
                "schema": SCHEMA,
                "payload": payload,
                "payload_sha256": hashlib.sha256(
                    _canonical(payload).encode()
                ).hexdigest(),
            }
        ).encode()
    )
