"""Finite storage/lifetime controls using original captured inventories only."""

import hashlib
import json
import multiprocessing
import os
import signal
from copy import deepcopy
from pathlib import Path

import pytest

from pharmacophoremt_results import canonical_json
from phmt_test_support.feature_snapshot import FeatureSnapshotStudy
from phmt_test_support.feature_store import (
    FeatureStoreReaderStudy,
    FeatureStoreStudy,
)
from phmt_test_support.search_asset_contract import family_coverage
from phmt_test_support.typed_retrieval import load_entries


@pytest.fixture(scope="module")
def entries():
    return load_entries(os.environ.get("PHMT_RECEIVING_CONTEXT", "source"))


def records(entries):
    result = []
    for entry in entries:
        parent = FeatureSnapshotStudy(entry["snapshot"]).describe()["parent"]
        result.append(
            {
                "work_key": entry["work_key"],
                "source_key": parent["source_key"],
                "occurrence_key": parent["occurrence_key"],
                "status": "ready",
                "snapshot": entry["snapshot"],
            }
        )
    return result


def encode(value):
    return canonical_json(value).encode()


def changed_snapshot(raw, change):
    value = FeatureSnapshotStudy(raw).to_dict()
    change(value["payload"])
    value["payload_sha256"] = hashlib.sha256(encode(value["payload"])).hexdigest()
    return FeatureSnapshotStudy(encode(value)).to_bytes()


def seed(root, rows):
    with FeatureStoreStudy(root, create=True) as store:
        generation = store.seal(rows)
        store.publish(generation, expected_current=None)
    return generation


def test_original_bytes_order_aliases_and_payload_deduplication(entries, tmp_path):
    rows = records(entries)
    root = tmp_path / "store"
    generation = seed(root, rows)
    with FeatureStoreReaderStudy(root) as view:
        info = view.describe()
        assert info["generation"] == generation and info["unique_payloads"] == 10
        assert info["complete"] and info["scope"] == "captured-inventory-only"
        assert not info["quantity_semantics_validated_by_open"]
        assert (
            not info["molecular_origin_authenticated"]
            and not info["persisted_lookup_index"]
        )
        restored = list(view.entries())
        assert [r["snapshot"] for r in restored] == [e["snapshot"] for e in entries]
        assert [r["work_key"] for r in restored] == [e["work_key"] for e in entries]
        assert (
            restored[1]["source_key"] == "nm"
            and restored[1]["occurrence_key"] == "1 nm"
        )
        info["records"][0]["work_key"] = "changed by caller"
        restored[0]["work_key"] = "also changed"
        assert view.describe()["records"][0]["work_key"] == rows[0]["work_key"]
        assert (
            FeatureSnapshotStudy(view.snapshot(1)).to_dict()
            == FeatureSnapshotStudy(entries[1]["snapshot"]).to_dict()
        )
    assert (
        root / "generations" / (generation + ".json")
    ).stat().st_size < 4 * 1024 * 1024


def test_create_open_refuse_without_overwrite_or_autocreation(tmp_path):
    root = tmp_path / "missing"
    with pytest.raises(FileNotFoundError):
        FeatureStoreStudy(root)
    assert not root.exists()
    with FeatureStoreStudy(root, create=True) as store:
        assert store.current() is None
        with pytest.raises(ValueError, match="no published"):
            FeatureStoreReaderStudy(root)
        with pytest.raises(FileExistsError):
            FeatureStoreStudy(root, create=True)
    with FeatureStoreStudy(root):
        pass
    with pytest.raises(ValueError):
        FeatureStoreStudy(tmp_path / "bad-option", create="yes")
    assert not (tmp_path / "bad-option").exists()


