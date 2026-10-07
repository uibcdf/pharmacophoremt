"""Public geometry, diagnostic rendering and optional-provider boundaries."""

import subprocess
import sys

import numpy as np
import pytest

from pharmacophoremt import Pharmacophore
from pharmacophoremt._private.smonitor.catalog import CATALOG, CODES, PACKAGE_ROOT
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    LibraryNotFoundError,
)
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere, SphereAndVector


@pytest.mark.parametrize(
    "center,radius",
    [
        ([0, 0, 0], "0.1 nm"),
        ("[0,0] nm", "0.1 nm"),
        ("[0,0,0] nm", "-1 nm"),
        ("[0,0,0] nm", "1 ps"),
    ],
)
def test_invalid_geometry_has_host_diagnostic(center, radius):
    with pytest.raises(ArgumentError) as caught:
        Sphere(center, radius)
    assert caught.value.code == "PHMT-E102"
    assert "Invalid '" in str(caught.value)


@pytest.mark.parametrize("direction", [[0, 0, 0], [1, 0], [np.nan, 0, 1]])
def test_invalid_directions_raise(direction):
    with pytest.raises(ArgumentError):
        SphereAndVector("[0,0,0] nm", "0.1 nm", direction)


def test_nonnegative_weight_known_features_and_detached_metadata():
    shape = Sphere("[0,0,0] nm", "0.1 nm")
    with pytest.raises(ArgumentError):
        InteractionSite(shape, "hydrophobicity", weight=-1)
    with pytest.raises(ArgumentError):
        InteractionSite(shape, "unknown")
    metadata = {"indices": [1]}
    site = InteractionSite(shape, "hydrophobicity", metadata=metadata)
    metadata["indices"].append(2)
    assert site.metadata["indices"] == [1]


def test_detached_provenance_preserves_literal_strings_and_quantity_objects():
    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt._private.molsysmt import detached

    identities = ["a", "b", "nm", "s", "1 nm"]
    original = dict(
        ligand_ids=identities.copy(),
        nested=dict(label=np.str_("a"), values=np.array([1, 2])),
        distance=puw.quantity(0.12, "nm"),
    )
    saved = detached(original)
    assert saved["ligand_ids"] == identities
    assert type(saved["nested"]["label"]) is str
    assert saved["nested"]["label"] == "a"
    assert all(type(identity) is str for identity in saved["ligand_ids"])
    restored = puw.QuantityRecord.from_dict(saved["distance"]).to_quantity()
    assert float(puw.get_value(restored, to_unit="nm")) == pytest.approx(0.12)
    original["ligand_ids"].append("mutated")
    original["nested"]["values"][0] = 99
    assert saved["ligand_ids"] == identities
    assert saved["nested"]["values"] == [1, 2]


