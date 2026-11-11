"""Argument-only admission; no archive consumption or quantity interpretation."""

from argdigest import DigestConfig, FunctionContract

from pharmacophoremt._private.feature_snapshot_v1 import PAYLOAD_PROFILE
from pharmacophoremt_features import FeatureAssetView, _schema
from pharmacophoremt_features._diagnostics import fail
from pharmacophoremt_features._digestion import _families, _keys


def _view(view):
    if not isinstance(view, FeatureAssetView):
        fail(301, argument="view")
    return view


def _generation(expected_generation):
    return _schema.digest(expected_generation, argument="expected_generation")


def _profile(payload_profile):
    if type(payload_profile) is not str or payload_profile not in (
        PAYLOAD_PROFILE,
        _schema.NATIVE_PAYLOAD_PROFILE,
    ):
        fail(301, argument="payload_profile")
    return payload_profile


ARGUMENT_DIGESTERS = {
    "view": _view,
    "required_families": _families,
    "expected_generation": _generation,
    "work_keys": _keys,
    "payload_profile": _profile,
}
CONTRACTS = [
    FunctionContract(
        caller="pharmacophoremt.screening.feature_reuse.reuse_feature_inventories",
        admits="signature",
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
