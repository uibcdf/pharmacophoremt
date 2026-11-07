# Prepared-library recovery reference

## Later public implementation — 2026-11-07 UTC

The [public prepared-run contract](public_prepared_runs.md) is now implemented
with197 selected local cases and bounded source/installed/development receiving.
The old recovery helper contains exact public
aliases; the old storage helper delegates to the one shipped private stdlib core.
Historical reading preserves the old format; public writing uses a distinct
versioned format and admits no implicit legacy reexecution. Changed helper/runtime
fingerprints can refuse old reexecution without implying changed chemistry.
The original experiment and its measured evidence below retain their identities.

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108).
This extends the [incremental reference](prepared_library_reference.md) with an
unshipped transaction/recovery experiment. Source lives in
[`reference_run_store.py`](../phmt_test_support/reference_run_store.py) and
[`prepared_library_recovery.py`](../phmt_test_support/prepared_library_recovery.py).
Names and SQLite layout remain experimental, with no new public runtime API.

The later [read-only inspection](reference_run_inspection.md) reuses this same
ledger to expose work coverage and bounded observed rankings without current
scientific providers or reexecution. It has separate controls and evidence;
it does not weaken the compatibility checks for resuming a run.

## Binding a run

The producer supplies a saved native JSON query, a PHMT work manifest and explicit
prepared/preparation/feature/index/grouping/numerical compatibility declarations.
The manifest is metadata, one JSON object per line, with exactly `work_key`,
`source_key` and `occurrence_key`. It is not a molecular reader or molecular
equivalence implementation. Duplicate work keys are rejected; repeated sources
and occurrence grouping remain possible. Original counts and variant/assay
aggregation keep their separate contracts.

`build_recovery_plan` validates the saved query through public native I/O and
constructs the selected existing native tool. Constructor/evaluation defaults
are expanded from their defining signatures. Options must be finite JSON values;
physical options retain explicit native unit strings. Native ArgDigest/scientific
preflight is reused. No new general molecular, argument or quantity engine is added.

The exact query bytes, detached effective recipe, compatibility declarations,
PHMT Python-source digest, reference-helper digests, interpreter and selected
provider versions bind the run. Resume compares the current binding before
requesting a source iterator, and reconstructs its private evaluator from saved
query bytes and options. It never accepts an unrelated mutable evaluator pointer.
JSON spelling and query-byte differences conservatively require a new run even
when a human considers them equivalent. Storage paths/times are not scientific
identity; relocation of unchanged artifacts remains possible.

**These checks do not authenticate molecular input.** A prepared snapshot identity
is a producer declaration. Provider code/native artifacts and preparation accuracy
need their separately qualified identities; package versions alone do not prove
their source closure. Prepared objects and source mapping must remain unchanged.
Tests use controlled existing explicit-coordinate fixtures, with no new collection
download or preparation. A second query or changed method/budget/policy uses a new
run, optionally recording `parent_run_id`; that link is provenance, not molecular
equivalence, automatic parent validation or another independent compound.

## Publication and interruption

