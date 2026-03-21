
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
import molsysmt as msm
from pharmacophoremt.modeler.ligand_based import LigandBasedModeler
from pharmacophoremt import pyunitwizard as puw

def test_ligand_based_modeler_conformers():
    # 1. Create two identical molecules (proline)
    smiles = "C1CCNC1C(=O)O"
    mol1 = Chem.MolFromSmiles(smiles)
    mol1 = Chem.AddHs(mol1)
    AllChem.EmbedMultipleConfs(mol1, numConfs=5, randomSeed=42)
    
    mol2 = Chem.MolFromSmiles(smiles)
    mol2 = Chem.AddHs(mol2)
    AllChem.EmbedMultipleConfs(mol2, numConfs=3, randomSeed=43)

    # 2. Wrap them in systems
    systems = [mol1, mol2]

    # 3. Initialize Modeler
    # We want a 3-point pharmacophore that appears in both ligands (min_actives=2)
    modeler = LigandBasedModeler(systems, n_points=3, min_actives=2)
    
    # 4. Build
    ph = modeler.build()
    
    print(f"Pharmacophore name: {ph.name}")
    assert ph.n_interaction_sites == 3
    print("Test with 2 ligands passed!")

    # 5. Test with only 1 ligand and min_actives=2 (should not find consensus)
    systems_1 = [mol1]
    modeler_1 = LigandBasedModeler(systems_1, n_points=3, min_actives=2)
    ph_1 = modeler_1.build()
    print(f"Pharmacophore name with 1 ligand: {ph_1.name}")
    assert ph_1.name == "No Consensus Found"
    assert ph_1.n_interaction_sites == 0
    print("Test with 1 ligand and min_actives=2 passed!")

if __name__ == "__main__":
    test_ligand_based_modeler_conformers()
