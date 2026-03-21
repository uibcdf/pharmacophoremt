import pharmacophoremt as phmt
import pandas as pd

# 1. Load from pharmer.json
pharmer_file = 'pharmacophoremt/data/pharmer.json'
print(f"Loading pharmacophore from {pharmer_file}...")
ph = phmt.Pharmacophore(pharmer_file, form='pharmer')

# 2. Inspect basic attributes
print(f"\nPharmacophore: {ph}")
print(f"Number of sites: {ph.n_interaction_sites}")

# 3. Test .to_dataframe()
print("\nDataFrame Inspection:")
df = ph.to_dataframe()
print(df)

# 4. Test .get() method
print("\nTesting .get() method:")
centers, radii = ph.get(get_center=True, get_radius=True)
print(f"Centers (Quantity):\n{centers}")
print(f"Radii (Quantity):\n{radii}")

# 5. Test .get_distance_matrix()
print("\nDistance Matrix (nm):")
dist_matrix = ph.get_distance_matrix()
print(dist_matrix)

# 6. Test filtering in .get()
print("\nFiltering Hydrophobic sites:")
hydrophobic_sites = ph.get(feature_name='hydrophobicity')
print(f"Found {len(hydrophobic_sites)} hydrophobic sites.")
for site in hydrophobic_sites:
    print(f" - {site}")

# 7. Test add/remove
print("\nTesting add/remove:")
from pharmacophoremt.interaction_site import PositiveChargeSphere
new_site = PositiveChargeSphere(center='[1.0, 1.0, 1.0] nm', radius='0.5 nm')
ph.add_interaction_site(new_site)
print(f"After add: {ph.n_interaction_sites} sites")
ph.remove_interaction_site(-1)
print(f"After remove: {ph.n_interaction_sites} sites")
