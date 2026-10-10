"""Independent PHMT SDF geometry, persistence and placed-query controls."""

import json

import numpy as np
import pytest
from rdkit import Chem

from pharmacophoremt import Pharmacophore
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import (
    Cylinder,
    Disk,
    GaussianKernel,
    Point,
    Shapelet,
    Sphere,
    SphereAndVector,
)
from pharmacophoremt.io import load_json, load_sdf, to_json, to_sdf

CENTER = [1.23456789, -0.02, 0.001]


def model(shape=None):
    result = Pharmacophore(
        name="1 nm",
        description="donor\nα",
        score=0.25,
        ref_mol=2,
        ref_struct=3,
    )
    result.metadata = {"labels": ["nm", "1 ps", "null"], "provenance": {"frame": 3}}
    result.add_interaction_site(
        InteractionSite(
            shape
            if shape is not None
            else SphereAndVector("[0,0,0] nm", ".1 nm", [1, 0, 0]),
            ["hb donor", "hydrophobicity"],
            weight=2.5,
            essential=False,
            metadata={"atom_indices": [4, 7], "tolerance": puw.quantity(0.04, "nm")},
        )
    )
    return result


@pytest.mark.parametrize(
    "kind",
    ["point", "sphere", "sphere and vector", "disk", "gaussian kernel", "cylinder"],
)
def test_supported_shapes_preserve_scientific_fields_across_unit_contexts(
    tmp_path, kind
):
    # More precision than a V2000 coordinate field can preserve.
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        center = puw.quantity(np.array(CENTER) * 10, "angstrom")
        radius = puw.quantity(1.3, "angstrom")
        shapes = {
            "point": lambda: Point(center),
            "sphere": lambda: Sphere(center, radius),
            "sphere and vector": lambda: SphereAndVector(center, radius, [0, 1, 0]),
            "disk": lambda: Disk(center, [0, 0, -1], radius),
            "gaussian kernel": lambda: GaussianKernel(center, radius),
            "cylinder": lambda: Cylinder(center, "[2,3,4] nm", radius),
        }
        original = model(shapes[kind]())
        path = tmp_path / "model.sdf"
        to_sdf(original, path)
        to_json(original, tmp_path / "native.json")
        sd = Chem.SDMolSupplier(str(path))[0]
        assert sd.GetNumAtoms() == 1 and sd.GetAtomWithIdx(0).GetAtomicNum() == 2
        assert sd.GetNumBonds() == 0
        assert sd.GetProp("PHARMACOPHOREMT_SCHEMA") == "pharmacophoremt.sdf@1"
        assert list(sd.GetConformer().GetAtomPosition(0)) == pytest.approx(
            np.array(CENTER) * 10, abs=5.1e-5
        )
        assert json.loads(sd.GetProp("PHARMACOPHOREMT_MODEL")) == json.loads(
            (tmp_path / "native.json").read_text()
        )
    with puw.context(standard_units=["angstrom", "ps", "radians"]):
        restored = load_sdf(path)
        site = restored.interaction_sites[0]
        assert site.shape_name == kind
        assert site.features == ["hb donor", "hydrophobicity"]
        assert site.weight == 2.5 and site.essential is False
        assert site.metadata["atom_indices"] == [4, 7]
        quantity = puw.QuantityRecord.from_dict(
            site.metadata["tolerance"]
        ).to_quantity()
        assert puw.get_value(quantity, to_unit="nm") == pytest.approx(0.04)
        anchor = getattr(
            site.shape, {"point": "position", "cylinder": "start"}.get(kind, "center")
        )
        np.testing.assert_allclose(
            puw.get_value(anchor, to_unit="nm"), CENTER, rtol=0, atol=1e-12
        )
        if kind == "sphere and vector":
            np.testing.assert_allclose(
                puw.get_value(site.direction, to_unit="dimensionless"), [0, 1, 0]
            )
        if kind == "disk":
            np.testing.assert_allclose(
                puw.get_value(site.shape.normal, to_unit="dimensionless"), [0, 0, -1]
            )
        if kind == "cylinder":
            np.testing.assert_allclose(
                puw.get_value(site.shape.end, to_unit="nm"), [2, 3, 4]
            )
        if kind != "point":
            size = site.sigma if kind == "gaussian kernel" else site.radius
            assert puw.get_value(size, to_unit="nm") == pytest.approx(0.13)
        assert (
            restored.name,
            restored.description,
            restored.score,
            restored.ref_mol,
            restored.ref_struct,
        ) == ("1 nm", "donor\nα", 0.25, 2, 3)
        assert restored.metadata == original.metadata
        assert restored.molecular_system is None
        # The existing constructor consumes the same codec.
        assert (
            Pharmacophore(str(path), form="sdf").interaction_sites[0].shape_name == kind
        )
        assert (
            load_json(tmp_path / "native.json").interaction_sites[0].shape_name == kind
        )


