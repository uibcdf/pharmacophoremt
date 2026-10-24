"""Independent frame, hit/negative, budget and consumer controls for #63."""

import json
from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import Pharmacophore
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
from pharmacophoremt.modeler import from_ligand
from pharmacophoremt.screening import (
    ConformerScreening,
    RigidPoseSearch,
    VirtualScreening,
    get_screening_score,
)
from pharmacophoremt.validation.retrospective import RetrospectiveValidator
from phmt_test_support.absence_inputs import moved, system


def hydrophobic_query():
    query = Pharmacophore()
    for center in ([0, 0, 0], [0.15, 0, 0], [0, 0.15, 0]):
        query.add_interaction_site(
            InteractionSite(
                Sphere(puw.quantity(center, "nm"), ".02 nm"), "hydrophobicity"
            )
        )
    return query


def ionic_case(*, extra_essential=False, extra_optional=False):
    source = system("[Na+].[K+].[Li+]", [[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    query = from_ligand(source, features=["positive charge"], radius=".02 nm")
    if extra_essential or extra_optional:
        query.add_interaction_site(
            InteractionSite(
                Sphere("[5,5,5] nm", ".02 nm"),
                "positive charge" if extra_essential else "negative charge",
                essential=extra_essential,
            )
        )
    return source, query


def test_negative_score_is_invariant_and_pose_coverage_remains_distinct():
    source = system("CCC", [[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0]])
    query = hydrophobic_query()
    original = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    translated = msm.structure.translate(
        source, translation=puw.quantity([[[2, 1, 3]]], "nm"), in_place=False
    )
    legacy = RigidPoseSearch(query)
    assert legacy.evaluate(source)["fit_value"] == pytest.approx(1 / 3)
    assert legacy.evaluate(translated)["fit_value"] == 0
    search = RigidPoseSearch(query, search_method="seeded_hit")
    for ligand in (source, translated, moved(source)):
        result = search.evaluate(ligand)
        assert result["status"] == "not_matched"
        assert result["ranking_score"] == 0
        assert result["fit_value"] is None  # no placed pose was evaluated
        assert result["pose_evaluated"] is False
        assert "assignments" not in result
        assert not result["search"]["identity_pose_tested"]
        assert result["search"]["enumeration_complete"]
        assert result["search"]["n_fitted"] == 0
        json.dumps(result, allow_nan=False)
    np.testing.assert_array_equal(
        original, puw.get_value(msm.get(source, coordinates=True), to_unit="nm")
    )


@pytest.mark.parametrize("negative", [False, True])
def test_fitted_results_are_invariant_under_proper_motion(negative):
    source, query = ionic_case(extra_essential=negative)
    search = RigidPoseSearch(query, search_method="seeded_hit")
    for ligand in (source, moved(source)):
        result = search.evaluate(ligand)
        assert result["ranking_score"] == int(not negative)
        assert result["status"] == ("not_matched" if negative else "matched")
        assert result["fit_value"] == pytest.approx(0.75 if negative else 1)
        assert result["pose_evaluated"] is True
        assert result["search"]["n_fitted"] > 0
        assert not result["search"]["identity_pose_tested"]


def test_binary_hit_proves_maximum_without_unit_coverage_or_complete_enumeration():
    source, query = ionic_case(extra_optional=True)
    # Product order over three same-kind features: first injective triplet is
    # (0,1,2), the sixth raw product. Remaining products exceed this budget.
    search = RigidPoseSearch(query, search_method="seeded_hit", max_trials=6)
    result = search.evaluate(moved(source))
    assert result["status"] == "matched"
    assert result["fit_value"] == pytest.approx(0.75)
    assert result["ranking_score"] == 1
    assert not result["search"]["enumeration_complete"]
    assert result["search"]["termination"] == "hit_found"
    assert result["search"]["n_fitted"] == 1
    failed = RigidPoseSearch(query, search_method="seeded_hit", max_trials=1).run(
        [source], on_error="record"
    )[0]
    assert failed["status"] == "failed" and failed["fit_value"] is None
    assert get_screening_score(failed, score_method="seeded_hit") is None
    assert failed["error"]["stage"] == "search_budget"


def test_exclusion_veto_is_not_a_binary_maximum_even_at_unit_coverage():
    source, query = ionic_case()
    query.add_interaction_site(
        InteractionSite(Sphere("[0,0,0] nm", ".1 nm"), "excluded volume")
    )
    result = RigidPoseSearch(query, search_method="seeded_hit").evaluate(source)
    assert result["fit_value"] == 1 and result["excluded_volume_clashes"]
    assert result["status"] == "not_matched" and result["ranking_score"] == 0
    with pytest.raises(PoseEvaluationError):
        RigidPoseSearch(query, search_method="seeded_hit", max_trials=6).evaluate(
            source
        )


def test_zero_weight_essential_hit_still_scores_above_completed_negatives():
    source, query = ionic_case(extra_optional=True)
    for site in query.interaction_sites[:3]:
        site.weight = 0
    result = RigidPoseSearch(query, search_method="seeded_hit").evaluate(source)
    assert result["status"] == "matched" and result["fit_value"] == 0
    assert result["ranking_score"] == 1


def test_retrospective_uses_binary_scores_preserves_indices_failures_and_ties():
    source, query = ionic_case()
    negative = system("CCC", [[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0]])
    search = RigidPoseSearch(query, search_method="seeded_hit")
    report = RetrospectiveValidator(query, evaluator=search).run(
        [source, moved(source)],
        [negative, moved(negative), "invalid system"],
        on_error="record",
    )
    assert report["score_method"] == "seeded_hit@1"
    assert report["scores"].tolist() == [1, 1, 0, 0]
    assert report["evaluated_indices"].tolist() == [0, 1, 2, 3]
    assert report["n_failed"] == 1
    assert report["failures"][0]["input_index"] == 4
    assert report["AUC"] == report["BEDROC"] == 1
    assert report["evaluations"][2]["fit_value"] is None


def test_legacy_ranking_requires_explicit_checked_pose_criterion():
    source, query = ionic_case()
    for evaluator in (RigidPoseSearch(query), ConformerScreening(query)):
        with pytest.raises(ArgumentError, match="requires"):
            RetrospectiveValidator(query, evaluator=evaluator)
        result = RetrospectiveValidator(
            query, evaluator=evaluator, score_method="checked_pose_coverage"
        ).run([source], [source])
        assert result["AUC"] == 0.5
        assert result["score_method"] == "checked_pose_coverage@1"
    with pytest.raises(ArgumentError, match="requires"):
        VirtualScreening(query, screening_method="rigid")
    with pytest.raises(ArgumentError):
        RetrospectiveValidator(
            query, evaluator=RigidPoseSearch(query), score_method="seeded_hit"
        )
    with pytest.raises(ArgumentError):
        RetrospectiveValidator(
            query,
            evaluator=RigidPoseSearch(query, search_method="seeded_hit"),
            score_method="checked_pose_coverage",
        )


def test_conformer_scores_and_facade_use_the_same_binary_criterion():
    source, query = ionic_case(extra_optional=True)
    source.structures.append(coordinates=msm.get(moved(source), coordinates=True))
    screen = ConformerScreening(query, search_method="seeded_hit", max_trials=6)
    result = screen.evaluate(source, structure_indices=[1, 0])
    assert result["ranking_score"] == 1 and result["fit_value"] == 0.75
    assert result["best_conformer_index"] == 1
    assert result["ensemble"]["ranking"] == "seeded_hit_first_requested_tie"
    facade = VirtualScreening(
        query, screening_method="conformers", search_method="seeded_hit"
    )
    hits = facade.run([source, source])
    assert [hit["input_index"] for hit in hits] == [0, 1]
    assert all(hit["ranking_score"] == 1 for hit in hits)
    assert all(hit["score_method"] == "seeded_hit@1" for hit in hits)
    frame = facade.to_dataframe()
    assert frame["ranking_score"].tolist() == [1, 1]
    assert frame["fit_value"].tolist() == [0.75, 0.75]


def test_empty_seed_conformer_has_no_fabricated_pose_and_remains_a_valid_zero():
    source = system("CCC", [[0, 0, 0], [0.15, 0, 0], [0.30, 0, 0]])
    source.structures.append(coordinates=msm.get(moved(source), coordinates=True))
    result = ConformerScreening(
        hydrophobic_query(), search_method="seeded_hit"
    ).evaluate(source, structure_indices=[1, 0])
    assert result["status"] == "not_matched" and result["ranking_score"] == 0
    assert result["fit_value"] is None and result["pose_coordinates"] is None
    assert result["best_conformer_index"] == 1
    assert result["ensemble"]["complete"] and result["ensemble"]["score_resolved"]


def test_failed_conformer_is_resolved_only_by_a_binary_hit(monkeypatch):
    source, query = ionic_case(extra_optional=True)
    source.structures.append(coordinates=msm.get(source, coordinates=True))
    for hit in (False, True):
        screen = ConformerScreening(query, search_method="seeded_hit")
        evaluate = screen.search.evaluate

        def injected(system, **options):
            if options["structure_index"] == 1:
                raise PoseEvaluationError(
                    pose_id=options["pose_id"],
                    stage="control",
                    reason="independent failure injection",
                )
            result = evaluate(system, **options)
            if not hit:
                result = dict(result, status="not_matched", ranking_score=0)
                result["search"] = dict(result["search"], enumeration_complete=True)
            return result

        monkeypatch.setattr(screen.search, "evaluate", injected)
        result = screen.evaluate(source, on_error="record")
        assert not result["ensemble"]["complete"]
        assert result["ensemble"]["score_resolved"] == hit
        if hit:
            assert result["ranking_score"] == 1 and result["fit_value"] == 0.75
        else:
            assert result["status"] == "failed" and result["ranking_score"] is None
            assert result["best_observed"]["status"] == "not_matched"


def test_saved_score_is_detached_and_does_not_reach_molecular_tools(monkeypatch):
    source, query = ionic_case()
    result = RigidPoseSearch(query, search_method="seeded_hit").evaluate(source)
    saved = json.loads(json.dumps(result))
    before = deepcopy(saved)

    def forbidden(*args, **kwargs):
        pytest.fail("Scoring saved evidence must not perform molecular work")

    monkeypatch.setattr(msm, "convert", forbidden)
    monkeypatch.setattr(msm, "get", forbidden)
    assert get_screening_score(saved, score_method="seeded_hit") == 1
    assert saved == before
    saved["search"]["identity_pose_tested"] = True
    with pytest.raises(ArgumentError):
        get_screening_score(saved, score_method="seeded_hit")


def test_saved_scoring_credits_only_its_new_operation_in_real_sessions():
    import ackredit

    import pharmacophoremt as phmt

    source, query = ionic_case()
    saved = RigidPoseSearch(query, search_method="seeded_hit").evaluate(source)
    with ackredit.session("score reader") as application:
        with ackredit.capture("scoring") as capture, phmt.attribution():
            assert get_screening_score(saved, score_method="seeded_hit") == 1
            assert (
                get_screening_score(
                    json.loads(json.dumps(saved)), score_method="seeded_hit"
                )
                == 1
            )
        assert ackredit.current_session() is application
    payload = capture.attribution.to_dict()
    text = json.dumps(payload)
    assert "pharmacophoremt.screening.scoring.get_screening_score" in text
    assert "pharmacophoremt.modeler.features.get_features" not in text
    assert "molsysmt.structure.least_rmsd_fit" not in text


@pytest.mark.parametrize(
    "patch",
    [
        {"fit_value": 0.5},
        {"pose_evaluated": True},
        {"search": {"n_fitted": True}},
        {"search": {"n_fitted": -1}},
        {"search": {"enumeration_complete": False}},
        {"search": {"identity_pose_tested": True}},
        {"search": []},
        {"ensemble": []},
        {"status": []},
    ],
)
def test_scoring_refuses_incomplete_or_contradictory_saved_evidence(patch):
    saved = dict(
        status="not_matched",
        fit_value=None,
        pose_evaluated=False,
        search=dict(
            method="rigid_triplet_seed_hit@1",
            n_fitted=0,
            enumeration_complete=True,
            identity_pose_tested=False,
        ),
    )
    if isinstance(patch.get("search"), dict):
        saved["search"].update(patch["search"])
    else:
        saved.update(patch)
    with pytest.raises(ArgumentError):
        get_screening_score(saved, score_method="seeded_hit")


@pytest.mark.parametrize("method", [None, [], True, "unknown"])
def test_new_method_contracts_reject_unknown_or_implicit_choices(method):
    with pytest.raises(ArgumentError):
        RigidPoseSearch(hydrophobic_query(), search_method=method)
    with pytest.raises(ArgumentError):
        get_screening_score({"status": "failed"}, score_method=method)
