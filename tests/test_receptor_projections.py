"""Independent hypothesis controls; cached construction has no molecular kernel."""

import json
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest
from argdigest.core.errors import DigestNotDigestedWarning, UnknownArgumentError

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.io import load_json, to_json
from pharmacophoremt.modeler import (
    StructureBasedModeler,
    from_receptor_projections,
    get_features,
)
from pharmacophoremt.screening import PoseEvaluator
from tests.test_pose_evaluation import system


def control_inventory():
    kinds = [
        "hydrophobicity",
        "hb donor",
        "hb acceptor",
        "aromatic ring",
        "positive charge",
        "negative charge",
    ]
    records = []
    for i, kind in enumerate(kinds):
        atoms = [3, 6, 7] if kind == "aromatic ring" else [i]
        records.append(
            dict(
                kind=kind,
                atom_indices=atoms,
                geometry_atom_indices=[1, 8] if kind == "hb donor" else atoms.copy(),
                center=puw.quantity([i * 10, 0, 0], "angstrom"),
                direction=puw.quantity([1, 0, 0], "dimensionless")
                if kind == "hb donor"
                else None,
                normal=puw.quantity([0, 0, 1], "dimensionless")
                if kind == "aromatic ring"
                else None,
                charge=puw.quantity(
                    1 if kind == "positive charge" else -1, "elementary_charge"
                )
                if "charge" in kind
                else None,
            )
        )
    return dict(
        definition="classical_atomic_formal@1",
        features=records,
        selected_atom_indices=list(range(9)),
        structure_index=2,
        chemical_state=1,
        recognition={"control": "synthetic cached geometry, not molecular recognition"},
        attribution={"status": "control", "references": ["cached-only"]},
    )


def control_specs():
    directions = [[4, 0, 0], [0, 2, 0], [0, 0, 3], [0, 0, -2], [0, 5, 0], [0, 1, 0]]
    distances = [
        "3.5 angstrom",
        "280 pm",
        "0.28 nm",
        "4.5 angstrom",
        "400 pm",
        "0.4 nm",
    ]
    specs = [
        dict(
            feature_index=i,
            projection_direction=d,
            distance=distance,
            label=f"declared control {i}",
        )
        for i, (d, distance) in enumerate(zip(directions, distances))
    ]
    specs[2]["target_direction"] = [0, -2, 0]
    specs[3]["target_normal"] = [1, 0, 0]
    specs[0]["evidence"] = {"producer": "manual hypothesis", "choices": ["outward x"]}
    return specs


