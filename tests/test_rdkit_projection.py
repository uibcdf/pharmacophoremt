"""Actual provider geometry, field loss and complete-preflight controls."""

import json
import warnings
from copy import deepcopy

import numpy as np
import pytest
from rdkit import Geometry
from rdkit.Chem import ChemicalFeatures
from rdkit.Chem.Pharm3D import Pharmacophore as rd

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    ProjectionLossError,
)
from pharmacophoremt._private.smonitor.warnings import ProjectionLossWarning
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


def native():
    result = phmt.Pharmacophore()
    result.add_interaction_site(
        InteractionSite(Sphere("[0,0,0] angstrom", "1.5 angstrom"), "hb donor")
    )
    result.add_interaction_site(
        InteractionSite(Sphere("[0.3,0.4,0] nm", "0.2 nm"), "hb acceptor")
    )
    return result


def test_default_type_bounds_and_loss_warning_preserve_source():
    source = native()
    before = deepcopy(_to_dict(source))
    with pytest.warns(ProjectionLossWarning) as caught:
        target, report = phmt.io.to_rdkit(source, return_report=True)
    assert len(caught) == 1
    assert caught[0].message.code == "PHMT-W103"
    assert isinstance(target, rd.Pharmacophore)
    assert target.getLowerBound(0, 1) == pytest.approx(5)
    assert target.getUpperBound(0, 1) == pytest.approx(5)
    assert report["losses"] == ["sites[0].radius", "sites[1].radius"]
    assert report["sites"][1]["center"] == pytest.approx([3, 4, 0])
    assert json.loads(json.dumps(report, allow_nan=False)) == report
    assert _to_dict(source) == before


@pytest.mark.parametrize(
    "feature,family",
    [
        ("hb donor", "Donor"),
        ("hb acceptor", "Acceptor"),
        ("aromatic ring", "Aromatic"),
        ("hydrophobicity", "Hydrophobic"),
        ("positive charge", "PosIonizable"),
        ("negative charge", "NegIonizable"),
    ],
)
def test_explicit_round_trip_preserves_family_center_and_individual_radius(
    feature, family
):
    source = phmt.Pharmacophore()
    source.add_interaction_site(InteractionSite(Point("[1,2,3] angstrom"), feature))
    source.add_interaction_site(
        InteractionSite(Sphere("[0.3,0.4,0] nm", "0.2 nm"), feature)
    )
    before = deepcopy(_to_dict(source))
    target, report = phmt.io.to_rdkit(
        source, representation="spheres", return_report=True, on_loss="raise"
    )
    assert isinstance(target, rd.ExplicitPharmacophore)
    assert list(target.getRadii()) == pytest.approx([0, 2])
    assert target.getFeature(1).GetFamily() == family
    restored, imported = phmt.io.load_rdkit(
        target, radius=None, return_report=True, on_loss="raise"
    )
    assert imported["losses"] == report["losses"] == []
    assert isinstance(restored.interaction_sites[0].shape, Point)
    assert isinstance(restored.interaction_sites[1].shape, Sphere)
    assert puw.get_value(
        restored.interaction_sites[0].shape.position, to_unit="angstrom"
    ) == pytest.approx([1, 2, 3])
    assert puw.get_value(
        restored.interaction_sites[1].radius, to_unit="angstrom"
    ) == pytest.approx(2)
    assert all(site.features == [feature] for site in restored.interaction_sites)
    assert _to_dict(source) == before
    report["sites"][1]["center"][0] = 200
    imported["sites"][1]["center"][0] = 300
    assert target.getFeature(1).GetPos().x == pytest.approx(3)
    assert puw.get_value(restored.interaction_sites[1].center, to_unit="angstrom")[
        0
    ] == pytest.approx(3)
    target.setRadius(1, 7)
    assert report["sites"][1]["radius"] == pytest.approx(2)
    assert puw.get_value(
        restored.interaction_sites[1].radius, to_unit="angstrom"
    ) == pytest.approx(2)


