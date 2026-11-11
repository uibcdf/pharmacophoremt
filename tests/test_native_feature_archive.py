"""Native archive science, explicit source ordinals and real publication recovery."""

import hashlib
import importlib
import json
import multiprocessing
import os
import shutil
import signal
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from test_feature_archive_store import publication_child
from test_feature_asset_view import archive as archive
from test_feature_asset_view import bundle, identity, install
from test_feature_asset_view import originals as originals
from test_native_feature_payload import captured as captured
from test_native_feature_payload import encode, inventory

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.screening import reuse_feature_inventories
from pharmacophoremt_features import (
    FeatureAssetError,
    FeatureAssetRecord,
    FeatureAssetStore,
    FeatureAssetView,
    FeatureInventoryPayload,
    _schema,
)
from pharmacophoremt_features import _native_archive_schema as spec
from pharmacophoremt_results import canonical_json
from phmt_test_support.feature_snapshot import FeatureSnapshotStudy
from phmt_test_support.feature_snapshot_case import projection

PROFILE = "native-classical-v1"


def reuse(view, families, **kwargs):
    return reuse_feature_inventories(
        view,
        families,
        expected_generation=view.generation,
        payload_profile=PROFILE,
        **kwargs,
    )


@pytest.fixture(scope="module")
def native_originals(tmp_path_factory, captured):
    root = tmp_path_factory.mktemp("native-archive-originals")
    rows = []
    records = []
    for entry in captured:
        study = FeatureSnapshotStudy(entry["snapshot"])
        info = study.describe()
        native = study.decode_inventory()
        parent = {
            k: info["parent"][k]
            for k in (
                "source_key",
                "occurrence_key",
                "artifact_sha256",
                "artifact_bytes",
                "n_atoms",
                "preparation",
            )
        }
        parent["mapping_policy"] = "caller-declared-local-atom-axis@1"
        payload = encode(
            native,
            info["request"]["features"],
            parent=parent,
            extraction_producer=info["producer"],
        )
        record = FeatureAssetRecord.from_payload(entry["work_key"], payload)
        rows.append(
            {
                "metadata": record.describe(),
                "raw": payload.to_bytes(),
                "inventory": native,
                "historical_original": entry["snapshot"],
            }
        )
        records.append(record)
    with FeatureAssetStore.create(root / "store", payload_profile=PROFILE) as store:
        generation = store.stage_records(records)
        store.publish(generation, expected_current=None)
    return root / "store", rows


@pytest.fixture
def native_archive(native_originals, tmp_path):
    root = tmp_path / "native-store"
    shutil.copytree(native_originals[0], root)
    return root


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("ordinal", range(11))
def test_all_original_native_bytes_quantities_maps_and_versions(
    native_archive, native_originals, unit, ordinal
):
    before = identity(native_archive)
    original = native_originals[1][ordinal]
    with (
        FeatureAssetView.open(native_archive) as view,
        puw.context(standard_units=[unit, "ps", "radians"]),
    ):
        policy = puw.configure.report()
        row = view.work_items(offset=ordinal, limit=1)["records"][0]
        families = row["extraction"]["evaluated_families"]
        result = reuse(view, families, work_keys=[row["work_key"]])
        restored = result["inventories"][0]
        assert projection(restored["inventory"]) == projection(original["inventory"])
        assert (
            restored["inventory"]["recognition"] == original["inventory"]["recognition"]
        )
        assert restored["inventory"].get("attribution") == original["inventory"].get(
            "attribution"
        )
        assert restored["work_ordinal"] == ordinal and restored["lineage"] == []
        assert restored["extraction"] == original["metadata"]["extraction"]
        assert view.snapshot_bytes(ordinal) == original["raw"]
        assert (
            view.payload_info(ordinal)["format"]
            == "pharmacophoremt.native-feature-payload@1"
        )
        assert view.summary()["schema"] == _schema.NATIVE_GENERATION_SCHEMA
        assert view.summary()["original_payloads_interpreted"]
        assert view.summary()["payload_interpretation_scope"] == "native-layout-only"
        assert not view.summary()["quantity_semantics_checked"]
        assert not result["report"]["molecular_origin_authenticated"]
        assert puw.configure.report() == policy
    assert identity(native_archive) == before


