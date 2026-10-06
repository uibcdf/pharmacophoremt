"""Independent ionic query controls using public MolSysMT observations."""

import json
import warnings
from copy import deepcopy

import ackredit as ack
import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import _ackredit
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt._private.smonitor.warnings import AckreditTrackingWarning
from pharmacophoremt.io import load_json, to_json
from pharmacophoremt.modeler import (
    from_interactions,
    get_excluded_volume_sites,
    get_features,
)
from pharmacophoremt.screening import PoseEvaluator
from tests.test_attribution import run_reader
from tests.test_pose_evaluation import system

CARBOXYLATE = [
    [0, -0.15, 0],
    [0, 0, 0],
    [-0.1, 0.1, 0],
    [0.1, 0.1, 0],
    [0.1, 0.4, 0],
    [-0.1, 0.4, 0],
]


def observations(source, first, second, threshold="0.31 nm", **kwargs):
    return msm.interactions.ionic.get_ionic_interactions(
        source,
        threshold,
        selection=first,
        selection_2=second,
        selection_mode="between",
        structure_indices=[0],
        pbc=False,
        **kwargs,
    )


@pytest.fixture
def carboxylate():
    source = system("CC(=O)[O-].[Na+].[Na+]", CARBOXYLATE)
    return source, observations(source, [0, 1, 2, 3], [4, 5])


def replace_records(
    observed,
    *,
    participants=None,
    measurements=None,
    parameters=None,
    images=None,
    atom_source_indices=None,
    structure_source_indices=None,
):
    """Construct declared malformed/alternate evidence through the public codec."""
    records = []
    data = observed.to_dict()
    for row, index in enumerate(data["relation_indices"]):
        relation = observed.relation(int(index))
        record = dict(
            structure_index=int(data["structure_indices"][row]),
            **relation,
            evidence=str(data["evidence"][row]),
            measurements={
                name: float(values[row])
                for name, values in data["measurements"].items()
            },
        )
        if participants is not None:
            record["participants"] = participants
        if measurements is not None:
            record["measurements"].update(measurements)
        if images is not None:
            record["images"] = images
        records.append(record)
    return msm.Interactions.from_records(
        records,
        n_atoms=observed.n_atoms,
        n_structures=observed.n_structures,
        evaluated_structure_indices=observed.evaluated_structure_indices,
        method=observed.method,
        software=observed.software,
        measure_units=observed.measure_units,
        parameters=deepcopy(observed.parameters) if parameters is None else parameters,
        atom_source_indices=atom_source_indices,
        structure_source_indices=structure_source_indices,
        source_n_atoms=200,
        source_n_structures=20,
        source_id="declared-parent",
    )


@pytest.mark.parametrize(
    "selection,kind,center,charge",
    [
        ([0], "positive charge", [0, 0, 0], 1),
        ([1], "negative charge", [0.3, 0, 0], -1),
    ],
)
def test_atomic_roles_share_recognition_and_reject_wrong_sign(
    selection, kind, center, charge
):
    source = system("[Na+].[Cl-]", [[0, 0, 0], [0.3, 0, 0]])
    observed = observations(source, [0], [1])
    query = from_interactions(source, observed, selection, radius="0.02 nm")
    site = query.interaction_sites[0]
    assert site.feature_name == kind
    assert site.essential and site.weight == 1
    assert site.shape_name == "sphere"
    np.testing.assert_allclose(puw.get_value(site.center, to_unit="nm"), center)
    assert site.metadata["charge"]["values"] == charge
    assert (
        PoseEvaluator(query).evaluate(source, selection=selection)["status"]
        == "matched"
    )
    opposite = system("[Cl-]" if charge > 0 else "[Na+]", [center])
    result = PoseEvaluator(query).evaluate(opposite)
    assert result["status"] == "not_matched" and result["fit_value"] == 0


