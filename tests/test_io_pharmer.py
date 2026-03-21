import pytest
import os
from pharmacophoremt import Pharmacophore

def test_load_from_pharmer():
    # Use the data file included in the package
    current_dir = os.path.dirname(__file__)
    pharmer_file = os.path.join(current_dir, '../pharmacophoremt/data/pharmer.json')
    
    ph = Pharmacophore(pharmer_file, form='pharmer')
    
    assert ph.n_interaction_sites == 19
    # Check for some expected features
    features = ph.get(get_features=True)
    flat_features = [f for sublist in features for f in sublist]
    assert 'aromatic ring' in flat_features
    assert 'hydrophobicity' in flat_features
