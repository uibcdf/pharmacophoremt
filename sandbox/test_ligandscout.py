import pharmacophoremt as phmt
import os
import numpy as np
from pharmacophoremt import pyunitwizard as puw

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
    <feature type="AR" id="3">
        <position x="10.0" y="0.0" z="0.0" tolerance="1.2"/>
        <direction x="1.0" y="0.0" z="0.0"/>
    </feature>
</pharmacophore>
"""

pml_file = 'sandbox/test_input.pml'
with open(pml_file, 'w') as f:
    f.write(pml_content)

print(f"Created dummy PML: {pml_file}")

# 2. Import
ph = phmt.io.from_ligandscout(pml_file)
print(f"\nImported Pharmacophore: {ph}")
print(f"Number of sites: {ph.n_interaction_sites}")

# 3. Verify
df = ph.to_dataframe()
print("\nDataFrame Inspection:")
print(df)

# Check first site (HBD)
site0 = ph.interaction_sites[0]
print(f"\nSite 0: {site0}")
print(f" - Features: {site0.features}")
print(f" - Shape: {site0.shape_name}")
# Center should be converted from 1.0, 2.0, 3.0 Angstroms to nm
center = puw.get_value(site0.center, to_unit='nm')
expected_center = np.array([0.1, 0.2, 0.3])
assert np.allclose(center, expected_center)
print(f" - Center (nm): {center} (Verified)")

# Check direction
if hasattr(site0, 'direction'):
    print(f" - Direction: {site0.direction}")

# 4. Export Round-trip
output_pml = 'sandbox/test_output.pml'
phmt.io.to_ligandscout(ph, output_pml)
print(f"\nExported back to: {output_pml}")

# 5. Re-import and check consistency
ph2 = phmt.io.from_ligandscout(output_pml)
print(f"Re-imported Pharmacophore: {ph2}")
assert ph2.n_interaction_sites == ph.n_interaction_sites
print("Round-trip verified successfully!")

# Cleanup
# os.remove(pml_file)
# os.remove(output_pml)
