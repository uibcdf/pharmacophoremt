"""Guided/expert parity over original features and controlled publication state."""

import hashlib
import json
import multiprocessing
import os
import shutil
import signal

import pytest

from pharmacophoremt_results import canonical_json
from phmt_test_support.feature_snapshot import FeatureSnapshotStudy
from phmt_test_support.feature_snapshot_case import projection
from phmt_test_support.feature_store import FeatureStoreReaderStudy, FeatureStoreStudy
from phmt_test_support.feature_store_workflow import (
    FeatureStoreWorkflowStudy,
    WorkflowRefusalStudy,
    explain_reuse,
    inspect_publication_recovery,
    inspect_reuse,
    prepare_reuse,
    recover_publication,
    retry_publication,
)
from phmt_test_support.typed_retrieval import load_entries


@pytest.fixture(scope="module")
def entries():
    return load_entries(os.environ.get("PHMT_RECEIVING_CONTEXT", "source"))


def make_records(entries):
    rows = []
    for entry in entries:
        parent = FeatureSnapshotStudy(entry["snapshot"]).describe()["parent"]
        rows.append(
            {
                "work_key": entry["work_key"],
                "source_key": parent["source_key"],
                "occurrence_key": parent["occurrence_key"],
                "status": "ready",
                "snapshot": entry["snapshot"],
            }
        )
    return rows


@pytest.fixture
def store(entries, tmp_path):
    root = tmp_path / "store"
    with FeatureStoreStudy(root, create=True) as writer:
        generation = writer.seal(make_records(entries))
        writer.publish(generation, expected_current=None)
    return root, generation


def identities(root):
    return {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.rglob("*")
        if p.is_file()
    }


@pytest.mark.parametrize(
    "families,keys,ordinals,code",
    [
        (["hb donor"], ["repeat=α", "1 nm", "nm"], [1, 6, 10], "validate_quantities"),
        (["aromatic ring"], ["empty:nm"], [0], "validate_quantities"),
        (["hb donor"], ["empty:nm"], [0], "evaluate_missing_families"),
        (["hb donor"], [], [], "empty_selection"),
        (["hb donor"], None, list(range(11)), "evaluate_missing_families"),
    ],
)
def test_guided_expert_inspection_preserves_global_ordinals_and_scope(
    store, families, keys, ordinals, code
):
    root, generation = store
    before = identities(root)
    with (
        FeatureStoreWorkflowStudy(root) as guided,
        FeatureStoreReaderStudy(root) as expert,
    ):
        left = guided.inspect(families, work_keys=keys)
        right = inspect_reuse(expert, families, work_keys=keys)
        assert left == right
        assert left["generation"] == generation
        assert left["selection_ordinals"] == ordinals
        assert left["decision"]["code"] == code
        assert left["query_admitted"] is left["match_outcome"] is None
        assert (
            not left["quantity_semantics_checked"]
            and not left["molecular_origin_authenticated"]
        )
        assert left["manifest_occurrence_count"] == 11 and left["manifest_complete"]
        assert explain_reuse(left) == explain_reuse(right)
    assert identities(root) == before


