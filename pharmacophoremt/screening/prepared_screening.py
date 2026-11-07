"""Incremental native screening with explicit prepared-source correspondence."""

from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._private.arg_digestion.prepared_screening import CONFIG
from pharmacophoremt._private.pose_batch import failure_record
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)

from .conformer_screening import ConformerScreening
from .pose_evaluation import PoseEvaluator
from .rigid_search import RigidPoseSearch
from .scoring import _resolve_score_method, get_screening_score


@dataclass(frozen=True)
class PreparedInput:
    """A declared work/source occurrence and its already prepared molecule.

    Parameters
    ----------
    work_key : str
        Opaque nonempty identifier for this evaluation, also used as the native
        pose ID. The producer supplies globally unique work keys.
    source_key : str
        Opaque nonempty original source reference. Repeated references remain
        distinct declared work; the key does not establish molecular identity.
    occurrence_key : str
        Opaque nonempty source occurrence reference. It may group work expanded
        from an occurrence and does not establish an independent assay sample.
    molecular_system : molecular system
        Already prepared source accepted by the selected native evaluator.

    Notes
    -----
    The record freezes its fields, not the referenced molecular object. Keep
    prepared inputs and evaluator/query settings unchanged during consumption.
    No source authentication, molecular preparation, snapshot or chemical
    equivalence is inferred. Mapping keys and record type are checked when the
    entry is pulled; molecular validity belongs to the native provider boundary.
    Repeated source keys, occurrence keys and molecular handles are allowed.
    """

    work_key: str
    source_key: str
    occurrence_key: str
    molecular_system: object


@signal(tags=["screening", "prepared", "incremental"])
@arg_digest(config=CONFIG)
def screen_prepared(
    inputs,
    evaluator,
    *,
    score_method,
    on_error="raise",
    evaluation_options=None,
):
    """Preflight now, then yield source-linked native outcomes on demand.

    Parameters
    ----------
    inputs : iterable of PreparedInput
        Producer-prepared entries in their intended encounter order. The source
        is not iterated or sampled while constructing the returned iterator.
    evaluator : PoseEvaluator, RigidPoseSearch or ConformerScreening
        Existing native tool with its query and method already selected. Keep
        the evaluator and query unchanged while consuming outcomes.
    score_method : {'checked_pose_coverage', 'seeded_hit'} or None
        Explicit choice passed to the native score resolver. None resolves to
        checked-pose coverage for PoseEvaluator or binary hit for a seed-only
        tool. Legacy rigid/conformer search requires an explicit coverage choice.
        The outcome records the resolved versioned criterion.
    on_error : {'raise', 'record'}, default='raise'
        Raise native evaluation failures, or retain them as unscored outcomes.
        ConformerScreening uses the same policy for its internal frames.
    evaluation_options : mapping or None, optional
        Common native evaluate options, copied before consumption. The selected
        evaluator owns option admission through its public empty-batch run.
        Pose IDs come from work_key; embedded on_error and digestion bypasses
        are refused. Source-dependent selections still need provider access.

    Returns
    -------
    iterator of dict
        One outcome per pulled input with exactly work_key, source_key,
        occurrence_key, native_result, ranking_score and score_method. Native
        evidence retains frame/state/assignment/failure fields and nested IDs.
        The envelope retains no input molecular handle and is not a persistent
        run format. Encounter order is not a global ranking or a hit-only list.

    Notes
    -----
    Decidable plan errors are rejected before calling iter(inputs), including
    empty/one-pass sources. Each pull completes one native evaluation before
    yielding. Valid nonmatches can score zero; failures remain unscored. Only
    native PoseEvaluationError is recordable. Reader, mapping and programming
    errors propagate; previously yielded outcomes remain caller-owned.

    The caller owns readers and their closure/replay policy. Closing the result
    iterator stops further pulls and releases its references; it never explicitly
    closes a caller-owned reader. Normal Python finalization can still close an
    unreferenced source generator. Retain/manage a reader intended for reuse.
    Adapter state retains the current input/result and fixed options; individual
    molecular workload and caller accumulation have their own memory costs.

    No collection-sized uniqueness set, journal, retry, resume or durability
    guarantee is added. Native evaluations capture attribution when actually
    consumed under an application-enabled attribution context. Constructing this
    iterator does not credit a completed screening workflow.

    Examples
    --------
    >>> from contextlib import closing
    >>> entries = [PreparedInput('work:0', 'source:42', 'row:0', prepared_ligand)]
    >>> with closing(screen_prepared(entries, evaluator,
    ...                             score_method='checked_pose_coverage')) as outcomes:
    ...     first = next(outcomes)
    >>> first['source_key']
    'source:42'
    """
    if not isinstance(evaluator, (PoseEvaluator, RigidPoseSearch, ConformerScreening)):
        raise ArgumentError(argument="evaluator", reason="expected a native pose tool")
    if evaluation_options is not None and not isinstance(evaluation_options, Mapping):
        raise ArgumentError(argument="evaluation_options", reason="expected a mapping")
    options = deepcopy(dict(evaluation_options or {}))
    if "skip_digestion" in options:
        raise ArgumentError(
            argument="evaluation_options", reason="digestion bypass is not supported"
        )
    if "on_error" in options:
        raise ArgumentError(
            argument="evaluation_options", reason="pass on_error explicitly"
        )
    method = _resolve_score_method(evaluator, score_method)
    evaluator.run((), on_error=on_error, **options)
    if isinstance(evaluator, ConformerScreening):
        options["on_error"] = on_error

    def outcomes():
        for entry in inputs:
            if not isinstance(entry, PreparedInput):
                raise ArgumentError(
                    argument="inputs", reason="expected PreparedInput entries"
                )
            for name in ("work_key", "source_key", "occurrence_key"):
                if (
                    not isinstance(getattr(entry, name), str)
                    or not getattr(entry, name).strip()
                ):
                    raise ArgumentError(
                        argument=name, reason="expected a nonempty string"
                    )
            try:
                result = evaluator.evaluate(
                    entry.molecular_system, pose_id=entry.work_key, **options
                )
            except PoseEvaluationError as error:
                if on_error == "raise":
                    raise
                result = failure_record(error, entry.work_key)
            yield dict(
                work_key=entry.work_key,
                source_key=entry.source_key,
                occurrence_key=entry.occurrence_key,
                native_result=result,
                ranking_score=get_screening_score(result, score_method=method),
                score_method=method + "@1",
            )

    return outcomes()
