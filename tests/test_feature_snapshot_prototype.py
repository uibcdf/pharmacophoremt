"""Actual native capture and independent integrity/unit/ownership refusal controls."""

import hashlib
from copy import deepcopy
from dataclasses import FrozenInstanceError

import pytest

from phmt_test_support.feature_snapshot import (
    MAX_BYTES,
    FeatureSnapshotStudy,
    capture_feature_snapshot,
)
from phmt_test_support.feature_snapshot_case import (
    declaration,
    independent_geometry,
    load_parent,
    producer_context,
    projection,
)


def encoded(record, *, resign=False):
    from pharmacophoremt_results import canonical_json

    if resign:
        record["payload_sha256"] = hashlib.sha256(
            canonical_json(record["payload"]).encode()
        ).hexdigest()
    return canonical_json(record).encode()


@pytest.fixture(scope="module")
def producer():
    return producer_context("a" * 64)


@pytest.fixture(scope="module")
def captured(producer):
    result = {}
    for request in declaration()["requests"]:
        source, parent = load_parent(request["parent"])
        result[request["key"]] = capture_feature_snapshot(
            source, parent=parent, features=request["features"], producer=producer
        )
    return result


@pytest.mark.parametrize("key", ["charges", "empty", "donors", "aromatic"])
def test_original_native_geometry_and_complete_requested_coverage(captured, key):
    snapshot = captured[key]
    restored = FeatureSnapshotStudy(snapshot.to_bytes())
    inventory = restored.decode_inventory()
    independent_geometry(key, inventory)
    request = next(r for r in declaration()["requests"] if r["key"] == key)
    assert {
        kind: row["count"] for kind, row in restored.describe()["coverage"].items()
    } == request["expected_counts"]
    assert restored.to_bytes() == snapshot.to_bytes()
    assert not restored.describe()["molecular_origin_authenticated"]
    assert not restored.describe()["quantity_semantics_validated_by_inspection"]


def test_shared_donor_center_preserves_both_original_participant_occurrences(captured):
    rows = projection(captured["donors"].decode_inventory())["features"]
    assert len(rows) == 2 and rows[0]["center"] == rows[1]["center"]
    assert {tuple(r["atom_indices"]) for r in rows} == {(1, 0), (1, 2)}
    assert rows[0]["direction"] != rows[1]["direction"]


def test_literal_unit_like_source_keys_and_empty_request_evidence_survive(captured):
    description = captured["empty"].describe()
    assert description["parent"]["source_key"] == "nm"
    assert description["parent"]["occurrence_key"] == "1 nm"
    assert description["request"]["features"] == ["aromatic ring"]
    assert description["coverage"] == {
        "aromatic ring": {"count": 0, "status": "evaluated_empty"}
    }
    assert description["feature_count"] == 0
    assert "1 nm" not in repr(captured["empty"])


def test_data_descriptions_and_reconstructed_quantities_are_detached(captured):
    snapshot = captured["charges"]
    original = snapshot.to_bytes()
    document = snapshot.to_dict()
    document["payload"]["parent"]["source_key"] = "changed"
    description = snapshot.describe()
    description["request"]["features"].clear()
    decoded = snapshot.decode_inventory()
    decoded["features"][0]["center"].magnitude[0] = 999
    assert snapshot.to_bytes() == original
    independent_geometry("charges", snapshot.decode_inventory())
    with pytest.raises(FrozenInstanceError):
        snapshot.encoded = b"changed"


def test_capture_does_not_follow_later_caller_or_molecular_mutation(producer):
    import molsysmt as msm

    from pharmacophoremt import pyunitwizard as puw

    source, parent = load_parent("ions")
    context = deepcopy(producer)
    snapshot = capture_feature_snapshot(
        source,
        parent=parent,
        features=["positive charge", "negative charge"],
        producer=context,
    )
    original = snapshot.to_bytes()
    parent["source_key"] = "changed"
    context["versions"].clear()
    msm.structure.translate(
        source, translation=puw.quantity([[[1, 2, 3]]], "nm"), in_place=True
    )
    assert snapshot.to_bytes() == original
    independent_geometry("charges", snapshot.decode_inventory())


def test_repeated_source_occurrence_has_its_own_binding_without_deduplication(producer):
    source, parent = load_parent("ions")
    first = capture_feature_snapshot(
        source,
        parent=parent,
        features=["positive charge", "negative charge"],
        producer=producer,
    )
    parent["occurrence_key"] = "repeat=α"
    second = capture_feature_snapshot(
        source,
        parent=parent,
        features=["negative charge", "positive charge", "positive charge"],
        producer=producer,
    )
    assert first.describe()["request"] == second.describe()["request"]
    assert projection(first.decode_inventory()) == projection(second.decode_inventory())
    assert first.describe()["payload_sha256"] != second.describe()["payload_sha256"]
    assert second.describe()["parent"]["occurrence_key"] == "repeat=α"


@pytest.mark.parametrize(
    "bad", ["schema", "checksum", "whitespace", "duplicate", "oversize"]
)
def test_reader_refuses_corrupt_unknown_noncanonical_and_oversized_bytes(captured, bad):
    snapshot = captured["charges"]
    record = snapshot.to_dict()
    if bad == "schema":
        record["schema"] = "pharmacophoremt.feature-snapshot-study@999"
        raw = encoded(record)
    elif bad == "checksum":
        record["payload"]["parent"]["source_key"] = "altered"
        raw = encoded(record)
    elif bad == "whitespace":
        raw = b" " + snapshot.to_bytes()
    elif bad == "duplicate":
        raw = (
            b'{"schema":"pharmacophoremt.feature-snapshot-study@1",'
            + snapshot.to_bytes()[1:]
        )
    else:
        raw = b"x" * (MAX_BYTES + 1)
    with pytest.raises(ValueError):
        FeatureSnapshotStudy(raw)