def test_missing_evaluation_is_not_known_empty_and_messages_name_required_action(store):
    root, _ = store
    with FeatureStoreWorkflowStudy(root) as workflow:
        aromatic = workflow.inspect(["aromatic ring"], work_keys=["empty:nm"])
        donor = workflow.inspect(["hb donor"], work_keys=["empty:nm"])
        assert aromatic["occurrences"][0]["coverage"]["known_counts"] == {
            "aromatic ring": 0
        }
        assert donor["occurrences"][0]["coverage"]["known_counts"] == {}
        assert donor["occurrences"][0]["coverage"]["unobserved_families"] == [
            "hb donor"
        ]
        assert "Evaluate the missing families explicitly" in explain_reuse(donor)
        assert "'empty:nm': missing evaluation for hb donor" in explain_reuse(donor)


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_both_routes_decode_same_original_maps_quantities_and_immutable_input(
    store, entries, unit
):
    from pharmacophoremt import pyunitwizard as puw

    root, generation = store
    before = identities(root)
    keys = ["repeat=α", "1 nm", "nm"]
    with (
        FeatureStoreWorkflowStudy(root) as guided,
        FeatureStoreReaderStudy(root) as expert,
        puw.context(standard_units=[unit, "ps", "radians"]),
    ):
        a = guided.reuse(
            ["positive charge", "hb donor", "hb donor"],
            expected_generation=generation,
            work_keys=keys,
        )
        b = prepare_reuse(
            expert,
            ["hb donor", "positive charge"],
            expected_generation=generation,
            work_keys=list(reversed(keys)),
        )
        assert a["report"] == b["report"]
        assert a["report"]["decision"]["code"] == "captured_features_ready"
        assert (
            a["report"]["quantity_semantics_checked"]
            and a["report"]["query_admitted"] is None
        )
        assert [r["work_ordinal"] for r in a["inventories"]] == [1, 6, 10]
        for left, right in zip(a["inventories"], b["inventories"]):
            assert projection(left["inventory"]) == projection(right["inventory"])
            original = FeatureSnapshotStudy(entries[left["work_ordinal"]]["snapshot"])
            assert projection(left["inventory"]) == projection(
                original.decode_inventory()
            )
        a["inventories"][0]["inventory"]["features"][0]["atom_indices"].clear()
        again = guided.reuse(
            ["hb donor", "positive charge"],
            expected_generation=generation,
            work_keys=keys,
        )
        assert projection(again["inventories"][0]["inventory"]) == projection(
            b["inventories"][0]["inventory"]
        )
    assert identities(root) == before


@pytest.mark.parametrize("kind", ["missing-family", "generation", "unknown-key"])
def test_both_routes_refuse_before_quantity_access_and_leave_reader_open(
    store, monkeypatch, kind
):
    root, generation = store

    def forbidden(*args):
        raise AssertionError("Refused metadata reached quantity decoding")

    monkeypatch.setattr(FeatureStoreReaderStudy, "inventory", forbidden)
    families, keys, expected = ["hb donor"], ["nm"], generation
    code = {
        "missing-family": "evaluate_missing_families",
        "generation": "generation_mismatch",
        "unknown-key": "unknown_work_key",
    }[kind]
    if kind == "missing-family":
        keys = ["empty:nm"]
    elif kind == "generation":
        expected = "0" * 64
    else:
        keys = [" nm"]
    reports = []
    with (
        FeatureStoreWorkflowStudy(root) as guided,
        FeatureStoreReaderStudy(root) as expert,
    ):
        for operation in (
            lambda: guided.reuse(
                families, expected_generation=expected, work_keys=keys
            ),
            lambda: prepare_reuse(
                expert, families, expected_generation=expected, work_keys=keys
            ),
        ):
            with pytest.raises(WorkflowRefusalStudy) as caught:
                operation()
            assert caught.value.code == code
            reports.append(caught.value.report)
        assert reports[0] == reports[1]
        assert (
            expert.describe()["generation"]
            == guided.inspect(["hb donor"], work_keys=["nm"])["generation"]
        )


@pytest.mark.parametrize(
    "families,keys",
    [
        ([], ["nm"]),
        (["unknown"], None),
        (["hb donor"], "nm"),
        (["hb donor"], ["nm", "nm"]),
        (["hb donor"], [0]),
        (["hb donor"], [""]),
    ],
)
def test_invalid_inputs_refuse_before_reader_access(families, keys):
    class Unreadable:
        def describe(self):
            raise AssertionError("Invalid request accessed reader")

    with pytest.raises(ValueError):
        inspect_reuse(Unreadable(), families, work_keys=keys)