@pytest.mark.parametrize("mutation", ["reorder", "alias", "unit-payload"])
def test_identity_tracks_order_literal_work_alias_and_original_payload(
    entries, tmp_path, mutation
):
    rows = records(entries)
    with FeatureStoreStudy(tmp_path / "store", create=True) as store:
        baseline = store.seal(rows)
        changed = deepcopy(rows)
        if mutation == "reorder":
            changed[1], changed[6] = changed[6], changed[1]
        elif mutation == "alias":
            changed[1]["work_key"] = "distinct literal=α"
        else:
            changed[1]["snapshot"] = entries[6]["snapshot"]
            parent = FeatureSnapshotStudy(changed[1]["snapshot"]).describe()["parent"]
            for key in ("source_key", "occurrence_key"):
                changed[1][key] = parent[key]
        assert store.seal(changed) != baseline
        assert store.seal(rows) == baseline


def test_relocation_reopen_and_pinned_old_reader(entries, tmp_path):
    root, moved = tmp_path / "first", tmp_path / "moved"
    rows = records(entries[:2])
    first = seed(root, rows)
    old = FeatureStoreReaderStudy(root)
    with FeatureStoreStudy(root) as store:
        newer = deepcopy(rows)
        newer[0]["work_key"] = "newer"
        second = store.seal(newer)
        store.publish(second, expected_current=first)
        assert old.describe()["generation"] == first
        assert old.snapshot(0) == rows[0]["snapshot"]
    root.rename(moved)
    with FeatureStoreReaderStudy(moved) as view:
        assert view.describe()["generation"] == second
    with FeatureStoreReaderStudy(moved, first) as view:
        assert view.describe()["generation"] == first
    assert old.inventory(1)["features"]
    old.close()


def test_close_releases_only_owned_resources_and_pending_iteration(entries, tmp_path):
    root = tmp_path / "store"
    writer = FeatureStoreStudy(root, create=True)
    generation = writer.seal(records(entries[:2]))
    writer.publish(generation, expected_current=None)
    reader = FeatureStoreReaderStudy(root)
    pending = reader.entries()
    assert next(pending)["work_key"] == entries[0]["work_key"]
    inventory = reader.inventory(1)
    writer.close()
    writer.close()
    assert reader.snapshot(1) == entries[1]["snapshot"]
    reader.close()
    reader.close()
    for operation in (
        reader.describe,
        reader.entries,
        lambda: reader.snapshot(0),
        lambda: reader.inventory(0),
        lambda: next(pending),
        writer.current,
        writer.attempts,
        lambda: writer.seal([]),
    ):
        with pytest.raises(ValueError, match="closed"):
            operation()
    assert inventory["features"]  # Detached caller-owned quantity inventory survives.
    with FeatureStoreStudy(root):
        pass


@pytest.mark.parametrize("status", ["failed", "partial", "unsupported", "unattempted"])
def test_incomplete_causes_seal_but_cannot_replace_current(entries, tmp_path, status):
    root = tmp_path / "store"
    first = seed(root, records(entries[:1]))
    cause = {
        "type": "analytical-control",
        "reason": "source extraction explicitly " + status,
    }
    rows = records(entries[:1]) + [
        {
            "work_key": "gap",
            "source_key": "source-gap",
            "occurrence_key": "repeat=α",
            "status": status,
            "cause": cause,
        }
    ]
    with FeatureStoreStudy(root) as store:
        candidate = store.seal(rows)
        cause["reason"] = "caller mutation"
        with FeatureStoreReaderStudy(root, candidate) as view:
            assert not view.describe()["complete"]
            assert view.describe()["records"][1]["cause"]["reason"].endswith(status)
            assert list(view.entries())[1]["status"] == status
            with pytest.raises(ValueError, match="no completed"):
                view.snapshot(1)
        with pytest.raises(ValueError, match="Incomplete"):
            store.publish(candidate, expected_current=first)
        assert store.current() == first
        failures = [r for r in store.attempts() if r["state"] == "raised"]
        assert len(failures) == 1 and "Incomplete" in failures[0]["terminal"]["reason"]


