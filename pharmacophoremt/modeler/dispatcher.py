from argdigest import arg_digest
from smonitor import signal
import molsysmt as msm
from pharmacophoremt.utils.chemistry import fix_bond_orders

@signal(tags=["modeler", "dispatch"])
@arg_digest(type_check=True)
def model(molecular_system, method='complex-based', ligand_selection=None, 
          receptor_selection=None, **kwargs):
    """
    High-level convenience function to build a pharmacophore model with 
    automatic entity recognition.
    """
    
    # Ensure system is a MolSysMT object
    if isinstance(molecular_system, str):
        system = msm.convert(molecular_system, to_form='molsysmt.MolSys')
    else:
        system = molecular_system
    
    # Unpack list if necessary
    if isinstance(system, (list, tuple)) and len(system) == 1:
        system = system[0]

    if method == 'complex-based':
        # 1. Automatic Ligand Recognition (Rescued from legacy get_pharmacophore.py)
        if ligand_selection is None:
            # Try to find the first small molecule
            small_mols = msm.select(system, selection='molecule_type == "small molecule"')
            if len(small_mols) > 0:
                ligand_selection = 'molecule_type == "small molecule"'
                # Get PDB ID to fix bond orders
                resnames = msm.get(system, element='group', selection=small_mols, name=True)
                # Note: fix_bond_orders will be called inside ComplexBasedModeler
            else:
                raise ValueError("No ligand found automatically. Please provide 'ligand_selection'.")

        if receptor_selection is None:
            receptor_selection = 'molecule_type == "protein"'

        from pharmacophoremt.modeler.complex_based import ComplexBasedModeler
        modeler = ComplexBasedModeler(system, ligand_selection=ligand_selection, 
                                      receptor_selection=receptor_selection, **kwargs)
        return modeler.build()
    
    elif method == 'ligand-based':
        from pharmacophoremt.modeler.ligand_based import LigandBasedModeler
        modeler = LigandBasedModeler(system, **kwargs)
        return modeler.build()
    
    else:
        raise NotImplementedError(f"Method '{method}' is not yet implemented.")
