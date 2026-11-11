"""Definition-owned ArgDigest std contracts, with no filesystem consumption."""

import os
import re
from pathlib import Path

from argdigest import DigestConfig, FunctionContract
from argdigest.core.caller import caller_is_one_of

from phmt_test_support.feature_snapshot import _request
from phmt_test_support.feature_store import MAX_RECORDS

from ._diagnostics import refuse

PREFIX = "pharmacophoremt_features"
OWNERS = {
    "open": PREFIX + ".FeatureAssetView.open",
    "inspect": PREFIX + ".FeatureAssetView.inspect",
    "reuse": "pharmacophoremt.screening.reuse_feature_inventories",
    "page": PREFIX + ".FeatureAssetView.work_items",
    "publish": PREFIX + ".FeatureAssetStore.publish",
}


def _path(path):
    if not isinstance(path, (str, os.PathLike)):
        refuse(1, "path")
    value = os.fspath(path)
    if type(value) is not str or not value or "\x00" in value:
        refuse(1, "path")
    return Path(value)


def _required_hash(value, argument):
    if type(value) is not str or not re.fullmatch("[a-f0-9]{64}", value):
        refuse(2, argument)
    return value


def _generation(generation, caller=None):
    if generation is None and caller_is_one_of(caller, (OWNERS["open"],)):
        return None
    return _required_hash(generation, "generation")


def _expected_generation(expected_generation):
    return _required_hash(expected_generation, "expected_generation")


def _expected_current(expected_current):
    return (
        None
        if expected_current is None
        else _required_hash(expected_current, "expected_current")
    )


def _families(required_families):
    try:
        return tuple(_request(required_families))
    except ValueError as error:
        try:
            refuse(3, "required_families")
        except ValueError as refusal:
            raise refusal from error


def _keys(work_keys):
    if work_keys is None:
        return None
    if (
        type(work_keys) not in (list, tuple)
        or len(work_keys) > MAX_RECORDS
        or any(type(k) is not str or not k or len(k.encode()) > 512 for k in work_keys)
    ):
        refuse(4, "work_keys")
    if len(set(work_keys)) != len(work_keys):
        refuse(4, "work_keys")
    return tuple(work_keys)


def _offset(offset):
    if type(offset) is not int or offset < 0:
        refuse(5, "offset")
    return offset


def _limit(limit):
    if type(limit) is not int or limit < 0:
        refuse(5, "limit")
    return limit


def _attempt(retry_of):
    if retry_of is not None and (
        type(retry_of) is not str or not re.fullmatch("[a-f0-9]{32}", retry_of)
    ):
        refuse(6, "retry_of")
    return retry_of


ARGUMENT_DIGESTERS = {
    "path": _path,
    "generation": _generation,
    "required_families": _families,
    "work_keys": _keys,
    "expected_generation": _expected_generation,
    "expected_current": _expected_current,
    "offset": _offset,
    "limit": _limit,
    "retry_of": _attempt,
}
CONTRACTS = [
    FunctionContract(caller=owner, admits="signature") for owner in OWNERS.values()
]


def config(operation):
    return DigestConfig(
        digestion_source=__name__,
        digestion_style="registry",
        standardizer=None,
        strictness="error",
        function_source=__name__,
        contract_owner=OWNERS[operation],
    )
