# Inspect one saved screening work item

Owners LMMV/dprada; prospective contract 2026-11-08;
[#157](https://github.com/uibcdf/pharmacophoremt/issues/157), milestone2/#108.
The [plan](evidence/work_item_plan_20261108.json) precedes implementation/testing.

## Public operation and output

`ScreeningRunView.work_item(work_key)` inspects one exact opaque work key in the
caller-owned verified read-only snapshot. Source/occurrence keys do not substitute
for work keys. Valid strings retain their literal whitespace/Unicode. Unknown,
empty or invalid keys refuse through the existing structured error boundary.

The detached result format is `pharmacophoremt.screening-work-item@1`:

- `run_id`, `run_format`, `work_sha256`: minimal original run/ordered-work identity;
- `work_item`: original manifest_ordinal/work_key/source_key/occurrence_key;
- `confirmed`: whether an original terminal outcome is published;
- `status`: original native matched/not_matched/failed, or pending;
- `attempts`: retained started/staged/committed counts for this work only;
- `outcome`: complete original confirmed envelope, or null while pending.

Staged and never-started work stay pending; draft payloads are not results.
Started attempts are retained records, not proof of active workers, retry safety
or live scheduler status. Confirmed failure remains unscored. Valid zero outcomes
remain confirmed negatives. No score criterion or native score is recomputed.
Returned outcome fields, quantity records and attribution are copied literally;
the reader interprets no chemical/biological equivalence or scientific validity.

Use existing key admission and confirmed-outcome decoding. Aggregate the existing
meta-only attempt iterator; do not create another persistence/parser or expose
unpublished payloads. Opening still verifies the complete run. Retention depends
on the selected original evidence size; attempt traversal is linear in retained
attempts. This is no index, incremental-memory or large-library performance claim.

## Command composition and compatibility

`python -m pharmacophoremt_results RUN.sqlite3 --work-key WORK_KEY` calls that
public method directly and prints its complete JSON only after successful view
closure. Confirmed detail can contain geometry and portable references; this
explicit selection authorizes neither redistribution nor a scientific rerun.
`--summary`, `--work-items` and outcome exports remain mutually exclusive.
`--score-method`, `--limit` and `--offset` do not apply to detail inspection.
Syntax conflicts refuse before database I/O; method values/storage use the
definition-owned ArgDigest/SMonitor contract. Handled failures exit2 without
success JSON. Legacy files need the unchanged explicit `--allow-legacy` admission.

Existing ranked/scalar, progress, work-page and export responses stay unchanged.
No persisted schema, dependency, launcher or acquisition route changes. Main
scientific bindings can require a new linked run when producer code changes;
independent historical reading remains valid. Molecular collection/preparation
stays MolSysMT-owned. Optional engines, quantity conversion and new attribution
are inapplicable; no such namespace is loaded by this reader.

## Receiving state

The API/core and command are implemented. The final source selection passes
85 cases: 16 new guards and 69 original reader/CLI/page/progress/export cases.
The initial 15-case run retains 12 failures/three passes and failed subtests;
the earlier 84-case pass and final stored-error propagation guard stay separate.
Old API/core definitions except command orchestration remain AST-identical.
Strict full docs, rendered method/recipe links and local governance pass. The
[source receipt](evidence/work_item_source_20261108.json) preserves actual limits,
original failures and scope. Exact owned installed receiving remains pending.
Original failures and each producer/artifact identity remain separate. Full source exact-head, complete public
dependency/installed-platform, human usability and release gates remain open.
