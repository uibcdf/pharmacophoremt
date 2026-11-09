"""Independent scientific-field admission and projection-loss controls for #163."""

import json
import warnings
from copy import deepcopy

import pytest

from pharmacophoremt import Pharmacophore, io
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    ProjectionLossError,
)
from pharmacophoremt._private.smonitor.warnings import ProjectionLossWarning


def point(**fields):
    return dict(name="PositiveIon", x=0, y=0, z=0, radius=0.5, enabled=True, **fields)


def test_optional_requirement_is_visible_in_the_default_loss_report():
    raw = {"points": [point(requirement="optional")]}
    original = deepcopy(raw)
    with pytest.warns(ProjectionLossWarning, match="points\\[0\\].requirement"):
        model = io.from_pharmer(raw)
    report = model.metadata["pharmer"]["import_report"]
    assert report["schema"] == "pharmacophoremt.pharmer-import@1"
    assert report["losses"] == ["points[0].requirement"]
    assert model.interaction_sites[0].essential
    assert raw == original


@pytest.mark.parametrize("requirement", ["optional", "notpresent"])
def test_strict_refusal_precedes_any_native_or_molecular_construction(
    requirement, monkeypatch
):
    import pharmacophoremt.io.pharmer as reader
    import pharmacophoremt.pharmacophore as module

    calls = []
    monkeypatch.setattr(module, "Pharmacophore", lambda *a, **k: calls.append("model"))
    monkeypatch.setattr(reader.msm, "convert", lambda *a, **k: calls.append("molecule"))
    raw = {"points": [point(requirement=requirement)], "ligand": "not decoded"}
    with pytest.raises(ProjectionLossError) as caught:
        io.from_pharmer(raw, on_loss="raise")
    assert caught.value.code == "PHMT-E110" and calls == []


def test_warning_as_error_stops_before_model_construction(monkeypatch):
    import pharmacophoremt.pharmacophore as module

    calls = []
    monkeypatch.setattr(module, "Pharmacophore", lambda *a, **k: calls.append("model"))
    with warnings.catch_warnings():
        warnings.simplefilter("error", ProjectionLossWarning)
        with pytest.raises(ProjectionLossWarning):
            io.from_pharmer({"points": [point(requirement="notpresent")]})
    assert calls == []


@pytest.mark.parametrize("requirement", [None, "required", "Required"])
def test_supported_required_sphere_has_no_scientific_loss(requirement):
    row = point()
    if requirement is not None:
        row["requirement"] = requirement
    model, report = io.from_pharmer(
        {"points": [row]}, return_report=True, on_loss="raise"
    )
    assert report["losses"] == [] and report["length_unit"] == "angstrom"
    assert model.n_interaction_sites == 1 and model.interaction_sites[0].essential
    assert model.metadata == {}


@pytest.mark.parametrize(
    "bound,value",
    [("minsize", 2), ("minsize", "3"), ("maxsize", 4), ("maxsize", 0), ("size", 1)],
)
def test_nonpreserved_size_information_cannot_pass_strict_mode(bound, value):
    with pytest.raises(ProjectionLossError, match=bound):
        io.from_pharmer({"points": [point(**{bound: value})]}, on_loss="raise")


@pytest.mark.parametrize(
    "bounds",
    [
        {},
        {"minsize": "", "maxsize": ""},
        {"minsize": None, "maxsize": None},
        {"minsize": 0},
        {"minsize": "0"},
    ],
)
def test_neutral_size_bounds_remain_ordinary_spheres(bounds):
    _, report = io.from_pharmer(
        {"points": [point(**bounds)]}, on_loss="raise", return_report=True
    )
    assert report["losses"] == []


@pytest.mark.parametrize("mode", [False, 0])
def test_explicitly_inactive_vector_never_creates_a_directional_constraint(mode):
    row = point()
    row.update(name="HydrogenDonor", vector_on=mode, svector={"x": -1, "y": 0, "z": 0})
    model = io.from_pharmer({"points": [row]})
    assert model.interaction_sites[0].shape_name == "sphere"
    assert model.interaction_sites[0].direction is None


