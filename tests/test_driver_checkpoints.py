"""Real-provider, bounded native prefixes and interruption of owned children only."""

import importlib
import json
import multiprocessing
import os
import runpy
import signal
from pathlib import Path

import pytest

DRIVERS = ("snapshot", "typed")
pytestmark = pytest.mark.skipif(
    "fork" not in multiprocessing.get_all_start_methods(),
    reason="Controlled local POSIX child interruption requires fork",
)


@pytest.fixture(scope="module", autouse=True)
def real_providers():
    import ackredit

    import pharmacophoremt

    return ackredit, pharmacophoremt


def _driver(name):
    path = Path(__file__).resolve().parents[1] / (
        "devtools/qualify_" + name + "_retrieval.py"
    )
    return runpy.run_path(str(path), run_name="driver_under_test")["main"]


def _probe(name, output, mode, connection):
    import ackredit

    from phmt_test_support.retrieval_controls import exact_mapping_oracle
    from phmt_test_support.snapshot_retrieval import (
        SnapshotRetrievalStudy,
        project,
        reference_proposals,
    )

    module = importlib.import_module("phmt_test_support." + name + "_retrieval")
    spec = module.declaration()
    spec["unit_contexts"] = ["nm", "pm"]
    module.declaration = lambda: spec

    def compare(entries, declaration, progress):
        study = SnapshotRetrievalStudy(entries, declaration["bin_widths"][0])
        state = {
            "test_body": "two actual native calls; not a full declared experiment",
            "complete": False,
            "rows": [],
            "reference_calls": {"exhaustive": 0, "retrieved": 0},
            "original_manifest": study.describe(),
        }
        progress(state)
        query = declaration["queries"][0]
        for ordinal in (1, 0):
            native = study.original_inventory(ordinal)
            actual = reference_proposals(query, native)
            oracle = exact_mapping_oracle(query, {"features": project(native)})
            assert actual == oracle
            assert bool(actual) == (ordinal == 1)
            state["reference_calls"]["exhaustive"] += 1
            state["rows"].append({"ordinal": ordinal, "mappings": actual})
            if mode == "replacement" and ordinal == 0:
                from phmt_test_support import retrieval_checkpoint

                original = retrieval_checkpoint.os.replace

                def pause_replace(source, destination):
                    connection.send(
                        {"ready": True, "before": Path(output).read_bytes()}
                    )
                    connection.recv()
                    return original(source, destination)

                retrieval_checkpoint.os.replace = pause_replace
            progress(state)
            if ordinal == 1:
                if mode == "partial":
                    connection.send(
                        {"ready": True, "actual": ackredit.get_attribution().to_dict()}
                    )
                    connection.recv()
                if mode == "failure":
                    raise ValueError(
                        "controlled scientific failure after one native call"
                    )
        state["complete"] = True
        progress(state)
        return state

    setattr(
        module, "compare_retrieval" if name == "snapshot" else "compare_domain", compare
    )
    code = _driver(name)(
        [
            "--output",
            str(output),
            "--snapshot-context",
            os.environ.get("PHMT_RECEIVING_CONTEXT", "source"),
            "--admission-sha256",
            "a" * 64,
        ]
    )
    connection.send({"code": code})


def _start(name, output, mode):
    context = multiprocessing.get_context("fork")
    parent, child = context.Pipe()
    process = context.Process(target=_probe, args=(name, output, mode, child))
    process.start()
    child.close()
    return process, parent


def _stop(process, connection):
    if process.is_alive():
        process.terminate()
        process.join(5)
    if process.is_alive():
        process.kill()
        process.join(5)
    connection.close()
    assert not process.is_alive()


@pytest.mark.parametrize("name", DRIVERS)
@pytest.mark.parametrize("signum", [signal.SIGTERM, signal.SIGKILL])
def test_driver_partial_checkpoint_keeps_real_attribution(tmp_path, name, signum):
    import ackredit

    output = tmp_path / "partial.json"
    process, connection = _start(name, output, "partial")
    try:
        assert connection.poll(20), "Owned child did not reach its native checkpoint"
        ready = connection.recv()
        assert ready["ready"]
        saved = output.read_bytes()
        report = json.loads(saved)
        assert report["actual_attribution"] == ready["actual"]
        portable = ackredit.Attribution.from_dict(report["actual_attribution"])
        assert portable.to_dict()["items"] and portable.to_dict()["uses"]
        assert report["status"] == report["policies"][0]["status"] == "running"
        assert len(report["policies"][0]["scientific"]["rows"]) == 1
        assert report["checkpoint"]["uncommitted_work"] == "unknown"
        assert report["checkpoint"]["attribution"]["status"] == "recorded"
        os.kill(process.pid, signum)
        process.join(5)
        assert process.exitcode == -signum
        assert output.read_bytes() == saved
    finally:
        _stop(process, connection)


@pytest.mark.parametrize("name", DRIVERS)
def test_kill_during_replacement_preserves_previous_science_and_credit(tmp_path, name):
    output = tmp_path / "atomic.json"
    process, connection = _start(name, output, "replacement")
    try:
        assert connection.poll(20)
        ready = connection.recv()
        os.kill(process.pid, signal.SIGKILL)
        process.join(5)
        assert process.exitcode == -signal.SIGKILL
        assert output.read_bytes() == ready["before"]
        report = json.loads(output.read_bytes())
        assert len(report["policies"][0]["scientific"]["rows"]) == 1
        assert report["actual_attribution"]["items"]
        assert report["checkpoint"]["uncommitted_work"] == "unknown"
        assert not report["policies"][0]["scientific"]["complete"]
    finally:
        _stop(process, connection)


