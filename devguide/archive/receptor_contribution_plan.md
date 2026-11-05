---
summary: Freeze a paired receptor constraint-contribution development protocol and matrix.
issue: uibcdf/pharmacophoremt#89
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: measured
area: [modeling, validation]
guard: tests/test_receptor_contribution_plan.py
normative: devguide/receptor_contribution_protocol.md
blocked_by: []
supersedes: []
---

# Receptor contribution prespecification

## What and why

Following #87/#88, audit12/15 needs a paired development comparison of donors,
rings, their combination and exclusions. Freeze the first deliverable before
generating/evaluating new hypotheses. This issue owns prespecification, not
execution results or biological validation.

## Method and observed eligibility

The original prepared #52 source is unchanged. A frozen source-order rule inspects
all seven PHE regions through public MolSysMT; all are eligible and deterministically
retain 337/367/404. Actual input/source/native/helper/test/metadata identities,
full custody and actual input/operation credit remain in the evidence. No model
or pose is evaluated during eligibility. Failed initial collector/setup attempts
are retained separately from the completed audit.

The protocol/explicit JSON matrix fixes six query variants, five candidate
controls, two unit policies and separate tolerance/budget blocks. The orientation
control refines the issue's initial four-candidate sketch before any comparison
outcome. Planned workload: 60 cells, 342 returned models, 1,710 primary evaluations;
30 zero-budget slots are unevaluated. Recovery plans 108 extra evaluations.
These are analytical expectations, not observed model results.

## Ownership and alternatives

All molecular source access, selection, representation, recognition, vectors,
planes, coordinates and transformations remain public MolSysMT operations.
PHMT owns projection/composition, matching and comparison. No local molecular
helper, direct RDKit use, molecular format parser, pocket detector or scientific
fallback is introduced. Frozen geometric controls precede broader chemistries,
preparation variants, biological evaluation and performance work.

## Acceptance

Keep complete prospective factors/cells, independent positive-fit expectations,
strict-inside oracles, complete/truncated/zero and failed/unevaluated rules,
statistical limits, custody, executable lightweight plan guard and clear next
execution handoff. Close only this first deliverable after applicable checks;
broader scientific comparison and audit12/15 remain open.

## Resolution — 2026-11-05

Eight offline declaration guards pass (also collected with published Pytest
Receptor), protecting fixed input/eligibility, paired factors, analytical
component/radius answers, independent exclusion rules, incomplete/zero semantics,
proper control rotations and exact planned denominators. Actual eligibility uses
public MolSysMT with stable source/native/helper/test/input/metadata identities;
no hypothesis or pose is evaluated. The protocol/matrix is frozen and execution
is tracked separately in [#90](https://github.com/uibcdf/pharmacophoremt/issues/90).
Applicable administrative checks and original full evidence belong to the
prespecification receipt. This closes the declared first deliverable only;
scientific execution and broader audit12/15 remain open.
