"""Independent geometry and attribution controls for exclusion-site construction."""

import json
from copy import deepcopy

import ackredit
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import Pharmacophore
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt._private.smonitor.warnings import AckreditTrackingWarning
from pharmacophoremt.io import load_json, to_json
from pharmacophoremt.modeler import (
    from_ligand,
    get_excluded_volume_sites,
    get_features,
)
from pharmacophoremt.screening import PoseEvaluator
from tests.test_attribution import run_reader
from tests.test_pose_evaluation import system


def heavy_inventory():
    return get_features(system(), selection=[3, 4, 5], features=["included volume"])


def test_cached_builder_requires_no_molecular_access_and_retains_source_maps(
    monkeypatch,
):
    inventory = heavy_inventory()

    def forbidden(*args, **kwargs):
        raise AssertionError("cached site construction must not read molecular data")

    monkeypatch.setattr(msm, "get", forbidden)
    monkeypatch.setattr(msm, "select", forbidden)
    result = get_excluded_volume_sites(inventory, radius="0.10 nm")
    sites, report = result["interaction_sites"], result["report"]
    assert report["n_sites"] == len(sites) == 3
    assert report["selected_atom_indices"] == [3, 4, 5]
    assert report["structure_index"] == inventory["structure_index"] == 0
    assert report["software"] == {
        "pharmacophoremt": phmt.__version__,
        "numpy": np.__version__,
        "pyunitwizard": puw.__version__,
    }
    assert [s.metadata["atom_indices"] for s in sites] == [[3], [4], [5]]
    assert all(s.features == ["excluded volume"] and s.weight == 0 for s in sites)
    assert all(s.shape_name == "sphere" and s.essential for s in sites)
    assert report["policy"]["site_indices"] == "local_to_returned_list"
    assert not report["policy"]["physical_radius_assignment"]
    json.dumps(report, allow_nan=False)


def test_inventory_sites_and_report_have_independent_geometry_and_metadata():
    inventory = heavy_inventory()
    original = deepcopy(inventory)
    result = get_excluded_volume_sites(inventory, radius="0.10 nm")
    report = deepcopy(result["report"])
    centers = [
        puw.get_value(s.center, to_unit="nm").copy()
        for s in result["interaction_sites"]
    ]
    inventory["features"][0]["center"][0] = puw.quantity(99, "nm")
    inventory["selected_atom_indices"].clear()
    inventory["features"].clear()
    assert result["report"] == report
    for center, site in zip(centers, result["interaction_sites"]):
        np.testing.assert_array_equal(puw.get_value(site.center, to_unit="nm"), center)
    result["interaction_sites"][0].shape.radius = puw.quantity(3, "nm")
    result["interaction_sites"][0].metadata["atom_indices"].clear()
    assert result["report"] == report
    rebuilt = get_excluded_volume_sites(original, radius="1 angstrom")
    assert rebuilt["report"]["n_sites"] == 3


@pytest.mark.parametrize("radius", [0.1, "0 nm", "-1 nm", "nan nm", "1 ps", "[1,2] nm"])
def test_invalid_or_unitless_uniform_radius_is_rejected(radius):
    with pytest.raises(ArgumentError):
        get_excluded_volume_sites(heavy_inventory(), radius=radius)


@pytest.mark.parametrize(
    "problem", ["missing", "chemical", "grouped", "duplicate", "direction"]
)
def test_missing_or_nonatomic_volume_inventory_is_rejected(problem):
    inventory = heavy_inventory()
    if problem == "missing":
        inventory = None
    elif problem == "chemical":
        inventory["features"][0]["kind"] = "hydrophobicity"
    elif problem == "grouped":
        inventory["features"][0]["atom_indices"] = [3, 4]
    elif problem == "duplicate":
        inventory["features"].append(deepcopy(inventory["features"][0]))
    else:
        inventory["features"][0]["direction"] = puw.quantity([1, 0, 0], "dimensionless")
    with pytest.raises(ArgumentError):
        get_excluded_volume_sites(inventory, radius="0.10 nm")


def test_empty_declared_inventory_returns_empty_construction_not_valid_query():
    inventory = heavy_inventory()
    inventory["features"].clear()
    result = get_excluded_volume_sites(inventory, radius="0.10 nm")
    assert result["interaction_sites"] == [] and result["report"]["n_sites"] == 0
    excluded_only = Pharmacophore()
    for site in get_excluded_volume_sites(heavy_inventory(), radius="0.10 nm")[
        "interaction_sites"
    ]:
        excluded_only.add_interaction_site(site)
    with pytest.raises(ArgumentError, match="positive total weight"):
        PoseEvaluator(excluded_only)


def boundary_query():
    ligand = system(smiles="CCC", coordinates=[[0, 0, 0], [0.15, 0, 0], [0.3, 0, 0]])
    receptor = system(smiles="[He]", coordinates=[[0, 0, 0]])
    query = from_ligand(ligand, features=["hydrophobicity"], radius="0.5 nm")
    result = get_excluded_volume_sites(
        get_features(receptor, features=["included volume"]), radius="0.1 nm"
    )
    for site in result["interaction_sites"]:
        query.add_interaction_site(site)
    return ligand, query, result


@pytest.mark.parametrize(
    "displacement,expected",
    [(0.09, "not_matched"), (0.1, "matched"), (0.11, "matched")],
)
def test_inside_boundary_and_outside_veto_without_changing_positive_fit(
    displacement, expected
):
    ligand, query, _ = boundary_query()
    moved = msm.structure.translate(
        ligand, translation=puw.quantity([[[displacement, 0, 0]]], "nm"), in_place=False
    )
    outcome = PoseEvaluator(query).evaluate(moved)
    assert outcome["fit_value"] == 1 and len(outcome["assignments"]) == 1
    assert outcome["status"] == expected
    assert outcome["excluded_volume_clashes"] == (
        [{"site_index": 1, "atom_index": 0}] if displacement < 0.1 else []
    )


