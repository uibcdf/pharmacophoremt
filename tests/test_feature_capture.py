"""Executed request provenance and native/archive composition on prepared sources."""

import importlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt_features import (
    FeatureAssetError,
    FeatureAssetRecord,
    FeatureAssetStore,
    FeatureAssetView,
    FeatureInventoryPayload,
    _schema,
)
from phmt_test_support.feature_snapshot_case import load_parent, projection

PROFILE = "native-classical-v1"
OWNER = importlib.import_module("pharmacophoremt.modeler.features")


def source_parent(key="water"):
    source, original = load_parent(key)
    parent = {
        k: original[k]
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
    return source, parent


def encode(capture, parent):
    return FeatureInventoryPayload.from_capture(
        capture, parent=parent, payload_profile=PROFILE
    )


@pytest.mark.parametrize("unit", ["nm", "pm"])
@pytest.mark.parametrize("key", ["ions", "water", "ring"])
def test_real_default_once_unchanged_inventory_source_and_native_roundtrip(
    monkeypatch, key, unit
):
    source, parent = source_parent(key)
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    atoms = deepcopy(msm.get(source, element="atom", atom_type=True))
    charges = deepcopy(msm.get(source, formal_charge=True))
    with puw.context(standard_units=[unit, "ps", "radians"]):
        expected = OWNER.get_features(source)
    calls = []
    original = OWNER.get_features

    def observed(*args, **kwargs):
        calls.append(kwargs)
        return original(*args, **kwargs)

    monkeypatch.setattr(OWNER, "get_features", observed)
    with puw.context(standard_units=[unit, "ps", "radians"]):
        policy = puw.configure.report()
        capture = phmt.modeler.capture_features(source)
        assert len(calls) == 1
        assert calls[0]["features"] == list(_schema.FAMILIES)
        assert set(capture["inventory"]) == set(expected)
        assert projection(capture["inventory"]) == projection(expected)
        assert capture["inventory"]["recognition"] == expected["recognition"]
        assert capture["evaluation"]["families"] == list(_schema.FAMILIES)
        assert capture["evaluation"]["n_atoms"] == parent["n_atoms"]
        payload = encode(capture, parent)
        assert len(calls) == 1  # encoding cannot re-extract
        restored = payload.to_inventory(required_families=list(_schema.FAMILIES))
        assert projection(restored) == projection(expected)
        assert (
            payload.describe()["extraction_producer"]["producer"] == capture["producer"]
        )
        assert (
            payload.describe()["serialization"]["operation"]
            == "FeatureInventoryPayload.from_inventory"
        )
        assert puw.configure.report() == policy
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), coordinates
    )
    assert msm.get(source, element="atom", atom_type=True) == atoms
    assert msm.get(source, formal_charge=True) == charges
    source_parent(key)  # rechecks original H5 bytes against the source manifest


@pytest.mark.parametrize(
    "features", [["hb donor"], ["hb acceptor", "hb donor", "hb donor"]]
)
def test_effective_subset_duplicates_empty_and_unrequested_not_inferred(features):
    source, parent = source_parent("ions")
    capture = phmt.modeler.capture_features(source, features=features)
    effective = [k for k in _schema.FAMILIES if k in features]
    assert capture["evaluation"]["families"] == effective
    assert capture["evaluation"]["coverage"] == {
        k: {"status": "evaluated_empty", "count": 0} for k in effective
    }
    assert capture["inventory"]["features"] == []
    payload = encode(capture, parent)
    assert payload.describe()["evaluated_families"] == effective
    with pytest.raises(FeatureAssetError) as caught:
        payload.to_inventory(required_families=["positive charge"])
    assert caught.value.code == "PHMT-E334"


@pytest.mark.parametrize("selection,count", [([0, 1, 2], 1), ([0, 2], 0)])
def test_volume_capture_complete_and_classical_payload_explicitly_refuses(
    selection, count
):
    source, parent = source_parent()
    capture = phmt.modeler.capture_features(
        source, selection=selection, features=["included volume"]
    )
    assert capture["evaluation"]["coverage"]["included volume"]["count"] == count
    assert projection(capture["inventory"]) == projection(
        OWNER.get_features(source, selection=selection, features=["included volume"])
    )
    with pytest.raises(FeatureAssetError) as caught:
        encode(capture, parent)
    assert caught.value.code == "PHMT-E331"


