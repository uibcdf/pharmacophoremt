"""Independent public cached-profile, budget, unit and ownership controls."""

import importlib
import json
import subprocess
import sys
import warnings

import ackredit
import molsysmt as msm
import numpy as np
import pytest
from argdigest import UnknownArgumentError, describe_contract

from pharmacophoremt import _ackredit, attribution
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.io import load_json, load_yaml, to_json, to_yaml
from pharmacophoremt.modeler import from_receptor_features, get_features
from phmt_test_support.prepared_ccd_ligands import state_payload
from phmt_test_support.prepared_receptor_workflow import load_input
from phmt_test_support.prepared_workflow import models_equivalent
from phmt_test_support.saved_model_reader import native_record
from tests.test_receptor_hypothesis_pilot import original_geometry

OWNER = importlib.import_module("pharmacophoremt.modeler.receptor_generation")
OPTIONS = dict(
    receptor_profile="donor_aromatic_faces",
    donor_distances=[".28 nm", "350 pm"],
    aromatic_distances=["3.5 angstrom", ".45 nm"],
    radius="20 pm",
    max_hypotheses=8,
)


def inventory(kinds=("hb donor", "hb acceptor", "aromatic ring")):
    records = []
    for index, kind in enumerate(kinds):
        records.append(
            dict(
                kind=kind,
                atom_indices=[index],
                center=puw.quantity([index, 0, 0], "nm"),
                direction=puw.quantity([1, 0, 0], "dimensionless")
                if kind == "hb donor"
                else None,
                normal=puw.quantity([0, 0, 1], "dimensionless")
                if kind == "aromatic ring"
                else None,
            )
        )
    return dict(
        definition="classical_atomic_formal@1",
        features=records,
        selected_atom_indices=list(range(max(1, len(records)))),
        structure_index=4,
        chemical_state="reference",
        recognition={"origin": "synthetic cached feature control"},
        attribution={"status": "cached-test-marker", "producer": "historical only"},
    )


def build(source=None, **options):
    return from_receptor_features(
        inventory() if source is None else source, **(OPTIONS | options)
    )


def test_definition_owned_argdigest_contract_and_closed_signature():
    plan = from_receptor_features.digestion_plan
    assert plan.contract_caller == OWNER.__name__ + ".from_receptor_features"
    contract = plan.contracts.resolve(plan.contract_caller)
    assert describe_contract(contract, plan.domains)["admits"] == "signature"
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert build()["complete"]
    with pytest.raises(UnknownArgumentError):
        build(typo=True)