@pytest.mark.parametrize("name", DRIVERS)
@pytest.mark.parametrize("mode,code", [("complete", 0), ("failure", 1)])
def test_complete_and_failed_driver_prefixes_keep_original_science(
    tmp_path, name, mode, code
):
    output = tmp_path / "prefix.json"
    process, connection = _start(name, output, mode)
    try:
        assert connection.poll(20)
        assert connection.recv() == {"code": code}
        process.join(5)
        assert process.exitcode == 0
        report = json.loads(output.read_bytes())
        assert report["status"] == ("completed" if code == 0 else "failed")
        assert report["actual_attribution"]["items"]
        if code == 0:
            assert [p["unit_policy"] for p in report["policies"]] == ["nm", "pm"]
            scientific = [p["scientific"] for p in report["policies"]]
            assert scientific[0] == scientific[1]
            assert all(p["complete"] and len(p["rows"]) == 2 for p in scientific)
        else:
            assert report["failure"] == {
                "type": "ValueError",
                "reason": "controlled scientific failure after one native call",
            }
            assert report["policies"][0]["status"] == "failed"
            assert len(report["policies"][0]["scientific"]["rows"]) == 1
    finally:
        _stop(process, connection)


@pytest.mark.parametrize("name", DRIVERS)
@pytest.mark.parametrize("invalid", ["existing", "admission"])
def test_driver_refuses_existing_output_or_invalid_admission(tmp_path, name, invalid):
    output = tmp_path / "existing.json"
    output.write_bytes(b"original caller bytes")
    argv = [
        "--output",
        str(output),
        "--snapshot-context",
        "source",
        "--admission-sha256",
    ]
    with pytest.raises(FileExistsError if invalid == "existing" else ValueError):
        _driver(name)(argv + ["a" * 64 if invalid == "existing" else "invalid"])
    assert output.read_bytes() == b"original caller bytes"


@pytest.mark.parametrize("first_export_succeeds", [True, False])
def test_checkpoint_export_failure_keeps_last_credit_and_completed_science(
    tmp_path, first_export_succeeds
):
    import ackredit

    from phmt_test_support.retrieval_checkpoint import RetrievalCheckpoint

    report = {"status": "running", "policies": [{"scientific": {"rows": [1]}}]}
    output = tmp_path / "export.json"
    with ackredit.session("real checkpoint provider"):
        ackredit.register_item(
            id="phmt:test:checkpoint",
            type="software",
            title="Test control",
            version="1",
        )
        ackredit.track_item("phmt:test:checkpoint", used_by="controlled test")
        checkpoint = RetrievalCheckpoint(
            output, report, lambda: ackredit.get_attribution().to_dict()
        )

        def fail():
            raise RuntimeError("controlled export failure")

        if not first_export_succeeds:
            checkpoint.snapshot = fail
        before = ackredit.get_attribution().to_dict()
        checkpoint.retain()
        assert ackredit.get_attribution().to_dict() == before
        original = json.loads(output.read_bytes())
        report["policies"][0]["scientific"]["rows"].append(2)
        checkpoint.snapshot = fail
        checkpoint.retain()
        failed = json.loads(output.read_bytes())
        assert failed["actual_attribution"] == original["actual_attribution"]
        assert failed["policies"][0]["scientific"]["rows"] == [1, 2]
        attribution = failed["checkpoint"]["attribution"]
        assert attribution["status"] == "unavailable"
        assert attribution["recorded_sequence"] == (
            original["checkpoint"]["sequence"] if first_export_succeeds else None
        )
        if not first_export_succeeds:
            assert failed["actual_attribution"] is None
        assert attribution["failure"]["type"] == "RuntimeError"


def test_invalid_scientific_json_keeps_previous_committed_checkpoint(tmp_path):
    import ackredit

    from phmt_test_support.retrieval_checkpoint import RetrievalCheckpoint

    output = tmp_path / "serialization.json"
    report = {"status": "running", "policies": []}
    with ackredit.session("real serialization checkpoint"):
        checkpoint = RetrievalCheckpoint(
            output, report, lambda: ackredit.get_attribution().to_dict()
        )
        checkpoint.retain()
        original = output.read_bytes()
        report["invalid"] = float("nan")
        with pytest.raises(ValueError):
            checkpoint.retain()
        assert output.read_bytes() == original
        assert list(tmp_path.iterdir()) == [output]


def test_failed_atomic_write_preserves_previous_committed_checkpoint(
    tmp_path, monkeypatch
):
    import ackredit

    from phmt_test_support import retrieval_checkpoint

    output = tmp_path / "write.json"
    report = {"status": "running", "policies": []}
    with ackredit.session("real atomic checkpoint"):
        checkpoint = retrieval_checkpoint.RetrievalCheckpoint(
            output, report, lambda: ackredit.get_attribution().to_dict()
        )
        checkpoint.retain()
        original = output.read_bytes()
        report["status"] = "completed"

        def refuse(*args):
            raise OSError("controlled replacement failure")

        monkeypatch.setattr(retrieval_checkpoint.os, "replace", refuse)
        with pytest.raises(OSError, match="controlled replacement failure"):
            checkpoint.retain()
        assert output.read_bytes() == original
        assert list(tmp_path.iterdir()) == [output]
