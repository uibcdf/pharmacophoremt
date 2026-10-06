"""Joint classical hypotheses, identity-aware reuse and independent ownership."""

import json
import warnings
from copy import deepcopy

import ackredit as ack
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from devtools.interaction_collection_cases import build_case, observe
from pharmacophoremt import _ackredit
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt._private.smonitor.warnings import AckreditTrackingWarning
from pharmacophoremt.io import load_json, to_json
from pharmacophoremt.modeler import (
    compose_pharmacophores,
    from_interaction_collection,
    from_interactions,
    get_excluded_volume_sites,
    get_features,
)
from pharmacophoremt.pharmacophore import Pharmacophore
from pharmacophoremt.screening import PoseEvaluator
from tests.test_attribution import run_reader
from tests.test_ionic_interactions import replace_records


@pytest.fixture(scope="module")
def case():
    source, ligand, partner = build_case()
    return source, ligand, partner, observe(source, ligand, partner)


def components(case):
    source, ligand, _, analyses = case
    return {
        label: from_interactions(source, observed, ligand, radius=".02 nm")
        for label, observed in analyses.items()
    }


def test_all_families_reuse_shared_constraints_without_inflating_weight(case):
    source, ligand, _, analyses = case
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    model = from_interaction_collection(source, analyses, ligand, radius=".02 nm")
    assert model.n_interaction_sites == 9
    assert sum(site.weight for site in model.interaction_sites) == 9
    assert {site.feature_name for site in model.interaction_sites} == {
        "hydrophobicity",
        "hb donor",
        "positive charge",
        "aromatic ring",
    }
    rows = model.metadata["site_map"]
    assert sum(row["action"] == "reused" for row in rows) == 2
    for feature, expected_labels in [
        ("positive charge", {"ionic", "cation_pi"}),
        ("aromatic ring", {"pi_prolif", "pi_molstar"}),
    ]:
        site = next(
            site for site in model.interaction_sites if site.feature_name == feature
        )
        assert {
            row["component"] for row in site.metadata["observations"]
        } == expected_labels
        assert len(site.metadata["composition_contributions"]) == 2
        # Relation IDs are local to each independent native analysis.
        assert {row["relation_index"] for row in site.metadata["observations"]} == {0}
    empty = next(
        row for row in model.metadata["components"] if row["label"] == "ionic_empty"
    )
    assert empty["n_sites"] == 0 and empty["metadata"][
        "evaluated_structure_indices"
    ] == [0]
    result = PoseEvaluator(model).evaluate(source, selection=ligand)
    assert result["status"] == "matched" and result["fit_value"] == 1
    moved = msm.structure.translate(
        source, selection=ligand, translation="[1,0,0] nm", in_place=False
    )
    result = PoseEvaluator(model).evaluate(moved, selection=ligand)
    assert result["status"] == "not_matched" and result["fit_value"] == 0
    reversed_h = msm.structure.translate(
        source, selection=[7], translation="[-.2,0,0] nm", in_place=False
    )
    result = PoseEvaluator(model).evaluate(reversed_h, selection=ligand)
    assert result["status"] == "not_matched" and result["fit_value"] == pytest.approx(
        8 / 9
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )


def test_keep_policy_preserves_independent_constraints_and_one_to_one_semantics(case):
    source, ligand, _, analyses = case
    kept = from_interaction_collection(
        source, analyses, ligand, duplicate_policy="keep"
    )
    assert kept.n_interaction_sites == 11
    assert all(row["action"] == "added" for row in kept.metadata["site_map"])
    result = PoseEvaluator(kept).evaluate(source, selection=ligand)
    assert result["status"] == "not_matched" and result["fit_value"] == pytest.approx(
        9 / 11
    )
    assert len(result["missing_essential_sites"]) == 2


