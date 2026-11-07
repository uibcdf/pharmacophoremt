"""Closed, definition-owned RDKit projection signatures."""

from argdigest import DigestConfig, FunctionContract

CONTRACTS = [
    FunctionContract(caller=f"pharmacophoremt.io.rdkit.{name}", admits="signature")
    for name in ("to_rdkit", "load_rdkit")
]

CONFIG = DigestConfig(
    argument_digestion=False,
    standardizer=None,
    function_source=__name__,
    contract_owner="definition",
)
