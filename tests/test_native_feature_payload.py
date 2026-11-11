"""Native payload round trips, independent geometry expectations and cold reads."""

import hashlib
import importlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt_features import FeatureAssetError, FeatureInventoryPayload
from pharmacophoremt_features import _payload_schema as spec
from pharmacophoremt_results import canonical_json
from phmt_test_support.feature_snapshot import FeatureSnapshotStudy
from phmt_test_support.feature_snapshot_case import projection
from phmt_test_support.typed_retrieval import load_entries

PROFILE = "native-classical-v1"


def parent():
    return {
        "source_key": "nm",
        "occurrence_key": "1 nm:α",
        "artifact_sha256": None,
        "artifact_bytes": None,
        "n_atoms": 16,
        "preparation": None,
        "mapping_policy": "caller-declared-local-atom-axis@1",
    }


def inventory():
    rows = []
    for index, kind in enumerate(spec._schema.FAMILIES):
        rows.append(
            {
                "kind": kind,
                "atom_indices": [2, 4]
                if kind == "hb donor"
                else [0, 6, 8]
                if kind == "aromatic ring"
                else [2],
                "geometry_atom_indices": [0, 2, 4, 6, 8],
                "center": puw.quantity([index * 2.0, 4.0, -6.0], "angstrom"),
                "direction": puw.quantity([2.0, 0.0, 0.0], "dimensionless")
                if kind == "hb donor"
                else None,
                "normal": puw.quantity([0.0, 0.0, 3.0], "dimensionless")
                if kind == "aromatic ring"
                else None,
                "charge": puw.quantity(2.0 if kind == "positive charge" else -1.0, "e")
                if "charge" in kind
                else None,
            }
        )
    return {
        "definition": "classical_atomic_formal@1",
        "features": rows,
        "recognition": {
            "source": "analytical detached capture",
            "literal": "1 nm",
            "nested": [None, True],
        },
        "selected_atom_indices": [8, 0, 2, 4, 6],
        "structure_index": 5,
        "chemical_state": "reference",
    }


def encode(value=None, families=None, **kwargs):
    return FeatureInventoryPayload.from_inventory(
        inventory() if value is None else value,
        list(spec._schema.FAMILIES) if families is None else families,
        parent=kwargs.pop("parent", parent()),
        extraction_producer=kwargs.pop(
            "extraction_producer", {"version": "original-v1", "unknown": None}
        ),
        payload_profile=PROFILE,
        **kwargs,
    )


def reseal(payload):
    return canonical_json(
        {
            "schema": spec.SCHEMA,
            "payload": payload,
            "payload_sha256": hashlib.sha256(
                canonical_json(payload).encode()
            ).hexdigest(),
        }
    ).encode()


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("state", [None, 3, "reference", "structure"])
def test_complete_native_geometry_maps_frame_state_and_policy(unit, state):
    native = inventory()
    native["chemical_state"] = state
    before = projection(native)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = puw.configure.report()
        payload = encode(native, list(reversed(spec._schema.FAMILIES)))
        restored = payload.to_inventory(required_families=["hb donor"])
        for index, row in enumerate(restored["features"]):
            np.testing.assert_allclose(
                puw.get_value(row["center"], to_unit="nm"),
                [index * 0.2, 0.4, -0.6],
                atol=1e-15,
                rtol=0,
            )
        np.testing.assert_array_equal(
            puw.get_value(
                restored["features"][1]["direction"], to_unit="dimensionless"
            ),
            [2.0, 0.0, 0.0],
        )
        np.testing.assert_array_equal(
            puw.get_value(restored["features"][3]["normal"], to_unit="dimensionless"),
            [0.0, 0.0, 3.0],
        )
        assert puw.get_value(restored["features"][4]["charge"], to_unit="e") == 2.0
        assert restored["selected_atom_indices"] == [8, 0, 2, 4, 6]
        assert restored["structure_index"] == 5 and restored["chemical_state"] == state
        assert restored["recognition"] == native["recognition"]
        assert all(
            restored["features"][i]["geometry_atom_indices"]
            == native["features"][i]["geometry_atom_indices"]
            for i in range(6)
        )
        assert projection(native) == before
        assert payload.describe()["evaluated_families"] == list(spec._schema.FAMILIES)
        assert not payload.describe()["quantity_semantics_checked"]
        assert puw.configure.report() == policy


