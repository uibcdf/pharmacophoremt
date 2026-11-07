"""Definition-owned admission for the public prepared-input iterator.

The source remains borrowed and untouched during admission. Native evaluator
contracts continue to own the contents of ``evaluation_options``; the public
factory forwards those options to the selected tool's empty-batch preflight.
"""

from collections.abc import Mapping

from argdigest import DigestConfig, FunctionContract

from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_evaluator,
    digest_on_error,
    digest_score_method,
)
from pharmacophoremt._private.smonitor.exceptions import ArgumentError


def _borrowed_inputs(value):
    # Even iter(value) can consume a one-shot reader or acquire its resources.
    # Entry/source validation belongs to actual consumption after preflight.
    return value


def _evaluation_options(value):
    if value is not None and not isinstance(value, Mapping):
        raise ArgumentError(argument="evaluation_options", reason="expected a mapping")
    return value


ARGUMENT_DIGESTERS = {
    "inputs": _borrowed_inputs,
    "evaluator": digest_evaluator,
    "score_method": digest_score_method,
    "on_error": digest_on_error,
    "evaluation_options": _evaluation_options,
}

CONTRACTS = [
    FunctionContract(
        caller="pharmacophoremt.screening.prepared_screening.screen_prepared",
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
