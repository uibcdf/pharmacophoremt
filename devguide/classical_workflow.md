# Classical Pharmacophore Workflow: Complete Specification

This document is the **definitive specification** for what PharmacophoreMT must implement to be robust and complete for classical pharmacophore-based drug design. It defines the requirements for each phase of the workflow and serves as the implementation guide for **Gen 1b: Classical Consolidation**.

---

## Overview: The Eight Phases

A rigorous classical pharmacophore workflow comprises eight sequential phases:

0. **Molecular Standardization** — Normalize all inputs to a canonical, consistent form.
1. **Molecular Preparation** — Assign protonation states, tautomers, stereochemistry, and 3D conformers.
2. **Feature Detection** — Identify chemical features in molecules and receptors.
3. **Pharmacophore Modeling** — Build the 3D hypothesis (ligand-based, structure-based, or complex-based).
4. **Model Refinement** — Annotate, adjust, and curate the hypothesis before screening.
5. **Validation** — Measure predictive power before committing to a large screening campaign.
6. **Virtual Screening** — Apply the model to filter and rank a molecular database.
7. **Post-Screening Analysis** — Analyze hits for diversity, quality, and SAR insight.

Skipping or underimplementing any of these phases compromises the scientific validity of the results.

---

## New Module Structure

The following new modules must be created as part of Gen 1b:

| Module | Purpose |
| :--- | :--- |
| `pharmacophoremt/utils/preparation.py` | Molecular standardization, protonation, tautomers, stereoisomers |
| `pharmacophoremt/validation/__init__.py` | LOO, EF, BEDROC, ROC, hit rate, benchmark runner |
| `pharmacophoremt/io/fdef.py` | Build native RDKit `.fdef` feature factory from `LIGAND_SMARTS` |

---

## Phase 0: Molecular Standardization

**This phase must run before any protonation, tautomer enumeration, or feature detection.** Molecules arriving from external sources (SMILES, SDF, databases) are rarely in a consistent form. Standardization ensures a canonical starting point.

### 0.1 Desalting and Counterion Removal

**Why it matters:** A molecule stored as `CC(=O)O.[Na+]` (sodium acetate) must be treated as `CC(=O)O`. Counterions and solvents in the SMILES string produce wrong atom counts and wrong features.

**Requirement:** Strip salts and counterions, keeping only the largest organic fragment. Integration point: `rdkit.Chem.MolStandardize.fragment_parent()`.

**Implementation target:** `standardize_mol(mol)` in `utils/preparation.py`.

### 0.2 Functional Group Normalization

**Why it matters:** The same functional group can be represented in multiple canonical forms (e.g., nitro group as `[N+](=O)[O-]` or `N(=O)=O`; guanidinium with different charge placement). Inconsistent representations lead to SMARTS pattern mismatches.

**Requirement:** Apply RDKit's `MolStandardize.normalize()` to ensure consistent bond orders and charges before any feature detection.

### 0.3 Sanitization

**Requirement:** Always call `Chem.SanitizeMol()` with full error handling. Log failures via `smonitor` with the molecule ID and the specific sanitization error. Failed molecules must be moved to a `failures` list rather than silently discarded.

### 0.4 Molecular Weight and Drug-Likeness Pre-Filter (for Screening Databases)

**Why it matters:** Generating 3D conformers for millions of molecules is expensive. Filtering the database first to drug-like chemical space eliminates compounds that cannot be hits before spending any compute on them.

**Requirements:**
- Filter by molecular weight (default: 150–600 Da).
- Filter by Lipinski Ro5: MW ≤ 500, HBD ≤ 5, HBA ≤ 10, logP ≤ 5. Report violations but allow configurable strictness.
- Apply PAINS (Pan-Assay INterference compoundS) filter via RDKit's `FilterCatalog`. Compounds matching PAINS patterns are flagged, not silently removed.
- Expose all filter parameters as configurable arguments.

**Implementation target:** `filter_database(mols, mw_range=(150, 600), apply_ro5=True, flag_pains=True)` in `utils/preparation.py`.

---

## Phase 1: Molecular Preparation

### 1.1 Protonation State Assignment

**Why it matters:** A carboxylate at pH 7.4 is an HB Acceptor, not an HB Donor. An amine can be cationic (positive charge) or neutral (HB Donor) depending on its pKa. Assigning the wrong protonation state creates phantom or missing features.

