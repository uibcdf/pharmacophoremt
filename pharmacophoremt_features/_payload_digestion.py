"""Closed payload signatures; scientific field validation stays in its owner."""

from argdigest import DigestConfig, FunctionContract

from . import _payload_schema as spec
from . import _schema
from ._diagnostics import FeatureAssetError, fail
from ._digestion import _identity

OWNER = "pharmacophoremt_features.FeatureInventoryPayload."


def _profile(payload_profile):
    if type(payload_profile) is not str or payload_profile != spec.PAYLOAD_PROFILE:
        fail(301, argument="payload_profile")
    return payload_profile


def _families(value):
    try:
        return spec.declared_families(value)
    except FeatureAssetError as error:
        raise FeatureAssetError(
            code="PHMT-E301", argument="evaluated/required_families"
        ) from error


def _inventory(inventory):
    if type(inventory) is not dict:
        fail(301, argument="inventory")
    return inventory


def _parent(parent):
    if type(parent) is not dict:
        fail(301, argument="parent")
    return parent


def _producer(extraction_producer):
    if extraction_producer is not None and type(extraction_producer) is not dict:
        fail(301, argument="extraction_producer")
    return extraction_producer


def _raw(raw):
    if type(raw) is not bytes or not raw:
        fail(301, argument="raw")
    if len(raw) > _schema.MAX_PAYLOAD_BYTES:
        fail(333)
    return raw


ARGUMENT_DIGESTERS = {
    "self": _identity,
    "cls": _identity,
    "inventory": _inventory,
    "parent": _parent,
    "extraction_producer": _producer,
    "payload_profile": _profile,
    "evaluated_families": _families,
    "required_families": _families,
    "raw": _raw,
}
METHODS = ("from_inventory", "from_bytes", "to_bytes", "describe", "to_inventory")
CONTRACTS = [
    FunctionContract(caller=OWNER + name, admits="signature") for name in METHODS
]


def config(name):
    return DigestConfig(
        digestion_source=__name__,
        digestion_style="registry",
        standardizer=None,
        strictness="error",
        function_source=__name__,
        contract_owner=OWNER + name,
    )