@pytest.mark.parametrize("representation", ["points", "spheres"])
def test_empty_provider_objects_use_public_initialization(representation):
    target = phmt.io.to_rdkit(
        phmt.Pharmacophore(), representation=representation, on_loss="raise"
    )
    assert list(target.getFeatures()) == []
    restored = phmt.io.load_rdkit(
        target,
        radius=None if representation == "spheres" else "1 angstrom",
        on_loss="raise",
    )
    assert restored.n_interaction_sites == 0


@pytest.mark.parametrize(
    "radius,expected", [("1 angstrom", 1), ("0.25 nm", 2.5), ("0 angstrom", 0)]
)
def test_reader_fixed_radius_is_an_explicit_assumption(radius, expected):
    target = phmt.io.to_rdkit(native(), representation="spheres", on_loss="raise")
    restored, report = phmt.io.load_rdkit(
        target, radius=radius, return_report=True, on_loss="ignore"
    )
    assert report["losses"] == ["sites[0].stored_radius", "sites[1].stored_radius"]
    assert {row["field"]: row["value"] for row in report["assumptions"]}[
        "sites.radius"
    ] == pytest.approx(expected)
    for site in restored.interaction_sites:
        if expected == 0:
            assert isinstance(site.shape, Point)
        else:
            assert puw.get_value(site.radius, to_unit="angstrom") == pytest.approx(
                expected
            )
    assert list(target.getRadii()) == pytest.approx([1.5, 2])


def test_default_reader_retains_specialized_one_angstrom_sphere():
    target = phmt.io.to_rdkit(native(), on_loss="ignore")
    with pytest.warns(ProjectionLossWarning):
        restored = phmt.io.load_rdkit(target)
    assert isinstance(
        restored.interaction_sites[0], phmt.interaction_site.HBDonorSphere
    )
    assert puw.get_value(
        restored.interaction_sites[0].radius, to_unit="angstrom"
    ) == pytest.approx(1)


def test_strict_and_warning_as_error_stop_before_any_feature_construction(monkeypatch):
    source = native()

    def forbidden(*args, **kwargs):
        pytest.fail("target feature constructed before loss admission")

    monkeypatch.setattr(ChemicalFeatures, "FreeChemicalFeature", forbidden)
    with pytest.raises(ProjectionLossError) as caught:
        phmt.io.to_rdkit(source, on_loss="raise")
    assert caught.value.code == "PHMT-E110"
    with warnings.catch_warnings():
        warnings.simplefilter("error", ProjectionLossWarning)
        with pytest.raises(ProjectionLossWarning):
            phmt.io.to_rdkit(source)


@pytest.mark.parametrize(
    "change",
    [
        "unknown",
        "unmapped",
        "alternatives",
        "counts",
        "feature_counts",
        "nan_center",
        "negative_radius",
        "zero_sphere",
        "nan_weight",
        "essential",
        "metadata",
        "cylinder",
    ],
)
def test_all_native_sites_are_preflighted_before_target_creation(change, monkeypatch):
    source = native()
    site = source.interaction_sites[1]
    if change in {"unknown", "unmapped", "alternatives"}:
        site.features = {
            "unknown": ["any"],
            "unmapped": ["metal coordination"],
            "alternatives": ["hb donor", "hb acceptor"],
        }[change]
        site.n_features = len(site.features)
    elif change == "counts":
        source.n_interaction_sites = 3
    elif change == "feature_counts":
        site.n_features = 0
    elif change == "nan_center":
        site.shape.center = puw.quantity([0, np.nan, 0], "nm")
    elif change in {"negative_radius", "zero_sphere"}:
        site.shape.radius = puw.quantity(-1 if change == "negative_radius" else 0, "nm")
    elif change == "nan_weight":
        site.weight = np.nan
    elif change == "essential":
        site.essential = "yes"
    elif change == "metadata":
        site.metadata = []
    else:
        site.shape = Cylinder("[0,0,0] nm", "[1,0,0] nm", "1 nm")

    def forbidden(*args, **kwargs):
        pytest.fail("partial RDKit target constructed before complete native admission")

    monkeypatch.setattr(ChemicalFeatures, "FreeChemicalFeature", forbidden)
    with pytest.raises(ArgumentError):
        phmt.io.to_rdkit(source, on_loss="ignore")


