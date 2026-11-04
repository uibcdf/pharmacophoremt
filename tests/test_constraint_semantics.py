"""Scientific interpretations of native constraints, using real MolSysMT inputs.

Coordinates are analytical fixtures, not experimental or optimized conformers.
These controls establish method behavior, not biological predictive validity.
"""

import json

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import Pharmacophore
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Disk, Point, Sphere, SphereAndVector
from pharmacophoremt.io import load_json, load_yaml, to_json, to_yaml
from pharmacophoremt.modeler import (
    edit_pharmacophore,
    from_interactions,
    from_ligand,
    from_receptor_projections,
    get_features,
)
from pharmacophoremt.screening import (
    PoseEvaluator,
    align_to_pharmacophore,
    get_correspondences,
)
from phmt_test_support.absence_inputs import system
from tests.test_ionic_interactions import CARBOXYLATE, observations

CHARGES = ["positive charge", "negative charge"]
POLICIES = [["nm", "ps", "radians"], ["pm", "fs", "degrees"]]


def charge_query(shape="sphere", reverse=False, centers=((0, 0, 0),)):
    query = Pharmacophore()
    for center in centers:
        position = puw.quantity(center, "nm")
        geometry = Point(position) if shape == "point" else Sphere(position, ".02 nm")
        query.add_interaction_site(
            InteractionSite(geometry, CHARGES[::-1] if reverse else CHARGES)
        )
    return query


@pytest.mark.parametrize("shape", ["point", "sphere"])
@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize(
    "smiles,kind",
    [("[Na+]", "positive charge"), ("[Cl-]", "negative charge"), ("C", None)],
)
def test_site_features_are_alternatives_not_joint_requirements(
    shape, reverse, smiles, kind
):
    query = charge_query(shape, reverse)
    result = PoseEvaluator(query, point_tolerance=".02 nm").evaluate(
        system(smiles, [[0, 0, 0]])
    )
    assert result["status"] == ("matched" if kind else "not_matched")
    assert result["fit_value"] == (1 if kind else 0)
    assert [row["feature"] for row in result["assignments"]] == ([kind] if kind else [])
    assert result["missing_essential_sites"] == ([] if kind else [0])


@pytest.mark.parametrize("second_weight", [0, 1])
def test_feature_alternatives_do_not_duplicate_a_candidate_or_relax_essential_sites(
    second_weight,
):
    query = charge_query(centers=((0, 0, 0), (0, 0, 0)))
    query.interaction_sites[1].weight = second_weight
    result = PoseEvaluator(query).evaluate(system("[Na+]", [[0, 0, 0]]))
    assert result["status"] == "not_matched"
    assert len(result["assignments"]) == len(result["missing_essential_sites"]) == 1
    assert {row["site_index"] for row in result["assignments"]} | set(
        result["missing_essential_sites"]
    ) == {0, 1}
    assert result["fit_value"] == (1 if second_weight == 0 else 0.5)


@pytest.mark.parametrize("policy", POLICIES)
def test_distinct_donor_acceptor_roles_can_share_an_atom(policy):
    with puw.context(standard_units=policy):
        source = system("[2H]O", [[0.1, 0, 0], [0, 0, 0]])
        query = from_ligand(
            source, features=["hb donor", "hb acceptor"], radius=".02 nm"
        )
        result = PoseEvaluator(query).evaluate(source)
        assert result["status"] == "matched" and result["fit_value"] == 1
        assigned = {
            row["feature"]: row["atom_indices"] for row in result["assignments"]
        }
        assert assigned == {"hb donor": [1, 0], "hb acceptor": [1]}
        assert set(assigned["hb donor"]) & set(assigned["hb acceptor"]) == {1}


@pytest.mark.parametrize("policy", POLICIES)
def test_distinct_indexed_hydrogens_share_donor_and_retain_assignment_identity(policy):
    with puw.context(standard_units=policy):
        source = system(
            "[2H]N([3H])C", [[0.1, 0, 0], [0, 0, 0], [0, 0.1, 0], [-0.1, -0.1, 0]]
        )
        query = Pharmacophore()
        for direction in ([1, 0, 0], [0, 1, 0]):
            query.add_interaction_site(
                InteractionSite(
                    SphereAndVector("[0,0,0] nm", ".02 nm", direction), "hb donor"
                )
            )
        evaluator = PoseEvaluator(query, direction_tolerance="0 degrees")
        result = evaluator.evaluate(source)
        assert result["status"] == "matched" and result["fit_value"] == 1
        assert [
            (row["site_index"], row["atom_indices"]) for row in result["assignments"]
        ] == [(0, [1, 0]), (1, [1, 2])]
        # Only the second indexed H changes; the first candidate cannot fill both sites.
        reversed_h = msm.structure.translate(
            source, selection=[2], translation="[0,-.2,0] nm", in_place=False
        )
        negative = evaluator.evaluate(reversed_h)
        assert negative["status"] == "not_matched" and negative["fit_value"] == 0.5
        assert negative["missing_essential_sites"] == [1]
        assert negative["assignments"][0]["atom_indices"] == [1, 0]
        assert evaluator.evaluate(source)["status"] == "matched"


@pytest.mark.parametrize(
    "shape,features,reason",
    [
        (
            SphereAndVector("[0,0,0] nm", ".02 nm", [1, 0, 0]),
            ["hb donor", "hb acceptor"],
            "donor-H",
        ),
        (
            Disk("[0,0,0] nm", [0, 0, 1], ".02 nm"),
            ["aromatic ring", "hydrophobicity"],
            "aromatic-ring",
        ),
        (
            Sphere("[0,0,0] nm", ".02 nm"),
            ["excluded volume", "included volume"],
            "standalone sphere",
        ),
    ],
)
def test_feature_alternatives_do_not_expand_shape_specific_contracts(
    shape, features, reason
):
    query = Pharmacophore()
    query.add_interaction_site(InteractionSite(shape, features))
    with pytest.raises(ArgumentError, match=reason):
        PoseEvaluator(query)


