# Strategic Roadmap

The development of PharmacophoreMT is divided into generations. **Gen 1b** has been added between the original Gen 1 and Gen 2 after an audit revealed that the classical pharmacophore workflow was incomplete and required consolidation before advancing to dynamic modeling.

---

## Gen 1: Foundation (Completed)
- [x] Refactor from `openpharmacophore` to `pharmacophoremt`.
- [x] Integration with `molsysmt`, `pyunitwizard`, `argdigest`, and `smonitor`.
- [x] Complete Pharmer and LigandScout I/O.
- [x] Official `molsysviewer` integration (RFC-001, `add_interaction_sites`).
- [x] High-Resolution modeling triad: `ComplexBasedModeler`, `LigandBasedModeler` (consensus), `StructureBasedModeler` (projections).
- [x] `InteractionSite` composition pattern (Feature + Shape) with full arsenal of shapes and features.
- [x] `ConformerGenerator` utility.
- [x] Rescue and migration of all logic from legacy repositories.

---

## Gen 1b: Classical Consolidation (Current Focus)

**Goal:** Make the classical pharmacophore workflow — ligand-based, structure-based, and complex-based modeling through to virtual screening and validation — complete, robust, and scientifically rigorous.

See [`classical_workflow.md`](classical_workflow.md) for the full specification of each task.

### Data Model
- [ ] Add `essential: bool` and `weight: float` to `InteractionSite`.
- [ ] Add provenance annotation (residue, coverage, mol_indices, source) to `InteractionSite.metadata`.
- [ ] Complete `_from_dict()` in IO for all 7 shapes (JSON/YAML native format).
- [ ] Complete pharmacophore serialization: all attributes preserved in round-trips.

### Molecular Standardization and Preparation (`utils/preparation.py`)
- [ ] `standardize_mol()`: desalt, normalize functional groups, sanitize.
- [ ] `filter_database()`: Ro5, PAINS, MW range filtering.
- [ ] `prepare_ligand(mol, pH=7.4)`: protonation state assignment.
- [ ] `enumerate_tautomers(mol)`: tautomer enumeration.
- [ ] `enumerate_stereoisomers(mol)`: stereocenter enumeration.
- [ ] Fix `PROTEIN_SMARTS` with residue-aware patterns (backbone N-H, C=O, sidechains).
- [ ] Integrate `ConformerGenerator` into `LigandBasedModeler` and `VirtualScreening`.

### ComplexBasedModeler
- [ ] Implement aromatic ring / pi-stacking (face-to-face and T-shaped).
- [ ] Implement cation-pi interaction detection.
- [ ] Implement water-mediated interaction detection.
- [ ] Extend `_merge_interaction_sites()` to all feature types.
- [ ] Add `ExcludedVolumeSphere` generation from non-interacting binding site atoms.
- [ ] Add multi-complex consensus workflow.

### LigandBasedModeler
- [ ] Track feature coverage; auto-assign `essential` flag by coverage threshold.
- [ ] Preserve directionality (SphereAndVector) for HBD/HBA in consensus.
- [ ] Add negative modeling (`inactive_systems` → ExcludedVolumeSphere).
- [ ] Add activity weighting (`activities` parameter, Ki/IC50).
- [ ] Refine consensus with Kabsch alignment after distance partitioning.

### StructureBasedModeler
- [ ] Add `pocket_center` + `pocket_radius` fallback pocket definition.
- [ ] Add `ExcludedVolumeSphere` generation from receptor surface.

### Model Refinement API (`Pharmacophore`)
- [ ] `set_essential(index/feature_name, bool)`.
- [ ] `set_radius(index/'all'/feature_name, radius)`.
- [ ] `add_excluded_volumes_from_receptor(system, radius)`.
- [ ] `similarity(other)` and `merge(other)`.
- [ ] `show()` robust when `molecular_system=None`.

### VirtualScreening — complete rewrite
- [ ] Input format flexibility (SMILES list, SDF path, DataFrame, rdkit Mol list).
- [ ] Database pre-processing pipeline (standardize → filter → protonate → conformers).
- [ ] Native RDKit feature factory from `LIGAND_SMARTS` (`io/fdef.py`).
- [ ] Partial matching (essential mandatory, optional scored).
- [ ] Directional tolerance for `SphereAndVector` sites (default 30°).
- [ ] Fit Value computation using `InteractionSite.weight`.
- [ ] Excluded volume clash detection.
- [ ] Multi-conformer screening (best match per molecule).
- [ ] Robust error handling: specific exceptions + `smonitor` + `failures` list.
- [ ] `show(top_n)`, `to_dataframe()`, `to_sdf()`, `to_csv()`.

### Validation Module (`pharmacophoremt/validation/`)
- [ ] LOO validation.
- [ ] EF at 1%, 5%, 10%.
- [ ] BEDROC (α=20.0).
- [ ] ROC curve and AUC.
- [ ] `benchmark()` runner.
- [ ] Benchmark datasets in `data/` (ERα, DHFR, thrombin actives + DUD-E decoys).

### Post-Screening Analysis
- [ ] `VirtualScreening.show(top_n)` — hits overlaid on pharmacophore in MolSysViewer.
- [ ] `cluster_hits()` — Butina clustering on Morgan fingerprints.
- [ ] `characterize_false_positives()` — structural pattern analysis.

### Testing
- [ ] Integration tests for all three modelers end-to-end.
- [ ] Full pipeline test: model → screen → validate (EF + BEDROC).
- [ ] Physical invariance tests (translational, rotational, unit).
- [ ] Format round-trip tests for all IO formats.

---

## Gen 2: Dynamic Modeling (Dynophores)
- [ ] `TrajectoryExtractionPipeline`: generate pharmacophore lists from MD trajectories.
- [ ] Native MSM engine: pharmacophore objects as nodes in a kinetic network.
- [ ] PCCA+ for metastable macrostate discovery.
- [ ] Vectorized `molsysviewer-pharmacophoremt` UI add-on.

## Gen 3: Specialized Horizons
- [ ] Peptide and macrocycle hierarchical modeling (backbone motifs + sidechain hotspots).
- [ ] Covalent pharmacophores (Warhead features with reaction geometry).
- [ ] Water-Replacement modeling from solvent MD (high-energy hydration sites).
- [ ] Quantum-Enhanced Pharmacophores (QEP): ESP integration.

## Gen 4: AI & Generative Synergy
- [ ] 3D Spatial Graph exports for GNNs.
- [ ] Diffusion-based generative blueprints (tensor/voxel representations).
- [ ] Multi-objective optimization (Anti-Target negative pharmacophores for toxicity).
- [ ] Ultra-large scale screening using 3D Pharmacophore Fingerprints (3DPFs).
