"""Actual original-payload reuse, unit handshakes, maps and refusal boundaries."""

import base64
import hashlib
import json
from copy import deepcopy

import pytest
from test_feature_asset_view import archive as archive
from test_feature_asset_view import bundle, identity, install
from test_feature_asset_view import originals as originals

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.screening import reuse_feature_inventories
from pharmacophoremt_features import FeatureAssetError, FeatureAssetView
from pharmacophoremt_results import canonical_json
from phmt_test_support.feature_snapshot import FeatureSnapshotStudy
from phmt_test_support.feature_snapshot_case import projection


def reuse(view, families, **kwargs):
    return reuse_feature_inventories(
        view,
        families,
        expected_generation=view.generation,
        payload_profile="snapshot-study-v1",
        **kwargs,
    )


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("ordinal", range(11))
def test_original_full_inventories_maps_quantities_and_provenance(
    archive, originals, unit, ordinal
):
    before = identity(archive)
    with (
        FeatureAssetView.open(archive) as view,
        puw.context(standard_units=[unit, "ps", "radians"]),
    ):
        record = view.work_items(offset=ordinal, limit=1)["records"][0]
        original = view.snapshot_bytes(ordinal)
        policy = puw.configure.report()
        result = reuse(
            view,
            record["extraction"]["requested_families"],
            work_keys=[record["work_key"]],
        )
        row = result["inventories"][0]
        assert row["work_ordinal"] == ordinal and row["work_key"] == record["work_key"]
        assert (
            row["source_key"] == record["source_key"]
            and row["occurrence_key"] == record["occurrence_key"]
        )
        assert row["extraction"] == record["extraction"]
        oracle = FeatureSnapshotStudy(original).decode_inventory()
        assert projection(row["inventory"]) == projection(oracle)
        assert row["inventory"]["recognition"] == oracle["recognition"]
        assert row["inventory"].get("attribution") == oracle.get("attribution")
        assert puw.configure.report() == policy
        assert (
            view.snapshot_bytes(ordinal)
            == original
            == originals[2][ordinal]["snapshot"]
        )
        assert result["report"]["quantity_semantics_checked"]
        assert not result["report"]["molecular_origin_authenticated"]
        assert (
            result["report"]["query_admitted"]
            is result["report"]["match_outcome"]
            is None
        )
    assert identity(archive) == before


def test_literal_keys_global_order_complete_inventory_and_fresh_ownership(archive):
    with FeatureAssetView.open(archive) as view:
        a = reuse(
            view, ["positive charge", "hb donor"], work_keys=["repeat=α", "1 nm", "nm"]
        )
        assert a["report"]["selection_ordinals"] == [1, 6, 10]
        first = a["inventories"][0]
        original = deepcopy(projection(first["inventory"]))
        first["inventory"]["features"][0]["atom_indices"].clear()
        first["extraction"]["producer"]["versions"].clear()
        again = reuse(view, ["hb donor"], work_keys=["nm"])
        assert projection(again["inventories"][0]["inventory"]) == original
        assert again["inventories"][0]["extraction"]["producer"]["versions"]
        assert any(
            row["kind"] != "hb donor"
            for row in again["inventories"][0]["inventory"]["features"]
        )


def test_empty_selection_does_not_claim_quantity_validation(archive):
    with FeatureAssetView.open(archive) as view:
        result = reuse(view, ["hb donor"], work_keys=[])
        assert result["inventories"] == [] and result["report"]["selected_count"] == 0
        assert not result["report"]["quantity_semantics_checked"]
        assert result["report"]["decision"]["action"] == "empty_selection"


@pytest.mark.parametrize(
    "argument,value",
    [
        ("view", {}),
        ("required_families", []),
        ("required_families", ["unknown"]),
        ("expected_generation", None),
        ("expected_generation", "current"),
        ("payload_profile", None),
        ("payload_profile", "auto"),
        ("work_keys", ["nm", "nm"]),
        ("work_keys", "nm"),
    ],
)
def test_argument_contracts_are_catalogued(archive, argument, value):
    with FeatureAssetView.open(archive) as view:
        args = dict(
            view=view,
            required_families=["hb donor"],
            expected_generation=view.generation,
            payload_profile="snapshot-study-v1",
            work_keys=["nm"],
        )
        args[argument] = value
        with pytest.raises(FeatureAssetError) as caught:
            reuse_feature_inventories(**args)
        assert caught.value.code == "PHMT-E301"