@pytest.mark.parametrize(
    "change", ["atom", "geometry_atom", "frame", "coverage", "definition", "partial"]
)
def test_checksum_consistency_does_not_replace_structural_admission(captured, change):
    record = captured["charges"].to_dict()
    p = record["payload"]
    if change == "atom":
        p["inventory"]["features"][0]["atom_indices"] = [999]
    elif change == "geometry_atom":
        p["inventory"]["features"][0]["geometry_atom_indices"] = [True]
    elif change == "frame":
        p["request"]["structure_index"] = 1
    elif change == "coverage":
        p["coverage"]["positive charge"]["count"] = True
    elif change == "definition":
        p["request"]["definition"] = "unknown@1"
    else:
        p["inventory"]["complete"] = False
    with pytest.raises(ValueError):
        FeatureSnapshotStudy(encoded(record, resign=True))


@pytest.mark.parametrize("kind", ["wrong_unit", "wrong_field", "nonfinite"])
def test_explicit_reconstruction_uses_the_provider_quantity_handshake(captured, kind):
    from pyunitwizard.record import RecordError

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt._private.smonitor.exceptions import ArgumentError

    record = captured["charges"].to_dict()
    unit = "ps" if kind == "wrong_unit" else "nm"
    values = [float("nan"), 0, 0] if kind == "nonfinite" else [0, 0, 0]
    field = "wrong" if kind == "wrong_field" else "features[0].center"
    quantity = puw.QuantityRecord.from_quantity(puw.quantity(values, unit), field=field)
    record["payload"]["inventory"]["features"][0]["center"] = quantity.to_dict(
        encoding="base64" if kind == "nonfinite" else "json"
    )
    snapshot = FeatureSnapshotStudy(encoded(record, resign=True))
    assert not snapshot.describe()["quantity_semantics_validated_by_inspection"]
    with pytest.raises(ArgumentError if kind == "nonfinite" else RecordError):
        snapshot.decode_inventory()


@pytest.mark.parametrize(
    "bad", ["parent", "frame", "count", "request", "empty_request", "producer"]
)
def test_decidable_request_refusal_precedes_molecular_metadata_and_extraction(
    monkeypatch, producer, bad
):
    import molsysmt as msm

    from pharmacophoremt import modeler

    # Only this test-owned parent declaration is needed before metadata access.
    parent = {
        "source_key": "nm",
        "occurrence_key": "1 nm",
        "artifact_sha256": "a" * 64,
        "artifact_bytes": 1,
        "n_atoms": 3,
        "structure_index": 0,
        "chemical_state": 0,
        "trust": "caller-verified-artifact/unchanged-source",
        "preparation": "controlled",
    }
    features = ["positive charge"]
    context = deepcopy(producer)
    if bad == "parent":
        parent["trust"] = "unverified"
    elif bad == "frame":
        parent["structure_index"] = 1
    elif bad == "count":
        parent["n_atoms"] = 257
    elif bad == "request":
        features = ["included volume"]
    elif bad == "empty_request":
        features = []
    else:
        context["admission_sha256"] = "missing"

    def unexpected(*args, **kwargs):
        pytest.fail("molecular work reached before decidable refusal")

    monkeypatch.setattr(msm, "get", unexpected)
    monkeypatch.setattr(modeler, "get_features", unexpected)
    with pytest.raises(ValueError):
        capture_feature_snapshot(
            object(), parent=parent, features=features, producer=context
        )


def test_mismatched_declared_parent_axis_is_refused_before_extraction(
    monkeypatch, producer
):
    from pharmacophoremt import modeler

    source, parent = load_parent("ions")
    parent["n_atoms"] = 4

    def unexpected(*args, **kwargs):
        pytest.fail("extraction reached after parent-axis mismatch")

    monkeypatch.setattr(modeler, "get_features", unexpected)
    with pytest.raises(ValueError, match="axis"):
        capture_feature_snapshot(
            source, parent=parent, features=["positive charge"], producer=producer
        )


def test_actual_controlled_feature_failure_is_not_an_empty_success(
    monkeypatch, producer
):
    from pharmacophoremt import modeler

    source, parent = load_parent("ions")
    failure = RuntimeError("controlled feature producer failure")

    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(modeler, "get_features", fail)
    with pytest.raises(RuntimeError) as caught:
        capture_feature_snapshot(
            source, parent=parent, features=["positive charge"], producer=producer
        )
    assert caught.value is failure


def test_partial_return_is_never_promoted_to_a_successful_empty_capture(
    monkeypatch, producer, captured
):
    from pharmacophoremt import modeler

    source, parent = load_parent("ions")
    partial = captured["empty"].decode_inventory()
    partial["complete"] = False
    monkeypatch.setattr(modeler, "get_features", lambda *a, **k: partial)
    with pytest.raises(ValueError, match="layout"):
        capture_feature_snapshot(
            source, parent=parent, features=["aromatic ring"], producer=producer
        )
