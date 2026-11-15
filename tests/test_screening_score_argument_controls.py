"""Score admission preserves independent evidence meanings and saved-source custody."""

import importlib
import inspect
import json
from copy import deepcopy

import ackredit
import molsysmt as msm
import numpy as np
import pytest
from argdigest import describe_contract

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.screening import (
    PoseEvaluator,
    RigidPoseSearch,
    get_screening_score,
)
from phmt_test_support.absence_inputs import moved, system
from tests.test_seeded_scoring import ionic_case

SCORING = importlib.import_module("pharmacophoremt.screening.scoring")


def seeded_hit():
    # Analytical saved-evidence control; no molecular search is claimed here.
    return dict(
        status="matched",
        fit_value=0.75,
        pose_evaluated=True,
        assignments=[{"site_index": 0, "atom_indices": [0]}],
        missing_essential_sites=[],
        excluded_volume_clashes=[],
        search=dict(
            method="rigid_triplet_seed_hit@1",
            identity_pose_tested=False,
            n_fitted=1,
            enumeration_complete=False,
        ),
    )


def no_fit_negative():
    return dict(
        status="not_matched",
        fit_value=None,
        pose_evaluated=False,
        search=dict(
            method="rigid_triplet_seed_hit@1",
            identity_pose_tested=False,
            n_fitted=0,
            enumeration_complete=True,
        ),
    )


def test_explicit_required_method_and_definition_owned_closed_public_export():
    assert phmt.screening.get_screening_score is SCORING.get_screening_score
    signature = inspect.signature(get_screening_score)
    control = signature.parameters["skip_digestion"]
    assert control.kind is inspect.Parameter.KEYWORD_ONLY and control.default is False
    assert signature.parameters["score_method"].default is inspect.Parameter.empty
    plan = get_screening_score.digestion_plan
    assert plan.contract_owner == "definition"
    assert plan.contract_caller == SCORING.__name__ + ".get_screening_score"
    assert (
        describe_contract(plan.contracts.resolve(plan.contract_caller), plan.domains)[
            "admits"
        ]
        == "signature"
    )


