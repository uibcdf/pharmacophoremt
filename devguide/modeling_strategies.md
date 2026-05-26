# Modeling Strategies and the Modeler Engine

This document defines the architecture for pharmacophore generation in PharmacophoreMT through the **Modeler** engine. It covers all three classical strategies and the planned dynamic approach.

---

## 1. The Modeler Philosophy

PharmacophoreMT separates **data storage** (`Pharmacophore` class) from **modeling logic** (`Modeler` classes). This modularity allows complex algorithms to evolve without bloating the core data structures.

### The Modeler Interface

All modeling engines follow a common workflow:
1. **Prepare**: Standardize molecular inputs (protonation, tautomers, conformers).
2. **Initialize**: Provide the molecular system and target entities.
3. **Configure**: Set distance cutoffs, feature types to include, etc.
4. **Build**: Execute the algorithm and return a `Pharmacophore` object.

**Rule:** The `build()` method must always call molecular preparation internally (or assert it has been done) so that the user does not need to manually run preparation steps.

---

## 2. Molecular Preparation (Prerequisite for All Modelers)

Before any feature detection, inputs must be standardized. This is handled by the `pharmacophoremt.utils.preparation` module.

### 2.1 Ligand Preparation
- **Protonation state at pH 7.4**: Use pKa-based assignment (integration with `rdkit.Chem.MolStandardize` or Dimorphite-DL).
- **Tautomer canonicalization**: Enumerate and select the dominant tautomer.
- **Stereochemistry**: Warn if undefined stereocenters are present.
- **3D Conformers**: Call `ConformerGenerator` if no conformers exist.

### 2.2 Receptor Preparation
- **Add missing hydrogens**: Call `msm.build.add_missing_hydrogens()`.
- **Protonation state**: Assign His δ/ε tautomers and Asp/Glu/Lys/Arg protonation states based on local environment.

### 2.3 Protein SMARTS
Protein features are detected using `PROTEIN_SMARTS`, which must be a **separate dictionary from `LIGAND_SMARTS`** with residue-aware patterns for backbone (N-H, C=O) and amino acid sidechains (Ser/Thr/Tyr, His, Lys, Arg, Asp, Glu, Phe/Trp/Tyr aromatic rings, aliphatic residues Val/Leu/Ile/Met).

---

## 3. Modeler Specializations

### 3.1 ComplexBasedModeler

**Inputs:** A protein-ligand complex (single structure or ensemble of structures/frames).
**Goal:** Extract pharmacophoric interaction sites directly from the 3D contact geometry.
**Output:** A single `Pharmacophore` per structure/frame.

#### Implemented Interactions
| Interaction | Status | Key Parameters |
| :--- | :--- | :--- |
| Hydrophobic | Done | `hyd_dist_max` = 0.50 nm |
| HB Donor (ligand → receptor) | Done | `hb_dist_max` = 0.35 nm, `hb_ang_min` = 120° |
| HB Acceptor (ligand ← receptor) | Done | same |
| Positive / Negative Charge | Done | `charge_dist_max` = 0.56 nm |
| Halogen Bond | Done | `halogen_dist_max` = 0.40 nm, C-X···A angle ≥ 150° |
| Metal Coordination | Done | `metal_dist_max` = 0.28 nm |

#### Missing Interactions (Gen 1b)
| Interaction | Status | Key Geometry |
| :--- | :--- | :--- |
| Aromatic / Pi-stacking | **Not implemented** | centroid-centroid ≤ 0.75 nm; ring normal angle ≤ 30° (parallel) or ~90° (T-shaped); offset ≤ 0.20 nm |
| Cation-Pi | **Not implemented** | cation center over aromatic ring, dist 0.35–0.60 nm |
| Excluded Volumes | **Not implemented** | VdW surface of non-interacting receptor atoms in binding site |

#### Site Merging
After all interaction sites are added, nearby sites of the **same feature type** must be merged using the existing `_merge_interaction_sites()` clique algorithm. Currently this is called only for hydrophobicity. It must be called for all feature types with type-appropriate thresholds.

### 3.2 LigandBasedModeler

**Inputs:** Multiple active molecules (with 3D conformers, generated internally if absent).
**Goal:** Find the consensus pharmacophore — the common 3D feature pattern shared by all (or most) actives.
**Output:** A ranked list of `Pharmacophore` hypotheses.

#### Algorithm: Recursive Partitioning with Clique Consensus
1. Detect chemical features in each conformer of each active (via `LIGAND_SMARTS`).
2. Enumerate all combinations of N feature points per conformer.
3. Group candidates by feature type signature (e.g., `(hb donor, hb donor, aromatic ring)`).
4. Within each group, apply recursive partitioning on the inter-point distance vector to identify candidates with similar 3D geometry.
5. Build a consensus graph and find maximal cliques covering the most actives.
6. Score each clique by RMSD of inter-site distances; rank hypotheses.
7. After distance-based partitioning, refine with Kabsch alignment (`align_pharmacophores`) within each clique to compute accurate 3D consensus centers.

