"""Cross-method support and deliberate input multiplicity, not activity evidence.

All molecular construction uses MolSysMT. Repeated sources are explicit caller
declarations in analytical controls, never inferred chemical equivalence.
"""

import json

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.io import load_json, load_yaml, to_json, to_yaml
from pharmacophoremt.modeler import (
    from_aligned_ligand_cliques,
    from_aligned_ligands,
    from_rigid_ligands,
)
from pharmacophoremt.screening import PoseEvaluator
from phmt_test_support.absence_inputs import system

POLICIES = [["nm", "ps", "radians"], ["pm", "fs", "degrees"]]
CHARGES = ["positive charge", "negative charge"]


def charge_cohort():
    sources = [
        system("[Na+].[Cl-]", [[0, 0, 0], [0.3, 0, 0]]),
        system("[Na+]", [[0, 0, 0]]),
        system("[Cl-]", [[0.3, 0, 0]]),
    ]
    return [
        dict(ligand_id=name, molecular_system=source)
        for name, source in zip(["a", "b", "c"], sources)
    ]


def build(ligands, method, **options):
    if method == "reference":
        return [from_aligned_ligands(ligands, **options)]
    if method == "cliques":
        return from_aligned_ligand_cliques(ligands, **options)["models"]
    return from_rigid_ligands(ligands, min_matches=4, min_sites=4, **options)["models"]


def supporters(site):
    return {member["ligand_id"] for member in site.metadata["members"]}


@pytest.mark.parametrize("policy", POLICIES)
def test_same_cohort_distinguishes_marginal_site_support_from_joint_hypothesis_support(
    policy,
):
    with puw.context(standard_units=policy):
        ligands = charge_cohort()
        options = dict(features=CHARGES, distance_tolerance=".02 nm", radius=".02 nm")
        reference = build(ligands, "reference", **options)[0]
        assert reference.n_interaction_sites == 2
        by_kind = {
            site.feature_name: supporters(site) for site in reference.interaction_sites
        }
        assert by_kind == {"positive charge": {"a", "b"}, "negative charge": {"a", "c"}}
        assert set.intersection(*by_kind.values()) == {"a"}
        assert all(
            site.metadata["support_count"] == 2 for site in reference.interaction_sites
        )
        assert [
            PoseEvaluator(reference).evaluate(entry["molecular_system"])["status"]
            for entry in ligands
        ] == ["matched", "not_matched", "not_matched"]

        alternatives = build(ligands, "cliques", **options)
        assert len(alternatives) == 2
        assert {
            model.interaction_sites[0].feature_name for model in alternatives
        } == set(CHARGES)
        for model in alternatives:
            assert model.n_interaction_sites == 1
            common = supporters(model.interaction_sites[0])
            assert len(common) == 2
            assert set(model.metadata["hypothesis"]["joint_ligand_ids"]) == common
            assert model.metadata["hypothesis"]["joint_support_count"] == 2
            matched = {
                entry["ligand_id"]
                for entry in ligands
                if PoseEvaluator(model).evaluate(entry["molecular_system"])["status"]
                == "matched"
            }
            assert matched == common


@pytest.mark.parametrize("method", ["reference", "cliques"])
@pytest.mark.parametrize("policy", POLICIES)
def test_repeated_prepared_source_under_new_id_can_change_model_eligibility(
    method, policy
):
    with puw.context(standard_units=policy):
        ligands = charge_cohort()
        options = dict(
            features=CHARGES,
            min_support=3,
            distance_tolerance=".02 nm",
            radius=".02 nm",
        )
        if method == "reference":
            with pytest.raises(
                ArgumentError, match="no supported geometrically consistent"
            ):
                build(ligands, method, **options)
        else:
            assert build(ligands, method, **options) == []
        # Intentional repeat of one known source, not an identity/comparison routine.
        repeated = ligands + [
            dict(ligand_id="b-repeat", molecular_system=ligands[1]["molecular_system"])
        ]
        models = build(repeated, method, **options)
        assert len(models) == 1 and models[0].n_interaction_sites == 1
        site = models[0].interaction_sites[0]
        assert site.feature_name == "positive charge"
        assert supporters(site) == {"a", "b", "b-repeat"}
        assert site.metadata["support_count"] == 3
        assert site.metadata["support_fraction"] == 0.75
        assert site.essential is True and site.weight == 1


