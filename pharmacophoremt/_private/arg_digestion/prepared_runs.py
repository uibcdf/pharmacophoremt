"""Definition-owned contracts for saved prepared-screening composition.

Borrowed inputs are never sampled by admission. Native tools own scientific
options, and the result store owns manifest, schema and SQLite validation.
"""

from collections.abc import Mapping
from pathlib import Path

from argdigest import DigestConfig, FunctionContract

from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_on_error,
    digest_score_method,
    digest_screening_method,
)
from pharmacophoremt._private.smonitor.exceptions import ArgumentError


def _identity(value):
    return value


def _path(value):
    try:
        Path(value)
    except TypeError as error:
        raise ArgumentError(
            argument="path", reason="expected a filesystem path"
        ) from error
    return value


def _mapping(value):
    if not isinstance(value, Mapping):
        raise ArgumentError(argument="compatibility", reason="expected a mapping")
    return value


def _options(value):
    if value is not None and not isinstance(value, Mapping):
        raise ArgumentError(argument="options", reason="expected a mapping or None")
    return value


def _plan(value):
    # Called only after the public class exists; defer this import cycle.
    from pharmacophoremt.screening.prepared_runs import PreparedRunPlan

    if not isinstance(value, PreparedRunPlan):
        raise ArgumentError(argument="plan", reason="expected a PreparedRunPlan")
    return value


def _store(value):
    from pharmacophoremt_results import ScreeningRunStore

    if not isinstance(value, ScreeningRunStore):
        raise ArgumentError(argument="ledger", reason="expected a ScreeningRunStore")
    return value


def _key(value):
    if not isinstance(value, str) or not value.strip():
        raise ArgumentError(argument="run_id", reason="expected a nonempty string")
    return value


def _parent(value):
    return None if value is None else _key(value)


def _limit(value):
    if type(value) is not int or value < 0:
        raise ArgumentError(argument="limit", reason="expected a nonnegative integer")
    return value


ARGUMENT_DIGESTERS = {
    "self": _identity,
    "cls": _identity,
    "query_path": _path,
    "path": _path,
    "manifest_path": _path,
    "screening_method": digest_screening_method,
    "score_method": digest_score_method,
    "compatibility": _mapping,
    "constructor_options": _options,
    "evaluation_options": _options,
    "on_error": digest_on_error,
    "ledger": _store,
    "store": _store,
    "inputs": _identity,
    "plan": _plan,
    "run_id": _key,
    "parent_run_id": _parent,
    "work_key": _key,
    "limit": _limit,
}

CONTRACTS = [
    FunctionContract(
        caller=f"pharmacophoremt.screening.prepared_runs.{name}",
        admits="signature",
    )
    for name in (
        "build_prepared_run_plan",
        "resume_prepared_run",
        "new_evaluator",
        "__init__",
        "create",
        "open",
        "resume",
        "attempts",
        "summary",
        "top_results",
    )
]

CONFIG = DigestConfig(
    digestion_source=__name__,
    digestion_style="registry",
    standardizer=None,
    strictness="error",
    function_source=__name__,
    contract_owner="definition",
)
