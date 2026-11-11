"""Cold structure and bounded provenance for native feature payload v1."""

import hashlib
import math
from collections import Counter

from . import _schema
from ._diagnostics import FeatureAssetError, fail

PAYLOAD_PROFILE = _schema.NATIVE_PAYLOAD_PROFILE
SCHEMA = "pharmacophoremt.native-feature-payload@1"
PROFILE = "classical-single-frame@1"
MAPPING_POLICY = "caller-declared-local-atom-axis@1"
DEFINITION = "classical_atomic_formal@1"
MAX_FEATURES = 64
MAX_ATOMS = 256
MAX_PROVENANCE_NODES = 16384
MAX_PROVENANCE_DEPTH = 24
MAX_PROVENANCE_TEXT = 128 * 1024
INVENTORY_FIELDS = {
    "definition",
    "features",
    "recognition",
    "selected_atom_indices",
    "structure_index",
    "chemical_state",
}
FEATURE_FIELDS = {
    "kind",
    "atom_indices",
    "geometry_atom_indices",
    "center",
    "direction",
    "normal",
    "charge",
}


def require(condition):
    if not condition:
        fail(330)


def _integer(value, maximum=2**63 - 1):
    return type(value) is int and 0 <= value <= maximum


def _text(value, maximum=512):
    require(type(value) is str and bool(value))
    try:
        require(len(value.encode("utf-8")) <= maximum)
    except UnicodeError as error:
        raise FeatureAssetError(code="PHMT-E330") from error


def provenance(*values):
    """Bound plain JSON before copying; reject cycles by the finite depth bound."""
    nodes, text_bytes = 0, 0

    def visit(value, depth):
        nonlocal nodes, text_bytes
        nodes += 1
        if nodes > MAX_PROVENANCE_NODES or depth > MAX_PROVENANCE_DEPTH:
            fail(333)
        if type(value) is str:
            try:
                text_bytes += len(value.encode("utf-8"))
            except UnicodeError as error:
                raise FeatureAssetError(code="PHMT-E330") from error
            if text_bytes > MAX_PROVENANCE_TEXT:
                fail(333)
        elif type(value) is dict:
            if len(value) > MAX_PROVENANCE_NODES - nodes:
                fail(333)
            for key, item in value.items():
                require(type(key) is str)
                visit(key, depth + 1)
                visit(item, depth + 1)
        elif type(value) is list:
            if len(value) > MAX_PROVENANCE_NODES - nodes:
                fail(333)
            for item in value:
                visit(item, depth + 1)
        elif type(value) is float:
            require(math.isfinite(value))
        else:
            require(value is None or type(value) in (bool, int))
            # Prevent unbounded integer-to-text conversion during detachment.
            if type(value) is int and value.bit_length() > 64:
                fail(333)

    for value in values:
        visit(value, 0)


def declared_families(value):
    require(type(value) in (list, tuple) and 0 < len(value) <= len(_schema.FAMILIES))
    require(all(type(k) is str and k in _schema.FAMILIES for k in value))
    require(len(set(value)) == len(value))
    return [k for k in _schema.FAMILIES if k in value]