@pytest.mark.parametrize("method", ["reference", "cliques"])
@pytest.mark.parametrize("policy", POLICIES)
def test_controlled_multiplicity_moves_feature_mean_without_increasing_site_weight(
    method, policy
):
    with puw.context(standard_units=policy):
        ligands = [
            dict(ligand_id="a", molecular_system=system("[Na+]", [[0, 0, 0]])),
            dict(ligand_id="b", molecular_system=system("[Na+]", [[0.06, 0, 0]])),
        ]
        options = dict(
            features=["positive charge"], distance_tolerance=".1 nm", radius=".1 nm"
        )
        original = build(ligands, method, **options)[0].interaction_sites[0]
        repeated = ligands + [
            dict(ligand_id="b-repeat", molecular_system=ligands[1]["molecular_system"])
        ]
        changed = build(repeated, method, **options)[0].interaction_sites[0]
        np.testing.assert_allclose(
            puw.get_value(original.center, to_unit="nm"), [0.03, 0, 0]
        )
        np.testing.assert_allclose(
            puw.get_value(changed.center, to_unit="nm"), [0.04, 0, 0]
        )
        assert (
            original.metadata["support_count"] == 2
            and changed.metadata["support_count"] == 3
        )
        assert original.essential is changed.essential is True
        assert original.weight == changed.weight == 1


def shared_role_cohort():
    # Four typed features at three centers, with donor/acceptor sharing O atom 1.
    coordinates = [[0.1, 0, 0], [0, 0, 0], [0.3, 0.1, 0], [0.3, 0, 0], [0, 0.4, 0]]
    return [
        dict(ligand_id=name, molecular_system=system("[2H]O.C=O.[Na+]", coordinates))
        for name in ["a", "b"]
    ]


@pytest.mark.parametrize("method", ["reference", "cliques", "rigid"])
@pytest.mark.parametrize("policy", POLICIES)
def test_consensus_occurrence_uniqueness_allows_distinct_roles_sharing_atoms(
    method, policy
):
    with puw.context(standard_units=policy):
        ligands = shared_role_cohort()
        before = [
            puw.get_value(
                msm.get(entry["molecular_system"], coordinates=True), to_unit="nm"
            ).copy()
            for entry in ligands
        ]
        models = build(
            ligands,
            method,
            features=["hb donor", "hb acceptor", "positive charge"],
            distance_tolerance=".02 nm",
            radius=".02 nm",
        )
        assert models
        for model in models:
            assert model.n_interaction_sites == 4
            occurrences = []
            donor, acceptor = None, None
            for site in model.interaction_sites:
                assert supporters(site) == {"a", "b"}
                assert (
                    site.metadata["support_count"] == 2
                    and site.metadata["support_fraction"] == 1
                )
                assert site.essential is True and site.weight == 1
                occurrences.extend(
                    (member["ligand_id"], member["feature_index"])
                    for member in site.metadata["members"]
                )
                atoms = site.metadata["members"][0]["atom_indices"]
                if site.feature_name == "hb donor":
                    donor = atoms
                elif site.feature_name == "hb acceptor" and atoms == [1]:
                    acceptor = atoms
            assert len(occurrences) == len(set(occurrences)) == 8
            assert donor == [1, 0] and acceptor == [1]
            assert all(
                PoseEvaluator(model).evaluate(entry["molecular_system"])["status"]
                == "matched"
                for entry in ligands
            )
        for entry, coordinates in zip(ligands, before):
            np.testing.assert_array_equal(
                puw.get_value(
                    msm.get(entry["molecular_system"], coordinates=True), to_unit="nm"
                ),
                coordinates,
            )


@pytest.mark.parametrize("method", ["reference", "cliques", "rigid"])
@pytest.mark.parametrize("codec", ["json", "yaml"])
@pytest.mark.parametrize("policy", POLICIES)
def test_consensus_support_and_member_decisions_remain_recoverable_after_persistence(
    method, codec, policy, tmp_path
):
    with puw.context(standard_units=policy):
        ligands = shared_role_cohort()
        model = build(
            ligands,
            method,
            features=["hb donor", "hb acceptor", "positive charge"],
            distance_tolerance=".02 nm",
            radius=".02 nm",
        )[0]
        writer, reader = (
            (to_json, load_json) if codec == "json" else (to_yaml, load_yaml)
        )
        path = str(tmp_path / (method + "." + codec))
        writer(model, path)
    with puw.context(standard_units=["angstrom", "ps", "radians"]):
        restored = reader(path)
        assert restored.metadata == model.metadata
        assert restored.n_interaction_sites == model.n_interaction_sites == 4
        for site, original in zip(restored.interaction_sites, model.interaction_sites):
            assert site.metadata == original.metadata
            assert site.features == original.features
            assert site.weight == 1 and site.essential is True
            assert supporters(site) == {"a", "b"}
        if method != "reference":
            assert restored.metadata["hypothesis"]["joint_support_count"] == 2
            assert restored.metadata["hypothesis"]["joint_ligand_ids"] == ["a", "b"]
        json.dumps(restored.metadata, allow_nan=False)
