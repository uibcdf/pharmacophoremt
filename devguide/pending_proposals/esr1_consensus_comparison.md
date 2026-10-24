---
summary: Compare training-only rigid consensus against a frozen reference on new assay CIDs.
issue: uibcdf/pharmacophoremt#64
status: partial
opened: 2026-10-24
closed:
verification: measured
area: [validation, modeling, mvp]
guard: devtools/tests/test_esr1_consensus_training.py::TestEsr1ConsensusTraining::test_archived_readiness_freezes_selected_query_and_keeps_evaluation_unopened
normative: devguide/esr1_consensus_comparison.md
blocked_by: []
supersedes: []
---

# Training-only consensus versus frozen reference

## What and why

Continue the scientific MVP after the bounded #62 pilot and #63 scoring contract.
The observed pilot cannot become a fresh holdout after criterion development.
Declare a separate comparison using three new training actives and 64 previously
unscreened evaluation CIDs from the original primary assay source.

## Delivered pre-score slice — 2026-10-24

The [protocol](../esr1_consensus_comparison.md),
[declaration](../../tests/data/esr1_consensus_comparison/declaration.json) and
[standalone declaration driver](../../phmt_test_support/esr1_consensus_declaration.py)
freeze all IDs and methods before any new structure acquisition or molecular
calculation. They use unchanged archived PubChem AID 743075 v2 responses and
exclude the entire Bath source CID population plus all conflicting assay CIDs.
Three active CIDs train; 16 other actives and 48 inactives evaluate. Lowest-SID
representatives and hash ordering are independent of source row order.

Baseline is the exact original #62 query with explicit seed-only binary ranking.
Native rigid consensus uses only the three training inputs, a fixed pivot,
association cliques, at least two jointly supporting ligands and three sites,
and declared finite budgets. One model is selected using training-only site and
support counts with deterministic ties. Every training prerequisite and a native
training-hit readiness check must pass before evaluation opens. No fallback,
replacement, relaxed bounds or tuning on evaluation outcomes is permitted.

Two offline guards pass: original-source reconstruction of all 67 frozen IDs,
counts, source/query identities and no-clobber CLI; and synthetic conflicting/
inconclusive labels, row-order/lowest-SID selection and insufficient-input failure.
This is executed declaration verification, not measured molecular science.
The complete administrative/documentation selection passes 40 tests and 24
subtests, including strict Sphinx; three reporting tests, whole-tree Ruff and
generated indexes pass. Declaration SHA-256:
`a1a476e7e94fd3480ee3845fbc5cca138221c4052eb7165a254499fd526ff647`.

## Ownership and limitations

MolSysMT owns all molecular I/O, preparation, states, identity/coordinate controls
and fits. PHMT owns pharmacophore hypotheses, method/model choice and study
interpretation. No runtime molecular routine or optional engine is introduced.
The new source script is unshipped case orchestration; existing archive reading,
source retention and scientific APIs are reused, not replaced.