def test_explicit_empty_manifest_and_known_empty_family_keep_distinct_meanings(
    entries, tmp_path
):
    root = tmp_path / "store"
    empty = seed(root, [])
    with FeatureStoreReaderStudy(root) as view:
        assert view.describe()["complete"] and list(view.entries()) == []
    with FeatureStoreStudy(root) as store:
        candidate = store.seal(records(entries[:1]))
        store.publish(candidate, expected_current=empty)
    with FeatureStoreReaderStudy(root) as view:
        snapshot = FeatureSnapshotStudy(view.snapshot(0))
        assert family_coverage(snapshot, ["aromatic ring"])["known_counts"] == {
            "aromatic ring": 0
        }
        assert family_coverage(snapshot, ["hb donor"])["unobserved_families"] == [
            "hb donor"
        ]


@pytest.mark.parametrize(
    "mutation",
    [
        "duplicate",
        "parent",
        "unknown-field",
        "status",
        "cause",
        "too-many",
        "not-list",
        "no-bytes",
        "oversized",
    ],
)
def test_bad_input_refuses_without_publication(entries, tmp_path, mutation):
    rows = records(entries[:2])
    if mutation == "duplicate":
        rows[1]["work_key"] = rows[0]["work_key"]
    elif mutation == "parent":
        rows[1]["source_key"] = "another parent"
    elif mutation == "unknown-field":
        rows[0]["extra"] = True
    elif mutation == "status":
        rows[0]["status"] = "silently-empty"
    elif mutation == "cause":
        rows = [
            {
                "work_key": "x",
                "source_key": "x",
                "occurrence_key": "x",
                "status": "failed",
                "cause": {"reason": "lost type"},
            }
        ]
    elif mutation == "too-many":
        rows = rows * 7
    elif mutation == "not-list":
        rows = iter(rows)
    elif mutation == "oversized":
        rows[0]["snapshot"] = b"x" * (2 * 1024 * 1024 + 1)
    else:
        rows[0]["snapshot"] = bytearray(rows[0]["snapshot"])
    with FeatureStoreStudy(tmp_path / "store", create=True) as store:
        with pytest.raises(ValueError):
            store.seal(rows)
        assert store.current() is None
        assert list((tmp_path / "store/generations").iterdir()) == []


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_seal_rejects_wrong_dimension_before_install_and_preserves_old(
    entries, tmp_path, unit
):
    from pharmacophoremt import pyunitwizard as puw

    root = tmp_path / "store"
    first = seed(root, records(entries[:1]))
    rows = records(entries[1:2])
    bad = puw.QuantityRecord.from_quantity(
        puw.quantity([0.0, 0.0, 0.0], "ps"), field="features[0].center"
    ).to_dict()
    rows[0]["snapshot"] = changed_snapshot(
        rows[0]["snapshot"], lambda p: p["inventory"]["features"][0].update(center=bad)
    )
    old = FeatureStoreReaderStudy(root)
    with (
        FeatureStoreStudy(root) as store,
        puw.context(standard_units=[unit, "ps", "radians"]),
    ):
        with pytest.raises(Exception) as caught:
            store.seal(rows)
        assert (
            "dimension" in str(caught.value).lower()
            or "unit" in str(caught.value).lower()
        )
        assert store.current() == first and old.describe()["generation"] == first
        assert len(list((root / "generations").iterdir())) == 1
    old.close()


def test_publish_revalidates_quantities_and_stale_caller_refuses(
    entries, tmp_path, monkeypatch
):
    root = tmp_path / "store"
    first = seed(root, records(entries[:1]))
    with FeatureStoreStudy(root) as store:
        candidate = store.seal(records(entries[:2]))
        with pytest.raises(ValueError, match="Stale"):
            store.publish(candidate, expected_current=None)

        def refuse(self):
            raise ValueError("public quantity handshake refused")

        monkeypatch.setattr(FeatureSnapshotStudy, "decode_inventory", refuse)
        with pytest.raises(ValueError, match="handshake"):
            store.publish(candidate, expected_current=first)
        assert store.current() == first


