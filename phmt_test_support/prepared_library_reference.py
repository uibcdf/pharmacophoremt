"""Unshipped incremental reference for the public-library design (#108).

This development prototype composes existing native tools. It is not a public
collection API, persistent manifest, checkpoint store or molecular reader.
"""

from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass

from pharmacophoremt._private.pose_batch import failure_record
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)
from pharmacophoremt.screening import (
    ConformerScreening,
    PoseEvaluator,
    RigidPoseSearch,
    get_screening_score,
)
from pharmacophoremt.screening.scoring import _resolve_score_method


@dataclass(frozen=True)
class PreparedInput:
    """Producer-declared work/source occurrence mapping and prepared handle.

    Keys are opaque nonempty strings, not inferred molecular identities.
    Globally unique work keys and unchanged inputs/query are producer
    preconditions; this prototype neither authenticates nor freezes molecules.
    Repeated source keys and repeated molecular handles are allowed.
    """

    work_key: str
    source_key: str
    occurrence_key: str
    molecular_system: object


def screen_prepared(
    inputs,
    evaluator,
    *,
    score_method,
    on_error="raise",
    evaluation_options=None,
):
    """Preflight now, then yield source-linked native evidence on demand.

    The native tool validates options against its own contract on an empty
    batch before this function even calls ``iter(inputs)``. The returned
    generator evaluates one prepared item per pull, with its work key as the
    native pose ID, including nested conformer/failure IDs. Options are copied
    at construction; inputs/query/evaluator settings must remain unchanged while
    consuming. Molecular selection validity still needs actual provider access.

    Results retain no molecular handles, and encounter order is not a global
    ranking. Status and the explicit native score criterion remain independent.
    Only native PoseEvaluationError is recordable; source/adapter/programming
    errors propagate. Already yielded results remain the caller's responsibility.

    The caller owns the source and its closure/replay policy. Closing this
    generator stops pulling and releases its references; it never explicitly
    closes a caller-owned reader. Memory scales with the current molecular
    evaluation, not collection length, unless the caller accumulates outputs.
    No uniqueness set, journal, retry, resume or durability guarantee is added.
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
