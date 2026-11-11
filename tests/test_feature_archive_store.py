"""Real local writer, immutable originals, publication and interrupted recovery."""

import gc
import hashlib
import importlib
import json
import multiprocessing
import os
import signal
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from test_feature_asset_view import archive as archive
from test_feature_asset_view import bundle, identity, install
from test_feature_asset_view import originals as originals
from test_native_feature_reuse import rewritten

from pharmacophoremt_features import (
    FeatureAssetError,
    FeatureAssetStore,
    FeatureAssetView,
    _writer,
    _writer_schema,
)
from pharmacophoremt_results import canonical_json


def stage(store, source):
    return store.stage(source, expected_generation=source.generation)


def new_source(archive, policy):
    value = bundle(archive)
    value["origin"]["policy"] = policy
    install(archive, value)
    return FeatureAssetView.open(archive)


def test_whole_generation_preserves_all_original_bytes_metadata_and_positions(
    archive, tmp_path
):
    before = identity(archive)
    root = tmp_path / "owned"
    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(root, payload_profile="snapshot-study-v1") as store,
    ):
        assert store.current() is None
        first = stage(store, source)
        assert store.current() is None
        with store.view(generation=first) as candidate:
            assert candidate.work_items(limit=64) == {
                **source.work_items(limit=64),
                "generation": first,
            }
            for ordinal in range(11):
                assert candidate.snapshot_bytes(ordinal) == source.snapshot_bytes(
                    ordinal
                )
                a, b = candidate.payload_info(ordinal), source.payload_info(ordinal)
                assert a == {**b, "generation": first}
            assert candidate.summary()["origin"] == {
                "format": "pharmacophoremt.feature-archive-generation@1",
                "generation": source.generation,
                "policy": "explicit-original-generation-copy@1",
            }
            assert not candidate.summary()["quantity_semantics_checked"]
        assert store.publish(first, expected_current=None) == first
        detached = store.view()
        assert detached.generation == store.current() == first
    assert detached.snapshot_bytes(1)
    detached.close()
    with FeatureAssetStore.open(root) as reopened:
        assert reopened.current() == first
        assert [r["state"] for r in reopened.attempts()] == ["completed", "completed"]
        software = reopened.attempts()[0]["started"]["software"]
        assert software["distribution"] == "pharmacophoremt"
        assert (
            software["observed_writer_sha256"]
            == hashlib.sha256(Path(_writer.__file__).read_bytes()).hexdigest()
        )
    assert identity(archive) == before


def test_create_and_open_never_adopt_or_overwrite_an_existing_destination(
    archive, tmp_path
):
    before = identity(archive)
    for target in [archive, tmp_path]:
        with pytest.raises(FeatureAssetError) as caught:
            FeatureAssetStore.create(target, payload_profile="snapshot-study-v1")
        assert caught.value.code == "PHMT-E329"
    with pytest.raises(FeatureAssetError) as caught:
        FeatureAssetStore.open(archive)
    assert caught.value.code == "PHMT-E328"
    assert identity(archive) == before


def test_stale_publication_retains_safe_failure_and_original_confirmed_view(
    archive, tmp_path
):
    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(
            tmp_path / "store", payload_profile="snapshot-study-v1"
        ) as store,
    ):
        first = stage(store, source)
        store.publish(first, expected_current=None)
        with new_source(archive, "second-origin") as changed:
            second = stage(store, changed)
        with pytest.raises(FeatureAssetError) as caught:
            store.publish(second, expected_current=None)
        assert caught.value.code == "PHMT-E322" and store.current() == first
        attempt = store.attempts()[-1]
        assert (
            attempt["state"] == "raised"
            and attempt["terminal"]["category"] == "PHMT-E322"
        )
        assert "reason" not in attempt["terminal"]
        report = store.inspect_recovery(attempt["attempt"])
        assert report["decision"]["action"] == "publication_changed"
        assert not report["candidate_native_validation_performed"]
        with pytest.raises(FeatureAssetError):
            store.retry_publication(attempt["attempt"])
        assert store.publish(second, expected_current=first) == second


