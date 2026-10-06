"""Native aromatic construction with independent geometry/profile controls."""

import json
import warnings
from copy import deepcopy

import ackredit as ack
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from devtools.aromatic_interaction_cases import (
    CATION_PROFILES,
    PI_PROFILES,
    REFERENCE_DOIS,
    build_case,
    observe,
    ring_coordinates,
)
from pharmacophoremt import _ackredit
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt._private.smonitor.warnings import AckreditTrackingWarning
from pharmacophoremt.io import load_json, to_json
from pharmacophoremt.modeler import from_interactions
from pharmacophoremt.screening import PoseEvaluator
from tests.test_attribution import run_reader
from tests.test_ionic_interactions import replace_records
from tests.test_pose_evaluation import system


@pytest.mark.parametrize("method,profile", PI_PROFILES)
@pytest.mark.parametrize("case", ["parallel", "edge"])
def test_pi_profiles_preserve_observations_and_share_query_planes(
    method, profile, case
):
    source, ligand, partner = build_case(case)
    observed = observe(source, ligand, partner, method, profile)
    assert observed.n_interactions == 1
    evidence = observed.to_dict()["evidence"][0]
    assert ("parallel" if case == "parallel" else "edge_to_face") in evidence
    for selection, expected_center, expected_axis in [
        (ligand, [0, 0, 0], [0, 0, 1]),
        (partner, [0, 0, 0.35], [0, 0, 1] if case == "parallel" else [1, 0, 0]),
    ]:
        query = from_interactions(source, observed, selection, radius=".02 nm")
        assert query.n_interaction_sites == 1
        site = query.interaction_sites[0]
        assert site.shape_name == "disk" and site.feature_name == "aromatic ring"
        np.testing.assert_allclose(
            puw.get_value(site.center, to_unit="nm"), expected_center, atol=1e-15
        )
        assert abs(np.dot(site.shape.normal, expected_axis)) == pytest.approx(1)
        assert site.metadata["atom_indices"] == selection
        assert query.metadata["parameters"] == detached(observed.parameters)
        assert (
            query.metadata["aromatic_conversion_policy"]["geometry"]
            == "shared_classical_geometry@1"
        )
        assert (
            PoseEvaluator(query).evaluate(source, selection=selection)["status"]
            == "matched"
        )


@pytest.mark.parametrize("method,profile", CATION_PROFILES)
def test_cation_ring_and_charge_roles_and_neutral_negative(method, profile):
    source, cation, ring = build_case("atomic_cation")
    observed = observe(source, cation, ring, method, profile, family="cation_pi")
    assert observed.n_interactions == 1
    for selection, feature, shape in [
        (cation, "positive charge", "sphere"),
        (ring, "aromatic ring", "disk"),
    ]:
        query = from_interactions(source, observed, selection)
        assert query.interaction_sites[0].feature_name == feature
        assert query.interaction_sites[0].shape_name == shape
        assert (
            PoseEvaluator(query).evaluate(source, selection=selection)["status"]
            == "matched"
        )
    charged_query = from_interactions(source, observed, cation)
    neutral = system("[Ne]", [[0, 0, 0.35]])
    result = PoseEvaluator(charged_query).evaluate(neutral)
    assert result["status"] == "not_matched" and result["fit_value"] == 0


def test_containing_cation_policy_is_explicit_and_retains_reference_charges():
    source, cation, ring = build_case("compound_cation")
    observed = observe(
        source,
        cation,
        ring,
        "centroid_distance_angle",
        "smarts_5_6",
        family="cation_pi",
    )
    assert observed.n_interactions == 3
    with pytest.raises(ArgumentError, match="does not map uniquely"):
        from_interactions(source, observed, cation)
    query = from_interactions(
        source, observed, cation, cation_mapping="containing_center", radius=".02 nm"
    )
    site = query.interaction_sites[0]
    assert query.n_interaction_sites == 1
    assert site.metadata["atom_indices"] == [0, 1, 2, 3]
    assert site.metadata["geometry_atom_indices"] == [0, 2, 3]
    np.testing.assert_allclose(
        puw.get_value(site.center, to_unit="nm"), [0, 0.01, 0.35], atol=1e-15
    )
    assert len(site.metadata["observations"]) == 3
    assert sorted(
        row["participant_mapping"]["observed_atom_indices"]
        for row in site.metadata["observations"]
    ) == [[0], [2], [3]]
    assert {
        row["measurements"]["cation_charge"]["values"]
        for row in site.metadata["observations"]
    } == {0.0, 1.0}
    assert site.metadata["charge"]["values"] == 1
    assert all(
        row["participant_mapping"]["policy"] == "containing_center"
        for row in site.metadata["observations"]
    )
    assert (
        PoseEvaluator(query).evaluate(source, selection=cation)["status"] == "matched"
    )
    # The aromatic ligand role does not require canonicalizing its partner cation.
    aromatic_query = from_interactions(source, observed, ring)
    assert len(aromatic_query.interaction_sites[0].metadata["observations"]) == 3


