"""Definition-owned closed argument contracts for native reference queries."""

from argdigest import DigestConfig, FunctionContract

from pharmacophoremt import _argdigest

CONTRACTS = [
    FunctionContract(
        caller="pharmacophoremt.modeler.reference_ligand.from_feature_inventory",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.modeler.reference_ligand.from_ligand",
        admits="signature",
    ),
]

CONFIG = DigestConfig(
    digestion_source=_argdigest.DIGESTION_SOURCE,
    digestion_style=_argdigest.DIGESTION_STYLE,
    standardizer=_argdigest.STANDARDIZER,
    strictness=_argdigest.STRICTNESS,
    skip_param=_argdigest.SKIP_PARAM,
    function_source=__name__,
    contract_owner="definition",
)
