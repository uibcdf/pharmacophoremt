"""Retrospective ranking with stable input accounting and explicit failures."""

import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.screening.virtual_screening import VirtualScreening
from pharmacophoremt.validation.metrics import bedroc, enrichment_factor, roc_auc


class RetrospectiveValidator:
    """Rank labeled inputs without treating calculation failures as negatives.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        Query model.
    min_match_ratio : float, default=1.0
        Essential-weight hit threshold for the legacy screening route.
    evaluator : PoseEvaluator, RigidPoseSearch or ConformerScreening, optional
        Evaluate placed poses or search prepared rigid ligands/conformers.
        The tool's hit criteria apply.
        When absent, retain the existing VirtualScreening route, whose molecular
        preparation and feature matching still await MolSysMT migration.
    """

    @signal(tags=["validation", "retrospective", "init"])
    @arg_digest()
    def __init__(self, pharmacophore, min_match_ratio=1.0, *, evaluator=None):
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
        self.pharmacophore = pharmacophore
        self.evaluator = evaluator

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
        """
        if on_error not in {"raise", "record"}:
            raise ArgumentError(
                argument="on_error", reason="expected 'raise' or 'record'"
            )
        actives, decoys = list(actives), list(decoys)
        systems = actives + decoys
        true_labels = np.array([1] * len(actives) + [0] * len(decoys), dtype=int)
        if self.evaluator is not None:
            evaluations = self.evaluator.run(
                systems, on_error=on_error, **evaluation_options
            )
        else:
            if evaluation_options:
                raise ArgumentError(
                    argument="evaluation_options",
                    reason="options require a native pose evaluator/search",
                )
            screener = VirtualScreening(self.pharmacophore, min_match_ratio=0.0)
            screener.run(systems)
            evaluations = screener.evaluations
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
        scores = np.array([entry["fit_value"] for entry in valid], dtype=float)
        labels = true_labels[indices]
        if self.evaluator is not None:
            hits = [entry["status"] == "matched" for entry in valid]
        else:
            hits = [
                entry["status"] == "matched"
                and entry["fit_value"] > 0
                and entry["essential_match_ratio"] >= self.min_match_ratio
                for entry in valid
            ]
        report = dict(
            n_actives=len(actives),
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
