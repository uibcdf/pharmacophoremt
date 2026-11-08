---
summary: Stream complete historical ESR1 CSVs while preserving frozen cohort and exclusion semantics.
issue: uibcdf/pharmacophoremt#152
status: resolved
opened: 2026-11-08
closed: 2026-11-08
severity: medium
verification: measured
area: [validation, resources]
guard: devtools/tests/test_esr1_activity_pilot.py::TestEsr1ActivityPilot::test_original_inputs_restore_offline_with_source_labels_and_failures
normative:
blocked_by: []
supersedes: []
---

# Historical metadata materializes wide CSV tables

Under the existing local512MiB DATA limit, the original-input restoration guard
and two historical-exclusion guards raise MemoryError in complete CSV reads.
Full150case administrative receiving retains those failures, separately from
the route declarations in[#151](feature_reuse_route_inventory.md). The host
remains responsive; no budget is increased and no native calculation is retried.

`historical_exclusions()` retains full wide Bath row dictionaries merely to
derive counts/CIDs. `frozen_cohort()` retains full rows when only first SID per
CID is needed, and its acquisition/restoration callers first materialize the
complete table. Stream the same entire CSVs through standard readers and retain
only required case metadata. Preserve hashes, every row, deterministic ordering,
first occurrence, ambiguous CIDs, complete exclusions, unresolved SID positions
and all prior failures. No new source, activity, structure, score or chemistry.

Acceptance requires exact archived cohort/exclusion equality and the original
failing controls under the unchanged512MiB limit, plus durable one-pass/first-SID/
ambiguity guards. This is separate from the preserved DATA/OpenMM mapping failure,
biological validation and any molecular-performance claim.

## Received correction

Both complete CSVs are streamed. Cohort selection retains only the first SID
per outcome/CID, while preserving ambiguity removal and deterministic ordering.
The acquisition metadata path also retains complete population/outcome counts
and the original ambiguity projections without retaining wide rows. The enhanced
original restoration guard verifies those complete archived values as well as
the32original selected SID/CID/label/role records. Separate lifetime/iterator
guards prove irrelevant row payloads are released and a reused mapping preserves
first occurrence. No source, label, threshold or query is changed.

All three original memory-failing controls plus two new guards pass under the
same512MiB DATA limit; whole-command child peak RSS is122654720bytes. The final
154case administrative receiving also passes, with whole-command peak242102272
bytes. These are execution-resource observations, not a molecular speed claim.
The [receipt](../evidence/feature_reuse_native_preparation_20261108.json) retains
the original150case failure and an intermediate F821 in unused acquisition
report fields; full population/ambiguity assertions now guard that correction.
SQLite finalization warnings remain separately owned by#153.