def test_compound_geometry_is_oxygen_centroid_and_contacts_aggregate(carboxylate):
    source, observed = carboxylate
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    query = from_interactions(source, observed, [0, 1, 2, 3], radius="0.02 nm")
    assert observed.n_interactions == 2 and query.n_interaction_sites == 1
    site = query.interaction_sites[0]
    assert site.metadata["atom_indices"] == [1, 2, 3]
    assert site.metadata["geometry_atom_indices"] == [2, 3]
    np.testing.assert_allclose(puw.get_value(site.center, to_unit="nm"), [0, 0.1, 0])
    assert len(site.metadata["observations"]) == 2
    assert all(
        record["measurements"]["distance"]["values"] == pytest.approx(0.3)
        for record in site.metadata["observations"]
    )
    assert puw.get_value(site.radius, to_unit="nm") == pytest.approx(0.02)
    result = PoseEvaluator(query).evaluate(source, selection=[0, 1, 2, 3])
    assert result["status"] == "matched" and result["fit_value"] == 1
    assert result["assignments"][0]["atom_indices"] == [1, 2, 3]
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )


def test_guanidinium_geometry_is_nitrogen_centroid():
    source = system(
        "NC(=[NH2+])N.[Cl-]",
        [
            [-0.1, 0, 0],
            [0, 0, 0],
            [0.1, 0, 0],
            [0, 0.15, 0],
            [0, 0.4, 0],
        ],
    )
    observed = observations(source, [0, 1, 2, 3], [4])
    query = from_interactions(source, observed, [0, 1, 2, 3], radius="0.02 nm")
    site = query.interaction_sites[0]
    assert site.feature_name == "positive charge"
    assert site.metadata["atom_indices"] == [0, 1, 2, 3]
    assert site.metadata["geometry_atom_indices"] == [0, 2, 3]
    np.testing.assert_allclose(puw.get_value(site.center, to_unit="nm"), [0, 0.05, 0])
    assert site.metadata["observations"][0]["measurements"]["distance"][
        "values"
    ] == pytest.approx(0.25)
    assert (
        PoseEvaluator(query).evaluate(source, selection=[0, 1, 2, 3])["status"]
        == "matched"
    )


def test_displacement_and_neutralization_are_independent_negatives(carboxylate):
    source, observed = carboxylate
    query = from_interactions(source, observed, [0, 1, 2, 3], radius="0.02 nm")
    moved = msm.structure.translate(
        source,
        translation="[1,0,0] nm",
        selection=[0, 1, 2, 3],
        in_place=False,
    )
    neutral = system("CC(=O)O.[Na+].[Na+]", CARBOXYLATE)
    for candidate in (moved, neutral):
        result = PoseEvaluator(query).evaluate(candidate, selection=[0, 1, 2, 3])
        assert result["status"] == "not_matched" and result["fit_value"] == 0
    assert (
        PoseEvaluator(query).evaluate(source, selection=[0, 1, 2, 3])["status"]
        == "matched"
    )


def test_public_exclusion_composition_vetoes_a_positive_charge_match(carboxylate):
    source, observed = carboxylate
    ligand = [0, 1, 2, 3]
    query = from_interactions(source, observed, ligand, radius="0.4 nm")
    collision = msm.structure.translate(
        source,
        translation="[0,0.3,0] nm",
        selection=ligand,
        in_place=False,
    )
    assert (
        PoseEvaluator(query).evaluate(collision, selection=ligand)["status"]
        == "matched"
    )
    exclusions = get_excluded_volume_sites(
        get_features(source, selection=[4, 5], features=["included volume"]),
        radius="0.05 nm",
    )
    for site in exclusions["interaction_sites"]:
        query.add_interaction_site(site)
    result = PoseEvaluator(query).evaluate(collision, selection=ligand)
    assert result["status"] == "not_matched" and result["fit_value"] == 1
    assert result["excluded_volume_clashes"] == [
        {"site_index": 1, "atom_index": 3},
        {"site_index": 2, "atom_index": 2},
    ]
    assert (
        PoseEvaluator(query).evaluate(source, selection=ligand)["status"] == "matched"
    )


@pytest.mark.parametrize("selection", [[1], [2, 3], [0, 1, 2, 4, 5]])
def test_cut_compound_charge_center_is_rejected(carboxylate, selection):
    source, observed = carboxylate
    with pytest.raises(ArgumentError, match="charge center crosses"):
        from_interactions(source, observed, selection)


@pytest.mark.parametrize(
    "field,value",
    [
        ("chemical_state_index", None),
        ("chemical_state_index", True),
        ("chemical_state_index", -1),
        ("participant_definition", "partial_charge"),
        ("recognition_rule_version", "formal_charge_centers@999"),
        ("charge_source", "inferred"),
    ],
)
def test_unsupported_state_and_recognition_contracts_raise(carboxylate, field, value):
    source, observed = carboxylate
    parameters = deepcopy(observed.parameters)
    parameters[field] = value
    declared = replace_records(observed, parameters=parameters)
    with pytest.raises(ArgumentError, match="state contract"):
        from_interactions(source, declared, [0, 1, 2, 3])


