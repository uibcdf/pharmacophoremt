"""Known point geometry must compose with the ordinary native inspectors."""

import json
from copy import deepcopy

import pytest

from pharmacophoremt import Pharmacophore, io
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.interaction_site import (
    HBDonorPoint,
    HBDonorSphere,
    InteractionSite,
)
from pharmacophoremt.interaction_site.shape import Cylinder, Point
from pharmacophoremt.io.phmt import _to_dict


@pytest.mark.parametrize("units", [["nm", "ps", "radians"], ["pm", "fs", "degrees"]])
@pytest.mark.parametrize("inherited", [False, True])
def test_point_center_is_a_live_read_only_alias_of_canonical_position(units, inherited):
    shape_type = type("ApplicationPoint", (Point,), {}) if inherited else Point
    with puw.context(standard_units=units):
        shape = shape_type("[1,2,3] angstrom")
        site = InteractionSite(shape, "hb donor")
        assert shape.center is shape.position
        assert site.center is shape.position
        assert puw.get_value(site.center, to_unit="nm") == pytest.approx(
            [0.1, 0.2, 0.3]
        )
        with pytest.raises(AttributeError):
            shape.center = puw.quantity([7, 8, 9], "nm")
        shape.position = puw.quantity([4, 5, 6], "angstrom")
        assert shape.center is shape.position
        assert puw.get_value(site.center, to_unit="nm") == pytest.approx(
            [0.4, 0.5, 0.6]
        )
        assert site.radius is None


@pytest.mark.parametrize("units", [["nm", "ps", "radians"], ["pm", "fs", "degrees"]])
@pytest.mark.parametrize(
    "kinds", [("point", "point"), ("point", "sphere"), ("sphere", "sphere")]
)
def test_native_queries_preserve_known_centers_and_three_four_five_distance(
    units, kinds
):
    with puw.context(standard_units=units):
        model = Pharmacophore()
        for kind, position in zip(kinds, ["[1,2,3] angstrom", "[0.4,0.6,0.3] nm"]):
            site = (
                HBDonorPoint(position)
                if kind == "point"
                else HBDonorSphere(position, "0.1 nm")
            )
            model.add_interaction_site(site)
        original = deepcopy(_to_dict(model))
        centers = puw.get_value(model.get(get_center=True), to_unit="nm")
        assert centers.shape == (2, 3)
        assert centers[0] == pytest.approx([0.1, 0.2, 0.3])
        assert centers[1] == pytest.approx([0.4, 0.6, 0.3])
        distances = puw.get_value(model.get_distance_matrix(), to_unit="angstrom")
        assert distances.shape == (2, 2)
        assert distances[0, 1] == pytest.approx(5)
        assert distances[1, 0] == pytest.approx(5)
        assert distances[0, 0] == distances[1, 1] == 0
        assert _to_dict(model) == original


@pytest.mark.parametrize("kind", ["empty", "selection", "feature", "shape"])
def test_empty_center_queries_keep_three_coordinate_columns(kind):
    model = Pharmacophore()
    options = {}
    if kind != "empty":
        model.add_interaction_site(HBDonorPoint("[0,0,0] nm"))
        options = (
            {"selection": []}
            if kind == "selection"
            else {"feature_name": "hb acceptor"}
            if kind == "feature"
            else {"shape_name": "sphere"}
        )
    result = model.get(get_center=True, **options)
    assert puw.is_quantity(result)
    assert puw.get_value(result, to_unit="nm").shape == (0, 3)


def test_point_center_alias_does_not_add_a_native_serialized_field(tmp_path):
    model = Pharmacophore()
    model.add_interaction_site(HBDonorPoint("[1,2,3] angstrom"))
    path = tmp_path / "query.json"
    io.to_json(model, path)
    stored = json.loads(path.read_text())
    assert set(stored["interaction_sites"][0]["shape"]) == {"type", "position"}
    restored = io.load_json(path)
    site = restored.interaction_sites[0]
    assert site.shape.center is site.shape.position
    assert puw.get_value(site.center, to_unit="nm") == pytest.approx([0.1, 0.2, 0.3])


def test_inspection_does_not_invent_a_cylinder_center_or_point_radius():
    cylinder = InteractionSite(
        Cylinder("[0,0,0] nm", "[1,0,0] nm", "0.1 nm"), "hb donor"
    )
    assert cylinder.center is None
    assert HBDonorPoint("[0,0,0] nm").radius is None