@pytest.mark.parametrize(
    "target,mutation",
    [
        ("STORE.json", "truncate"),
        ("STORE.json", "schema"),
        ("CURRENT", "truncate"),
        ("CURRENT", "traversal"),
        ("CURRENT", "size"),
        ("CURRENT", "noncanonical"),
        ("generation", "truncate"),
        ("generation", "checksum"),
    ],
)
def test_corruption_refuses_open_while_existing_reader_stays_pinned(
    entries, tmp_path, target, mutation
):
    root = tmp_path / "store"
    generation = seed(root, records(entries[:1]))
    pinned = FeatureStoreReaderStudy(root)
    path = root / (
        "generations/" + generation + ".json" if target == "generation" else target
    )
    original = path.read_bytes()
    if mutation in ("truncate", "checksum"):
        altered = original[:8] if mutation == "truncate" else original + b" "
    else:
        value = json.loads(original)
        if mutation == "schema":
            value["schema"] = "unknown"
        elif mutation == "traversal":
            value["generation"] = "../CURRENT"
        elif mutation == "size":
            value["bytes"] += 1
        altered = (
            json.dumps(value, indent=2).encode()
            if mutation == "noncanonical"
            else encode(value)
        )
    path.write_bytes(altered)
    with pytest.raises((ValueError, json.JSONDecodeError)):
        FeatureStoreReaderStudy(root)
    assert pinned.snapshot(0) == entries[0]["snapshot"]
    pinned.close()


@pytest.mark.parametrize(
    "mutation", ["schema", "missing", "unused", "payload", "binding"]
)
def test_self_consistent_generation_hash_does_not_bypass_bundle_checks(
    entries, tmp_path, mutation
):
    root = tmp_path / "store"
    first = seed(root, records(entries[:1]))
    value = json.loads((root / "generations" / (first + ".json")).read_bytes())
    if mutation == "schema":
        value["schema"] = "unknown"
    elif mutation == "missing":
        value["payloads"].clear()
    elif mutation == "unused":
        value["records"].clear()
    elif mutation == "binding":
        value["records"][0]["source_key"] = "forged"
    else:
        key = next(iter(value["payloads"]))
        value["payloads"][key] = "AA=="
    raw = encode(value)
    generation = hashlib.sha256(raw).hexdigest()
    (root / "generations" / (generation + ".json")).write_bytes(raw)
    with pytest.raises(ValueError):
        FeatureStoreReaderStudy(root, generation)


@pytest.mark.parametrize("kind", ["symlink", "fifo", "directory"])
def test_nonregular_control_files_refuse_without_blocking(entries, tmp_path, kind):
    root = tmp_path / "store"
    seed(root, records(entries[:1]))
    current = root / "CURRENT"
    current.rename(root / "original")
    if kind == "symlink":
        current.symlink_to(root / "original")
    elif kind == "fifo":
        os.mkfifo(current)
    else:
        current.mkdir()
    with pytest.raises((ValueError, OSError)):
        FeatureStoreReaderStudy(root)


def test_second_cooperating_writer_refuses_and_readers_need_no_lease(entries, tmp_path):
    root = tmp_path / "store"
    seed(root, records(entries[:1]))
    with FeatureStoreStudy(root), FeatureStoreReaderStudy(root):
        with pytest.raises(BlockingIOError):
            FeatureStoreStudy(root)


def interrupted_child(root, candidate, first, side, ready):
    from phmt_test_support import feature_store

    original = feature_store.os.replace

    def boundary(source, destination):
        if side == "after":
            original(source, destination)
        ready.send("at-publication-" + side)
        signal.pause()  # The parent terminates only this owned, bounded child.
        raise AssertionError("Unexpected resumed publication child")

    feature_store.os.replace = boundary
    with FeatureStoreStudy(root) as store:
        store.publish(candidate, expected_current=first)