@pytest.mark.parametrize("status", ["failed", "partial", "unsupported", "unattempted"])
def test_incomplete_causes_and_explicit_ready_subset_survive_both_routes(
    entries, tmp_path, status
):
    root = tmp_path / "incomplete"
    rows = make_records(entries[1:2]) + [
        {
            "work_key": "gap",
            "source_key": "gap",
            "occurrence_key": "gap:0",
            "status": status,
            "cause": {
                "type": "synthetic-control",
                "reason": "original incomplete extraction",
            },
        }
    ]
    with FeatureStoreStudy(root, create=True) as writer:
        candidate = writer.seal(rows)
    with (
        FeatureStoreWorkflowStudy(root, candidate) as guided,
        FeatureStoreReaderStudy(root, candidate) as expert,
    ):
        a = guided.inspect(["hb donor"])
        assert a == inspect_reuse(expert, ["hb donor"])
        assert not a["manifest_complete"] and not a["selected_extraction_complete"]
        assert a["occurrences"][1]["cause"] == rows[1]["cause"]
        assert status in explain_reuse(
            a
        ) and "original incomplete extraction" in explain_reuse(a)
        with pytest.raises(WorkflowRefusalStudy, match="incomplete"):
            guided.reuse(["hb donor"], expected_generation=candidate)
        selected = guided.reuse(
            ["hb donor"], expected_generation=candidate, work_keys=["nm"]
        )
        assert (
            selected["report"]["selected_extraction_complete"]
            and not selected["report"]["manifest_complete"]
        )
        assert selected["report"]["selection_ordinals"] == [0]
        assert selected["report"]["query_admitted"] is None


def test_refresh_does_not_silently_switch_session_and_close_does_not_close_other_reader(
    store, entries
):
    root, first = store
    guided = FeatureStoreWorkflowStudy(root)
    expert = FeatureStoreReaderStudy(root)
    with FeatureStoreStudy(root) as writer:
        rows = make_records(entries)
        rows[1]["work_key"] = "new literal key"
        second = writer.seal(rows)
        writer.publish(second, expected_current=first)
    assert guided.inspect(["hb donor"], work_keys=["nm"])["generation"] == first
    assert (
        guided.reuse(["hb donor"], work_keys=["nm"], expected_generation=first)[
            "report"
        ]["generation"]
        == first
    )
    guided.close()
    guided.close()
    assert expert.describe()["generation"] == first
    with pytest.raises(WorkflowRefusalStudy) as caught:
        guided.inspect(["hb donor"])
    assert caught.value.code == "closed_session"
    expert.close()
    with pytest.raises(WorkflowRefusalStudy) as caught:
        inspect_reuse(expert, ["hb donor"])
    assert caught.value.code == "closed_session"
    with FeatureStoreWorkflowStudy(root) as reopened:
        with pytest.raises(WorkflowRefusalStudy) as caught:
            reopened.reuse(
                ["hb donor"], expected_generation=first, work_keys=["new literal key"]
            )
        assert caught.value.code == "generation_mismatch"


def test_metadata_report_mutation_cannot_skip_fresh_quantity_handshake(
    store, monkeypatch
):
    root, generation = store
    with FeatureStoreWorkflowStudy(root) as guided:
        preview = guided.inspect(["hb donor"], work_keys=["nm"])
        preview["quantity_semantics_checked"] = True
        preview["occurrences"].clear()

        def refuse(self, ordinal):
            raise ValueError("controlled public quantity refusal")

        monkeypatch.setattr(FeatureStoreReaderStudy, "inventory", refuse)
        with pytest.raises(WorkflowRefusalStudy) as caught:
            guided.reuse(["hb donor"], expected_generation=generation, work_keys=["nm"])
        assert caught.value.code == "invalid_quantities"
        assert caught.value.report["quantity_failure"] == {
            "work_ordinal": 1,
            "work_key": "nm",
            "type": "ValueError",
            "previously_validated_ordinals": [],
        }
        assert isinstance(caught.value.__cause__, ValueError)
        assert not caught.value.report["quantity_semantics_checked"]
        assert guided.inspect(["hb donor"], work_keys=["nm"])["occurrences"]


