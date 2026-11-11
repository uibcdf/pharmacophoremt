"""Bounded public metadata-archive profile; original payloads stay opaque."""

import base64
import hashlib
import json
import math
import re

from pharmacophoremt_results import canonical_json

from ._diagnostics import fail

STORE_SCHEMA = "pharmacophoremt.feature-archive@1"
GENERATION_SCHEMA = "pharmacophoremt.feature-archive-generation@1"
PROFILE = "declared-classical-inventory@1"
MAX_DOCUMENT_BYTES = 8 * 1024 * 1024
MAX_UNIQUE_PAYLOAD_BYTES = 4 * 1024 * 1024
MAX_PAYLOAD_BYTES = 2 * 1024 * 1024
MAX_RECORDS = 4096
FAMILIES = (
    "hydrophobicity",
    "hb donor",
    "hb acceptor",
    "aromatic ring",
    "positive charge",
    "negative charge",
)
STATES = ("ready", "failed", "partial", "unsupported", "unattempted")
MARKER = {"schema": STORE_SCHEMA, "profile": PROFILE}


def encoded(value):
    return canonical_json(value).encode("utf-8")


def detached(value):
    return json.loads(canonical_json(value))


def digest(value, *, argument=None):
    if type(value) is not str or not re.fullmatch("[a-f0-9]{64}", value):
        fail(301 if argument else 302, argument=argument)
    return value


def text(value, maximum=512):
    if type(value) is not str or not value or len(value.encode("utf-8")) > maximum:
        fail(302)


def families(value, *, argument=False):
    if (
        type(value) not in (list, tuple)
        or not value
        or any(type(k) is not str or k not in FAMILIES for k in value)
    ):
        fail(
            301 if argument else 302, argument="required_families" if argument else None
        )
    return [k for k in FAMILIES if k in value]


def _finite_float(text):
    value = float(text)
    if not math.isfinite(value):
        fail(302)
    return value


def _constant(text):
    fail(302)


def json_document(raw):
    try:
        value = json.loads(raw, parse_float=_finite_float, parse_constant=_constant)
        if encoded(value) != raw:
            fail(302)
        return value
    except (UnicodeError, ValueError, RecursionError) as error:
        from ._diagnostics import FeatureAssetError

        if isinstance(error, FeatureAssetError):
            raise
        try:
            fail(302)
        except FeatureAssetError as failure:
            raise failure from error


def _integer(value, *, minimum=0):
    if type(value) is not int or not minimum <= value <= 2**63 - 1:
        fail(302)


def _extraction(value, row):
    if type(value) is not dict or set(value) != {
        "definition",
        "requested_families",
        "coverage",
        "parent",
        "producer",
    }:
        fail(302)
    if value["definition"] != "classical_atomic_formal@1":
        fail(307)
    requested = families(value["requested_families"])
    if (
        value["requested_families"] != requested
        or type(value["coverage"]) is not dict
        or set(value["coverage"]) != set(requested)
    ):
        fail(302)
    total = 0
    for coverage in value["coverage"].values():
        if type(coverage) is not dict or set(coverage) != {"count", "status"}:
            fail(302)
        _integer(coverage["count"])
        total += coverage["count"]
        if coverage["status"] != (
            "completed" if coverage["count"] else "evaluated_empty"
        ):
            fail(302)
    if total > 64:
        fail(302)
    parent = value["parent"]
    if type(parent) is not dict or set(parent) != {
        "source_key",
        "occurrence_key",
        "artifact_sha256",
        "artifact_bytes",
        "n_atoms",
        "structure_index",
        "chemical_state",
        "trust",
        "preparation",
    }:
        fail(302)
    for key in ("source_key", "occurrence_key", "trust", "preparation"):
        text(parent[key])
    if any(parent[k] != row[k] for k in ("source_key", "occurrence_key")):
        fail(302)
    digest(parent["artifact_sha256"])
    for key in ("artifact_bytes", "n_atoms"):
        _integer(parent[key], minimum=1)
    for key in ("structure_index", "chemical_state"):
        _integer(parent[key])
    producer = value["producer"]
    if type(producer) is not dict or set(producer) != {
        "scope",
        "admission_sha256",
        "runtime_version",
        "versions",
    }:
        fail(302)
    digest(producer["admission_sha256"])
    for key in ("scope", "runtime_version"):
        text(producer[key])
    versions = producer["versions"]
    if type(versions) is not dict or not versions or len(versions) > 128:
        fail(302)
    for key, version in versions.items():
        text(key)
        text(version)


def generation(raw):
    value = json_document(raw)
    if type(value) is not dict:
        fail(302)
    if value.get("schema") != GENERATION_SCHEMA or value.get("profile") != PROFILE:
        fail(307)
    if set(value) != {"schema", "profile", "origin", "records", "payloads"}:
        fail(302)
    origin = value["origin"]
    if type(origin) is not dict or set(origin) != {"format", "generation", "policy"}:
        fail(302)
    text(origin["format"])
    text(origin["policy"])
    digest(origin["generation"])
    rows, payloads = value["records"], value["payloads"]
    if (
        type(rows) is not list
        or len(rows) > MAX_RECORDS
        or type(payloads) is not dict
        or len(payloads) > MAX_RECORDS
    ):
        fail(302)
    originals, total = {}, 0
    for key, item in payloads.items():
        digest(key)
        if type(item) is not dict or set(item) != {"format", "data"}:
            fail(302)
        text(item["format"])
        if type(item["data"]) is not str or len(item["data"]) > 4 * (
            (MAX_PAYLOAD_BYTES + 2) // 3
        ):
            fail(302)
        try:
            original = base64.b64decode(item["data"], validate=True)
        except ValueError as error:
            from ._diagnostics import FeatureAssetError

            raise FeatureAssetError(code="PHMT-E302") from error
        if (
            not 0 < len(original) <= MAX_PAYLOAD_BYTES
            or base64.b64encode(original).decode("ascii") != item["data"]
            or hashlib.sha256(original).hexdigest() != key
        ):
            fail(302)
        total += len(original)
        if total > MAX_UNIQUE_PAYLOAD_BYTES:
            fail(302)
        originals[key] = original
    used, keys = set(), set()
    for row in rows:
        if (
            type(row) is not dict
            or type(row.get("status")) is not str
            or row["status"] not in STATES
        ):
            fail(302)
        extra = (
            {"payload_sha256", "extraction"} if row["status"] == "ready" else {"cause"}
        )
        if set(row) != {"work_key", "source_key", "occurrence_key", "status"} | extra:
            fail(302)
        for key in ("work_key", "source_key", "occurrence_key"):
            text(row[key])
        if row["work_key"] in keys:
            fail(302)
        keys.add(row["work_key"])
        if row["status"] == "ready":
            key = digest(row["payload_sha256"])
            if key not in originals:
                fail(302)
            used.add(key)
            _extraction(row["extraction"], row)
        else:
            cause = row["cause"]
            if type(cause) is not dict or set(cause) != {"type", "reason"}:
                fail(302)
            for text_value in cause.values():
                text(text_value, 2048)
    if used != set(originals):
        fail(302)
    return value, originals
