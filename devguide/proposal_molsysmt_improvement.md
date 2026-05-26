During the PharmacophoreMT reimplementation effort we are expanding the use of
`molsysmt` adapters and digesters.

Record the requirement, the desired API shape, and why the change would benefit other
projects. That way we can
track the request, shape a PR, and keep PharmacophoreMT aligned with the central
`molsysmt` configuration.

---

## Proposal 1 — `msm.build.generate_conformers()`

**Origin:** `pharmacophoremt/utils/conformers.py` — `ConformerGenerator` class.

**Problem:** Generating 3D conformers from a flat (2D) molecule is a prerequisite
for both pharmacophore modeling (LigandBasedModeler) and virtual screening
(VirtualScreening). The current implementation lives inside pharmacophoremt but
the operation is entirely general. Any project that receives SMILES or 2D structures
— topomt, future ADMET tools, etc. — will need the same thing.

**Proposed API:**

```python
mol_3d = msm.build.generate_conformers(
    mol,
    n_conformers=50,
    rmsd_threshold=0.5,   # Å, for diversity pruning
    forcefield='uff',     # 'uff' | 'mmff'
    seed=-1,
)
```

Returns the same molecular object with conformers embedded and minimised.
Internally: `AllChem.EmbedMultipleConfs` → forcefield minimisation → RMSD
pruning (`AllChem.GetBestRMS`). Should fall back gracefully (return input)
if embedding fails, and emit a smonitor warning.

**Benefit:** pharmacophoremt, topomt, and any pipeline starting from SMILES
would share a single, tested implementation instead of each rolling their own.

---

## Proposal 2 — `msm.build.fix_bond_orders()`

**Origin:** `pharmacophoremt/utils/chemistry.py` — `fix_bond_orders()`.

**Problem:** Ligands extracted from PDB structures lose bond order information
(all bonds become single). Correcting bond orders requires a reference structure
looked up by residue/ligand name. This is a standard preparation step for any
complex-based or structure-based pipeline, not specific to pharmacophore modelling.

**Proposed API:**

```python
mol_fixed = msm.build.fix_bond_orders(mol, residue_name)
```

`residue_name` is the 3-letter PDB code (e.g. `'LIG'`, `'ATP'`). Internally
queries a reference source (CCD, SMILES lookup, or user-provided template) to
assign the correct bond orders via `AllChem.AssignBondOrdersFromTemplate`.

**Benefit:** Any project that handles protein–ligand PDB structures (pharmacophoremt,
topomt, future docking tools) would use the same validated routine.

---

## Proposal 3 — Molecular plane geometry utilities in `msm.geometry`

**Origin:** `pharmacophoremt/utils/maths.py` — `ring_normal()`,
`point_projection()`, `angle_between_normals()`.

**Problem:** Computing ring plane normals and inter-plane angles is needed
wherever aromatic interactions are analysed (pi-stacking, cation-pi, T-shaped
contacts). pharmacophoremt uses these functions in `ComplexBasedModeler` and
`StructureBasedModeler`. topomt will need them for pocket geometry analysis
(e.g. detecting aromatic-lined channels). Each project reimplementing the same
three functions is unnecessary duplication.

**Proposed API:**

```python
import molsysmt.geometry as geo

normal = geo.ring_normal(atom_indices, coords, centroid)
# → unit ndarray (3,)

proj = geo.point_projection(normal, plane_point, point)
# → quantity, same units as point

angle = geo.angle_between_normals(normal_1, normal_2)
# → float, degrees (returns acute angle, 0–90)
```

All three accept puw quantities for coordinates and return unit-consistent results.

**Benefit:** Shared, tested geometric primitives for pharmacophoremt, topomt,
and any future tool that reasons about molecular planes.
