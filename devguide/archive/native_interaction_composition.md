---
summary: Compose named pharmacophore hypotheses and native interaction analyses with explicit participant reuse.
issue: uibcdf/pharmacophoremt#36
status: resolved
opened: 2026-10-04
closed: 2026-11-03
verification: measured
area: [modeling, interactions]
guard: tests/test_interaction_composition.py
normative: devguide/interaction_composition_workflow.md
blocked_by: []
supersedes: []
---

# Public hypothesis and interaction-collection composition

## Source/API acceptance resolved — 2026-11-03

Clean producer **9387852af67a17f59e48d14fc78260ffc4320650** passes 219 coupled source
controls, zero failures/errors/skips, including all 41 composition cases. Nine new
controls preserve eight pre-fix failures and nine post-fix passes: contradictory,
incomplete, repeated, boolean or out-of-range geometry declarations and conflicting
site states are rejected; reordered geometry under nonidentity source maps stays
valid. Cached inputs and intentional molecular references are unchanged. Generic
keep preserves independent evidence without asserting native participant identity.

The [new receipt](../evidence/composition_acceptance_20261103_summary.json) retains
full tests, original reproduction, source/native/input identities, runners, models,
observations, actual credits and before/after regressions. Both existing driver
profiles pass nine evaluations each: seven analyses/23 observations, nine reused
sites versus eleven kept constraints, displacement/donor negatives and independent
steric veto. Scientific projections agree across tracking; actual captures retain
5 items/21 uses off and 13 items/50 uses on. Three cookbook blocks and strict
isolated page rendering pass; the page has an adjacent link-target stub and does
not qualify full-site rendering/navigation.

Full code/native/helper/test/input and distribution-metadata identities remain
equal before/after all three current phases. The correction validates PHMT cached
provenance only: no molecular operation, detector/profile, state interpretation,
geometry definition, provider pin or dependency floor changes. The prior full
1,020-item run belongs to 96f917a and is retained as a baseline, not execution of
this new correction. Current exact-head hosted receiving stays #9; clean installed/
public/Conda/platform qualification stays #23/#10, with shared #82 conflicts.

The durable guard is `tests/test_interaction_composition.py`; the maintained
[workflow](../interaction_composition_workflow.md) specifies the strict native
mapping/state boundary and generic keep distinction. Historical October claims
and original archives below are unchanged. This closes cached-composition source/
API acceptance, not biological or performance qualification. #37 receives this
same correction with complete CCD inputs, separately recorded.

## What

Provide public `compose_pharmacophores()` and `from_interaction_collection()`
for independently computed classical families and cached common-frame models.

## How

Keep component metadata and per-site correspondence detached. Generic composition
keeps constraints by default. Native identity reuse requires declared common
source axes, ligand, frame and state; incompatible constraints raise. The
collection adapter calls the existing public conversion and composition tools.

## Why

Ionic/cation-pi and multiple pi-pi profiles can support the same chemical feature.
Counting each as a new required site inflates weights and can incorrectly fail
one-to-one evaluation. Original evidence must survive without that duplication.

## What is measured and what is assumed

The dispatcher/contract gate passes 16 controls in 7.57 s on Python 3.14.7.
The reproducible driver passes both tracking profiles with nine pose evaluations
each and preserved producer/input identities. Three cookbook blocks execute.
Final full integration and evidence identities are recorded in the maintained
contract. Prepared disconnected inputs are not a chemical ligand, biological
binding complex or performance benchmark.

The corrected full local tree passes 476 tests in 452.91 s on Python 3.14.7,
including all 32 composition controls, with the same eight known warnings.
Ruff, indexes, three offline reporting tests, whitespace checks, strict isolated
cookbook rendering and all twelve original archive hashes pass. The twelfth full
evidence artifact and summary retain both tracking profiles and source identities.

The [owning issue result](https://github.com/uibcdf/pharmacophoremt/issues/36#issuecomment-5977455025)
records executed checks and acceptance limits; the proposal remains active for review.

## Alternatives and refuted paths

Keep generic composition independent of molecular algorithms. Do not flatten
heterogeneous MolSysMT criteria or recreate its native result machinery here.
No radius clustering, geometry averaging, silent weight aggregation or discarded
failed analysis. Legacy `Pharmacophore.merge()` remains outside this slice.

## Scope and exclusions

Common-frame hypotheses and separately computed native observations. No molecular
preparation, automatic alignment, consensus, release or biological acceptance.

## Acceptance criteria

**Consumer migration, 2026-10-06:** Current MolSysMT #346 deliberately removes
the early `between` spelling. The native interaction adapter now calls public
`between_selections` with unchanged ligand/complement/frame selections and retains
scientific detector parameters and evidence. Before migration the publication
selection reports ten curation setup errors and 59 passes; afterward all 164
ionic/aromatic/composition/CCD/curation controls pass in 231.78 s on Python 3.14.7.
Current controlled CI source pins are recorded separately from public distribution
and four-minor acceptance. Original local evidence remains historical and unchanged;
the publication receipt is `devguide/evidence/publication_20261006.json`.

Public-tool composition, both duplicate policies, source/constraint compatibility,
evaluated-empty and failed cases, source preservation, persistence, independent
geometry/veto controls and real optional attribution pass. Document the standalone
tools and executable cookbook; retain reproducible original evidence.

## Functional acceptance in progress — 2026-11-03

Review of main b5564f4 reproduced cached participant reuse despite a contradictory
`source_geometry_atom_indices` declaration: local atom/geometry [6] was accepted
with source geometry [7] under an identity source map. Optional site-level state
declarations were also unchecked against their native component. Eight new
counterexamples fail before the correction; a reordered/nonidentity source-map
control already passes. All nine controls pass after validating declared geometry
maps and site states before reuse. Inputs and intentional molecular references
remain unchanged; generic keep remains independent of native identity assertions.

This is PHMT cached-evidence validation, without molecular queries, normalization,
coordinate calculations, provider changes or new scientific definitions. Next
qualify the complete owning/coupled controls, existing tracking off/on driver and
three cookbook blocks on a committed producer before deciding closure. The recent
1,020-case full source run at 96f917a remains its original baseline, not execution
of this new correction. Exact-head hosted receiving stays #9.
