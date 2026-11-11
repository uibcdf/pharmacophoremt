"""Closed capture arguments reuse existing extractor value contracts."""

from argdigest import DigestConfig, FunctionContract

from .argument._contracts import (
    digest_chemical_state,
    digest_features,
    digest_skip_digestion,
    digest_structure_index,
)
from .argument.misc import digest_selection
from .argument.molecular_system import digest_molecular_system

ARGUMENT_DIGESTERS = {
    "molecular_system": digest_molecular_system,
    "selection": digest_selection,
    "structure_index": digest_structure_index,
    "chemical_state": digest_chemical_state,
    "features": digest_features,
    "skip_digestion": digest_skip_digestion,
}
CONTRACTS = [
    FunctionContract(
        caller="pharmacophoremt.modeler.feature_capture.capture_features",
        admits="signature",
    )
]
CONFIG = DigestConfig(
    digestion_source=__name__,
    digestion_style="registry",
    standardizer=None,
    strictness="error",
    function_source=__name__,
    contract_owner="definition",
)