def layout(inventory, parent, families, *, records):
    """Check lossless profile layout/maps without interpreting quantities."""
    require(
        type(parent) is dict
        and set(parent)
        == {
            "source_key",
            "occurrence_key",
            "artifact_sha256",
            "artifact_bytes",
            "n_atoms",
            "preparation",
            "mapping_policy",
        }
    )
    for name in ("source_key", "occurrence_key"):
        _text(parent[name])
    require(parent["mapping_policy"] == MAPPING_POLICY)
    if parent["preparation"] is not None:
        _text(parent["preparation"])
    require(_integer(parent["n_atoms"]) and parent["n_atoms"] > 0)
    if parent["n_atoms"] > MAX_ATOMS:
        fail(333)
    if parent["artifact_sha256"] is None:
        require(parent["artifact_bytes"] is None)
    else:
        try:
            _schema.digest(parent["artifact_sha256"])
        except FeatureAssetError as error:
            raise FeatureAssetError(code="PHMT-E330") from error
        require(_integer(parent["artifact_bytes"]) and parent["artifact_bytes"] > 0)
    require(
        type(inventory) is dict
        and INVENTORY_FIELDS <= set(inventory) <= INVENTORY_FIELDS | {"attribution"}
    )
    if inventory["definition"] != DEFINITION:
        fail(331)
    require(type(inventory["recognition"]) is dict)
    require(_integer(inventory["structure_index"]))
    state = inventory["chemical_state"]
    require(
        state is None
        or _integer(state)
        or (type(state) is str and state in ("reference", "structure"))
    )
    indices = inventory["selected_atom_indices"]
    require(type(indices) is list and 0 < len(indices) <= parent["n_atoms"])
    require(all(_integer(i, parent["n_atoms"] - 1) for i in indices))
    require(len(set(indices)) == len(indices))
    features = inventory["features"]
    require(type(features) is list)
    if len(features) > MAX_FEATURES:
        fail(333)
    for row in features:
        require(type(row) is dict and set(row) == FEATURE_FIELDS)
        if type(row["kind"]) is not str or row["kind"] not in _schema.FAMILIES:
            fail(331)
        require(row["kind"] in families)
        for name in ("atom_indices", "geometry_atom_indices"):
            atoms = row[name]
            require(type(atoms) is list and 0 < len(atoms) <= len(indices))
            require(all(type(i) is int and i in indices for i in atoms))
            require(len(set(atoms)) == len(atoms))
        for name, present in (
            ("center", True),
            ("direction", row["kind"] == "hb donor"),
            ("normal", row["kind"] == "aromatic ring"),
            ("charge", row["kind"] in ("positive charge", "negative charge")),
        ):
            require(row[name] is not None if present else row[name] is None)
            if records and present:
                require(type(row[name]) is dict)
    counts = Counter(row["kind"] for row in features)
    return {
        family: {
            "count": counts[family],
            "status": "completed" if counts[family] else "evaluated_empty",
        }
        for family in families
    }


def document(raw):
    require(type(raw) is bytes and bool(raw))
    if len(raw) > _schema.MAX_PAYLOAD_BYTES:
        fail(333)
    try:
        value = _schema.json_document(raw)
    except FeatureAssetError as error:
        raise FeatureAssetError(code="PHMT-E330") from error
    require(
        type(value) is dict and set(value) == {"schema", "payload", "payload_sha256"}
    )
    if value["schema"] != SCHEMA:
        fail(331)
    payload = value["payload"]
    require(
        type(payload) is dict
        and set(payload)
        == {
            "profile",
            "parent",
            "evaluated_families",
            "coverage",
            "inventory",
            "extraction_producer",
            "serialization",
        }
    )
    if payload["profile"] != PROFILE:
        fail(331)
    require(
        value["payload_sha256"] == hashlib.sha256(_schema.encoded(payload)).hexdigest()
    )
    families = declared_families(payload["evaluated_families"])
    require(payload["evaluated_families"] == families)
    expected = layout(payload["inventory"], payload["parent"], families, records=True)
    require(_schema.encoded(payload["coverage"]) == _schema.encoded(expected))
    producer, observation = payload["extraction_producer"], payload["serialization"]
    require(producer is None or type(producer) is dict)
    require(
        type(observation) is dict
        and set(observation)
        == {
            "distribution",
            "distribution_version",
            "observed_codec_sha256",
            "operation",
        }
    )
    require(
        observation["distribution"] == "pharmacophoremt"
        and observation["operation"] == "FeatureInventoryPayload.from_inventory"
    )
    if observation["distribution_version"] is not None:
        _text(observation["distribution_version"], 128)
    if observation["observed_codec_sha256"] is not None:
        try:
            _schema.digest(observation["observed_codec_sha256"])
        except FeatureAssetError as error:
            raise FeatureAssetError(code="PHMT-E330") from error
    provenance(
        payload["parent"],
        payload["inventory"]["recognition"],
        payload["inventory"].get("attribution"),
        producer,
        observation,
    )
    return payload