def test_default_ordinal_protection_and_explicit_subset_rebase(
    native_archive, tmp_path
):
    with FeatureAssetView.open(native_archive) as source:
        source_row = source.work_items(offset=1, limit=1)["records"][0]
        record = FeatureAssetRecord.from_view(
            source, 1, expected_generation=source.generation
        )
        expected = {k: v for k, v in source_row.items() if k != "work_ordinal"}
        anchor = record.describe()["lineage"][-1]
        assert anchor["generation"] == source.generation and anchor["work_ordinal"] == 1
        assert (
            anchor["record_sha256"]
            == hashlib.sha256(canonical_json(expected).encode()).hexdigest()
        )
        raw = source.snapshot_bytes(1)
    with FeatureAssetStore.create(
        tmp_path / "subset", payload_profile=PROFILE
    ) as store:
        with pytest.raises(FeatureAssetError) as caught:
            store.stage_records([record])
        assert caught.value.code == "PHMT-E337"
        assert store.current() is None and not list(
            (tmp_path / "subset/generations").iterdir()
        )
        candidate = store.stage_records([record], ordinal_policy="explicit-rebase@1")
        store.publish(candidate, expected_current=None)
        with store.view() as view:
            row = view.work_items()["records"][0]
            assert row["work_ordinal"] == 0 and row["lineage"] == [anchor]
            assert all(row[k] == source_row[k] for k in spec.KEYS)
            assert view.snapshot_bytes(0) == raw
            assert view.summary()["origin"]["ordinal_policy"] == "explicit-rebase@1"
            restored = reuse(view, row["extraction"]["evaluated_families"])[
                "inventories"
            ][0]
            assert restored["work_ordinal"] == 0 and restored["lineage"] == [anchor]


def test_reorder_requires_consent_and_preserves_every_original_binding(
    native_archive, tmp_path
):
    with FeatureAssetView.open(native_archive) as source:
        records = [
            FeatureAssetRecord.from_view(
                source, i, expected_generation=source.generation
            )
            for i in (1, 0)
        ]
    with FeatureAssetStore.create(
        tmp_path / "reordered", payload_profile=PROFILE
    ) as store:
        with pytest.raises(FeatureAssetError) as caught:
            store.stage_records(records)
        assert caught.value.code == "PHMT-E337"
        candidate = store.stage_records(records, ordinal_policy="explicit-rebase@1")
        with store.view(generation=candidate) as view:
            rows = view.work_items()["records"]
            assert [r["work_ordinal"] for r in rows] == [0, 1]
            assert [r["lineage"][-1]["work_ordinal"] for r in rows] == [1, 0]
            assert [view.snapshot_bytes(i) for i in (0, 1)] == [
                r.payload_bytes() for r in records
            ]


def test_whole_copy_preserves_rebased_rows_lineage_and_payloads(
    native_archive, tmp_path
):
    with FeatureAssetView.open(native_archive) as source:
        record = FeatureAssetRecord.from_view(
            source, 1, expected_generation=source.generation
        )
    with FeatureAssetStore.create(
        tmp_path / "rebased", payload_profile=PROFILE
    ) as store:
        candidate = store.stage_records([record], ordinal_policy="explicit-rebase@1")
        store.publish(candidate, expected_current=None)
        borrowed = store.view()
    with (
        borrowed,
        FeatureAssetStore.create(tmp_path / "copy", payload_profile=PROFILE) as copy,
    ):
        candidate = copy.stage(borrowed, expected_generation=borrowed.generation)
        copy.publish(candidate, expected_current=None)
        detached = copy.view()
        assert detached.work_items()["records"] == borrowed.work_items()["records"]
        assert detached.snapshot_bytes(0) == borrowed.snapshot_bytes(0)
        assert detached.summary()["origin"]["generation"] == borrowed.generation
    assert detached.work_items()["records"][0]["lineage"][-1]["work_ordinal"] == 1
    detached.close()