def test_observed_membership_and_charge_must_match_current_recognition(carboxylate):
    source, observed = carboxylate
    declared = replace_records(
        observed,
        participants=[
            {"role": "positive", "atom_indices": [4]},
            {"role": "negative", "atom_indices": [3]},
        ],
    )
    with pytest.raises(ArgumentError, match="current charge recognition"):
        from_interactions(source, declared, [0, 1, 2, 3])
    declared = replace_records(observed, measurements={"negative_charge": -2})
    with pytest.raises(ArgumentError, match="measurement and recognition disagree"):
        from_interactions(source, declared, [0, 1, 2, 3])


def test_provider_charge_geometry_tool_is_reused(carboxylate, monkeypatch):
    source, observed = carboxylate
    public = msm.structure.get_center
    calls = []

    def recording(*args, **kwargs):
        calls.append(kwargs["selection"])
        return public(*args, **kwargs)

    monkeypatch.setattr(msm.structure, "get_center", recording)

    def forbidden(*args, **kwargs):
        raise AssertionError("cached observations must not rerun the ionic detector")

    monkeypatch.setattr(msm.interactions.ionic, "get_ionic_interactions", forbidden)
    from_interactions(source, observed, [0, 1, 2, 3])
    assert calls == [[[2, 3]]]


def test_query_metadata_and_original_mapping_survive_persistence(carboxylate, tmp_path):
    source, observed = carboxylate
    declared = replace_records(
        observed,
        atom_source_indices=[40, 41, 42, 43, 44, 45],
        structure_source_indices=[7],
    )
    query = from_interactions(source, declared, [0, 1, 2, 3])
    assert query.metadata["source_structure_indices"] == [7]
    assert query.interaction_sites[0].metadata["source_atom_indices"] == [41, 42, 43]
    assert query.interaction_sites[0].metadata["source_geometry_atom_indices"] == [
        42,
        43,
    ]
    frozen = deepcopy(query.metadata["parameters"])
    declared.parameters["attribution"]["items"].clear()
    assert query.metadata["parameters"] == frozen
    path = tmp_path / "ionic.json"
    to_json(query, path)
    restored = load_json(path)
    assert restored.metadata == query.metadata
    assert restored.interaction_sites[0].metadata == query.interaction_sites[0].metadata
    assert (
        PoseEvaluator(restored).evaluate(source, selection=[0, 1, 2, 3])["status"]
        == "matched"
    )


def test_empty_internal_uncovered_and_periodic_observations(carboxylate):
    source, observed = carboxylate
    internal = from_interactions(source, observed, "all")
    assert internal.n_interaction_sites == 0
    empty = observations(source, [0, 1, 2, 3], [4, 5], threshold="0.1 nm")
    query = from_interactions(source, empty, [0, 1, 2, 3])
    assert query.n_interaction_sites == 0
    assert query.metadata["evaluated_structure_indices"] == [0]
    assert (
        query.metadata["parameters"]["attribution"] == empty.parameters["attribution"]
    )
    with pytest.raises(ArgumentError):
        PoseEvaluator(query)
    periodic = replace_records(observed, images=[[0, 0, 0], [1, 0, 0]])
    with pytest.raises(ArgumentError, match="nonzero periodic"):
        from_interactions(source, periodic, [0, 1, 2, 3])
    source.structures.append(coordinates=msm.get(source, coordinates=True))
    observed = observations(source, [0, 1, 2, 3], [4, 5])
    with pytest.raises(ArgumentError, match="not evaluated"):
        from_interactions(source, observed, [0, 1, 2, 3], structure_index=1)


def test_nondefault_units_and_shared_rigid_transform():
    xyz = np.asarray(CARBOXYLATE, dtype=float)
    rotation = np.array([[0.0, -1, 0], [1, 0, 0], [0, 0, 1]])
    xyz = xyz @ rotation.T + [2, 1, -3]
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        source = system("CC(=O)[O-].[Na+].[Na+]", xyz * 10, "angstrom")
        observed = observations(source, [0, 1, 2, 3], [4, 5], threshold="3.1 angstrom")
        query = from_interactions(source, observed, [0, 1, 2, 3], radius="0.2 angstrom")
        np.testing.assert_allclose(
            puw.get_value(query.interaction_sites[0].center, to_unit="nm"), [1.9, 1, -3]
        )
        assert (
            PoseEvaluator(query).evaluate(source, selection=[0, 1, 2, 3])["status"]
            == "matched"
        )


