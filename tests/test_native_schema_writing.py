"""Native schema admission and destination preservation before encoding completes."""

import copy
import json

import pytest
import yaml

from pharmacophoremt import io
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.io.phmt import _to_dict
from tests.test_io_sdf import model
from tests.test_native_persistence_validation import SHAPES

SCHEMA = "pharmacophoremt.native@1"


@pytest.fixture(params=["json", "yaml"])
def native(request, tmp_path):
    path = tmp_path / ("query." + request.param)
    if request.param == "json":
        return path, io.to_json, io.load_json, json.dumps, json.loads
    return path, io.to_yaml, io.load_yaml, yaml.safe_dump, yaml.safe_load


def record():
    return {"schema": SCHEMA, **_to_dict(model())}


@pytest.mark.parametrize("level", ["model", "site", "shape"])
@pytest.mark.parametrize("change", ["unknown", "missing"])
def test_tagged_records_refuse_unrecognized_or_missing_fields(native, level, change):
    path, _, reader, encode, _ = native
    data = record()
    target = data if level == "model" else data["interaction_sites"][0]
    if level == "shape":
        target = target["shape"]
    if change == "unknown":
        target["unrecognized_constraint"] = True
    else:
        target.pop({"model": "metadata", "site": "essential", "shape": "radius"}[level])
    path.write_text(encode(data))
    with pytest.raises(ValueError, match="fields"):
        reader(path)


@pytest.mark.parametrize("schema", ["pharmacophoremt.native@2", "foreign@1", None, 1])
def test_explicit_unknown_schema_is_never_treated_as_legacy(native, schema):
    path, _, reader, encode, _ = native
    data = record()
    data["schema"] = schema
    path.write_text(encode(data))
    with pytest.raises(ValueError, match="schema"):
        reader(path)


@pytest.mark.parametrize("kind", SHAPES)
def test_new_export_tags_schema_and_remains_readable(native, kind):
    path, writer, reader, _, decode = native
    original = model(SHAPES[kind]())
    expected = copy.deepcopy(_to_dict(original))
    assert writer(original, path) is None
    data = decode(path.read_text())
    assert data.pop("schema") == SCHEMA
    assert data == expected
    restored = reader(path)
    assert restored.interaction_sites[0].shape_name == kind
    assert restored.interaction_sites[0].essential is False
    assert restored.interaction_sites[0].weight == 2.5
    assert _to_dict(original) == expected


def test_package_version_and_metadata_schema_are_not_admission_keys(native):
    path, _, reader, encode, _ = native
    data = record()
    data["version"] = "9000.0.0+future-producer"
    metadata = {"schema": "arbitrary@99", "unrecognized_constraint": ["1 nm", "nm"]}
    data["metadata"].update(metadata)
    path.write_text(encode(data))
    assert reader(path).metadata == data["metadata"]


@pytest.mark.parametrize("existing", [False, True])
@pytest.mark.parametrize("bad", ["opaque", "nan", "weight", "radius"])
def test_invalid_export_leaves_destination_unchanged(native, existing, bad):
    path, writer, _, _, _ = native
    original = model()
    if bad == "opaque":
        original.metadata["opaque"] = object()
    elif bad == "nan":
        original.metadata["nonfinite"] = float("nan")
    elif bad == "weight":
        original.interaction_sites[0].weight = -1
    else:
        from pharmacophoremt import pyunitwizard as puw

        original.interaction_sites[0].shape.radius = puw.quantity(-1, "nm")
    previous = b"Previous data must survive\n"
    if existing:
        path.write_bytes(previous)
    with pytest.raises((ArgumentError, TypeError, ValueError, yaml.YAMLError)):
        writer(original, path)
    assert path.read_bytes() == previous if existing else not path.exists()


def test_successful_export_can_replace_existing_native_file(native):
    path, writer, reader, _, _ = native
    path.write_text("previous content")
    assert writer(model(), path) is None
    assert reader(path).n_interaction_sites == 1


@pytest.mark.parametrize("value", [float("nan"), float("inf")])
def test_tagged_nonfinite_metadata_is_refused(native, value):
    path, _, reader, encode, _ = native
    data = record()
    data["metadata"]["value"] = value
    path.write_text(encode(data))
    with pytest.raises(ValueError):
        reader(path)


def test_untagged_extra_fields_keep_legacy_compatibility(native):
    path, _, reader, encode, _ = native
    data = record()
    data.pop("schema")
    data["historical_extra"] = True
    data["interaction_sites"][0].pop("essential")
    path.write_text(encode(data))
    restored = reader(path)
    assert restored.n_interaction_sites == 1
    assert restored.interaction_sites[0].essential is True
