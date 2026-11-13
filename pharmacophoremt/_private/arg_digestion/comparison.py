"""Closed public comparison admission; scientific budgets/axes stay native."""

from argdigest import DigestConfig, FunctionContract

from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.smonitor.exceptions import ArgumentError


def model_type(obj):
    from pharmacophoremt.pharmacophore import Pharmacophore

    if not isinstance(obj, Pharmacophore):
        raise ArgumentError(
            argument="pharmacophore/other", reason="expected a native model"
        )
    return obj


def distance_tolerance(obj):
    return _contracts._length(obj, "distance_tolerance", nonnegative=True)


def max_sites(obj):
    return _contracts._positive_integer(obj, "max_sites")


def max_matrix_entries(obj):
    return _contracts._positive_integer(obj, "max_matrix_entries")


ARGUMENT_DIGESTERS = dict(
    pharmacophore=model_type,
    other=model_type,
    distance_tolerance=distance_tolerance,
    max_sites=max_sites,
    max_matrix_entries=max_matrix_entries,
    skip_digestion=_contracts.digest_skip_digestion,
)
CONTRACTS = [
    FunctionContract(
        caller="pharmacophoremt.comparison.compare_pharmacophores", admits="signature"
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