@pytest.mark.parametrize("policy", [["nm", "ps", "radians"], ["pm", "fs", "degrees"]])
def test_independent_numeric_product_roles_faces_units_and_source_identity(policy):
    with puw.context(standard_units=policy):
        result = build()
        enumeration = result["report"]["enumeration"]
        assert enumeration["total_possible"] == enumeration["returned"] == 8
        assert enumeration["remaining"] == 0 and result["complete"]
        for index, model in enumerate(result["models"]):
            donor_distance = [0.28, 0.35][index // 4]
            ring_distance = [0.35, 0.45][index % 4 // 2]
            face = [1, -1][index % 2]
            first, second = model.interaction_sites
            np.testing.assert_allclose(
                puw.get_value(first.center, to_unit="nm"),
                [donor_distance, 0, 0],
                atol=1e-12,
                rtol=0,
            )
            np.testing.assert_allclose(
                puw.get_value(second.center, to_unit="nm"),
                [2, 0, face * ring_distance],
                atol=1e-12,
                rtol=0,
            )
            assert first.features == ["hb acceptor"] and second.features == [
                "aromatic ring"
            ]
            assert (
                first.essential
                and second.essential
                and first.weight == second.weight == 1
            )
            assert first.metadata["atom_indices"] == [0] and second.metadata[
                "atom_indices"
            ] == [2]
            assert model.ref_struct == 4
            assert (
                model.metadata["source_attribution"]["status"] == "cached-test-marker"
            )
            assert model.metadata["method"] == OWNER.METHOD
            assert (
                model.metadata["projection_method"] == "explicit_receptor_projection@1"
            )
            choices = model.metadata["generation"]["choices"]
            assert [c["feature_index"] for c in choices] == [0, 2]
            assert choices[1]["face_sign"] == face
            recovered_distance = puw.QuantityRecord.from_dict(
                choices[0]["distance"]
            ).to_quantity()
            assert float(
                puw.get_value(recovered_distance, to_unit="nm")
            ) == pytest.approx(donor_distance, abs=1e-12)


@pytest.mark.parametrize("budget", [0, 1, 3, 8, 20])
def test_budget_prefix_and_exact_exhaustion_are_not_activity(budget):
    result = build(max_hypotheses=budget)
    report = result["report"]
    assert len(result["models"]) == min(budget, 8)
    assert report["enumeration"]["remaining"] == max(8 - budget, 0)
    assert result["complete"] is (budget >= 8)
    assert [r["hypothesis_id"] for r in report["hypotheses"]] == [
        f"receptor:{i}" for i in range(min(budget, 8))
    ]
    assert report["omitted"] == [
        dict(
            feature_index=1,
            kind="hb acceptor",
            atom_indices=[1],
            reason="ideal_acceptor_profile_not_adopted",
        )
    ]
    assert "fit_value" not in result


@pytest.mark.parametrize(
    "kinds,total,sites",
    [
        ([], 0, 0),
        (["hb acceptor"], 0, 0),
        (["hb donor"], 2, 1),
        (["aromatic ring"], 4, 1),
        (["hb donor", "hb donor", "aromatic ring"], 16, 3),
    ],
)
def test_optional_families_empty_and_multiple_source_occurrences(kinds, total, sites):
    result = build(inventory(kinds), max_hypotheses=100)
    assert result["report"]["enumeration"]["total_possible"] == total
    assert len(result["models"]) == total and result["complete"]
    assert all(len(model.interaction_sites) == sites for model in result["models"])
    assert result["report"]["status"] == (
        "enumerated" if total else "no_supported_features"
    )


def test_shared_donor_heavy_atom_keeps_indexed_hydrogen_identity():
    source = inventory(["hb donor", "hb donor"])
    source["selected_atom_indices"] = [3, 7, 9]
    source["features"][0]["atom_indices"] = [3, 7]
    source["features"][1]["atom_indices"] = [3, 9]
    result = build(source, donor_distances=[".3 nm"])
    assert [
        site.metadata["atom_indices"] for site in result["models"][0].interaction_sites
    ] == [[3, 7], [3, 9]]


@pytest.mark.parametrize("budget", [0, 1])
@pytest.mark.parametrize(
    "kinds", [["included volume"], ["hb donor", "included volume"]]
)
def test_exclusion_records_are_a_separate_input_domain(kinds, budget):
    with pytest.raises(ArgumentError, match="separate inventory"):
        build(inventory(kinds), max_hypotheses=budget)


@pytest.mark.parametrize("value", [None, 1, "yes"])
def test_skip_control_rejects_nonboolean_values(value):
    with pytest.raises(ArgumentError):
        build(skip_digestion=value)


def test_repeated_declared_choices_remain_distinct():
    result = build(inventory(["hb donor"]), donor_distances=[".3 nm", "3 angstrom"])
    assert len(result["models"]) == 2
    assert [
        x["choices"][0]["distance_index"] for x in result["report"]["hypotheses"]
    ] == [0, 1]
    np.testing.assert_allclose(
        puw.get_value(result["models"][0].interaction_sites[0].center, to_unit="nm"),
        puw.get_value(result["models"][1].interaction_sites[0].center, to_unit="nm"),
        atol=1e-12,
    )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "option,value",
    [
        ("receptor_profile", "auto"),
        ("donor_distances", []),
        ("donor_distances", [0.3]),
        ("donor_distances", ["1 ps"]),
        ("aromatic_distances", ["0 nm"]),
        ("aromatic_distances", ["nan nm"]),
        ("radius", "-1 nm"),
        ("max_hypotheses", -1),
        ("max_hypotheses", True),
        ("max_hypotheses", None),
        ("max_hypotheses", 1.5),
    ],
)
def test_scientific_admission_survives_explicit_bypass(skip, option, value):
    with pytest.raises(ArgumentError) as caught:
        build(**{option: value}, skip_digestion=skip)
    assert caught.value.code == "PHMT-E102"


@pytest.mark.parametrize("budget", [0, 1])
def test_invalid_later_geometry_is_not_a_partial_or_empty_success(monkeypatch, budget):
    source = inventory()
    source["features"][2]["normal"] = None

    def forbidden(*args, **kwargs):
        pytest.fail("a model was built before full cache validation")

    monkeypatch.setattr(OWNER, "from_receptor_projections", forbidden)
    with pytest.raises(ArgumentError, match="feature 2"):
        build(source, max_hypotheses=budget)


def test_large_product_is_bounded_before_materialization(monkeypatch):
    original = OWNER.product

    def guarded(*choices):
        for index, row in enumerate(original(*choices)):
            assert index < 2, "enumeration exceeded its budget"
            yield row

    monkeypatch.setattr(OWNER, "product", guarded)
    result = build(inventory(["aromatic ring"] * 40), max_hypotheses=2)
    assert len(result["models"]) == 2
    assert result["report"]["enumeration"]["total_possible"] == 4**40
    assert not result["complete"]


def test_cached_boundary_and_independent_result_ownership(monkeypatch):
    source = inventory()

    def forbidden(*args, **kwargs):
        pytest.fail("cached construction accessed a molecular system")

    for name in ["get", "select", "convert", "copy", "extract", "set"]:
        monkeypatch.setattr(msm, name, forbidden)
    monkeypatch.setattr(msm.structure, "get_vectors", forbidden)
    monkeypatch.setattr(msm.structure, "get_least_squares_plane", forbidden)
    result = build(source)
    a, b = result["models"][:2]
    a.metadata["generation"]["omitted"][0]["atom_indices"].append(99)
    a.metadata["source_inventory"]["features"][0]["atom_indices"].append(98)
    result["report"]["source_inventory"]["features"][0]["atom_indices"].append(97)
    assert source["features"][0]["atom_indices"] == [0]
    assert b.metadata["generation"]["omitted"][0]["atom_indices"] == [1]
    assert b.metadata["source_inventory"]["features"][0]["atom_indices"] == [0]


def test_real_optional_credit_reuse_model_results_and_saved_reader(tmp_path):
    with ackredit.session("public receptor client") as session:
        with attribution():
            first, second = build(), build()
        assert ackredit.current_session() is session
    for result in [first, second]:
        assert result["attribution"]["status"] == "captured"
        assert all(
            m.metadata["attribution"] == result["attribution"] for m in result["models"]
        )
        payload = json.dumps(result["attribution"])
        assert (
            "from_receptor_features" in payload and "software:molsysmt:" not in payload
        )
    original = native_record(first["models"][0], tmp_path, "captured")
    restored = native_record(
        load_json(tmp_path / "captured.json"), tmp_path, "restored"
    )
    assert models_equivalent(original, restored)
    first["models"][0].metadata["attribution"]["references"]["items"].clear()
    assert second["attribution"]["references"]["items"]


@pytest.mark.parametrize("fail", [False, True])
def test_optional_tracking_failure_or_absence_preserves_models(monkeypatch, fail):
    def backend():
        if fail:
            raise RuntimeError("controlled optional tracking failure")
        return None

    monkeypatch.setattr(_ackredit, "backend", backend)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("error")
        with attribution():
            result = build()
    assert len(result["models"]) == 8 and result["complete"]
    assert result["attribution"]["status"] != "captured"
    assert result["attribution"]["references"] is None
    assert result["attribution"]["host_references"]


def test_fresh_engine_blocked_saved_reader_preserves_credit(tmp_path):
    with attribution():
        result = build(max_hypotheses=1)
    to_json(result["models"][0], tmp_path / "saved.json")
    code = """
import importlib.abc,sys
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0]=='ackredit':
            raise ModuleNotFoundError('blocked optional provider',name='ackredit')
sys.meta_path.insert(0,Block())
from pharmacophoremt.io import load_json
from pharmacophoremt.modeler import from_receptor_features
m=load_json(sys.argv[1])
assert m.metadata['attribution']['status']=='captured'
assert m.metadata['generation']['method']=='cached_receptor_donor_aromatic_faces@1'
assert 'ackredit' not in sys.modules
from pharmacophoremt import attribution,pyunitwizard as puw
cache=dict(definition='classical_atomic_formal@1',structure_index=0,chemical_state='reference',selected_atom_indices=[0,1],recognition={},features=[dict(kind='hb donor',atom_indices=[0,1],center=puw.quantity([0,0,0],'nm'),direction=puw.quantity([1,0,0],'dimensionless'))])
with attribution():
    result=from_receptor_features(cache,receptor_profile='donor_aromatic_faces',donor_distances=['.3 nm'],aromatic_distances=['.4 nm'],radius='20 pm',max_hypotheses=1)
assert len(result['models'])==1 and result['complete']
assert result['attribution']['status']!='captured' and result['attribution']['provider'] is None
assert 'ackredit' not in sys.modules
"""
    child = subprocess.run(
        [sys.executable, "-B", "-c", code, str(tmp_path / "saved.json")],
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert child.returncode == 0, child.stdout + child.stderr


@pytest.mark.parametrize("policy", [["nm", "ps", "radians"], ["pm", "fs", "degrees"]])
def test_unchanged_prepared_region_matches_independent_frozen_oracles_and_recovers(
    tmp_path, policy
):
    configuration = puw.configure.report()
    with puw.context(standard_units=policy):
        source, identity = load_input(tmp_path)
        before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
        state_before = json.dumps(state_payload(source), sort_keys=True)
        cache = get_features(
            source,
            selection=msm.select(source, selection='group_id == "404"'),
            features=["hb donor", "hb acceptor", "aromatic ring"],
        )
        result = build(cache)
        plan = dict(donor_atoms=[791, 2772], ring_atoms=list(range(796, 802)))
        donor, direction, center, normal = original_geometry(
            plan, {"inputs_before": {"coordinates_nm": before}}
        )
        for index, model in enumerate(result["models"]):
            d, r, face = (
                [0.28, 0.35][index // 4],
                [0.35, 0.45][index % 4 // 2],
                [1, -1][index % 2],
            )
            np.testing.assert_allclose(
                puw.get_value(model.interaction_sites[0].center, to_unit="nm"),
                donor + d * direction,
                atol=1e-12,
                rtol=0,
            )
            displacement = (
                puw.get_value(model.interaction_sites[1].center, to_unit="nm") - center
            )
            assert abs(np.dot(displacement, normal)) == pytest.approx(r, abs=1e-12)
            assert model.metadata["generation"]["choices"][1]["face_sign"] == face
            original = native_record(model, tmp_path, f"model-{index}")
            for suffix, write, read in [
                ("json", to_json, load_json),
                ("yaml", to_yaml, load_yaml),
            ]:
                path = tmp_path / f"model-{index}.{suffix}"
                write(model, path)
                assert models_equivalent(
                    original,
                    native_record(read(path), tmp_path, f"read-{index}-{suffix}"),
                )
        np.testing.assert_array_equal(
            before, puw.get_value(msm.get(source, coordinates=True), to_unit="nm")
        )
        assert json.dumps(state_payload(source), sort_keys=True) == state_before
        record = dict(
            policy=policy,
            input_identity=identity,
            report=result["report"],
            models=[
                native_record(m, tmp_path, f"record-{i}")
                for i, m in enumerate(result["models"])
            ],
            input_coordinates_unchanged=True,
            chemical_history_unchanged=True,
        )
        (tmp_path / "prepared_public_results.json").write_text(
            json.dumps(record, indent=2, allow_nan=False) + "\n"
        )
    assert puw.configure.report() == configuration
