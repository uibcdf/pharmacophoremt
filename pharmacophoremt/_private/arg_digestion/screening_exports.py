"""Closed cached-export contracts; Pandas owns destination admission and I/O."""

from argdigest import DigestConfig, FunctionContract

from .argument._contracts import digest_skip_digestion


def _pandas_destination(obj):
    """Preserve the exact path/file-like object for the existing Pandas call."""
    return obj


ARGUMENT_DIGESTERS = {
    "file_name": _pandas_destination,
    "skip_digestion": digest_skip_digestion,
}
CONTRACTS = [
    FunctionContract(
        caller=f"pharmacophoremt.screening.virtual_screening.{name}", admits="signature"
    )
    for name in ("to_dataframe", "to_csv")
]
CONFIG = DigestConfig(
    digestion_source=__name__,
    digestion_style="registry",
    standardizer=None,
    strictness="error",
    function_source=__name__,
    contract_owner="definition",
)
