"""External native files must reuse public pharmacophore value validation."""

import copy
import json

import numpy as np
import pytest
import yaml

from pharmacophoremt import Pharmacophore, io
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import (
    Cylinder,
    Disk,
    GaussianKernel,
    Point,
    Sphere,
    SphereAndVector,
)
from pharmacophoremt.io.phmt import _to_dict

SHAPES = {
    "point": lambda: Point("[1,2,3] nm"),
    "sphere": lambda: Sphere("[1,2,3] nm", ".2 nm"),
    "sphere and vector": lambda: SphereAndVector("[1,2,3] nm", ".2 nm", [1, 0, 0]),
    "disk": lambda: Disk("[1,2,3] nm", [0, 1, 0], ".2 nm"),
    "gaussian kernel": lambda: GaussianKernel("[1,2,3] nm", ".2 nm"),
    "cylinder": lambda: Cylinder("[1,2,3] nm", "[2,3,4] nm", ".2 nm"),
}


def payload(kind="sphere"):
    model = Pharmacophore(
        name="1 nm", description="literal α", score=0.25, ref_mol=2, ref_struct=3
    )
    model.metadata = {"source": ["id", "1 ps"], "distance": puw.quantity(0.04, "nm")}
    model.add_interaction_site(
        InteractionSite(
            SHAPES[kind](),
            "hydrophobicity",
            weight=0,
            essential=False,
            metadata={"indices": [2, 4]},
        )
    )
    return _to_dict(model)


@pytest.fixture(params=["json", "yaml"])
def native(request, tmp_path):
    kind = request.param
    path = tmp_path / ("native." + kind)

    def read(data):
        path.write_text(json.dumps(data) if kind == "json" else yaml.safe_dump(data))
        return (io.load_json if kind == "json" else io.load_yaml)(path)

    return read


@pytest.mark.parametrize(
    "field,value",
    [
        ("weight", -1),
        ("weight", True),
        ("weight", float("nan")),
        ("essential", "false"),
        ("essential", 1),
        ("features", []),
        ("features", ["invented"]),
        ("metadata", [1]),
    ],
)
def test_invalid_site_values_are_refused(native, field, value):
    data = payload()
    data["interaction_sites"][0][field] = value
    with pytest.raises(ArgumentError):
        native(data)


@pytest.mark.parametrize(
    "kind,field,value",
    [
        ("sphere", "radius", -0.1),
        ("sphere", "radius", float("inf")),
        ("sphere", "center", [1, 2]),
        ("point", "position", [float("nan"), 0, 0]),
        ("sphere and vector", "direction", [0, 0, 0]),
        ("disk", "normal", [1, 2]),
        ("gaussian kernel", "sigma", 0),
        ("cylinder", "end", [1, 2]),
    ],
)
def test_invalid_shape_values_are_refused(native, kind, field, value):
    data = payload(kind)
    data["interaction_sites"][0]["shape"][field] = value
    with pytest.raises(ArgumentError):
        native(data)


def test_invalid_model_metadata_is_refused(native):
    data = payload()
    data["metadata"] = ["not a mapping"]
    with pytest.raises(ArgumentError):
        native(data)


@pytest.mark.parametrize("kind", SHAPES)
def test_supported_fields_survive_read_and_write_across_unit_contexts(native, kind):
    data = payload(kind)
    before = copy.deepcopy(data)
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        restored = native(data)
        saved = _to_dict(restored)
        assert restored.molecular_system is None
    assert data == before
    expected = copy.deepcopy(data)
    observed_shape = saved["interaction_sites"][0].pop("shape")
    expected_shape = expected["interaction_sites"][0].pop("shape")
    assert saved == expected
    assert observed_shape["type"] == expected_shape["type"]
    for field in set(expected_shape) - {"type"}:
        np.testing.assert_allclose(
            observed_shape[field], expected_shape[field], rtol=1e-13, atol=1e-14
        )
    saved["interaction_sites"][0]["shape"] = observed_shape
    assert saved["interaction_sites"][0]["weight"] == 0
    assert saved["interaction_sites"][0]["essential"] is False
    np.testing.assert_allclose(
        saved["interaction_sites"][0]["shape"][
            "position"
            if kind == "point"
            else "start"
            if kind == "cylinder"
            else "center"
        ],
        [1, 2, 3],
    )


def test_historical_optional_defaults_remain_supported(native):
    data = payload()
    data.pop("units")
    data.pop("metadata")
    site = data["interaction_sites"][0]
    for key in ["essential", "weight", "metadata"]:
        site.pop(key)
    restored = native(data)
    assert restored.metadata == {}
    assert restored.interaction_sites[0].essential is True
    assert restored.interaction_sites[0].weight == 1
    assert restored.interaction_sites[0].metadata == {}