@pytest.mark.parametrize("side", ["before", "after"])
@pytest.mark.parametrize("termination", [signal.SIGTERM, signal.SIGKILL])
def test_own_child_interruption_preserves_confirmed_visibility_and_unknown_attempt(
    entries, tmp_path, side, termination
):
    root = tmp_path / "store"
    first = seed(root, records(entries[:1]))
    with FeatureStoreStudy(root) as store:
        candidate = store.seal(records(entries[:2]))
    old = FeatureStoreReaderStudy(root)
    ctx = multiprocessing.get_context("fork")
    parent, child = ctx.Pipe(duplex=False)
    process = ctx.Process(
        target=interrupted_child, args=(root, candidate, first, side, child)
    )
    process.start()
    try:
        assert parent.poll(15), "Owned child failed to reach publication boundary"
        assert parent.recv() == "at-publication-" + side
        os.kill(process.pid, termination)
        process.join(10)
        assert process.exitcode == -termination
    finally:
        if process.is_alive():
            process.terminate()
            process.join(5)
        parent.close()
        child.close()
    expected = first if side == "before" else candidate
    with FeatureStoreReaderStudy(root) as current:
        assert current.describe()["generation"] == expected
    assert old.describe()["generation"] == first
    old.close()
    with FeatureStoreStudy(root) as store:
        unknown = [r for r in store.attempts() if r["state"] == "unknown"]
        assert len(unknown) == 1 and unknown[0]["started"]["candidate"] == candidate
        assert store.current() == expected
        store.publish(
            candidate, expected_current=expected, retry_of=unknown[0]["attempt"]
        )
        assert any(
            r["started"]["retry_of"] == unknown[0]["attempt"]
            and r["state"] == "completed"
            for r in store.attempts()
        )
    assert (root / "generations" / (first + ".json")).exists()


def test_operation_receipts_retain_failures_without_claiming_rollback(
    entries, tmp_path, monkeypatch
):
    import phmt_test_support.feature_store as module

    root = tmp_path / "store"
    first = seed(root, records(entries[:1]))
    with FeatureStoreStudy(root) as store:
        candidate = store.seal(records(entries[:2]))
        original = module.os.replace

        def replace_then_raise(source, destination):
            original(source, destination)
            raise OSError("injected failure after visible replace")

        monkeypatch.setattr(module.os, "replace", replace_then_raise)
        with pytest.raises(OSError, match="after visible"):
            store.publish(candidate, expected_current=first)
        assert store.current() == candidate
        failures = [r for r in store.attempts() if r["state"] == "raised"]
        assert (
            len(failures) == 1
            and failures[0]["terminal"]["exception_type"] == "OSError"
        )
        assert "after visible" in failures[0]["terminal"]["reason"]


def test_reading_original_artifacts_creates_no_new_attribution(entries, tmp_path):
    import ackredit

    import pharmacophoremt as phmt

    root = tmp_path / "store"
    seed(root, records(entries))
    with (
        ackredit.session("feature-store reading"),
        phmt.attribution(),
        ackredit.capture("stored originals") as captured,
    ):
        before = ackredit.get_attribution().to_dict()
        for _ in range(2):
            with FeatureStoreReaderStudy(root) as reader:
                for ordinal, original in enumerate(entries):
                    assert reader.snapshot(ordinal) == original["snapshot"]
                    assert (
                        FeatureSnapshotStudy(reader.snapshot(ordinal)).to_dict()
                        == FeatureSnapshotStudy(original["snapshot"]).to_dict()
                    )
                    reader.inventory(ordinal)
        assert ackredit.get_attribution().to_dict() == before
    assert (
        not captured.attribution.to_dict()["items"]
        and not captured.attribution.to_dict()["uses"]
    )


