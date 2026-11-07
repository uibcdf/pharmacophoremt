"""Fixed synthetic saved-reader profile; no molecular work or timing assertions."""

import csv
import hashlib
import json
import time
from itertools import islice
from pathlib import Path

COUNTS = (100, 1000, 10000)
PADDING_BYTES = 256
CRITERION = "checked_pose_coverage@1"
COMMITTED = (0, 1, 2, 3, 6, 7, 8)
COLUMNS = (
    "work_key",
    "source_key",
    "occurrence_key",
    "status",
    "ranking_score",
    "score_method",
)


def file_identity(path):
    digest = hashlib.sha256()
    size = 0
    with Path(path).open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
            size += len(block)
    return {"bytes": size, "sha256": digest.hexdigest()}


def mapping(ordinal):
    return {
        "work_key": f"work:{ordinal}",
        "source_key": f"source:{ordinal // 2}",
        "occurrence_key": f"row:{ordinal}",
    }


def outcome(ordinal, padding_bytes=PADDING_BYTES):
    residue = ordinal % 10
    if residue in (4, 9):
        raise ValueError("pending/begun-only work has no outcome")
    score = 1.0 if residue in (0, 5, 6) else 0.5 if residue in (1, 7) else 0.0
    status = "matched" if score else "not_matched"
    if residue == 3:
        score, status = None, "failed"
    return {
        **mapping(ordinal),
        "native_result": {
            "pose_id": f"work:{ordinal}",
            "status": status,
            "fit_value": score,
            "synthetic_reader_fixture": True,
            "padding": "x" * padding_bytes,
        },
        "ranking_score": score,
        "score_method": CRITERION,
    }


def expected_summary(count):
    blocks = count // 10
    return {
        "counts": {
            "declared_work": count,
            "committed_work": 7 * blocks,
            "scored_work": 6 * blocks,
            "matched_work": 4 * blocks,
            "not_matched_work": 2 * blocks,
            "failed_work": blocks,
            "pending_work": 3 * blocks,
        },
        "attempts": {
            "started": 9 * blocks,
            "staged": 8 * blocks,
            "committed": 7 * blocks,
        },
    }


