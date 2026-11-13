"""Definition-owned closed contracts for native observations and composition."""

from argdigest import DigestConfig, FunctionContract

from pharmacophoremt import _argdigest

CONTRACTS = [
    FunctionContract(
        caller="pharmacophoremt.modeler.interaction_based.from_interactions",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.modeler.interaction_collection.from_interaction_collection",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.modeler.composition.compose_pharmacophores",
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
