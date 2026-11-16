"""Definition-owned contracts for explicitly migrated native consensus tools."""

from argdigest import DigestConfig, FunctionContract

from pharmacophoremt import _argdigest

CONTRACTS = [
    FunctionContract(
        caller="pharmacophoremt.modeler.aligned_consensus.get_aligned_feature_matches",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.modeler.aligned_consensus.get_consensus_sites",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.modeler.aligned_consensus.from_aligned_ligands",
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
