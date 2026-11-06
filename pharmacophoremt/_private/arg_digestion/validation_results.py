"""Public result contracts; native evaluators retain their option domains."""

from argdigest import DigestConfig, FunctionContract

from pharmacophoremt import _argdigest

CONTRACTS = [
    FunctionContract(
        caller=f"pharmacophoremt.validation.saved_results.{name}", admits="signature"
    )
    for name in ("summarize_screening_results", "compare_screening_results")
] + [
    FunctionContract(
        caller="pharmacophoremt.validation.retrospective.__init__", admits="signature"
    ),
    # The selected evaluator is instance state, not a run argument. Forward its
    # options to its native domain without inventing a self-derived Domain here.
    FunctionContract(
        caller="pharmacophoremt.validation.retrospective.run", admits="any"
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
