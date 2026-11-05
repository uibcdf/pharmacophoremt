"""Independent cached-composition and native placed-pose exclusion controls."""

import json
import math
import warnings
from copy import deepcopy

import ackredit
import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import _ackredit, attribution
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.io import load_json, load_yaml, to_json, to_yaml
from pharmacophoremt.modeler import (
    StructureBasedModeler,
    from_receptor_features,
    get_features,
)
from pharmacophoremt.screening import PoseEvaluator
from phmt_test_support.prepared_ccd_ligands import state_payload
from phmt_test_support.prepared_receptor_workflow import credit_input, load_input
from phmt_test_support.prepared_workflow import models_equivalent
from phmt_test_support.saved_model_reader import native_record
from phmt_test_support.validate_eralpha_template import portable
from tests.test_pose_evaluation import system
from tests.test_public_receptor_generation import OPTIONS, inventory

POLICIES = [["nm", "ps", "radians"], ["pm", "fs", "degrees"]]


def heavy_cache(chemical):
    heavy = deepcopy(chemical)
    heavy["features"] = [
        dict(
            kind="included volume",
            atom_indices=[i],
            geometry_atom_indices=[i],
            center=puw.quantity([i, 0, 0], "nm"),
            direction=None,
            normal=None,
        )
        for i in chemical["selected_atom_indices"]
    ]
    return heavy


def build(chemical=None, heavy=None, **changes):
    chemical = inventory() if chemical is None else chemical
    heavy = heavy_cache(chemical) if heavy is None else heavy
    options = (
        OPTIONS
        | dict(excluded_volume_inventory=heavy, excluded_volume_radius=".05 nm")
        | changes
    )
    return from_receptor_features(chemical, **options)


@pytest.mark.parametrize("policy", POLICIES)
def test_positive_enumeration_and_real_global_indices_are_preserved(policy):
    with puw.context(standard_units=policy):
        chemical = inventory()
        baseline = from_receptor_features(chemical, **OPTIONS)
        result = build(chemical)
        assert result["report"]["enumeration"] == baseline["report"]["enumeration"]
        assert result["report"]["hypotheses"] == baseline["report"]["hypotheses"]
        root = result["report"]["excluded_volumes"]
        assert root["attached_model_count"] == 8 and root["n_sites"] == 3
        assert "global_site_indices" not in root
        for model, positive in zip(result["models"], baseline["models"], strict=True):
            assert model.n_interaction_sites == 5
            assert model.metadata["excluded_volumes"]["global_site_indices"] == [
                2,
                3,
                4,
            ]
            for index, site in enumerate(model.interaction_sites):
                if index < 2:
                    np.testing.assert_allclose(
                        puw.get_value(site.center, to_unit="nm"),
                        puw.get_value(
                            positive.interaction_sites[index].center, to_unit="nm"
                        ),
                        atol=1e-12,
                        rtol=0,
                    )
                    assert site.weight == 1
                else:
                    atom = index - 2
                    assert site.features == ["excluded volume"] and site.weight == 0
                    assert site.metadata["atom_indices"] == [atom]
                    np.testing.assert_allclose(
                        puw.get_value(site.center, to_unit="nm"),
                        [atom, 0, 0],
                        atol=1e-12,
                        rtol=0,
                    )
                    assert float(
                        puw.get_value(site.radius, to_unit="nm")
                    ) == pytest.approx(0.05)


@pytest.mark.parametrize(
    "budget,kinds", [(0, ["hb donor"]), (4, ["hb acceptor"]), (0, [])]
)
def test_zero_and_no_supported_features_have_no_exclusion_only_model(budget, kinds):
    result = build(inventory(kinds), max_hypotheses=budget)
    assert result["models"] == []
    assert result["report"]["excluded_volumes"]["attached_model_count"] == 0
    assert "global_site_indices" not in result["report"]["excluded_volumes"]
    assert result["complete"] is (kinds != ["hb donor"])


