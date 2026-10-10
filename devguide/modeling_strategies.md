# Modeling Strategies and the Modeler Engine

**2026-10-10 structure transition (#44):** The structure class/dispatcher now
consume native cached inventories and explicit query projections, with optional
cached heavy-atom exclusions; see [the contract](structure_based_workflow.md).
No local receptor recognition, pocket selection or inferred molecular direction
remains in this route. MolSysMT #375 tracks the missing reusable direction tools
and outstanding donor-vector arithmetic in shared `get_features()`.

**2026-10-10 transition (#42):** The complex class and default `model()` now
consume an explicit ligand selection and named prepared native observations;
see [the current contract](complex_based_workflow.md). The old default-route
finding below is historical. No molecular inference, preparation or detection
is performed in the complex modeler. #41 remains partial for other legacy routes.

**2026-10-10 ownership audit:** #41 records the
[reachable legacy callers](pending_proposals/retire_legacy_molecular_operations.md),
including the surviving `model()` complex-based default. Use the documented
prepared-input native methods explicitly while their legacy transition is
reviewed. Older requests below to call the local `ConformerGenerator` are
superseded by MolSysMT #219; do not add local molecular preparation to a modeler.

**2026-10-02 revision:** The current [growth contracts](extensible_modeling_contracts.md)
and [roadmap](roadmap.md) supersede the older implementation proposals below.
Molecular preparation/recognition/geometry belongs in MolSysMT. Prepared inputs
and chemical-state choices must be explicit; no unconditional pH/tautomer or
salt transformation is required. Inactive-only features do not establish steric
excluded volumes. See the native workflow documents for measured current scope.


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

**Current rule:** Validate the declared input prerequisites. If a workflow
requests preparation, call a public MolSysMT provider with explicit scientific
policies and retain its provenance. Otherwise consume the prepared source
without hidden chemical transformations.

---

## 2. Molecular Preparation (Prerequisite for All Modelers)

Molecular standardization and preparation are MolSysMT responsibilities. The historical local preparation proposals below require provider migration before adoption.

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

**Current native facade (#42):** Supply the same unchanged prepared source,
`ligand_selection` and `interaction_collection`; the class delegates to public
`from_interaction_collection()`. A single requested frame returns one model,
multiple frames an ordered list. Native hydrophobic/H-bond/ionic/pi-pi/cation-pi
profiles, evaluated-empty families and errors retain their declared semantics.
`radius` controls query tolerance; detection cutoffs belong to prior MolSysMT
calls. Receptor-selection arguments, legacy thresholds and implicit recovery
are refused. See the maintained contract above and the executable cookbook.

**Retired design below:** The old cutoffs, status tables and spatial-merging
proposal describe the removed heuristic engine. They are not current defaults,
native compatibility promises or instructions to implement molecular routines.

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

**2026-10-07 transition (#18):** The class now requires explicit
`consensus_method='rigid'` or `'aligned_cliques'` and consumes prepared ligands
through existing public native tools. `n_points` is a minimum site count;
`min_actives` is joint distinct-ligand support. `build()` returns the native
model list and retains `result`/`report`; there is no legacy RMSD ranking or
hidden conformer generation. See [the migration contract](ligand_based_workflow.md)
and [executable recipe](../docs/content/cookbook/ligand_based_modeler.md).
The [distance/clique review](clique_consensus_review.md) and unchanged helper
audit retain the reasons for retiring the former builder. The historical
recipe and proposed completeness requirements below describe that older design,
not the current native contract.

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

**Inputs:** A prepared receptor reference, cached native chemical inventory and
explicit pharmacophoric projection specifications.
**Goal:** Build declared complementary ligand hypotheses in the receptor frame.
**Output:** A single `Pharmacophore`.

#### Algorithm: Feature Projection
1. Select/prepare the receptor through MolSysMT; actual pocket detection belongs
   to TopoMT. No pocket API or fallback is inferred in the facade.
2. Obtain/cache native `get_features()` chemical records and provider geometry.
3. Use `from_receptor_projections()` with explicit feature index, query projection
   direction, positive physical distance and hypothesis label. Donors/acceptors
   and charges are complemented; aromatic/hydrophobic kinds are preserved.
   Ligand donor direction and aromatic normal are separate target decisions;
   ligand acceptor targets remain spherical.
4. Optionally compose `get_excluded_volume_sites()` from a native heavy-atom
   inventory and explicit radius with a common declared frame/state and atom set.
   No surface sampling or physical-radius assignment occurs.

#### Completeness Requirements (Gen 1b)
- Automatic chemically informed pocket hypotheses remain future work. Missing
  donor-pair/local acceptor geometry belongs to MolSysMT #375. Environmental
  refinement is separately #323; no direction/lone-pair engine is copied here.
- Alternative projection faces/directions require independent hypotheses. The
  fixed distances, first-neighbor/+z and SMARTS heuristics are retired without
  an equivalence or biological-validation claim.

### 3.4 DynamicModeler (Gen 2)

**Inputs:** MD trajectories (multiple frames) as a `molsysmt` system.
**Goal:** Discover metastable pharmacophoric states (Dynophores).

*Architecture details in [`dynamics_and_msm.md`](dynamics_and_msm.md).*

---

## 4. The High-Level API (`phmt.model`)

For zero-friction usage, a convenience function delegates to the appropriate Modeler:

```python
import pharmacophoremt as phmt

# Complex-based: same prepared source and explicit cached native observations
ph = phmt.model(molecular_system, method='complex-based',
                ligand_selection=ligand, interaction_collection=analyses)

# Ligand-based: explicitly prepared ligand records; choose the native method
hypotheses = phmt.model(prepared_ligands, method='ligand-based',
                       consensus_method='rigid', n_points=4)

# Structure-based: prepared native evidence and explicit hypothesis decisions
ph = phmt.model(receptor, method='structure-based',
                feature_inventory=inventory, projection_specs=specifications)
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
| `ComplexBasedModeler` (explicit native observation collection) | Native facade; legacy engine retired | #42; hydrophobic/H-bond/ionic/pi-pi/cation-pi follow supported provider definitions |
| Complex halogen/metal observations, exclusions and cross-complex consensus | Separate current contracts/backlog | No legacy threshold or global spatial-merging compatibility; exclusions are a public independent query step |
| `LigandBasedModeler` (explicit native rigid/aligned consensus) | Native facade; legacy builder retired | See #18 and the migration contract; no affinity ranking |
| Conformer preparation, negative modeling and activity weighting | **Gen 1b** | Directional features are covered by the selected native contracts; preparation belongs to MolSysMT |
| `StructureBasedModeler` (explicit cached feature projection/complementarity) | Native facade; legacy engine retired | #44; caller-declared projection and target orientation |
| Automatic structure-based pocket hypotheses | **Gen 1b** | Provider geometry #375 and TopoMT pocket contract required; cached exclusions are separately delivered |
| `DynamicModeler` | Gen 2 | |
| Model refinement API (`essential` flag, `set_radius`, `merge`, `similarity`) | **Gen 1b** | |
| Molecular preparation utilities (`prepare_ligand`, `enumerate_tautomers`) | **Gen 1b** | |
| `PROTEIN_SMARTS` (residue-aware patterns) | **Gen 1b** | Currently = `LIGAND_SMARTS` |
