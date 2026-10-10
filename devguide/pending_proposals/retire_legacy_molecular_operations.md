---
summary: Retire general molecular operations from reachable legacy workflows.
issue: uibcdf/pharmacophoremt#41
status: partial
opened: 2026-10-10
closed:
verification: measured
area: [architecture, modeling, screening, integration]
guard:
normative: devguide/extensible_modeling_contracts.md
blocked_by: []
supersedes: []
---

# Molecular ownership audit and bounded legacy retirement

## Progress — 2026-10-10, structure transition (#44)

`StructureBasedModeler` and its dispatcher now delegate cached chemical records
and explicit hypothesis decisions to reusable `from_receptor_projections()`.
Local spherical selection, RDKit SMARTS, centroids/ring geometry and first-neighbor
or arbitrary +z direction inference are removed from that route. Optional cached
exclusions delegate to `get_excluded_volume_sites()`, with explicit radius and
common declared selection/frame/state. See [the contract](../structure_based_workflow.md)
and [#44 report](../archive/native_structure_modeler_transition.md).

This is explicit query construction, not automatic chemically informed pocket
modeling or biological equivalence. Inventory origin/common coordinates remain
caller declarations. The review also found donor–H vector subtraction and
normalization inside native `get_features()`: recognition/centers/planes are
provider-mediated, but this geometry operation is not yet migrated. Public
donor-pair/local acceptor directions are requested in **uibcdf/molsysmt#375**.
Do not add another local kernel. Existing donor-vector retention remains bounded
by this record's 2026-10-17 review date, with PHMT maintainers responsible and
removal when a qualified public provider contract is consumed. This qualifies
the earlier audit's broad native-geometry claim rather than rewriting its evidence.
#41 stays partial/open for this gap and remaining screening, I/O and utilities.

## Progress — 2026-10-10, complex transition (#42)

The complex modeler and default dispatcher now consume named native MolSysMT
observations on the same unchanged prepared source with an explicit ligand
selection, delegating to `from_interaction_collection()`. Local inference,
preparation, SMARTS detection, detector geometry and spatial merging have been
removed from that route. The [migration contract](../complex_based_workflow.md)
and [#42 record](../archive/native_complex_modeler_transition.md) define this breaking
scientific transition. The original audit below remains dated source evidence;
its complex caller finding is now retired. #41 remains **partial/open** for the
other inventoried routes, including structure-based and legacy screening. The
bounded review date and provider gaps remain in force for those retained callers.

## What

The native prepared-input workflows use public MolSysMT chemistry, recognition,
geometry and molecular transformations. The package as a whole is not yet
architecturally migrated: exported legacy modelers and screening still implement
general molecular operations. In particular, `pharmacophoremt.model()` defaults
to `complex-based`, which reaches legacy molecular inference. Merely delivering
native alternatives does not retire that public default.

This audit follows the accepted modular-tool rule and the user's explicit
ownership instruction. MolSysMT owns general molecular operations; PharmacophoreMT
owns pharmacophore models and scientific criteria; DockingMT owns docking protocols,
sampling/scoring composition and engine integration. MOLI delegates suite-internal
contracts to MolSysSuite. No new platform policy is required for this finding.

## How: inspected boundaries and actual callers

Consumer source: `a504a01a06876f66093ff88887dd6049d26fbffa`, with a separate
test-only #31 overlay. The audit inspected the package's public exports,
dispatcher, native and legacy modeling/screening paths, general utilities,
molecular/pharmacophore I/O, and the maintained preparation recipes. Source
identities are retained in
`devguide/evidence/molecular_ownership_audit_20261010.json`.

| Operation and consumer call | Owner and present boundary | Finding / next action |
| --- | --- | --- |
| `modeler.features.get_features()` | MolSysMT `physchem.get_hydrophobic_sites`, `get_hbond_sites`, `get_aromatic_rings`, `get_charge_centers`; `structure.get_least_squares_plane` / `get_center` | Native recognition and ring/charge geometry delegate correctly. PHMT chooses the versioned feature interpretation and constructs pharmacophoric records. |
| `screening.alignment.align_to_pharmacophore()` | MolSysMT `Structures`, `structure.least_rmsd_fit`, `get_rmsd`, `copy`, `get`, `set` | Native fit and coordinate mutation delegate correctly, but the provider's degeneracy contract fails the measured control below: uibcdf/molsysmt#367. |
| Rigid placement, refinement, search and consensus | PHMT proposal/assignment criteria call the above alignment boundary | Pharmacophoric correspondence graphs, feature tolerances, ranking and hypothesis selection remain PHMT. These are not an implementation of a docking engine. |
| `from_interactions()` / named interaction collections | Consume native MolSysMT `Interactions`, participants, measurements, state and provider recognition | PHMT converts observed molecular relations into pharmacophoric constraints. It does not redetect interactions or optimize molecular geometry. |
| Declared ERalpha/CCD preparation recipes | Public MolSysMT extraction, template assessment/application, aromatic normalization, fixed-state H addition, merge, rotate/translate | Molecular algorithms delegate correctly. Explicit fixture atom maps, state choices and source evidence are case declarations. Calling native `Structures.append` or chemical-history methods is using a provider-owned object contract, not writing a consumer engine. Complete receptor preparation is not claimed. |
| `model()` default -> `ComplexBasedModeler.build()` | Local `utils.chemistry.fix_bond_orders`, RDKit `DetermineBondOrders`, receptor PDB reparse, SMARTS and local molecular geometry | Reachable duplication. Replace by explicitly prepared source plus native observed-interaction construction; do not silently change the legacy scientific method. Template application already exists through uibcdf/molsysmt#298. New interaction-family needs must go to MolSysMT. |
| Exported `StructureBasedModeler.build()` | Local spherical atom selection, RDKit recognition and ring/neighbor geometry | Reachable duplication. Compose public provider selections/geometry/recognition, retaining ideal pharmacophoric projection choices locally. Current native reference/interaction workflows are not a scientific replacement for structure-based projections. Pocket definition is a separate TopoMT concern where applicable, not a new local molecular utility. |
| Exported `VirtualScreening.run()` -> `ConformerGenerator.generate()` | Local H addition, RDKit embedding, UFF/MMFF minimization and RMSD pruning | Reachable general preparation. Existing provider request uibcdf/molsysmt#219 is open. Native `ConformerScreening` consumes prepared structures; native `LigandBasedModeler` also requires preparation and explicit method choice. |
| `VirtualScreening.to_dataframe()` / `to_sdf()` | Local H removal, molecular SMILES/SDF conversion, best-structure export | General molecular conversion belongs to MolSysMT; PHMT owns result selection and `FitValue`. Do not hide H removal in result formatting. Single-record SDF support is present, but collection/property fidelity remains separate work under provider triage uibcdf/molsysmt#215 / #223. |
| `data.ligand_sets.read_sdf()` | RDKit record parsing and conformation assembly grouped only by `_Name` | Molecular library ingestion belongs to MolSysMT. Same names do not establish identical graph or atom correspondence. Reported alongside SDF collection/property needs; do not expand this consumer reader. |
| Importable `utils.preparation` | Local salt stripping, normalization/uncharging, sanitization, stereo removal, SMILES parsing and molecular descriptors | No package runtime callers found. Retire unused implementations or consume explicit provider preparation when the library workflow is adopted. Optional normalization/fragment handling is proposed in uibcdf/molsysmt#366. Do not promote silent loss/failure or stereo erasure as its contract. Descriptor calculation is general; PHMT may select filter thresholds. No descriptor API is proposed without an accepted caller/contract. |
| `utils.alignment` / generic parts of `utils.maths` | Local principal-axis SVD, alignment/embedding and molecular ring geometry | Alignment utilities have no package runtime callers found; ring/angle helpers remain used by legacy modelers. Retire unused molecular tools and consume existing public fit/plane/axis tools where scientifically compatible. Do not substitute algorithms solely because their names match. |
| `io.rdkit` / annotated pharmacophore `io.sdf` | PHMT feature/shape model and virtual-site format | These encode a pharmacophore, not an input molecular system. PHMT owns the feature tags, shapes and round-trip contract. Any reusable low-level molecular/file adapter should still be provider-owned; a direct RDKit import alone does not establish duplicated molecular science. |

The donor-H displacement used to define a pharmacophoric direction, arithmetic
on cached feature centers, and exclusion/query score comparisons do not alter
the molecular system. They implement the PHMT scientific representation and
criteria. This distinction does not authorize a new generic molecular geometry
tool in PHMT. General molecular fits, recognition, plane construction and
coordinate editing stay with MolSysMT.

## Measured provider defect and #31 scope

Nine public `molsysmt.structure.least_rmsd_fit()` calls on native `Structures`
use explicit numeric selections and test degenerate source, degenerate reference
and valid self-fit controls at three origins. At the two translated origins,
the provider accepts exactly two distinct centers as three fit anchors; at zero
it rejects both degenerate controls. All three valid controls succeed. The
six degenerate calls therefore give four wrongful acceptances and two proper
rejections. Source and reference coordinates remain unchanged in all nine calls.

The complete measured outputs, executable reproducer stored as inert text,
fit-source hash and loaded molecular extension hashes are retained in
`devguide/evidence/molecular_ownership_provider_fit_py314.json`. The installed
provider reports `0.22.4+215.g5bd893c85`, while its clean checkout head is
`8ae160fc93ed5bc815bcc24b37c2875ba735623d`; both identities are recorded rather
than assuming the version string identifies the current source.

After fetching references, the provider checkout was 37 commits behind
`origin/main` at `d47b528dabc0a68bf0ce90660b6c3a71701e674c`. The upstream fit
source is identical, and the searched public conformer/standardization
capabilities remain absent. Upstream execution is not claimed. DockingMT is
current but has unrelated untracked validation work, which this task leaves
untouched. No sibling worktree, branch or runtime implementation was changed.

The provider defect is now uibcdf/molsysmt#367. PHMT #31 covers eligibility of
automatically proposed pharmacophoric seeds; its private rank predicate is an
internal criterion of those public proposal tools. General molecular fit
validation is independently owned by MolSysMT. Direct caller-supplied mappings
can reach the provider without automatic proposal filtering, so a reviewed #31
guard must not be described as repairing every molecular fit route. Do not
duplicate a provider validator or import its private helper to mask #367.

## Provider feedback and dependencies

- uibcdf/molsysmt#219: additional actual `VirtualScreening` caller, fixed-state
  preparation separation and retirement link posted; existing proposal reused.
- uibcdf/molsysmt#215: additional multi-record/name-merging and result-property
  requirements posted for provider triage. Its delivered single-record scope
  remains separate from collections; #223 owns lossy export atom correspondence.
- uibcdf/molsysmt#366: new explicit molecular standardization proposal, with
  original-state preservation, fragment/atom mapping and separate chemistry choices.
- uibcdf/molsysmt#367: new public-fit validation defect, independently reproduced.
- uibcdf/molsysmt#323: environmental fixed-state H refinement remains open;
  local H placement is not environmental optimization. It is not implemented here.
- uibcdf/molsysmt#350: rejected aromatic-candidate diagnostics remain open;
  maintain existing PHMT limitations until the provider contract is delivered.
- uibcdf/molsysmt#298: explicit template assignment is delivered and already
  consumed by the prepared native recipes; this is not an unresolved blocker.

DockingMT's inspected contract assigns docking problems, domains/guidance,
constraints, engine negotiation and sampling/scoring/refinement composition to
DockingMT. PHMT query evaluation and rigid feature placement have their own
scientific meaning and do not call Vina/Meeko or implement receptor-ligand energy
sampling. No concrete missing docking-owned capability was identified in this
audit, so no speculative DockingMT API issue is opened. A future docking-guided
integration must request its actual provider contract and link evidence there.

## Why

Continuing local molecular preparation would create incompatible chemistry,
identity, units and failure behavior between suite consumers. The surviving
default also makes it possible to bypass the explicit native preparation
contracts unintentionally. The migration needs public compatibility decisions,
not additional preparation kernels or broad claims of native adoption.

## Bounded historical retention / next implementation steps

This record tracks an architectural limitation, not acceptance of the duplicated
routes. The responsible role is the PharmacophoreMT maintainers; the next review
date is **2026-10-17**, or before any work relies on or expands a legacy molecular
operation. Consumer tracking is #41; provider links and scopes are listed above.
Existing public calls remain available during this review to avoid an unreviewed
API/scientific-method change. Native workflows keep requiring prepared inputs.

1. Decide the explicit transition for `model()` / `ComplexBasedModeler`, with
   prepared-source prerequisites, observed-interaction scope and compatibility
   evidence. Do not make automatic chemical inference the new default.
2. Migrate structure-based provider recognition/geometry while preserving its
   specific projection method; qualify its independent scientific controls.
3. Retire or explicitly transition legacy `VirtualScreening` preparation. Until
   #219 is available, use the existing prepared-input workflow rather than build
   a second conformer generator.
4. Replace molecular library I/O only after a provider collection/property
   contract is available, or retire the unsupported consumer convenience path.
5. Remove unused generic utilities and reconcile imports/docs after the public
   transition decisions. If standardization is needed, consume #366's delivered
   contract; otherwise remove the unused local route.

Removal conditions are independently qualified native consumer replacements or
explicit retirement of the relevant legacy entry points/helpers. Provider fixes
are made in their owners; no local workaround may be expanded under this record.
Expired retention requires renewed review, not automatic continuation.

## What is measured and what is assumed

The nine provider calls and preservation assertions are executed observations.
Call paths, exported defaults, missing runtime callers and upstream tool absence
are source inspection. Provider issue states are separately checked live.
The audit does not execute all legacy paths, compare biological outcomes, qualify
upstream or a released MolSysMT artifact, measure performance, or prove scientific
equivalence of legacy and native methods. Future migration requires those
operation-specific contracts and controls; presence of a similarly named public
tool is insufficient.

## Alternatives and refuted paths

- Extending local preparation to make a pilot pass violates molecular ownership.
- Removing every NumPy/RDKit use would confuse PHMT feature science and adapters
  with molecular-system manipulation.
- Moving pharmacophoric graph search into DockingMT solely because it places
  a ligand would confuse specialized pharmacophore matching with docking protocols.
- Reopening #298 or duplicating #219 would hide delivered work and split provider
  ownership; existing issues/tools are reused.
- Corrected PHMT automatic seed selection does not repair MolSysMT's public
  validation of arbitrary explicit mappings.

## Acceptance criteria

Close #41 only when reachable general molecular operations are provider-mediated
or explicitly retired, unused generic utilities no longer advertise a parallel
molecular toolbox, and public default/migration guidance matches executed contracts.
Retain operation-specific guards for source/state/atom identity, units, failure
semantics and scientific results. Open provider proposals or this completed audit
alone do not satisfy molecular migration acceptance.