@pytest.mark.parametrize("mode", [True, 1, None])
@pytest.mark.parametrize("field", ["svector", "vector"])
def test_one_active_vector_is_preserved_without_inventing_an_angle_policy(mode, field):
    row = point()
    row.update(name="HydrogenDonor", hasvec=False)
    if mode is not None:
        row["vector_on"] = mode
    vector = {"x": 1, "y": 0, "z": 0}
    row[field] = vector if field == "svector" else [vector]
    model, report = io.from_pharmer(
        {"points": [row]}, on_loss="raise", return_report=True
    )
    assert model.interaction_sites[0].shape_name == "sphere and vector"
    assert report["losses"] == []
    assert report["sites"][0]["direction_active"]


def test_multiple_active_vectors_are_not_arbitrarily_reduced_even_in_ignore_mode():
    row = point()
    row.update(
        name="HydrogenDonor",
        vector_on=1,
        vector=[{"x": 1, "y": 0, "z": 0}, {"x": -1, "y": 0, "z": 0}],
    )
    with pytest.raises(ArgumentError, match="multiple"):
        io.from_pharmer({"points": [row]}, on_loss="ignore")


def test_unknown_scientific_fields_and_engine_settings_are_not_hidden_in_ui_metadata():
    row = point(mystery_constraint=12, selected=True)
    raw = {
        "points": [row],
        "max-hits": 7,
        "minMolWeight": 150,
        "view": {"private": "do-not-copy"},
        "backgroundcolor": "white",
    }
    original = deepcopy(raw)
    model, report = io.from_pharmer(raw, on_loss="ignore", return_report=True)
    assert set(report["losses"]) == {
        "points[0].mystery_constraint",
        "query.max-hits",
        "query.minMolWeight",
    }
    assert set(report["unapplied_settings"]) == {"query.max-hits", "query.minMolWeight"}
    assert set(report["ignored_fields"]) >= {
        "query.view",
        "query.backgroundcolor",
        "points[0].selected",
    }
    assert "do-not-copy" not in json.dumps(report)
    stored = deepcopy(model.metadata["pharmer"]["import_report"])
    report["losses"].clear()
    assert model.metadata["pharmer"]["import_report"] == stored and raw == original


@pytest.mark.parametrize("route", ["reader", "facade", "constructor"])
def test_guided_and_expert_default_decisions_match(route, tmp_path):
    raw = {"points": [point(requirement="optional")]}
    path = tmp_path / "query.json"
    path.write_text(json.dumps(raw))
    original = path.read_bytes()
    with pytest.warns(ProjectionLossWarning):
        if route == "reader":
            model = io.from_pharmer(str(path))
        elif route == "facade":
            model = io.load(str(path))
        else:
            model = Pharmacophore(str(path), form="pharmer")
    assert model.metadata["pharmer"]["import_report"]["losses"] == [
        "points[0].requirement"
    ]
    assert path.read_bytes() == original


def test_disabled_points_keep_original_mapping_without_admitting_inactive_constraints():
    raw = {
        "points": [
            {
                "enabled": False,
                "name": "unknown",
                "requirement": "notpresent",
                "vector": "ignored",
            },
            point(),
        ]
    }
    model, report = io.from_pharmer(raw, on_loss="raise", return_report=True)
    assert model.metadata["pharmer"]["source_point_indices"] == [1]
    assert report["losses"] == [] and report["disabled_point_indices"] == [0]


@pytest.mark.parametrize(
    "options", [{"on_loss": "silent"}, {"on_loss": None}, {"return_report": 1}]
)
def test_invalid_policy_options_never_select_an_implicit_fallback(options):
    with pytest.raises(ArgumentError):
        io.from_pharmer({"points": [point()]}, **options)


def test_native_donor_matching_obeys_an_explicitly_disabled_source_vector():
    from pharmacophoremt.screening import PoseEvaluator
    from phmt_test_support.absence_inputs import system

    row = point()
    row.update(name="HydrogenDonor", vector_on=0, svector={"x": -1, "y": 0, "z": 0})
    source = system("[2H]O", [[0.1, 0, 0], [0, 0, 0]])
    model = io.from_pharmer({"points": [row]})
    final = PoseEvaluator(model).evaluate(source)
    assert final["status"] == "matched" and final["fit_value"] == 1
    row["vector_on"] = 1
    directed = io.from_pharmer({"points": [row]})
    assert PoseEvaluator(directed).evaluate(source)["status"] == "not_matched"


