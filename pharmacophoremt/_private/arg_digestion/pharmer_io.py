"""Definition-owned admission for the public Pharmer projection endpoint."""

from argdigest import DigestConfig, FunctionContract

CONTRACTS = [
    FunctionContract(
        caller="pharmacophoremt.io.pharmer.from_pharmer", admits="signature"
    )
]

CONFIG = DigestConfig(
    argument_digestion=False,
    standardizer=None,
    function_source=__name__,
    contract_owner="definition",
)
