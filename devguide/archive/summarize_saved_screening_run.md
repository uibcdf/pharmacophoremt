---
summary: Analyze labelled cohorts directly from verified saved screening work.
issue: uibcdf/pharmacophoremt#146
status: resolved
opened: 2026-11-08
closed: 2026-11-08
verification: reproduced
area: [validation, screening, results]
guard: tests/test_saved_run_analysis.py
normative: devguide/saved_run_analysis.md
blocked_by: []
supersedes: []
---

# Saved screening-run cohort analysis

The public prepared iterator calls single-input `evaluate`, so saved native
records need not contain batch `input_index`. All three original public source
run confirmations lack that field. Existing batch summaries correctly require
unique native indices; they cannot directly consume these saved outcomes.
The read-only view also lacks public iteration over declared pending identities.
Existing#100/#6 saved-result argument admission is already received, not missing.

Implement the [declared contract](../saved_run_analysis.md) under#108/#103:
public ordered `ScreeningRunView.work_items()` and
`pharmacophoremt.validation.summarize_screening_run`. Preserve original native
fields and all work/source/occurrence/ordinal identities; explicit complete
mapping and binary labels own cohort correspondence. Pending work, native
failure, upstream unavailability and zero scores remain separate. Reuse the
existing scientific accounting/metric core without changing its definitions.

Acceptance requires independent source controls, the public recipe and the same
exact owned installed artifact outside checkout. Full#9/#23 and biological,
library-provider and mature0.x qualification remain separate. Companion/main code
changes retain fresh-linked-run compatibility; no saved record is rewritten.
Owners LMMV/dprada.

## Source receiving, 2026-11-08

The [receipt](../evidence/saved_run_analysis_source_20261108_summary.json) receives
268distinct cases, including41new guards, the exact analytical public recipe
and full strict/source Sphinx rendering with real API anchors. Original native
fields, work identities, input bytes and existing metric/accounting definitions
remain guarded. New metadata admission's original own prototype failure is
retained, alongside32initial missing-capability failures/one positive control.

The original broader12module native selection remains failed. Its unrelated
OpenMM adapter mapping/resource failure is masked by older MolSysMT as an invalid
coordinate input, then pytest formatting exhausts allocation headroom. The
owning contract preserves exact diagnosis, resource disposition and existing
MolSysMT#601 feedback. Accepted11module223case receiving is explicit, not a
substitute for full exact-head hosted#9 or fresh provider#23 evidence. No budget
increase or provider/prefix/native modification occurs. Exact owned installed
receiving remains required before closure.

## Resolution received, 2026-11-08

The [installed receipt](../evidence/saved_run_analysis_installed_20261108_summary.json)
receives one exact wheel0.4.0+162.gcc26d45 from producer
cc26d45909728c0bf0b92fc690287bef6a538c48:4523599bytes,SHA-256
`bbce52ee0b03ccc86fee901e254b1f60753575a25109edce1c6a3f7a9b5e0f6e`.
All211payload/156nongenerated runtime files authenticate. Outside-checkout
`-I -S -B` receiving passes the same223original bodies,35guarded children and
exact public recipe; the qualified shared SDK verifies152loaded runtime modules.
Existing source-provider/native/prefix state remains unchanged.

The same artifact separately passes75overlapping independent-reader bodies,
52guarded children and16documented commands over four unchanged original saved
databases, using actual published support payloads with no scientific/main
import. Contexts/child executions are not summed as independent scientific cases.
The [real attribution supplement](../evidence/saved_run_analysis_attribution_20261108.json)
retains4items/12uses, full portable records and the enclosing application's
session, while preserving original bytes/source attribution without recredit.

`tests/test_saved_run_analysis.py` protects full sparse/reordered mapping,
original envelopes/absent or repeated native IDs, pending/native/upstream/zero
accounting, metric oracles, score/criterion/label conflicts, detach/lifetime and
actual attribution. `tests/test_public_run_work_items.py` independently guards
manifest ordering, pending/legacy/empty evidence, streaming/connection/thread
refusal and the no-science fresh reader. Existing batch/scoring/metric tests and
the unchanged-definition proof protect shared-core extraction.

This resolves the bounded analysis bridge. The original broader resource/native
failure remains recorded; full exact-head source#9, full installed/public/platform
#23 and publication#10/#95 remain separate. No new molecular provider tool,
biological/predictive/performance or release claim is made. The mature0.x goal
is active, and code-bound prepared runs still require explicit fresh linked runs.