**Requirements:**
- For **ligands**: assign the dominant microstate at pH 7.4 using a pKa model (RDKit's `MolStandardize`, or Dimorphite-DL for more accuracy).
- For **receptor residues**: assign protonation states for histidine (δ vs. ε tautomer), glutamate, aspartate, lysine, arginine, and cysteine based on local electrostatic environment.

**Implementation target:** `prepare_ligand(mol, pH=7.4)` and `prepare_receptor(system)` in `utils/preparation.py`.

**Current status:** Only `add_missing_hydrogens` (structural) is called. No pKa-based protonation.

### 1.2 Tautomer Enumeration and Canonicalization

**Why it matters:** Different tautomers expose different HBD/HBA features. A keto form has C=O (acceptor) and N-H (donor); the enol form changes both.

**Requirements:**
- For **training sets**: enumerate all chemically reasonable tautomers and use them all during feature detection.
- For **screening databases**: select the canonical dominant tautomer at pH 7.4 as the representative form.
- Integration point: `rdkit.Chem.MolStandardize.TautomerEnumerator`.

**Implementation target:** `enumerate_tautomers(mol, max_tautomers=10)` in `utils/preparation.py`.

### 1.3 Stereochemistry Handling

**Why it matters:** Undefined stereocenters produce incorrect 3D geometries. A molecule with 2 undefined stereocenters represents up to 4 real compounds with potentially different pharmacophoric profiles.

**Requirements:**
- For **training sets**: warn if an active has undefined stereocenters and optionally enumerate.
- For **screening databases**: enumerate undefined stereocenters up to a configurable limit (default: max 4 undefined centers → max 16 isomers).

**Implementation target:** `enumerate_stereoisomers(mol, max_centers=4)` in `utils/preparation.py`.

### 1.4 Conformer Generation

**Why it matters:** All modeling and screening requires 3D conformers. `ConformerGenerator` exists and is functional but is not integrated into any Modeler or `VirtualScreening`.

**Requirements:**
- `LigandBasedModeler.build()` must call `ConformerGenerator` for any molecule with zero conformers.
- `VirtualScreening.run()` must call `ConformerGenerator` for every database molecule with zero conformers.
- Expose `n_conformers`, `rmsd_threshold`, and `forcefield` at the Modeler and `VirtualScreening` level.

**Current status:** `ConformerGenerator` exists but is not called anywhere.

### 1.5 Protein-Specific SMARTS Patterns

**Why it matters:** `PROTEIN_SMARTS = LIGAND_SMARTS.copy()` is semantically incorrect. Protein features arise from specific residue patterns (backbone amide N-H, backbone C=O, Ser/Thr/Tyr hydroxyl, His imidazole, Lys amine, Arg guanidinium, Asp/Glu carboxylate, aromatic rings of Phe/Tyr/Trp/His).

**Requirements:** A separate `PROTEIN_SMARTS` dictionary with residue-aware patterns:
```python
PROTEIN_SMARTS = {
    "hb donor": [
        "[NH1,NH2;!$(N-[SX4](=O)(=O)[CX4](F)(F)F)]",  # backbone + sidechain NH
        "[OH1;$([OH][CX4,CX3])]",                       # Ser, Thr, Tyr
        "[nH1]",                                          # His imidazole NH
    ],
    "hb acceptor": [
        "[$([O]=C-[NX3])]",                              # backbone C=O
        "[$([O])&!$([OX2](C)C=O)&!$(*(~a)~a)]",         # sidechain oxygens
        "[#7;!$(N-[SX4](=O)(=O))]",                      # nitrogen acceptors
    ],
    "aromatic ring": [
        "a1aaaa1",   # 5-membered (His, Trp)
        "a1aaaaa1",  # 6-membered (Phe, Tyr, Trp)
    ],
    "hydrophobicity": [...],  # Val, Leu, Ile, Met aliphatic carbons
    "positive charge": [
        "N=[CX3](N)-N",   # Arg guanidinium
        "[NX4+;H3]",      # Lys ammonium
    ],
    "negative charge": [
        "[$([CX3](=O)[O-,OH])](=O)[O-,OH]",  # Asp, Glu carboxylate
    ],
}
```

**Current status:** `PROTEIN_SMARTS = LIGAND_SMARTS.copy()` — incorrect.

---

## Phase 2: Feature Detection

### 2.1 Deduplication and Overlap Resolution

**Current issue:** The same atom can match multiple SMARTS patterns within the same feature type (e.g., a phenol oxygen matching both HB Acceptor patterns), creating phantom duplicate sites.

**Requirement:** After detecting matches for each feature type, cluster overlapping atom groups (sharing > 50% of atoms) and keep one representative centroid per group.

### 2.2 Aromatic Ring Centroid and Normal

**Requirement:** For aromatic features, always compute both the ring centroid **and** the ring normal vector. Both are required for pi-stacking detection. `ring_normal()` in `utils/maths.py` already exists — it must be used consistently in all Modelers.

### 2.3 Feature Provenance Annotation

**Why it matters:** Each `InteractionSite` must carry metadata linking it to its biological origin so the model can be interpreted scientifically and visualized interactively (e.g., "this HB Acceptor corresponds to the backbone C=O of Lys203").

**Requirements:**
- Add a `provenance` dict to each `InteractionSite` (stored in `metadata`):
  ```python
  {
      'source': 'complex-based' | 'ligand-based' | 'structure-based',
      'residue_name': 'LYS',    # for complex/structure-based
      'residue_index': 203,
      'atom_indices': [1042, 1043],
      'mol_indices': [0, 2, 4],  # for ligand-based: which training molecules contributed
      'coverage': 0.85,          # fraction of training set this feature covers
  }
  ```
- `ComplexBasedModeler` must store which receptor residue/atom triggered each site.
- `LigandBasedModeler` must store which training molecule indices contributed to each consensus site.

---

## Phase 3: Pharmacophore Modeling

### 3.1 ComplexBasedModeler — Complete Interaction Set

#### 3.1.1 Aromatic Ring / Pi-Stacking

**Why it matters:** Pi-stacking is among the most frequent interactions in drug-receptor binding (kinases, GPCRs, nuclear receptors). Parameters are already defined in `RULES` but the detection code is absent.

**Geometry:**
- Centroid-to-centroid distance ≤ 0.75 nm.
- Face-to-face (parallel): angle between ring normals ≤ 30°; centroid projection offset ≤ 0.20 nm.
- Edge-to-face (T-shaped): angle between ring normals between 60° and 120°.

**Feature to create:** `AromaticRingSphereAndVector` at the ligand ring centroid, direction = ring normal.

**Reference implementation:**
```python
for l_indices in lig_feats['aromatic ring']:
    l_center = self._get_centroid(ligand_mol, l_indices)
    l_normal = ring_normal(l_indices, ligand_mol, l_center)
    for r_indices in rec_feats['aromatic ring']:
        r_center = self._get_centroid(receptor_bs_mol, r_indices)
        r_normal = ring_normal(r_indices, receptor_bs_mol, r_center)
        dist = self._dist(l_center, r_center)
        ang_dev = angle_between_normals(l_normal, r_normal)
        offset = self._ring_offset(l_center, r_center, l_normal)
        is_face_to_face = dist <= max_pi_dist and ang_dev <= pi_ang_dev and offset <= max_pi_offset
        is_t_shaped = dist <= max_pi_dist and 60 <= ang_dev <= 120
        if is_face_to_face or is_t_shaped:
            ph.add_interaction_site(AromaticRingSphereAndVector(l_center, '0.15 nm', l_normal))
            break
```

#### 3.1.2 Cation-Pi Interactions

**Geometry:** A cationic group centered 0.35–0.60 nm above an aromatic ring plane, angle between cation-to-centroid vector and ring normal ≤ 30°.

**Implementation:** Check ligand aromatic rings vs. protein positive charges, and ligand positive charges vs. protein aromatic rings. Create `CationPiSphere` at the ligand feature center.

#### 3.1.3 Water-Mediated Interactions

**Why it matters:** Conserved structural water molecules that bridge ligand-protein HB interactions are a real pharmacophoric feature in many targets (e.g., serine proteases, kinases). They must be detected in the input crystal structure, not ignored.

**Requirements:**
- Identify water molecules in the binding site (within `hb_dist_max` of both the ligand and the receptor simultaneously).
- If a water acts as a bridge (accepts HB from ligand, donates to receptor, or vice versa), add an `HBAcceptorSphere` or `HBDonorSphere` at the water oxygen position, flagged as `water_mediated=True` in provenance metadata.
- Expose a parameter `include_water_bridges=True`.

#### 3.1.4 Excluded Volume Generation

**Why it matters:** Excluded volumes encode where a ligand *cannot* go — regions occluded by the receptor. Without them, the model accepts molecules that would clash with the protein. Critical for selectivity and false-positive reduction.

**Requirements:**
- After extracting interaction sites, identify receptor atoms in the binding site that are **not** making pharmacophoric interactions.
- Place `ExcludedVolumeSphere` sites at the Van der Waals surface of those atoms.
- Expose `add_excluded_volumes=True` (default) and `excluded_volume_radius='0.15 nm'`.

#### 3.1.5 Global Site Merging

**Current issue:** `_merge_interaction_sites()` is called only for hydrophobicity.

**Requirement:** After all features are added, call `_merge_interaction_sites()` for every feature type with type-appropriate thresholds:
- Hydrophobic: 0.20 nm
- HB Donor / Acceptor: 0.10 nm (tighter, directional)
- Charge: 0.15 nm
- Aromatic: 0.10 nm

#### 3.1.6 Multi-Complex Consensus

**Why it matters:** It is very common to have 5-15 crystal structures of the same protein target with different co-crystallized ligands. The standard workflow is to run `ComplexBasedModeler` on each and then build a consensus across complexes, analogous to ligand-based consensus but starting from observed interactions.

**Requirements:**
- `ComplexBasedModeler` can already process multiple frames via `structure_indices`. Add support for a **list of separate molecular systems** (different PDB structures).
- After obtaining one `Pharmacophore` per complex, merge them using `Pharmacophore.merge()` and store site frequency (how many complexes contributed each feature) in the provenance `coverage` field.
- Sites present in ≥ 50% of complexes are marked `essential=True` by default.

### 3.2 LigandBasedModeler — Complete Algorithm

#### 3.2.1 Feature Coverage Tracking

**Why it matters:** A feature present in 10/10 actives is essential; one present in 3/10 is optional. This must be computed automatically and used to set `essential` flags and `weight` on each consensus site.

**Requirement:** For each `InteractionSite` in a consensus hypothesis, count how many training molecules have a matching feature within the site's radius. Store as `coverage` in provenance. Automatically set `essential=True` if coverage ≥ configurable threshold (default: 0.8), `essential=False` otherwise.

#### 3.2.2 Directional Features

**Current issue:** HBD/HBA in the consensus are created as generic `Sphere`, losing directional information.

**Requirement:** For HBD/HBA consensus sites, average the direction vectors of all contributing conformers/molecules and create `SphereAndVector` sites. Angular spread among contributors goes into provenance metadata.

#### 3.2.3 Negative Modeling (Inactive Compounds)

**Why it matters:** A model built only from actives cannot distinguish selective binders from promiscuous binders or inactives with similar shapes.

**Requirements:**
- Accept an `inactive_systems` parameter.
- Detect features in inactives that do not overlap (within tolerance) with any consensus site.
- Add those as `ExcludedVolumeSphere` sites with `provenance['source'] = 'negative-modeling'`.

#### 3.2.4 Activity Weighting

**Requirement:** Accept an optional `activities` list (Ki or IC50 as `Quantity`). Use activity-weighted scoring when ranking hypotheses: consensus groups that capture more potent actives score higher.

#### 3.2.5 Alignment-Based Consensus Refinement

**Current approach:** Distance fingerprint clustering — no actual 3D alignment.

**Requirement:** After distance-based grouping identifies clusters, perform pairwise Kabsch alignment within each cluster (`align_pharmacophores`) to verify spatial consistency and compute accurate 3D consensus centers.

### 3.3 StructureBasedModeler — Complete Implementation

#### 3.3.1 Automatic Pocket Detection

**Current issue:** Without `pocket_selection`, the entire receptor is used, producing hundreds of spurious sites.

**Requirements:**
- **Fallback (default, Gen 1b):** Accept `pocket_center` (3-vector or `Quantity`) + `pocket_radius` (distance `Quantity`) to define the binding site sphere. This is the primary route for Gen 1b because `topomt` is still in early development.
- **Optional `topomt` integration:** Guard with `@dep_digest('topomt')`. When `topomt` is installed and `pocket_selection=None` and no center/radius are provided, call `topomt.get_pockets(molecular_system)` and use the largest pocket. This integration must be entirely optional.
- If none of the above are provided, raise an informative `PHMT-E`-coded error rather than silently using the full receptor.

**Note on topomt maturity:** As of Gen 1b, `topomt` is in early/mid-stage development and its API may change. Never hard-depend on it; always use `depdigest.is_installed('topomt')` before calling any `topomt` function.

#### 3.3.2 Excluded Volume Generation

**Requirement:** After projecting interaction sites into the cavity, sample non-interacting receptor surface atoms facing the cavity and add `ExcludedVolumeSphere` sites.

---

## Phase 4: Model Refinement

### 4.1 InteractionSite Data Model Extensions

The `InteractionSite` class requires two new attributes for Gen 1b:

```python
class InteractionSite:
    # Existing
    shape: Shape
    features: list[str]
    # New in Gen 1b
    essential: bool = True        # must be matched in screening
    weight: float = 1.0           # contribution to Fit Value
    metadata: dict = {}           # stores provenance, coverage, etc.
```

### 4.2 Feature Toggle (Essential vs. Optional)

Each `InteractionSite` carries an `essential` flag. Essential features must be matched in virtual screening; optional features improve the score but are not required.

```python
ph.interaction_sites[3].essential = False
ph.set_essential(feature_name='hb donor', essential=False)  # batch
```

### 4.3 Tolerance Adjustment

```python
ph.set_radius('all', '0.15 nm')
ph.set_radius(feature_name='hb donor', radius='0.1 nm')
ph.set_radius(index=2, radius='0.2 nm')
```

### 4.4 Excluded Volume Management

```python
ph.add_excluded_volumes_from_receptor(molecular_system, radius='0.15 nm')
```

### 4.5 Pharmacophore Comparison and Merging

```python
similarity = ph_complex.similarity(ph_ligand)   # float 0–1, overlap after alignment
ph_combined = ph_complex.merge(ph_ligand)        # union with averaged overlapping sites
```

### 4.6 Pharmacophore Serialization — Complete Coverage

When a `Pharmacophore` is saved to JSON or YAML, **all** attributes must be preserved and restorable:
- `name`, `description`, `score`, `ref_mol`, `ref_struct`
- For each `InteractionSite`: shape (all types, not just sphere/sphere+vector), features, `essential`, `weight`, `metadata` (provenance, coverage)

**Current gap:** `_from_dict()` in the PHMT IO module raises `NotImplementedError` for shapes other than `sphere` and `sphere and vector`. All seven shapes (Point, Sphere, SphereAndVector, GaussianKernel, Shapelet, Disk, Cylinder) must be fully serializable.

### 4.7 `Pharmacophore.show()` Without Molecular System

**Current issue:** `show()` calls `msm.view(self.molecular_system)`, which fails if `molecular_system=None`. Ligand-based pharmacophores have no associated system.

**Requirement:** `show()` must handle `molecular_system=None` gracefully, rendering only the pharmacophore glyphs in an empty MolSysViewer scene.

---

## Phase 5: Validation

### 5.1 Leave-One-Out (LOO) Validation

**Protocol:**
1. For each active `i` in the training set:
   a. Build a pharmacophore excluding compound `i`.
   b. Screen compound `i` against it.
   c. Record whether `i` is recovered (Fit Value ≥ threshold or RMSD ≤ cutoff).
2. Report LOO recall: `n_recovered / N`.
3. LOO recall < 0.70 → warn that the hypothesis may be over-fitted or too narrow.

**Target:** `pharmacophoremt.validation.validate_loo(modeler, actives, cutoff_rmsd=2.0, fit_value_threshold=0.7)`.

### 5.2 Enrichment Factor (EF)

**Protocol:**
1. Prepare: known actives + decoys (ratio 1:39, from DUD-E or property-matched).
2. Screen and rank by Fit Value (descending) or RMSD (ascending).
3. `EF(x%) = (actives in top x%) / (x% × total_actives)`. Report at x = 1%, 5%, 10%.
4. EF@1% ≥ 10: good model. EF@1% < 2: poor model.

**Target:** `pharmacophoremt.validation.compute_enrichment_factor(matches, actives_ids, fractions=[0.01, 0.05, 0.10])`.

### 5.3 BEDROC (Boltzmann-Enhanced Discrimination of ROC)

**Why it matters:** BEDROC is preferred over EF in pharmaceutical research because it provides a statistically rigorous, parameter-free summary of early enrichment that does not depend on an arbitrary fraction cutoff.

**Definition:**
```
BEDROC(α) = (Ra × sinh(α/2)) / (cosh(α/2) - cosh(α/2 - α×Ra×n/N)) + 1/(1 + e^(α(1-2Ra)))
```
where `α` is a parameter weighting early enrichment (default α = 20.0 for 80% weight on top 8% of database), `Ra` is the ratio of actives, `n` the number of actives in the early portion, `N` total compounds.

**Target:** `pharmacophoremt.validation.compute_bedroc(matches, actives_ids, alpha=20.0)`.

### 5.4 ROC Curve and AUC

**Target:** `pharmacophoremt.validation.compute_roc(matches, actives_ids)` → `(fpr, tpr, auc)`.

AUC thresholds: 0.5 = random; 0.7 = acceptable; 0.8 = good; 0.9 = excellent.

### 5.5 Hit Rate

**Target:** `pharmacophoremt.validation.compute_hit_rate(matches, actives_ids, cutoff_rmsd=2.0)` → `float`.

### 5.6 Benchmark Datasets

Standard datasets must be available in `pharmacophoremt.data` via `load_benchmark(name)`:

| Target | PDB complex | Actives | Decoys |
| :--- | :--- | :--- | :--- |
| Estrogen Receptor α | 1ERE | ChEMBL / DUD-E | DUD-E |
| DHFR | 1DRF | ChEMBL / DUD-E | DUD-E |
| Thrombin | 2ZC9 | ChEMBL / DUD-E | DUD-E |

`load_benchmark(name)` returns `(complex_system, actives, decoys)` ready for use.

---

## Phase 6: Virtual Screening

### 6.1 Input Format Flexibility

**Current issue:** `VirtualScreening.run()` takes `molecular_database` as an iterable but doesn't specify or validate what forms are acceptable.

**Requirements:** `molecular_database` must accept all of:
- `list[str]` — SMILES strings.
- `str` — path to a SMILES file or SDF file (auto-detected by extension).
- `list[rdkit.Chem.Mol]` — RDKit Mol objects.
- `list[molsysmt.MolSys]` — molsysmt systems.
- `pandas.DataFrame` with a `smiles` or `SMILES` column.

Each input form is converted internally via `msm.convert()` or `Chem.MolFromSmiles()` as appropriate.

### 6.2 Database Pre-Processing Pipeline

Before matching, each database molecule passes through:
1. **Phase 0**: standardize → desalt → normalize → sanitize.
2. **Phase 0.4**: drug-likeness filter (configurable, default Ro5 + MW range).
3. **Phase 1.1–1.3**: protonation, tautomer, stereoisomer (optional, off by default for large databases due to cost).
4. **Phase 1.4**: conformer generation if molecule has zero conformers.

All these steps are configurable via `VirtualScreening.__init__` parameters.

### 6.3 Pharmacophore-Native Feature Factory

**Current issue:** `VirtualScreening` uses RDKit's `BaseFeatures.fdef`, which does not match `pharmacophoremt`'s `LIGAND_SMARTS`. The same molecule can appear to have different features in the model and in the screening step.

**Requirements:**
- Generate a custom `.fdef` file from `LIGAND_SMARTS` at library initialization time (`io/fdef.py`).
- `VirtualScreening` must use this native factory for all feature detection.
- This ensures complete consistency: the same SMARTS detect features during model building and during screening.

### 6.4 Partial Matching (Essential + Optional Features)

**Current issue:** RDKit's `EmbedLib.MatchPharmacophoreToMol()` requires all features to match. Molecules matching all essential + some optional features are discarded.

**Requirements:**
- Essential features must all match (hard constraint).
- Optional features contribute to the Fit Value but are not required.
- Strategy: first attempt full match; if it fails, retry with all subsets of optional features excluded; accept the best partial match that covers all essentials.

### 6.5 Directional Feature Matching (Tolerance Angle)

**Why it matters:** `SphereAndVector` sites encode directionality (e.g., the H-bond vector). During screening, if a molecule's matching feature has a direction vector that deviates too far from the pharmacophore site direction, it should not be considered a valid match even if the distance is within the sphere radius.

**Requirements:**
- For each `SphereAndVector` site, after geometric embedding, compute the angle between the pharmacophore direction and the matched molecule's feature direction.
- Reject match if angle > configurable threshold (default: 30°).
- Expose `direction_tolerance_angle=30.0` as a `VirtualScreening` parameter.

### 6.6 Fit Value

**Definition:**
```
FitValue = Σ(weight_i for matched features i) / Σ(weight_i for all features)
```
where `weight_i` is `InteractionSite.weight` (default 1.0). Essential features that fail to match make FitValue = 0 for that molecule.

**Requirement:** Compute and store `fit_value` in each match result alongside `rmsd`.

**Score thresholds (defaults, configurable):**
- Hit: FitValue ≥ 0.7 AND RMSD ≤ 2.0 Å.
- Strong hit: FitValue ≥ 0.9 AND RMSD ≤ 1.5 Å.

### 6.7 Multi-Conformer Screening

**Requirement:** For each molecule, screen all conformers and report the best match (highest FitValue, then lowest RMSD). Store the conformer index in the result.

### 6.8 Excluded Volume Clash Detection

**Requirement:** After feature matching, check that the matched conformation does not clash with any `ExcludedVolumeSphere` in the pharmacophore. A clash is defined as any atom of the candidate molecule falling within the excluded volume radius. Clashing molecules are discarded or penalized in the score.

### 6.9 Results Structure

Each match result must be a well-defined dict:
```python
{
    'mol': original_mol,
    'mol_id': str,
    'rmsd': float,               # Å, of matched features
    'fit_value': float,          # 0–1, weighted feature coverage
    'n_matched': int,            # number of features matched
    'n_total': int,              # total features in pharmacophore
    'n_essential_matched': int,  # essential features matched (must == n_essential for a hit)
    'conf_idx': int,             # which conformer matched
    'aligned_rdkit_mol': Mol,    # aligned 3D structure
    'matched_features': list,    # pharmacophore feature indices that matched
    'ev_clash': bool,            # True if any excluded volume was violated
}
```

### 6.10 Results Export

```python
vs.to_dataframe()          # pandas DataFrame with all fields
vs.to_sdf(path)            # SDF file with RMSD, FitValue, NMatched as SD tags
vs.to_csv(path)            # CSV for spreadsheet analysis
```

### 6.11 Error Handling and Reporting

**Current issue:** Bare `except:` clauses silently discard molecules.

**Requirement:**
- Catch specific exceptions (`Chem.AtomValenceException`, `ValueError`, etc.).
- Log each failure via `smonitor` with molecule ID, failure stage, and exception message.
- Return a `failures` list alongside `matches`, containing `{'mol_id': ..., 'stage': ..., 'reason': ...}`.

---

## Phase 7: Post-Screening Analysis

### 7.1 Hit Visualization (Primary Deliverable)

**Why it matters:** The primary output a medicinal chemist needs is a 3D view of the top hits superimposed on the pharmacophore. This is the deliverable that drives experimental follow-up.

**Requirements:**
- `VirtualScreening.show(top_n=10, view=None)` — creates or reuses a MolSysViewer instance, adds the pharmacophore glyphs, and overlays the top-N aligned hit structures.
- Uses `pharmacophore.add_to_molsysviewer(view)` followed by per-hit coordinate rendering.
- Color-code hits by FitValue (green = perfect, red = marginal).

### 7.2 Hit Clustering

**Why it matters:** Thousands of hits must be reduced to a manageable set of diverse scaffolds for experimental follow-up.

**Requirement:** `cluster_hits(matches, method='butina', threshold=0.4)` using RDKit's Butina algorithm on Morgan fingerprints (radius 2). Returns cluster labels and cluster representatives (the hit with best FitValue per cluster).

### 7.3 Pharmacophore-Activity Relationship (PhAR)

**Requirement:** Given hits with experimental activity data, compute the correlation between the presence/absence of each pharmacophore feature match and activity. Identifies which features are most predictive.

**Target:** `compute_phar(matches, activities)` → per-feature correlation coefficients.

### 7.4 False Positive Characterization

**Why it matters:** Analyzing patterns in false positives (molecules that match the pharmacophore but are known inactives) guides model refinement — where to add excluded volumes or tighten tolerances.

**Requirement:** `characterize_false_positives(matches, actives_ids)` → identifies structural patterns (SMARTS) common among false positives. These patterns can be reviewed to add excluded volumes or tighten specific site tolerances, closing the loop back to Phase 4.

### 7.5 Pharmacophore Comparison

**Requirement:** `Pharmacophore.similarity(other)` — scalar overlap score (0–1) after optimal alignment using `align_pharmacophores`. Used to compare complex-based vs. ligand-based results on the same target.

### 7.6 Benchmark Runner

**Requirement:** `pharmacophoremt.validation.benchmark(pharmacophore, dataset_name)` — loads a built-in benchmark, runs screening, and reports LOO recall, EF@1%/5%/10%, BEDROC, and AUC in a single call.

---

## Summary: Implementation Priorities for Gen 1b

| Priority | Task | Phase | Blocks |
| :---: | :--- | :---: | :--- |
| 1 | Fix `PROTEIN_SMARTS` (residue-aware patterns) | 1.5 | All complex/structure-based modeling |
| 2 | Complete IO `_from_dict()` for all 7 shapes | 4.6 | Native format persistence |
| 3 | Integrate `ConformerGenerator` in `LigandBasedModeler` | 1.4 | Ligand-based modeling |
| 4 | Integrate `ConformerGenerator` in `VirtualScreening` | 1.4 | Screening of any real database |
| 5 | Add `essential` and `weight` to `InteractionSite` | 4.1 | Screening stringency + Fit Value |
| 6 | Add provenance annotation to all Modelers | 2.3 | Interpretability |
| 7 | Implement pi-stacking in `ComplexBasedModeler` | 3.1.1 | ~30% of drug targets |
| 8 | Implement `ExcludedVolumeSphere` generation (Complex & Structure) | 3.1.4 | Selectivity, false-positive reduction |
| 9 | Implement excluded volume clash detection in `VirtualScreening` | 6.8 | Screening quality |
| 10 | Build native RDKit feature factory from `LIGAND_SMARTS` | 6.3 | Modeling/screening consistency |
| 11 | Implement partial matching + directional tolerance | 6.4–6.5 | Screening quality |
| 12 | Implement Fit Value | 6.6 | Screening scoring |
| 13 | Fix `VirtualScreening` error handling (bare except → smonitor) | 6.11 | Reliability |
| 14 | Implement multi-conformer screening | 6.7 | Screening completeness |
| 15 | Add `VirtualScreening.show()`, `to_dataframe()`, `to_sdf()` | 7.1 / 6.10 | Primary deliverable |
| 16 | Extend site merging to all feature types | 3.1.5 | Model cleanliness |
| 17 | Implement LOO validation | 5.1 | Model validation |
| 18 | Implement EF, BEDROC, ROC | 5.2–5.4 | Model validation |
| 19 | Add `VirtualScreening` input format flexibility | 6.1 | Usability |
| 20 | Add molecular standardization (`standardize_mol`, `filter_database`) | 0.1–0.4 | Database pre-processing |
| 21 | Implement multi-complex consensus in `ComplexBasedModeler` | 3.1.6 | Multi-structure workflow |
| 22 | Add feature coverage tracking in `LigandBasedModeler` | 3.2.1 | Auto-assignment of essential flag |
| 23 | Fix `Pharmacophore.show()` when `molecular_system=None` | 4.7 | Ligand-based usability |
| 24 | Implement negative modeling in `LigandBasedModeler` | 3.2.3 | Selectivity |
| 25 | Add protonation state assignment (`prepare_ligand`) | 1.1 | Feature correctness |
| 26 | Add tautomer enumeration | 1.2 | Feature correctness |
| 27 | Implement cation-pi in `ComplexBasedModeler` | 3.1.2 | Completeness |
| 28 | Implement water-mediated interactions | 3.1.3 | Accuracy in crystal structures |
| 29 | Automatic pocket detection (fallback sphere) | 3.3.1 | Structure-based usability |
| 30 | Add `Pharmacophore.similarity()` and `merge()` | 4.5 | Model comparison |
| 31 | Hit clustering | 7.2 | Post-screening analysis |
| 32 | Add activity weighting in `LigandBasedModeler` | 3.2.4 | Training quality |
| 33 | Alignment-based consensus refinement | 3.2.5 | Ligand-based quality |
| 34 | Implement BEDROC benchmark function | 7.6 | Continuous validation |
| 35 | False positive characterization | 7.4 | Iterative model improvement |
| 36 | Add benchmark datasets to `data/` | 5.6 | Automated testing |
