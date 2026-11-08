# Immutable saved-progress reuse

Prospective declaration2026-11-08; owners LMMV/dprada;
[#145](https://github.com/uibcdf/pharmacophoremt/issues/145).

## Existing operation and ownership

`ScreeningRunView.open()` fully verifies all saved work, attempts and outcomes
and owns one read-only SQLite transaction until closed. Only views admitted by
that factory may reuse their criterion-independent `progress()` counts after
the first successful scan. Each return must detach nested dictionaries and
preserve connection lifetime and SQLite thread restrictions. Failed scans must
remain retryable. `ScreeningRunStore.progress()` must observe begin/stage/publish
changes. Criteria-specific summaries, ranking, exports, explicit legacy admission,
scores/statuses and database bytes/schema keep their existing contracts.

Reuse the existing PHMT-owned storage scan; use standard-library copying and
SQLite operations, with no persistent cache or new dependency. Existing
ArgDigest argument admission and SMonitor PHMT-E201 diagnostics remain in use;
no new public arguments, optional engine (DepDigest), physical quantities
(PyUnitWizard) or scientific attribution (Ackredit) arise at this boundary.
MolSysMT owns molecular collections; this change owns only saved-result counts.

The public saved view is a snapshot, not a live writer monitor. Opening still
verifies every record, including unpublished/failed/nonranked work. Its first
progress call still scans confirmed payloads. Subsequent calls may reuse only
small count metadata, with no result payload retention. Closing releases it.
Changing companion code changes conservative prepared scientific-run bindings;
use a new linked run rather than silently resuming a differently bound plan.

## Guards and prospective measurement

Before/after tests cover exact partial/empty/complete/legacy counters, nested
mutation isolation, absence of repeated payload reads, closed/native-closed/
wrong-thread refusal after priming, retry after first-scan failure, fresh writer
updates and independent snapshots. Existing full-admission, rank/export and byte
guards remain selected. No timing assertion is a CI guard.

Use the exact immutable#144100/1000databases and recovered10000database.
Frozen baseline is `f5eda452094d22a57bbb4b12e4a5597f8a613180`.
Separate fresh guarded interpreters load all nine reader source files from the
selected baseline/changed overlay and identical existing support providers.
For each size run three paired repetitions, alternating arm order. A new view
per arm/pair measures first verified open, first progress/cache build, and five
subsequent progress calls. Retain every wall/process-CPU sample and whole-process
peak RSS. Validate detached outputs, complete ranks/exports and original file
identities outside timed regions. Report initialization/build separately;
do not pool the original75baseline samples into this experiment.

Execute serially onCPU19/thread1/nice19/idleI/O with512MiB per-process AS,
180s per child, entry available memory>2GiB and memory pressureavg10<1. Defer
under pressure, preserve failures and do not increase budgets. No owned cgroup
can enforce aggregate memory/swap/tasks/quota. This is a synthetic saved-format
experiment: no molecular throughput, faster one-shot CLI/open, live-writer
performance or general index claim. Source and exact owned-wheel receiving
precede closure; full source/platform/public gates remain#9/#23.

## Current state

The implementation keeps a private detached summary only after a successful
factory-opened read-only scan. Cache hits execute a trivial SQLite statement to
preserve native closed-connection/thread refusal. Writer-created views retain
fresh scans; closing clears saved counts. Standard-library deep copies preserve
key order and isolate every nested return.

The original runtime fails five repeated-read controls and passes five positive
controls. The changed runtime passes all10; the original failure log remains
in `build/phmt-progress-reuse-20261108-a8u6u562`. The
[prospective plan](evidence/saved_progress_reuse_plan_20261108.json) retains exact
input identities and declaration. All130selected reader/store/profile controls
pass. Native JUnit retains220reported test events and130distinct testcase nodes;
the latter defines distinct case counting. An initial receipt assertion assumed
these counts were interchangeable; the original assertion/failure is retained.

## Paired source observations, 2026-11-08

All nine pairs/18fresh arms pass exact counts, complete ranked outcomes, full
JSONL/CSV and same-byte input controls. All nine reader files are authenticated
in each arm; eight importable modules and the executable CLI module's spec
resolve to the selected overlay. Identical ArgDigest/SMonitor source snapshots
are retained for all18arms and checked again afterward. A separate fresh probe
executes the exact measured guard and refuses all seven scientific/main imports.

Each cell below reports the median of three opens/first calls and15subsequent
calls. The receipt retains all wall/process-CPU samples, ranges and per-process
RSS; the original#14475samples remain separate.

| Declared/confirmed work | Arm | Verified open ms | First progress ms | Subsequent progress ms |
| --- | --- | ---: | ---: | ---: |
|100/70|Frozen baseline|25.258435|5.273888|5.129725|
|100/70|Snapshot reuse|24.366049|5.202569|0.097941|
|1000/700|Frozen baseline|133.231348|49.532225|49.882698|
|1000/700|Snapshot reuse|132.926075|49.572161|0.077524|
|10000/7000|Frozen baseline|1185.410950|484.376003|497.892380|
|10000/7000|Snapshot reuse|1169.596062|474.282420|0.103223|

This qualifies the repeated same-snapshot progress operation on these synthetic
records in the measured Linux/Python3.14 context. Opening and first progress
still pay their full verification/scan cost; their small differences are not
claimed as improvements. Whole-process peak RSS includes complete rank/export
controls and stays below60million bytes in every arm; it does not measure the
incremental cache footprint. No single-use CLI, writer or molecular-throughput
claim follows. These source observations retain their original overlay identity;
the subsequent installed receiving below keeps its exact producer/artifact.

The [source receipt](evidence/saved_progress_reuse_source_20261108_summary.json)
authenticates the changed source overlay and119owned evidence files, all175
distinct selected cases (130reader/store/profile,24distribution,3reporting,
18archive), complete paired observations and original administrative failures.
Full Ruff, declared dependency routes and generated indexes pass. The source
parent remains the frozen baseline; the receipt records exact changed bytes.

## Exact installed receiving, 2026-11-08

The [installed receipt](evidence/saved_progress_reuse_installed_20261108_summary.json)
receives all67original public reader/export/CLI/progress/reuse bodies,51fresh
guarded children and16documented commands over four unchanged original historical
databases. Producer2a0c4469e2aaeb257c8eca7a77e394711abbcd6f owns wheel
0.4.0+160.g2a0c446,4520580bytes, SHA-256
`b91d0882eb3520be9de58336fd02ca04362d8a6ce9abf752c591b260b4f3eea7`.
All210payload files and155nongenerated runtime files authenticate. Receiving
runs outside the checkout with `-I -S -B` and original published ArgDigest0.17.1,
SMonitor0.22.1 and available DepDigest0.11.0 payloads. No `.pth` startup, scientific
or main-package import is admitted; the shared prefix is unchanged.

Existing qualified receiving controls preserve the explicit private legacy-fixture
mapping to the installed core and isolated fresh-child launch. Test bodies are
byte equal; this is one installed-reader slice, not a complete PHMT dependency
solve or supported scientific/platform gate. Source175/installed67counts remain
separate rather than summed as independent scientific tests.

The [owning report](archive/reuse_saved_progress.md) resolves#145. Current-head
source#9/full installed/public#23 and mature0.x acceptance remain open.