@pytest.mark.parametrize(
    "options",
    [
        {"representation": "unknown"},
        {"representation": []},
        {"on_loss": "quiet"},
        {"on_loss": []},
        {"return_report": 1},
    ],
)
def test_invalid_export_options_do_not_select_a_fallback(options):
    with pytest.raises(ArgumentError):
        phmt.io.to_rdkit(native(), **options)


@pytest.mark.parametrize(
    "shape,fields",
    [
        (SphereAndVector("[0,0,0] nm", "0.1 nm", [1, 0, 0]), ["direction", "radius"]),
        (
            Disk(center="[0,0,0] nm", normal=[0, 0, 1], radius="0.1 nm"),
            ["normal", "radius"],
        ),
        (GaussianKernel("[0,0,0] nm", "0.1 nm"), ["sigma"]),
    ],
)
def test_nonpoint_geometry_reports_constraints_without_inventing_them(shape, fields):
    source = phmt.Pharmacophore()
    source.add_interaction_site(InteractionSite(shape, "hb donor"))
    target, report = phmt.io.to_rdkit(source, return_report=True, on_loss="ignore")
    assert isinstance(target, rd.Pharmacophore)
    assert report["losses"] == ["sites[0]." + field for field in fields]
    if isinstance(shape, GaussianKernel):
        with pytest.raises(ArgumentError):
            phmt.io.to_rdkit(source, representation="spheres", on_loss="ignore")


def test_model_site_and_exclusion_losses_are_field_only_not_metadata_copies():
    source = native()
    source.name = "private label"
    marker = object()
    source.metadata = {"private": marker}
    site = source.interaction_sites[0]
    site.metadata = {"private": marker}
    site.essential, site.weight = False, 2
    site.features = ["excluded volume"]
    _, report = phmt.io.to_rdkit(
        source, representation="spheres", return_report=True, on_loss="ignore"
    )
    assert report["losses"] == [
        "model.name",
        "model.metadata",
        "sites[0].essential",
        "sites[0].weight",
        "sites[0].metadata",
        "sites[0].exclusion_constraint",
    ]
    serialized = json.dumps(report, allow_nan=False)
    assert "private label" not in serialized and '"private"' not in serialized
    assert source.metadata["private"] is site.metadata["private"] is marker


def test_arbitrary_pair_intervals_are_not_inverted_to_radii():
    target = phmt.io.to_rdkit(native(), on_loss="ignore")
    target.setLowerBound(0, 1, 1)
    target.setUpperBound(0, 1, 9)
    restored, report = phmt.io.load_rdkit(target, return_report=True, on_loss="ignore")
    assert report["losses"] == ["pair_bounds", "pair_bounds_2d"]
    assert all(
        puw.get_value(site.radius, to_unit="angstrom") == pytest.approx(1)
        for site in restored.interaction_sites
    )
    with pytest.raises(ArgumentError):
        phmt.io.load_rdkit(target, radius=None, on_loss="ignore")
    assert (target.getLowerBound(0, 1), target.getUpperBound(0, 1)) == (1, 9)


@pytest.mark.parametrize(
    "fault", ["unknown", "radius", "count", "position", "bounds", "provider"]
)
def test_external_preflight_and_provider_failures_precede_native_construction(
    fault, monkeypatch
):
    target = phmt.io.to_rdkit(
        native(),
        representation="spheres" if fault != "bounds" else "points",
        on_loss="ignore",
    )
    if fault == "unknown":
        features = list(target.getFeatures())
        features[1] = ChemicalFeatures.FreeChemicalFeature(
            "Unknown", "any", Geometry.Point3D(0, 0, 0)
        )
        target = rd.ExplicitPharmacophore(features, [1, 2])
    elif fault == "radius":
        target.setRadius(1, float("inf"))
    elif fault == "count":

        class WrongCount(rd.ExplicitPharmacophore):
            def getRadii(self):
                return []

        target = WrongCount(list(target.getFeatures()), [1, 2])
    elif fault == "position":
        target.getFeature(1).SetPos(Geometry.Point3D(float("nan"), 0, 0))
    elif fault == "bounds":
        target.setUpperBound(0, 1, float("nan"))
    else:

        class FailedProvider(rd.ExplicitPharmacophore):
            def getFeatures(self):
                raise RuntimeError("original provider failure")

        target = FailedProvider()

    def forbidden(*args, **kwargs):
        pytest.fail("native target constructed before full external admission")

    monkeypatch.setattr(phmt.Pharmacophore, "__init__", forbidden)
    with (
        pytest.raises(RuntimeError, match="original provider failure")
        if fault == "provider"
        else pytest.raises(ArgumentError)
    ):
        phmt.io.load_rdkit(
            target, radius="1 angstrom" if fault == "bounds" else None, on_loss="ignore"
        )