def test_original_directional_donor_regression(tmp_path):
    original = Pharmacophore()
    original.add_interaction_site(
        InteractionSite(
            SphereAndVector("[0,0,0] nm", ".1 nm", [1, 0, 0]),
            "hb donor",
            weight=2,
            essential=False,
        )
    )
    path = tmp_path / "donor.sdf"
    to_sdf(original, path)
    site = load_sdf(path).interaction_sites[0]
    assert site.shape_name == "sphere and vector"
    assert site.weight == 2 and site.essential is False
    np.testing.assert_array_equal(
        puw.get_value(site.direction, to_unit="dimensionless"), [1, 0, 0]
    )


def test_empty_and_multiple_sites_preserve_order_without_stale_counts(tmp_path):
    original = Pharmacophore(name="empty")
    path = tmp_path / "sites.sdf"
    to_sdf(original, path)
    assert load_sdf(path).n_interaction_sites == 0
    for coordinate in [2, 0, 1]:
        original.add_interaction_site(
            InteractionSite(
                Sphere(f"[{coordinate},0,0] nm", ".1 nm"),
                "hydrophobicity",
                weight=coordinate,
            )
        )
    original.n_interaction_sites = 99  # The serialized site list is authoritative.
    to_sdf(original, path)
    restored = load_sdf(path)
    assert restored.n_interaction_sites == 3
    assert [site.weight for site in restored.interaction_sites] == [2, 0, 1]
    assert [
        puw.get_value(site.center, to_unit="nm")[0]
        for site in restored.interaction_sites
    ] == [2, 0, 1]


@pytest.mark.parametrize("bad", ["shapelet", "nan metadata", "negative weight"])
def test_unsupported_export_does_not_touch_destination(tmp_path, bad):
    original = model()
    if bad == "shapelet":
        # Bypass the site's own rejection to exercise the codec's export guard.
        original.interaction_sites[0].shape = Shapelet()
    if bad == "nan metadata":
        original.metadata["score"] = float("nan")
    if bad == "negative weight":
        original.interaction_sites[0].weight = -1
    path = tmp_path / "existing.sdf"
    path.write_text("keep original bytes")
    with pytest.raises(ValueError):
        to_sdf(original, path)
    assert path.read_text() == "keep original bytes"


def test_historical_sphere_tags_are_explicitly_rejected(tmp_path):
    # A real legacy-style donor cannot recover its omitted direction/weight/status.
    molecule = Chem.MolFromSmiles("[He]")
    conf = Chem.Conformer(1)
    conf.SetAtomPosition(0, (0, 0, 0))
    molecule.AddConformer(conf)
    molecule.SetProp("SITE_0_FEATURES", "hb donor")
    molecule.SetProp("SITE_0_SHAPE", "sphere and vector")
    molecule.SetProp("SITE_0_RADIUS", "1.0")
    path = tmp_path / "legacy.sdf"
    with Chem.SDWriter(str(path)) as writer:
        writer.write(molecule)
    with pytest.raises(ValueError, match="Unversioned.*original model"):
        load_sdf(path)


