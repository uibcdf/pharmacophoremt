---
summary: Compare original labelled cohorts directly across verified saved screening runs.
issue: uibcdf/pharmacophoremt#147
status: resolved
opened: 2026-11-08
closed: 2026-11-08
verification: reproduced
area: [validation, screening, public-api]
guard: tests/test_saved_run_comparison.py
normative: devguide/saved_run_comparison.md
blocked_by: []
supersedes: []
---

# Paired saved-screening-run analysis

## What and why

Resolved#146 admits a verified saved run without inventing native batch indices.
Existing compare_screening_results still requires batch results with unique
native indices. A user cannot directly compare two real saved runs with their
original absent/repeated native indices. This bounded bridge belongs to PHMT
validation under#108/#103, alongside completed#65/#100/#146 contracts.

## Implementation and acceptance

Public compare_screening_runs uses strict baseline/comparison descriptors with
run_view/input_mapping/score_method and optional unscored/source_metadata. Reuse
summarize_screening_run and one factored existing paired-statistics tail, with
new screening_run_comparison@1 and unchanged old batch output/schema/formulas.
Require matching explicit criteria; compare only scored original-cohort
intersection, preserving original order and zero scores. Full detached per-arm
summaries retain all pending/native-failed/upstream counts and native evidence.
Views remain caller-owned; no molecular operation, reindexing, aggregation,
source/chemical/label authority or biological independence is inferred.

The prospective local plan in the owned paired-run capsule declares guards and
independent exact two-class metric oracles before implementation: six sparse
samples, differing work identities/coverage; per-arm denominators and common
scores[1,0] versus[0,1], AUC/BEDROC1versus0 andEF50%2versus0. Cover self/swap,
single-class/empty/pending, malformed descriptors/mapping/criteria/lifetime,
detachment/original bytes/source attribution/no molecular access and unchanged
batch comparison. Receive real optional attribution, the public recipe, selected
source and one exact owned installed artifact with original guard bodies.

## Scope and current state

Issue and plan precede implementation. Initial fixture setup fails29cases because
the synthetic right-arm native records omit required pose_id; correction is
fixture-only and the failed attempt stays preserved. Then31missing-operation
failures/one positive old-batch refusal precede implementation. All32initial
focused controls pass. The complete selected receiving passes256distinct cases,
including33new guards after adding public keyword-contract coverage, with the
complete supported Pytest Receptor event journal and one intentional existing
optional-attribution warning. Source code comparison proves all old summary/helper
ASTs and the factored paired tail identical, and metric/retrospective files byte
equal. The exact public analytical recipe passes with whole-process RSS261128192
bytes and before/after provider/native files unchanged. After a same-module import
ordering correction for Ruff, final exact-source receiving again passes256cases
and the recipe, with its complete log and260935680byte whole-process RSS. Both
runs remain separate, not512distinct cases. Distribution24/reporting3/archive18,
full Ruff/declared routes/indexes and strict full Sphinx HTML pass; actual four
function anchors and work_items are verified. Exact owned installed receiving is received below.

The [source receipt](../evidence/saved_run_comparison_source_20261108_summary.json)
and hash-bound full archive preserve90owned files, all original failures,
actual final source/provider/native fingerprints, complete event journals and
the declared [plan](../evidence/saved_run_comparison_plan_20261108.json).

Existing full source42436392248/attempt1 is frozen at5c3cd64 and cannot qualify
this later increment. The original broader native/resource route remains failed;
use the explicitly declared eleven-module receiving scope plus new guards,
without native/provider/prefix/budget change. Full source/public provider/
installed supported-platform, biological/human-usability/performance/release
gates remain separate. No new release or dependency is selected.

## Exact owned installed receiving and closure

Implementation1392bad3c8efc479b769aa5c6f1e3d9871bdaee7 owns one authenticated
wheel0.4.0+165.g1392bad,4524546bytes,SHA-256
278461bf01595970e760ee5d2cb577ab3cf331e52f3128408f0d6033587b15d0.
The [installed receipt](../evidence/saved_run_comparison_installed_20261108_summary.json)
passes the same256original bodies,35guarded children and exact public recipe
outside checkout with -I-S-B. SDK verifies152loaded runtime modules; all211wheel
payload/156nongenerated runtime files and854unshipped original fixture files
authenticate. Whole-process RSS390557696bytes retains its parent-command scope.

The first old-plan preparation finds that Sabueso's finder210 no longer exists;
a prematurely launched attempt3 fails before tests because the plan is absent.
Read-only current declarations admit exactly the same namespaces/roots; final
attempt4 passes on the same original wheel. No shared-prefix/provider/native
mutation or rebuild occurs. The first sealing helper's list-versus-count check
is corrected without rerunning tests; its original helper and local disposition
remain preserved. No upstream bug is invented for either harness issue.

[Real installed optional attribution](../evidence/saved_run_comparison_attribution_20261108.json)
retains4items/13uses, full portable references, original source attribution and
the enclosing application session. This supplement is not another independent
guard or molecular calculation. Nine companion Python files remain byte equal
to earlier wheel162; its independent-reader receiving keeps its original artifact
and is not rerun/relabelled here.

The relevant guard tests/test_saved_run_comparison.py protects exact paired
original-index alignment, full failure denominators, independently known metrics,
strict descriptors/lifetime, original bytes/native indices/source attribution
and detached output. Existing batch/core controls and AST/byte comparison protect
unchanged definitions. The bounded public bridge is resolved; the mature0.x goal,
full source9/public-provider/installed-platform23/publication10/release95,
biological and human-usability/performance gates remain open.