def ranked_ordinals(count):
    """Independent table oracle: positive ties first, then lower ties, then zeros."""
    for residues in ((0, 6), (1, 7), (2, 8)):
        for block in range(count // 10):
            for residue in residues:
                yield 10 * block + residue


def build_fixture(directory, count, padding_bytes=PADDING_BYTES):
    """Create the declared fixture using public durability operations only."""
    if type(count) is not int or count <= 0 or count % 10:
        raise ValueError("count must be a positive multiple of ten")
    if type(padding_bytes) is not int or padding_bytes < 0:
        raise ValueError("padding_bytes must be a nonnegative integer")
    from pharmacophoremt_results import ScreeningRunStore

    directory = Path(directory)
    directory.mkdir()
    manifest = directory / "work.jsonl"
    with manifest.open("x", encoding="utf-8") as output:
        for ordinal in range(count):
            output.write(json.dumps(mapping(ordinal)) + "\n")
    database = directory / "run.sqlite3"
    with ScreeningRunStore.create(
        database,
        run_id=f"synthetic-profile:{count}",
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
        for ordinal in reversed(range(count)):
            if ordinal % 10 == 4:
                continue
            attempt = store.begin(mapping(ordinal)["work_key"])
            if ordinal % 10 == 9:
                continue
            store.stage(attempt, outcome(ordinal, padding_bytes))
            if ordinal % 10 != 5:
                assert store.publish(attempt)
    configuration = {
        "schema": "pharmacophoremt.synthetic-reader-profile@1",
        "declared_work": count,
        "padding_bytes": padding_bytes,
        "database": database.name,
        "database_identity": file_identity(database),
        "manifest": manifest.name,
        "manifest_identity": file_identity(manifest),
        "expected": expected_summary(count),
        "scope": "Synthetic saved-format records; no molecular/native evaluation or activity data.",
    }
    (directory / "fixture.json").write_text(json.dumps(configuration, indent=2) + "\n")
    return configuration


def check_summary(actual, count):
    expected = expected_summary(count)
    assert actual["counts"] == expected["counts"]
    assert actual["attempts"] == expected["attempts"]
    assert actual["manifest_work_complete"] is False
    assert actual["run_id"] == f"synthetic-profile:{count}"


def check_top(actual, count, limit, padding_bytes=PADDING_BYTES):
    check_summary(actual["summary"], count)
    expected = [
        {"manifest_ordinal": ordinal, "outcome": outcome(ordinal, padding_bytes)}
        for ordinal in islice(ranked_ordinals(count), limit)
    ]
    assert actual["records"] == expected
    assert actual["limit"] == limit


def check_export(receipt, count, file_format, padding_bytes=PADDING_BYTES):
    path = Path(receipt["path"])
    assert receipt["published"] is True
    assert receipt["exported_records"] == 7 * (count // 10)
    assert receipt["pending_work"] == 3 * (count // 10)
    assert {key: receipt[key] for key in ("bytes", "sha256")} == file_identity(path)
    expected = (outcome(i, padding_bytes) for i in range(count) if i % 10 in COMMITTED)
    with path.open(encoding="utf-8", newline="") as source:
        if file_format == "jsonl":
            actual = (json.loads(line) for line in source)
        else:
            reader = csv.DictReader(source)
            assert tuple(reader.fieldnames) == COLUMNS
            actual = iter(reader)
        total = 0
        for wanted in expected:
            received = next(actual)
            if file_format == "csv":
                wanted = {
                    "work_key": wanted["work_key"],
                    "source_key": wanted["source_key"],
                    "occurrence_key": wanted["occurrence_key"],
                    "status": wanted["native_result"]["status"],
                    "ranking_score": ""
                    if wanted["ranking_score"] is None
                    else str(wanted["ranking_score"]),
                    "score_method": CRITERION,
                }
            assert received == wanted
            total += 1
        assert next(actual, None) is None
    assert total == receipt["exported_records"]


def measure(call, *, sample=None):
    """Time only the selected operation; result checking belongs to its caller."""
    cpu_start = time.process_time_ns()
    wall_start = time.perf_counter_ns()
    sample = {} if sample is None else sample
    try:
        result = call()
    finally:
        sample.update(
            wall_ns=time.perf_counter_ns() - wall_start,
            process_cpu_ns=time.process_time_ns() - cpu_start,
        )
    return result, sample


def profile_fixture(directory, *, repeats=5, on_update=None):
    """Measure an immutable fixture with complete verification and exact oracles."""
    if type(repeats) is not int or repeats < 1:
        raise ValueError("repeats must be a positive integer")
    from pharmacophoremt_results import ScreeningRunView

    directory = Path(directory)
    config = json.loads((directory / "fixture.json").read_text())
    database = directory / config["database"]
    assert file_identity(database) == config["database_identity"]
    count, padding = config["declared_work"], config["padding_bytes"]
    report = {
        "schema": "pharmacophoremt.saved-reader-profile@1",
        "fixture": config,
        "status": "running",
        "repeats": repeats,
        "samples": {},
        "exports": [],
        "cache_state": "OS cache uncontrolled; imports precede first verified open",
    }

    def retain():
        if on_update is not None:
            on_update(report)

    view = None
    active = {"operation": "first_verified_open", "phase": "call", "timing": {}}
    try:
        view, report["first_verified_open"] = measure(
            lambda: ScreeningRunView.open(database), sample=active["timing"]
        )
        retain()
        operations = ("progress", "top10", "top100", "jsonl", "csv")
        for operation in operations:
            report["samples"][operation] = []
            for repeat in range(-1, repeats):
                label = "warmup" if repeat < 0 else f"repeat{repeat}"
                active = {
                    "operation": operation,
                    "repeat": label,
                    "phase": "call",
                    "timing": {},
                }
                if operation == "progress":
                    result, sample = measure(view.progress, sample=active["timing"])
                    active["phase"] = "validation"
                    check_summary(result, count)
                elif operation.startswith("top"):
                    limit = int(operation[3:])
                    result, sample = measure(
                        lambda: view.top_results(score_method=CRITERION, limit=limit),
                        sample=active["timing"],
                    )
                    active["phase"] = "validation"
                    check_top(result, count, limit, padding)
                else:
                    destination = directory / f"{operation}-{label}.{operation}"
                    active["destination"] = str(destination)
                    method = view.to_jsonl if operation == "jsonl" else view.to_csv
                    result, sample = measure(
                        lambda: method(destination), sample=active["timing"]
                    )
                    active["phase"] = "validation"
                    check_export(result, count, operation, padding)
                    report["exports"].append(
                        {"phase": label, "file_format": operation, "receipt": result}
                    )
                if repeat >= 0:
                    report["samples"][operation].append(sample)
                retain()
        assert file_identity(database) == config["database_identity"]
        assert (
            file_identity(directory / config["manifest"]) == config["manifest_identity"]
        )
        report.update(
            status="completed",
            independent_oracles_passed=True,
            original_input_bytes_unchanged=True,
        )
        retain()
        return report
    except BaseException as error:
        report.update(
            status="failed",
            error_type=type(error).__name__,
            error=str(error),
            failed_operation=active,
        )
        retain()
        raise
    finally:
        if view is not None:
            view.close()
