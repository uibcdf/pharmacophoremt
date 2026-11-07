"""Independent synthetic accounting protects the opt-in engineering profile."""

import json
import sqlite3
from contextlib import closing
from copy import deepcopy

import pytest

from pharmacophoremt_results import ScreeningRunError, ScreeningRunView
from phmt_test_support.saved_run_profile import (
    CRITERION,
    build_fixture,
    check_export,
    check_summary,
    check_top,
    file_identity,
    profile_fixture,
)


def test_declared_pattern_keeps_ties_failures_and_unpublished_work(tmp_path):
    directory = tmp_path / "case"
    config = build_fixture(directory, 10, padding_bytes=16)
    before = file_identity(directory / "run.sqlite3")
    with ScreeningRunView.open(directory / "run.sqlite3") as view:
        progress = view.progress()
        assert progress["counts"] == {
            "declared_work": 10,
            "committed_work": 7,
            "scored_work": 6,
            "matched_work": 4,
            "not_matched_work": 2,
            "failed_work": 1,
            "pending_work": 3,
        }
        assert progress["attempts"] == {"started": 9, "staged": 8, "committed": 7}
        check_summary(progress, 10)
        top = view.top_results(score_method=CRITERION, limit=100)
        assert [row["manifest_ordinal"] for row in top["records"]] == [0, 6, 1, 7, 2, 8]
        check_top(top, 10, 100, 16)
        assert [row["work_key"] for row in view.results()] == [
            "work:0",
            "work:1",
            "work:2",
            "work:3",
            "work:6",
            "work:7",
            "work:8",
        ]
        assert [row["ranking_score"] for row in view.results()] == [
            1,
            0.5,
            0,
            None,
            1,
            0.5,
            0,
        ]
        assert all(len(row["native_result"]["padding"]) == 16 for row in view.results())
        for file_format in ("jsonl", "csv"):
            method = view.to_jsonl if file_format == "jsonl" else view.to_csv
            receipt = method(directory / ("export." + file_format))
            check_export(receipt, 10, file_format, 16)
    assert (
        before
        == file_identity(directory / "run.sqlite3")
        == config["database_identity"]
    )


def test_oracles_refuse_changed_accounting_and_reversed_ties(tmp_path):
    directory = tmp_path / "case"
    build_fixture(directory, 10)
    with ScreeningRunView.open(directory / "run.sqlite3") as view:
        wrong = deepcopy(view.progress())
        wrong["counts"]["pending_work"] = 0
        with pytest.raises(AssertionError):
            check_summary(wrong, 10)
        wrong = view.top_results(score_method=CRITERION, limit=2)
        wrong["records"].reverse()
        with pytest.raises(AssertionError):
            check_top(wrong, 10, 2)


@pytest.mark.parametrize("target", ["failure", "staged"])
def test_nonranked_corruption_is_refused_before_profiling(tmp_path, target):
    directory = tmp_path / "case"
    build_fixture(directory, 10)
    database = directory / "run.sqlite3"
    # Preserve payload validity and stored digest mismatch; these rows cannot win Top-K.
    key = "work:3" if target == "failure" else "work:5"
    with closing(sqlite3.connect(database)) as connection, connection:
        (payload,) = connection.execute(
            "SELECT payload FROM attempts WHERE work_key=?", (key,)
        ).fetchone()
        changed = json.loads(payload)
        changed["native_result"]["padding"] = "corrupted outside retained ranking"
        connection.execute(
            "UPDATE attempts SET payload=? WHERE work_key=?", (json.dumps(changed), key)
        )
    before = file_identity(database)
    with pytest.raises(ScreeningRunError):
        ScreeningRunView.open(database)
    assert file_identity(database) == before


def test_profile_keeps_every_sample_and_checks_complete_exports(tmp_path):
    directory = tmp_path / "case"
    build_fixture(directory, 10, padding_bytes=16)
    updates = []
    report = profile_fixture(
        directory, repeats=2, on_update=lambda row: updates.append(row["status"])
    )
    assert report["status"] == "completed"
    assert (
        report["independent_oracles_passed"]
        and report["original_input_bytes_unchanged"]
    )
    assert set(report["samples"]) == {"progress", "top10", "top100", "jsonl", "csv"}
    assert all(len(samples) == 2 for samples in report["samples"].values())
    assert all(
        set(s) == {"wall_ns", "process_cpu_ns"} and all(v >= 0 for v in s.values())
        for samples in report["samples"].values()
        for s in samples
    )
    assert len(report["exports"]) == 6
    assert updates[-1] == "completed"


