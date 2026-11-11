"""Source-owned effective evaluation around one existing feature extraction."""

import hashlib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._private import feature_capture as receipt
from pharmacophoremt._private.arg_digestion.feature_capture import CONFIG
from pharmacophoremt._private.molsysmt import capability
from pharmacophoremt_features import _payload_schema as spec
from pharmacophoremt_features import _schema
from pharmacophoremt_features._diagnostics import fail

from .features import CLASSICAL_FEATURES


def _producer(owner):
    from pharmacophoremt._version import __version__

    versions = {}
    for name in ("pharmacophoremt", "molsysmt", "numpy", "pyunitwizard"):
        try:
            versions[name] = version(name)
        except PackageNotFoundError:
            versions[name] = None
    try:
        digest = hashlib.sha256(Path(owner.__file__).read_bytes()).hexdigest()
    except OSError:
        digest = None
    return {
        "schema": receipt.PRODUCER_SCHEMA,
        "operation": receipt.OPERATION,
        "distribution_version": versions["pharmacophoremt"],
        "runtime_version": __version__,
        "observed_extractor_sha256": digest,
        "versions": versions,
    }


@signal(tags=["modeling", "features", "capture"])
@arg_digest(config=CONFIG, type_check=False)
def capture_features(
    molecular_system,
    *,
    selection="all",
    structure_index=0,
    chemical_state="reference",
    features=CLASSICAL_FEATURES,
    skip_digestion=False,
):
    """Extract once and retain the effective request, coverage and original producer.

    The separate runtime envelope keeps the ordinary inventory unchanged. At most
    256 source atoms, 64 features and 2 MiB of sealed observation are admitted. Every
    requested family, including included volume, retains completed/evaluated-empty
    coverage; native payload encoding separately refuses unsupported families.
    Provider failures propagate without a successful capture. Source identity is
    caller-owned and must remain unchanged across the existing provider calls.
    """
    from . import features as owner

    requested = receipt.families(features)
    n_atoms = capability("get")(molecular_system, n_atoms=True)
    # MolSysMT may supply a NumPy integer; normalize via the existing int contract.
    from pharmacophoremt._private.arg_digestion.argument._contracts import (
        digest_structure_index,
    )

    n_atoms = digest_structure_index(n_atoms)
    if n_atoms > spec.MAX_ATOMS:
        fail(333)
    receipt.require(n_atoms > 0)
    producer = _producer(owner)
    inventory = owner.get_features(
        molecular_system,
        selection=selection,
        structure_index=structure_index,
        chemical_state=chemical_state,
        features=requested,
    )
    coverage = spec.inventory_layout(
        inventory, n_atoms, requested, records=False, allow_volume=True
    )
    receipt.require(
        type(inventory["structure_index"]) is int
        and inventory["structure_index"] == structure_index
    )
    receipt.require(
        _schema.encoded(inventory["chemical_state"]) == _schema.encoded(chemical_state)
    )
    evaluation = {
        "schema": receipt.EVALUATION_SCHEMA,
        "status": "completed",
        "operation": receipt.OPERATION,
        "definition": inventory["definition"],
        "families": requested,
        "coverage": coverage,
        "n_atoms": n_atoms,
        "selected_atom_indices": list(inventory["selected_atom_indices"]),
        "structure_index": inventory["structure_index"],
        "chemical_state": inventory["chemical_state"],
        "coordinate_policy": "cartesian-no-imaging",
    }
    receipt._inventory(inventory, evaluation)
    return {
        "schema": receipt.SCHEMA,
        "inventory": inventory,
        "evaluation": evaluation,
        "producer": producer,
        "capture_sha256": receipt.binding(inventory, evaluation, producer),
    }
