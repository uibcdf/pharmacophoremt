"""Offline admission guards for the tiny PubChem3D receiving pilot.

Source files here are opaque dummy bytes. Molecular interpretation belongs to
the provider and is deliberately absent from these administrative controls.
"""

from __future__ import annotations

import builtins
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
PILOT = ROOT / "phmt_test_support/pubchem3d_receiving_pilot.py"
_spec = importlib.util.spec_from_file_location("pubchem_receiving_guard", PILOT)
_pilot = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_pilot)


class TestPubChem3DReceivingPilot(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="phmt-pubchem-receiving-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.plan_path = self.root / "plan.json"
        self.acquisition_path = self.root / "acquisition.json"
        self.plan = {
            "schema": "pharmacophoremt.pubchem3d-pilot-plan@1",
            "cids": [1983, 2244, 2519],
            "molecules": [
                {"cid": 1983, "formula": "C8H9NO2", "n_atoms": 20, "n_hydrogens": 9},
                {"cid": 2244, "formula": "C9H8O4", "n_atoms": 21, "n_hydrogens": 8},
                {"cid": 2519, "formula": "C8H10N4O2", "n_atoms": 24, "n_hydrogens": 10},
            ],
            "acquisition": {"record_type": "3d", "conformers_per_cid": 1},
            "preparation": {"policy": "provider-owned supplied geometry"},
            "query": {"scope": "declared software controls"},
        }
        self.write_plan()
        self.originals = {}
        records = []
        for index, cid in enumerate(self.plan["cids"]):
            path = self.root / f"source-{index}.sdf"
            raw = f"opaque original bytes for CID {cid}\n".encode()
            path.write_bytes(raw)
            self.originals[path] = raw
            records.append(
                {
                    "cid": cid,
                    "conformer_id": f"{cid:08X}00000001",
                    "status": "received",
                    "sdf": {
                        "path": path.name,
                        "bytes": len(raw),
                        "sha256": hashlib.sha256(raw).hexdigest(),
                    },
                }
            )
        self.acquisition = {
            "plan_sha256": hashlib.sha256(self.plan_path.read_bytes()).hexdigest(),
            "records": records,
        }
        self.write_acquisition()

    def write_plan(self):
        self.plan_path.write_text(json.dumps(self.plan) + "\n", encoding="utf-8")

    def write_acquisition(self):
        self.acquisition_path.write_text(
            json.dumps(self.acquisition) + "\n", encoding="utf-8"
        )

    @contextmanager
    def source_access_forbidden(self):
        sources = {str(path) for path in self.originals}

        def protect(original):
            def guarded(path, *args, **kwargs):
                if str(path) in sources:
                    raise AssertionError(
                        "preflight reached a source before metadata admission"
                    )
                return original(path, *args, **kwargs)

            return guarded

        with (
            patch.object(Path, "open", protect(Path.open)),
            patch.object(builtins, "open", protect(builtins.open)),
            patch.object(io, "open", protect(io.open)),
        ):
            yield

    def validate(self):
        return _pilot.validate_acquisition(self.plan_path, self.acquisition_path)

    def test_valid_opaque_preflight_and_import_are_stdlib_only(self):
        script = """
import importlib.util, sys
blocked = {'pharmacophoremt', 'molsysmt', 'numpy', 'scipy', 'rdkit'}
class DenyScience:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in blocked:
            raise AssertionError('scientific import in metadata preflight: ' + fullname)
sys.meta_path.insert(0, DenyScience())
spec = importlib.util.spec_from_file_location('isolated_pilot', sys.argv[1])
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)
pilot.validate_acquisition(sys.argv[2], sys.argv[3])
assert not any(name.split('.')[0] in blocked for name in sys.modules)
print('validated without science')
"""
        result = subprocess.run(
            [
                sys.executable,
                "-P",
                "-c",
                script,
                str(PILOT),
                str(self.plan_path),
                str(self.acquisition_path),
            ],
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "validated without science")

    def test_wrong_plan_hash_fails_before_source_access(self):
        self.acquisition["plan_sha256"] = "0" * 64
        self.write_acquisition()
        with self.source_access_forbidden(), self.assertRaises(ValueError):
            self.validate()

    def test_every_record_must_be_received_before_any_source_is_read(self):
        records = deepcopy(self.acquisition["records"])
        failed = deepcopy(records)
        failed[-1]["status"] = "failed"
        missing = deepcopy(records)
        missing[-1].pop("status")
        for altered in ([], records[:2], failed, missing, [*records[:2], None]):
            with self.subTest(records=altered):
                self.acquisition["records"] = altered
                self.write_acquisition()
                with self.source_access_forbidden(), self.assertRaises(ValueError):
                    self.validate()

    def test_candidate_order_duplicates_and_unknown_cids_are_refused(self):
        records = deepcopy(self.acquisition["records"])
        duplicate = deepcopy(records)
        duplicate[-1]["cid"] = records[0]["cid"]
        unknown = deepcopy(records)
        unknown[-1]["cid"] = 999999
        for altered in (list(reversed(records)), duplicate, unknown):
            with self.subTest(records=altered):
                self.acquisition["records"] = altered
                self.write_acquisition()
                with self.source_access_forbidden(), self.assertRaises(ValueError):
                    self.validate()
        self.plan["cids"] = list(reversed(self.plan["cids"]))
        self.write_plan()
        self.acquisition = {
            "plan_sha256": hashlib.sha256(self.plan_path.read_bytes()).hexdigest(),
            "records": list(reversed(records)),
        }
        self.write_acquisition()
        with self.source_access_forbidden(), self.assertRaises(ValueError):
            self.validate()

    def test_missing_or_malformed_identity_cannot_trigger_a_fallback(self):
        records = deepcopy(self.acquisition["records"])
        changes = [
            {"conformer_id": None},
            {"conformer_id": 1},
            {"conformer_id": "not-a-native-id"},
            {"conformer_id": "00000001"},
            {"sdf": None},
            {"sdf": {"path": None, "sha256": "0" * 64, "bytes": 1}},
            {"sdf": {"path": "source-2.sdf", "sha256": "wrong", "bytes": 1}},
            {"sdf": {"path": "source-2.sdf", "sha256": "0" * 64, "bytes": True}},
            {"sdf": {"path": "source-2.sdf", "sha256": "0" * 64, "bytes": 0}},
            {
                "sdf": {
                    "path": "source-2.sdf",
                    "sha256": "0" * 64,
                    "bytes": 2 * 1024 * 1024 + 1,
                }
            },
        ]
        for change in changes:
            with self.subTest(change=change):
                altered = deepcopy(records)
                altered[-1].update(change)
                self.acquisition["records"] = altered
                self.write_acquisition()
                with self.source_access_forbidden(), self.assertRaises(ValueError):
                    self.validate()

    def test_byte_or_length_corruption_is_detected_without_rewriting_sources(self):
        originals = deepcopy(self.originals)
        records = deepcopy(self.acquisition["records"])
        first = next(iter(originals))
        for change in ("same-length-bytes", "truncated-bytes", "declared-length"):
            with self.subTest(change=change):
                for path, raw in originals.items():
                    path.write_bytes(raw)
                self.acquisition["records"] = deepcopy(records)
                if change == "same-length-bytes":
                    raw = originals[first]
                    first.write_bytes(b"X" + raw[1:])
                elif change == "truncated-bytes":
                    first.write_bytes(originals[first][:-1])
                else:
                    self.acquisition["records"][0]["sdf"]["bytes"] += 1
                self.write_acquisition()
                before = {path: path.read_bytes() for path in originals}
                with self.assertRaises(ValueError):
                    self.validate()
                self.assertEqual(
                    {path: path.read_bytes() for path in originals}, before
                )

    def test_relative_locations_and_original_manifest_bytes_are_preserved(self):
        plan_before = self.plan_path.read_bytes()
        acquisition_before = self.acquisition_path.read_bytes()
        result = self.validate()
        self.assertEqual(result["plan_sha256"], hashlib.sha256(plan_before).hexdigest())
        self.assertEqual(
            result["acquisition_sha256"], hashlib.sha256(acquisition_before).hexdigest()
        )
        self.assertEqual(
            [record["sdf"]["path"] for record in result["records"]],
            [str(path) for path in self.originals],
        )
        self.assertEqual(self.plan_path.read_bytes(), plan_before)
        self.assertEqual(self.acquisition_path.read_bytes(), acquisition_before)
        self.assertEqual(
            {path: path.read_bytes() for path in self.originals}, self.originals
        )

    def test_run_refuses_invalid_acquisition_or_existing_output_before_science(self):
        valid = deepcopy(self.acquisition)
        self.acquisition["records"][-1]["status"] = "failed"
        self.write_acquisition()
        output = self.root / "new-output"
        blocked = {"pharmacophoremt", "molsysmt", "numpy", "scipy", "rdkit"}

        class DenyScience:
            def find_spec(self, fullname, path=None, target=None):
                if fullname.split(".")[0] in blocked:
                    raise AssertionError("science imported before complete admission")

        guard = DenyScience()
        sys.meta_path.insert(0, guard)
        try:
            with self.source_access_forbidden(), self.assertRaises(ValueError):
                _pilot.run(self.plan_path, self.acquisition_path, output)
            self.assertFalse(output.exists())
            self.acquisition = valid
            self.write_acquisition()
            output.mkdir()
            sentinel = output / "caller-owned.bin"
            sentinel.write_bytes(b"preserve this existing output")
            with self.assertRaises(FileExistsError):
                _pilot.run(self.plan_path, self.acquisition_path, output)
            self.assertEqual(sentinel.read_bytes(), b"preserve this existing output")
        finally:
            sys.meta_path.remove(guard)