def publication_child(root, candidate, first, side, reply):
    import phmt_test_support.feature_store as module

    original = module.os.replace

    def boundary(source, destination):
        if side == "after":
            original(source, destination)
        reply.send("ready")
        signal.pause()

    module.os.replace = boundary
    with FeatureStoreStudy(root) as writer:
        writer.publish(candidate, expected_current=first)


def interrupted_publication(root, entries, side):
    with FeatureStoreStudy(root, create=True) as writer:
        first = writer.seal(make_records(entries[:1]))
        writer.publish(first, expected_current=None)
        candidate = writer.seal(make_records(entries[:2]))
    ctx = multiprocessing.get_context("spawn")
    parent, child = ctx.Pipe(duplex=False)
    process = ctx.Process(
        target=publication_child, args=(root, candidate, first, side, child)
    )
    process.start()
    try:
        assert parent.poll(15) and parent.recv() == "ready"
        process.terminate()
        process.join(10)
        assert process.exitcode == -signal.SIGTERM
    finally:
        if process.is_alive():
            process.kill()
            process.join(5)
        parent.close()
        child.close()
    with FeatureStoreStudy(root) as writer:
        attempt = next(
            r["attempt"] for r in writer.attempts() if r["state"] == "unknown"
        )
    return first, candidate, attempt


@pytest.mark.parametrize("side", ["before", "after"])
def test_guided_expert_recovery_observe_real_interruption_without_inferred_rollback(
    entries, tmp_path, side
):
    root = tmp_path / "interrupted"
    first, candidate, attempt = interrupted_publication(root, entries, side)
    before = identities(root)
    a = recover_publication(root, attempt)
    with FeatureStoreStudy(root) as writer, FeatureStoreReaderStudy(root) as reader:
        b = inspect_publication_recovery(writer, reader, attempt)
    assert a == b and identities(root) == before
    assert (
        a["attempt_state"] == "unknown"
        and not a["rollback_inferred"]
        and not a["automatic_retry"]
    )
    assert a["current_generation"] == (first if side == "before" else candidate)
    assert a["decision"]["code"] == (
        "candidate_not_current" if side == "before" else "candidate_is_current"
    )
    left, right = tmp_path / "guided", tmp_path / "expert"
    shutil.copytree(root, left)
    shutil.copytree(root, right)
    if side == "after":
        with pytest.raises(WorkflowRefusalStudy) as caught:
            recover_publication(left, attempt, retry=True, expected_current=candidate)
        assert (
            caught.value.code == "candidate_is_current" and identities(left) == before
        )
    else:
        guided = recover_publication(left, attempt, retry=True, expected_current=first)
        with (
            FeatureStoreStudy(right) as writer,
            FeatureStoreReaderStudy(right) as reader,
        ):
            expert = retry_publication(writer, reader, attempt, expected_current=first)
        assert guided == expert and guided["published_generation"] == candidate
        with FeatureStoreStudy(left) as writer:
            history = writer.attempts()
            assert (
                next(r for r in history if r["attempt"] == attempt)["state"]
                == "unknown"
            )
            assert (
                len(
                    [
                        r
                        for r in history
                        if r["started"]["retry_of"] == attempt
                        and r["state"] == "completed"
                    ]
                )
                == 1
            )
        assert (left / "CURRENT").read_bytes() == (right / "CURRENT").read_bytes()
    assert identities(root) == before


