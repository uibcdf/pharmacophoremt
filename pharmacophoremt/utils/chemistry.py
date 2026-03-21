import pickle
import os
import requests
from rdkit import Chem
from rdkit.Chem import AllChem
from pathlib import Path

def fix_bond_orders(mol, pdb_id):
    """
    Fix bond orders of a molecule extracted from PDB using a template SMILES.
    """
    # 1. Standardize pdb_id (Rescued rule: 'A' -> 'ADE')
    clean_id = pdb_id.split(":")[0].upper()
    if clean_id == 'A':
        clean_id = 'ADE'

    # 2. Try local mapper
    data_path = Path(__file__).parents[2] / 'data' / 'pdb_to_smi.pickle'
    smiles = None
    if data_path.exists():
        with open(data_path, 'rb') as f:
            mapper = pickle.load(f)
        smiles = mapper.get(clean_id)
    
    # 3. Fallback to online RCSB PDB API
    if not smiles:
        from .chemistry import get_smiles_from_pdb_id
        smiles = get_smiles_from_pdb_id(clean_id)
        
    if smiles:
        template = Chem.MolFromSmiles(smiles)
        if template:
            # Rescued logic: Check atom count consistency before assigning
            if template.GetNumAtoms() != mol.GetNumAtoms():
                # Try to add/remove hydrogens to match count if necessary
                # (Simple fallback for now: return original if mismatch)
                return mol
            try:
                return AllChem.AssignBondOrdersFromTemplate(template, mol)
            except:
                return mol
    return mol

def get_smiles_from_pdb_id(pdb_id):
    """Fetch canonical SMILES from RCSB PDB."""
    clean_id = pdb_id.split(":")[0].upper()
    url = f"https://data.rcsb.org/rest/v1/core/chemcomp/{clean_id}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            for desc in data.get('rcsb_chem_comp_descriptor', []):
                if desc.get('type') == 'SMILES_CANONICAL' and desc.get('program') == 'CACTVS':
                    return desc.get('descriptor')
    except:
        pass
    return None
