"""Offline declaration guards; these never establish molecular performance."""

import hashlib
import json
import subprocess
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path

import pytest

from devtools import feature_reuse_plan as control

ROOT = Path(__file__).resolve().parents[1]
STAMP = "2026-11-08T03:40:45+00:00"
PARENT = "a1d210abb7308205d7ed87375678fb2b8b011907"


def plan():
    return control.build_plan(parent_source=PARENT, recorded_at_utc=STAMP)


def test_complete_denominators_and_balanced_serial_order():
    declared = plan()
    pairs = declared["pairs"]
    assert len(pairs) == 48
    assert len({pair["pair_key"] for pair in pairs}) == 48
    assert {pair["cid"] for pair in pairs} == {1983, 2244, 2519}
    assert Counter(pair["arm_order"][0] for pair in pairs) == {
        "fresh": 24,
        "reused": 24,
    }
    for cid in (1983, 2244, 2519):
        for workload in ("one-caffeine", "one-aspirin", "two-mixed", "eight-repeated"):
            stratum = [
                pair
                for pair in pairs
                if pair["cid"] == cid and pair["workload"] == workload
            ]
            assert [pair["repeat"] for pair in stratum] == [0, 1, 2, 3]
            assert [pair["arm_order"] for pair in stratum] == [
                ["fresh", "reused"],
                ["reused", "fresh"],
                ["fresh", "reused"],
                ["reused", "fresh"],
            ]
    assert sum(len(pair["queries"]) for pair in pairs) == 144
    assert sum(len(pair["arm_order"]) for pair in pairs) == 96
    assert declared["admission_pilot"]["arm_processes"] == 2
    assert not declared["admission_pilot"]["included_in_timed_samples"]
    assert declared["state"] == "declared_not_executed"
    assert not any(declared["claims"].values())


def test_single_query_strata_cover_both_geometries_and_repetition_is_explicit():
    pairs = plan()["pairs"][:4]
    expected = [
        ["caffeine-acceptors"],
        ["aspirin-acceptors"],
        ["caffeine-acceptors", "aspirin-acceptors"],
        ["caffeine-acceptors", "aspirin-acceptors"] * 4,
    ]
    for pair, references in zip(pairs, expected, strict=True):
        assert [query["reference"] for query in pair["queries"]] == references
        assert len({query["key"] for query in pair["queries"]}) == len(references)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda p: p["pairs"].pop(),
        lambda p: p["pairs"][0]["arm_order"].pop(),
        lambda p: p["pairs"][1]["queries"].clear(),
        lambda p: p["pairs"].reverse(),
        lambda p: p["settings"].update(max_placements=2),
        lambda p: p["settings"]["distance_tolerance"].update(unit="angstrom"),
        lambda p: p["source_records"][0]["snapshot"].update(sha256="0" * 64),
        lambda p: p["execution_admission"].update(memory_bytes=1073741824),
        lambda p: p["denominators"].update(sources=True),
        lambda p: p["claims"].update(performance_improvement=True),
        lambda p: p.update(samples=[]),
        lambda p: p["measurement_contract"].update(reused="Do not charge build cost"),
    ],
)
def test_omissions_scientific_drift_budget_changes_and_invented_results_are_refused(
    mutation,
):
    altered = deepcopy(plan())
    mutation(altered)
    with pytest.raises(ValueError, match="fixed prospective declaration"):
        control.validate_plan(altered)


@pytest.mark.parametrize(
    "parent,stamp",
    [
        ("main", STAMP),
        (PARENT, "2026-11-08T03:40:45"),
        (PARENT, "2026-11-08T03:40:45+01:00"),
        (PARENT, None),
    ],
)
def test_producer_and_explicit_utc_are_required(parent, stamp):
    with pytest.raises(ValueError):
        control.build_plan(parent_source=parent, recorded_at_utc=stamp)


def test_frozen_equality_plan_cannot_drift(tmp_path, monkeypatch):
    modified = tmp_path / "original.json"
    modified.write_bytes(control.ORIGINAL.read_bytes() + b" ")
    monkeypatch.setattr(control, "ORIGINAL", modified)
    with pytest.raises(ValueError, match="original prospective equality plan changed"):
        plan()


def test_snapshot_checks_entire_bytes_including_same_size_corruption(tmp_path):
    path = tmp_path / "fixture.h5msm"
    raw = b"opaque frozen bytes" * 5000
    path.write_bytes(raw)
    identity = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    assert control.verify_snapshot(path, identity) == identity
    path.write_bytes(raw[:-1] + b"X")
    with pytest.raises(ValueError, match="snapshot bytes differ"):
        control.verify_snapshot(path, identity)
    path.write_bytes(raw + b"X")
    with pytest.raises(ValueError, match="snapshot bytes differ"):
        control.verify_snapshot(path, identity)


def test_missing_relocated_inputs_never_trigger_acquisition_or_create_files(tmp_path):
    missing = tmp_path / "absent"
    with pytest.raises(FileNotFoundError):
        control.verify_inputs(plan(), snapshot_root=missing)
    assert not missing.exists()


def test_cli_operates_without_site_or_scientific_imports_and_preserves_existing_plan(
    tmp_path,
):
    destination = tmp_path / "plan.json"
    # Scientific imports fail rather than being silently optional. This child
    # checks declaration mechanics only, without replacing a scientific tool.
    script = """
import importlib.abc
import sys
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'pharmacophoremt', 'molsysmt', 'numpy',
                'scipy', 'rdkit', 'pyunitwizard', 'ackredit'}:
            raise AssertionError('unexpected scientific import: ' + fullname)
sys.meta_path.insert(0, Block())
sys.path.insert(0, sys.argv[1])
from devtools.feature_reuse_plan import main
raise SystemExit(main(sys.argv[2:]))
"""
    command = [sys.executable, "-I", "-S", "-B", "-c", script, str(ROOT)]
    written = subprocess.run(
        [*command, "--write", str(destination), "--parent-source", PARENT],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert written.returncode == 0, written.stderr
    original = destination.read_bytes()
    checked = subprocess.run(
        [*command, "--check", str(destination)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert checked.returncode == 0, checked.stderr
    assert json.loads(checked.stdout) == {
        "valid_declaration": True,
        "native_measurement_executed": False,
    }
    repeated = subprocess.run(
        [*command, "--write", str(destination), "--parent-source", PARENT],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert repeated.returncode != 0
    assert "FileExistsError" in repeated.stderr
    assert destination.read_bytes() == original
