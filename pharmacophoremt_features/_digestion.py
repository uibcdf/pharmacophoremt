"""Closed public contracts using ArgDigest's registered standard route."""

import os
from pathlib import Path

from argdigest import DigestConfig, FunctionContract

from . import _schema
from ._diagnostics import fail


def _identity(value):
    return value


def _path(path):
    if not isinstance(path, (str, os.PathLike)):
        fail(301, argument="path")
    raw = os.fspath(path)
    if type(raw) is not str or not raw or "\x00" in raw:
        fail(301, argument="path")
    return Path(raw)


def _generation(generation):
    return (
        None
        if generation is None
        else _schema.digest(generation, argument="generation")
    )


def _families(required_families):
    return _schema.families(required_families, argument=True)


def _keys(work_keys):
    if work_keys is None:
        return None
    if type(work_keys) not in (list, tuple) or len(work_keys) > _schema.MAX_RECORDS:
        fail(301, argument="work_keys")
    try:
        valid = all(
            type(k) is str and k and len(k.encode("utf-8")) <= 512 for k in work_keys
        )
    except UnicodeError as error:
        from ._diagnostics import FeatureAssetError

        raise FeatureAssetError(code="PHMT-E301", argument="work_keys") from error
    if not valid or len(set(work_keys)) != len(work_keys):
        fail(301, argument="work_keys")
    return tuple(work_keys)


def _integer(value):
    if type(value) is not int or value < 0:
        fail(301, argument="ordinal/offset/limit")
    return value


ARGUMENT_DIGESTERS = {
    "self": _identity,
    "cls": _identity,
    "path": _path,
    "generation": _generation,
    "required_families": _families,
    "work_keys": _keys,
    "offset": _integer,
    "limit": _integer,
    "ordinal": _integer,
}
METHODS = (
    "open",
    "generation",
    "summary",
    "work_items",
    "snapshot_bytes",
    "inspect",
    "close",
)
CONTRACTS = [
    FunctionContract(
        caller="pharmacophoremt_features.FeatureAssetView." + name, admits="signature"
    )
    for name in METHODS
]


def config(name):
    return DigestConfig(
        digestion_source=__name__,
        digestion_style="registry",
        standardizer=None,
        strictness="error",
        function_source=__name__,
        contract_owner="pharmacophoremt_features.FeatureAssetView." + name,
    )
