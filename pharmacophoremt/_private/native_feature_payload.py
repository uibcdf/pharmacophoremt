"""PHMT native-inventory science behind the public standalone payload tool."""

import hashlib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import numpy as np

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler.aligned_consensus import _records
from pharmacophoremt_features import _payload_schema as spec
from pharmacophoremt_features import _schema
from pharmacophoremt_features._diagnostics import FeatureAssetError, fail

FIELDS = (
    ("center", "nm", {"[L]": 1}),
    ("direction", "dimensionless", {}),
    ("normal", "dimensionless", {}),
    ("charge", "e", None),
)


def _capability():
    record_type = getattr(puw, "QuantityRecord", None)
    if record_type is None:
        fail(312)
    return record_type


def _validate_native(inventory, *, allow_volume=False):
    for row in inventory["features"]:
        for field, unit, _ in FIELDS:
            quantity = row[field]
            if quantity is None:
                continue
            if not puw.is_quantity(quantity):
                fail(332)
            values = np.asarray(puw.get_value(quantity, to_unit=unit))
            if (
                values.shape != (() if field == "charge" else (3,))
                or values.dtype.kind not in "iuf"
                or not np.isfinite(values).all()
            ):
                fail(332)
            if field in ("direction", "normal") and not np.any(values):
                fail(332)
            if field == "charge" and (
                values == 0 or (values > 0) != (row["kind"] == "positive charge")
            ):
                fail(332)
    # Preserve the native owner's center/orientation admission. Do not return its
    # normalized numerical projection in place of the captured native quantities.
    _records(
        dict(
            inventory,
            features=[
                r for r in inventory["features"] if r["kind"] != "included volume"
            ],
        )
        if allow_volume
        else inventory
    )


def decode(payload):
    """Work on a freshly parsed detached payload; return no partial inventory."""
    record_type = _capability()
    inventory = payload["inventory"]
    try:
        for index, row in enumerate(inventory["features"]):
            for field, unit, dimension in FIELDS:
                if row[field] is not None:
                    row[field] = record_type.from_dict(row[field]).to_quantity(
                        field=f"features[{index}].{field}",
                        unit=unit,
                        dimensionality=dimension,
                    )
        _validate_native(inventory)
    except FeatureAssetError:
        raise
    except Exception as error:
        raise FeatureAssetError(code="PHMT-E332") from error
    return inventory


def _observation():
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
        "observed_codec_sha256": digest,
        "operation": "FeatureInventoryPayload.from_inventory",
    }


def encode(inventory, families, parent, extraction_producer):
    coverage = spec.layout(inventory, parent, families, records=False)
    spec.provenance(
        parent,
        inventory["recognition"],
        inventory.get("attribution"),
        extraction_producer,
    )
    record_type = _capability()
    try:
        _validate_native(inventory)
        stored = {
            key: _schema.detached(value)
            for key, value in inventory.items()
            if key != "features"
        }
        stored["features"] = []
        for index, row in enumerate(inventory["features"]):
            converted = {
                key: _schema.detached(row[key])
                for key in ("kind", "atom_indices", "geometry_atom_indices")
            }
            for field, _, _ in FIELDS:
                converted[field] = (
                    None
                    if row[field] is None
                    else record_type.from_quantity(
                        row[field], field=f"features[{index}].{field}"
                    ).to_dict(encoding="json")
                )
            stored["features"].append(converted)
    except FeatureAssetError:
        raise
    except Exception as error:
        raise FeatureAssetError(code="PHMT-E332") from error
    payload = {
        "profile": spec.PROFILE,
        "parent": _schema.detached(parent),
        "evaluated_families": list(families),
        "coverage": coverage,
        "inventory": stored,
        "extraction_producer": _schema.detached(extraction_producer),
        "serialization": _observation(),
    }
    raw = _schema.encoded(
        {
            "schema": spec.SCHEMA,
            "payload": payload,
            "payload_sha256": hashlib.sha256(_schema.encoded(payload)).hexdigest(),
        }
    )
    # Reuse the same cold/native reader admission rather than granting a writer
    # passport. A later native consumption still revalidates every record afresh.
    decode(spec.document(raw))
    return raw
