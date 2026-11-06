"""Definition-owned native evaluation and batch option contracts.

Domains read each defining evaluate signature lazily, after its class exists.
This avoids a circular import and keeps frame options with their native owner.
An application extending evaluate must also own its corresponding batch API.
"""

from functools import partial
from importlib import import_module
from inspect import Parameter, signature

from argdigest import DigestConfig, Domain, FunctionContract

from pharmacophoremt import _argdigest

_TOOLS = (
    ("pose_evaluation", "PoseEvaluator"),
    ("rigid_search", "RigidPoseSearch"),
    ("conformer_screening", "ConformerScreening"),
)


def _evaluation_options(module, name):
    tool = getattr(import_module(f"pharmacophoremt.screening.{module}"), name)
    return tuple(
        parameter.name
        for parameter in signature(tool.evaluate).parameters.values()
        if parameter.name not in {"self", "molecular_system"}
        and parameter.kind in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY)
    )


DOMAINS = [
    Domain(
        name=f"{module}_evaluation_options",
        members=partial(_evaluation_options, module, name),
        description="Native evaluate options; batch pose IDs remain input indices.",
    )
    for module, name in _TOOLS
]
CONTRACTS = [
    FunctionContract(
        caller=f"pharmacophoremt.screening.{module}.{method}",
        admits=f"{module}_evaluation_options" if method == "run" else "signature",
    )
    for module, _ in _TOOLS
    for method in ("__init__", "evaluate", "run")
]
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
