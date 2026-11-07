# Public prepared screening runs and independent saved-result reading

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108), mature-0.x milestone2.
Source qualification passes; owned installed-wheel receiving is pending. The
[prospective plan](evidence/public_prepared_runs_plan_20261107.json) was
[declared before execution](https://github.com/uibcdf/pharmacophoremt/issues/108#issuecomment-6702125074).
Passing evidence and actual counts will be recorded after execution.

## One public task, separate scientific and saved-reading boundaries

The scientific API belongs to `pharmacophoremt.screening`:
`PreparedRunPlan`, `build_prepared_run_plan`, `resume_prepared_run` and
`PreparedScreeningRun`. A caller saves a native query and ordered three-key work
manifest, declares preparation/input compatibility, creates a run, consumes an
incremental result iterator, closes it and later reopens the same compatible run.
The friendly run class owns its store; it does not own the supplied readers.
Expert composition exposes the same native plan and publication operations.

`pharmacophoremt_results` is an independent companion package in the same
distribution. `ScreeningRunStore` owns transaction/publication and
`ScreeningRunView` owns read-only saved inspection. The public reader and
`python -m pharmacophoremt_results` use ArgDigest's standard contracts and
SMonitor, without importing the main PHMT, molecular, numerical or attribution
namespaces. Their private storage core remains standard-library-only.
This preserves meaningful historical reading without changing PHMT's intentional
application-preserving eager unit-policy initialization.

## Version and compatibility contracts

New public stores write `pharmacophoremt.screening-run@1`. The legacy
`pharmacophoremt.reference-ledger@1` remains an experimental historical format.
Public reading admits that format only with explicit `allow_legacy=True`;
public writing/resume must never implicitly convert it. Old support-store
entrypoints keep their legacy semantics through the one private implementation.
No previously saved query/context, attempt or outcome is rewritten by promotion.

Saved reading validates schema, checksums, mapping, every attempt and every
outcome, including evidence outside the requested top results. It retains
original query bytes, native fields, source multiplicity, producer versions and
attribution. It compares no current scientific provider, executes no stored
code or molecular calculation and records no new scientific credit. These
checks establish internal consistency, not authenticity or scientific validity.

The new public envelope enforces `seeded_hit@1`'s declared binary value:1 for
matched work and0 for not-matched work; failures remain unscored. This validates
the stored field without reconstructing fitted witnesses or importing scoring
providers. Even a checksum-valid conflicting score is refused. Explicit legacy
reading preserves the original experimental admission rules and values rather
than rewriting them to the newer format's contract.

Reexecution uses a separate `pharmacophoremt.prepared-run-plan@1` binding. Exact
query bytes, detached effective settings, six producer compatibility declarations,
interpreter/provider versions and location-independent PHMT/companion source
content determine compatibility. A code or byte-spelling change can conservatively
require a new linked run without implying changed chemistry. This is not an
automatic scientific-compatibility evaluator or complete native/provider closure.
Changed queries/settings and retries of terminal failures use new run identities.
The original run remains readable; `parent_run_id` is a provenance link.

Native JSON I/O and evaluators remain the authorities for query schemas, physical
units, options, geometry, scores, failure causes and actual attribution. The run
adapter stores their existing explicit native records without interpreting bare
numbers as quantities or normalizing producer versions. MolSysMT#624 retains
molecular collection/preparation/lifetime/snapshot ownership; supplied snapshot
identities remain producer declarations.

## Publication, interruption and source ownership

One exclusive writer owns a SQLite connection. Started attempts, staged evidence
and confirmed terminal publication remain separate transactions. Reexecution may
repeat unconfirmed work; confirmed outcomes, including failures, are immutable
and skipped. Confirmation occurs before an outcome is yielded. Consequently,
the resume iterator yields only new confirmations; `results()` is the complete
authoritative saved view. Appending iterator delivery to an external file is not
an exactly-once export protocol. Fresh exports must read the saved complete view.

Resume checks the complete binding before obtaining the source iterator, then
checks every encountered mapping against the ordered manifest, including work
already confirmed. Reordering, duplicates, unknown work and premature exhaustion
fail visibly while preserving confirmed progress. The caller reopens its source
from the beginning; no provider seek/replay capability is invented. Closing the
result iterator stops further pulls without explicitly closing borrowed readers.

The read-only view owns a verified read transaction until close; close the writer
before opening it, and close the view before resuming. Observed ranks include
valid zero scores, exclude unscored failures and break ties by manifest ordinal.
They cover observed scored work only. Work completion may include failures and
does not imply chemical, conformer-search or biological completion.

SQLite transactions and controlled-process interruption do not by themselves
qualify power-loss, filesystem-fault, network-filesystem, distributed or multiwriter
durability. Per-input payload size, SQLite cache and caller accumulation remain
separate costs; bounded iteration/top-K retention is not a throughput claim.

## Source qualification checkpoint

The [final execution overlay](evidence/public_prepared_runs_execution_20261107_attempt3.json)
fixes40 source/control/recipe files.197 distinct local cases pass:82 scientific,
94 administrative,3 reporting and18 archive. This includes22 promoted recovery
controls,15 friendly scientific controls and21 new public-storage controls.
Ruff check/format, indexes and declared dependency routes pass. Recipe blocks,
fresh-process receiving and helper computations are not extra test cases.

Both public recipe blocks execute with the same three original PubChem3D
conformers/query. A first zero-score confirmation remains unchanged after close;
resume adds only the remaining two, with scores0/1/1 and one attempt per work.
Fresh guarded readers/CLI inspect the partial, complete and explicitly admitted
legacy views without scientific/provider imports. Legacy new-writer reopening
is refused. Original database/query/H5 bytes and all18 original pilot files
remain unchanged. The application-owned session retains12 attribution items/27
uses. The separate migrated pilot callback reproduces full native composition
and translation controls with12 items/34 uses and no network operations.

Original attempts are retained in `build/phmt-public-runs-20261107-w9c85754`:
administrative attempt1 has one package-namespace assertion failure out of92;
attempt2 passes82 scientific/92 administrative cases under its original bytes.
The pre-freeze binary-criterion review adds two regressions for the final core;
attempt3 passes82/94. Earlier native/source observations are preserved, never
rewritten or added to the distinct-case count. The earlier plan/snapshots retain
their hashes and authority only for their original source.

All heavy execution is serial, CPU19/quota100%, one backend thread, nice19/idle
I/O,512MiB cgroup and no swap. Final scientific peak451,026,944 bytes;
administration79,155,200, public recipe249,688,064 and migrated consumer244,723,712.
No OOM/max events occur. These are execution observations, not benchmarks.

Next freeze a source commit, build one owned wheel using the verified cached
versioningit2.3.0 overlay, and repeat the public task outside the checkout.
Also read the source-produced run from that installation while preserving its
original runtime and refusing incompatible reexecution. The unchanged project
requirement~=2.0 is not replaced to fit the shared prefix's3.3.0.
Full supported
source/dependency/installed/public/platform/release gates remain under
#9/#10/#23/#95; biological studies and measured large-library performance retain
their independent plans. Original geometry and complete native database/export
bodies remain local under the existing publication scope.
