"""Constructor option admission owned by the selected native consensus tool."""

from inspect import Parameter, signature

from argdigest import DigestConfig, Domain, FunctionContract

from pharmacophoremt import _argdigest
from pharmacophoremt.modeler.aligned_cliques import from_aligned_ligand_cliques
from pharmacophoremt.modeler.rigid_consensus import from_rigid_ligands


def _options(tool):
    return tuple(
        sorted(
            name
            for name, parameter in signature(tool).parameters.items()
            if name not in {"ligands", "min_support", "min_sites", "skip_digestion"}
            and parameter.kind
            in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY)
        )
    )


domain = Domain(
    name="ligand_consensus_options",
    depends_on="consensus_method",
    by_value={
        "rigid": _options(from_rigid_ligands),
        "aligned_cliques": _options(from_aligned_ligand_cliques),
    },
    description="Native consensus options; the facade owns n_points/min_actives and explicit prepared inputs.",
)
contract = FunctionContract(
    caller="pharmacophoremt.modeler.ligand_based.__init__",
    admits="ligand_consensus_options",
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
