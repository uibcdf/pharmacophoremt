"""Constructor option admission for explicitly selected native screening."""

from inspect import Parameter, signature

from argdigest import DigestConfig, Domain, FunctionContract

from pharmacophoremt import _argdigest
from pharmacophoremt.screening.conformer_screening import ConformerScreening
from pharmacophoremt.screening.pose_evaluation import PoseEvaluator
from pharmacophoremt.screening.rigid_search import RigidPoseSearch


def _options(tool):
    return tuple(
        sorted(
            name
            for name, parameter in signature(tool.__init__).parameters.items()
            if name
            not in {"self", "pharmacophore", "point_tolerance", "direction_tolerance"}
            and parameter.kind
            in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY)
        )
    )


domain = Domain(
    name="screening_constructor_options",
    depends_on="screening_method",
    by_value={
        "placed": _options(PoseEvaluator),
        "rigid": _options(RigidPoseSearch),
        "conformers": _options(ConformerScreening),
    },
    description="Native evaluator constructor options; evaluation-time options stay on run().",
)
contract = FunctionContract(
    caller="pharmacophoremt.screening.virtual_screening.__init__",
    admits="screening_constructor_options",
)
CONFIG = DigestConfig(
    digestion_source=_argdigest.DIGESTION_SOURCE,
    digestion_style=_argdigest.DIGESTION_STYLE,
    standardizer=_argdigest.STANDARDIZER,
    strictness=_argdigest.STRICTNESS,
    skip_param=_argdigest.SKIP_PARAM,
    function_source=__name__,
    domain_source=__name__,
    contract_owner="definition",
)
