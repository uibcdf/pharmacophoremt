import pharmacophoremt as phmt
import numpy as np
from pharmacophoremt import pyunitwizard as puw

# 1. Create a PharmacophoreMT object
ph = phmt.Pharmacophore(name="Test RDKit")
ph.add_interaction_site(phmt.interaction_site.HBDonorSphere(center='[1, 2, 3] angstroms', radius='1.0 angstroms'))
ph.add_interaction_site(phmt.interaction_site.AromaticRingSphere(center='[5, 5, 5] angstroms', radius='1.5 angstroms'))

print(f"Original PHMT: {ph}")

# 2. Convert TO RDKit
rd_ph = phmt.io.to_rdkit(ph)
print(f"\nConverted to RDKit object: {rd_ph}")
print(f"RDKit Features: {len(rd_ph.getFeatures())}")

# Check first feature family
feat0 = rd_ph.getFeature(0)
print(f"Feature 0 Family: {feat0.GetFamily()}")
assert feat0.GetFamily() == 'Donor'

# 3. Load BACK from RDKit
ph2 = phmt.io.load_rdkit(rd_ph)
print(f"\nLoaded back to PHMT: {ph2}")
print(f"Number of sites: {ph2.n_interaction_sites}")

# Verify coordinates
center2 = puw.get_value(ph2.interaction_sites[0].center, to_unit='angstroms')
assert np.allclose(center2, [1.0, 2.0, 3.0])
print("Coord verification successful!")

print("\nRDKit In-Memory Round-trip successful!")