@pytest.mark.parametrize("reverse", [False, True])
def test_correspondence_and_alignment_admit_the_same_alternative_feature_kinds(reverse):
    centers = [[0, 0, 0], [0.3, 0, 0], [0, 0.4, 0]]
    source = system("[Na+].[Cl-].[Na+]", centers)
    query = charge_query(reverse=reverse, centers=centers)
    inventory = get_features(source, features=CHARGES)
    mapping = [
        [
            i,
            next(
                j
                for j, record in enumerate(inventory["features"])
                if record["atom_indices"] == [i]
            ),
        ]
        for i in range(3)
    ]
    proposed = get_correspondences(query, inventory)
    assert proposed["complete"] and mapping in proposed["correspondences"]
    placed = align_to_pharmacophore(source, query, mapping, feature_inventory=inventory)
    assert (
        PoseEvaluator(query).evaluate(placed["molecular_system"])["status"] == "matched"
    )
    assert {row["kind"] for row in placed["alignment"]["participants"]} == set(CHARGES)
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm")[0], centers
    )


def hypothesis(origin):
    if origin == "reference":
        source = system("[Na+]", [[0, 0, 0]])
        return from_ligand(source, features=["positive charge"], radius=".02 nm")
    if origin == "observed":
        source = system("CC(=O)[O-].[Na+].[Na+]", CARBOXYLATE)
        observed = observations(source, [0, 1, 2, 3], [4, 5])
        query = from_interactions(source, observed, [0, 1, 2, 3], radius=".02 nm")
        assert len(query.interaction_sites[0].metadata["observations"]) == 2
        return query
    source = system("[Na+]", [[0, 0, 0]])
    return from_receptor_projections(
        get_features(source, features=["positive charge"]),
        radius=".02 nm",
        projection_specs=[
            dict(
                feature_index=0,
                projection_direction=[0, 1, 0],
                distance=".3 nm",
                label="declared analytical hypothesis",
            )
        ],
    )


@pytest.mark.parametrize("origin", ["reference", "observed", "projected"])
@pytest.mark.parametrize("format", ["json", "yaml"])
@pytest.mark.parametrize("policy", POLICIES)
def test_construction_defaults_and_explicit_curation_keep_distinct_origins_after_persistence(
    origin, format, policy, tmp_path
):
    with puw.context(standard_units=policy):
        query = hypothesis(origin)
        assert query.n_interaction_sites == 1
        site = query.interaction_sites[0]
        assert site.essential is True and site.weight == 1
        assert puw.get_value(site.radius, to_unit="nm") == pytest.approx(0.02)
        curated = edit_pharmacophore(
            query,
            essential=False,
            weight=2,
            reason="declared analytical sensitivity variant",
        )
        assert (
            curated.metadata["policy"]
            == "caller_declared_no_automatic_fit_or_weighting"
        )
        assert curated.metadata["reason"] == "declared analytical sensitivity variant"
        assert curated.metadata["source_model"]["metadata"] == query.metadata
        assert (
            curated.metadata["source_model"]["interaction_sites"][0]["essential"]
            is True
        )
        assert curated.metadata["source_model"]["interaction_sites"][0]["weight"] == 1
        writer, reader = (
            (to_json, load_json) if format == "json" else (to_yaml, load_yaml)
        )
        path = str(tmp_path / (origin + "." + format))
        writer(curated, path)
        restored = reader(path)
        assert restored.metadata == curated.metadata
        assert restored.interaction_sites[0].metadata == site.metadata
        assert restored.interaction_sites[0].essential is False
        assert restored.interaction_sites[0].weight == 2
        assert (
            query.interaction_sites[0].essential is True
            and query.interaction_sites[0].weight == 1
        )
        json.dumps(restored.metadata, allow_nan=False)


def test_evaluation_criteria_explain_site_alternatives_and_assignment_capacity():
    result = PoseEvaluator(charge_query()).evaluate(system("[Na+]", [[0, 0, 0]]))
    assert result["criteria"]["site_feature_logic"] == "any_of"
    assert result["criteria"]["assignment_unit"] == "typed_feature_record"
    assert result["criteria"]["assignment"] == "one_to_one"
    assert result["criteria"]["essential"] == "all"
    assert (
        result["execution"]["matching_method"] == "essential_then_weighted_one_to_one@1"
    )


@pytest.mark.parametrize("format", ["json", "yaml"])
@pytest.mark.parametrize("policy", POLICIES)
def test_native_persistence_preserves_alternative_feature_semantics(
    format, policy, tmp_path
):
    with puw.context(standard_units=policy):
        query = charge_query(reverse=True)
        sources = [system(smiles, [[0, 0, 0]]) for smiles in ("[Na+]", "[Cl-]", "C")]
        before = [PoseEvaluator(query).evaluate(source) for source in sources]
        writer, reader = (
            (to_json, load_json) if format == "json" else (to_yaml, load_yaml)
        )
        path = str(tmp_path / ("alternatives." + format))
        writer(query, path)
        restored = reader(path)
        assert restored.interaction_sites[0].features == CHARGES[::-1]
        assert [
            PoseEvaluator(restored).evaluate(source) for source in sources
        ] == before
        assert [row["status"] for row in before] == [
            "matched",
            "matched",
            "not_matched",
        ]
