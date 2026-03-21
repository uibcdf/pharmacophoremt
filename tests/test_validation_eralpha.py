import pytest
import os
import pharmacophoremt as phmt
import molsysmt as msm

def test_eralpha_pharmacophore_extraction():
    # 1. Path to migrated data
    current_dir = os.path.dirname(__file__)
    pdb_file = os.path.join(current_dir, 'data/eralpha_complex.pdb')
    
    if not os.path.exists(pdb_file):
        pytest.skip("ERalpha benchmark PDB not found.")

    # Load system explicitly to avoid auto-detection issues in test
    system = msm.convert(pdb_file, to_form='molsysmt.MolSys')

    # 2. Extract using high-level dispatcher (phmt.model)
    # The ligand in this specific PDB file has an empty resname and index 8076
    ph = phmt.model(
        system, 
        method='complex-based',
        ligand_selection='group_index == 8076',
        receptor_selection='molecule_type == "protein"'
    )

    # 3. Scientific Validation
    print(f"\nERalpha Pharmacophore: {ph}")
    assert ph.n_interaction_sites > 0
    
    features = ph.get(get_features=True)
    # flattened features list
    flat_features = []
    for site_feats in features:
        flat_features.extend(site_feats)
    
    assert 'aromatic ring' in flat_features
    assert 'hydrophobicity' in flat_features