The store uses the Python standard library's SQLite interface. Its rollback journal,
explicit transactions and exclusive connection ownership avoid inventing an
append-file framing/recovery protocol. The chosen modes follow SQLite's primary
[transaction](https://www.sqlite.org/lang_transaction.html) and
[locking](https://www.sqlite.org/pragma.html#pragma_locking_mode) contracts;
their availability does not qualify this consumer's platform or durability claims.

| State | Persisted evidence | Recovery behavior |
| --- | --- | --- |
| Started | Work/attempt identity before molecular evaluation | Unconfirmed work can be recomputed in a new retained attempt |
| Staged | Encoded result and checksum, not published | It remains unconfirmed; resumed evaluation can recompute it |
| Confirmed | One outcome and its winning attempt linked atomically | Preserve and skip evaluation, including terminal failures |

Work uniqueness, source mapping and confirmed visibility are stored on disk.
Creation streams manifest metadata with bounded line reads. Reopen checks the
schema, query/context/manifest identities, ordered mapping and stored payload
integrity before trusting confirmed outcomes. Verification and replay stream rows;
the store retains no collection-sized Python uniqueness/output set. Checksums
establish consistency, not trusted origin or biological/scientific validity.

An identical publication is idempotent and retains the original winning attempt.
A conflicting payload fails visibly. Confirmed terminal failures stay authoritative
in that run; retrying a failure requires a linked new run. Original attempts and
failures are not rewritten. A failed new-store creation is not silently replaced
or treated as a valid empty run; an existing path is never overwritten.

`resume_prepared` reopens the caller-owned prepared sequence from its declared
beginning. Every mapping, including previously confirmed entries, must match the
ordered manifest. Reordered, unknown, duplicate or prematurely exhausted work
fails visibly. Reading already confirmed handles may still be necessary; this
does not implement provider seek/reopen capabilities. The result generator stops
pulling when closed and does not close a caller-owned source or ledger.

## Saved view versus delivery

The result generator yields **newly confirmed outcomes only**. `ledger.results()`
is the authoritative complete run view, in declared work order. A process may stop
after confirming a result and before yielding it to its consumer. Reopening the
saved view recovers that result; appending generator deliveries to an external
export is not an exactly-once export protocol. No exactly-once computation is
claimed either: interruption before confirmation can require another calculation.

Saved-result replay uses only the standard-library store and preserves original
native/provenance fields. It neither accesses molecules nor registers new scientific
attribution. The scientific composer retains existing native diagnostics and
actual attribution behavior. Storage-format errors use ordinary standard-library
exceptions, as other unshipped evidence utilities do; no new public diagnostic
or optional-provider boundary is introduced.

## Scope of qualification

The [frozen plan](evidence/public_library_recovery_plan_20261107.json) and
[original receipt](evidence/public_library_recovery_20261107_summary.json) record
the selected administrative/analytical controls, source overlay, providers and
limits. Guards
are [`test_reference_run_store.py`](../devtools/tests/test_reference_run_store.py)
and [`test_prepared_library_recovery.py`](../tests/test_prepared_library_recovery.py).
The former can run without scientific imports. Both helpers are declared explicitly
for the existing private installed-test support route; staging alone does not
qualify an installed artifact.

The declared selection passed **48 scientific cases** (22 recovery and 26 original
incremental controls) and **45 administrative cases** (21 ledger and 24
distribution/staging). Reporting (3), archive (18), full Ruff check/format, indexes
and declared dependency routes are separate local checks in the receipt.

Scientific execution used Python 3.14.10, CPU 19/100% quota, 512 MiB memory, no
swap, 32 tasks, nice 19, idle I/O and one backend thread. Whole-cgroup peak was
348,200,960 bytes; administration peaked at 76,042,240 bytes under the same caps.
Neither scope had OOM/max events. These are execution observations, not comparative
performance or incremental per-input allocation measurements.

The retained worked artifacts contain two closed SQLite runs, their exact saved
queries and the same two-row manifest. The first query yields scores `[1, 1]`;
the second, deliberately distant query yields `[0, 0]`, with the original run
unchanged. Both rows refer to occurrences of one repeated controlled molecule;
there are no activity labels or independent-compound accuracy estimates.
Separate saved replay with scientific/citation imports forbidden recovers both
views, changes no database bytes and executes no new molecular calculations.
The receipt's `worked_original` and `worked_second` binary envelopes use existing
`evidence_archive.read_archived_bytes(..., identity_key=...)` integrity checking;
the main evidence archive retains their query/manifest text and full source/logs.

Controlled Python exceptions and process termination around publication are the
target here. Power loss, filesystem faults, network filesystems, distributed or
multiwriter execution, supported-platform/minor matrices, a public guided API,
production provider snapshots and large-collection performance remain separate.
None follows merely from SQLite's own guarantees. No biological validation or
receptor-study admission is claimed. The earlier #9 administrative OOM attempt
retains its original failed scope and recovery route.
