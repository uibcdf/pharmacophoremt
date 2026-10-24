"""Retrospective ranking with stable input accounting and explicit failures."""

import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.arg_digestion.argument._contracts import digest_evaluator
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.screening.scoring import _resolve_score_method, get_screening_score
from pharmacophoremt.validation.metrics import bedroc, enrichment_factor, roc_auc


class RetrospectiveValidator:
    """Rank labeled inputs without treating calculation failures as negatives.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        Query model.
    min_match_ratio : float, default=1.0
        Inert historical default. Other values are refused; the evaluator owns
        essential-site and weighted-coverage hit criteria.
    evaluator : PoseEvaluator, RigidPoseSearch or ConformerScreening
        Evaluate placed poses or search prepared rigid ligands/conformers.
        The tool's hit criteria apply.
        Required explicit tool. No molecular preparation or legacy fallback.
    score_method : {'checked_pose_coverage', 'seeded_hit'} or None
        Placed evaluation defaults to checked coverage; a seed-only tool selects
        its declared binary criterion. Legacy rigid/conformer partial coverage
        requires explicit checked_pose_coverage consent and is not frame invariant.
    """

    @signal(tags=["validation", "retrospective", "init"])
    @arg_digest()
    def __init__(
        self, pharmacophore, min_match_ratio=1.0, *, evaluator=None, score_method=None
    ):
        try:
            self.min_match_ratio = float(min_match_ratio)
        except (TypeError, ValueError) as error:
            raise ArgumentError(
                argument="min_match_ratio", reason="expected a fraction in [0, 1]"
            ) from error
        if (
            isinstance(min_match_ratio, (bool, np.bool_))
            or not np.isfinite(self.min_match_ratio)
            or not 0 <= self.min_match_ratio <= 1
        ):
            raise ArgumentError(
                argument="min_match_ratio", reason="expected a fraction in [0, 1]"
            )
        if self.min_match_ratio != 1:
            raise ArgumentError(
                argument="min_match_ratio",
                reason="only the inert default is supported; choose the native evaluator's hit criteria",
            )
        evaluator = digest_evaluator(evaluator)
        if evaluator is None:
            raise ArgumentError(
                argument="evaluator",
                reason="supply an explicit prepared-native evaluator/search with run()",
            )
        self.pharmacophore = pharmacophore
        self.evaluator = evaluator
        self.score_method = _resolve_score_method(evaluator, score_method)

    @signal(tags=["validation", "retrospective", "run"])
    @arg_digest()
    @attributed("numpy")
    def run(
        self,
        actives,
        decoys,
        ef_fractions=(0.01, 0.05, 0.10),
        bedroc_alpha=20.0,
        skip_digestion=False,
        *,
        on_error="raise",
        **evaluation_options,
    ):
        """Return ranking metrics and per-input evaluation records.

        Inputs are materialized once, so generators and repeated objects retain
        independent indices. ``on_error='raise'`` is the default. Explicit
        ``on_error='record'`` excludes failures from metrics and reports the
        evaluated indices, original class counts and failure counts. A batch
        with no evaluable inputs raises. Single-class AUC/BEDROC remain NaN.
        Additional options apply only to the native evaluator/search tool.
        Scores follow score_method, never an implicit substitution of coverage
        for a molecular score. Valid seed-only negatives may have fit_value=None
        because no pose was fitted; their binary score is zero, not a failure.
        """
        if on_error not in {"raise", "record"}:
            raise ArgumentError(
                argument="on_error", reason="expected 'raise' or 'record'"
            )
        actives, decoys = list(actives), list(decoys)
        systems = actives + decoys
        true_labels = np.array([1] * len(actives) + [0] * len(decoys), dtype=int)
        evaluations = self.evaluator.run(
            systems, on_error=on_error, **evaluation_options
        )
        failures = [entry for entry in evaluations if entry["status"] == "failed"]
        if failures and on_error == "raise":
            failed = failures[0]
            raise PoseEvaluationError(
                pose_id=failed["input_index"],
                stage=failed["error"].get("stage", "screening"),
                reason=failed["error"]["message"],
            )
        valid = [entry for entry in evaluations if entry["status"] != "failed"]
        if not valid:
            raise ArgumentError(
                argument="dataset", reason="no successfully evaluated inputs"
            )
        indices = np.array([entry["input_index"] for entry in valid], dtype=int)
        scores = np.array(
            [
                get_screening_score(entry, score_method=self.score_method)
                for entry in valid
            ],
            dtype=float,
        )
        labels = true_labels[indices]
        hits = [entry["status"] == "matched" for entry in valid]
        report = dict(
            n_actives=len(actives),
            score_method=self.score_method + "@1",
            n_decoys=len(decoys),
            n_evaluated=len(valid),
            n_failed=len(failures),
            n_actives_evaluated=int(labels.sum()),
            n_decoys_evaluated=int((labels == 0).sum()),
            n_actives_found=int(np.sum(labels.astype(bool) & hits)),
            AUC=roc_auc(labels, scores),
            BEDROC=bedroc(labels, scores, alpha=bedroc_alpha),
            scores=scores,
            labels=labels,
            evaluated_indices=indices,
            failures=failures,
            evaluations=evaluations,
        )
        for fraction in ef_fractions:
            key = f"EF@{100 * fraction:g}%"
            report[key] = enrichment_factor(labels, scores, fraction=fraction)
        return report
