# Strategic Roadmap

## Current priorities — 2026-10-10

The native class/default routes now require prepared input and explicit scientific
choices: ligand consensus (#18), observed-complex construction (#42), cached
receptor projections (#44), and placed/rigid/prepared-conformer screening (#45).
Orphaned general molecular utilities and the historical library reader are
retired (#46). Versioned pharmacophore SDF persistence preserves its declared
six-shape/native-payload contract (#47); the attribution subprocess import guard
is repaired (#48). General molecular preparation, geometry and molecular library
I/O remain MolSysMT responsibilities.

The authored-diagnostic rendering and zero-angle comparison corrections are
reviewed under #2/#16 with fresh controls and archived reports. Their original
archive checkpoints retain their dated evidence. These narrow closures do not
close every implemented workflow's scientific/API review.

The prepared end-to-end control (#49) now reviews cached inventory construction,
explicit ring/hydrophobic curation, JSON/YAML/versioned PHMT SDF recovery and
ranked placed screening on public CCD EST. Independent displacement, exclusion,
failure and stable-tie controls pass with preserved maps/history and detached
readers; see [the contract](prepared_end_to_end_workflow.md). This advances the
bounded analytical acceptance gate while MolSysMT #375 remains post-1.0 work.
It does not establish biological discrimination or close every classical route.

The rigid/frame continuation (#50) adds explicit non-collinear essential anchors,
saved-query proper-motion recovery, complete selected-participant negatives and
budget-failure/ensemble-resolution controls; see [the contract](prepared_search_workflow.md).
It reuses existing tools and keeps 29 prior evidence archives unchanged. These
prepared placements do not supply generated conformers or activity validation.

The next steps are:

1. Complete inspection of the applicable hosted matrix and installed/public
   delivery gates under #9/#10/#23. A passing focused run or one matrix cell
   cannot stand for all Python versions/platforms or a public artifact.
2. Extend the bounded prepared native workflow review to independently declared
   consensus or activity-based validation cases. Reuse existing
   method/recipe/evidence tools; define independent positive/negative controls
   and preserve original inputs, states, mappings and failures. The collection
   and the ERα continuation remain tracked in #20/#22. Prepared/analytical
   controls do not by themselves establish biological or activity-based success.
3. Finish the remaining consumer migration in #41 when MolSysMT #375 supplies
   a qualified public geometry contract. Its only retained molecular arithmetic
   is the bounded donor-H displacement/normalization in `get_features()`; do not
   recreate missing provider geometry in PHMT. Independent preparation (#219),
   molecular collection/property correspondence (#215 follow-up / #223) and
   environmental H refinement (#323) stay with their provider owners.

Automatic pocket/direction hypotheses, viewer/docking integration, biological
pilots and strategy/performance comparisons remain separate acceptance work.
Advanced dynamic or accelerated methods follow the classical acceptance gate.

## Historical checkpoints

The dated checkpoints below record the state and then-next step at each
measurement. Current priorities above supersede completed next-step instructions;
original provider limitations and measurements keep their original scope.

**2026-10-10 utility retirement (#46):** The orphaned molecular utility package
and name-grouped SDF reader are removed, with matching distribution inventory
updates. Retained `openpharmacophore` notebooks are explicitly historical;
their original data/output bytes stay unchanged. See [the retirement contract](molecular_utility_retirement.md).
#41 remains partial for donor-H geometry delegation to MolSysMT #375; provider
preparation/collection/environment-refinement requirements stay in their owners.

**2026-10-10 screening transition (#45):** `VirtualScreening` now requires an
explicit placed/rigid/prepared-conformer method and delegates to native tools;
see [the contract](virtual_screening_workflow.md). Legacy preparation/matching,
implicit validator fallbacks and local molecular SDF export are retired.
CSV contains scalar hit evidence. #41 remains partial for unused generic
utilities/library ingestion and donor geometry delegation (MolSysMT #375).
Next local work is that bounded utility/caller inventory and retirement; provider
#219/#215/#223/#323 remain independent capabilities, not local implementation tasks.

**2026-10-10 structure transition (#44):** Structure-based construction now
consumes cached receptor inventories and explicit pharmacophoric projections;
see [the contract](structure_based_workflow.md). The old local recognition,
selection and neighbor/+z inference are retired. Automatic pocket hypotheses
remain future work. Donor-pair/local acceptor geometry is requested in MolSysMT
#375, including the outstanding donor-vector migration in `get_features()`.
#41 remains partial; next local work is legacy screening/preparation retirement.

**2026-10-10 complex transition (#42):** `ComplexBasedModeler` and the default
`model()` now require prepared native observations and an explicit ligand
selection. The old preparation/detection engine is retired; see the
[migration contract](complex_based_workflow.md). This supersedes the default-route
finding in the earlier audit checkpoint below. #41 remains partial; next local
work is structure-based provider consumption and legacy screening retirement.
Provider #323/#350/#367 remain independent limitations.

**2026-10-10 ownership review:** The
[molecular ownership audit](pending_proposals/retire_legacy_molecular_operations.md)
tracks remaining reachable legacy preparation/recognition/I/O under #41. Native
workflows delegate molecular operations to MolSysMT, but `model()` still defaults
to the legacy complex builder. Next local work is its explicit prepared-input
transition, followed by structure-based provider consumption and legacy screening
retirement. Do not extend local molecular utilities. Conformer generation remains
provider #219; optional standardization is proposed in #366, and a reproduced
public-fit degeneracy defect is #367. The #31 automatic seed guard is reviewed
with 60 focused cases and 680 full-suite tests; it does not repair arbitrary
provider fits. Existing #323/#350 limitations remain explicit. Docking-specific
contracts belong to DockingMT; no new docking-owned gap was identified in this
source audit.

**2026-10-07 ERα checkpoint:** The maintained declared 304–550 fragment/EST
chain and its independent placed/exclusion/persistence controls are delivered.
[Empty-family diagnosis](eralpha_interaction_diagnostics.md) now distinguishes
recognized participants from geometric rejection: local generated H fail the
declared H-bond angular gate; PHE404/EST fail the reference pi-pi intersection
gate. Environmental H refinement remains MolSysMT #323, and public rejected-pair
geometry diagnostics are requested in #350. These controls do not establish
complete receptor preparation or activity-based validation; Gen 1b remains the
current acceptance focus.

**2026-10-02 review checkpoint:** Traditional workflows are the immediate
acceptance gate. The native [observed-complex slice](placed_pose_workflow.md) and
[reference-ligand slice](reference_ligand_workflow.md) are implemented locally
with analytical controls. [Growth contracts](extensible_modeling_contracts.md)
record the accepted ownership and method/backend/execution separation. Local
verification does not qualify legacy routes or establish biological-pilot success.

The development of PharmacophoreMT is divided into generations. **Gen 1b** has been added between the original Gen 1 and Gen 2 after an audit revealed that the classical pharmacophore workflow was incomplete and required consolidation before advancing to dynamic modeling.

---

## Gen 1: Historical Foundation Deliveries
These historical delivery marks mean code exists, not that all scientific or
integration contracts have passed the current classical acceptance gate.

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

The accepted implementation order is below. The older detailed feature catalog
in [`classical_workflow.md`](classical_workflow.md) retains scientific backlog
ideas; its direct-RDKit and hidden-preparation proposals are superseded.

### 1. Shared chemical definitions and placed-pose controls
- [x] Strict explicit units, validated geometry, essential/weight/site metadata.
- [x] Observed-complex construction for native hydrophobic/H-bond interactions (#13).
- [x] Reusable chemical extraction and reference-ligand queries with six classical families (#14).
- [x] Shared pose evaluation, directional/plane controls, one-to-one assignments and exclusion veto.
- [x] Retrospective ROC/AUC, BEDROC and EF with correct ties and explicit failure accounting (#12; reviewed closure 2026-10-07, independent ranking and native/legacy accounting guards).
- [x] Source/state/method provenance and native persistence for these delivered slices.
- [ ] Scientific/API review and biological-pilot validation of these slices.
- [ ] General extension registration, stable site identity and complete portable codecs.

### 2. Native traditional workflows
- [x] Bounded rigid triplet search and prepared-ligand alignment through MolSysMT (#15); continuous exhaustive search remains outside this method.
- [x] Screen prepared multi-frame conformers with best-pose/state evidence and explicit failure accounting (#17).
- [ ] Provider-supported conformer preparation; resolve missing tools in MolSysMT.
- [ ] Ligand/complex consensus with coverage, explicit frames and curated essential/weight policies.
- [x] First reference-anchored consensus from prepared aligned ligands, with reusable matching/aggregation, unique ligand support and portable evidence (#21).
- [x] Bounded aligned clique discovery and alternative jointly supported hypotheses, with reusable tools, independent subset controls and executed-method attribution (#24).
- [x] First prepared rigid unaligned consensus with explicit pivot, maximal association mappings or triplet seeds, MolSysMT fits and alternative layout evidence (#26); see [the contract](rigid_consensus_workflow.md).
- [x] Public inventory-to-query, explicit-mapping placement and saved-report summary tools; six frozen analytical comparison controls (#27), with [modular contracts](rigid_strategy_comparison.md) and an [executable recipe](../docs/content/cookbook/modular_rigid_tools.md).
- [x] Typed-neighborhood comparison and supplied-triplet ranking tools, consumed by ranked_triplet_seeds with explicit selection/false-negative controls (#28); this is the G3PS seed stage, not full greedy refinement.
- [x] Public pair evaluation and greedy rigid refinement with final/each_step angular policies, best valid checkpoint retention and reciprocal analytical controls (#29). Both variants remain available; eleven seed/tolerance/mixed-family/3D workloads now have retained coverage, runtime and scoped-memory comparisons.
- [x] Traceable prepared real chemical components (CCD ideal EST/DES) with public MolSysMT preparation, refinement/consensus/frame-screening controls, retained hypotheses and actual resource/method citation capture (#30). This does not establish experimental conformer or biological performance.
- [x] Observed 1QKU EST heavy-atom template integration through public MolSysMT assessment/application, with selected acceptor/aromatic placed controls, persistence and actual input citations (#22). Receptor/biological acceptance remains pending.
- [x] Explicit fixed-state H placement through the resolved MolSysMT #300 tool, with donor-inclusive observed-pose evaluation, persistence and both rigid recovery policies (#22). Local generated H geometry does not establish environment refinement or biological acceptance.
- [x] Observed receptor residue/readiness audit through public MolSysMT #217/#218 diagnostics, with declared spatial scopes, preserved detector failures and actual-data-only credit (#22). The declared fragment adopts delivered MolSysMT #298 template preparation; complete-receptor acceptance remains open.
- [x] Maintained declared receptor-fragment/EST composition, independent placed/orientation/exclusion/persistence controls and fixed empty-family diagnosis (#22). Recognition and geometric rejection are distinguished without changing the original observations; environmental H refinement remains provider #323.
- [ ] Compare G3PS, safe RDP/frequent-clique conformer discovery and triangle indexing on controlled workloads; see [the primary-source survey](pharmacophore_search_strategies.md).
- [x] Review recursive partitioning/clique literature and execute bounded legacy counterexamples (#18); see [the consensus review](clique_consensus_review.md).
- [x] Retire the defective legacy ligand consensus builder; preserve its audit and expose explicit rigid/aligned native choices through the class and dispatcher (#18); see [the migration contract](ligand_based_workflow.md).
- [x] Extend native complex construction to aromatic/charge interaction families with independent controls.
  The first ionic extension now calls shared public charge-feature tools and
  retains compound membership/geometry, contact evidence and actual attribution
  (#33; [contract](ionic_interaction_workflow.md)). Pi-pi/cation-pi conversion now
  supports seven declared profiles, shared geometry and explicit atomic-to-compound
  cation mapping (#34; [contract](aromatic_interaction_workflow.md)). Prepared
  analytical controls do not establish biological complex validation.
- [ ] Native structure-based hypotheses using TopOMT pockets and MolSysMT molecular geometry.
  The explicit cached hypothesis constructor and historical facade transition
  are delivered under #44. Automatic provider-informed directions/pockets and
  biological qualification remain separate from this controlled projection tool.
- [x] Public common-frame hypothesis composition and named native interaction-collection conversion (#36), with labeled evidence, explicit keep/participant-reuse policies, independent controls and preserved empty/failure semantics. Disconnected prepared controls do not establish biological complex acceptance.
- [x] Joint native interaction controls with complete frozen CCD EST/DES molecules (#37), two caller-declared rigid placements and both participant roles. Existing public tools retain neutral empty families, duplicate-profile evidence, directional controls and an independent DES steric veto; designed CCD pairs do not establish biological complex acceptance.
- [x] Independent cached-model selection, copying, extraction and explicit constraint editing (#38), with class delegation, source-model history, score invalidation, distinct radius/sigma semantics and independent essential/weight/exclusion controls. Scientific/API review and activity-based comparison remain open.
- [x] Standalone exclusion-sphere construction from cached MolSysMT heavy-atom geometry, with explicit constant-radius choices, independent veto controls, native persistence and an observed receptor continuation (#32). Physical-radius/surface/pruning strategies and biological validation remain open; do not infer steric volumes from inactive-only features.
- [ ] Refinement, validated I/O and inspectable MolSysViewer/DockingMT workflow integration.
- [ ] Execute the chosen public vertical pilots with declared preparation, independent controls and no leakage.

### 3. Product and ecosystem closure
- [ ] Complete molecular geometry delegation to MolSysMT (#41 / #375).
  Prepared class/default transitions and obsolete utility/reader retirement are
  delivered under #18/#42/#44/#45/#46. The remaining bounded donor-H arithmetic
  in `get_features()` awaits the provider contract; broad molecular ownership
  and provider scientific acceptance are not inferred from those retirements.
- [x] Implement own deferred native Ackredit capture and portable bibliography (#19); see [the cookbook](../docs/content/cookbook/attribution.md).
- [ ] Review the attribution contract and verify optional-integration distribution support (#6, #19).
- [ ] Confirm production dependency/distribution closure (#10) and required hosted CI evidence (#9).
- [ ] Verify independent routes for all three traditional modeling approaches before claiming consolidation.
- [x] Collect validation/benchmark cases through the existing documentation and original evidence archives (#20; publication/layout decision, contribution template, ownership/execution policy and frozen CCD demonstrator).

### 4. Measured acceleration and future contracts
- [ ] Profile representative matching/search workloads after establishing reference equivalence guards.
- [ ] Introduce Rust for measured pharmacophoric bottlenecks; molecular kernel ownership stays in MolSysMT.
- [ ] Design bounded arrays/membership data and deterministic reductions for parallel/distributed or GPU execution.
- [ ] Extend relations, uncertainty, coordinate frames and ensemble contracts as advanced methods need them.

Scientific method, compute backend and execution plan remain independent axes.
No Rust, GPU or distributed PHMT implementation is claimed by the current slice.

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
