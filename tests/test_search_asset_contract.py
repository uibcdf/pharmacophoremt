"""Real existing snapshot boundaries plus a conservative coverage-only plane."""

import hashlib
import json
import os
from copy import deepcopy

import pytest

from phmt_test_support.feature_snapshot import FAMILIES, FeatureSnapshotStudy
from phmt_test_support.search_asset_contract import family_coverage
from phmt_test_support.snapshot_retrieval import SnapshotRetrievalStudy, project
from phmt_test_support.typed_retrieval import declaration, load_entries


@pytest.fixture(scope="module")
def entries():
    return load_entries(os.environ.get("PHMT_RECEIVING_CONTEXT", "source"))


def seal_changed_metadata(record):
    from pharmacophoremt_results import canonical_json

    record["payload_sha256"] = hashlib.sha256(
        canonical_json(record["payload"]).encode()
    ).hexdigest()
    return FeatureSnapshotStudy(canonical_json(record).encode())


def test_empty_aromatic_evaluation_does_not_evaluate_donor_charge_families(entries):
    snapshot = FeatureSnapshotStudy(entries[0]["snapshot"])
    aromatic = family_coverage(snapshot, ["aromatic ring"])
    assert aromatic["family_coverage_complete"]
    assert aromatic["known_counts"] == {"aromatic ring": 0}
    donor = family_coverage(
        snapshot, ["hb donor", "positive charge", "negative charge"]
    )
    assert not donor["family_coverage_complete"] and donor["known_counts"] == {}
    assert donor["unobserved_families"] == [
        "hb donor",
        "positive charge",
        "negative charge",
    ]
    assert aromatic["match_outcome"] is donor["match_outcome"] is None


@pytest.mark.parametrize(
    "ordinal,required,known,missing",
    [
        (
            1,
            ["hb donor", "positive charge", "negative charge"],
            {"hb donor": 2, "positive charge": 1, "negative charge": 1},
            [],
        ),
        (
            1,
            ["aromatic ring", "positive charge", "negative charge"],
            {"positive charge": 1, "negative charge": 1},
            ["aromatic ring"],
        ),
        (
            3,
            ["aromatic ring", "positive charge", "negative charge"],
            {"aromatic ring": 1, "positive charge": 1, "negative charge": 1},
            [],
        ),
        (
            4,
            ["hydrophobicity", "hb acceptor", "positive charge"],
            {"hydrophobicity": 1, "hb acceptor": 1, "positive charge": 1},
            [],
        ),
        (
            5,
            ["hydrophobicity", "hb acceptor", "positive charge"],
            {"hydrophobicity": 2, "hb acceptor": 1, "positive charge": 1},
            [],
        ),
    ],
)
def test_recorded_family_counts_preserve_original_evaluation_scope(
    entries, ordinal, required, known, missing
):
    report = family_coverage(
        FeatureSnapshotStudy(entries[ordinal]["snapshot"]), required
    )
    assert report["known_counts"] == known and report["unobserved_families"] == missing
    assert report["family_coverage_complete"] == (not missing)
    assert report["query_admitted"] is report["match_outcome"] is None
    assert (
        not report["quantity_semantics_checked"]
        and not report["molecular_origin_authenticated"]
    )


def test_required_family_order_duplicates_and_literal_parent_keys_are_separate(entries):
    snapshot = FeatureSnapshotStudy(entries[1]["snapshot"])
    a = family_coverage(snapshot, ["positive charge", "hb donor", "hb donor"])
    b = family_coverage(snapshot, ["hb donor", "positive charge"])
    assert a == b
    assert snapshot.describe()["parent"]["source_key"] == "nm"
    assert snapshot.describe()["parent"]["occurrence_key"] == "1 nm"
    a["known_counts"]["hb donor"] = 999
    a["captured_request"].clear()
    assert family_coverage(snapshot, ["hb donor", "positive charge"]) == b


@pytest.mark.parametrize("required", [[], "hb donor", ["unknown family"], [1]])
def test_invalid_required_families_refuse_before_snapshot_inspection(
    entries, required, monkeypatch
):
    snapshot = FeatureSnapshotStudy(entries[1]["snapshot"])

    def forbidden(*args):
        raise AssertionError("Invalid family request reached snapshot inspection")

    monkeypatch.setattr(FeatureSnapshotStudy, "describe", forbidden)
    with pytest.raises(ValueError):
        family_coverage(snapshot, required)


def test_requesting_all_families_keeps_unobserved_families_explicit(entries):
    report = family_coverage(
        FeatureSnapshotStudy(entries[1]["snapshot"]), list(FAMILIES)
    )
    assert report["unobserved_families"] == [
        "hydrophobicity",
        "hb acceptor",
        "aromatic ring",
    ]
    assert not report["family_coverage_complete"]