@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], np.array(True)])
def test_invalid_control_refuses_before_native_scoring(flag, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Invalid controls must refuse before the native scoring body")

    monkeypatch.setattr(SCORING, "digest_score_method", forbidden)
    with pytest.raises(ArgumentError, match="skip_digestion"):
        get_screening_score(
            {"status": "matched", "fit_value": 0.75},
            score_method="checked_pose_coverage",
            skip_digestion=flag,
        )


@pytest.mark.parametrize("flag", [False, True, np.bool_(False), np.bool_(True)])
def test_actual_literal_bypass_and_numpy_control_behavior(flag, monkeypatch):
    seen = []
    original = _contracts._boolean

    def boolean(value, argument):
        if argument == "skip_digestion":
            seen.append(value)
        return original(value, argument)

    monkeypatch.setattr(_contracts, "_boolean", boolean)
    assert (
        get_screening_score(
            {"status": "matched", "fit_value": 0.75},
            score_method="checked_pose_coverage",
            skip_digestion=flag,
        )
        == 0.75
    )
    assert len(seen) == (0 if flag is True else 1)
    if flag is not True:
        assert seen[0] is flag


@pytest.mark.parametrize("skip", [False, True])
def test_unknown_keyword_is_closed_before_native_body(skip, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Unknown keywords cannot enter native scoring")

    monkeypatch.setattr(SCORING, "digest_score_method", forbidden)
    with pytest.raises(TypeError):
        get_screening_score(
            {"status": "failed"},
            score_method="seeded_hit",
            skip_digestion=skip,
            criterion="other",
        )


@pytest.mark.parametrize("skip", [False, True])
def test_method_remains_required_even_for_failed_evidence(skip):
    with pytest.raises(TypeError):
        get_screening_score({"status": "failed"}, skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("method", [None, [], True, "unknown"])
def test_native_criterion_guard_precedes_failed_result_shortcut(skip, method):
    with pytest.raises(ArgumentError, match="score_method"):
        get_screening_score(
            {"status": "failed"}, score_method=method, skip_digestion=skip
        )


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "case",
    [
        "failed_pose",
        "failed_seed",
        "coverage",
        "zero",
        "partial_hit",
        "no_fit_negative",
        "fitted_negative",
    ],
)
def test_independent_score_oracles_preserve_none_zero_partial_coverage_and_binary_hit(
    skip, case
):
    method = "seeded_hit"
    if case.startswith("failed"):
        evidence, expected = {"status": "failed"}, None
        if case == "failed_pose":
            method = "checked_pose_coverage"
    elif case in {"coverage", "zero"}:
        expected = 0.75 if case == "coverage" else 0.0
        evidence = dict(status="not_matched", fit_value=expected)
        method = "checked_pose_coverage"
    elif case == "partial_hit":
        evidence, expected = seeded_hit(), 1.0
    elif case == "no_fit_negative":
        evidence, expected = no_fit_negative(), 0.0
    else:
        evidence, expected = seeded_hit(), 0.0
        evidence.update(status="not_matched", fit_value=0.5)
        evidence["search"]["enumeration_complete"] = True
    before = deepcopy(evidence)
    assert (
        get_screening_score(evidence, score_method=method, skip_digestion=skip)
        == expected
    )
    assert evidence == before


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize(
    "case",
    [
        "unknown_status",
        "unresolved_ensemble",
        "legacy_identity",
        "incomplete_negative",
        "no_fit_hit",
        "missing_pose",
        "missing_assignment",
        "excluded_clash",
    ],
)
def test_scientific_evidence_guards_remain_mandatory_during_bypass(skip, case):
    evidence = seeded_hit()
    if case == "unknown_status":
        evidence["status"] = "unknown"
    elif case == "unresolved_ensemble":
        evidence["ensemble"] = {"score_resolved": False}
    elif case == "legacy_identity":
        evidence["search"]["identity_pose_tested"] = True
    elif case == "incomplete_negative":
        evidence = no_fit_negative()
        evidence["search"]["enumeration_complete"] = False
    elif case == "no_fit_hit":
        evidence = no_fit_negative()
        evidence["status"] = "matched"
    elif case == "missing_pose":
        evidence["pose_evaluated"] = False
    elif case == "missing_assignment":
        evidence["assignments"] = []
    else:
        evidence["excluded_volume_clashes"] = [{"site_index": 0, "atom_index": 0}]
    with pytest.raises(ArgumentError):
        get_screening_score(evidence, score_method="seeded_hit", skip_digestion=skip)


@pytest.mark.parametrize("skip", [False, True])
@pytest.mark.parametrize("value", [None, -0.1, 1.1, float("nan"), True, "0.5"])
def test_native_coverage_requires_a_finite_recorded_fraction(skip, value):
    with pytest.raises(ArgumentError):
        get_screening_score(
            {"status": "matched", "fit_value": value},
            score_method="checked_pose_coverage",
            skip_digestion=skip,
        )


@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_actual_saved_scores_preserve_custody_and_credit_only_the_new_operation(
    unit, monkeypatch
):
    with puw.context(standard_units=[unit, "ps", "radians"]):
        source, query = ionic_case(extra_optional=True)
        displaced = moved(source)
        coordinates = puw.get_value(
            msm.get(source, coordinates=True), to_unit="nm"
        ).copy()
        with phmt.attribution():
            rows = {
                "checked": PoseEvaluator(query).evaluate(source),
                "hit": RigidPoseSearch(
                    query, search_method="seeded_hit", max_trials=6
                ).evaluate(displaced),
                "negative": RigidPoseSearch(query, search_method="seeded_hit").evaluate(
                    system("CCC", [[0, 0, 0], [0.15, 0, 0], [0.3, 0, 0]])
                ),
                "failure": RigidPoseSearch(
                    query, search_method="seeded_hit", max_trials=1
                ).run([displaced], on_error="record")[0],
            }
        saved = json.loads(json.dumps(rows))
        before = deepcopy(saved)
        assert (
            saved["hit"]["fit_value"] == 0.75
            and not saved["hit"]["search"]["enumeration_complete"]
        )
        assert (
            saved["negative"]["fit_value"] is None
            and saved["negative"]["pose_evaluated"] is False
        )

        def forbidden(*args, **kwargs):
            pytest.fail(
                "Scoring saved evidence cannot read, recognize or fit molecules"
            )

        with monkeypatch.context() as patch:
            for name in ("get", "convert", "select", "copy"):
                patch.setattr(msm, name, forbidden)
            patch.setattr(msm.structure, "least_rmsd_fit", forbidden)
            with ackredit.session("score receiving") as application:
                with ackredit.capture("score only") as capture, phmt.attribution():
                    for options in (
                        {},
                        {"skip_digestion": False},
                        {"skip_digestion": True},
                    ):
                        for name, expected in (
                            ("checked", 0.75),
                            ("hit", 1.0),
                            ("negative", 0.0),
                            ("failure", None),
                        ):
                            method = (
                                "checked_pose_coverage"
                                if name == "checked"
                                else "seeded_hit"
                            )
                            assert (
                                get_screening_score(
                                    saved[name], score_method=method, **options
                                )
                                == expected
                            )
                assert ackredit.current_session() is application
        credit = json.dumps(capture.attribution.to_dict())
        assert "pharmacophoremt.screening.scoring.get_screening_score" in credit
        assert "pharmacophoremt.modeler.features.get_features" not in credit
        assert "molsysmt.structure.least_rmsd_fit" not in credit
        assert saved == before
        np.testing.assert_array_equal(
            puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), coordinates
        )
