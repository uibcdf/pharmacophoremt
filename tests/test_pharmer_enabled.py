"""Public disabled-point admission and original-query identity controls for #162."""

import json
from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest

from pharmacophoremt import Pharmacophore, io
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentTypeError

DATA = Path(__file__).resolve().parents[1] / "pharmacophoremt/data/pharmer.json"


def query():
    return {
        "points": [
            dict(name="PositiveIon", x=0, y=0, z=0, radius=0.3125, enabled=True),
            dict(name="PositiveIon", x=5, y=0, z=0, radius=0.3125, enabled=True),
            dict(name="PositiveIon", x=0, y=10, z=0, radius=0.3125, enabled=True),
        ]
    }


def test_disabled_point_is_omitted_with_original_point_mapping():
    raw = query()
    raw["points"][0]["enabled"] = False
    before = deepcopy(raw)
    result = io.from_pharmer(raw)
    assert result.n_interaction_sites == 2
    assert result.metadata["pharmer"] == {
        "source_point_indices": [1, 2],
        "disabled_point_indices": [0],
    }
    np.testing.assert_allclose(
        puw.get_value(result.get(get_center=True), to_unit="nm"),
        [[0.5, 0, 0], [0, 1, 0]],
        rtol=0,
        atol=1e-15,
    )
    assert all(site.essential and site.weight == 1 for site in result.interaction_sites)
    assert raw == before


@pytest.mark.parametrize("route", ["reader", "facade", "constructor"])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_file_routes_preserve_survivor_order_and_unit_meaning(route, unit, tmp_path):
    raw = query()
    raw["points"][1]["enabled"] = False
    del raw["points"][2]["enabled"]
    path = tmp_path / "query.json"
    path.write_text(json.dumps(raw))
    original = path.read_bytes()
    with puw.context(standard_units=[unit, "ps", "radians"]):
        if route == "reader":
            result = io.from_pharmer(str(path))
        elif route == "facade":
            result = io.load(str(path))
        else:
            result = Pharmacophore(str(path), form="pharmer")
        assert result.n_interaction_sites == 2
        assert result.metadata["pharmer"]["source_point_indices"] == [0, 2]
        np.testing.assert_allclose(
            puw.get_value(result.get(get_center=True), to_unit="nm"),
            [[0, 0, 0], [0, 1, 0]],
            rtol=0,
            atol=1e-15,
        )
        np.testing.assert_allclose(
            puw.get_value(result.get(get_radius=True), to_unit="nm"),
            [0.03125, 0.03125],
            rtol=0,
            atol=1e-15,
        )
    assert path.read_bytes() == original


@pytest.mark.parametrize("flag", ["missing", "true"])
def test_ordinary_enabled_points_keep_geometry_defaults_and_metadata(flag):
    raw = query()
    if flag == "missing":
        for point in raw["points"]:
            del point["enabled"]
    before = deepcopy(raw)
    result = io.from_pharmer(raw)
    assert result.n_interaction_sites == 3 and result.metadata == {}
    np.testing.assert_allclose(
        puw.get_value(result.get(get_center=True), to_unit="nm"),
        [[0, 0, 0], [0.5, 0, 0], [0, 1, 0]],
        rtol=0,
        atol=1e-15,
    )
    assert raw == before


@pytest.mark.parametrize(
    "point", [{"enabled": False}, {"enabled": False, "name": "unknown"}]
)
def test_disabled_record_is_omitted_before_feature_or_geometry_parsing(point):
    raw = {"points": [point, query()["points"][1]]}
    before = deepcopy(raw)
    result = io.from_pharmer(raw)
    assert result.n_interaction_sites == 1
    assert result.metadata["pharmer"]["source_point_indices"] == [1]
    assert raw == before


def test_all_disabled_points_return_a_declared_empty_model():
    raw = query()
    for point in raw["points"]:
        point["enabled"] = False
    result = io.from_pharmer(raw)
    assert result.n_interaction_sites == 0
    assert result.metadata["pharmer"] == {
        "source_point_indices": [],
        "disabled_point_indices": [0, 1, 2],
    }


@pytest.mark.parametrize("value", [0, 1, None, "false", [], {}])
def test_nonboolean_enabled_value_is_refused_with_catalog_context(value):
    raw = query()
    raw["points"][1]["enabled"] = value
    before = deepcopy(raw)
    with pytest.raises(ArgumentTypeError) as caught:
        io.from_pharmer(raw)
    assert caught.value.code == "PHMT-E109"
    assert "points[1].enabled" in str(caught.value)
    assert raw == before


def test_filtered_mapping_survives_public_native_persistence(tmp_path):
    raw = query()
    raw["points"][0]["enabled"] = False
    model = io.from_pharmer(raw)
    path = tmp_path / "native.json"
    io.to_json(model, path)
    loaded = io.load(str(path))
    assert loaded.n_interaction_sites == 2
    assert loaded.metadata == model.metadata
    assert loaded.metadata["pharmer"]["source_point_indices"] == [1, 2]


def test_disabled_point_no_longer_vetoes_actual_public_evaluation():
    from pharmacophoremt.screening import PoseEvaluator
    from phmt_test_support.absence_inputs import system

    raw = query()
    raw["points"][0]["enabled"] = False
    model = io.from_pharmer(raw)
    source = system("[Na+].[K+]", [[0.5, 0, 0], [0, 1, 0]])
    result = PoseEvaluator(model).evaluate(source)
    assert result["status"] == "matched" and result["fit_value"] == 1
    assert result["missing_essential_sites"] == []


def test_attached_ligand_still_uses_the_public_molecular_provider():
    import molsysmt as msm

    raw = query()
    raw["points"][0]["enabled"] = False
    raw["ligand"] = "smiles:[Na+]"
    before = deepcopy(raw)
    result = io.from_pharmer(raw)
    assert result.n_interaction_sites == 2
    assert msm.get(result.molecular_system, n_atoms=True) == 1
    assert raw == before


def test_original_bundled_flags_define_ten_retained_sites():
    raw = json.loads(DATA.read_text())
    assert [row["enabled"] for row in raw["points"]] == [True] * 10 + [False] * 9
    # Isolate query interpretation. The original unlabelled attached-ligand
    # form-discovery operation has its separate full-source admission gate.
    points = {"points": deepcopy(raw["points"])}
    before = deepcopy(points)
    model = io.from_pharmer(points)
    assert model.n_interaction_sites == 10
    assert model.metadata["pharmer"] == {
        "source_point_indices": list(range(10)),
        "disabled_point_indices": list(range(10, 19)),
    }
    np.testing.assert_allclose(
        puw.get_value(model.get(get_center=True), to_unit="angstrom"),
        [[row[k] for k in ("x", "y", "z")] for row in raw["points"][:10]],
        rtol=0,
        atol=1e-12,
    )
    assert points == before