@pytest.fixture(scope="module")
def captured():
    import os

    return load_entries(os.environ.get("PHMT_RECEIVING_CONTEXT", "source"))


@pytest.mark.parametrize("ordinal", range(11))
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_all_frozen_original_inventories_and_original_versions(captured, ordinal, unit):
    raw = captured[ordinal]["snapshot"]
    study = FeatureSnapshotStudy(raw)
    info = study.describe()
    native = study.decode_inventory()
    source = {k: info["parent"][k] for k in parent() if k != "mapping_policy"}
    source["mapping_policy"] = spec.MAPPING_POLICY
    before = deepcopy(projection(native))
    with puw.context(standard_units=[unit, "ps", "radians"]):
        payload = encode(
            native,
            info["request"]["features"],
            parent=source,
            extraction_producer=info["producer"],
        )
        result = payload.to_inventory(required_families=info["request"]["features"])
    assert projection(result) == before
    assert result["recognition"] == native["recognition"]
    assert result.get("attribution") == native.get("attribution")
    assert payload.describe()["extraction_producer"] == info["producer"]
    assert payload.describe()["serialization"] != info["producer"]
    assert captured[ordinal]["snapshot"] == raw


def test_empty_is_evaluated_and_unobserved_remains_refused():
    native = inventory()
    native["features"] = []
    payload = encode(native, ["hb donor"], extraction_producer=None)
    info = payload.describe()
    assert info["coverage"] == {"hb donor": {"count": 0, "status": "evaluated_empty"}}
    assert info["extraction_producer"] is None
    assert payload.to_inventory(required_families=["hb donor"])["features"] == []
    with pytest.raises(FeatureAssetError) as caught:
        payload.to_inventory(required_families=["hb acceptor"])
    assert caught.value.code == "PHMT-E334"


def test_exact_bytes_and_detached_ownership_without_extraction(monkeypatch):
    from pharmacophoremt import modeler

    def forbidden(*args, **kwargs):
        raise AssertionError("Serialization cannot perform new extraction")

    monkeypatch.setattr(modeler, "get_features", forbidden)
    native = inventory()
    source = parent()
    producer = {"versions": {"original": "old"}}
    payload = encode(native, parent=source, extraction_producer=producer)
    raw = payload.to_bytes()
    native["features"].clear()
    source["source_key"] = "changed"
    producer["versions"].clear()
    info = payload.describe()
    info["parent"].clear()
    info["coverage"].clear()
    first = payload.to_inventory(required_families=["hb donor"])
    first["features"][0]["atom_indices"].clear()
    first["recognition"].clear()
    second = FeatureInventoryPayload.from_bytes(raw, payload_profile=PROFILE)
    assert second.to_bytes() == raw
    assert second.describe()["parent"]["source_key"] == "nm"
    assert second.describe()["extraction_producer"] == {"versions": {"original": "old"}}
    assert second.describe()["payload_sha256"] == hashlib.sha256(raw).hexdigest()
    assert len(second.to_inventory(required_families=["hb donor"])["features"]) == 6


@pytest.mark.parametrize(
    "change,code",
    [
        (lambda i, p: i.update(structure_index=True), "330"),
        (lambda i, p: i.update(chemical_state=False), "330"),
        (lambda i, p: i.update(selected_atom_indices=[0, 0]), "330"),
        (lambda i, p: p.update(artifact_bytes=5), "330"),
        (lambda i, p: p.update(n_atoms=257), "333"),
        (lambda i, p: p.update(mapping_policy="authenticated"), "330"),
        (lambda i, p: i.update(status="partial"), "330"),
        (lambda i, p: i.update(definition="unknown"), "331"),
        (lambda i, p: i["features"][0].update(kind="included volume"), "331"),
        (lambda i, p: i["features"][0].update(atom_indices=[True]), "330"),
        (lambda i, p: i["features"][0].update(geometry_atom_indices=[15]), "330"),
        (lambda i, p: i["features"][0].update(geometry_atom_indices=[2, 2]), "330"),
        (lambda i, p: i["features"][0].update(unknown=None), "330"),
        (
            lambda i, p: i["features"][0].update(
                direction=puw.quantity([1.0, 0.0, 0.0], "dimensionless")
            ),
            "330",
        ),
        (lambda i, p: i["features"][1].update(direction=None), "330"),
    ],
)
def test_native_layout_refusals_never_drop_maps_or_fields(change, code):
    native = inventory()
    source = parent()
    change(native, source)
    with pytest.raises(FeatureAssetError) as caught:
        encode(native, parent=source)
    assert caught.value.code == "PHMT-E" + code