@pytest.mark.parametrize(
    "mode,code",
    [
        ("generation", "308"),
        ("closed", "304"),
        ("unknown-key", "305"),
        ("missing-family", "309"),
    ],
)
def test_generation_lifetime_and_selected_coverage(archive, mode, code):
    with FeatureAssetView.open(archive) as view:
        if mode == "closed":
            view.close()
        with pytest.raises(FeatureAssetError) as caught:
            if mode == "generation":
                reuse_feature_inventories(
                    view,
                    ["hb donor"],
                    expected_generation="a" * 64,
                    payload_profile="snapshot-study-v1",
                )
            else:
                reuse(
                    view,
                    ["hb donor"],
                    work_keys=["unknown"] if mode == "unknown-key" else None,
                )
        assert caught.value.code == "PHMT-E" + code


def rewritten(archive, change, ordinal=1):
    value = bundle(archive)
    row = value["records"][ordinal]
    old = row["payload_sha256"]
    original = value["payloads"][old]
    document = json.loads(base64.b64decode(original["data"]))
    change(document)
    document["payload_sha256"] = hashlib.sha256(
        canonical_json(document["payload"]).encode()
    ).hexdigest()
    raw = canonical_json(document).encode()
    new = hashlib.sha256(raw).hexdigest()
    row["payload_sha256"] = new
    value["payloads"][new] = {
        "format": original["format"],
        "data": base64.b64encode(raw).decode(),
    }
    if not any(r.get("payload_sha256") == old for r in value["records"]):
        del value["payloads"][old]
    install(archive, value)


@pytest.mark.parametrize(
    "change,code",
    [
        (lambda d: d.update(schema="unknown"), "307"),
        (lambda d: d["payload"]["parent"].update(preparation="different"), "310"),
        (lambda d: d["payload"]["producer"].update(runtime_version="new"), "310"),
        (lambda d: d["payload"]["request"].update(chemical_state=False), "310"),
        (lambda d: d["payload"]["parent"].update(chemical_state=False), "310"),
        (
            lambda d: d["payload"]["inventory"]["features"][0].update(
                geometry_atom_indices=[999]
            ),
            "310",
        ),
        (lambda d: d["payload"]["inventory"]["features"].pop(), "310"),
    ],
)
def test_valid_archive_bytes_do_not_admit_false_payload_metadata(archive, change, code):
    rewritten(archive, change)
    with FeatureAssetView.open(archive) as view:
        assert view.summary()["record_count"] == 11
        with pytest.raises(FeatureAssetError) as caught:
            reuse(view, ["hb donor"], work_keys=["nm"])
        assert caught.value.code == "PHMT-E" + code


@pytest.mark.parametrize("mode", ["unit", "field", "shape", "seal", "zero-direction"])
def test_quantity_owner_rejects_corrupt_or_wrong_semantics(archive, mode):
    def change(document):
        row = document["payload"]["inventory"]["features"][0]
        field = "direction" if mode == "zero-direction" else "center"
        value = (
            [0, 0, 0]
            if mode == "zero-direction"
            else ([1, 2] if mode == "shape" else [1, 2, 3])
        )
        unit = (
            "dimensionless"
            if field == "direction"
            else ("ps" if mode == "unit" else "nm")
        )
        record = puw.QuantityRecord.from_quantity(
            puw.quantity(value, unit),
            field="wrong" if mode == "field" else f"features[0].{field}",
        ).to_dict()
        if mode == "seal":
            record["digest"] = "0" * 64
        row[field] = record

    rewritten(archive, change)
    with FeatureAssetView.open(archive) as view:
        with pytest.raises(FeatureAssetError) as caught:
            reuse(view, ["hb donor"], work_keys=["nm"])
        assert caught.value.code == "PHMT-E311" and caught.value.__cause__ is not None


def test_reading_keeps_original_references_without_new_credit(archive):
    import ackredit

    with (
        ackredit.session("native-feature-reading"),
        ackredit.capture("reader") as captured,
    ):
        before = ackredit.get_attribution().to_dict()
        with FeatureAssetView.open(archive) as view:
            result = reuse(view, ["hb donor"], work_keys=["nm"])
        assert result["inventories"][0]["inventory"]["attribution"]["host_references"]
        assert ackredit.get_attribution().to_dict() == before
    assert (
        not captured.attribution.to_dict()["items"]
        and not captured.attribution.to_dict()["uses"]
    )


@pytest.mark.parametrize("status", ["partial", "failed", "unsupported", "unattempted"])
def test_incomplete_manifest_and_complete_selected_subset_remain_distinct(
    archive, status
):
    value = bundle(archive)
    old = value["records"][0]["payload_sha256"]
    value["records"][0] = {
        **{
            k: value["records"][0][k]
            for k in ("work_key", "source_key", "occurrence_key")
        },
        "status": status,
        "cause": {"type": "retained-original", "reason": "uncompleted"},
    }
    if not any(r.get("payload_sha256") == old for r in value["records"]):
        del value["payloads"][old]
    install(archive, value)
    with FeatureAssetView.open(archive) as view:
        with pytest.raises(FeatureAssetError) as caught:
            reuse(view, ["hb donor"])
        assert caught.value.code == "PHMT-E306"
        result = reuse(view, ["hb donor"], work_keys=["nm"])
        assert (
            not result["report"]["manifest_complete"]
            and result["report"]["selected_count"] == 1
        )


