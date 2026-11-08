---
summary: Analyze labelled cohorts directly from verified saved screening work.
issue: uibcdf/pharmacophoremt#146
status: active
opened: 2026-11-08
closed:
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
