import pytest
import os
import numpy as np
import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw

def test_ligandscout_roundtrip(tmp_path):
    # 1. Create a dummy .pml file
    pml_content = """<?xml version="1.0" encoding="UTF-8"?>
<pharmacophore>
    <feature type="HBD" id="1">
        <position x="1.0" y="2.0" z="3.0" tolerance="1.5"/>
        <direction x="0.0" y="0.0" z="1.0"/>
    </feature>
    <feature type="H" id="2">
        <position x="5.0" y="5.0" z="5.0" tolerance="2.0"/>
    </feature>
</pharmacophore>
"""
    pml_file = tmp_path / "test.pml"
    pml_file.write_text(pml_content)

    # 2. Import
    ph = phmt.io.from_ligandscout(str(pml_file))
    assert ph.n_interaction_sites == 2
    
    # Check HBD
    site0 = ph.interaction_sites[0]
    assert 'hb donor' in site0.features
    center = puw.get_value(site0.center, to_unit='nm')
    assert np.allclose(center, [0.1, 0.2, 0.3])

    # 3. Export and Re-import
    out_file = tmp_path / "output.pml"
    phmt.io.to_ligandscout(ph, str(out_file))
    
    ph2 = phmt.io.from_ligandscout(str(out_file))
    assert ph2.n_interaction_sites == 2
    assert ph2.interaction_sites[0].features == ph.interaction_sites[0].features