@pytest.mark.parametrize(
    "index,field,value",
    [
        (0, "center", [1.0, 2.0, 3.0]),
        (0, "center", puw.quantity([1.0, 2.0, 3.0], "ps")),
        (0, "center", puw.quantity([1.0, 2.0], "nm")),
        (0, "center", puw.quantity([1.0, np.nan, 3.0], "nm")),
        (1, "direction", [1.0, 0.0, 0.0]),
        (1, "direction", puw.quantity([1.0, 0.0, 0.0], "nm")),
        (1, "direction", puw.quantity([0.0, 0.0, 0.0], "dimensionless")),
        (3, "normal", puw.quantity([1.0, 0.0], "dimensionless")),
        (4, "charge", puw.quantity(-1.0, "e")),
        (4, "charge", puw.quantity(0.0, "e")),
        (4, "charge", puw.quantity([1.0], "e")),
        (4, "charge", puw.quantity(1.0, "ps")),
        (5, "charge", puw.quantity(1.0, "e")),
    ],
)
def test_native_quantity_shapes_units_and_charge_sign(index, field, value):
    native = inventory()
    native["features"][index][field] = value
    with pytest.raises(FeatureAssetError) as caught:
        encode(native)
    assert caught.value.code == "PHMT-E332"


@pytest.mark.parametrize("mode", ["sealed-unit", "field", "seal", "shape", "charge"])
def test_cold_metadata_never_certifies_scientific_validity(mode):
    value = json.loads(encode().to_bytes())["payload"]
    rows = value["inventory"]["features"]
    if mode in ("sealed-unit", "field", "shape"):
        q = puw.quantity(
            [1.0, 2.0] if mode == "shape" else [1.0, 2.0, 3.0],
            "ps" if mode == "sealed-unit" else "nm",
        )
        rows[0]["center"] = puw.QuantityRecord.from_quantity(
            q, field="features[1].center" if mode == "field" else "features[0].center"
        ).to_dict()
    elif mode == "seal":
        rows[0]["center"]["digest"] = "0" * 64
    else:
        rows[4]["charge"] = puw.QuantityRecord.from_quantity(
            puw.quantity(-1.0, "e"), field="features[4].charge"
        ).to_dict()
    payload = FeatureInventoryPayload.from_bytes(reseal(value), payload_profile=PROFILE)
    assert not payload.describe()["quantity_semantics_checked"]
    with pytest.raises(FeatureAssetError) as caught:
        payload.to_inventory(required_families=["hb donor"])
    assert caught.value.code == "PHMT-E332"
    assert not payload.describe()["quantity_semantics_checked"]


@pytest.mark.parametrize(
    "change,code",
    [
        (lambda d: d.update(profile="unknown"), "331"),
        (lambda d: d["coverage"]["hb donor"].update(count=True), "330"),
        (lambda d: d["coverage"]["hb donor"].update(status="partial"), "330"),
        (lambda d: d.update(evaluated_families=["hb donor"]), "330"),
        (lambda d: d["inventory"]["features"][0].update(atom_indices=[999]), "330"),
        (lambda d: d["serialization"].update(operation="extraction"), "330"),
    ],
)
def test_resealed_metadata_still_requires_full_profile(change, code):
    value = json.loads(encode().to_bytes())["payload"]
    change(value)
    with pytest.raises(FeatureAssetError) as caught:
        FeatureInventoryPayload.from_bytes(reseal(value), payload_profile=PROFILE)
    assert caught.value.code == "PHMT-E" + code


