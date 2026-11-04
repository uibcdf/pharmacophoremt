"""Native pharmacophore refusals carry codes without reclassifying providers."""

import json
import subprocess
import sys

import pytest
import yaml

from pharmacophoremt import io
from tests.test_native_schema_writing import record


@pytest.fixture(params=["json", "yaml"])
def native(request, tmp_path):
    codec = request.param
    return (
        tmp_path / ("query." + codec),
        io.load_json if codec == "json" else io.load_yaml,
        io.to_json if codec == "json" else io.to_yaml,
        json.dumps if codec == "json" else yaml.safe_dump,
    )


@pytest.mark.parametrize(
    "change,field",
    [
        ("mapping", "record"),
        ("schema", "schema"),
        ("model_fields", "model"),
        ("site_fields", "site"),
        ("shape_fields", "shape"),
        ("version", "version"),
        ("site_list", "interaction_sites"),
        ("shape_record", "shape"),
        ("shape_type", "shape"),
        ("software", "software"),
        ("units", "units"),
    ],
)
def test_owned_native_refusals_keep_valueerror_and_structured_context(
    native, change, field
):
    path, reader, _, encode = native
    data = record()
    if change == "mapping":
        data = []
    elif change == "schema":
        data["schema"] = "pharmacophoremt.native@999"
    elif change == "model_fields":
        data.pop("metadata")
    elif change == "site_fields":
        data["interaction_sites"][0].pop("essential")
    elif change == "shape_fields":
        data["interaction_sites"][0]["shape"]["unrecognized"] = True
    elif change == "version":
        data["version"] = 1
    elif change == "site_list":
        data["interaction_sites"] = {}
    elif change == "shape_record":
        data["interaction_sites"][0]["shape"] = 1
    elif change == "shape_type":
        data["interaction_sites"][0]["shape"]["type"] = "unrecognized"
    elif change == "software":
        data["software"] = "foreign"
    else:
        data["units"]["length"] = "angstrom"
    path.write_text(encode(data))
    with pytest.raises(ValueError) as caught:
        reader(path)
    error = caught.value
    assert getattr(error, "code", None) == "PHMT-E108"
    assert type(error).__name__ == "NativeFormatError"
    assert error.extra["field"] == field
    assert error.extra["reason"] and str(error)
    assert type(error)(*error.args).args == error.args


def test_native_json_facade_keeps_the_direct_native_diagnostic(tmp_path):
    data = record()
    data["schema"] = "pharmacophoremt.native@999"
    path = tmp_path / "query.json"
    path.write_text(json.dumps(data))
    errors = []
    for reader in [io.load_json, io.load]:
        with pytest.raises(ValueError) as caught:
            reader(str(path))
        assert getattr(caught.value, "code", None) == "PHMT-E108"
        errors.append(caught.value)
    assert type(errors[0]) is type(errors[1])
    assert errors[0].extra == errors[1].extra


@pytest.mark.parametrize("value", [42, None, b"query.json"])
def test_dispatch_file_argument_keeps_typeerror_and_typed_context(value):
    with pytest.raises(TypeError) as caught:
        io.load(value)
    error = caught.value
    assert getattr(error, "code", None) == "PHMT-E109"
    assert type(error).__name__ == "ArgumentTypeError"
    assert error.extra["argument"] == "file_name"
    assert error.extra["actual_type"] == type(value).__name__
    assert error.extra["expected_type"] == "a string path"
    assert type(error)(*error.args).args == error.args


def test_nonfinite_native_record_keeps_original_encoder_cause(native):
    path, reader, _, encode = native
    data = record()
    data["metadata"]["nonfinite"] = float("nan")
    path.write_text(encode(data))
    with pytest.raises(ValueError) as caught:
        reader(path)
    assert getattr(caught.value, "code", None) == "PHMT-E108"
    assert caught.value.extra["field"] == "record"
    assert isinstance(caught.value.__cause__, ValueError)
    assert "JSON" in str(caught.value.__cause__)


@pytest.mark.parametrize("existing", [False, True])
def test_coded_nonfinite_writer_refusal_preserves_destination(native, existing):
    from tests.test_io_sdf import model

    path, _, writer, _ = native
    query = model()
    query.metadata["nonfinite"] = float("nan")
    previous = b"previous contents\n"
    if existing:
        path.write_bytes(previous)
    with pytest.raises(ValueError) as caught:
        writer(query, path)
    assert getattr(caught.value, "code", None) == "PHMT-E108"
    assert path.read_bytes() == previous if existing else not path.exists()


def test_native_parser_exceptions_keep_their_original_identity(native, monkeypatch):
    path, reader, _, _ = native
    path.write_text("{}")
    if reader is io.load_json:
        error = json.JSONDecodeError("controlled parse failure", "{", 1)
        module, name = json, "load"
    else:
        error = yaml.YAMLError("controlled parse failure")
        module, name = yaml, "safe_load"

    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(module, name, fail)
    with pytest.raises(type(error)) as caught:
        reader(path)
    assert caught.value is error
    assert not hasattr(error, "code")


def test_native_filesystem_errors_remain_standard_io_errors(native):
    path, reader, writer, _ = native
    with pytest.raises(FileNotFoundError) as caught:
        reader(path)
    assert caught.value.filename == str(path)
    assert not hasattr(caught.value, "code")
    path.mkdir()
    from tests.test_io_sdf import model

    with pytest.raises(IsADirectoryError) as caught:
        writer(model(), path)
    assert caught.value.filename == str(path)
    assert not hasattr(caught.value, "code")


def test_existing_scientific_value_validator_keeps_its_argument_code(native):
    path, reader, _, encode = native
    data = record()
    data["interaction_sites"][0]["weight"] = -1
    path.write_text(encode(data))
    with pytest.raises(ValueError) as caught:
        reader(path)
    assert caught.value.code == "PHMT-E102"
    assert type(caught.value).__name__ == "ArgumentError"


@pytest.mark.parametrize("exception_type", [TypeError, RuntimeError])
def test_unrelated_encoder_failures_are_not_reclassified(
    native, monkeypatch, exception_type
):
    path, reader, _, encode = native
    path.write_text(encode(record()))
    error = exception_type("controlled encoder failure")

    def fail(*args, **kwargs):
        raise error

    monkeypatch.setattr(json, "dumps", fail)
    with pytest.raises(exception_type) as caught:
        reader(path)
    assert caught.value is error
    assert not hasattr(error, "code")


def test_new_catalog_errors_render_and_rebuild_in_each_profile():
    script = """
import smonitor
import pharmacophoremt._private.smonitor.exceptions as errors
from pharmacophoremt._smonitor import PROFILES
from pharmacophoremt._private.smonitor.catalog import CODES, META
for profile in PROFILES:
    smonitor.configure(profile=profile, handlers=[])
    for name, code, extra in [
        ('NativeFormatError','PHMT-E108',dict(field='schema',reason='unsupported schema')),
        ('ArgumentTypeError','PHMT-E109',dict(argument='file_name',expected_type='a string path',actual_type='int')),
    ]:
        error = getattr(errors,name)(extra=extra)
        assert error.code == code and CODES[code]['message']
        assert str(error) and '{' not in str(error)
        assert all(error.extra[key] == value for key, value in extra.items())
        assert all(error.extra[key] == value for key, value in META.items())
        assert type(error)(*error.args).args == error.args
print('Both new catalogue errors render and rebuild in all five profiles.')
"""
    result = subprocess.run(
        [sys.executable, "-B", "-c", script], capture_output=True, text=True, timeout=90
    )
    assert result.returncode == 0, result.stdout + result.stderr