@pytest.mark.parametrize(
    "bad",
    [
        "schema",
        "missing payload",
        "invalid json",
        "missing weight",
        "missing essential",
        "missing direction",
        "extra shape field",
        "unknown shape",
        "units",
        "zero vector",
        "negative radius",
        "string weight",
        "essential integer",
        "unknown feature",
        "anchor",
        "atom",
        "site count",
        "multiple",
        "invalid record",
    ],
)
def test_incomplete_or_inconsistent_sdf_is_rejected(tmp_path, bad):
    path = tmp_path / "invalid.sdf"
    to_sdf(model(), path)
    molecule = Chem.SDMolSupplier(str(path))[0]
    payload = json.loads(molecule.GetProp("PHARMACOPHOREMT_MODEL"))
    site = payload["interaction_sites"][0]
    if bad == "schema":
        molecule.SetProp("PHARMACOPHOREMT_SCHEMA", "pharmacophoremt.sdf@99")
    elif bad == "missing payload":
        molecule.ClearProp("PHARMACOPHOREMT_MODEL")
    elif bad == "invalid json":
        molecule.SetProp("PHARMACOPHOREMT_MODEL", "{not json}")
    elif bad.startswith("missing "):
        field = bad.removeprefix("missing ")
        del (site["shape"] if field == "direction" else site)[field]
    elif bad == "extra shape field":
        site["shape"]["cone_angle"] = 10
    elif bad == "unknown shape":
        site["shape"]["type"] = "shapelet"
    elif bad == "units":
        payload["units"]["length"] = "angstrom"
    elif bad == "zero vector":
        site["shape"]["direction"] = [0, 0, 0]
    elif bad == "negative radius":
        site["shape"]["radius"] = -1
    elif bad == "string weight":
        site["weight"] = "2"
    elif bad == "essential integer":
        site["essential"] = 0
    elif bad == "unknown feature":
        site["features"] = ["unknown"]
    elif bad == "anchor":
        molecule.GetConformer().SetAtomPosition(0, (5, 0, 0))
    elif bad == "atom":
        molecule.GetAtomWithIdx(0).SetAtomicNum(6)
    elif bad == "site count":
        payload["interaction_sites"] = []
    if bad not in {"missing payload", "invalid json"}:
        molecule.SetProp("PHARMACOPHOREMT_MODEL", json.dumps(payload))
    with Chem.SDWriter(str(path)) as writer:
        writer.write(molecule)
        if bad == "multiple":
            writer.write(molecule)
    if bad == "invalid record":
        path.write_text("not an SDF\n$$$$\n")
    with pytest.raises(ValueError):
        load_sdf(path)


@pytest.mark.parametrize(
    "direction,essential", [([1, 0, 0], True), ([-1, 0, 0], True), ([-1, 0, 0], False)]
)
def test_saved_query_preserves_direction_weight_and_mandatory_behavior(
    tmp_path, direction, essential
):
    from pharmacophoremt.screening import PoseEvaluator
    from tests.test_pose_evaluation import system

    source = system("[2H]O", [[0.1, 0, 0], [0, 0, 0]])
    original = Pharmacophore()
    original.add_interaction_site(
        InteractionSite(
            SphereAndVector("[0,0,0] nm", ".15 nm", direction),
            "hb donor",
            weight=2,
            essential=essential,
        )
    )
    original.add_interaction_site(
        InteractionSite(
            Sphere("[2,0,0] nm", ".1 nm"),
            "hydrophobicity",
            weight=1,
            essential=False,
        )
    )
    path = tmp_path / "query.sdf"
    to_sdf(original, path)
    for query in [original, load_sdf(path)]:
        result = PoseEvaluator(query).evaluate(source)
        assert result["fit_value"] == pytest.approx(2 / 3 if direction[0] == 1 else 0)
        assert result["missing_essential_sites"] == (
            [0] if direction[0] == -1 and essential else []
        )
        # With no assignment the evaluator reports not_matched even if optional.
        assert result["status"] == ("matched" if direction[0] == 1 else "not_matched")