def forbid_molecular_calls(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("cached receptor hypotheses must not access molecular data")

    for name in ("get", "select", "convert", "extract", "copy", "set"):
        monkeypatch.setattr(msm, name, forbidden)
    for owner, name in (
        (msm.physchem, "get_hbond_sites"),
        (msm.structure, "get_center"),
        (msm.structure, "get_least_squares_plane"),
    ):
        monkeypatch.setattr(owner, name, forbidden)


@pytest.mark.parametrize("route", ["tool", "class", "dispatcher"])
def test_complementary_numerical_controls_and_no_molecular_operations(
    monkeypatch, route
):
    inventory, specs = control_inventory(), control_specs()
    forbid_molecular_calls(monkeypatch)
    source = object()
    options = dict(
        feature_inventory=inventory,
        projection_specs=specs,
        radius="20 pm",
        name="explicit control",
    )
    if route == "tool":
        query = from_receptor_projections(**options)
        assert query.molecular_system is None
    elif route == "class":
        modeler = StructureBasedModeler(source, **options)
        assert modeler.result is None
        query = modeler.build()
        assert modeler.result is query and query.molecular_system is source
    else:
        query = phmt.model(
            source, method="structure-based", structure_indices=[2], **options
        )
        assert query.molecular_system is source
    assert query.name == "explicit control" and query.ref_struct == 2
    assert query.n_interaction_sites == 6
    assert [site.feature_name for site in query.interaction_sites] == [
        "hydrophobicity",
        "hb acceptor",
        "hb donor",
        "aromatic ring",
        "negative charge",
        "positive charge",
    ]
    expected = [
        [0.35, 0, 0],
        [1, 0.28, 0],
        [2, 0, 0.28],
        [3, 0, -0.45],
        [4, 0.4, 0],
        [5, 0.4, 0],
    ]
    for i, (site, center) in enumerate(zip(query.interaction_sites, expected)):
        np.testing.assert_allclose(
            puw.get_value(site.center, to_unit="nm"), center, atol=1e-14
        )
        assert puw.get_value(site.radius, to_unit="nm") == pytest.approx(0.02)
        assert site.essential and site.weight == 1
        assert site.metadata["source_feature_index"] == i
    assert query.interaction_sites[1].shape_name == "sphere"
    np.testing.assert_array_equal(
        puw.get_value(query.interaction_sites[2].shape.direction), [0, -1, 0]
    )
    np.testing.assert_array_equal(
        puw.get_value(query.interaction_sites[3].shape.normal), [1, 0, 0]
    )
    assert query.interaction_sites[3].shape_name == "disk"
    assert query.metadata["omitted_feature_indices"] == []
    assert query.metadata["source_attribution"] == inventory["attribution"]
    assert not query.metadata["policy"]["molecular_geometry_inference"]
    json.dumps(query.metadata, allow_nan=False)


def test_declared_omissions_order_empty_and_separate_alternatives():
    inventory, specs = control_inventory(), control_specs()
    query = from_receptor_projections(inventory, projection_specs=[specs[4], specs[0]])
    assert [row["feature_index"] for row in query.metadata["sites"]] == [4, 0]
    assert query.metadata["omitted_feature_indices"] == [1, 2, 3, 5]
    first = from_receptor_projections(inventory, projection_specs=[specs[3]])
    specs[3]["projection_direction"] = [0, 0, 1]
    second = from_receptor_projections(inventory, projection_specs=[specs[3]])
    np.testing.assert_allclose(
        puw.get_value(first.interaction_sites[0].center), [3, 0, -0.45]
    )
    np.testing.assert_allclose(
        puw.get_value(second.interaction_sites[0].center), [3, 0, 0.45]
    )
    empty = from_receptor_projections(inventory, projection_specs=[])
    assert empty.n_interaction_sites == 0 and empty.metadata[
        "omitted_feature_indices"
    ] == list(range(6))
    with pytest.raises(ArgumentError):
        PoseEvaluator(empty)
    inventory["features"].clear()
    assert (
        from_receptor_projections(inventory, projection_specs=[]).n_interaction_sites
        == 0
    )


@pytest.mark.parametrize(
    "problem",
    [
        "missing",
        "unknown",
        "negative",
        "boolean",
        "fractional",
        "outside",
        "duplicate",
        "zero",
        "nonfinite",
        "dimensional",
        "distance_unitless",
        "distance_zero",
        "distance_negative",
        "distance_wrong_unit",
        "distance_nonfinite",
        "distance_vector",
        "label",
        "evidence",
        "donor_orientation",
        "ring_orientation",
        "extra_orientation",
        "orientation_zero",
        "orientation_units",
        "list",
        "none",
        "record",
    ],
)
def test_bad_projection_specifications_are_rejected(problem):
    inventory, specs = control_inventory(), control_specs()
    if problem == "missing":
        del specs[0]["projection_direction"]
    elif problem == "unknown":
        specs[0]["typo"] = True
    elif problem in {"negative", "boolean", "fractional", "outside"}:
        specs[0]["feature_index"] = {
            "negative": -1,
            "boolean": True,
            "fractional": 0.5,
            "outside": 100,
        }[problem]
    elif problem == "duplicate":
        specs.append(deepcopy(specs[0]))
    elif problem in {"zero", "nonfinite", "dimensional"}:
        specs[0]["projection_direction"] = {
            "zero": [0, 0, 0],
            "nonfinite": [np.inf, 0, 0],
            "dimensional": puw.quantity([1, 0, 0], "nm"),
        }[problem]
    elif problem.startswith("distance_"):
        specs[0]["distance"] = {
            "distance_unitless": 0.2,
            "distance_zero": "0 nm",
            "distance_negative": "-1 nm",
            "distance_wrong_unit": "1 ps",
            "distance_nonfinite": "nan nm",
            "distance_vector": "[1,2,3] nm",
        }[problem]
    elif problem == "label":
        specs[0]["label"] = " "
    elif problem == "evidence":
        specs[0]["evidence"] = "not a map"
    elif problem == "donor_orientation":
        del specs[2]["target_direction"]
    elif problem == "ring_orientation":
        del specs[3]["target_normal"]
    elif problem == "extra_orientation":
        specs[1]["target_direction"] = [1, 0, 0]
    elif problem == "orientation_zero":
        specs[2]["target_direction"] = [0, 0, 0]
    elif problem == "orientation_units":
        specs[3]["target_normal"] = puw.quantity([1, 0, 0], "nm")
    elif problem == "list":
        specs = {0: specs[0]}
    elif problem == "none":
        specs = None
    else:
        specs = ["not a spec"]
    with pytest.raises(ArgumentError):
        from_receptor_projections(inventory, projection_specs=specs)


@pytest.mark.parametrize(
    "problem", ["none", "definition", "included", "center", "source_atoms"]
)
def test_bad_source_inventory_is_rejected(problem):
    inventory = control_inventory()
    if problem == "none":
        inventory = None
    elif problem == "definition":
        inventory["definition"] = "legacy smarts"
    elif problem == "included":
        inventory["features"][0]["kind"] = "included volume"
    elif problem == "center":
        inventory["features"][0]["center"] = puw.quantity([np.nan, 0, 0], "nm")
    else:
        inventory["features"][0]["atom_indices"] = [100]
    with pytest.raises(ArgumentError):
        from_receptor_projections(inventory, projection_specs=[])


def test_custody_original_choices_json_and_optional_attribution(tmp_path):
    inventory, specs = control_inventory(), control_specs()
    with phmt.attribution():
        query = from_receptor_projections(inventory, projection_specs=specs)
    metadata = deepcopy(query.metadata)
    assert metadata["supplied_projection_specs"][0]["projection_direction"] == [4, 0, 0]
    credits = query.metadata["attribution"]["host_references"]
    assert {item["record"]["title"] for item in credits} >= {
        "PharmacophoreMT",
        "NumPy",
        "PyUnitWizard",
    }
    assert not any(item["record"]["title"] == "MolSysMT" for item in credits)
    query.interaction_sites[0].center[0] = puw.quantity(7, "nm")
    query.interaction_sites[0].metadata["projection"]["evidence"].clear()
    assert query.metadata == metadata
    inventory["features"][1]["center"][0] = puw.quantity(99, "nm")
    specs[0]["projection_direction"][0] = 99
    specs[0]["evidence"]["choices"].clear()
    assert query.metadata == metadata
    np.testing.assert_allclose(
        puw.get_value(query.interaction_sites[1].center), [1, 0.28, 0]
    )
    path = tmp_path / "projection.json"
    to_json(query, file_name=str(path))
    loaded = load_json(str(path))
    assert loaded.metadata == query.metadata and loaded.n_interaction_sites == 6
    for original, saved in zip(query.interaction_sites, loaded.interaction_sites):
        assert original.metadata == saved.metadata
        np.testing.assert_array_equal(
            puw.get_value(original.center), puw.get_value(saved.center)
        )
    # Portable metadata is retained, not treated as a native-quantity decoder.
    with pytest.raises(ArgumentError):
        from_receptor_projections(metadata["source_inventory"], projection_specs=[])


@pytest.mark.parametrize(
    "frames", [[], "all", -1, True, [2, 2], [0], [2, 3], [2.0], [False]]
)
def test_invalid_or_uncached_frames_clear_previous_result(frames):
    modeler = StructureBasedModeler(
        object(),
        feature_inventory=control_inventory(),
        projection_specs=control_specs(),
    )
    assert modeler.build().n_interaction_sites == 6
    with pytest.raises(ArgumentError):
        modeler.build(frames)
    assert modeler.result is None


@pytest.mark.parametrize("skip", [False, True])
def test_incomplete_legacy_calls_fail_before_molecular_access(monkeypatch, skip):
    forbid_molecular_calls(monkeypatch)
    with pytest.raises(ArgumentError):
        StructureBasedModeler(object(), skip_digestion=skip)
    with pytest.raises(ArgumentError):
        StructureBasedModeler(
            object(), feature_inventory=control_inventory(), skip_digestion=skip
        )


@pytest.mark.parametrize(
    "argument", ["selection", "pocket_selection", "pocket_center", "pocket_radius"]
)
def test_retired_pocket_arguments_are_not_silently_ignored(argument):
    if argument == "selection":
        with pytest.raises(UnknownArgumentError):
            phmt.model(object(), method="structure-based", selection="all")
        return
    with pytest.warns(DigestNotDigestedWarning), pytest.raises(UnknownArgumentError):
        phmt.model(object(), method="structure-based", **{argument: "all"})


@pytest.mark.parametrize("selection", ["ligand_selection", "receptor_selection"])
def test_dispatcher_rejects_ignored_selections(selection):
    with pytest.raises(ArgumentError):
        phmt.model(object(), method="structure-based", **{selection: "all"})


def test_native_public_inventory_exclusions_pose_and_preserved_source(monkeypatch):
    source = system(smiles="CCC", coordinates=[[0, 0, 0], [0.15, 0, 0], [0.3, 0, 0]])
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    inventory = get_features(source, features=["hydrophobicity"])
    heavy = get_features(source, features=["included volume"])
    specs = [
        dict(
            feature_index=i,
            projection_direction=[0, 1, 0],
            distance=".35 nm",
            label="analytical translation hypothesis",
        )
        for i in range(len(inventory["features"]))
    ]
    with monkeypatch.context() as cached:
        forbid_molecular_calls(cached)
        modeler = StructureBasedModeler(
            source,
            feature_inventory=inventory,
            projection_specs=specs,
            excluded_volume_inventory=heavy,
            excluded_volume_radius="10 pm",
            radius="20 pm",
        )
        query = modeler.build([0])
        assert modeler.build(0).n_interaction_sites == 4
    assert (
        query.n_interaction_sites == 4
        and sum(s.weight for s in query.interaction_sites) == 1
    )
    assert query.metadata["excluded_volumes"]["global_site_indices"] == [1, 2, 3]
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )
    candidate = system(
        smiles="CCC", coordinates=[[0, 0.35, 0], [0.15, 0.35, 0], [0.3, 0.35, 0]]
    )
    assert PoseEvaluator(query).evaluate(candidate)["status"] == "matched"
    assert PoseEvaluator(query).evaluate(source)["status"] == "not_matched"
    query.interaction_sites[3].shape.radius = puw.quantity(0.5, "nm")
    assert PoseEvaluator(query).evaluate(candidate)["status"] != "matched"


