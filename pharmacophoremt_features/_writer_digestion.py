"""Definition-owned writer admission without filesystem or source access."""

from argdigest import DigestConfig, FunctionContract
from argdigest.core.caller import caller_is_one_of

from . import _schema
from ._api import FeatureAssetView
from ._diagnostics import fail
from ._digestion import _identity, _path
from ._writer_schema import attempt_id

OWNER = "pharmacophoremt_features.FeatureAssetStore."


def _profile(payload_profile):
    if type(payload_profile) is not str or payload_profile != _schema.SNAPSHOT_PROFILE:
        fail(301, argument="payload_profile")
    return payload_profile


def _view(view):
    if not isinstance(view, FeatureAssetView):
        fail(301, argument="view")
    return view


def _generation(generation, caller=None):
    if generation is None and caller_is_one_of(
        caller,
        (OWNER + "view", "pharmacophoremt_features._writer.FeatureAssetStore.view"),
    ):
        return None
    return _schema.digest(generation, argument="generation")


def _expected(expected_generation):
    return _schema.digest(expected_generation, argument="expected_generation")


def _current(expected_current):
    return (
        None
        if expected_current is None
        else _schema.digest(expected_current, argument="expected_current")
    )


def _attempt(attempt):
    return attempt_id(attempt, argument=True)


def _retry(retry_of):
    return None if retry_of is None else attempt_id(retry_of, argument=True)


ARGUMENT_DIGESTERS = {
    "self": _identity,
    "cls": _identity,
    "path": _path,
    "payload_profile": _profile,
    "view": _view,
    "generation": _generation,
    "expected_generation": _expected,
    "expected_current": _current,
    "attempt": _attempt,
    "retry_of": _retry,
}
METHODS = (
    "create",
    "open",
    "current",
    "view",
    "stage",
    "publish",
    "attempts",
    "inspect_recovery",
    "retry_publication",
    "close",
)
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