def lease_probe(root, reply):
    try:
        with FeatureStoreStudy(root):
            reply.send("unexpectedly acquired")
    except BlockingIOError:
        reply.send("refused")


def test_separate_process_writer_is_refused_without_touching_parent_lease(
    entries, tmp_path
):
    root = tmp_path / "store"
    seed(root, records(entries[:1]))
    ctx = multiprocessing.get_context("fork")
    parent, child = ctx.Pipe(duplex=False)
    with FeatureStoreStudy(root) as writer:
        process = ctx.Process(target=lease_probe, args=(root, child))
        process.start()
        try:
            assert parent.poll(10) and parent.recv() == "refused"
            process.join(5)
            assert process.exitcode == 0 and writer.current() is not None
        finally:
            if process.is_alive():
                process.terminate()
                process.join(5)
            parent.close()
            child.close()


def test_partial_generation_install_failure_keeps_old_current_and_retains_cause(
    entries, tmp_path, monkeypatch
):
    import phmt_test_support.feature_store as module

    root = tmp_path / "store"
    first = seed(root, records(entries[:1]))
    original = module.os.link

    def fail_generation(source, destination):
        if Path(destination).parent.name == "generations":
            Path(source).write_bytes(b"partial staged bytes")
            raise OSError("injected generation installation failure")
        return original(source, destination)

    with FeatureStoreStudy(root) as store:
        monkeypatch.setattr(module.os, "link", fail_generation)
        with pytest.raises(OSError, match="installation failure"):
            store.seal(records(entries[:2]))
        assert store.current() == first
        assert sorted(p.name for p in (root / "generations").iterdir()) == [
            first + ".json"
        ]
        assert len([r for r in store.attempts() if r["state"] == "raised"]) == 1


def test_corrupt_receipts_refuse_history_without_invalidating_published_generation(
    entries, tmp_path
):
    root = tmp_path / "store"
    first = seed(root, records(entries[:1]))
    with FeatureStoreStudy(root) as store:
        first_attempt = store.attempts()[0]["attempt"]
        (root / "attempts" / (first_attempt + ".started.json")).write_bytes(
            b"truncated"
        )
        with pytest.raises(ValueError):
            store.attempts()
        with pytest.raises(ValueError):
            store.seal([])
    with FeatureStoreReaderStudy(root) as view:
        assert view.describe()["generation"] == first


def test_attempt_bound_and_unknown_retry_refuse_before_new_work(
    entries, tmp_path, monkeypatch
):
    import phmt_test_support.feature_store as module

    root = tmp_path / "store"
    with FeatureStoreStudy(root, create=True) as store:
        with pytest.raises(ValueError, match="retry_of"):
            store.seal([], retry_of="not-retained")
        assert store.attempts() == []
        monkeypatch.setattr(module, "MAX_ATTEMPTS", 1)
        generation = store.seal(records(entries[:1]))
        with pytest.raises(ValueError, match="operation limit"):
            store.seal([])
        assert len(store.attempts()) == 1
        assert (root / "generations" / (generation + ".json")).exists()


def test_ready_input_cannot_override_exact_bytes_with_claimed_hash(entries, tmp_path):
    rows = records(entries[:1])
    rows[0]["snapshot_sha256"] = "0" * 64
    with FeatureStoreStudy(tmp_path / "store", create=True) as store:
        with pytest.raises(ValueError, match="original bytes"):
            store.seal(rows)
        assert store.current() is None


def test_existing_generation_corruption_is_never_overwritten_on_reseal(
    entries, tmp_path
):
    root = tmp_path / "store"
    with FeatureStoreStudy(root, create=True) as store:
        generation = store.seal(records(entries[:1]))
        path = root / "generations" / (generation + ".json")
        path.write_bytes(b"truncated original generation")
        with pytest.raises(ValueError, match="conflicts"):
            store.seal(records(entries[:1]))
        assert path.read_bytes() == b"truncated original generation"
        assert store.current() is None