@pytest.mark.parametrize(
    "problem",
    [
        "radius_missing",
        "inventory_missing",
        "frame",
        "state",
        "selection",
        "chemical",
        "radius_invalid",
        "spec",
    ],
)
def test_exclusion_and_projection_failures_do_not_publish_partial_or_stale_model(
    problem,
):
    inventory = control_inventory()
    heavy = deepcopy(inventory)
    heavy["features"] = [
        dict(
            kind="included volume",
            atom_indices=[i],
            geometry_atom_indices=[i],
            center=puw.quantity([i, 0, 0], "nm"),
            direction=None,
            normal=None,
            charge=None,
        )
        for i in range(9)
    ]
    modeler = StructureBasedModeler(
        object(),
        feature_inventory=inventory,
        projection_specs=control_specs(),
        excluded_volume_inventory=heavy,
        excluded_volume_radius=".1 nm",
    )
    assert modeler.build().n_interaction_sites == 15
    if problem == "radius_missing":
        modeler.excluded_volume_radius = None
    elif problem == "inventory_missing":
        modeler.excluded_volume_inventory = None
    elif problem == "frame":
        heavy["structure_index"] = 3
    elif problem == "state":
        heavy["chemical_state"] = 2
    elif problem == "selection":
        heavy["selected_atom_indices"] = list(range(10))
    elif problem == "chemical":
        heavy["features"][0]["kind"] = "hydrophobicity"
    elif problem == "radius_invalid":
        modeler.excluded_volume_radius = "0 nm"
    else:
        modeler.projection_specs[0]["projection_direction"] = [0, 0, 0]
    with pytest.raises(ArgumentError):
        modeler.build()
    assert modeler.result is None