@pytest.mark.parametrize("format", ["json", "yaml"])
def test_native_saved_consensus_preserves_original_text_and_physical_units(
    tmp_path, format
):
    import molsysmt as msm

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.io import load_json, load_yaml, to_json, to_yaml
    from pharmacophoremt.modeler import from_aligned_ligand_cliques
    from tests.test_pose_evaluation import system

    first = system("CCC", [[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0]])
    second = msm.structure.translate(first, translation="[.04,0,0] nm", in_place=False)
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        result = from_aligned_ligand_cliques(
            [
                dict(ligand_id="a", molecular_system=first),
                dict(ligand_id="b", molecular_system=second),
            ],
            features=["hydrophobicity"],
            distance_tolerance=".10 nm",
            radius=".06 nm",
        )
        assert len(result["models"]) == 1
        model = result["models"][0]
        model.name = np.str_("1 nm")
        model.description = np.str_("2 m")
        literals = ["a", "b", "nm", "s", "1 nm", "2 m", "1 ps", "yes", "null"]
        values = np.array([1, 2])
        model.metadata["review"] = dict(
            literals=tuple(np.str_(text) for text in literals),
            distance=puw.quantity(0.12, "nm"),
            values=values,
        )
        model.interaction_sites[0].metadata["review"] = dict(
            text=np.str_("1 ps"), distance=puw.quantity(0.04, "nm")
        )
        writer, reader = {"json": (to_json, load_json), "yaml": (to_yaml, load_yaml)}[
            format
        ]
        path = tmp_path / ("original-identities." + format)
        writer(model, path)
        assert "!!python" not in path.read_text()
        assert type(model.metadata["review"]["literals"][0]) is np.str_
        assert model.metadata["review"]["values"] is values
        values[0] = 99  # The saved result must already be detached from this input.

    with puw.context(standard_units=["angstrom", "ps", "radians"]):
        restored = reader(path)
        assert type(restored.name) is str and restored.name == "1 nm"
        assert type(restored.description) is str and restored.description == "2 m"
        assert restored.metadata["hypothesis"]["joint_ligand_ids"] == ["a", "b"]
        assert [item["ligand_id"] for item in restored.metadata["sources"]] == [
            "a",
            "b",
        ]
        for member in restored.interaction_sites[0].metadata["members"]:
            assert type(member["ligand_id"]) is str and member["ligand_id"] in {
                "a",
                "b",
            }
        review = restored.metadata["review"]
        assert review["literals"] == literals
        assert all(type(text) is str for text in review["literals"])
        assert review["values"] == [1, 2]
        distance = puw.QuantityRecord.from_dict(review["distance"]).to_quantity()
        assert float(puw.get_value(distance, to_unit="nm")) == pytest.approx(0.12)
        site = restored.interaction_sites[0]
        assert type(site.metadata["review"]["text"]) is str
        assert site.metadata["review"]["text"] == "1 ps"
        distance = puw.QuantityRecord.from_dict(
            site.metadata["review"]["distance"]
        ).to_quantity()
        assert float(puw.get_value(distance, to_unit="nm")) == pytest.approx(0.04)
        np.testing.assert_allclose(
            puw.get_value(site.center, to_unit="nm"), [0.17, 0, 0], atol=1e-14
        )
        assert float(puw.get_value(site.radius, to_unit="nm")) == pytest.approx(0.06)


def test_catalog_codes_and_exception_reconstruction():
    assert PACKAGE_ROOT.name == "pharmacophoremt"
    assert CODES["PHMT-E001"]["message"].startswith("Optional library")
    error = LibraryNotFoundError(library="molsysviewer")
    assert "pip install molsysviewer" in str(error)
    reconstructed = type(error)(str(error), code=error.code, extra=error.extra)
    assert str(reconstructed) == str(error)


@pytest.mark.parametrize(
    "group,key,extra,expected",
    [
        (
            "exceptions",
            "InvalidInteractionSiteError",
            {"reason": "fixture"},
            "Invalid interaction site configuration: fixture.",
        ),
        (
            "exceptions",
            "LibraryNotFoundError",
            {"library": "viewer", "pypi": "viewer", "conda": "viewer"},
            "pip install viewer",
        ),
        (
            "warnings",
            "UnitConsistencyWarning",
            {"interaction_site": "fixture", "expected_unit": "nm"},
            "Coordinates should be nm.",
        ),
    ],
)
def test_catalog_authored_messages_render_through_smonitor(group, key, extra, expected):
    from smonitor.integrations import emit_from_catalog

    event = emit_from_catalog(
        CATALOG[group][key], package_root=PACKAGE_ROOT, extra=extra
    )
    assert expected in event["message"]
    assert event["code"] == CATALOG[group][key]["code"]


def test_show_reports_missing_optional_viewer_before_import(monkeypatch):
    from depdigest.core import checker

    monkeypatch.setattr(
        checker, "is_installed", lambda module: module != "molsysviewer"
    )
    with pytest.raises(LibraryNotFoundError) as caught:
        Pharmacophore().show()
    assert caught.value.code == "PHMT-E001"
    assert "pip install molsysviewer" in str(caught.value)


def test_nondefault_units_survive_package_import_and_distance_calculation():
    script = """
import pyunitwizard as puw
import numpy as np
puw.configure.set_default_form("pint")
puw.configure.set_default_parser("pint")
puw.configure.set_standard_units(["angstrom", "ps", "radian"], provenance="test")
import pharmacophoremt as phmt
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
model = phmt.Pharmacophore()
for center in ("[0,0,0] nm", "[1,0,0] nm"):
    model.add_interaction_site(InteractionSite(Sphere(center, "0.1 nm"), "hydrophobicity"))
assert float(puw.get_value(model.interaction_sites[1].center, to_unit="angstrom")[0]) == 10
assert np.isclose(float(puw.get_value(model.get_distance_matrix(), to_unit="nm")[0,1]), 1)
assert "angstrom" in str(puw.get_unit(model.interaction_sites[1].center))
"""
    result = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