@pytest.mark.parametrize(
    "mode", ["features", "text", "nodes", "depth", "cycle", "integer", "bytes"]
)
def test_finite_admission_precedes_encoding(mode):
    native = inventory()
    if mode == "features":
        native["features"] = [native["features"][0]] * 65
    if mode == "text":
        native["recognition"] = {"note": "x" * (128 * 1024)}
    if mode == "nodes":
        native["recognition"] = {"items": [None] * 16384}
    if mode == "integer":
        native["recognition"] = {"unbounded": 2**1000}
    if mode == "cycle":
        native["recognition"]["cycle"] = native["recognition"]
    if mode == "depth":
        value = None
        for _ in range(26):
            value = [value]
        native["recognition"] = {"nested": value}
    with pytest.raises(FeatureAssetError) as caught:
        if mode == "bytes":
            FeatureInventoryPayload.from_bytes(
                b"x" * (2 * 1024 * 1024 + 1), payload_profile=PROFILE
            )
        else:
            encode(native)
    assert caught.value.code == "PHMT-E333"


@pytest.mark.parametrize(
    "argument,value",
    [
        ("inventory", None),
        ("parent", []),
        ("extraction_producer", "new"),
        ("evaluated_families", []),
        ("evaluated_families", ["hb donor", "hb donor"]),
        ("payload_profile", "auto"),
    ],
)
def test_closed_argument_contracts(argument, value):
    args = dict(
        inventory=inventory(),
        evaluated_families=list(spec._schema.FAMILIES),
        parent=parent(),
        extraction_producer=None,
        payload_profile=PROFILE,
    )
    args[argument] = value
    with pytest.raises(FeatureAssetError) as caught:
        FeatureInventoryPayload.from_inventory(**args)
    assert caught.value.code == "PHMT-E301"


def test_real_attribution_original_references_and_no_new_extraction_credit(captured):
    import ackredit

    study = FeatureSnapshotStudy(captured[1]["snapshot"])
    native = study.decode_inventory()
    info = study.describe()
    assert native["attribution"]["host_references"]
    source = {k: info["parent"][k] for k in parent() if k != "mapping_policy"}
    source["mapping_policy"] = spec.MAPPING_POLICY
    with (
        ackredit.session("native-payload"),
        ackredit.capture("serialization-and-reading") as captured_run,
    ):
        before = ackredit.get_attribution().to_dict()
        payload = encode(
            native,
            info["request"]["features"],
            parent=source,
            extraction_producer=info["producer"],
        )
        result = payload.to_inventory(required_families=info["request"]["features"])
        assert result["attribution"] == native["attribution"]
        assert ackredit.get_attribution().to_dict() == before
    assert not captured_run.attribution.to_dict()["items"]
    assert not captured_run.attribution.to_dict()["uses"]


def test_actual_catalog_capture_and_preserved_native_cause(monkeypatch):
    import smonitor
    from smonitor.handlers import MemoryHandler

    from pharmacophoremt._private import native_feature_payload

    class PrivateFailure(Exception):
        def __str__(self):
            raise AssertionError("Private exceptions must not be rendered")

    error = PrivateFailure()

    def forbidden(*args, **kwargs):
        raise error

    manager = smonitor.get_manager()
    handler = MemoryHandler()
    manager.add_handler(handler)
    try:
        with (
            smonitor.diagnostic_scope(safe_extra={"operation": "native-payload"}),
            monkeypatch.context() as patch,
        ):
            patch.setattr(native_feature_payload, "_records", forbidden)
            with pytest.raises(FeatureAssetError) as caught:
                encode()
        assert caught.value.code == "PHMT-E332" and caught.value.__cause__ is error
        assert any(event.get("code") == "PHMT-E332" for event in handler.events)
        assert "analytical detached capture" not in str(handler.events)
        assert "1 nm:α" not in str(handler.events)
    finally:
        manager.remove_handler(handler)


def test_missing_record_capability_never_falls_back(monkeypatch):
    monkeypatch.setattr(puw, "QuantityRecord", None)
    with pytest.raises(FeatureAssetError) as caught:
        encode()
    assert caught.value.code == "PHMT-E312"


