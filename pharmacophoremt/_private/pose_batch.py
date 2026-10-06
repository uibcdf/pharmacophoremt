"""Shared input identity and failure accounting for native pose tools."""

from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    PoseEvaluationError,
)


def failure_record(error, pose_id):
    """Retain coded failures without manufacturing scientific scores."""
    return dict(
        pose_id=pose_id,
        status="failed",
        fit_value=None,
        error=dict(
            code=error.code,
            message=str(error),
            stage=error.extra.get("stage"),
            cause=type(error.__cause__).__name__,
            cause_code=getattr(error.__cause__, "code", None),
        ),
    )


def run_evaluations(evaluator, molecular_database, on_error, evaluation_options):
    if on_error not in {"raise", "record"}:
        raise ArgumentError(argument="on_error", reason="expected 'raise' or 'record'")
    if "pose_id" in evaluation_options:
        raise ArgumentError(
            argument="pose_id", reason="batch pose IDs are input indices"
        )
    results = []
    for index, system in enumerate(molecular_database):
        try:
            result = evaluator.evaluate(system, pose_id=index, **evaluation_options)
        except PoseEvaluationError as error:
            if on_error == "raise":
                raise
            result = failure_record(error, index)
        results.append(dict(result, input_index=index))
    return results
