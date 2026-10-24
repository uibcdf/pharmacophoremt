---
summary: Define a frame-independent molecular ranking contract for completed rigid negatives.
issue: uibcdf/pharmacophoremt#63
status: resolved
opened: 2026-10-23
closed: 2026-10-24
verification: measured
area: [screening, validation, mvp]
guard: tests/test_seeded_scoring.py::test_negative_score_is_invariant_and_pose_coverage_remains_distinct
normative: devguide/seeded_ranking_workflow.md
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

## Source implementation under qualification — 2026-10-24

The [seed-only contract](../seeded_ranking_workflow.md) is now implemented as an
explicit `search_method='seeded_hit'` on rigid/conformer tools. It excludes the
arbitrary supplied placement and uses a binary molecular criterion: fitted hit
one, completed negative zero, failed/unresolved input unscored. Raw `fit_value`
remains checked-pose evidence; no fitted pose means no invented coverage or
coordinates. No graded partial optimum is claimed. A first hit proves maximum
binary score, including optional coverage below one; an unproven exhausted
search remains failed. Ensemble ties preserve requested frame order.

Public `get_screening_score` is a reusable read-only scoring operation. The
retrospective/facade consumers share it; they refuse implicit legacy
rigid/conformer coverage ranking and allow deliberate compatibility through
`score_method='checked_pose_coverage'`. Scalar exports name both criterion and
score. Direct compatibility search defaults and all molecular operations remain
unchanged; MolSysMT still owns fitting, reading, states and transformations.

Fourteen initial source controls and 97 public-provider focused tests pass.
The complete source suite (949 collected tests), additional criterion guards
and replay are under qualification in `/tmp/phmt-seeded-ranking-20261024`.
Public MolSysMT 0.23.0 is isolated from the newer shared development provider.
Historical public-version Pandas warnings remain visible and are not repaired
or suppressed in this component. No public package or new release is produced.

The [replay declaration](../../tests/data/esr1_activity_pilot/seeded_replay_declaration.json)
fixes the original #62 manifest, query and report byte identities before new
scores. The driver reuses the existing public-provider preparation recipe and
refuses changed inputs/query even with rehashed declaration fields. This is
development replay of an exposed dataset, not a fresh independent holdout or
an optimized biological comparison. The original frozen evidence is preserved.

## Measured closeout — 2026-10-24

Source producer `c80325c5c3851691bcc0a993d1e73eaf294654f6` implements the
bounded criterion above. The complete local suite passes **949 tests** on
Linux/Python 3.14.9 with public MolSysMT 0.23.0, PyUnitWizard 0.29.0 and the
declared scientific test extras. All 223 recorded runtime/test/support Python
hashes remain unchanged through the source commit and suite. Historical public
provider and explicit fault-injection warnings are retained. This is source
qualification, not receiving the public 0.4.0 implementation or a new artifact.

The [replay summary](../evidence/esr1_seeded_hit_replay_20261024_summary.json)
qualifies the original new full result, preparation journal, log and source
qualification receipt. The query bytes are identical to #62's original file;
all 32 input identities/order and the six preparation failures are preserved.
Twenty-five inputs are evaluated (6 active / 19 inactive); six remain unscored
(1 / 5). The same sole active CID 24964624 hits. Binary AUC is 0.5833333333,
BEDROC(alpha=20) 0.6496274186 and tie-aware EF at 10% 1.9675925926. Twenty-four
scores tie at zero; 23 valid negatives have no fitted pose. These are the new
criterion's observations, not a demonstrated biological improvement or fresh
independent validation. Original #62 output bytes and hashes are unchanged.

All five updated prepared-conformer cookbook blocks execute with the qualified
providers. Administrative/archive controls protect both experiment identities,
query/cohort substitution rejection, failure denominators and independent
pairwise AUC/tie-aware EF arithmetic. The source qualification receipt retains
the complete test log, environment, native hashes and the editable metadata caveat:
pre-commit distribution metadata is not executed-source identity. Actual clean
producer and runtime origins/hashes are authoritative.

The accepted scope is explicit binary molecular ranking and explicit restriction
of legacy partial coverage. A graded frame-independent partial-match optimum is
not implemented or implied. No molecular backend, provider source, runtime
dependency requirement or public package is changed. Portable input retention
and stronger biological validation remain #62; final hosted CI receiving remains
separately recorded under #9 and owning run identities.
