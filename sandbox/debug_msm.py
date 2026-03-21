
from rdkit import Chem
from rdkit.Chem import AllChem
import molsysmt as msm

smiles = "C1CCNC1C(=O)O"
mol = Chem.MolFromSmiles(smiles)
mol = Chem.AddHs(mol)
AllChem.EmbedMultipleConfs(mol, numConfs=2)

print(f"Type of mol: {type(mol)}")
print(f"Form of mol: {msm.get_form(mol)}")
print(f"Num conformers: {mol.GetNumConformers()}")

try:
    mol2 = msm.convert(mol, to_form='rdkit.Mol')
    print(f"Conversion successful! Type: {type(mol2)}")
    print(f"Num conformers in mol2: {mol2.GetNumConformers()}")
except Exception as e:
    print(f"Conversion failed: {e}")
    import traceback
    traceback.print_exc()