@pytest.mark.parametrize("status", ["failed", "partial", "unsupported", "unattempted"])
def test_incomplete_states_survive_relocation_and_never_publish(tmp_path, status):
    cause = {"type": "original", "reason": "not evaluated"}
    record = FeatureAssetRecord.incomplete(
        "literal:α", "nm", "1 nm", status=status, cause=cause
    )
    cause.clear()
    assert record.payload_bytes() is None
    root = tmp_path / "incomplete"
    with FeatureAssetStore.create(root, payload_profile=PROFILE) as store:
        candidate = store.stage_records([record])
        with store.view(generation=candidate) as view:
            assert view.summary()["status_counts"][status] == 1
            assert (
                view.inspect(["hb donor"])["decision"]["action"]
                == "resolve_incomplete_extraction"
            )
            with pytest.raises(FeatureAssetError) as caught:
                reuse(view, ["hb donor"])
            assert caught.value.code == "PHMT-E306"
            borrowed = FeatureAssetRecord.from_view(
                view, 0, expected_generation=candidate
            )
        with pytest.raises(FeatureAssetError) as caught:
            store.publish(candidate, expected_current=None)
        assert caught.value.code == "PHMT-E326" and store.current() is None
    moved = tmp_path / "relocated"
    root.rename(moved)
    with FeatureAssetStore.open(moved) as store:
        candidate2 = store.stage_records([borrowed])
        with store.view(generation=candidate2) as view:
            row = view.work_items()["records"][0]
            assert row["cause"] == {"type": "original", "reason": "not evaluated"}
            assert row["lineage"][-1]["generation"] == candidate


def test_empty_generation_and_evaluated_empty_are_distinct(tmp_path):
    native = inventory()
    native["features"] = []
    record = FeatureAssetRecord.from_payload(
        "empty evaluated", encode(native, ["hb donor"])
    )
    with FeatureAssetStore.create(tmp_path / "empty", payload_profile=PROFILE) as store:
        first = store.stage_records([])
        store.publish(first, expected_current=None)
        with store.view() as view:
            result = reuse(view, ["hb donor"])
            assert (
                result["inventories"] == []
                and not result["report"]["quantity_semantics_checked"]
            )
        candidate = store.stage_records([record])
        store.publish(candidate, expected_current=first)
        with store.view() as view:
            result = reuse(view, ["hb donor"])
            assert result["inventories"][0]["inventory"]["features"] == []
            assert view.inspect(["hb donor"])["records"][0]["declared_counts"] == {
                "hb donor": 0
            }
            with pytest.raises(FeatureAssetError) as caught:
                reuse(view, ["hb acceptor"])
            assert caught.value.code == "PHMT-E309"


def test_exact_literal_keys_repetition_and_independent_record_ownership(tmp_path):
    payload = encode()
    keys = ["nm", "1 nm", " A ", "A\u0301", "Á"]
    records = [FeatureAssetRecord.from_payload(k, payload) for k in keys]
    info = records[0].describe()
    info["extraction"]["parent"].clear()
    assert records[0].describe()["source_key"] == "nm"
    with FeatureAssetStore.create(
        tmp_path / "literals", payload_profile=PROFILE
    ) as store:
        candidate = store.stage_records(records)
        store.publish(candidate, expected_current=None)
        with store.view() as view:
            assert view.summary()["unique_payload_count"] == 1
            assert [r["work_key"] for r in view.work_items()["records"]] == keys
            assert reuse(view, ["hb donor"], work_keys=["1 nm", "nm"])["report"][
                "selection_ordinals"
            ] == [0, 1]
        with pytest.raises(FeatureAssetError) as caught:
            store.stage_records([records[0], records[0]])
        assert caught.value.code == "PHMT-E335" and store.current() == candidate


def test_cross_profile_operations_refuse_without_converting_originals(
    archive, tmp_path
):
    before = identity(archive)
    with (
        FeatureAssetView.open(archive) as old,
        FeatureAssetStore.create(
            tmp_path / "native", payload_profile=PROFILE
        ) as native,
    ):
        with pytest.raises(FeatureAssetError) as caught:
            FeatureAssetRecord.from_view(old, 0, expected_generation=old.generation)
        assert caught.value.code == "PHMT-E336"
        with pytest.raises(FeatureAssetError) as caught:
            native.stage(old, expected_generation=old.generation)
        assert caught.value.code == "PHMT-E336"
        candidate = native.stage_records(
            [FeatureAssetRecord.from_payload("new", encode())]
        )
        native.publish(candidate, expected_current=None)
        with (
            native.view() as view,
            FeatureAssetStore.create(
                tmp_path / "legacy", payload_profile="snapshot-study-v1"
            ) as legacy,
        ):
            with pytest.raises(FeatureAssetError) as caught:
                legacy.stage(view, expected_generation=view.generation)
            assert caught.value.code == "PHMT-E336"
            with pytest.raises(FeatureAssetError) as caught:
                legacy.stage_records([])
            assert caught.value.code == "PHMT-E336"
            with pytest.raises(FeatureAssetError) as caught:
                reuse_feature_inventories(
                    view,
                    ["hb donor"],
                    expected_generation=view.generation,
                    payload_profile="snapshot-study-v1",
                )
            assert caught.value.code == "PHMT-E336"
    assert identity(archive) == before


