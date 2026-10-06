"""Compose separately computed native analyses through public modeling tools."""

import molsysmt as msm
import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.arg_digestion.argument.interaction_collection import (
    digest_interaction_collection,
)
from pharmacophoremt._private.smonitor.exceptions import ArgumentError

from .composition import compose_pharmacophores
from .interaction_based import from_interactions


@signal(tags=["modeling", "interactions", "composition"])
@arg_digest()
@attributed("molsysmt")
def from_interaction_collection(
    molecular_system,
    interaction_collection,
    ligand_selection,
    *,
    structure_index=0,
    radius="0.15 nm",
    name=None,
    cation_mapping="exact",
    duplicate_policy="same_participant",
):
    """Build a joint hypothesis from a named collection of cached native analyses.

    Parameters
    ----------
    molecular_system : molecular system
        Same unchanged source used by every MolSysMT analysis.
    interaction_collection : mapping of str to molsysmt.Interactions
        Explicit analysis labels, preserved with original profile/version/evidence.
        All analyses must share source maps, axes, selected frame and one declared
        chemical state. No detector is run here. Evaluated-empty analyses remain
        visible; uncovered frames and any failed conversion raise.
    ligand_selection : MolSysMT selection
        Whole ligand participants, as for `from_interactions`.
    structure_index : int, default=0
        One common evaluated frame in each result's local index space.
    radius : length quantity, default='0.15 nm'
        Common emitted matching radius, independent of detection cutoffs.
    name : str, optional
        Composed query name.
    cation_mapping : {'exact', 'containing_center'}, default='exact'
        Explicit cation-pi conversion policy, passed to each public adapter.
    duplicate_policy : {'same_participant', 'keep'}, default='same_participant'
        Public composition policy. Reuse compatible constraints without adding
        weights. Use `compose_pharmacophores` directly for independently edited
        component radii, flags or weights.

    Returns
    -------
    Pharmacophore
        Joint query with detached labeled component evidence and site mapping.

    Notes
    -----
    No preparation, alignment, molecular recognition implementation or native
    heterogeneous-result merging occurs here. MolSysMT owns those operations.
    Atomic H-bond/hydrophobic conversion currently uses the source reference
    state; those analyses must declare it. Failures never yield a partial query
    or fit value. Completed child attribution may remain in an application capture.
    """
    collection = digest_interaction_collection(interaction_collection)
    first = next(iter(collection.values()))
    states = set()
    atomic = False
    for label, observed in collection.items():
        if (
            observed.source_id != first.source_id
            or observed.n_atoms != first.n_atoms
            or observed.n_structures != first.n_structures
            or not np.array_equal(
                observed.atom_source_indices, first.atom_source_indices
            )
            or not np.array_equal(
                observed.structure_source_indices, first.structure_source_indices
            )
        ):
            raise ArgumentError(
                argument="interaction_collection",
                reason=f"source axes/maps differ for {label}",
            )
        state = observed.parameters.get("chemical_state_index")
        if (
            isinstance(state, (bool, np.bool_))
            or not isinstance(state, (int, np.integer))
            or state < 0
        ):
            raise ArgumentError(
                argument="interaction_collection",
                reason=f"require explicit chemical state for {label}",
            )
        states.add(int(state))
        atomic |= bool({"hydrophobic_contact", "hbond"} & set(observed.relation_types))
    if len(states) != 1:
        raise ArgumentError(
            argument="interaction_collection",
            reason="analyses declare different chemical states",
        )
    if atomic and msm.get(
        molecular_system, reference_chemical_state_index=True
    ) != next(iter(states)):
        raise ArgumentError(
            argument="interaction_collection",
            reason="atomic analysis must use the source reference state",
        )
    components = {
        label: from_interactions(
            molecular_system,
            observed,
            ligand_selection,
            structure_index=structure_index,
            radius=radius,
            cation_mapping=cation_mapping,
            name=label,
        )
        for label, observed in collection.items()
    }
    model = compose_pharmacophores(
        components, duplicate_policy=duplicate_policy, name=name
    )
    model.metadata["interaction_collection"] = dict(
        method="named_native_interaction_collection@1",
        chemical_state_index=next(iter(states)),
        cation_mapping=cation_mapping,
        analyses=[
            dict(
                label=label,
                n_observations=observed.n_interactions,
                evaluated_structure_indices=observed.evaluated_structure_indices.tolist(),
            )
            for label, observed in collection.items()
        ],
    )
    return model
