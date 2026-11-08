---
summary: Compare original labelled cohorts directly across verified saved screening runs.
issue: uibcdf/pharmacophoremt#147
status: active
opened: 2026-11-08
closed:
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
function anchors and work_items are verified. Exact owned installed receiving
remains pending.

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
