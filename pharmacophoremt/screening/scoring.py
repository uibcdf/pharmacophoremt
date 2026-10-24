"""Explicit ranking criteria over portable native screening evidence."""

import math
from numbers import Real

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_score_method,
)
from pharmacophoremt._private.smonitor.exceptions import ArgumentError


def _resolve_score_method(evaluator, score_method):
    """Choose only a declared tool criterion; legacy search needs explicit consent."""
    from pharmacophoremt.screening.pose_evaluation import PoseEvaluator

    score_method = digest_score_method(score_method)
    seeded = getattr(evaluator, "score_method", None) == "seeded_hit"
    if score_method is None:
        if seeded:
            return "seeded_hit"
        if isinstance(evaluator, PoseEvaluator):
            return "checked_pose_coverage"
        raise ArgumentError(
            argument="score_method",
            reason="rigid/conformer ranking requires search_method='seeded_hit' or explicit score_method='checked_pose_coverage'; legacy partial coverage depends on the input frame",
        )
    if (score_method == "seeded_hit") != seeded:
        raise ArgumentError(
            argument="score_method",
            reason="seeded_hit scores require seed-only search; checked_pose_coverage requires a placed/legacy search with an evaluated pose",
        )
    return score_method


@signal(tags=["screening", "ranking"])
@arg_digest()
@attributed()
def get_screening_score(result, *, score_method):
    """Read an explicit score from native single-input screening evidence.

    ``checked_pose_coverage`` returns the recorded ``fit_value`` of a checked
    pose. It is not an optimum over rigid motions and may depend on input frame.

    ``seeded_hit`` returns 1 for an admissible fitted triplet-seed hit, 0 for a
    completed seed-only negative, and None for a failure. It refuses legacy
    identity-pose searches. It ignores partial coverage, optional-site coverage
    differences and the supplied placement. The criterion is invariant under
    proper changes of input frame within numerical matching tolerances; it does
    not establish exhaustive continuous-pose or conformer coverage, or affinity.

    Input dictionaries are read without mutation. No molecular access, fitting,
    recognition or new credit for a saved source calculation occurs. Attribution
    records this scoring operation itself, independently of source provenance.
    """
    score_method = digest_score_method(score_method)
    if score_method is None:
        raise ArgumentError(
            argument="score_method", reason="choose an explicit criterion"
        )
    if (
        not isinstance(result, dict)
        or not isinstance(result.get("status"), str)
        or result["status"]
        not in {
            "matched",
            "not_matched",
            "failed",
        }
    ):
        raise ArgumentError(
            argument="result", reason="expected native screening evidence"
        )
    if result["status"] == "failed":
        return None
    ensemble = result.get("ensemble")
    if ensemble is not None and (
        not isinstance(ensemble, dict) or ensemble.get("score_resolved") is not True
    ):
        raise ArgumentError(argument="result", reason="unresolved conformer evidence")
    if score_method == "seeded_hit":
        search = result.get("search", {})
        if (
            not isinstance(search, dict)
            or search.get("method") != "rigid_triplet_seed_hit@1"
            or search.get("identity_pose_tested") is not False
        ):
            raise ArgumentError(
                argument="result",
                reason="seeded_hit requires seed-only search evidence",
            )
        fitted = search.get("n_fitted")
        if type(fitted) is not int or fitted < 0:
            raise ArgumentError(argument="result", reason="invalid fitted-pose count")
        if fitted:
            if result.get("pose_evaluated") is not True:
                raise ArgumentError(
                    argument="result", reason="missing fitted-pose evidence"
                )
            _coverage(result)
        elif (
            result.get("pose_evaluated") is not False
            or result.get("fit_value") is not None
        ):
            raise ArgumentError(
                argument="result", reason="no-fit search cannot claim pose coverage"
            )
        if result["status"] == "matched":
            if (
                fitted < 1
                or not result.get("assignments")
                or result.get("missing_essential_sites") != []
                or result.get("excluded_volume_clashes") != []
            ):
                raise ArgumentError(
                    argument="result", reason="a seeded hit requires a fitted pose"
                )
            return 1.0
        if search.get("enumeration_complete") is not True:
            raise ArgumentError(
                argument="result", reason="an incomplete search is not a negative score"
            )
        return 0.0
    return _coverage(result)


def _coverage(result):
    value = result.get("fit_value")
    if (
        isinstance(value, bool)
        or not isinstance(value, Real)
        or not math.isfinite(value)
        or not 0 <= value <= 1
    ):
        raise ArgumentError(
            argument="result",
            reason="expected a checked pose with finite coverage in [0, 1]",
        )
    return float(value)
