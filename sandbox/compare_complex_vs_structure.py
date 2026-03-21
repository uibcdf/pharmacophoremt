import pharmacophoremt as phmt
import molsysmt as msm
import numpy as np
from pharmacophoremt import pyunitwizard as puw

# 1. Load the ERalpha complex
pdb_file = 'tests/data/eralpha_complex.pdb'
system = msm.convert(pdb_file, to_form='molsysmt.MolSys')

# Identify ligand and pocket for structured modeling
ligand_selection = 'group_index == 8076'
pocket_selection = f'(molecule_type == "protein") within 0.6 nm of ({ligand_selection})'

print("--- Step 1: Complex-Based Modeling (Real Contacts) ---")
ph_complex = phmt.model(
    system, 
    method='complex-based',
    ligand_selection=ligand_selection
)
print(f"Complex Model: {ph_complex.n_interaction_sites} sites found.")

print("\n--- Step 2: Structure-Based Modeling (Empty Pocket Projections) ---")
# To simulate an empty pocket, we could remove the ligand, 
# but the modeler just needs the pocket selection.
modeler_struct = phmt.modeler.StructureBasedModeler(
    system, 
    pocket_selection=pocket_selection
)
ph_structure = modeler_struct.build()
print(f"Structure Model: {ph_structure.n_interaction_sites} sites projected.")

# 3. Scientific Comparison
print("\n--- Step 3: Comparing Models ---")
# Let's find if any projected site matches a real contact site
complex_centers = ph_complex.get(get_center=True, skip_digestion=True)
struct_centers = ph_structure.get(get_center=True, skip_digestion=True)

# Calculate distances between all complex sites and all projected sites
c_coords = puw.get_value(complex_centers, to_unit='nm')
s_coords = puw.get_value(struct_centers, to_unit='nm')

# Matrix N_complex x M_projected
diff = c_coords[:, np.newaxis, :] - s_coords[np.newaxis, :, :]
dist_matrix = np.sqrt(np.sum(diff**2, axis=-1))

# Find matches within 1.5 Angstroms (0.15 nm)
matches = np.where(dist_matrix <= 0.15)

print(f"Number of hits (overlap < 1.5A): {len(matches[0])}")
for i, j in zip(matches[0], matches[1]):
    c_site = ph_complex.interaction_sites[i]
    s_site = ph_structure.interaction_sites[j]
    dist = dist_matrix[i, j]
    print(f"MATCH: Complex Site {i} ({c_site.features}) <-> Structure Site {j} ({s_site.features})")
    print(f"       Distance: {dist:.3f} nm")

if len(matches[0]) > 0:
    print("\nSUCCESS: The Structure-Based projections are consistent with real interactions!")
else:
    print("\nINFO: No direct matches found. This might be due to strict rules or incomplete feature types.")