@pytest.mark.parametrize("state", [None, 0, "reference", "structure"])
def test_frame_state_order_and_nondefault_units(state):
    source, parent = source_parent()
    second = puw.get_value(msm.get(source, coordinates=True), to_unit="nm")[0].copy()
    second[0] = [0, 0, 0.2]
    source.structures.append(coordinates=puw.quantity([second], "nm"))
    kwargs = dict(
        selection=[2, 1, 0],
        structure_index=np.int64(1),
        chemical_state=state,
        features=["hb donor"],
    )
    with puw.context(standard_units=["pm", "ps", "radians"]):
        capture = phmt.modeler.capture_features(source, **kwargs)
        expected = OWNER.get_features(source, **kwargs)
        assert projection(capture["inventory"]) == projection(expected)
        assert (
            capture["evaluation"]["selected_atom_indices"]
            == expected["selected_atom_indices"]
        )
        assert capture["evaluation"]["structure_index"] == 1
        assert capture["evaluation"]["chemical_state"] == state
        assert projection(
            encode(capture, parent).to_inventory(required_families=["hb donor"])
        ) == projection(expected)


@pytest.mark.parametrize(
    "part",
    [
        "inventory",
        "coverage",
        "families",
        "producer",
        "digest",
        "status",
        "parent",
        "frame",
        "selected",
        "extra",
    ],
)
def test_edits_and_false_completed_provenance_are_refused(part):
    source, parent = source_parent()
    capture = phmt.modeler.capture_features(source, features=["hb donor"])
    if part == "inventory":
        capture["inventory"]["recognition"]["edited"] = True
    elif part == "coverage":
        capture["evaluation"]["coverage"]["hb donor"]["count"] = 0
    elif part == "families":
        capture["evaluation"]["families"].append("hb acceptor")
    elif part == "producer":
        capture["producer"]["runtime_version"] = "fabricated"
    elif part == "digest":
        capture["capture_sha256"] = "0" * 64
    elif part == "status":
        capture["evaluation"]["status"] = "failed"
    elif part == "parent":
        parent["n_atoms"] += 1
    elif part == "frame":
        capture["evaluation"]["structure_index"] = 1
    elif part == "selected":
        capture["evaluation"]["selected_atom_indices"].reverse()
    else:
        capture["extra"] = None
    with pytest.raises(FeatureAssetError) as caught:
        encode(capture, parent)
    assert caught.value.code == "PHMT-E339"


@pytest.mark.parametrize(
    "field,value,code",
    [
        ("center", "1 ps", "332"),
        ("direction", [0, 0, 0], "332"),
        ("atom_indices", [99], "330"),
    ],
)
def test_native_fields_revalidated_without_a_success_passport(field, value, code):
    source, parent = source_parent()
    capture = phmt.modeler.capture_features(source, features=["hb donor"])
    capture["inventory"]["features"][0][field] = (
        puw.quantity(value)
        if field == "center"
        else puw.quantity(value, "dimensionless")
        if field == "direction"
        else value
    )
    with pytest.raises(FeatureAssetError) as caught:
        encode(capture, parent)
    assert caught.value.code == "PHMT-E" + code


def test_provider_failure_is_original_and_invalid_request_never_extracts(monkeypatch):
    source, _ = source_parent()
    failure = RuntimeError("controlled molecular extraction failure")
    calls = []

    def failed(*args, **kwargs):
        calls.append(kwargs)
        raise failure

    monkeypatch.setattr(OWNER, "get_features", failed)
    with pytest.raises(RuntimeError) as caught:
        phmt.modeler.capture_features(source, features=["hb donor"])
    assert caught.value is failure and len(calls) == 1
    with pytest.raises(ArgumentError):
        phmt.modeler.capture_features(source, features=["unknown"])
    assert len(calls) == 1


def test_source_budget_refused_before_extraction(monkeypatch):
    owner = importlib.import_module("pharmacophoremt.modeler.feature_capture")
    monkeypatch.setattr(owner, "capability", lambda name: lambda *a, **k: 257)
    monkeypatch.setattr(
        OWNER, "get_features", lambda *a, **k: pytest.fail("oversized input extracted")
    )
    with pytest.raises(FeatureAssetError) as caught:
        phmt.modeler.capture_features(object())
    assert caught.value.code == "PHMT-E333"


@pytest.mark.parametrize("mode", ["features", "metadata"])
def test_oversized_extraction_output_never_returns_partial_capture(monkeypatch, mode):
    source, _ = source_parent()
    original = OWNER.get_features

    def oversized(*args, **kwargs):
        result = original(*args, **kwargs)
        if mode == "features":
            result["features"] = [result["features"][0]] * 65
        else:
            result["recognition"]["excessive"] = "x" * (128 * 1024)
        return result

    monkeypatch.setattr(OWNER, "get_features", oversized)
    with pytest.raises(FeatureAssetError) as caught:
        phmt.modeler.capture_features(source, features=["hb donor"])
    assert caught.value.code == "PHMT-E333"


@pytest.mark.parametrize(
    "argument,value", [("capture", None), ("parent", []), ("payload_profile", "auto")]
)
def test_capture_encoding_closed_argument_contract(argument, value):
    source, parent = source_parent()
    kwargs = dict(
        capture=phmt.modeler.capture_features(source),
        parent=parent,
        payload_profile=PROFILE,
    )
    kwargs[argument] = value
    with pytest.raises(FeatureAssetError) as caught:
        FeatureInventoryPayload.from_capture(**kwargs)
    assert caught.value.code == "PHMT-E301"
    assert caught.value.extra["argument"] == argument


