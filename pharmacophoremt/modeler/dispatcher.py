from argdigest import arg_digest
from smonitor import signal


@signal(tags=["modeler", "dispatch"])
@arg_digest(type_check=True)
def model(
    molecular_system,
    method="complex-based",
    ligand_selection=None,
    receptor_selection=None,
    **kwargs,
):
    """
    Build a pharmacophore through an explicitly configured modeling route.

    The default complex-based route requires ligand_selection and a named
    interaction_collection of cached native MolSysMT observations on the same
    unchanged prepared source. It performs no implicit molecular preparation,
    ligand recognition or interaction detection. Optional structure_indices is
    passed to the modeler's build method. Other native methods keep their own
    prepared-input contracts. Structure-based consumes cached receptor inventories
    and explicit hypothesis projections; it performs no molecular inference.
    """

    if method == "reference-ligand":
        from pharmacophoremt._private.smonitor.exceptions import ArgumentError
        from pharmacophoremt.modeler.reference_ligand import from_ligand

        if receptor_selection is not None or "selection" in kwargs:
            raise ArgumentError(
                argument="reference-ligand",
                reason="use ligand_selection to select the reference ligand",
            )
        return from_ligand(
            molecular_system,
            selection="all" if ligand_selection is None else ligand_selection,
            **kwargs,
        )

    if method == "interaction-based":
        from pharmacophoremt._private.smonitor.exceptions import ArgumentError
        from pharmacophoremt.modeler.interaction_based import from_interactions

        if (
            ligand_selection is None
            or "interactions" not in kwargs
            or receptor_selection is not None
        ):
            raise ArgumentError(
                argument="interaction-based",
                reason="provide interactions and ligand_selection; the complement defines the receptor",
            )
        return from_interactions(
            molecular_system, ligand_selection=ligand_selection, **kwargs
        )

    if method == "interaction-collection":
        from pharmacophoremt._private.smonitor.exceptions import ArgumentError
        from pharmacophoremt.modeler.interaction_collection import (
            from_interaction_collection,
        )

        if (
            ligand_selection is None
            or "interaction_collection" not in kwargs
            or receptor_selection is not None
        ):
            raise ArgumentError(
                argument="interaction-collection",
                reason="provide interaction_collection and ligand_selection; observations define the receptor",
            )
        return from_interaction_collection(
            molecular_system, ligand_selection=ligand_selection, **kwargs
        )

    if method == "ligand-based":
        from pharmacophoremt._private.smonitor.exceptions import ArgumentError
        from pharmacophoremt.modeler.ligand_based import LigandBasedModeler

        if ligand_selection is not None or receptor_selection is not None:
            raise ArgumentError(
                argument="ligand-based",
                reason="declare selections in each prepared ligand record",
            )
        return LigandBasedModeler(molecular_system, **kwargs).build()

    if method == "complex-based":
        from pharmacophoremt.modeler.complex_based import ComplexBasedModeler

        structure_indices = kwargs.pop("structure_indices", None)
        modeler = ComplexBasedModeler(
            molecular_system,
            ligand_selection=ligand_selection,
            receptor_selection=receptor_selection,
            **kwargs,
        )
        return modeler.build(structure_indices=structure_indices)

    elif method == "structure-based":
        from pharmacophoremt._private.smonitor.exceptions import ArgumentError
        from pharmacophoremt.modeler.structure_based import StructureBasedModeler

        if ligand_selection is not None or receptor_selection is not None:
            raise ArgumentError(
                argument="structure-based",
                reason="declare the receptor selection in cached native inventories",
            )
        structure_indices = kwargs.pop("structure_indices", None)
        modeler = StructureBasedModeler(molecular_system, **kwargs)
        return modeler.build(structure_indices=structure_indices)

    else:
        raise NotImplementedError(f"Method '{method}' is not yet implemented.")