Source/issue inspection found no identified reusable molecular identity/scaffold
overlap tool. The concrete proposal is
[MolSysMT #447](https://github.com/uibcdf/molsysmt/issues/447), linked to this
consumer. The study does not block on that proposal, but only claims external-CID
separation, not chemical-series or independent-assay validation. Existing
conformer/stereo/environmental-H work stays with its provider issues.

## Remaining acceptance and next action

The executable training driver is `phmt_test_support/esr1_consensus_training.py`.
It reuses the original case's HTTP/identity/serialization and existing MolSysMT
preservation checks; the latter are moved without changing their operations
(verified by AST comparison after explicit feature injection). Two additional
offline guards restrict requests to the three training CIDs, preserve HTTP
failures/refuse substitutions and protect the fixed training-only model order.
It contains no evaluation acquisition/scoring mode. This establishes executable
orchestration, not a scientific result before its opt-in run.

Acquire and retain only the three training structures, qualify MolSysMT
preparation and execute native consensus in an owned public-provider environment.
Retain all failures and alternatives; commit the selected valid query and full
training evidence before any evaluation structure/score acquisition. If training
cannot produce a usable query, record that outcome and keep evaluation unopened.

After valid frozen queries, execute paired screening with all failures, per-arm
and common-subset denominators, independent metric/accounting guards, exact
runtime/source provenance, actual attribution and portable original outputs.
No new result is claimed by the declaration. Keep this issue partial for those
scientific execution stages; addon and release infrastructure remain deferred.

## Original training attempt — 2026-10-24

Clean producer `5242ca63eb239aaecb95ae782304dbeca7b53135` executed the training
stage against the unchanged declaration. PubChem returned SDFs for CIDs 31477
and 6293, and HTTP 404 `PUGREST.NotFound` for CID 24633. Both available systems
prepare successfully under public MolSysMT 0.23.0, passing every original-byte,
state, atom-identity, stereo and coordinate preservation check. The third input
is unavailable because acquisition failed; this is not a MolSysMT rejection.

The predeclared all-three prerequisite stops this attempt at preparation.
No consensus is attempted, no new query/readiness score is produced, and no
structure or score from the 64 reserved evaluation CIDs is acquired/computed.
Do not infer inactivity or unsuccessful consensus from absent input data.
No input or method is replaced, relaxed or tuned.

The [summary](../evidence/esr1_consensus_training_20261024_summary.json) qualifies
the full original run, execution/acquisition logs, native environment creation,
qualification and cleanup receipts. The [raw training inputs and notice](../../tests/data/esr1_consensus_comparison/training_20261024/NOTICE.md)
retain both SDFs and the original 82-byte error. The
[case](../../docs/content/validation/esr1_consensus_comparison.md) reports the
measured preparation counts and honest zero evaluation denominator. Actual
source/runtime hashes remain stable, with all 325 provisioned Conda records;
the editable PHMT version is `0.4.0+13.g5242ca6`, not a new public package.
The actual attribution contains 12 items / 14 uses for reached branches only.

All 51 selected rigid-consensus/scoring controls pass; 232 historical public
MolSysMT Pandas warnings remain in the original log. The exposed original
reference additionally reproduces archived counts/features/states/RMSD through
the shared preparation orchestration. This is not a new full hosted matrix or
a scientific timing benchmark. The owned environment is retired after capture;
no global cache cleanup or shared-environment repair is performed.
Closeout passes 43 administrative/documentation tests and 24 subtests, including
the archived-stop guard and strict Sphinx, plus three reporting tests, whole-tree
Ruff and index/whitespace checks. Those administrative checks do not rerun the
scientific workload or qualify a new full hosted matrix.

Retirement reports native success and removes the owned prefix, but its OpenCL
unlink hook attempts an active shared-prefix path. That target is absent and
the deletion fails. Original mixed text/JSON output is retained; root cause
and shared-tooling follow-up belong to
[MolSysSuite #139](https://github.com/uibcdf/molsyssuite/issues/139), not PHMT
molecular code or this availability result.

This original attempt is terminal under its declaration. The broader comparison
issue remains partial because no discrimination comparison exists. **Next:**
declare a distinct training-readiness policy/attempt before acquiring any new
training candidate or using provider-owned conformation capabilities; preserve
this stop and keep evaluation unopened. It must not silently replace CID 24633
or rerun this declaration against refreshed source responses as if unchanged.

## Second declaration — 2026-10-24

A separate [bounded-readiness declaration](../../tests/data/esr1_consensus_comparison/readiness_declaration.json)
freezes 12 training candidates before any new acquisition: original three plus
the next nine eligible actives outside the reserved evaluation cohort. All
original evaluation records, scientific parameters, model choice and comparison
criteria stay identical. Original responses are reused exactly, including the
404; only nine new URLs may be requested.

Every candidate's MolSysMT preparation is retained. The first three successfully
prepared candidates are chosen in fixed order without feature-count/geometry/
score filtering. No alternate trio/pivot/model or expanded pool follows a failed
consensus/readiness result. This is an explicit new sampling policy and run,
not silent replacement in the original stopped attempt. It does not open or
condition the evaluation set on availability.

New offline guards reconstruct the bounded pool and unchanged methods/evaluation,
exercise original-response reuse and exactly nine new requests, and ensure
first-success selection cannot rank candidates by feature count. The original
declaration/archive guards remain active. No new molecular routine or backend
is added; existing public APIs and case orchestration are reused.

## Second training attempt ready — 2026-10-24

Clean producer `25a49f5322a06c1deeff95b396cf194fc5d8f9b6` executes the second
declaration without changing its scientific parameters or touching evaluation.
There are eight SDFs and four preserved 404 responses among the 12 candidates;
all eight available systems prepare and pass the original preservation checks.
The first three eligible CIDs are 31477, 6293 and 9818306, with pivot 31477.

Native `from_rigid_ligands` completes 146 fits and two layouts, retaining three
three-site hypotheses with joint support two. The declared identifier tie-break
selects model 0, `layout_00000 / hypothesis_00000`, supported by 31477/9818306.
It contains two acceptors and one aromatic site, radius 0.15 nm, essential with
weight one. Training-only seed-hit scores are 1, 0, 1 in selected input order.
CID 6293 is unplaced to this pivot within the finite proposal family and retains
its original inventory/support denominator; its zero score is not inactivity.
No other trio/pivot/model is tried after those scores.

The outcome is `ready`, `training_complete`, `evaluation_opened=False`.
The [new summary](../evidence/esr1_consensus_readiness_training_20261024_summary.json)
qualifies original full output, selected query, logs, environment creation and
qualification. Query raw SHA-256 is
`f80a09a68e21a8826a399467bb449082765e10328c8480717811049aa1d93a6d`;
full output raw SHA-256 is
`608b0f41f7ee181785cccbfcde65bf758e7dd056b0b179815d4991028144d8f6`.
All original candidate responses and acquisition identities are portable in
`tests/data/esr1_consensus_comparison/readiness_training_20261024/` with a scoped
notice. Attempt 1 remains unchanged. Actual attribution retains 26 items /
86 uses from executed preparation/consensus/training branches only.

Linux/Python 3.14.9 uses the exact 325 public provider records, MolSysMT 0.23.0,
PyUnitWizard 0.29.0 and editable PHMT `0.4.0+17.g25a49f5`; actual source/native
hashes and producer audit remain stable. All 51 selected scientific controls
pass, with 232 historical public MolSysMT warnings retained. This is not a new
full hosted/installed matrix, public package or timing benchmark.

**Remaining:** commit the frozen query/full training evidence, then execute the
unchanged paired 64-input evaluation with all failures and per-arm/common-subset
denominators. No discrimination metric or predictive qualification exists yet.
The owned environment stays available for that pending scientific phase; no
retirement hooks or global/shared-cache cleanup run here. MolSysSuite #139 stays
separate. #64 remains partial for the held-out comparison.

Closeout passes 46 administrative/documentation tests plus 24 subtests, including
strict Sphinx and the new archive/query-selection guard, plus three reporting
tests, whole-tree Ruff, generated-index and whitespace checks. The original
stop/declaration guards remain active alongside the new measured record.
