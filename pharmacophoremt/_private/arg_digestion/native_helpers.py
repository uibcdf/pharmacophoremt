"""Definition-owned contracts for explicitly migrated native screening helpers.

Keep this list scoped to explicitly migrated public controls. Other public
screening tools retain their separate admission and receiving work.
"""

from argdigest import DigestConfig, FunctionContract

from pharmacophoremt import _argdigest

CONTRACTS = [
    FunctionContract(
        caller="pharmacophoremt.screening.correspondence.get_correspondences",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.screening.alignment.align_to_pharmacophore",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.screening.scoring.get_screening_score",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.screening.feature_geometry.evaluate_feature_correspondence",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.screening.rigid_placements.get_rigid_feature_placements",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.screening.rigid_refinement.refine_rigid_feature_correspondences",
        admits="signature",
    ),
    FunctionContract(
        caller="pharmacophoremt.screening.rigid_correspondence.get_rigid_feature_correspondences",
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