def test_compose_is_independent_and_calls_no_molecular_operations(case, monkeypatch):
    pieces = components(case)

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "cached model composition must not access molecular systems"
        )

    for name in ("get", "select", "convert"):
        monkeypatch.setattr(msm, name, forbidden)
    model = compose_pharmacophores(pieces, duplicate_policy="same_participant")
    assert model.n_interaction_sites == 9
    original = pieces["ionic"].interaction_sites[0]
    original.weight = 7
    original.metadata["observations"].clear()
    pieces["ionic"].metadata["parameters"].clear()
    charged = next(
        site
        for site in model.interaction_sites
        if site.feature_name == "positive charge"
    )
    assert charged.weight == 1 and len(charged.metadata["observations"]) == 2
    charged.metadata["composition_contributions"][0]["metadata"]["observations"].clear()
    snapshot = next(
        row for row in model.metadata["components"] if row["label"] == "ionic"
    )
    assert len(snapshot["metadata"]["parameters"]) > 0
    assert pieces["cation_pi"].interaction_sites[0].weight == 1


def test_collection_consumes_public_adapter_and_composition(case, monkeypatch):
    import pharmacophoremt.modeler.interaction_collection as module

    source, ligand, _, analyses = case
    adapter, composer = module.from_interactions, module.compose_pharmacophores
    calls = []

    def convert(*args, **kwargs):
        calls.append("convert")
        return adapter(*args, **kwargs)

    def compose(*args, **kwargs):
        calls.append("compose")
        return composer(*args, **kwargs)

    def forbidden(*args, **kwargs):
        raise AssertionError("cached workflow cannot rerun detection")

    monkeypatch.setattr(module, "from_interactions", convert)
    monkeypatch.setattr(module, "compose_pharmacophores", compose)
    monkeypatch.setattr(msm.interactions.pi_pi, "get_pi_pi_interactions", forbidden)
    from_interaction_collection(source, analyses, ligand)
    assert calls == ["convert"] * 7 + ["compose"]


@pytest.mark.parametrize(
    "property", ["radius", "center", "weight", "essential", "normal", "charge"]
)
def test_conflicting_constraints_raise_instead_of_averaging(case, property):
    pieces = components(case)
    original = pieces["pi_prolif"] if property == "normal" else pieces["ionic"]
    changed = deepcopy(original)
    site = changed.interaction_sites[0]
    if property == "radius":
        site.shape.radius = puw.quantity(0.04, "nm")
    elif property == "center":
        site.shape.center = puw.quantity([1, 0, 0], "nm")
    elif property == "normal":
        site.shape.normal = puw.quantity([1, 0, 0], "dimensionless")
    elif property == "charge":
        site.metadata["charge"] = puw.QuantityRecord.from_quantity(
            puw.quantity(2.0, "e")
        ).to_dict()
    else:
        setattr(site, property, 2 if property == "weight" else False)
    with pytest.raises(ArgumentError, match="conflicting constraints"):
        compose_pharmacophores(
            {"first": original, "changed": changed}, duplicate_policy="same_participant"
        )
    assert (
        compose_pharmacophores(
            {"first": original, "changed": changed}
        ).n_interaction_sites
        == 2
    )


def test_unit_conversion_and_plane_sign_are_representation_equivalence(case):
    pieces = components(case)
    first = pieces["pi_prolif"]
    equivalent = deepcopy(first)
    site = equivalent.interaction_sites[0]
    site.shape.center = puw.quantity(
        puw.get_value(site.center, to_unit="angstrom"), "angstrom"
    )
    site.shape.radius = puw.quantity(puw.get_value(site.radius, to_unit="pm"), "pm")
    site.shape.normal = -site.shape.normal
    assert (
        compose_pharmacophores(
            {"first": first, "equivalent": equivalent},
            duplicate_policy="same_participant",
        ).n_interaction_sites
        == 1
    )