@pytest.mark.parametrize("mode", ["unit", "field", "seal", "charge"])
def test_structurally_readable_native_record_never_grants_scientific_staging(
    mode, tmp_path
):
    value = json.loads(encode().to_bytes())
    row = value["payload"]["inventory"]["features"][0]
    if mode == "seal":
        row["center"]["digest"] = "0" * 64
    elif mode == "charge":
        value["payload"]["inventory"]["features"][4]["charge"] = (
            puw.QuantityRecord.from_quantity(
                puw.quantity(-1.0, "e"), field="features[4].charge"
            ).to_dict()
        )
    else:
        row["center"] = puw.QuantityRecord.from_quantity(
            puw.quantity([1.0, 2.0, 3.0], "ps" if mode == "unit" else "nm"),
            field="other" if mode == "field" else "features[0].center",
        ).to_dict()
    value["payload_sha256"] = hashlib.sha256(
        canonical_json(value["payload"]).encode()
    ).hexdigest()
    payload = FeatureInventoryPayload.from_bytes(
        canonical_json(value).encode(), payload_profile=PROFILE
    )
    record = FeatureAssetRecord.from_payload("invalid", payload)
    assert not record.describe()["extraction"]["quantity_semantics_checked"]
    with FeatureAssetStore.create(
        tmp_path / "invalid", payload_profile=PROFILE
    ) as store:
        with pytest.raises(FeatureAssetError) as caught:
            store.stage_records([record])
        assert caught.value.code == "PHMT-E332"
        assert store.current() is None and not list(
            (tmp_path / "invalid/generations").iterdir()
        )
        assert store.attempts()[0]["state"] == "raised"


def test_publication_and_retry_call_the_same_fresh_native_validator(
    tmp_path, monkeypatch
):
    payload = encode()
    record = FeatureAssetRecord.from_payload("new", payload)
    calls = []
    original = FeatureInventoryPayload.to_inventory

    def observed(self, **kwargs):
        calls.append(kwargs)
        return original(self, **kwargs)

    monkeypatch.setattr(FeatureInventoryPayload, "to_inventory", observed)
    with FeatureAssetStore.create(
        tmp_path / "validated", payload_profile=PROFILE
    ) as store:
        candidate = store.stage_records([record])
        assert len(calls) == 1
        store.publish(candidate, expected_current=None)
        assert len(calls) == 2
        with store.view() as view:
            borrowed = FeatureAssetRecord.from_view(
                view, 0, expected_generation=candidate
            )
            assert len(calls) == 2
            assert not borrowed.describe()["extraction"]["quantity_semantics_checked"]


@pytest.mark.parametrize(
    "change",
    [
        lambda row: row["extraction"]["coverage"]["hb donor"].update(count=True),
        lambda row: row.update(source_key="other"),
        lambda row: row.update(
            lineage=[
                {
                    "generation": "a" * 64,
                    "work_ordinal": True,
                    "record_sha256": "b" * 64,
                    "work_key": row["work_key"],
                    "source_key": row["source_key"],
                    "occurrence_key": row["occurrence_key"],
                }
            ]
        ),
        lambda row: row.update(extra=None),
    ],
)
def test_resealed_native_generation_metadata_and_lineage_refuse(native_archive, change):
    value = bundle(native_archive)
    change(value["records"][1])
    install(native_archive, value, store_schema=_schema.NATIVE_STORE_SCHEMA)
    with pytest.raises(FeatureAssetError) as caught:
        FeatureAssetView.open(native_archive)
    assert caught.value.code == "PHMT-E335"


