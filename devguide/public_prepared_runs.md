# Public prepared screening runs and independent saved-result reading

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108), mature-0.x milestone2.
Source and bounded owned installed-wheel receiving pass. The
[prospective plan](evidence/public_prepared_runs_plan_20261107.json) was
[declared before execution](https://github.com/uibcdf/pharmacophoremt/issues/108#issuecomment-6702125074).
The executed evidence and actual counts are recorded below.

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

The [complete export contract](saved_result_exports.md) adds
`ScreeningRunView.to_jsonl(path)` and `.to_csv(path)`, with a detached original
configuration/byte-digest receipt and explicit pending counts. These methods use
the same complete saved view, including zero negatives and confirmed failures.
JSONL retains original native evidence; CSV projects scalar fields. A private
file is completed before exclusive publication; existing destinations are never
replaced. Export is separate from ranking and scientific resumption.
The [CLI contract](saved_result_cli.md) composes those same methods through
`--to-jsonl FILE`/`--to-csv FILE`, preserving the existing ranked inspection
syntax and explicit legacy admission. Source controls and bounded independent
installed reader/command receiving pass. This
does not clear complete source/governance or installed scientific gates.

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

## Installed and development receiving

Frozen producer: `ee5d9fae7a412b5276840cbec7289fdd95ddd375`.
The one wheel is `pharmacophoremt-0.4.0+134.gee5d9fa-py3-none-any.whl`,4512131
bytes, SHA-256 `df36ba5e2d8e726813d4ce16ae36ce9738ad897a3f25eb3a7f81f7b8c71aa6db`.
The [receipt/archive](evidence/public_prepared_runs_20261107_summary.json)
retains exact code, metadata, controls and scalar results. Original geometry,
queries, databases and full native/attribution bodies remain local.

Both public recipe blocks pass from this identical installed file, with target
and cwd under owned `/tmp/phmt-public-runs-20261107-njzjsmvy`, outside the checkout.
Every imported PHMT/companion file matches the wheel. Partial/complete/legacy
fresh readers and actual public module CLI load no scientific namespace; source
run reading preserves original runtime/versions. Installed reexecution of that
source-produced run is refused before a source iterator is available. Scores,
source mappings and all18 original files remain unchanged; installed peak is
256,139,264 bytes, with no OOM/max events.

Build peak is425,848,832 bytes under the same limits. A verified cached
versioningit2.3.0 build-only overlay satisfies the unchanged~=2.0 requirement;
the shared build-tool3.3.0 is not substituted or upgraded.

After that unchanged-prefix qualification, normal-prefix cold lookup showed the
old editable registration omitted the new top-level namespace. The canonical
no-deps/no-index editable refresh updates only this member's metadata and ignored
generated version cache to0.4.0+134.gee5d9fa. Other provider versions and the
MolSysMT native hash remain unchanged. A fresh isolated interpreter from `/tmp`
imports both packages normally, without source-path injection. All154 Python
files equal the qualified wheel; the location-independent runtime binding matches.
It reopens the installed complete run, produces zero new results/evaluations and
preserves all bytes. Refresh peak is149,254,144 bytes, without OOM/max events.
This distinct development receiving does not requalify the entire shared prefix.
The original source measurement retains its earlier generated-version/cache
identity; no producer metadata or source-produced outcomes are normalized.

Full supported
source/dependency/installed/public/platform/release gates remain under
#9/#10/#23/#95; biological studies and measured large-library performance retain
their independent plans. Original geometry and complete native database/export
bodies remain local under the existing publication scope. Released support-provider
receiving is now [measured separately](reader_public_provider_receiving.md):
the same unchanged wheel passes22 reader controls per cell with four public
provider combinations; corrected SMonitor0.22.1 also passes all application
diagnostic scenarios. This qualifies the reader's support closure, not the whole
PHMT distribution. Continue guided/expert usability and MolSysMT collection/source
operations under their separate contracts.