@pytest.mark.parametrize("policy", POLICIES)
def test_empty_heavy_inventory_keeps_an_explicit_zero_site_recipe(policy):
    with puw.context(standard_units=policy):
        chemical = inventory()
        heavy = heavy_cache(chemical)
        heavy["features"] = []
        result = build(chemical, heavy, max_hypotheses=1)
        model = result["models"][0]
        assert model.n_interaction_sites == 2
        assert model.metadata["excluded_volumes"]["n_sites"] == 0
        assert model.metadata["excluded_volumes"]["global_site_indices"] == []
        assert result["report"]["excluded_volumes"]["attached_model_count"] == 1
        assert (
            result["report"]["excluded_volumes"]["source_inventory"]
            == (model.metadata["excluded_volumes"]["source_inventory"])
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("budget", [0, 2])
def test_malformed_exclusions_are_not_hidden_by_unsupported_positives(skip, budget):
    chemical = inventory(["hb acceptor"])
    heavy = heavy_cache(chemical)
    heavy["features"].append(deepcopy(heavy["features"][0]))
    with pytest.raises(ArgumentError) as caught:
        build(chemical, heavy, max_hypotheses=budget, skip_digestion=skip)
    assert caught.value.code == "PHMT-E102"


@pytest.mark.parametrize("fail", [False, True])
def test_optional_tracking_absence_or_failure_keeps_all_constraints(monkeypatch, fail):
    def backend():
        if fail:
            raise RuntimeError("controlled optional tracking failure")
        return None

    monkeypatch.setattr(_ackredit, "backend", backend)
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("error")
        with attribution():
            result = build(max_hypotheses=1)
    model = result["models"][0]
    assert model.n_interaction_sites == 5
    assert [s.weight for s in model.interaction_sites] == [1, 1, 0, 0, 0]
    assert model.metadata["excluded_volumes"]["global_site_indices"] == [2, 3, 4]
    assert result["attribution"]["status"] != "captured"
    assert result["attribution"]["references"] is None
    assert result["attribution"]["host_references"]


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("budget", [0, 1])
@pytest.mark.parametrize(
    "problem",
    [
        "radius_missing",
        "inventory_missing",
        "frame",
        "state",
        "selection",
        "chemical",
        "duplicates",
        "orientation",
        "radius_zero",
        "radius_unit",
    ],
)
def test_invalid_exclusions_fail_before_any_partial_model(skip, budget, problem):
    chemical = inventory()
    heavy = heavy_cache(chemical)
    changes = dict(max_hypotheses=budget, skip_digestion=skip)
    if problem == "radius_missing":
        changes["excluded_volume_radius"] = None
    elif problem == "inventory_missing":
        changes["excluded_volume_inventory"] = None
    elif problem == "frame":
        heavy["structure_index"] = 3
    elif problem == "state":
        heavy["chemical_state"] = "other"
    elif problem == "selection":
        heavy["selected_atom_indices"] = [0, 1, 2, 3]
    elif problem == "chemical":
        heavy["features"][0]["kind"] = "hydrophobicity"
    elif problem == "duplicates":
        heavy["features"].append(deepcopy(heavy["features"][0]))
    elif problem == "orientation":
        heavy["features"][0]["normal"] = [0, 0, 1]
    elif problem == "radius_zero":
        changes["excluded_volume_radius"] = "0 nm"
    elif problem == "radius_unit":
        changes["excluded_volume_radius"] = "1 ps"
    with pytest.raises(ArgumentError) as caught:
        build(chemical, heavy, **changes)
    assert caught.value.code == "PHMT-E102"


def test_reordered_context_and_model_ownership_without_molecular_access(monkeypatch):
    chemical = inventory()
    heavy = heavy_cache(chemical)
    heavy["selected_atom_indices"].reverse()

    def forbidden(*args, **kwargs):
        pytest.fail("cached exclusion composition accessed a molecular system")

    for name in ["get", "select", "convert", "extract", "copy", "set"]:
        monkeypatch.setattr(msm, name, forbidden)
    monkeypatch.setattr(msm.structure, "get_vectors", forbidden)
    monkeypatch.setattr(msm.structure, "get_least_squares_plane", forbidden)
    result = build(chemical, heavy, max_hypotheses=2)
    first, second = result["models"]
    first.interaction_sites[2].shape.center = puw.quantity([99, 0, 0], "nm")
    first.interaction_sites[2].metadata["atom_indices"].append(999)
    first.metadata["excluded_volumes"]["sites"][0]["atom_indices"].append(998)
    result["report"]["excluded_volumes"]["sites"][0]["atom_indices"].append(997)
    assert second.interaction_sites[2].metadata["atom_indices"] == [0]
    assert second.metadata["excluded_volumes"]["sites"][0]["atom_indices"] == [0]
    assert heavy["features"][0]["atom_indices"] == [0]
    np.testing.assert_array_equal(
        puw.get_value(second.interaction_sites[2].center, to_unit="nm"), [0, 0, 0]
    )


def test_existing_facade_uses_the_same_recipe_and_retains_its_reference():
    chemical = inventory()
    heavy = heavy_cache(chemical)
    reference = object()
    specs = [
        dict(
            feature_index=0,
            projection_direction=[1, 0, 0],
            distance=".28 nm",
            label="donor",
        ),
        dict(
            feature_index=2,
            projection_direction=[0, 0, 1],
            distance=".35 nm",
            target_normal=[0, 0, 1],
            label="ring",
        ),
    ]
    modeler = StructureBasedModeler(
        reference,
        feature_inventory=chemical,
        projection_specs=specs,
        excluded_volume_inventory=heavy,
        excluded_volume_radius=".05 nm",
        radius="20 pm",
    )
    expected = modeler.build()
    actual = build(chemical, heavy, max_hypotheses=1)["models"][0]
    assert expected.molecular_system is reference and actual.molecular_system is None
    assert actual.metadata["excluded_volumes"] == expected.metadata["excluded_volumes"]
    for a, b in zip(actual.interaction_sites, expected.interaction_sites, strict=True):
        assert a.features == b.features and a.weight == b.weight
        np.testing.assert_allclose(
            puw.get_value(a.center, to_unit="nm"),
            puw.get_value(b.center, to_unit="nm"),
            atol=1e-12,
            rtol=0,
        )
    modeler.excluded_volume_radius = None
    with pytest.raises(ArgumentError):
        modeler.build()
    assert modeler.result is None


@pytest.mark.parametrize("policy", POLICIES)
def test_actual_credit_and_native_recovery_preserve_every_exclusion(tmp_path, policy):
    with puw.context(standard_units=policy), attribution():
        result = build(max_hypotheses=2)
    assert result["attribution"]["status"] == "captured"
    assert "get_excluded_volume_sites" in json.dumps(result["attribution"])
    assert "software:molsysmt:" not in json.dumps(result["attribution"])
    for index, model in enumerate(result["models"]):
        assert model.metadata["attribution"] == result["attribution"]
        original = native_record(model, tmp_path, f"model-{index}")
        for suffix, write, read in [
            ("json", to_json, load_json),
            ("yaml", to_yaml, load_yaml),
        ]:
            path = tmp_path / f"saved-{index}.{suffix}"
            write(model, path)
            assert models_equivalent(
                original, native_record(read(path), tmp_path, f"read-{index}-{suffix}")
            )


@pytest.mark.parametrize("policy", POLICIES)
def test_real_selected_heavy_center_inside_equal_outside(tmp_path, policy):
    configuration = puw.configure.report()
    with puw.context(standard_units=policy):
        source = system("[2H]O", [[0.1, 0, 0], [0, 0, 0]])
        chemical = get_features(source, features=["hb donor"])
        heavy = get_features(source, features=["included volume"])
        generated = from_receptor_features(
            chemical,
            receptor_profile="donor_aromatic_faces",
            donor_distances=[".5 nm"],
            aromatic_distances=[".4 nm"],
            radius=".4 nm",
            max_hypotheses=1,
            excluded_volume_inventory=heavy,
            excluded_volume_radius=".5 nm",
        )
        model = generated["models"][0]
        boundary = system("O", [[0.5, 0, 0]])
        candidates = [
            msm.structure.translate(
                boundary, translation="[-.25,0,0] nm", in_place=False
            ),
            boundary,
            msm.structure.translate(
                boundary, translation="[.25,0,0] nm", in_place=False
            ),
        ]
        rows = [
            PoseEvaluator(model, min_fit_value=1).evaluate(candidate)
            for candidate in candidates
        ]
        assert [r["fit_value"] for r in rows] == [1, 1, 1]
        assert [r["status"] for r in rows] == ["not_matched", "matched", "matched"]
        assert rows[0]["excluded_volume_clashes"] == [dict(site_index=1, atom_index=0)]
        assert (
            rows[1]["excluded_volume_clashes"]
            == rows[2]["excluded_volume_clashes"]
            == []
        )
        (tmp_path / "boundary_results.json").write_text(
            json.dumps(
                dict(
                    policy=policy,
                    model=native_record(model, tmp_path, "boundary"),
                    results=rows,
                ),
                indent=2,
                allow_nan=False,
            )
            + "\n"
        )
    assert puw.configure.report() == configuration


@pytest.mark.parametrize("policy", POLICIES)
def test_prepared_receptor_clashes_match_original_coordinate_oracle(tmp_path, policy):
    configuration = puw.configure.report()
    with (
        puw.context(standard_units=policy),
        attribution(),
        ackredit.capture("generated receptor exclusions") as captured,
    ):
        source, identity = load_input(tmp_path)
        credit_input()
        selected = msm.select(source, selection='group_id == "404"')

        def snapshot():
            return dict(
                coordinates_nm=puw.get_value(
                    msm.get(source, coordinates=True), to_unit="nm"
                ).tolist(),
                chemical_history=json.dumps(state_payload(source), sort_keys=True),
                analyses={
                    label: portable(
                        msm.convert(
                            source.interactions[label],
                            to_form="molsysmt.InteractionsDict",
                        ).data
                    )
                    for label in ["hydrophobic", "hbonds", "pi_pi"]
                },
            )

        before = snapshot()
        chemical = get_features(source, selection=selected, features=["aromatic ring"])
        heavy = get_features(source, selection=selected, features=["included volume"])
        axis = puw.get_value(chemical["features"][0]["normal"], to_unit="dimensionless")
        translation = 0.35 * axis
        candidate = msm.structure.translate(
            source, translation=puw.quantity(translation, "nm"), in_place=False
        )
        original = np.asarray(before["coordinates_nm"])[0]
        points = original[list(range(796, 802))]
        normal = np.linalg.svd(points - points.mean(axis=0))[2][-1]
        assert abs(np.dot(normal, axis)) == pytest.approx(1, abs=1e-12)
        np.testing.assert_allclose(
            puw.get_value(msm.get(candidate, coordinates=True), to_unit="nm"),
            [original + translation],
            atol=1e-12,
            rtol=0,
        )
        rows = []
        for radius in [0.01, 0.4]:
            result = from_receptor_features(
                chemical,
                receptor_profile="donor_aromatic_faces",
                donor_distances=[".28 nm"],
                aromatic_distances=[".35 nm"],
                radius=".02 nm",
                max_hypotheses=2,
                excluded_volume_inventory=heavy,
                excluded_volume_radius=puw.quantity(radius, "nm"),
            )
            for face, model in enumerate(result["models"]):
                evaluated = PoseEvaluator(model, min_fit_value=1).evaluate(
                    candidate, selection=selected
                )
                expected = [
                    dict(site_index=1 + local, atom_index=atom)
                    for local, excluded in enumerate(range(791, 802))
                    for atom in range(791, 802)
                    if math.dist(original[atom] + translation, original[excluded])
                    < radius
                ]
                assert evaluated["excluded_volume_clashes"] == expected
                assert evaluated["fit_value"] == (1 if face == 0 else 0)
                assert evaluated["status"] == (
                    "matched" if face == 0 and not expected else "not_matched"
                )
                if radius == 0.4:
                    assert len(expected) >= 11
                rows.append(
                    dict(
                        radius_nm=radius,
                        face=face,
                        model=native_record(model, tmp_path, f"r-{radius}-f-{face}"),
                        result=evaluated,
                    )
                )
        assert before == snapshot()
        output = dict(
            policy=policy,
            input_identity=identity,
            source_unchanged=True,
            rows=rows,
            translation_nm=translation.tolist(),
            original_selected_coordinates_nm=original[list(range(791, 802))].tolist(),
            workflow_attribution=captured.attribution.to_dict(),
        )
        (tmp_path / "prepared_exclusion_results.json").write_text(
            json.dumps(output, indent=2, allow_nan=False) + "\n"
        )
    assert puw.configure.report() == configuration