@pytest.mark.parametrize("status", ["partial", "failed", "unsupported", "unattempted"])
def test_incomplete_candidates_are_inspectable_but_never_published(
    archive, tmp_path, status
):
    value = bundle(archive)
    row = value["records"][0]
    old = row["payload_sha256"]
    value["records"][0] = {
        k: row[k] for k in ("work_key", "source_key", "occurrence_key")
    }
    value["records"][0].update(
        status=status, cause={"type": "original", "reason": "not completed"}
    )
    del value["payloads"][old]
    install(archive, value)
    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(
            tmp_path / "store", payload_profile="snapshot-study-v1"
        ) as store,
    ):
        candidate = stage(store, source)
        with store.view(generation=candidate) as view:
            assert not view.summary()["complete"]
            assert view.work_items(limit=1)["records"][0]["cause"] == {
                "type": "original",
                "reason": "not completed",
            }
        with pytest.raises(FeatureAssetError) as caught:
            store.publish(candidate, expected_current=None)
        assert caught.value.code == "PHMT-E326" and store.current() is None


def test_empty_declared_generation_stays_empty_without_a_scientific_negative(
    archive, tmp_path
):
    value = bundle(archive)
    value.update(records=[], payloads={})
    install(archive, value)
    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(
            tmp_path / "store", payload_profile="snapshot-study-v1"
        ) as store,
    ):
        candidate = stage(store, source)
        store.publish(candidate, expected_current=None)
        with store.view() as view:
            assert view.summary()["record_count"] == 0
            assert (
                view.summary()["query_admitted"]
                is view.summary()["match_outcome"]
                is None
            )


def test_source_generation_and_lifetime_are_rechecked_before_starting_an_attempt(
    archive, tmp_path
):
    source = FeatureAssetView.open(archive)
    with FeatureAssetStore.create(
        tmp_path / "store", payload_profile="snapshot-study-v1"
    ) as store:
        with pytest.raises(FeatureAssetError) as caught:
            store.stage(source, expected_generation="a" * 64)
        assert caught.value.code == "PHMT-E308" and store.attempts() == []
        source.close()
        with pytest.raises(FeatureAssetError) as caught:
            store.stage(source, expected_generation="a" * 64)
        assert caught.value.code == "PHMT-E304"


def test_publication_revalidates_native_quantities_each_time(
    archive, tmp_path, monkeypatch
):
    from pharmacophoremt import pyunitwizard as puw

    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(
            tmp_path / "store", payload_profile="snapshot-study-v1"
        ) as store,
    ):
        with puw.context(standard_units=["pm", "ps", "radians"]):
            candidate = stage(store, source)
        with monkeypatch.context() as patch:
            patch.setattr(puw, "QuantityRecord", None)
            with pytest.raises(FeatureAssetError) as caught:
                store.publish(candidate, expected_current=None)
            assert caught.value.code == "PHMT-E312" and store.current() is None
        old = deepcopy(store.attempts()[-1])
        with puw.context(standard_units=["nm", "ps", "radians"]):
            policy = puw.configure.report()
            assert store.retry_publication(old["attempt"]) == candidate
            assert puw.configure.report() == policy
        assert store.attempts()[-2] == old
        assert store.attempts()[-1]["started"]["retry_of"] == old["attempt"]


def test_corrupt_immutable_generation_refuses_reinstallation_and_publication(
    archive, tmp_path
):
    root = tmp_path / "store"
    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(root, payload_profile="snapshot-study-v1") as store,
    ):
        candidate = stage(store, source)
        path = root / "generations" / (candidate + ".json")
        path.write_bytes(b"corrupted original")
        for action in [
            lambda: stage(store, source),
            lambda: store.publish(candidate, expected_current=None),
        ]:
            with pytest.raises(FeatureAssetError):
                action()
            assert (
                path.read_bytes() == b"corrupted original" and store.current() is None
            )


def test_writer_lease_lifetime_and_detached_receipts(archive, tmp_path):
    root = tmp_path / "store"
    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(root, payload_profile="snapshot-study-v1") as store,
    ):
        candidate = stage(store, source)
        with pytest.raises(FeatureAssetError) as caught:
            FeatureAssetStore.open(root)
        assert caught.value.code == "PHMT-E320"
        with FeatureAssetView.open(root, generation=candidate) as independent:
            assert independent.summary()["record_count"] == 11
        rows = store.attempts()
        rows[0]["started"]["source_generation"] = "mutated"
        assert store.attempts()[0]["started"]["source_generation"] == source.generation
    store.close()
    with pytest.raises(FeatureAssetError) as caught:
        store.current()
    assert caught.value.code == "PHMT-E321"


