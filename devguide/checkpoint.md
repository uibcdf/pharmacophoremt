# Development Checkpoint

**Current Status**: `Gen 1b: Classical Consolidation (IN PROGRESS — Batches 1–3 complete, Batch 4 in progress)`

This is a living document. Use it to quickly catch up on the project's state and identify the next tasks. **Start here before reading anything else.**

---

## 1. What's Done (Gen 1 Foundation)

- **Brand Transition**: Successfully renamed the package; all internal references updated.
- **Ecosystem Setup**: Integrated `pyunitwizard`, `argdigest`, `smonitor`, `molsysmt`.
- **Source of Truth**: The `devguide/` is complete and authoritative.
- **Base Architecture**: `InteractionSite` (Feature + Shape) composition pattern implemented.
- **High-Resolution Arsenal**: All Features (Halogen, Metal, Cation-Pi) and Shapes (Disk, Cylinder) defined.
- **Modeling Engines (skeleton)**: `ComplexBasedModeler`, `LigandBasedModeler`, `StructureBasedModeler` exist and are functional for basic cases.
- **Interoperability**: Pharmer, LigandScout, RDKit, SDF, and PHMT (JSON/YAML) translators implemented.
- **Visual Integration**: RFC-001 compliant `add_to_molsysviewer()` bridge implemented.
- **ConformerGenerator**: Functional utility for 3D conformer generation (UFF/MMFF, RMSD filtering).
- **Rescue Operation**: 100% of legacy repository logic migrated.

---

## 2. Why Gen 1b Exists: The Honest Audit

An audit of the code against the requirements of a complete classical pharmacophore workflow revealed that **the three modeling engines and the virtual screening pipeline are incomplete for production use**. The key findings were:

| Area | Gap |
| :--- | :--- |
| Molecular standardization | Absent: no desalting, no normalization, no drug-likeness filtering |
| `PROTEIN_SMARTS` | Is a copy of `LIGAND_SMARTS` — semantically incorrect for protein feature detection |
| Feature provenance | `InteractionSite` stores no information about which residue/molecule caused it |
| `InteractionSite` data model | Missing `essential` flag and `weight` attribute (needed for Fit Value and partial matching) |
| IO JSON/YAML | `_from_dict()` raises `NotImplementedError` for 5 of 7 shapes — native format is broken |
| `ComplexBasedModeler` | Pi-stacking and cation-pi absent; water-mediated interactions absent; merging only hydrophobic; no excluded volumes; no multi-complex consensus |
| `LigandBasedModeler` | No conformer generation; non-directional HBD/HBA; no coverage tracking; no negative modeling |
| `StructureBasedModeler` | No automatic pocket detection; no excluded volumes |
| `VirtualScreening` | No input format flexibility; no database pre-processing; bare `except:`; no native feature factory; no partial matching; no directional tolerance; no Fit Value; no excluded volume clash detection; no `show()`, `to_sdf()`, `to_dataframe()` |
| `Pharmacophore.show()` | Fails when `molecular_system=None` (always the case for ligand-based models) |
| Validation | Entirely absent: no LOO, no EF, no BEDROC, no ROC |
| Tests | LigandBased, StructureBased, and VirtualScreening have zero integration tests |

Full technical specification for all required fixes: see [`classical_workflow.md`](classical_workflow.md).

---

## 3. Current Focus: Gen 1b Tasks

Tasks ordered by priority (see [`roadmap.md`](roadmap.md) for the full checklist):

### Batch 1 — Data Model and IO Foundations ✅
- [x] **Task 1.1**: Add `essential`, `weight`, `metadata` to `InteractionSite`.
- [x] **Task 1.2**: Complete IO `_from_dict()` for all 7 shapes in JSON/YAML.
- [x] **Task 1.3**: Complete pharmacophore serialization (`score`, `ref_mol`, `ref_struct`, `essential`, `weight`, `metadata`).
- [x] **Task 1.4**: Fix `PROTEIN_SMARTS` with residue-aware patterns (backbone, sidechains).
- [x] **Task 1.5** (partially): `ConformerGenerator` integrated; full provenance (residue/coverage) still pending.

### Batch 2 — Preparation and Input Pipeline ✅
- [x] **Task 2.1**: `pharmacophoremt/utils/preparation.py` — `standardize_mol()`, `filter_database()`, `smiles_to_mols()`.
- [x] **Task 2.2**: `ConformerGenerator` integrated into `LigandBasedModeler.build()`.
- [x] **Task 2.3**: `ConformerGenerator` integrated into `VirtualScreening.run()`.
- [x] **Task 2.5**: `Pharmacophore.show()` fixed for `molecular_system=None` (uses MolSysView directly).
- [ ] **Task 2.4**: Full SDF-path / DataFrame input route for `VirtualScreening` (molsysmt handles most of it).