def test_native_compound_cation_keeps_exact_geometry_policy():
    source, cation, ring = build_case("compound_cation")
    observed = observe(
        source,
        cation,
        ring,
        "centroid_angle_offset",
        "least_squares",
        family="cation_pi",
    )
    query = from_interactions(
        source, observed, cation, cation_mapping="containing_center"
    )
    site = query.interaction_sites[0]
    assert site.metadata["observations"][0]["participant_mapping"]["policy"] == "exact"
    # Detector uses all participant atoms; the shared hypothesis uses nitrogen members.
    assert (
        query.metadata["parameters"]["cation_point"]
        == "arithmetic_centroid_of_all_participant_atoms"
    )
    np.testing.assert_allclose(
        puw.get_value(site.center, to_unit="nm"), [0, 0.01, 0.35], atol=1e-15
    )


def test_repeated_ring_contacts_aggregate_and_negative_planes_are_independent():
    source, ligand, partner = build_case("repeated")
    observed = observe(
        source, ligand, partner, "centroid_angle_offset", "least_squares"
    )
    query = from_interactions(source, observed, ligand, radius=".02 nm")
    site = query.interaction_sites[0]
    assert query.n_interaction_sites == 1 and len(site.metadata["observations"]) == 2
    site.shape.normal = -site.shape.normal
    evaluator = PoseEvaluator(query, direction_tolerance="10 degrees")
    assert evaluator.evaluate(source, selection=ligand)["status"] == "matched"
    orthogonal = system("c1ccccc1", ring_coordinates()[:, [2, 0, 1]])
    assert evaluator.evaluate(orthogonal)["status"] == "not_matched"
    displaced = msm.structure.translate(
        source, selection=ligand, translation="[1,0,0] nm", in_place=False
    )
    assert evaluator.evaluate(displaced, selection=ligand)["status"] == "not_matched"


def test_public_geometry_and_inventory_constructor_are_reused(monkeypatch):
    import pharmacophoremt.modeler.interaction_based as module

    source, ligand, partner = build_case()
    observed = observe(
        source, ligand, partner, "centroid_angle_offset", "least_squares"
    )
    calls = []
    plane = msm.structure.get_least_squares_plane
    builder = module.from_feature_inventory

    def record_plane(*args, **kwargs):
        calls.append("plane")
        return plane(*args, **kwargs)

    def record_builder(*args, **kwargs):
        calls.append("inventory_constructor")
        return builder(*args, **kwargs)

    def forbidden(*args, **kwargs):
        raise AssertionError("cached construction cannot rerun interaction detection")

    monkeypatch.setattr(msm.structure, "get_least_squares_plane", record_plane)
    monkeypatch.setattr(module, "from_feature_inventory", record_builder)
    monkeypatch.setattr(msm.interactions.pi_pi, "get_pi_pi_interactions", forbidden)
    from_interactions(source, observed, ligand)
    assert calls == ["plane", "inventory_constructor"]


@pytest.mark.parametrize(
    "field,value",
    [
        ("profile", "unknown"),
        ("chemical_state_index", True),
        ("recognition_rule_version", "unknown@2"),
        ("plane_method", "unknown"),
        ("participant_definition", "unknown"),
    ],
)
def test_incompatible_profiles_states_and_rules_raise(field, value):
    source, ligand, partner = build_case()
    observed = observe(
        source, ligand, partner, "centroid_angle_offset", "least_squares"
    )
    parameters = deepcopy(observed.parameters)
    parameters[field] = value
    declared = replace_records(observed, parameters=parameters)
    with pytest.raises(ArgumentError):
        from_interactions(source, declared, ligand)


@pytest.mark.parametrize("policy", [None, True, "expand", [], {}])
def test_invalid_cation_mapping_policy_is_rejected(policy):
    source, ligand, partner = build_case()
    observed = observe(
        source, ligand, partner, "centroid_angle_offset", "least_squares"
    )
    with pytest.raises(ArgumentError, match="cation_mapping"):
        from_interactions(source, observed, ligand, cation_mapping=policy)