def test_public_provider_ring_plane_supplies_geometry_without_face_inference():
    coords = [
        [0.1 * np.cos(i * np.pi / 3), 0.1 * np.sin(i * np.pi / 3), 0] for i in range(6)
    ]
    source = system(smiles="c1ccccc1", coordinates=coords)
    inventory = get_features(source, features=["aromatic ring"])
    assert len(inventory["features"]) == 1
    normal = puw.get_value(inventory["features"][0]["normal"], to_unit="dimensionless")
    query = from_receptor_projections(
        inventory,
        projection_specs=[
            dict(
                feature_index=0,
                projection_direction=[0, 0, -1],
                distance="4.5 angstrom",
                target_normal=normal,
                label="declared negative-z aromatic face",
            )
        ],
    )
    np.testing.assert_allclose(
        puw.get_value(query.interaction_sites[0].center), [0, 0, -0.45], atol=1e-14
    )
    assert query.metadata["source_inventory"]["recognition"]["aromatic_geometry"]


def test_public_provider_charge_centers_are_complemented_with_source_correspondence():
    source = system(smiles="[Na+].[Cl-]", coordinates=[[0, 0, 0], [1, 0, 0]])
    inventory = get_features(source, features=["positive charge", "negative charge"])
    assert [record["atom_indices"] for record in inventory["features"]] == [[0], [1]]
    query = from_receptor_projections(
        inventory,
        projection_specs=[
            dict(
                feature_index=i,
                projection_direction=[0, 0, 1],
                distance="400 pm",
                label="declared charge control",
            )
            for i in range(2)
        ],
    )
    assert [site.feature_name for site in query.interaction_sites] == [
        "negative charge",
        "positive charge",
    ]
    np.testing.assert_allclose(
        puw.get_value(query.interaction_sites[0].center), [0, 0, 0.4]
    )
    np.testing.assert_allclose(
        puw.get_value(query.interaction_sites[1].center), [1, 0, 0.4]
    )
    assert [site.metadata["atom_indices"] for site in query.interaction_sites] == [
        [0],
        [1],
    ]