def test_newer_publication_blocks_automatic_rollback_and_stale_retry(store, entries):
    root, first = store
    with FeatureStoreStudy(root) as writer:
        candidate = writer.seal(make_records(entries[:2]))
        with pytest.raises(ValueError, match="Stale"):
            writer.publish(candidate, expected_current=None)
        attempt = next(
            r["attempt"] for r in writer.attempts() if r["state"] == "raised"
        )
        report = inspect_publication_recovery(
            writer, FeatureStoreReaderStudy(root), attempt
        )
        assert report["decision"]["code"] == "publication_changed"
    before = identities(root)
    with pytest.raises(WorkflowRefusalStudy) as caught:
        recover_publication(root, attempt, retry=True, expected_current=first)
    assert caught.value.code == "publication_changed" and identities(root) == before


def test_missing_candidate_retry_preserves_current_and_retains_new_failure(
    store, entries
):
    root, first = store
    with FeatureStoreStudy(root) as writer:
        candidate = writer.seal(make_records(entries[:2]))
        # A failed store operation supplies an original retained attempt.
        import phmt_test_support.feature_store as module

        original = module.os.replace

        def refused(source, destination):
            raise OSError("controlled before-publication refusal")

        module.os.replace = refused
        try:
            with pytest.raises(OSError):
                writer.publish(candidate, expected_current=first)
        finally:
            module.os.replace = original
        attempt = next(
            r["attempt"] for r in writer.attempts() if r["state"] == "raised"
        )
    (root / "generations" / (candidate + ".json")).unlink()
    assert recover_publication(root, attempt)["candidate_validation"].startswith(
        "not_performed"
    )
    with pytest.raises(FileNotFoundError):
        recover_publication(root, attempt, retry=True, expected_current=first)
    with FeatureStoreStudy(root) as writer:
        assert writer.current() == first
        assert len([r for r in writer.attempts() if r["state"] == "raised"]) == 2


def test_recovery_refuses_busy_unknown_seal_and_wrong_reader_without_writes(store):
    root, generation = store
    before = identities(root)
    with FeatureStoreStudy(root) as writer:
        seal = next(
            r["attempt"]
            for r in writer.attempts()
            if r["started"]["operation"] == "seal"
        )
        publish = next(
            r["attempt"]
            for r in writer.attempts()
            if r["started"]["operation"] == "publish"
        )
        for attempt, code in (
            ("not known", "unknown_attempt"),
            (seal, "not_publication_attempt"),
        ):
            with FeatureStoreReaderStudy(root) as reader:
                with pytest.raises(WorkflowRefusalStudy) as caught:
                    inspect_publication_recovery(writer, reader, attempt)
            assert caught.value.code == code
        with pytest.raises(WorkflowRefusalStudy) as caught:
            inspect_publication_recovery(writer, None, publish)
        assert caught.value.code == "inconsistent_reader"
        with pytest.raises(WorkflowRefusalStudy) as caught:
            recover_publication(root, publish)
        assert caught.value.code == "writer_busy"
    assert identities(root) == before


@pytest.mark.parametrize(
    "options", [{"retry": "yes"}, {"retry": True}, {"expected_current": None}]
)
def test_bad_recovery_options_refuse_before_open(monkeypatch, options):
    import phmt_test_support.feature_store_workflow as module

    def forbidden(*args, **kwargs):
        raise AssertionError("Invalid recovery options opened store")

    monkeypatch.setattr(module, "FeatureStoreStudy", forbidden)
    with pytest.raises(ValueError):
        recover_publication("unused", "attempt", **options)


def test_self_consistent_but_inconsistent_attempt_refuses_recovery(store):
    root, _ = store
    with FeatureStoreStudy(root) as writer:
        attempt = next(
            r["attempt"]
            for r in writer.attempts()
            if r["started"]["operation"] == "publish"
        )
    path = root / "attempts" / (attempt + ".terminal.json")
    value = json.loads(path.read_bytes())
    value["candidate"] = "0" * 64
    path.write_bytes(canonical_json(value).encode())
    with pytest.raises(WorkflowRefusalStudy) as caught:
        recover_publication(root, attempt)
    assert caught.value.code == "invalid_attempt"