### Batch 3 — Complete the Interaction Model ✅
- [x] **Task 3.1**: Pi-stacking (face-to-face + T-shaped) in `ComplexBasedModeler`.
- [x] **Task 3.2**: Cation-pi (ligand→receptor and receptor→ligand) in `ComplexBasedModeler`.
- [x] **Task 3.4**: `ExcludedVolumeSphere` from receptor heavy atoms in `StructureBasedModeler`.
- [x] **Task 3.5**: `_merge_interaction_sites()` extended to all feature types (HBD, HBA, aromatic, charges, cation-pi), handles SphereAndVector (averages direction).
- [x] **Task 3.7**: `pocket_center` + `pocket_radius` fallback in `StructureBasedModeler`.
- [ ] **Task 3.3**: Water-mediated interaction detection in `ComplexBasedModeler` (pending).
- [ ] **Task 3.6**: Multi-complex consensus in `ComplexBasedModeler` (pending).
- [ ] **Task 3.8**: Feature coverage tracking + auto-`essential` in `LigandBasedModeler` (pending).
- [ ] **Task 3.9**: SphereAndVector for HBD/HBA in `LigandBasedModeler` (pending).
- [ ] **Task 3.10**: Negative modeling (`inactive_systems`) in `LigandBasedModeler` (pending).

### Batch 4 — Complete Virtual Screening ✅
- [x] **Task 4.2**: Partial matching — `min_match_ratio`, essential vs optional sites.
- [x] **Task 4.3**: Directional tolerance (±30°) for `SphereAndVector` sites.
- [x] **Task 4.4**: Fit Value = Σ(weight matched) / Σ(weight all).
- [x] **Task 4.5**: Excluded volume clash detection (veto on heavy-atom overlap).
- [x] **Task 4.6**: Multi-conformer screening — best Fit Value across all conformers.
- [x] **Task 4.7**: Bare `except:` removed; specific exceptions throughout.
- [x] **Task 4.8**: `to_dataframe()`, `to_csv()`, `to_sdf()` added to `VirtualScreening`.
- [ ] **Task 4.1**: Native fdef from LIGAND_SMARTS for RDKit interop (low priority, VS no longer depends on it).

### Batch 5 — Validation Module ✅
- [x] **Task 5.1**: `pharmacophoremt/validation/__init__.py` created.
- [x] **Task 5.2**: LOO validation — `LeaveOneOutValidator`.
- [x] **Task 5.3**: EF@1%, 5%, 10% — `enrichment_factor()`.
- [x] **Task 5.4**: BEDROC (α=20.0) — `bedroc()` (Truchon & Bayly 2007).
- [x] **Task 5.5**: ROC/AUC — `roc_auc()`.
- [x] **Task 5.6**: `RetrospectiveValidator` — full pipeline from molecules to AUC/BEDROC/EF.
- [ ] **Task 5.7**: Benchmark datasets in `data/` (ERα, DHFR, thrombin + DUD-E decoys) — pending.

### Batch 6 — Refinement API, Utilities, and Tests (NEXT)
- [ ] **Task 6.1**: `Pharmacophore.set_radius()`, `set_essential()`, `add_excluded_volumes_from_receptor()`, `similarity()`, `merge()`.
- [ ] **Task 6.2**: `enumerate_tautomers()`, `enumerate_stereoisomers()` in `utils/preparation.py`.
- [ ] **Task 6.3**: Activity weighting in `LigandBasedModeler`.
- [ ] **Task 6.4**: Alignment-based consensus refinement in `LigandBasedModeler`.
- [ ] **Task 6.5**: Integration tests for all three modelers.
- [ ] **Task 6.6**: Full pipeline test (model → screen → validate with EF/BEDROC).
- [ ] **Task 6.7**: Physical invariance tests (translational, rotational, unit).
- [ ] **Task 6.8**: Format round-trip tests for all IO formats.

---

## 4. How to Contribute

1. **Read first**: [`classical_workflow.md`](classical_workflow.md) for the full specification of what each task must implement and why.
2. **Check standards**: [`api_design_standards.md`](api_design_standards.md) before writing any code.
3. **Pick a task**: Start from Batch 1 and proceed in order; later batches may depend on earlier ones.
4. **Write tests first** (or in parallel): No task is complete without at least one integration test demonstrating the full behavior.
5. **Mark done**: Update this checkpoint and the [`roadmap.md`](roadmap.md) when a task is completed.