def test_admitted_maximum_preserves_every_feature_and_original_extreme_indices():
    native = inventory()
    native["selected_atom_indices"] = [255, 0]
    row = native["features"][0]
    row["atom_indices"] = [255]
    row["geometry_atom_indices"] = [255, 0]
    native["features"] = [deepcopy(row) for _ in range(64)]
    source = parent()
    source["n_atoms"] = 256
    payload = encode(native, ["hydrophobicity"], parent=source)
    result = payload.to_inventory(required_families=["hydrophobicity"])
    assert len(result["features"]) == 64
    assert payload.describe()["coverage"]["hydrophobicity"]["count"] == 64
    assert result["selected_atom_indices"] == [255, 0]
    assert all(row["atom_indices"] == [255] for row in result["features"])


@pytest.mark.parametrize(
    "raw", [b"{}", b"null", b'{"schema":1,"schema":2}', b'{"value":NaN}', b"not JSON"]
)
def test_malformed_bytes_are_catalogued_without_scientific_admission(raw):
    with pytest.raises(FeatureAssetError) as caught:
        FeatureInventoryPayload.from_bytes(raw, payload_profile=PROFILE)
    assert caught.value.code == "PHMT-E330"


def test_first_scientific_activation_preserves_application_unit_authority(tmp_path):
    import pharmacophoremt_features

    path = tmp_path / "native.json"
    path.write_bytes(encode().to_bytes())
    roots = [str(Path(pharmacophoremt_features.__file__).resolve().parent.parent)]
    roots.extend(
        str(Path(importlib.import_module(n).__file__).resolve().parent.parent)
        for n in ["pyunitwizard", "argdigest", "smonitor", "depdigest"]
    )
    code = r"""
import json,sys
from pathlib import Path
sys.path[:0]=json.loads(sys.argv[1])
import pyunitwizard as puw
puw.configure.set_default_form('pint')
puw.configure.set_default_parser('pint')
puw.configure.set_standard_units(['pm','ps','radians'],provenance='application-before-native')
keys=('default_form','default_parser','standard_units','provenance')
before={k:puw.configure.report()[k] for k in keys}
from pharmacophoremt_features import FeatureInventoryPayload
assert 'pharmacophoremt' not in sys.modules
payload=FeatureInventoryPayload.from_bytes(Path(sys.argv[2]).read_bytes(),payload_profile='native-classical-v1')
assert 'pharmacophoremt' not in sys.modules
native=payload.to_inventory(required_families=['hb donor'])
assert {k:puw.configure.report()[k] for k in keys}==before
assert native['structure_index']==5
assert puw.get_value(native['features'][0]['center'],to_unit='pm')[1]==400.
import pharmacophoremt
assert Path(pharmacophoremt.__file__).is_relative_to(Path(sys.argv[1] and json.loads(sys.argv[1])[0]))
print(json.dumps({'first_scientific_activation':True,'application_policy_preserved':True}))
"""
    result = subprocess.run(
        [sys.executable, "-I", "-B", "-c", code, json.dumps(roots), str(path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["application_policy_preserved"]


def test_fresh_payload_inspection_is_scientifically_cold(tmp_path):
    import pharmacophoremt_features

    path = tmp_path / "native.json"
    path.write_bytes(encode().to_bytes())
    roots = [str(Path(pharmacophoremt_features.__file__).resolve().parent.parent)]
    roots.extend(
        str(Path(importlib.import_module(n).__file__).resolve().parent.parent)
        for n in ["argdigest", "smonitor", "depdigest"]
    )
    code = r"""
import importlib.abc,json,sys
from pathlib import Path
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
from pharmacophoremt_features import FeatureInventoryPayload
raw=Path(sys.argv[2]).read_bytes()
payload=FeatureInventoryPayload.from_bytes(raw,payload_profile='native-classical-v1')
report=payload.describe()
assert report['selected_atom_indices']==[8,0,2,4,6]
assert report['structure_index']==5 and report['parent']['source_key']=='nm'
assert not report['quantity_semantics_checked'] and payload.to_bytes()==raw
assert manager.config is policy and not attempts and not(blocked & set(sys.modules))
print(json.dumps({'scientific_imports':0,'policy_preserved':True}))
"""
    result = subprocess.run(
        [sys.executable, "-I", "-S", "-B", "-c", code, json.dumps(roots), str(path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=20,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["scientific_imports"] == 0
