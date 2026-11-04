"""Method-dependent admission for the public modeling facade.

Read keyword names from the owned endpoints, without executing scientific work.
The ligand facade retains its finer consensus-method checks; this domain admits
only their union. Value checks and prepared-input requirements remain downstream.
"""

from inspect import Parameter, signature

from argdigest import AliasTable, DigestConfig, Domain, FunctionContract

from pharmacophoremt import _argdigest
from pharmacophoremt.modeler import (
    ComplexBasedModeler,
    LigandBasedModeler,
    StructureBasedModeler,
    from_aligned_ligand_cliques,
    from_interaction_collection,
    from_interactions,
    from_ligand,
    from_rigid_ligands,
)


def _keywords(function, *excluded):
    # ArgDigest admits this control even when an endpoint signature omits it.
    return {
        name
        for name, parameter in signature(function).parameters.items()
        if name not in excluded
        and parameter.kind in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY)
    } | {_argdigest.SKIP_PARAM}


_INPUTS = ("self", "molecular_system", "ligand_selection", "receptor_selection")
_CONSENSUS_INPUTS = ("ligands", "min_support", "min_sites", "skip_digestion")
domain = Domain(
    name="model_options",
    depends_on="method",
    by_value={
        "reference-ligand": tuple(
            sorted(_keywords(from_ligand, "molecular_system", "selection"))
        ),
        "interaction-based": tuple(sorted(_keywords(from_interactions, *_INPUTS))),
        "interaction-collection": tuple(
            sorted(_keywords(from_interaction_collection, *_INPUTS))
        ),
        "ligand-based": tuple(
            sorted(
                _keywords(LigandBasedModeler.__init__, "self", "molecular_systems")
                | _keywords(from_rigid_ligands, *_CONSENSUS_INPUTS)
                | _keywords(from_aligned_ligand_cliques, *_CONSENSUS_INPUTS)
            )
        ),
        "complex-based": tuple(
            sorted(
                _keywords(ComplexBasedModeler.__init__, *_INPUTS)
                | _keywords(ComplexBasedModeler.build, "self")
            )
        ),
        "structure-based": tuple(
            sorted(
                _keywords(StructureBasedModeler.__init__, *_INPUTS)
                | _keywords(StructureBasedModeler.build, "self")
            )
        ),
    },
    description="Endpoint keyword options by public modeling method; ligand consensus retains its narrower downstream contract.",
)
contract = FunctionContract(
    caller="pharmacophoremt.modeler.dispatcher.model",
    admits="model_options",
)
table = AliasTable(
    applies_to="pharmacophoremt.modeler.dispatcher.model",
    aliases={"system": "molecular_system", "mol_sys": "molecular_system"},
)
CONFIG = DigestConfig(
    digestion_source=_argdigest.DIGESTION_SOURCE,
    digestion_style=_argdigest.DIGESTION_STYLE,
    standardizer=_argdigest.STANDARDIZER,
    strictness=_argdigest.STRICTNESS,
    skip_param=_argdigest.SKIP_PARAM,
    function_source=__name__,
    domain_source=__name__,
    normalization_source=__name__,
    contract_owner="definition",
)
