"""Legacy call compatibility required before native I/O ArgDigest receiving.

Provider spies verify raw option routing only; they provide no chemical answers.
The failing candidate/provider reproductions remain separate readiness evidence.
"""

import os
from pathlib import Path

import molsysmt as msm
import pytest

from pharmacophoremt import io
from pharmacophoremt import pyunitwizard as puw
from tests.test_io_sdf import model

TOOLS = [io.load_json, io.load_yaml, io.to_json, io.to_yaml]


class ForbiddenModelAccess:
    def __getattribute__(self, name):
        raise AssertionError("Unknown keywords must fail before model access")


@pytest.mark.parametrize("tool", TOOLS, ids=lambda tool: tool.__name__)
@pytest.mark.parametrize(
    "options",
    [
        {"typo": True},
        {"skip_digestion": False},
        {"skip_digestion": True},
        {"skip_digestion": "true"},
    ],
)
def test_closed_native_calls_keep_typeerror_before_file_or_model_work(
    tool, options, tmp_path
):
    path = tmp_path / "absent"
    args = (
        (path,) if tool.__name__.startswith("load") else (ForbiddenModelAccess(), path)
    )
    with pytest.raises(TypeError):
        tool(*args, **options)
    assert not path.exists()


@pytest.mark.parametrize("tool", TOOLS, ids=lambda tool: tool.__name__)
def test_missing_and_duplicate_native_arguments_keep_typeerror(tool, tmp_path):
    with pytest.raises(TypeError):
        tool()
    args = (
        (tmp_path / "absent",)
        if tool.__name__.startswith("load")
        else (ForbiddenModelAccess(), tmp_path / "absent")
    )
    with pytest.raises(TypeError):
        tool(*args, file_name=tmp_path / "second")


class CustomPath(os.PathLike):
    def __init__(self, path):
        self.path = path

    def __fspath__(self):
        return str(self.path)


@pytest.mark.parametrize("codec", ["json", "yaml"])
@pytest.mark.parametrize("path_kind", ["str", "Path", "pathlike", "bytes"])
def test_native_open_path_forms_keep_roundtrip_and_application_policy(
    codec, path_kind, tmp_path
):
    writer, reader = (
        (io.to_json, io.load_json) if codec == "json" else (io.to_yaml, io.load_yaml)
    )
    path = tmp_path / ("query." + codec)
    supplied = {
        "str": str(path),
        "Path": path,
        "pathlike": CustomPath(path),
        "bytes": os.fsencode(path),
    }[path_kind]
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        query = model()
        before = puw.configure.report()
        assert writer(query, supplied) is None
        restored = reader(supplied)
        assert restored.metadata == query.metadata
        assert (
            restored.interaction_sites[0].features
            == query.interaction_sites[0].features
        )
        assert puw.configure.report() == before
        assert Path(path).is_file()


def close_if_open(fd):
    try:
        os.close(fd)
    except OSError:
        pass  # These descriptors are owned here; native open normally closes them.


@pytest.mark.parametrize("codec", ["json", "yaml"])
def test_direct_native_open_file_descriptors_keep_existing_behavior(codec, tmp_path):
    writer, reader = (
        (io.to_json, io.load_json) if codec == "json" else (io.to_yaml, io.load_yaml)
    )
    path = tmp_path / ("descriptor." + codec)
    query = model()
    fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC, 0o600)
    try:
        assert writer(query, fd) is None
    finally:
        close_if_open(fd)
    fd = os.open(path, os.O_RDONLY)
    try:
        restored = reader(fd)
    finally:
        close_if_open(fd)
    assert restored.metadata == query.metadata
    assert restored.n_interaction_sites == query.n_interaction_sites


@pytest.mark.parametrize(
    "case",
    [
        "opaque",
        "mapping",
        "source_name",
        "empty",
        "collision",
        "skip_false",
        "skip_true",
    ],
)
def test_molecular_facade_keeps_literal_kwargs_and_option_value_identity(
    case, monkeypatch
):
    marker, other, result = object(), object(), object()
    supplied = {
        "opaque": {"kwargs": marker},
        "mapping": {"kwargs": {"selection": marker}},
        "source_name": {"kwargs": {"file_name": "replacement.sdf"}},
        "empty": {"kwargs": {}},
        "collision": {"selection": marker, "kwargs": {"selection": other}},
        "skip_false": {"skip_digestion": False, "kwargs": marker},
        "skip_true": {"skip_digestion": True, "kwargs": marker},
    }[case]
    calls = []

    def convert(*args, **options):
        calls.append((args, options))
        return result

    monkeypatch.setattr(msm, "convert", convert)
    assert io.load("original.sdf", **supplied) is result
    assert len(calls) == 1 and calls[0][0] == ("original.sdf",)
    assert calls[0][1]["to_form"] == "molsysmt.MolSys"
    assert set(calls[0][1]) == {"to_form", *supplied}
    for name, value in supplied.items():
        assert calls[0][1][name] is value


@pytest.mark.parametrize("path", [Path("original.sdf"), b"original.sdf", None, 1])
def test_dispatcher_string_only_refusal_stays_coded_and_does_not_enter_provider(
    path, monkeypatch
):
    def forbidden(*args, **kwargs):
        raise AssertionError("Invalid dispatcher path must not enter MolSysMT")

    monkeypatch.setattr(msm, "convert", forbidden)
    with pytest.raises(TypeError) as caught:
        io.load(path)
    assert caught.value.code == "PHMT-E109"
