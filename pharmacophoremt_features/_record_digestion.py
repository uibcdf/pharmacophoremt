"""ArgDigest admission for cold public native archive record tools."""

from argdigest import DigestConfig, FunctionContract

from . import _schema
from ._diagnostics import FeatureAssetError, fail
from ._digestion import _identity, _integer

OWNER = "pharmacophoremt_features.FeatureAssetRecord."


def _key(value):
    try:
        _schema.text(value)
    except (FeatureAssetError, UnicodeError) as error:
        raise FeatureAssetError(
            code="PHMT-E301", argument="work/source/occurrence_key"
        ) from error
    return value


def _payload(payload):
    from ._payload import FeatureInventoryPayload

    if not isinstance(payload, FeatureInventoryPayload):
        fail(301, argument="payload")
    return payload


def _view(view):
    from ._api import FeatureAssetView

    if not isinstance(view, FeatureAssetView):
        fail(301, argument="view")
    return view


def _expected(expected_generation):
    return _schema.digest(expected_generation, argument="expected_generation")


def _status(status):
    if type(status) is not str or status not in _schema.STATES[1:]:
        fail(301, argument="status")
    return status


def _cause(cause):
    if type(cause) is not dict or set(cause) != {"type", "reason"}:
        fail(301, argument="cause")
    for value in cause.values():
        try:
            _schema.text(value, 2048)
        except (FeatureAssetError, UnicodeError) as error:
            raise FeatureAssetError(code="PHMT-E301", argument="cause") from error
    return _schema.detached(cause)


ARGUMENT_DIGESTERS = {
    "self": _identity,
    "cls": _identity,
    "work_key": _key,
    "source_key": _key,
    "occurrence_key": _key,
    "payload": _payload,
    "view": _view,
    "ordinal": _integer,
    "expected_generation": _expected,
    "status": _status,
    "cause": _cause,
}
METHODS = ("from_payload", "from_view", "incomplete", "describe", "payload_bytes")
CONTRACTS = [FunctionContract(caller=OWNER + n, admits="signature") for n in METHODS]


def config(name):
    return DigestConfig(
        digestion_source=__name__,
        digestion_style="registry",
        standardizer=None,
        strictness="error",
        function_source=__name__,
        contract_owner=OWNER + name,
    )