@pytest.mark.parametrize(
    "method,kwargs",
    [
        ("create", {"payload_profile": "auto"}),
        ("stage", {"view": {}, "expected_generation": "a" * 64}),
        ("publish", {"generation": None, "expected_current": None}),
        ("publish", {"generation": "a" * 64, "expected_current": "current"}),
        ("inspect_recovery", {"attempt": "unobserved"}),
    ],
)
def test_closed_definition_owned_argument_contracts(tmp_path, method, kwargs):
    if method == "create":
        with pytest.raises(FeatureAssetError) as caught:
            FeatureAssetStore.create(tmp_path / "bad", **kwargs)
        assert not (tmp_path / "bad").exists()
    else:
        with FeatureAssetStore.create(
            tmp_path / "store", payload_profile="snapshot-study-v1"
        ) as store:
            with pytest.raises(FeatureAssetError) as caught:
                getattr(store, method)(**kwargs)
            assert store.attempts() == []
    assert caught.value.code == "PHMT-E301"


def test_no_new_extraction_credit_while_preserving_original_references(
    archive, tmp_path
):
    import ackredit

    with (
        ackredit.session("archive-preservation"),
        ackredit.capture("writer") as captured,
    ):
        before = ackredit.get_attribution().to_dict()
        with (
            FeatureAssetView.open(archive) as source,
            FeatureAssetStore.create(
                tmp_path / "store", payload_profile="snapshot-study-v1"
            ) as store,
        ):
            candidate = stage(store, source)
            store.publish(candidate, expected_current=None)
            with store.view() as view:
                assert view.snapshot_bytes(1) == source.snapshot_bytes(1)
        assert ackredit.get_attribution().to_dict() == before
    assert (
        not captured.attribution.to_dict()["items"]
        and not captured.attribution.to_dict()["uses"]
    )


def publication_child(root, candidate, first, side, connection):
    original = _writer.os.replace

    def boundary(source, destination):
        assert Path(destination).name == "CURRENT"
        if side == "after":
            original(source, destination)
        connection.send("at-" + side)
        signal.pause()

    _writer.os.replace = boundary
    with FeatureAssetStore.open(root) as store:
        store.publish(candidate, expected_current=first)


@pytest.mark.parametrize("side", ["before", "after"])
@pytest.mark.parametrize("signum", [signal.SIGTERM, signal.SIGKILL])
def test_real_owned_publication_interruption_and_linked_recovery(
    archive, tmp_path, side, signum
):
    root = tmp_path / "store"
    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(root, payload_profile="snapshot-study-v1") as store,
    ):
        first = stage(store, source)
        store.publish(first, expected_current=None)
        old = store.view()
        with new_source(archive, "new-evidence") as changed:
            candidate = stage(store, changed)
    context = multiprocessing.get_context("spawn")
    parent, child = context.Pipe(duplex=False)
    process = context.Process(
        target=publication_child, args=(root, candidate, first, side, child)
    )
    process.start()
    try:
        assert parent.poll(15), "Owned child did not reach the publication boundary"
        assert parent.recv() == "at-" + side
        os.kill(process.pid, signum)
        process.join(10)
        assert process.exitcode == -signum
    finally:
        if process.is_alive():
            process.kill()
            process.join(5)
        parent.close()
        child.close()
    with FeatureAssetStore.open(root) as store:
        assert store.current() == (first if side == "before" else candidate)
        unknown = next(r for r in store.attempts() if r["state"] == "unknown")
        assert unknown["started"]["candidate"] == candidate
        report = store.inspect_recovery(unknown["attempt"])
        assert report["decision"]["action"] == (
            "retry_available" if side == "before" else "already_current"
        )
        before = identity(root)
        assert (
            store.inspect_recovery(unknown["attempt"]) == report
            and identity(root) == before
        )
        if side == "before":
            assert store.retry_publication(unknown["attempt"]) == candidate
            assert store.attempts()[-2] == unknown
            assert store.attempts()[-1]["started"]["retry_of"] == unknown["attempt"]
            # An old unknown is not eligible again after a confirmed linked retry.
            store.publish(first, expected_current=candidate)
            assert (
                store.inspect_recovery(unknown["attempt"])["decision"]["action"]
                == "completed_attempt"
            )
        with pytest.raises(FeatureAssetError):
            store.retry_publication(unknown["attempt"])
        assert old.generation == first and old.snapshot_bytes(1)
    old.close()