def test_failed_export_preserves_prior_samples_and_timing(tmp_path):
    directory = tmp_path / "case"
    build_fixture(directory, 10)
    destination = directory / "jsonl-repeat0.jsonl"
    destination.write_text("caller-owned existing file")
    updates = []
    with pytest.raises(ScreeningRunError):
        profile_fixture(
            directory, repeats=2, on_update=lambda row: updates.append(deepcopy(row))
        )
    last = updates[-1]
    assert last["status"] == "failed"
    assert all(
        len(last["samples"][name]) == 2 for name in ("progress", "top10", "top100")
    )
    assert last["samples"]["jsonl"] == []
    assert last["failed_operation"]["operation"] == "jsonl"
    assert last["failed_operation"]["repeat"] == "repeat0"
    assert last["failed_operation"]["phase"] == "call"
    assert set(last["failed_operation"]["timing"]) == {"wall_ns", "process_cpu_ns"}
    assert destination.read_text() == "caller-owned existing file"


@pytest.mark.parametrize("count", [0, -10, 11, True])
def test_invalid_case_size_never_creates_fixture(tmp_path, count):
    directory = tmp_path / "case"
    with pytest.raises(ValueError):
        build_fixture(directory, count)
    assert not directory.exists()


def partial_fixture(directory, *, conflicting_stage=False):
    """Independent interrupted public writer: preserve concrete attempt identities."""
    from pharmacophoremt_results import ScreeningRunStore
    from phmt_test_support.saved_run_profile import outcome

    directory.mkdir()
    manifest = directory / "work.jsonl"
    manifest.write_text(
        "".join(
            json.dumps(
                {
                    "work_key": f"work:{i}",
                    "source_key": f"source:{i // 2}",
                    "occurrence_key": f"row:{i}",
                }
            )
            + "\n"
            for i in range(10)
        )
    )
    with ScreeningRunStore.create(
        directory / "run.sqlite3",
        run_id="synthetic-profile:10",
        query_bytes=b'{"case":"synthetic-reader-profile@1"}\n',
        context={
            "execution": {"score_method": "checked_pose_coverage"},
            "producer": {
                "kind": "synthetic-reader-profile@1",
                "scientific_evaluation": False,
            },
        },
        manifest_path=manifest,
    ) as store:
        for ordinal in (9, 6, 5, 1, 0):
            attempt = store.begin(f"work:{ordinal}")
            if ordinal in (9, 1):
                continue
            payload = outcome(ordinal, 16)
            if conflicting_stage and ordinal == 5:
                payload["native_result"]["padding"] = (
                    "different original staged payload"
                )
            store.stage(attempt, payload)
            if ordinal == 6:
                store.publish(attempt)
        return {
            key: list(store.attempts(key))
            for key in ("work:9", "work:6", "work:5", "work:1", "work:0")
        }


def test_public_fixture_recovery_preserves_existing_attempts_and_scores(tmp_path):
    import shutil

    from pharmacophoremt_results import ScreeningRunStore
    from phmt_test_support.saved_run_profile import recover_fixture

    original, copied = tmp_path / "original", tmp_path / "copy"
    attempts = partial_fixture(original)
    before = {p.name: file_identity(p) for p in original.iterdir()}
    shutil.copytree(original, copied)
    received = recover_fixture(copied, 10, 16)
    assert received["preserved_confirmations"] == 1
    assert received["new_confirmations"] == 6
    assert received["new_begins"] == 4
    assert received["after"]["attempts"] == {"started": 9, "staged": 8, "committed": 7}
    assert received["fixture"]["original_one_shot_preparation_qualified"] is False
    with ScreeningRunStore.open(
        copied / "run.sqlite3",
        query_bytes=b'{"case":"synthetic-reader-profile@1"}\n',
        context={
            "execution": {"score_method": "checked_pose_coverage"},
            "producer": {
                "kind": "synthetic-reader-profile@1",
                "scientific_evaluation": False,
            },
        },
        manifest_path=copied / "work.jsonl",
    ) as view:
        for key, old in attempts.items():
            assert [a["attempt_id"] for a in view.attempts(key)] == [
                a["attempt_id"] for a in old
            ]
        check_top(view.top_results(score_method=CRITERION, limit=100), 10, 100, 16)
    assert before == {p.name: file_identity(p) for p in original.iterdir()}
    with pytest.raises(ValueError, match="completed fixture"):
        recover_fixture(copied, 10, 16)