def test_partial_unmatched_and_periodic_participants_raise():
    source, ligand, partner = build_case()
    observed = observe(
        source, ligand, partner, "centroid_angle_offset", "least_squares"
    )
    with pytest.raises(ArgumentError, match="crosses"):
        from_interactions(source, observed, [0, 1])
    declared = replace_records(
        observed,
        participants=[
            {"role": "ring_a", "atom_indices": [0, 1, 2]},
            {"role": "ring_b", "atom_indices": partner},
        ],
    )
    with pytest.raises(ArgumentError, match="does not map uniquely"):
        from_interactions(source, declared, ligand)
    periodic = replace_records(observed, images=[[0, 0, 0], [0, 0, 1]])
    with pytest.raises(ArgumentError, match="nonzero periodic"):
        from_interactions(source, periodic, ligand)


def test_stale_cation_reference_charge_is_rejected():
    source, cation, ring = build_case("compound_cation")
    observed = observe(
        source,
        cation,
        ring,
        "centroid_distance_angle",
        "smarts_5_6",
        family="cation_pi",
    )
    declared = replace_records(observed, measurements={"cation_charge": 9})
    with pytest.raises(ArgumentError, match="charge and shared feature disagree"):
        from_interactions(source, declared, cation, cation_mapping="containing_center")


@pytest.mark.parametrize("method,profile", PI_PROFILES)
def test_units_persistence_source_maps_and_undefined_measurements(
    method, profile, tmp_path
):
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        source, ligand, partner = build_case(unit="angstrom", transform=True)
        observed = observe(source, ligand, partner, method, profile)
        before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
        declared = replace_records(
            observed,
            atom_source_indices=list(range(40, 52)),
            structure_source_indices=[7],
        )
        query = from_interactions(source, declared, ligand, radius=".2 angstrom")
        site = query.interaction_sites[0]
        assert site.metadata["source_atom_indices"] == list(range(40, 46))
        assert query.metadata["source_structure_indices"] == [7]
        path = tmp_path / "aromatic.json"
        to_json(query, path)
        restored = load_json(path)
        assert restored.metadata == query.metadata
        assert restored.interaction_sites[0].metadata == site.metadata
        assert (
            PoseEvaluator(restored).evaluate(source, selection=ligand)["status"]
            == "matched"
        )
        np.testing.assert_array_equal(
            puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
        )
        measures = site.metadata["observations"][0]["measurements"]
        if "intersection_distance" in measures:
            record = puw.QuantityRecord.from_dict(measures["intersection_distance"])
            assert np.isnan(puw.get_value(record.to_quantity(unit="nm"), to_unit="nm"))
        json.loads(path.read_text())


def test_sealed_nonfinite_provenance_preserves_values_and_finite_compatibility():
    values = puw.quantity([np.nan, np.inf, -np.inf, -0.0], "angstrom")
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        payload = detached(values)
        json.dumps(payload, allow_nan=False)
        restored = puw.QuantityRecord.from_dict(payload).to_quantity(unit="nm")
        result = puw.get_value(restored, to_unit="angstrom")
        np.testing.assert_array_equal(result, [np.nan, np.inf, -np.inf, -0.0])
        assert np.signbit(result[-1])
        finite = puw.quantity([1.0, 2.0], "angstrom")
        assert detached(finite) == puw.QuantityRecord.from_quantity(finite).to_dict()
    with pytest.raises(ArgumentError, match="finite coordinate"):
        source = system("c1ccccc1", np.full((6, 3), np.nan))
        phmt.modeler.get_features(source, features=["aromatic ring"])


def test_empty_internal_and_uncovered_are_distinct():
    source, ligand, partner = build_case()
    observed = observe(
        source, ligand, partner, "centroid_angle_offset", "least_squares"
    )
    assert from_interactions(source, observed, "all").n_interaction_sites == 0
    moved = msm.structure.translate(
        source, selection=partner, translation="[0,0,3] nm", in_place=False
    )
    empty = observe(moved, ligand, partner, "centroid_angle_offset", "least_squares")
    query = from_interactions(moved, empty, ligand)
    assert query.n_interaction_sites == 0 and query.metadata[
        "evaluated_structure_indices"
    ] == [0]
    with pytest.raises(ArgumentError):
        PoseEvaluator(query)
    source.structures.append(coordinates=msm.get(source, coordinates=True))
    observed = observe(
        source, ligand, partner, "centroid_angle_offset", "least_squares"
    )
    with pytest.raises(ArgumentError, match="not evaluated"):
        from_interactions(source, observed, ligand, structure_index=1)


