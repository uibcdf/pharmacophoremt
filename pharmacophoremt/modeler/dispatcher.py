import molsysmt as msm
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
    High-level convenience function to build a pharmacophore model with
    automatic entity recognition.
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

    # Ensure system is a MolSysMT object
    if isinstance(molecular_system, str):
        system = msm.convert(molecular_system, to_form="molsysmt.MolSys")
    else:
        system = molecular_system

    # Unpack list if necessary
    if isinstance(system, (list, tuple)) and len(system) == 1:
        system = system[0]

    if method == "complex-based":
        # 1. Automatic Ligand Recognition (Rescued from legacy get_pharmacophore.py)
        if ligand_selection is None:
            # Try to find the first small molecule
            small_mols = msm.select(
                system, selection='molecule_type == "small molecule"'
            )
            if len(small_mols) > 0:
                ligand_selection = 'molecule_type == "small molecule"'
                # Note: fix_bond_orders will be called inside ComplexBasedModeler
            else:
                raise ValueError(
                    "No ligand found automatically. Please provide 'ligand_selection'."
                )

        if receptor_selection is None:
            receptor_selection = 'molecule_type == "protein"'

        from pharmacophoremt.modeler.complex_based import ComplexBasedModeler

        modeler = ComplexBasedModeler(
            system,
            ligand_selection=ligand_selection,
            receptor_selection=receptor_selection,
            **kwargs,
        )
        return modeler.build()

    elif method == "ligand-based":
        from pharmacophoremt.modeler.ligand_based import LigandBasedModeler

        modeler = LigandBasedModeler(molecular_system, **kwargs)
        return modeler.build()

    elif method == "structure-based":
        from pharmacophoremt.modeler.structure_based import StructureBasedModeler

        modeler = StructureBasedModeler(molecular_system, **kwargs)
        return modeler.build()

    else:
        raise NotImplementedError(f"Method '{method}' is not yet implemented.")
