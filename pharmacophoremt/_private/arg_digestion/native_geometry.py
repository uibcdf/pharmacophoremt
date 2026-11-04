"""Signature contracts owned by the four native shape implementations.

The signatures are closed and have no shape-specific aliases or extra keyword
domains. Keep their defining contract when applications inherit these shapes.
"""

from argdigest import DigestConfig, FunctionContract

from pharmacophoremt import _argdigest

CONTRACTS = [
    FunctionContract(
        caller="pharmacophoremt.interaction_site.shape.point.__init__",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.interaction_site.shape.sphere.__init__",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.interaction_site.shape.sphere_and_vector.__init__",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.interaction_site.shape.disk.__init__",
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
