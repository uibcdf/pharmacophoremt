"""Explicit compatibility decoder for original bounded snapshot-study v1 bytes.

This is a consumer-owned scientific schema, not a study-class runtime dependency
or a replacement quantity codec. Original producer metadata stays uninterpreted.
"""

import hashlib
from collections import Counter

from pharmacophoremt_features import _schema
from pharmacophoremt_features._diagnostics import fail

PAYLOAD_PROFILE = _schema.SNAPSHOT_PROFILE
SCHEMA = "pharmacophoremt.feature-snapshot-study@1"
PROFILE = "native-classical-single-frame@1"
FIELDS = {
    "kind",
    "atom_indices",
    "geometry_atom_indices",
    "center",
    "direction",
    "normal",
    "charge",
}
INVENTORY = {
    "definition",
    "features",
    "recognition",
    "selected_atom_indices",
    "structure_index",
    "chemical_state",
}


def _require(condition):
    if not condition:
        fail(310)


def _structure(raw, extraction):
    """Check original bytes and the complete archive/payload metadata binding."""
    _require(type(raw) is bytes and 0 < len(raw) <= _schema.MAX_PAYLOAD_BYTES)
    value = _schema.json_document(raw)
    _require(
        type(value) is dict and set(value) == {"schema", "payload", "payload_sha256"}
    )
    if value["schema"] != SCHEMA:
        fail(307)
    payload = value["payload"]
    _require(
        type(payload) is dict
        and set(payload)
        == {"profile", "parent", "request", "coverage", "inventory", "producer"}
    )
    if payload["profile"] != PROFILE:
        fail(307)
    _require(
        value["payload_sha256"] == hashlib.sha256(_schema.encoded(payload)).hexdigest()
    )
    parent = extraction["parent"]
    _require(_schema.encoded(payload["parent"]) == _schema.encoded(parent))
    _require(
        _schema.encoded(payload["producer"]) == _schema.encoded(extraction["producer"])
    )
    _require(1 <= parent["n_atoms"] <= 256)
    _require(
        all(
            type(parent[k]) is int and parent[k] == 0
            for k in ("structure_index", "chemical_state")
        )
    )
    _require(parent["trust"] == "caller-verified-artifact/unchanged-source")
    _require(extraction["producer"]["scope"] == "selected-case-context")
    _require(
        _schema.encoded(payload["request"])
        == _schema.encoded(
            {
                "definition": extraction["definition"],
                "features": extraction["requested_families"],
                "selection": "all",
                "structure_index": 0,
                "chemical_state": 0,
                "coordinate_policy": "cartesian-no-imaging",
            }
        )
    )
    # Equality alone would admit False in place of 0.
    _require(
        all(
            type(payload["request"][k]) is int
            for k in ("structure_index", "chemical_state")
        )
    )
    inventory = payload["inventory"]
    _require(
        type(inventory) is dict
        and INVENTORY <= set(inventory) <= INVENTORY | {"attribution"}
    )
    _require(
        inventory["definition"] == extraction["definition"]
        and type(inventory["recognition"]) is dict
    )
    _require(
        all(
            type(inventory[k]) is int and inventory[k] == 0
            for k in ("structure_index", "chemical_state")
        )
    )
    indices = inventory["selected_atom_indices"]
    _require(
        type(indices) is list
        and indices == list(range(parent["n_atoms"]))
        and all(type(i) is int for i in indices)
    )
    features = inventory["features"]
    _require(type(features) is list and len(features) <= 64)
    for row in features:
        _require(type(row) is dict and set(row) == FIELDS)
        _require(
            type(row["kind"]) is str and row["kind"] in extraction["requested_families"]
        )
        for key in ("atom_indices", "geometry_atom_indices"):
            atoms = row[key]
            _require(
                type(atoms) is list
                and bool(atoms)
                and all(type(i) is int and i in indices for i in atoms)
            )
            _require(len(set(atoms)) == len(atoms))
        _require(type(row["center"]) is dict)
        for key, required in (
            ("direction", row["kind"] == "hb donor"),
            ("normal", row["kind"] == "aromatic ring"),
            ("charge", row["kind"] in {"positive charge", "negative charge"}),
        ):
            _require(type(row[key]) is dict if required else row[key] is None)
    counts = Counter(row["kind"] for row in features)
    expected = {
        k: {
            "count": counts[k],
            "status": "completed" if counts[k] else "evaluated_empty",
        }
        for k in extraction["requested_families"]
    }
    _require(
        _schema.encoded(payload["coverage"])
        == _schema.encoded(expected)
        == _schema.encoded(extraction["coverage"])
    )
    return inventory


def decode_snapshot(raw, extraction):
    """Reconstruct every feature quantity afresh, preserving original data/maps."""
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.modeler.aligned_consensus import _records

    inventory = _structure(raw, extraction)
    record_type = getattr(puw, "QuantityRecord", None)
    if record_type is None:
        fail(312)
    try:
        for index, row in enumerate(inventory["features"]):
            for field, unit, dimension in (
                ("center", "nm", {"[L]": 1}),
                ("direction", "dimensionless", {}),
                ("normal", "dimensionless", {}),
                ("charge", "e", None),
            ):
                if row[field] is not None:
                    row[field] = record_type.from_dict(row[field]).to_quantity(
                        field=f"features[{index}].{field}",
                        unit=unit,
                        dimensionality=dimension,
                    )
            if row["charge"] is not None:
                value = puw.get_value(row["charge"], to_unit="e")
                if (
                    np.shape(value) != ()
                    or not np.isfinite(value)
                    or value == 0
                    or (value > 0) != (row["kind"] == "positive charge")
                ):
                    fail(311)
        # The native owner validates centers, orientation and feature maps.
        _records(inventory)
    except Exception as error:
        from pharmacophoremt_features import FeatureAssetError

        if isinstance(error, FeatureAssetError):
            raise
        raise FeatureAssetError(code="PHMT-E311") from error
    return inventory
