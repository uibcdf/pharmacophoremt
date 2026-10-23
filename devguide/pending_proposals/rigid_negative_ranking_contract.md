---
summary: Define a frame-independent molecular ranking contract for completed rigid negatives.
issue: uibcdf/pharmacophoremt#63
status: open
opened: 2026-10-23
closed:
verification: reproduced
area: [screening, validation, mvp]
guard:
normative:
blocked_by: []
supersedes: []
---

# Partial negative scores depend on the supplied coordinate frame

## What and why

The first activity pilot #62 motivated an independent review of partial-score
comparability. A separate analytical source control confirms that translating
one propane system through public MolSysMT changes a completed negative's
`RigidPoseSearch.fit_value` from 1/3 to 0. Both outcomes remain `not_matched`,
with complete declared enumeration and no fitted proposal. That coverage cannot
be assumed to be a frame-independent molecular ranking quantity.

## Executed evidence

The [original probe](../evidence/rigid_negative_frame_probe_20261023.json)
identifies actual checkout source `598d3744dc5348b497747d68f3a22a4c5d14ae53`,
provider source `48aba006fbe17336dfb5f564823711c2923f7e0b`, source/native hashes,
versions and original outputs. Stale editable PHMT distribution metadata is
recorded explicitly, not used as executed-source identity. This control does
not qualify the new provider generally and does not replay/correct the frozen
public installed PHMT 0.4.0 / MolSysMT 0.23.0 assay result.

Use the complete executable reproduction in the owning issue. The existing
`phmt_test_support.absence_inputs.system` constructs propane through public
MolSysMT conversions and coordinate storage; public `structure.translate` moves
it by [2, 1, 3] nm. Recognition returns one hydrophobic feature at atom 1. A
three-site essential non-collinear query at [0,0,0], [.15,0,0], [0,.15,0] nm,
radius .02 nm, has no essential-triplet placement. Each enumeration records one
raw trial, one pruned trial, zero proposals and zero fits. The original placement
retains 1/3 coverage; its translated copy retains zero. Initial ethane control
has no recognized hydrophobic feature and scores zero in both frames.

## Mechanism and scope

The native method initializes its best result from identity-pose evaluation and
then tests compatible essential-triplet proposals. A completed no-proposal
negative retains the supplied pose's coverage. Existing search documentation
bounds seed/continuous completeness; the observed hit decision does not violate
that bound. The unresolved issue is how this score should be used in retrospective
and conformer ranking across unrelated input frames.

PharmacophoreMT owns feature matching, ranking and scientific interpretation.
All molecular transforms and fits remain public MolSysMT operations. Do not add
an exhaustive unbounded fallback, silently reinterpret `fit_value`, or implement
molecular geometry here. Preserve #62's original outputs, weak metrics and
missing outcomes; do not tune a new method against its exposed held-out set.

## Acceptance and next step

Choose/document a defensible molecular score or explicitly restrict use of the
current partial coverage. Distinguish checked-pose coverage from ranking evidence.
Add independent translated/rotated completed-negative controls, explicit budgets,
ties/failures and downstream retrospective/conformer tests. Reuse owning public
tools and declare a new scientific run for changed scoring semantics. No runtime
fix or new scoring contract is delivered by this report.
