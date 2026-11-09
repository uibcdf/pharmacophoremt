"""Reader-owned option admission and transparent molecular delegation."""

import json
from pathlib import Path

import molsysmt as msm
import numpy as np
import pytest
from argdigest import UnknownArgumentError

from pharmacophoremt import Pharmacophore, io
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere

DATA = Path(__file__).resolve().parents[1] / "pharmacophoremt" / "data"


@pytest.fixture(params=["json", "yaml", "yml", "pml", "pharmer"])
def native_input(request, tmp_path):
    kind = request.param
    if kind == "pharmer":
        # Nineteen original points, ten enabled query constraints.
        return str(DATA / "pharmer.json"), io.from_pharmer, 10
    path = tmp_path / ("model." + kind)
    if kind == "pml":
        path.write_text(
            '<pharmacophore><feature type="H" id="1">'
            '<position x="10" y="20" z="30" tolerance="2"/>'
            "</feature></pharmacophore>"
        )
        return str(path), io.from_ligandscout, 1
    model = Pharmacophore(name="native fixture")
    model.add_interaction_site(
        InteractionSite(Sphere("[1,2,3] nm", ".2 nm"), "hydrophobicity")
    )
    writer, reader = (
        (io.to_json, io.load_json) if kind == "json" else (io.to_yaml, io.load_yaml)
    )
    writer(model, path)
    return str(path), reader, 1


def test_native_facade_preserves_reader_results(native_input):
    path, reader, count = native_input
    direct, dispatched = reader(path), io.load(path)
    assert dispatched.n_interaction_sites == direct.n_interaction_sites == count
    for expected, observed in zip(
        direct.interaction_sites, dispatched.interaction_sites
    ):
        assert observed.features == expected.features
        assert observed.shape_name == expected.shape_name
        np.testing.assert_allclose(
            puw.get_value(observed.center, to_unit="nm"),
            puw.get_value(expected.center, to_unit="nm"),
        )


def test_native_facade_refuses_unknown_options_like_direct_reader(native_input):
    path, reader, _ = native_input
    for tool in (reader, io.load):
        with pytest.raises(TypeError) as caught:
            tool(path, typo_probe_option=True)
        if reader in (io.load_json, io.load_yaml):
            assert isinstance(caught.value, UnknownArgumentError)
            assert caught.value.code == "ARG-ERR-CONTRACT-001"
        else:
            assert "unexpected keyword argument" in str(caught.value)


def test_molecular_options_and_result_are_forwarded_unchanged(monkeypatch):
    result, option = object(), object()
    calls = []

    def convert(*args, **kwargs):
        calls.append((args, kwargs))
        return result

    monkeypatch.setattr(msm, "convert", convert)
    assert io.load("source.sdf", provider_option=option) is result
    assert calls == [
        (("source.sdf",), {"to_form": "molsysmt.MolSys", "provider_option": option})
    ]


def test_molecular_provider_failure_preserves_original_exception(monkeypatch):
    error = RuntimeError("provider failure with original context")

    def convert(*args, **kwargs):
        raise error

    monkeypatch.setattr(msm, "convert", convert)
    with pytest.raises(RuntimeError) as caught:
        io.load("source.sdf", selection="all")
    assert caught.value is error


def test_real_molecular_reader_preserves_coordinates_and_atom_count(tmp_path):
    source = tmp_path / "water.sdf"
    source.write_text(
        "water\n  dispatch fixture\n\n"
        "  1  0  0  0  0  0  0  0  0  0  0 V2000\n"
        "    1.0000    2.0000    3.0000 O   0  0  0  0  0  0  0  0  0  0  0  0\n"
        "M  END\n$$$$\n"
    )
    path = str(source)
    direct = msm.convert(path, to_form="molsysmt.MolSys", selection="all")
    dispatched = io.load(path, selection="all")
    assert msm.get(dispatched, n_atoms=True) == msm.get(direct, n_atoms=True) == 1
    np.testing.assert_allclose(
        puw.get_value(msm.get(dispatched, coordinates=True), to_unit="nm"),
        puw.get_value(msm.get(direct, coordinates=True), to_unit="nm"),
    )


def test_native_parse_failure_is_not_reclassified(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{invalid json")
    with pytest.raises(json.JSONDecodeError):
        io.load(str(path))