def test_writer_collection_releases_only_its_owned_lease(tmp_path):
    root = tmp_path / "store"
    store = FeatureAssetStore.create(root, payload_profile="snapshot-study-v1")
    del store
    gc.collect()
    with FeatureAssetStore.open(root) as store:
        assert store.current() is None


def test_operation_quota_preserves_all_history_and_readability(archive, tmp_path):
    value = bundle(archive)
    value.update(records=[], payloads={})
    install(archive, value)
    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(
            tmp_path / "store", payload_profile="snapshot-study-v1"
        ) as store,
    ):
        for _ in range(_writer_schema.MAX_ATTEMPTS):
            candidate = stage(store, source)
        original = deepcopy(store.attempts())
        assert len(original) == 64
        with pytest.raises(FeatureAssetError) as caught:
            stage(store, source)
        assert caught.value.code == "PHMT-E323"
        assert store.attempts() == original and store.current() is None
        with store.view(generation=candidate) as view:
            assert view.summary()["record_count"] == 0


@pytest.mark.parametrize(
    "change",
    [
        lambda row: row.update(ordinal=False),
        lambda row: row.update(ordinal=5),
        lambda row: row.update(operation="fabricated"),
        lambda row: row.update(retry_of="a" * 32),
        lambda row: row.update(extra="unknown"),
    ],
)
def test_original_receipt_structure_and_lineage_are_not_repaired(
    archive, tmp_path, change
):
    root = tmp_path / "store"
    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(root, payload_profile="snapshot-study-v1") as store,
    ):
        stage(store, source)
        row = store.attempts()[0]
        path = root / "attempts" / (row["attempt"] + ".started.json")
        altered = deepcopy(row["started"])
        change(altered)
        raw = canonical_json(altered).encode()
        path.write_bytes(raw)
        with pytest.raises(FeatureAssetError):
            store.attempts()
        assert path.read_bytes() == raw
    with pytest.raises(FeatureAssetError):
        FeatureAssetStore.open(root)


def test_ready_native_payload_validation_happens_before_candidate_install(
    archive, tmp_path
):
    rewritten(
        archive,
        lambda d: d["payload"]["inventory"]["features"][0]["center"].update(
            digest="0" * 64
        ),
    )
    root = tmp_path / "store"
    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(root, payload_profile="snapshot-study-v1") as store,
    ):
        with pytest.raises(FeatureAssetError) as caught:
            stage(store, source)
        assert caught.value.code == "PHMT-E311"
        assert store.current() is None and list((root / "generations").iterdir()) == []
        assert store.attempts()[0]["state"] == "raised"


def test_missing_terminal_receipt_never_rolls_back_an_observed_publication(
    archive, tmp_path, monkeypatch
):
    root = tmp_path / "store"
    original = _writer._install

    def refuse_terminal(path, raw, **kwargs):
        if path.name.endswith(".terminal.json"):
            raise OSError("private terminal failure")
        return original(path, raw, **kwargs)

    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(root, payload_profile="snapshot-study-v1") as store,
    ):
        candidate = stage(store, source)
        with monkeypatch.context() as patch:
            patch.setattr(_writer, "_install", refuse_terminal)
            with pytest.raises(FeatureAssetError) as caught:
                store.publish(candidate, expected_current=None)
            assert caught.value.code == "PHMT-E327"
        row = store.attempts()[-1]
        assert row["state"] == "unknown" and store.current() == candidate
        assert (
            store.inspect_recovery(row["attempt"])["decision"]["action"]
            == "already_current"
        )
        assert b"private terminal failure" not in b"".join(
            p.read_bytes() for p in (root / "attempts").iterdir()
        )


def test_unknown_or_nonpublication_retry_never_creates_fabricated_history(
    archive, tmp_path
):
    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(
            tmp_path / "store", payload_profile="snapshot-study-v1"
        ) as store,
    ):
        candidate = stage(store, source)
        original = store.attempts()
        for token in ["a" * 32, original[0]["attempt"]]:
            with pytest.raises(FeatureAssetError) as caught:
                store.publish(candidate, expected_current=None, retry_of=token)
            assert caught.value.code == "PHMT-E324" and store.attempts() == original


def test_process_bound_guard_refuses_before_waiting_for_a_foreign_lock(
    tmp_path, monkeypatch
):
    with FeatureAssetStore.create(
        tmp_path / "store", payload_profile="snapshot-study-v1"
    ) as store:
        with monkeypatch.context() as patch:
            patch.setattr(_writer.os, "getpid", lambda: store._pid + 1)
            with pytest.raises(FeatureAssetError) as caught:
                store.current()
            assert caught.value.code == "PHMT-E321"
        assert store.current() is None