@pytest.mark.parametrize(
    "change",
    [
        lambda row: row.update(schema="pharmacophoremt.feature-archive-attempt@1"),
        lambda row: row.update(record_count=True),
        lambda row: row.update(ordinal_policy="auto"),
    ],
)
def test_native_receipt_profile_and_assembly_context_are_checked(
    native_archive, change
):
    path = next(
        p
        for p in (native_archive / "attempts").glob("*.started.json")
        if json.loads(p.read_text())["operation"] == "stage_records"
    )
    value = json.loads(path.read_bytes())
    change(value)
    path.write_bytes(canonical_json(value).encode())
    with pytest.raises(FeatureAssetError) as caught:
        FeatureAssetStore.open(native_archive)
    assert caught.value.code == "PHMT-E325"


def test_finite_lineage_never_trims_older_origins(tmp_path):
    record = FeatureAssetRecord.from_payload("original", encode())
    with FeatureAssetStore.create(
        tmp_path / "lineage", payload_profile=PROFILE
    ) as store:
        current = store.stage_records([record])
        store.publish(current, expected_current=None)
        previous = []
        for count in range(1, 17):
            with store.view() as view:
                record = FeatureAssetRecord.from_view(
                    view, 0, expected_generation=current
                )
            lineage = record.describe()["lineage"]
            assert len(lineage) == count and lineage[:-1] == previous
            previous = lineage
            candidate = store.stage_records([record])
            store.publish(candidate, expected_current=current)
            current = candidate
        with store.view() as view:
            with pytest.raises(FeatureAssetError) as caught:
                FeatureAssetRecord.from_view(view, 0, expected_generation=current)
            assert caught.value.code == "PHMT-E338"
            assert view.work_items()["records"][0]["lineage"] == previous


@pytest.mark.parametrize("count", [64, 65])
def test_explicit_record_count_budget_and_maximum(tmp_path, count):
    payload = encode()
    records = [FeatureAssetRecord.from_payload(str(i), payload) for i in range(count)]
    with FeatureAssetStore.create(
        tmp_path / "budget", payload_profile=PROFILE
    ) as store:
        if count == 65:
            with pytest.raises(FeatureAssetError) as caught:
                store.stage_records(records)
            assert caught.value.code == "PHMT-E313" and store.attempts() == []
        else:
            candidate = store.stage_records(records)
            store.publish(candidate, expected_current=None)
            with store.view() as view:
                assert view.summary()["record_count"] == 64


def test_lazy_or_wrong_typed_record_arguments_are_not_consumed(tmp_path):
    def forbidden():
        raise AssertionError("An unbounded input must never be consumed")
        yield None

    with FeatureAssetStore.create(tmp_path / "args", payload_profile=PROFILE) as store:
        for value in (forbidden(), [{}], None):
            with pytest.raises(FeatureAssetError) as caught:
                store.stage_records(value)
            assert caught.value.code == "PHMT-E301"
        with pytest.raises(FeatureAssetError) as caught:
            store.stage_records([], ordinal_policy="auto")
        assert caught.value.code == "PHMT-E301"


def test_actual_reference_capture_adds_no_extraction_credit(native_archive, tmp_path):
    import ackredit

    with (
        ackredit.session("native-archive"),
        ackredit.capture("archive-and-reading") as run,
    ):
        before = ackredit.get_attribution().to_dict()
        with (
            FeatureAssetView.open(native_archive) as source,
            FeatureAssetStore.create(
                tmp_path / "credited", payload_profile=PROFILE
            ) as store,
        ):
            record = FeatureAssetRecord.from_view(
                source, 1, expected_generation=source.generation
            )
            candidate = store.stage_records(
                [record], ordinal_policy="explicit-rebase@1"
            )
            store.publish(candidate, expected_current=None)
            with store.view() as view:
                families = record.describe()["extraction"]["evaluated_families"]
                result = reuse(view, families)["inventories"][0]["inventory"]
                assert result["attribution"]["host_references"]
        assert ackredit.get_attribution().to_dict() == before
    assert (
        not run.attribution.to_dict()["items"] and not run.attribution.to_dict()["uses"]
    )