@pytest.mark.parametrize("method,profile", PI_PROFILES)
def test_actual_profile_credit_and_cached_reuse_are_distinct(method, profile):
    source, ligand, partner = build_case()
    with ack.session("aromatic-application") as application:
        with ack.capture("detection") as detection:
            observed = observe(source, ligand, partner, method, profile)
        declared_dois = {
            item.get("doi") for item in detection.attribution.to_dict()["items"]
        }
        expected = REFERENCE_DOIS.get(profile)
        assert declared_dois & set(REFERENCE_DOIS.values()) == (
            {expected} if expected else set()
        )
        with ack.capture("construction") as construction:
            with phmt.attribution():
                first = from_interactions(source, observed, ligand)
                second = from_interactions(source, observed, ligand)
                empty = from_interactions(source, observed, "all")
        assert ack.current_session() is application
        one, two = (
            query.metadata["attribution"]["references"] for query in (first, second)
        )
        assert one["items"] == two["items"] and one["uses"] and two["uses"]
        assert not any(
            "get_pi_pi_interactions" in use["used_by"]
            for use in construction.attribution.to_dict()["uses"]
        )
        assert empty.metadata["attribution"]["status"] == "captured"
        origin = first.metadata["parameters"]["attribution"]
        assert {item.get("doi") for item in origin["items"]} & set(
            REFERENCE_DOIS.values()
        ) == ({expected} if expected else set())
        original = json.dumps(second.metadata["attribution"], sort_keys=True)
        first.metadata["attribution"]["references"]["items"].clear()
        assert json.dumps(second.metadata["attribution"], sort_keys=True) == original


@pytest.mark.parametrize("method,profile", CATION_PROFILES)
def test_actual_cation_profile_credit_uses_its_declared_reference(method, profile):
    source, first, second = build_case("atomic_cation")
    with ack.session("cation-detection"):
        with ack.capture("observed cation detector") as capture:
            observations = observe(
                source, first, second, method, profile, family="cation_pi"
            )
        dois = {item.get("doi") for item in capture.attribution.to_dict()["items"]}
        expected = REFERENCE_DOIS.get(profile)
        assert dois & set(REFERENCE_DOIS.values()) == (
            {expected} if expected else set()
        )
        assert observations.parameters["attribution"]["items"]
        assert "10.3390/molecules26237201" not in dois


def test_optional_failure_absence_and_fresh_reader(tmp_path, monkeypatch):
    source, ligand, partner = build_case()
    observed = observe(
        source, ligand, partner, "centroid_angle_offset", "least_squares"
    )
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    with phmt.attribution():
        unavailable = from_interactions(source, observed, ligand)
    assert unavailable.metadata["attribution"]["status"] == "unavailable"
    monkeypatch.undo()
    with ack.session("writer"):
        with phmt.attribution():
            query = from_interactions(source, observed, ligand)
        references = tmp_path / "references.json"
        references.write_text(json.dumps(query.metadata["attribution"]["references"]))
        before = ack.get_attribution().to_dict()
        assert phmt.attribution_report(query.metadata["attribution"], format="bibtex")
        assert ack.get_attribution().to_dict() == before

    def broken():
        raise RuntimeError("controlled attribution failure")

    monkeypatch.setattr(_ackredit, "backend", broken)
    with warnings.catch_warnings(record=True) as emitted:
        warnings.simplefilter("always")
        with phmt.attribution():
            failed = from_interactions(source, observed, ligand)
    assert failed.metadata["attribution"]["status"] == "failed"
    assert any(isinstance(item.message, AckreditTrackingWarning) for item in emitted)
    assert (
        PoseEvaluator(failed).evaluate(source, selection=ligand)["status"] == "matched"
    )
    run_reader(
        """
import sys, json, importlib.abc
class NoScience(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'pharmacophoremt','molsysmt','rdkit','scipy'}:
            raise ModuleNotFoundError('reader excludes science', name=fullname)
sys.meta_path.insert(0, NoScience())
import ackredit as ack
data = json.load(open(sys.argv[1]))
with ack.session('reader'):
    saved = ack.Attribution.from_dict(data)
    assert saved.to_dict() == data and saved.report(format='bibtex')
    assert not ack.get_used_items()
""",
        references,
    )


def test_genuine_absence_does_not_prevent_aromatic_science():
    run_reader("""
import sys, importlib.abc
class NoAck(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] == 'ackredit':
            raise ModuleNotFoundError('controlled absence', name=fullname)
sys.meta_path.insert(0, NoAck())
import pharmacophoremt as phmt
assert 'ackredit' not in sys.modules
from devtools.aromatic_interaction_cases import build_case, observe
source, ligand, partner = build_case()
observed = observe(source, ligand, partner, 'plane_angle_intersection', 'smarts_5_6')
with phmt.attribution():
    query = phmt.modeler.from_interactions(source, observed, ligand)
assert query.metadata['attribution']['status'] == 'unavailable'
assert phmt.screening.PoseEvaluator(query).evaluate(source, selection=ligand)['status'] == 'matched'
assert 'ackredit' not in sys.modules
""")