def test_geometry_units_query_codec_and_source_report_roundtrip(tmp_path):
    inventory = heavy_inventory()
    baseline = get_excluded_volume_sites(inventory, radius="0.1 nm")
    with puw.context(standard_units=["pm", "fs"]):
        equivalent = get_excluded_volume_sites(inventory, radius="1 angstrom")
    for first, second in zip(
        baseline["interaction_sites"], equivalent["interaction_sites"]
    ):
        np.testing.assert_allclose(
            puw.get_value(first.center, to_unit="nm"),
            puw.get_value(second.center, to_unit="nm"),
        )
        assert puw.get_value(second.radius, to_unit="nm") == pytest.approx(0.1)
    ligand, query, construction = boundary_query()
    query.metadata["exclusion_construction"] = construction["report"]
    path = tmp_path / "query.json"
    to_json(query, str(path))
    loaded = load_json(str(path))
    assert loaded.metadata == query.metadata
    assert loaded.interaction_sites[-1].metadata == query.interaction_sites[-1].metadata
    assert PoseEvaluator(loaded).evaluate(ligand)["excluded_volume_clashes"] == [
        {"site_index": 1, "atom_index": 0}
    ]


def test_real_attribution_reused_empty_and_cached_origin_are_distinct():
    with ackredit.session("cached origin extraction"), phmt.attribution(True):
        inventory = heavy_inventory()
    original = deepcopy(inventory["attribution"])
    results = []
    with ackredit.session("exclusion construction reuse"), phmt.attribution(True):
        with ackredit.capture("two constructions and empty result") as outer:
            for _ in range(2):
                results.append(get_excluded_volume_sites(inventory, radius=".1 nm"))
            empty = deepcopy(inventory)
            empty["features"].clear()
            results.append(get_excluded_volume_sites(empty, radius=".1 nm"))
    for result in results:
        assert result["attribution"]["status"] == "captured"
        assert result["report"]["source_inventory"]["attribution"] == original
        references = result["attribution"]["references"]
        assert references["items"]
        assert not any(
            "molsysmt" in use["context"].get("software", "")
            for use in references["uses"]
        )
        assert not any(
            item.get("doi") == "10.3390/molecules26237201"
            for item in references["items"]
        )
        json.dumps(result["report"], allow_nan=False)
    # Reused identical uses may be deduplicated by the provider. Each result,
    # including empty construction, must still retain the complete bibliography.
    expected_ids = {item["id"] for item in outer.attribution.to_dict()["items"]}
    assert expected_ids
    assert all(
        {item["id"] for item in result["attribution"]["references"]["items"]}
        == expected_ids
        for result in results
    )
    assert inventory["attribution"] == original


def test_optional_attribution_absence_and_failure_preserve_construction(monkeypatch):
    from pharmacophoremt import _ackredit

    inventory = heavy_inventory()
    expected = get_excluded_volume_sites(inventory, radius=".1 nm")["report"]
    with phmt.attribution(True):
        monkeypatch.setattr(_ackredit, "backend", lambda: None)
        absent = get_excluded_volume_sites(inventory, radius=".1 nm")
        assert absent["attribution"]["status"] == "unavailable"

        def broken():
            raise RuntimeError("provider failed")

        monkeypatch.setattr(_ackredit, "backend", broken)
        with pytest.warns(AckreditTrackingWarning):
            failed = get_excluded_volume_sites(inventory, radius=".1 nm")
    assert absent["report"] == failed["report"] == expected
    assert failed["attribution"]["status"] == "failed"
    assert len(failed["interaction_sites"]) == 3


def test_fresh_process_import_is_lazy_and_genuine_provider_absence_is_supported():
    run_reader("""
import sys, importlib.abc
class NoAckredit(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] == 'ackredit':
            raise ModuleNotFoundError('absent provider', name='ackredit')
sys.meta_path.insert(0, NoAckredit())
import pharmacophoremt as phmt
assert 'ackredit' not in sys.modules
from tests.test_pose_evaluation import system
inventory = phmt.modeler.get_features(system(), selection=[3,4,5], features=['included volume'])
plain = phmt.modeler.get_excluded_volume_sites(inventory, radius='.1 nm')
assert 'ackredit' not in sys.modules
with phmt.attribution(True):
    result = phmt.modeler.get_excluded_volume_sites(inventory, radius='.1 nm')
assert result['report'] == plain['report']
assert result['attribution']['status'] == 'unavailable'
assert result['attribution']['host_references']
assert 'ackredit' not in sys.modules
""")


def test_detached_reader_retains_original_versions_without_new_credits(tmp_path):
    with ackredit.session("construction to save"), phmt.attribution(True):
        result = get_excluded_volume_sites(heavy_inventory(), radius=".1 nm")
    path = tmp_path / "construction-bibliography.json"
    path.write_text(json.dumps(result["attribution"]["references"]))
    run_reader(
        """
import json, sys, importlib.abc
class NoScience(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'rdkit', 'scipy', 'molsysmt', 'pharmacophoremt'}:
            raise ModuleNotFoundError('scientific engine unavailable', name=fullname)
sys.meta_path.insert(0, NoScience())
import ackredit
original = json.load(open(sys.argv[1]))
with ackredit.session('reader'):
    saved = ackredit.Attribution.from_dict(original)
    assert saved.to_dict() == original
    assert saved.report(format='bibtex')
    assert ackredit.get_used_items() == {}
assert not {'rdkit', 'scipy', 'molsysmt', 'pharmacophoremt'} & set(sys.modules)
""",
        path,
    )