@pytest.mark.parametrize("side", ["before", "after"])
@pytest.mark.parametrize("signum", [signal.SIGTERM, signal.SIGKILL])
def test_real_native_publication_interruption_and_linked_recovery(
    native_archive, tmp_path, side, signum
):
    with FeatureAssetStore.open(native_archive) as store:
        first = store.current()
        old = store.view()
        records = [
            FeatureAssetRecord.from_view(old, i, expected_generation=first)
            for i in range(old.summary()["record_count"])
        ]
        records.append(FeatureAssetRecord.from_payload("explicit repeat", encode()))
        candidate = store.stage_records(records)
    context = multiprocessing.get_context("spawn")
    parent, child = context.Pipe(duplex=False)
    process = context.Process(
        target=publication_child, args=(native_archive, candidate, first, side, child)
    )
    process.start()
    try:
        assert parent.poll(15), "Owned child did not reach native publication boundary"
        assert parent.recv() == "at-" + side
        os.kill(process.pid, signum)
        process.join(10)
        assert not process.is_alive()
    finally:
        if process.is_alive():
            process.terminate()
            process.join(5)
        parent.close()
        child.close()
    with FeatureAssetStore.open(native_archive) as store:
        row = store.attempts()[-1]
        assert row["state"] == "unknown"
        original = deepcopy(row)
        report = store.inspect_recovery(row["attempt"])
        assert not report["candidate_native_validation_performed"]
        assert store.current() == (candidate if side == "after" else first)
        if side == "before":
            assert report["decision"]["action"] == "retry_available"
            assert store.retry_publication(row["attempt"]) == candidate
        else:
            assert report["decision"]["action"] == "already_current"
        assert (
            next(r for r in store.attempts() if r["attempt"] == row["attempt"])
            == original
        )
        assert store.current() == candidate
        assert old.generation == first and old.summary()["record_count"] == 11
    old.close()


def test_fresh_native_record_reader_and_recovery_are_scientifically_cold(
    native_archive, tmp_path
):
    import pharmacophoremt_features

    roots = [str(Path(pharmacophoremt_features.__file__).resolve().parent.parent)]
    roots.extend(
        str(Path(importlib.import_module(n).__file__).resolve().parent.parent)
        for n in ("argdigest", "smonitor", "depdigest")
    )
    code = r"""
import importlib.abc,json,sys
sys.path[:0]=json.loads(sys.argv[1])
blocked={'pharmacophoremt','molsysmt','numpy','scipy','rdkit','pyunitwizard','ackredit','phmt_test_support'}
attempts=[]
class NoScience(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0] in blocked:
            attempts.append(fullname)
            raise ModuleNotFoundError('Scientific imports blocked',name=fullname)
sys.meta_path.insert(0,NoScience())
import smonitor
manager=smonitor.configure(profile='agent',level='ERROR',capture_logging=False,capture_warnings=False,args_summary=False,trace_depth=0)
policy=manager.config
from pharmacophoremt_features import FeatureAssetView,FeatureAssetRecord
assert 'pharmacophoremt_features._writer' not in sys.modules
with FeatureAssetView.open(sys.argv[2]) as view:
    record=FeatureAssetRecord.from_view(view,1,expected_generation=view.generation)
    assert record.describe()['lineage'][-1]['work_ordinal']==1
    assert not record.describe()['extraction']['quantity_semantics_checked']
    assert view.summary()['payload_interpretation_scope']=='native-layout-only'
    assert not view.summary()['quantity_semantics_checked']
from pharmacophoremt_features import FeatureAssetStore
with FeatureAssetStore.open(sys.argv[2]) as store:
    row=store.attempts()[-1]
    assert store.inspect_recovery(row['attempt'])['decision']['action']=='already_current'
assert manager.config is policy and not attempts and not(blocked & set(sys.modules))
print(json.dumps({'scientific_imports':0,'policy_preserved':True}))
"""
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-S",
            "-B",
            "-c",
            code,
            json.dumps(roots),
            str(native_archive),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["scientific_imports"] == 0


@pytest.mark.parametrize(
    "mode",
    [
        "empty-key",
        "surrogate-key",
        "wrong-payload",
        "ready-status",
        "wrong-cause",
        "boolean-ordinal",
        "missing-ordinal",
        "wrong-generation",
    ],
)
def test_record_factory_argument_and_source_identity_contracts(native_archive, mode):
    with FeatureAssetView.open(native_archive) as view:
        with pytest.raises(FeatureAssetError) as caught:
            if mode == "empty-key":
                FeatureAssetRecord.from_payload("", encode())
            elif mode == "surrogate-key":
                FeatureAssetRecord.from_payload("\ud800", encode())
            elif mode == "wrong-payload":
                FeatureAssetRecord.from_payload("work", {})
            elif mode in ("ready-status", "wrong-cause"):
                FeatureAssetRecord.incomplete(
                    "work",
                    "source",
                    "occurrence",
                    status="ready" if mode == "ready-status" else "partial",
                    cause={}
                    if mode == "wrong-cause"
                    else {"type": "pending", "reason": "unknown"},
                )
            else:
                FeatureAssetRecord.from_view(
                    view,
                    True
                    if mode == "boolean-ordinal"
                    else 99
                    if mode == "missing-ordinal"
                    else 0,
                    expected_generation="0" * 64
                    if mode == "wrong-generation"
                    else view.generation,
                )
        assert caught.value.code == (
            "PHMT-E308" if mode == "wrong-generation" else "PHMT-E301"
        )