def test_recovery_refuses_conflicting_original_unpublished_payload(tmp_path):
    import shutil

    from phmt_test_support.saved_run_profile import recover_fixture

    original, copied = tmp_path / "original", tmp_path / "copy"
    partial_fixture(original, conflicting_stage=True)
    before = {p.name: file_identity(p) for p in original.iterdir()}
    shutil.copytree(original, copied)
    with pytest.raises(ScreeningRunError):
        recover_fixture(copied, 10, 16)
    assert not (copied / "fixture.json").exists()
    assert before == {p.name: file_identity(p) for p in original.iterdir()}


def interrupted_control_directory(
    path, *, status="failed", phase="prepare", count=100, timeout=True
):
    """Opaque copy-control bytes, not a valid scientific or ledger fixture."""
    path.mkdir()
    (path / "run.json").write_text(
        json.dumps(
            {
                "schema": "pharmacophoremt.saved-reader-profile-run@1",
                "status": status,
                "commands": [
                    {
                        "phase": phase,
                        "count": count,
                        "timed_out": timeout,
                        "arguments": ["never-replay-saved-commands"],
                    }
                ],
            }
        )
    )
    partial = path / f"work-{count}"
    partial.mkdir()
    (partial / "run.sqlite3").write_bytes(b"opaque owned copy-control bytes")
    (partial / "work.jsonl").write_text("opaque owned manifest bytes")
    return partial


def test_recovery_copy_provenance_detects_later_original_change(tmp_path, monkeypatch):
    from devtools.profile_saved_run import copy_failed_fixture, verify_original

    source, destination = tmp_path / "source", tmp_path / "new"
    partial = interrupted_control_directory(source)
    destination.mkdir()
    monkeypatch.setattr(
        "subprocess.run",
        lambda *a, **kw: pytest.fail("saved commands must never be replayed"),
    )
    count, receipt = copy_failed_fixture(source, destination)
    assert count == 100
    assert receipt["original_preparation_qualified"] is False
    assert {p.name: file_identity(p) for p in partial.iterdir()} == {
        p.name: file_identity(p) for p in (destination / "work-100").iterdir()
    }
    verify_original(receipt)
    (partial / "work.jsonl").write_text("external change after verified copy")
    with pytest.raises(AssertionError):
        verify_original(receipt)


@pytest.mark.parametrize(
    "changes",
    [
        {"status": "completed"},
        {"phase": "measure"},
        {"count": True},
        {"count": 99},
        {"timeout": False},
        {"timeout": 0},
        {"timeout": "false"},
        {"timeout": 1},
    ],
)
def test_recovery_copy_refuses_ineligible_control_metadata(tmp_path, changes):
    from devtools.profile_saved_run import copy_failed_fixture

    source, destination = tmp_path / "source", tmp_path / "new"
    interrupted_control_directory(source, **changes)
    destination.mkdir()
    with pytest.raises(ValueError):
        copy_failed_fixture(source, destination)
    assert list(destination.iterdir()) == []


def test_recovery_copy_refuses_original_subdirectories_and_links(tmp_path):
    from devtools.profile_saved_run import copy_failed_fixture

    source, destination = tmp_path / "source", tmp_path / "new"
    partial = interrupted_control_directory(source)
    with pytest.raises(ValueError, match="outside the original"):
        copy_failed_fixture(source, source / "nested-output")
    assert not (source / "nested-output").exists()
    (partial / "run.sqlite3").unlink()
    (partial / "run.sqlite3").symlink_to(partial / "work.jsonl")
    destination.mkdir()
    with pytest.raises(ValueError, match="linked"):
        copy_failed_fixture(source, destination)
    assert list(destination.iterdir()) == []
