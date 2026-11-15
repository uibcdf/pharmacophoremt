"""Definition-owned contracts for explicitly migrated native screening helpers.

Keep this list scoped to received public controls. Alignment and scoring retain
their existing contracts until their separate migration is qualified.
"""

from argdigest import DigestConfig, FunctionContract

from pharmacophoremt import _argdigest

CONTRACTS = [
    FunctionContract(
        caller="pharmacophoremt.screening.correspondence.get_correspondences",
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