@pytest.mark.parametrize("radius", ["-1 nm", "nan nm", "[1,2] nm", 1, True, "1 second"])
def test_invalid_reader_radius_cannot_be_silently_normalized(radius):
    target = phmt.io.to_rdkit(native(), representation="spheres", on_loss="raise")
    with pytest.raises((ValueError, TypeError)):
        phmt.io.load_rdkit(target, radius=radius, on_loss="ignore")


def test_extra_keywords_remain_closed_on_both_public_functions():
    with pytest.raises(TypeError):
        phmt.io.to_rdkit(native(), representaton="spheres")
    target = phmt.io.to_rdkit(native(), on_loss="ignore")
    with pytest.raises(TypeError):
        phmt.io.load_rdkit(target, radiuss="1 nm")


def test_reader_reports_custom_type_and_identifier_before_strict_construction():
    feature = ChemicalFeatures.FreeChemicalFeature(
        "Donor", "SpecificDonor", Geometry.Point3D(1, 2, 3), 42
    )
    target = rd.ExplicitPharmacophore([feature], [2])
    restored, report = phmt.io.load_rdkit(
        target, radius=None, return_report=True, on_loss="ignore"
    )
    assert report["losses"] == ["sites[0].type", "sites[0].id"]
    assert restored.interaction_sites[0].features == ["hb donor"]
    assert json.loads(json.dumps(report, allow_nan=False)) == report
    with pytest.raises(ProjectionLossError):
        phmt.io.load_rdkit(target, radius=None, on_loss="raise")
    assert target.getFeature(0).GetType() == "SpecificDonor"
    assert target.getFeature(0).GetId() == 42


@pytest.mark.parametrize(
    "options", [{"on_loss": "quiet"}, {"on_loss": []}, {"return_report": 1}]
)
def test_reader_option_admission_is_independent_of_loss_policy(options):
    target = phmt.io.to_rdkit(native(), representation="spheres", on_loss="raise")
    with pytest.raises(ArgumentError):
        phmt.io.load_rdkit(target, radius=None, **options)


def test_strict_reader_refuses_pair_losses_before_native_constructor(monkeypatch):
    target = phmt.io.to_rdkit(native(), on_loss="ignore")

    def forbidden(*args, **kwargs):
        pytest.fail("native object constructed before strict pair-loss refusal")

    monkeypatch.setattr(phmt.Pharmacophore, "__init__", forbidden)
    with pytest.raises(ProjectionLossError):
        phmt.io.load_rdkit(target, on_loss="raise")


@pytest.mark.parametrize("fault", ["wire_center", "wire_radius", "pair_distance"])
def test_finite_native_units_do_not_allow_nonfinite_rdkit_fields(fault):
    source = native()
    if fault == "wire_center":
        source.interaction_sites[1].shape.center = puw.quantity([1e308, 0, 0], "nm")
    elif fault == "wire_radius":
        source.interaction_sites[1].shape.radius = puw.quantity(1e308, "nm")
    else:
        source.interaction_sites[1].shape.center = puw.quantity(
            [1e200, 0, 0], "angstrom"
        )
    with pytest.raises(ArgumentError):
        phmt.io.to_rdkit(source, on_loss="ignore")


def test_catalog_warning_survives_standard_python_reconstruction():
    original = ProjectionLossWarning(operation="to_rdkit", fields=["sites[0].radius"])
    rebuilt = type(original)(str(original))
    assert str(rebuilt) == str(original)
    with pytest.warns(ProjectionLossWarning):
        warnings.warn(rebuilt)