def test_actual_native_model_composition_does_not_extract_molecules(
    archive, monkeypatch
):
    from pharmacophoremt import modeler

    def forbidden(*args, **kwargs):
        raise AssertionError("Original feature reuse must not perform extraction")

    monkeypatch.setattr(modeler, "get_features", forbidden)
    with FeatureAssetView.open(archive) as view:
        inventory = reuse(view, ["hb donor"], work_keys=["nm"])["inventories"][0][
            "inventory"
        ]
    model = modeler.from_feature_inventory(inventory, radius="0.1 nm")
    assert model.n_interaction_sites == len(inventory["features"])


def test_actual_catalog_emission_respects_restrictive_application_capture(archive):
    import smonitor
    from smonitor.handlers import MemoryHandler

    manager = smonitor.get_manager()
    handler = MemoryHandler()
    manager.add_handler(handler)
    try:
        with (
            FeatureAssetView.open(archive) as view,
            smonitor.diagnostic_scope(safe_extra={"operation": "native-reuse"}),
        ):
            with pytest.raises(FeatureAssetError):
                reuse_feature_inventories(
                    view,
                    ["hb donor"],
                    expected_generation="a" * 64,
                    payload_profile="snapshot-study-v1",
                    work_keys=["nm"],
                )
        assert any(event.get("code") == "PHMT-E308" for event in handler.events)
        serialized = str(handler.events)
        assert (
            "b89340c6c33e6e053298779eca12f8ea2fe976d7e1b67fd54b288ac16748de0d"
            not in serialized
        )
        assert "recognition" not in serialized and "host_references" not in serialized
    finally:
        manager.remove_handler(handler)


@pytest.mark.parametrize("count", [64, 65])
def test_eager_record_limit_is_checked_before_any_decoding(archive, monkeypatch, count):
    from pharmacophoremt._private import feature_snapshot_v1

    value = bundle(archive)
    original = value["records"][1]
    value["records"] = [
        {**deepcopy(original), "work_key": f"literal:{i}"} for i in range(count)
    ]
    value["payloads"] = {
        original["payload_sha256"]: value["payloads"][original["payload_sha256"]]
    }
    install(archive, value)
    if count == 65:

        def forbidden(*args):
            raise AssertionError("Over-budget selections must not decode")

        monkeypatch.setattr(feature_snapshot_v1, "decode_snapshot", forbidden)
    with FeatureAssetView.open(archive) as view:
        if count == 65:
            with pytest.raises(FeatureAssetError) as caught:
                reuse(view, ["hb donor"])
            assert caught.value.code == "PHMT-E313"
        else:
            result = reuse(view, ["hb donor"])
            assert len(result["inventories"]) == 64
            assert result["report"]["selection_ordinals"] == list(range(64))


def test_missing_record_capability_is_not_a_molecular_fallback(archive, monkeypatch):
    monkeypatch.setattr(puw, "QuantityRecord", None)
    with FeatureAssetView.open(archive) as view:
        with pytest.raises(FeatureAssetError) as caught:
            reuse(view, ["hb donor"], work_keys=["nm"])
        assert caught.value.code == "PHMT-E312"


def test_repeated_original_bytes_count_toward_eager_budget(archive, monkeypatch):
    from pharmacophoremt._private import feature_snapshot_v1

    rewritten(
        archive,
        lambda d: d["payload"]["inventory"]["recognition"].update(
            budget_note="x" * 200000
        ),
    )
    value = bundle(archive)
    original = value["records"][1]
    payload = value["payloads"][original["payload_sha256"]]
    size = len(base64.b64decode(payload["data"]))
    count = (8 * 1024 * 1024) // size + 1
    assert 2 <= count <= 64
    value["records"] = [
        {**deepcopy(original), "work_key": f"repeated:{i}"} for i in range(count)
    ]
    value["payloads"] = {original["payload_sha256"]: payload}
    install(archive, value)

    def forbidden(*args):
        raise AssertionError("Byte budget must be checked before reconstruction")

    monkeypatch.setattr(feature_snapshot_v1, "decode_snapshot", forbidden)
    with FeatureAssetView.open(archive) as view:
        assert view.summary()["unique_payload_count"] == 1
        with pytest.raises(FeatureAssetError) as caught:
            reuse(view, ["hb donor"])
        assert caught.value.code == "PHMT-E313"
