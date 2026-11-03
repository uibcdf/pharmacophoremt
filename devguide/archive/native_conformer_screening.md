---
summary: Screen prepared conformations with native rigid search and explicit molecule-level score resolution.
issue: uibcdf/pharmacophoremt#17
status: resolved
opened: 2026-10-02
closed: 2026-11-03
verification: measured
area: [screening, integration, validation]
guard: tests/test_conformer_screening.py
normative: devguide/conformer_screening_workflow.md
blocked_by: []
supersedes: []
---

# Native prepared-conformer screening


## Source/API acceptance resolved — 2026-11-03

The current implementation satisfies this issue's prepared-frame source/API
contract without runtime or test changes. Clean source
**3ecfe23cbab455226ab48c99248f7c9c127b6d8c** passes **95 controls**, zero
failures/errors/skips: 20 conformer, 13 rigid-search, 26 seeded-scoring, 27 facade,
eight retrospective and one composed-attribution control. The workflow example
and all five current prepared-conformer cookbook blocks execute successfully.
The [new acceptance receipt](../evidence/conformer_acceptance_20261103_summary.json)
retains full models, poses, frame records, actual credits, runners and identities.

Five additional recorded ensembles reuse the existing analytical fixtures:
complete negative, unresolved negative with a failed frame, unit-coverage hit
with a failed frame, all frames failed, and a binary hit at optional coverage .75
with an actually missing state on another frame. The last case resolves binary
score one while retaining the provider failure and incomplete ensemble. No failed
frame becomes a negative. An analytical retrospective record preserves repeated
input identities, excludes the unresolved molecule and retains original scored
indices [0, 1, 3], with three evaluated inputs and one failed input. Atom identity,
coordinates, chemical state and frame-state association fingerprints are unchanged.
Actual Ackredit references/uses are retained for these executions.

Complete source/native/helper/test and distribution-metadata identities are
unchanged in all three phases. The existing ordinary editable PHMT install
identifies runtime 404aa38; measured main 3ecfe23 has identical tracked runtime,
support, tests, tools and workflows. The owned #69 venv and provider/native
installs are reused unchanged; canonical prefix and sibling worktrees are not
modified. Shared dependency conflicts remain MolSysSuite #82. The isolated
cookbook page renders strictly with a stub for its adjacent retrospective link;
this does not qualify full-site navigation/rendering.

The durable guard remains `tests/test_conformer_screening.py`; current seeded
consumer behavior additionally has `tests/test_seeded_scoring.py`. The maintained
[workflow](../conformer_screening_workflow.md) records the accepted boundaries.
Final-head hosted receiving remains #9; full installed/public/platform delivery
remains #23/#10. No full current-suite rerun, clean dependency closure, biological
validation, performance comparison, conformer generation, new molecular routine,
provider minimum or release is inferred. Earlier uncommitted/verification wording
below records October's original state and is superseded by this dated acceptance.

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
