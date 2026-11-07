"""Closed, definition-owned public contracts using ArgDigest's std route."""

import os
from pathlib import Path

from argdigest import DigestConfig, FunctionContract

from ._diagnostics import ScreeningRunError


def _error(argument, reason):
    raise ScreeningRunError(operation="admit " + argument, reason=reason)


def _unchanged(value):
    return value


def _path(value):
    if not isinstance(value, (str, os.PathLike)):
        _error("path", "expected a string or path-like value")
    raw = os.fspath(value)
    if type(raw) is not str or not raw:
        _error("path", "expected a nonempty text path")
    return Path(raw)


def _key(value):
    if type(value) is not str or not value.strip():
        _error("key", "expected a nonempty opaque string")
    return value


def _optional_key(value):
    return None if value is None else _key(value)


def _query(value):
    if type(value) is not bytes:
        _error("query_bytes", "expected exact saved bytes")
    return value


def _mapping(value):
    if type(value) is not dict:
        _error("mapping", "expected a plain JSON object")
    return value


def _nonnegative(value):
    if type(value) is not int or value < 0:
        _error("integer", "expected a nonnegative integer")
    return value


def _attempt(value):
    if type(value) is not int or value < 1:
        _error("attempt_id", "expected a positive integer")
    return value


def _criterion(value):
    if type(value) is not str or value not in {
        "seeded_hit@1",
        "checked_pose_coverage@1",
    }:
        _error("score_method", "choose an explicit supported versioned criterion")
    return value


def _boolean(value):
    if type(value) is not bool:
        _error("allow_legacy", "expected a boolean")
    return value


ARGUMENT_DIGESTERS = {
    "self": _unchanged,
    "cls": _unchanged,
    "value": _unchanged,
    "path": _path,
    "manifest_path": _path,
    "run_id": _key,
    "parent_run_id": _optional_key,
    "query_bytes": _query,
    "context": _mapping,
    "work_key": _key,
    "ordinal": _nonnegative,
    "attempt_id": _attempt,
    "outcome": _mapping,
    "score_method": _criterion,
    "limit": _nonnegative,
    "allow_legacy": _boolean,
}
_METHODS = {
    "ScreeningRunStore": (
        "create",
        "open",
        "expected",
        "begin",
        "stage",
        "publish",
        "committed",
        "results",
        "attempts",
        "summary",
        "top_results",
    ),
    "ScreeningRunView": ("open", "results", "summary", "top_results"),
}
CONTRACTS = [
    FunctionContract(
        caller=f"pharmacophoremt_results.{owner}.{name}", admits="signature"
    )
    for owner, names in _METHODS.items()
    for name in names
] + [
    FunctionContract(
        caller="pharmacophoremt_results.canonical_json", admits="signature"
    )
]


def config(owner):
    """Select an explicit logical owner so same-named methods stay distinct."""
    return DigestConfig(
        digestion_source=__name__,
        digestion_style="registry",
        standardizer=None,
        strictness="error",
        function_source=__name__,
        contract_owner="pharmacophoremt_results." + owner,
    )