def test_cached_projection_covariance_and_no_hidden_default_direction():
    inventory, specs = control_inventory(), control_specs()
    original = from_receptor_projections(inventory, projection_specs=specs)
    # Independent exact quarter-turn/translation oracle for query geometry.
    rotation = np.array([[0.0, -1, 0], [1, 0, 0], [0, 0, 1]])
    translation = np.array([2.0, -3, 4])
    for record in inventory["features"]:
        center = puw.get_value(record["center"], to_unit="nm")
        record["center"] = puw.quantity(rotation @ center + translation, "nm")
    for spec in specs:
        for key in ("projection_direction", "target_direction", "target_normal"):
            if key in spec:
                spec[key] = rotation @ spec[key]
    transformed = from_receptor_projections(inventory, projection_specs=specs)
    for before, after in zip(original.interaction_sites, transformed.interaction_sites):
        np.testing.assert_allclose(
            puw.get_value(after.center),
            rotation @ puw.get_value(before.center) + translation,
        )
        for key in ("direction", "normal"):
            if hasattr(before.shape, key):
                np.testing.assert_allclose(
                    puw.get_value(getattr(after.shape, key)),
                    rotation @ puw.get_value(getattr(before.shape, key)),
                )


def test_facade_composition_keeps_actual_projection_and_exclusion_attribution():
    source = system(smiles="CCC", coordinates=[[0, 0, 0], [0.15, 0, 0], [0.3, 0, 0]])
    inventory = get_features(source, features=["hydrophobicity"])
    heavy = get_features(source, features=["included volume"])
    options = dict(
        feature_inventory=inventory,
        projection_specs=[
            dict(
                feature_index=0,
                projection_direction=[0, 1, 0],
                distance=".35 nm",
                label="declared control",
            )
        ],
        excluded_volume_inventory=heavy,
        excluded_volume_radius=".1 nm",
    )
    with phmt.attribution(False):
        plain = StructureBasedModeler(source, **options).build()
    with phmt.attribution(True):
        tracked = StructureBasedModeler(source, **options).build()
    payload = tracked.metadata.pop("attribution")
    assert payload["status"] == "captured"
    targets = {row["used_by"] for row in payload["host_references"]}
    assert any(
        target.endswith("receptor_projections.from_receptor_projections")
        for target in targets
    )
    assert any(
        target.endswith("excluded_volumes.get_excluded_volume_sites")
        for target in targets
    )
    assert not any(
        row["record"]["title"] == "MolSysMT" for row in payload["host_references"]
    )
    assert plain.metadata == tracked.metadata
    for first, second in zip(plain.interaction_sites, tracked.interaction_sites):
        assert first.metadata == second.metadata
        np.testing.assert_array_equal(
            puw.get_value(first.center), puw.get_value(second.center)
        )