def test_actual_native_ordinal_diagnostic_respects_application_capture(
    native_archive, tmp_path
):
    import smonitor
    from smonitor.handlers import MemoryHandler

    with FeatureAssetView.open(native_archive) as view:
        record = FeatureAssetRecord.from_view(
            view, 1, expected_generation=view.generation
        )
    manager = smonitor.get_manager()
    handler = MemoryHandler()
    manager.add_handler(handler)
    try:
        with (
            smonitor.diagnostic_scope(safe_extra={"operation": "native-assembly"}),
            FeatureAssetStore.create(
                tmp_path / "capture", payload_profile=PROFILE
            ) as store,
        ):
            with pytest.raises(FeatureAssetError) as caught:
                store.stage_records([record])
            assert caught.value.code == "PHMT-E337"
        assert any(event.get("code") == "PHMT-E337" for event in handler.events)
        assert "admission_sha256" not in str(handler.events)
        assert "host_references" not in str(handler.events)
    finally:
        manager.remove_handler(handler)


def test_repeated_original_budget_refuses_before_any_scientific_decoding(
    tmp_path, monkeypatch
):
    native = inventory()
    native["features"] = [deepcopy(native["features"][0]) for _ in range(64)]
    payload = encode(native, extraction_producer={"padding": "x" * 125000})
    count = _schema.MAX_NATIVE_REPEATED_BYTES // len(payload.to_bytes()) + 1
    assert 2 <= count <= 64
    records = [FeatureAssetRecord.from_payload(str(i), payload) for i in range(count)]

    def forbidden(*args, **kwargs):
        raise AssertionError("Over-budget original bytes must not decode")

    monkeypatch.setattr(FeatureInventoryPayload, "to_inventory", forbidden)
    with FeatureAssetStore.create(
        tmp_path / "repeated-budget", payload_profile=PROFILE
    ) as store:
        with pytest.raises(FeatureAssetError) as caught:
            store.stage_records(records)
        assert caught.value.code == "PHMT-E313" and store.attempts() == []


def test_native_payload_table_budget_precedes_original_parsing(native_archive):
    value = bundle(native_archive)
    original = next(iter(value["payloads"].values()))
    value["payloads"] = {format(i, "064x"): original for i in range(65)}
    install(native_archive, value, store_schema=_schema.NATIVE_STORE_SCHEMA)
    with pytest.raises(FeatureAssetError) as caught:
        FeatureAssetView.open(native_archive)
    assert caught.value.code == "PHMT-E313"


def test_native_assembly_attempt_quota_preserves_history_and_candidate(tmp_path):
    with FeatureAssetStore.create(
        tmp_path / "attempt-quota", payload_profile=PROFILE
    ) as store:
        candidates = [store.stage_records([]) for _ in range(64)]
        assert len(set(candidates)) == 1
        before = store.attempts()
        assert len(before) == 64 and all(r["state"] == "completed" for r in before)
        with pytest.raises(FeatureAssetError) as caught:
            store.stage_records([])
        assert caught.value.code == "PHMT-E323" and store.attempts() == before
        with store.view(generation=candidates[0]) as view:
            assert view.summary()["record_count"] == 0


def test_borrowed_record_refuses_a_mismatched_public_page_ordinal(
    native_archive, monkeypatch
):
    with FeatureAssetView.open(native_archive) as view:
        original = view.work_items

        def wrong_page(*args, **kwargs):
            result = original(*args, **kwargs)
            result["records"][0]["work_ordinal"] = 0
            return result

        monkeypatch.setattr(view, "work_items", wrong_page)
        with pytest.raises(FeatureAssetError) as caught:
            FeatureAssetRecord.from_view(view, 1, expected_generation=view.generation)
        assert caught.value.code == "PHMT-E335"