def test_coincident_distinct_participants_are_not_spatially_clustered(case):
    pieces = components(case)
    hydro = deepcopy(pieces["hydrophobic"])
    hydro.interaction_sites[1].shape.center = deepcopy(
        hydro.interaction_sites[0].center
    )
    assert (
        compose_pharmacophores(
            {"hydro": hydro}, duplicate_policy="same_participant"
        ).n_interaction_sites
        == 6
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("source_id", "other-source"),
        ("structure_index", 3),
        ("ligand_atom_indices", [0]),
        ("source_atom_indices", list(range(20, 40))),
    ],
)
def test_incompatible_cached_model_sources_are_rejected(case, field, value):
    original = components(case)["ionic"]
    other = deepcopy(original)
    other.metadata[field] = value
    with pytest.raises(ArgumentError):
        compose_pharmacophores(
            {"a": original, "b": other}, duplicate_policy="same_participant"
        )


@pytest.mark.parametrize("failure", ["state", "maps", "uncovered", "profile"])
def test_any_collection_failure_propagates_without_partial_model(case, failure):
    source, ligand, _, analyses = case
    collection = {
        label: replace_records(observed) for label, observed in analyses.items()
    }
    original = collection["pi_prolif"]
    parameters = deepcopy(original.parameters)
    options = {}
    if failure == "state":
        parameters["chemical_state_index"] = 1
    elif failure == "maps":
        options["atom_source_indices"] = list(range(20, 40))
    elif failure == "profile":
        parameters["profile"] = "unknown"
    replacement = replace_records(original, parameters=parameters, **options)
    if failure == "uncovered":
        replacement = replacement.invalidate_structures([0])
    collection["pi_prolif"] = replacement
    with pytest.raises(ArgumentError):
        from_interaction_collection(source, collection, ligand)


def test_empty_analyses_remain_distinct_from_valid_queries(case):
    source, ligand, _, analyses = case
    empty = from_interaction_collection(
        source, {"empty": analyses["ionic_empty"]}, ligand
    )
    assert (
        empty.n_interaction_sites == 0
        and empty.metadata["components"][0]["n_sites"] == 0
    )
    with pytest.raises(ArgumentError, match="positive total weight"):
        PoseEvaluator(empty).evaluate(source, selection=ligand)


@pytest.mark.parametrize("input", [None, {}, [], {"": Pharmacophore()}, {"bad": 3}])
def test_invalid_named_models_are_rejected(input):
    with pytest.raises(ArgumentError):
        compose_pharmacophores(input)


def test_generic_composition_preserves_exclusions_with_independent_veto(case):
    source, ligand, _, analyses = case
    query = from_interaction_collection(source, analyses, ligand, radius=".4 nm")
    inventory = get_features(source, selection=[16], features=["included volume"])
    result = get_excluded_volume_sites(inventory, radius=".05 nm")
    excluded = Pharmacophore(ref_struct=0)
    for site in result["interaction_sites"]:
        excluded.add_interaction_site(site)
    joint = compose_pharmacophores({"positive": query, "excluded": excluded})
    assert (
        PoseEvaluator(joint).evaluate(source, selection=ligand)["status"] == "matched"
    )
    collision = msm.structure.translate(
        source, selection=[6], translation="[.25,0,0] nm", in_place=False
    )
    result = PoseEvaluator(joint).evaluate(collision, selection=ligand)
    assert result["status"] == "not_matched" and result["fit_value"] == 1
    assert result["excluded_volume_clashes"] == [{"site_index": 9, "atom_index": 6}]