def test_accepting_losses_remains_explicit_and_keeps_a_native_persisted_audit(tmp_path):
    raw = {"points": [point(requirement="notpresent", minsize=3)]}
    with warnings.catch_warnings(record=True) as observed:
        warnings.simplefilter("always", ProjectionLossWarning)
        model, report = io.from_pharmer(raw, on_loss="ignore", return_report=True)
    assert not [r for r in observed if issubclass(r.category, ProjectionLossWarning)]
    assert model.metadata["pharmer"]["source_point_indices"] == [0]
    assert model.metadata["pharmer"]["disabled_point_indices"] == []
    path = tmp_path / "native.json"
    io.to_json(model, path)
    restored = io.load(str(path))
    assert restored.metadata["pharmer"]["import_report"] == report
    assert set(report["losses"]) == {"points[0].requirement", "points[0].minsize"}


def test_loss_warnings_are_coalesced_and_do_not_copy_raw_payloads():
    raw = {"points": [point(requirement="optional", maxsize=4)], "max-hits": 3}
    with pytest.warns(ProjectionLossWarning) as observed:
        _, report = io.from_pharmer(raw, return_report=True)
    assert len(observed) == 1
    assert set(report["losses"]) == set(report["loss_details"])
    assert set(report["losses"]) == {
        "points[0].requirement",
        "points[0].maxsize",
        "query.max-hits",
    }


def test_a_direction_on_an_unsupported_feature_is_reported_without_a_fabricated_shape():
    raw = {"points": [point(vector_on=1, svector={"x": 1, "y": 0, "z": 0})]}
    with pytest.raises(ProjectionLossError, match="svector"):
        io.from_pharmer(raw, on_loss="raise")
    model, report = io.from_pharmer(raw, on_loss="ignore", return_report=True)
    assert model.interaction_sites[0].shape_name == "sphere"
    assert report["losses"] == ["points[0].svector"]


@pytest.mark.parametrize(
    "field,value",
    [
        ("requirement", None),
        ("requirement", "optionl"),
        ("minsize", -1),
        ("minsize", []),
        ("maxsize", True),
        ("vector_on", "false"),
        ("vector_on", 2),
        ("vector_on", None),
    ],
)
def test_malformed_admission_fields_are_not_excused_by_ignore_mode(field, value):
    row = point()
    row[field] = value
    with pytest.raises((ArgumentError, TypeError)):
        io.from_pharmer({"points": [row]}, on_loss="ignore")


def test_inactive_payloads_and_neutral_engine_settings_remain_inspectable():
    row = point(vector_on=0, svector="inactive, not decoded")
    model, report = io.from_pharmer(
        {"points": [row], "max-hits": ""}, on_loss="raise", return_report=True
    )
    assert report["losses"] == []
    assert report["unapplied_settings"] == ["query.max-hits"]
    assert "points[0].svector" in report["ignored_fields"]
    assert model.metadata["pharmer"]["source_point_indices"] == [0]


def test_single_vector_fields_keep_units_under_a_nondefault_application_policy():
    from pharmacophoremt import pyunitwizard as puw

    row = point()
    row.update(
        name="HydrogenDonor", x=2, vector_on=True, vector=[{"x": 1, "y": 0, "z": 0}]
    )
    with puw.context(standard_units=["pm", "ps", "radians"]):
        model, report = io.from_pharmer(
            {"points": [row]}, on_loss="raise", return_report=True
        )
        site = model.interaction_sites[0]
        assert puw.get_value(site.center, to_unit="nm").tolist() == pytest.approx(
            [0.2, 0, 0]
        )
        assert puw.get_value(site.radius, to_unit="nm") == pytest.approx(0.05)
        assert puw.get_value(
            site.direction, to_unit="dimensionless"
        ).tolist() == pytest.approx([1, 0, 0])
        assert report["length_unit"] == "angstrom"