@pytest.mark.parametrize("flag", [1, None, "true"])
def test_new_bypass_control_requires_literal_boolean(flag):
    source, parent = source_parent()
    with pytest.raises(ArgumentError):
        phmt.modeler.capture_features(source, skip_digestion=flag)
    capture = phmt.modeler.capture_features(source)
    with pytest.raises(FeatureAssetError) as caught:
        FeatureInventoryPayload.from_capture(
            capture, parent=parent, payload_profile=PROFILE, skip_digestion=flag
        )
    assert caught.value.code == "PHMT-E301"


def test_internal_bypass_never_skips_native_or_capture_validation():
    source, parent = source_parent()
    capture = phmt.modeler.capture_features(
        source, features=["hb donor"], skip_digestion=True
    )
    assert encode(capture, parent).to_inventory(required_families=["hb donor"])[
        "features"
    ]
    capture["capture_sha256"] = "0" * 64
    with pytest.raises(FeatureAssetError) as caught:
        FeatureInventoryPayload.from_capture(
            capture, parent=parent, payload_profile=PROFILE, skip_digestion=True
        )
    assert caught.value.code == "PHMT-E339"


def test_fresh_real_optional_absence_retains_original_offline_credit(tmp_path):
    from phmt_test_support.feature_snapshot_case import DIRECTORY, parent_manifest

    _, parent = source_parent()
    path = DIRECTORY / next(
        r["file"] for r in parent_manifest()["parents"] if r["key"] == "water"
    )
    roots = [str(Path(phmt.__file__).resolve().parent.parent)]
    roots.extend(
        str(Path(importlib.import_module(n).__file__).resolve().parent.parent)
        for n in ["pyunitwizard", "argdigest", "smonitor", "depdigest"]
    )
    code = r"""
import importlib.abc,json,sys
sys.path[:0]=json.loads(sys.argv[1])
class NoAckredit(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0]=='ackredit':
            raise ModuleNotFoundError('controlled absence',name=fullname)
sys.meta_path.insert(0,NoAckredit())
import molsysmt as msm
import pharmacophoremt as phmt
from pharmacophoremt_features import FeatureInventoryPayload
source=msm.h5msm.read(sys.argv[2])
with phmt.attribution():
    capture=phmt.modeler.capture_features(source,features=['hb donor'])
original=capture['inventory']['attribution']
assert original['status']=='unavailable' and original['host_references']
payload=FeatureInventoryPayload.from_capture(capture,parent=json.loads(sys.argv[3]),payload_profile='native-classical-v1')
assert payload.to_inventory(required_families=['hb donor'])['attribution']==original
assert 'ackredit' not in sys.modules
"""
    result = subprocess.run(
        [
            sys.executable,
            "-I",
            "-B",
            "-c",
            code,
            json.dumps(roots),
            str(path),
            json.dumps(parent),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=25,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_capture_to_published_archive_reuse_preserves_original_and_no_new_credit(
    tmp_path, monkeypatch
):
    import ackredit as ack

    source, parent = source_parent()
    with ack.session("capture application") as application:
        with ack.capture("enclosing") as enclosing:
            with phmt.attribution():
                first = phmt.modeler.capture_features(source, features=["hb donor"])
                second = phmt.modeler.capture_features(source, features=["hb donor"])
        assert ack.current_session() is application
        one, two = (r["inventory"]["attribution"] for r in (first, second))
        assert one["status"] == two["status"] == "captured"
        assert one["references"]["items"] == two["references"]["items"]
        assert {r["id"] for r in one["references"]["items"]} <= {
            r["id"] for r in enclosing.attribution.to_dict()["items"]
        }
        monkeypatch.setattr(
            OWNER,
            "get_features",
            lambda *a, **k: pytest.fail("persisting re-extracted"),
        )
        with ack.capture("persistence") as persistence:
            payload = encode(first, parent)
            record = FeatureAssetRecord.from_payload("water:0", payload)
            with FeatureAssetStore.create(
                tmp_path / "store", payload_profile=PROFILE
            ) as store:
                generation = store.stage_records([record])
                store.publish(generation, expected_current=None)
            with FeatureAssetView.open(tmp_path / "store") as view:
                result = phmt.screening.reuse_feature_inventories(
                    view,
                    ["hb donor"],
                    expected_generation=view.generation,
                    payload_profile=PROFILE,
                )
        assert not persistence.attribution.to_dict()["uses"]
        restored = result["inventories"][0]
        assert restored["inventory"]["attribution"] == one
        assert (
            restored["extraction"]["extraction_producer"]["evaluation"]
            == first["evaluation"]
        )
        assert restored["lineage"] == []
        assert projection(restored["inventory"]) == projection(first["inventory"])
        assert ack.current_session() is application