def test_real_attribution_reuse_empty_and_cached_origin(carboxylate):
    source, observed = carboxylate
    old = deepcopy(observed.parameters["attribution"])
    with ack.session("ionic-application") as application:
        with ack.capture("workflow") as workflow:
            with phmt.attribution():
                first = from_interactions(source, observed, [0, 1, 2, 3])
                second = from_interactions(source, observed, [0, 1, 2, 3])
                empty = from_interactions(source, observed, "all")
        assert ack.current_session() is application
        one, two = (query.metadata["attribution"] for query in (first, second))
        assert one["references"]["items"] == two["references"]["items"]
        assert one["references"]["uses"] and two["references"]["uses"]
        assert empty.metadata["attribution"]["status"] == "captured"
        payload = workflow.attribution.to_dict()
        assert not any(
            "get_ionic_interactions" in use["used_by"] for use in payload["uses"]
        )
        assert not {"10.1021/acs.jcim.1c00263", "10.3390/molecules26237201"} & {
            item.get("doi") for item in payload["items"]
        }
        assert first.metadata["parameters"]["attribution"] == old
        assert any("get_features" in use["used_by"] for use in payload["uses"])
        original = json.dumps(second.metadata["attribution"], sort_keys=True)
        first.metadata["attribution"]["references"]["items"].clear()
        assert json.dumps(second.metadata["attribution"], sort_keys=True) == original


def test_optional_provider_absence_and_failure_preserve_science(
    carboxylate, monkeypatch
):
    source, observed = carboxylate
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    with phmt.attribution():
        unavailable = from_interactions(source, observed, [0, 1, 2, 3])
    assert unavailable.metadata["attribution"]["status"] == "unavailable"

    def broken():
        raise RuntimeError("controlled attribution failure")

    monkeypatch.setattr(_ackredit, "backend", broken)
    with warnings.catch_warnings(record=True) as emitted:
        warnings.simplefilter("always")
        with phmt.attribution():
            failed = from_interactions(source, observed, [0, 1, 2, 3])
    assert failed.metadata["attribution"]["status"] == "failed"
    assert any(isinstance(item.message, AckreditTrackingWarning) for item in emitted)
    assert failed.n_interaction_sites == unavailable.n_interaction_sites == 1
    assert (
        PoseEvaluator(failed).evaluate(source, selection=[0, 1, 2, 3])["status"]
        == "matched"
    )


def test_genuine_absence_with_public_molecular_preparation():
    run_reader("""
import sys, importlib.abc
class NoAckredit(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] == 'ackredit':
            raise ModuleNotFoundError('controlled absence', name=fullname)
sys.meta_path.insert(0, NoAckredit())
import pharmacophoremt as phmt
assert 'ackredit' not in sys.modules
import molsysmt as msm
from tests.test_pose_evaluation import system
source = system('[Na+].[Cl-]', [[0,0,0],[.3,0,0]])
observed = msm.interactions.ionic.get_ionic_interactions(source, '.31 nm', pbc=False)
with phmt.attribution():
    query = phmt.modeler.from_interactions(source, observed, [0])
assert query.metadata['attribution']['status'] == 'unavailable'
assert phmt.screening.PoseEvaluator(query).evaluate(source, selection=[0])['status'] == 'matched'
assert 'ackredit' not in sys.modules
""")


def test_fresh_reader_retains_original_bibliography_without_credit(
    carboxylate, tmp_path
):
    source, observed = carboxylate
    with ack.session("ionic-producer"):
        with phmt.attribution():
            query = from_interactions(source, observed, [0, 1, 2, 3])
        path = tmp_path / "references.json"
        path.write_text(json.dumps(query.metadata["attribution"]["references"]))
        before = ack.get_attribution().to_dict()
        assert phmt.attribution_report(query.metadata["attribution"], format="bibtex")
        assert ack.get_attribution().to_dict() == before
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
    assert saved.to_dict() == data
    assert saved.report(format='bibtex')
    assert not ack.get_used_items()
""",
        path,
    )
