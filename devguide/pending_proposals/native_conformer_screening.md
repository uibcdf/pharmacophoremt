---
summary: Screen prepared conformations with native rigid search and explicit molecule-level score resolution.
issue: uibcdf/pharmacophoremt#17
status: active
opened: 2026-10-02
closed:
verification: measured
area: [screening, integration, validation]
guard: tests/test_conformer_screening.py
normative:
blocked_by: []
supersedes: []
---

# Native prepared-conformer screening

## What and how

`screening.ConformerScreening` composes the existing `RigidPoseSearch` over
MolSysMT-provided source frames. It preserves per-frame evidence, requested and
resolved chemical states, best-pose coordinates and stable molecule/frame IDs.
All requested frames are attempted. Exact ties retain requested order, and
hits take priority over negatives before comparing weighted coverage.

## Why and scope

This enables the next traditional workflow without introducing local molecular
preparation, torsional search or chemistry. MolSysMT owns coordinates, frame/state
resolution and molecular fitting. The current rigid method requires at least
three essential non-collinear sites and does not exhaust continuous pose space.
Conformer generation, state enumeration, consensus and accelerated execution
remain separate work. Feature + Shape is unchanged.

## Failure semantics

Default failures raise. Explicit recording retains each failed frame. Without a
valid unit-fit hit proving maximal coverage, any failed frame leaves the molecule
score unresolved: `status='failed'`, `fit_value=None`, with `best_observed` retained
for inspection. Retrospective metrics exclude unresolved molecules. A proven
maximum can coexist with recorded failures; ensemble completeness remains false.

## Acceptance and evidence

The guard covers real-provider rigid recovery, complete negatives, tie/frame
order, physical units, preserved inputs, state-dependent chemistry, missing
state associations, bounded-search failures, partial/all-failed ensembles,
portable coordinates and retrospective generator/repeated-input accounting.
See [the workflow contract](../conformer_screening_workflow.md).
The implementation is local and uncommitted. On 2026-10-02 the full local suite
passed 118 tests with the existing published provider source pins; the documented
example, Ruff, whitespace checks, generated indexes and three offline reporting
tests passed. The guard includes 20 conformer controls, including state-dependent
selection through the shared extraction, evaluation and alignment boundary.
User-facing instructions are also available in the
[cookbook recipe](../../docs/content/cookbook/prepared_conformers.md), alongside
reference-ligand, observed-interaction and retrospective-validation recipes.
On 2026-10-02 all six Python blocks across those four recipes passed with the
same provider pins. An isolated Sphinx/MyST-NB cookbook build using the project's
PyData theme passed with warnings treated as errors; this does not claim a
complete-site or hosted documentation build. Main navigation and user-guide
links include the cookbook.
No clean-wheel, hosted-matrix or biological-pilot success is claimed.