def test_relocation_preserves_original_bytes_and_noncanonical_reencoding_is_refused(
    entries, tmp_path
):
    original = FeatureSnapshotStudy(entries[1]["snapshot"])
    first = tmp_path / "first.json"
    moved = tmp_path / "moved.json"
    first.write_bytes(original.to_bytes())
    moved.write_bytes(first.read_bytes())
    required = ["hb donor", "positive charge"]
    baseline = family_coverage(original, required)
    assert (
        family_coverage(FeatureSnapshotStudy(moved.read_bytes()), required) == baseline
    )
    reformatted = (json.dumps(original.to_dict(), indent=2) + "\n").encode()
    assert json.loads(reformatted)["payload_sha256"] == baseline["payload_sha256"]
    assert hashlib.sha256(reformatted).hexdigest() != baseline["encoded_sha256"]
    with pytest.raises(ValueError, match="noncanonical study snapshot envelope"):
        FeatureSnapshotStudy(reformatted)


def test_self_consistent_claimed_producer_is_not_authenticated_origin(entries):
    original = FeatureSnapshotStudy(entries[1]["snapshot"])
    changed = original.to_dict()
    changed["payload"]["producer"]["runtime_version"] = "synthetic-contract-control"
    synthetic = seal_changed_metadata(changed)
    report = family_coverage(synthetic, ["hb donor"])
    assert (
        report["family_coverage_complete"]
        and report["payload_sha256"] != original.describe()["payload_sha256"]
    )
    assert (
        not report["molecular_origin_authenticated"]
        and report["query_admitted"] is None
    )


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_coverage_and_structural_inspection_do_not_validate_quantity_dimension(
    entries, unit
):
    from pharmacophoremt import pyunitwizard as puw

    original = FeatureSnapshotStudy(entries[1]["snapshot"])
    changed = original.to_dict()
    changed["payload"]["inventory"]["features"][0]["center"] = (
        puw.QuantityRecord.from_quantity(
            puw.quantity([0.0, 0.0, 0.0], "ps"), field="features[0].center"
        ).to_dict()
    )
    incompatible = seal_changed_metadata(changed)
    report = family_coverage(incompatible, ["hb donor"])
    assert (
        report["family_coverage_complete"] and not report["quantity_semantics_checked"]
    )
    with puw.context(standard_units=[unit, "ps", "radians"]):
        with pytest.raises(Exception) as caught:
            incompatible.decode_inventory()
    assert (
        "dimension" in str(caught.value).lower() or "unit" in str(caught.value).lower()
    )


@pytest.fixture(scope="module")
def study(entries):
    return SnapshotRetrievalStudy(entries, 1.0)


@pytest.mark.parametrize(
    "mutation", ["reencode", "reorder", "work_key", "other_unit_original"]
)
def test_current_lookup_refuses_changed_manifest_even_for_same_feature_content(
    entries, study, mutation
):
    changed = deepcopy(entries)
    if mutation == "reencode":
        changed[1]["snapshot"] = json.dumps(
            FeatureSnapshotStudy(changed[1]["snapshot"]).to_dict(), indent=2
        ).encode()
    elif mutation == "reorder":
        changed[1], changed[6] = changed[6], changed[1]
    elif mutation == "work_key":
        changed[1]["work_key"] += ":new-original-key"
    else:
        changed[1]["snapshot"] = entries[6]["snapshot"]
    reason = (
        "noncanonical study snapshot envelope"
        if mutation == "reencode"
        else "bindings changed"
    )
    with pytest.raises(ValueError, match=reason):
        study.lookup(declaration()["queries"][0], current_entries=changed)


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_same_physical_unit_projection_does_not_merge_original_encodings(entries, unit):
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    first = FeatureSnapshotStudy(entries[1]["snapshot"])
    second = FeatureSnapshotStudy(entries[6]["snapshot"])
    assert first.to_bytes() != second.to_bytes()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        a, b = project(first.decode_inventory()), project(second.decode_inventory())
    assert [p[0] for p in a] == [p[0] for p in b]
    np.testing.assert_allclose([p[1] for p in a], [p[1] for p in b], rtol=0, atol=1e-12)


def test_new_order_changes_manifest_while_candidate_original_keys_survive(
    entries, study
):
    changed = deepcopy(entries)
    changed[0], changed[1] = changed[1], changed[0]
    rebuilt = SnapshotRetrievalStudy(changed, 1.0)
    query = declaration()["queries"][0]
    before = study.lookup(query, current_entries=entries)
    after = rebuilt.lookup(query, current_entries=changed)
    assert (
        rebuilt.manifest_sha256 != study.manifest_sha256
        and rebuilt.identity != study.identity
    )
    assert {entries[i]["work_key"] for i in before["candidate_ordinals"]} == {
        changed[i]["work_key"] for i in after["candidate_ordinals"]
    }
    assert before["candidate_ordinals"] == [1, 6, 10] and after[
        "candidate_ordinals"
    ] == [0, 6, 10]


def test_supported_new_query_reuses_current_asset_without_claiming_run_resume(
    entries, study
):
    first, second = declaration()["queries"][:2]
    a = study.lookup(first, current_entries=entries)
    b = study.lookup(second, current_entries=entries)
    assert (
        a["complete"] and b["complete"] and a["asset_identity"] == b["asset_identity"]
    )
    assert a["candidate_ordinals"] != b["candidate_ordinals"]
