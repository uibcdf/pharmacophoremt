---
summary: Compose named pharmacophore hypotheses and native interaction analyses with explicit participant reuse.
issue: uibcdf/pharmacophoremt#36
status: active
opened: 2026-10-04
closed:
verification: measured
area: [modeling, interactions]
guard: tests/test_interaction_composition.py
normative: devguide/interaction_composition_workflow.md
blocked_by: []
supersedes: []
---

# Public hypothesis and interaction-collection composition

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
