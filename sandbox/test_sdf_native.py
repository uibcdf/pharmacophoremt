import pharmacophoremt as phmt
import numpy as np
import os

# 1. Create a PharmacophoreMT object with complex features
ph = phmt.Pharmacophore(name="Comprehensive Test", description="Test for SDF and Native")
ph.add_interaction_site(phmt.interaction_site.HBDonorSphere(center='[1, 2, 3] nm', radius='0.2 nm', skip_digestion=True))
ph.add_interaction_site(phmt.interaction_site.AromaticRingSphereAndVector(center='[5, 5, 5] nm', radius='0.3 nm', direction=[0,0,1], skip_digestion=True))

print(f"Original PHMT: {ph}")

# 2. Test SDF (Annotated)
sdf_file = 'sandbox/test.sdf'
phmt.io.to_sdf(ph, sdf_file)
print(f"\nExported to SDF: {sdf_file}")

ph_sdf = phmt.io.load_sdf(sdf_file)
print(f"Loaded from SDF: {ph_sdf}")
assert ph_sdf.n_interaction_sites == 2
print("SDF Round-trip verified!")

# 3. Test YAML
yaml_file = 'sandbox/test.yaml'
phmt.io.to_yaml(ph, yaml_file)
print(f"\nExported to YAML: {yaml_file}")

ph_yaml = phmt.io.load_yaml(yaml_file)
print(f"Loaded from YAML: {ph_yaml}")
assert ph_yaml.n_interaction_sites == 2
assert ph_yaml.interaction_sites[1].shape_name == 'sphere and vector'
print("YAML Round-trip verified!")

# 4. Test JSON
json_file = 'sandbox/test.json'
phmt.io.to_json(ph, json_file)
print(f"\nExported to JSON: {json_file}")

ph_json = phmt.io.load_json(json_file)
print(f"Loaded from JSON: {ph_json}")
assert ph_json.name == "Comprehensive Test"
print("Native JSON Round-trip verified!")

print("\nAll new I/O formats verified successfully!")
