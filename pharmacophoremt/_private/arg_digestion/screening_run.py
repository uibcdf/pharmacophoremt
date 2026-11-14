"""Facade-owned control; native admission stays after the entered-run reset."""

from argdigest import DigestConfig, FunctionContract, register_pipeline

from .argument._contracts import digest_skip_digestion


@register_pipeline(kind="pharmacophoremt", name="screening_run_skip")
def _skip_control(value, context):
    return digest_skip_digestion(value)


SKIP_CONTROL = {"kind": "pharmacophoremt", "rules": ["screening_run_skip"]}
CONTRACTS = [
    FunctionContract(
        caller="pharmacophoremt.screening.virtual_screening.run",
        admits="any",
        description="Native evaluation options retain their owner's post-reset admission.",
    )
]
CONFIG = DigestConfig(
    digestion_style="registry",
    argument_digestion=False,
    standardizer=None,
    strictness="error",
    function_source=__name__,
    contract_owner="definition",
)