def test_safe_raised_receipt_does_not_stringify_a_native_failure(
    archive, tmp_path, monkeypatch
):
    import smonitor

    class PrivateFailure(Exception):
        def __str__(self):
            raise AssertionError("A private native exception must not be formatted")

    def fail_install(*args, **kwargs):
        raise PrivateFailure()

    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(
            tmp_path / "store", payload_profile="snapshot-study-v1"
        ) as store,
    ):
        candidate = stage(store, source)
        with (
            monkeypatch.context() as patch,
            smonitor.diagnostic_scope(safe_extra={"operation": "publish"}),
        ):
            patch.setattr(_writer.spec, "validate_native", fail_install)
            with pytest.raises(PrivateFailure):
                store.publish(candidate, expected_current=None)
        terminal = store.attempts()[-1]["terminal"]
        assert (
            terminal["exception_type"] == "PrivateFailure"
            and terminal["category"] == "unclassified"
        )
        assert "reason" not in terminal and store.current() is None


def test_record_budget_refuses_before_pulling_originals_or_journaling(
    archive, tmp_path, monkeypatch
):
    value = bundle(archive)
    original = value["records"][1]
    value["records"] = [
        {**deepcopy(original), "work_key": f"literal:{i}"} for i in range(65)
    ]
    value["payloads"] = {
        original["payload_sha256"]: value["payloads"][original["payload_sha256"]]
    }
    install(archive, value)
    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(
            tmp_path / "store", payload_profile="snapshot-study-v1"
        ) as store,
    ):

        def forbidden(*args):
            raise AssertionError("Over-budget plans must not pull payloads")

        monkeypatch.setattr(source, "snapshot_bytes", forbidden)
        with pytest.raises(FeatureAssetError) as caught:
            stage(store, source)
        assert caught.value.code == "PHMT-E313" and store.attempts() == []


def test_actual_fresh_reader_and_writer_metadata_recovery_are_scientifically_cold(
    archive, tmp_path
):
    import pharmacophoremt_features

    root = tmp_path / "store"
    with (
        FeatureAssetView.open(archive) as source,
        FeatureAssetStore.create(root, payload_profile="snapshot-study-v1") as store,
    ):
        candidate = stage(store, source)
        store.publish(candidate, expected_current=None)
        attempt = store.attempts()[-1]["attempt"]
    before = identity(root)
    roots = [str(Path(pharmacophoremt_features.__file__).resolve().parent.parent)]
    roots.extend(
        str(Path(importlib.import_module(n).__file__).resolve().parent.parent)
        for n in ["argdigest", "smonitor", "depdigest"]
    )
    code = r"""
import importlib.abc,json,sys
sys.path[:0]=json.loads(sys.argv[1])
blocked={'pharmacophoremt','molsysmt','numpy','scipy','rdkit','pyunitwizard','ackredit','phmt_test_support'}
attempts=[]
class NoScience(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in blocked:
            attempts.append(fullname)
            raise ModuleNotFoundError('Scientific imports blocked',name=fullname)
sys.meta_path.insert(0,NoScience())
import smonitor
manager=smonitor.configure(profile='agent',level='ERROR',capture_logging=False,capture_warnings=False,args_summary=False,trace_depth=0)
policy=manager.config
from pharmacophoremt_features import FeatureAssetView
assert 'pharmacophoremt_features._writer' not in sys.modules
fcntl_before='fcntl' in sys.modules  # Support libraries may already import subprocess/fcntl.
from pharmacophoremt_features import FeatureAssetStore
assert ('fcntl' in sys.modules)==fcntl_before
with FeatureAssetStore.open(sys.argv[2]) as store:
    report=store.inspect_recovery(sys.argv[3])
    assert report['decision']['action']=='already_current'
    assert not report['candidate_native_validation_performed']
    with store.view() as view:
        assert view.summary()['record_count']==11
        assert view.payload_info(1)['work_ordinal']==1
assert manager.config is policy and not attempts
assert not (blocked & set(sys.modules))
print(json.dumps({'native_imports':0,'policy_preserved':True,'recovery':'already_current'}))
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
            str(root),
            attempt,
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["native_imports"] == 0
    assert identity(root) == before