def test_saved_components_compose_with_nondefault_units_and_detached_reader(
    case, tmp_path
):
    source, ligand, _, analyses = case
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        model = from_interaction_collection(source, analyses, ligand, radius="20 pm")
        path = tmp_path / "composed.json"
        to_json(model, path)
        restored = load_json(path)
        assert restored.metadata == model.metadata
        assert [site.metadata for site in restored.interaction_sites] == [
            site.metadata for site in model.interaction_sites
        ]
        assert (
            PoseEvaluator(restored).evaluate(source, selection=ligand)["fit_value"] == 1
        )
        cached = components(case)
        paths = {}
        for label, component in cached.items():
            target = tmp_path / (label + ".json")
            to_json(component, target)
            paths[label] = str(target)
        assert (
            compose_pharmacophores(
                {key: load_json(value) for key, value in paths.items()},
                duplicate_policy="same_participant",
            ).n_interaction_sites
            == 9
        )
    run_reader(
        """
import json, sys, importlib.abc
class NoAck(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] == 'ackredit':
            raise ModuleNotFoundError('controlled absence', name=fullname)
sys.meta_path.insert(0, NoAck())
from pharmacophoremt.io import load_json
from pharmacophoremt.modeler import compose_pharmacophores
from pharmacophoremt import attribution
paths = json.loads(sys.argv[1])
with attribution():
    result = compose_pharmacophores({label: load_json(path) for label, path in paths.items()}, duplicate_policy='same_participant')
assert result.n_interaction_sites == 9
assert result.metadata['attribution']['status'] == 'unavailable'
""",
        json.dumps(paths),
    )


def test_actual_capture_preserves_reuse_without_rerunning_detection(case, tmp_path):
    source, ligand, _, analyses = case
    with ack.session("composition"):
        results = []
        for _ in range(2):
            with ack.capture("compose cached") as run:
                with phmt.attribution():
                    result = from_interaction_collection(source, analyses, ligand)
            uses = run.attribution.to_dict()["uses"]
            assert any("from_interaction_collection" in use["used_by"] for use in uses)
            assert not any(
                "get_pi_pi_interactions" in use["used_by"]
                or "get_ionic_interactions" in use["used_by"]
                for use in uses
            )
            results.append(result)
        assert results[0].metadata["attribution"]["references"]["items"]
        results[0].metadata["components"][0]["metadata"].clear()
        assert results[1].metadata["components"][0]["metadata"]
        before = ack.get_attribution().to_dict()
        path = tmp_path / "credited.json"
        to_json(results[1], path)
        assert load_json(path).metadata == results[1].metadata
        assert ack.get_attribution().to_dict() == before


def test_optional_tracking_failure_preserves_completed_composition(case, monkeypatch):
    pieces = components(case)

    def broken():
        raise RuntimeError("provider failed")

    monkeypatch.setattr(_ackredit, "backend", broken)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with phmt.attribution():
            result = compose_pharmacophores(pieces, duplicate_policy="same_participant")
    assert (
        result.n_interaction_sites == 9
        and result.metadata["attribution"]["status"] == "failed"
    )
    assert any(isinstance(w.message, AckreditTrackingWarning) for w in caught)


def test_genuine_ackredit_absence_and_lazy_import_support_live_collection():
    run_reader(
        """
import sys, importlib.abc
class NoAck(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] == 'ackredit':
            raise ModuleNotFoundError('controlled absence', name=fullname)
sys.meta_path.insert(0, NoAck())
from devtools.interaction_collection_cases import build_case, observe
import pharmacophoremt as phmt
from pharmacophoremt.modeler import from_interaction_collection
from pharmacophoremt.screening import PoseEvaluator
assert 'ackredit' not in sys.modules
source, ligand, partner = build_case()
analyses = observe(source, ligand, partner)
with phmt.attribution():
    result = from_interaction_collection(source, analyses, ligand)
assert result.n_interaction_sites == 9
assert PoseEvaluator(result).evaluate(source, selection=ligand)['status'] == 'matched'
assert result.metadata['attribution']['status'] == 'unavailable'
""",
    )


def test_high_level_dispatcher_consumes_the_same_collection(case):
    source, ligand, _, analyses = case
    model = phmt.model(
        source,
        method="interaction-collection",
        interaction_collection=analyses,
        ligand_selection=ligand,
    )
    assert model.n_interaction_sites == 9
    with pytest.raises(ArgumentError):
        phmt.model(
            source, method="interaction-collection", interaction_collection=analyses
        )