#### Completeness Requirements (Gen 1b)
- **Conformer generation**: call `ConformerGenerator` for any molecule with 0 conformers.
- **Directional features**: HBD/HBA sites must be created as `SphereAndVector`, averaging direction vectors within each clique.
- **Negative modeling**: accept `inactive_systems`; detect features unique to inactives; add as `ExcludedVolumeSphere` sites.
- **Activity weighting**: accept `activities` (Ki/IC50 as `Quantity`); weight clique scores by the potency of the actives they cover.

### 3.3 StructureBasedModeler

**Inputs:** A receptor structure (without a co-crystallized ligand).
**Goal:** Project ideal interaction sites from the receptor atoms into the binding cavity.
**Output:** A single `Pharmacophore`.

#### Algorithm: Feature Projection
1. Isolate the binding site (via `pocket_selection`, `topomt`, or fallback sphere definition).
2. Detect receptor features using `PROTEIN_SMARTS`.
3. For each feature, project an ideal complementary site into the cavity:
   - Protein HB Donor → project an HB Acceptor site at 0.28 nm along the donor-H bond vector.
   - Protein HB Acceptor → project an HB Donor site at 0.28 nm along the lone-pair direction.
   - Protein Aromatic Ring → project an Aromatic site at 0.45 nm along the ring normal.
   - Protein hydrophobic atoms → project a Hydrophobic site at 0.35 nm.
   - Protein positive charge → project a Negative Charge site at 0.40 nm.
   - Protein negative charge → project a Positive Charge site at 0.40 nm.
4. Add `ExcludedVolumeSphere` sites at receptor surface atoms facing the cavity.

#### Completeness Requirements (Gen 1b)
- **Pocket definition**: if `pocket_selection` is `None` and `topomt` is unavailable, accept `pocket_center` + `pocket_radius` as a fallback sphere definition.
- **Excluded volumes**: after projecting interaction sites, sample non-interacting receptor surface atoms and add `ExcludedVolumeSphere` sites.

### 3.4 DynamicModeler (Gen 2)

**Inputs:** MD trajectories (multiple frames) as a `molsysmt` system.
**Goal:** Discover metastable pharmacophoric states (Dynophores).

*Architecture details in [`dynamics_and_msm.md`](dynamics_and_msm.md).*

---

## 4. The High-Level API (`phmt.model`)

For zero-friction usage, a convenience function delegates to the appropriate Modeler:

```python
import pharmacophoremt as phmt

# Complex-based: automatic ligand and receptor detection
ph = phmt.model(molecular_system, method='complex-based')

# Ligand-based: list of actives (SMILES, RDKit Mol, or molsysmt systems)
hypotheses = phmt.model(active_mols, method='ligand-based', n_points=4)

# Structure-based: receptor only, with a pocket center as fallback
ph = phmt.model(receptor, method='structure-based',
                pocket_center=[12.3, 4.5, -2.1], pocket_radius='1.2 nm')
```

---

## 5. Model Refinement

After automatic generation, the pharmacophore must support interactive refinement before screening.

### 5.1 Essential vs. Optional Features

Each `InteractionSite` carries an `essential` boolean flag (default: `True`). Essential features **must** be matched during virtual screening. Optional features contribute to the Fit Value score but are not required.

```python
ph.interaction_sites[3].essential = False  # mark one HB as optional
```

### 5.2 Tolerance Adjustment

```python
ph.set_radius('all', '0.15 nm')                 # global tolerance
ph.set_radius(feature_name='hb donor', radius='0.1 nm')  # per feature type
ph.set_radius(index=2, radius='0.2 nm')         # per site
```

### 5.3 Excluded Volume Management

```python
ph.add_excluded_volumes_from_receptor(receptor_system, radius='0.15 nm')
```

### 5.4 Pharmacophore Comparison and Merging

```python
similarity = ph_complex.similarity(ph_ligand)   # 0–1 overlap score
ph_combined = ph_complex.merge(ph_ligand)        # union of sites
```

---

## 6. Implementation Status

| Component | Status | Notes |
| :--- | :--- | :--- |
| `ComplexBasedModeler` (core HB, hydrophobic, charge, halogen, metal) | Done | |
| `ComplexBasedModeler` (pi-stacking, cation-pi, excluded volumes, global merging) | **Gen 1b** | |
| `LigandBasedModeler` (distance-based consensus, scoring) | Done | |
| `LigandBasedModeler` (conformer integration, directional features, negative modeling, weighting) | **Gen 1b** | |
| `StructureBasedModeler` (feature projection, charge complementarity) | Done | |
| `StructureBasedModeler` (pocket fallback, excluded volumes) | **Gen 1b** | |
| `DynamicModeler` | Gen 2 | |
| Model refinement API (`essential` flag, `set_radius`, `merge`, `similarity`) | **Gen 1b** | |
| Molecular preparation utilities (`prepare_ligand`, `enumerate_tautomers`) | **Gen 1b** | |
| `PROTEIN_SMARTS` (residue-aware patterns) | **Gen 1b** | Currently = `LIGAND_SMARTS` |
