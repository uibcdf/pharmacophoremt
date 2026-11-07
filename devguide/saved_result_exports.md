# Complete saved-result exports

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108), mature-0.x milestone2.
This increment extends the [independent saved reader](public_prepared_runs.md).
The contract and prospective plan preceded execution under
[the owning issue](https://github.com/uibcdf/pharmacophoremt/issues/108#issuecomment-6709737215).
Source controls pass; owned installed receiving remains pending at this source
checkpoint. Full supported installed/public gates remain separate.

## Public operations and data authority

`ScreeningRunView.to_jsonl(path)` and `.to_csv(path)` export **all confirmed
outcomes in manifest order** from the existing read-only snapshot. Neither
method ranks, filters, retries, executes science or loads molecular, numerical
or attribution providers. Pending work and unpublished attempts are omitted.
Confirmed failures and valid zero negatives are included. Explicit legacy
admission retains original values, including historical fractional scores.

JSONL writes one complete original outcome per line using the existing finite
canonical JSON codec. Original native geometry, unit records, producer versions
and attribution are retained without enrichment or fresh credit. CSV writes
the header `work_key,source_key,occurrence_key,status,ranking_score,score_method`;
status comes from the native result. Empty score cells mean unscored, including
failures; zero stays zero. Opaque identifiers are quoted as needed and retain
their literal Unicode and newline content. Both encodings use UTF-8 and LF row
terminators. CSV is a scalar projection; it does not contain native evidence.

Each method returns a detached plain-JSON `pharmacophoremt.screening-export@1`
receipt with `file_format`, absolute `path`, `encoding`, `bytes`, `sha256`,
`configuration`, `configuration_sha256`, `exported_records`, `pending_work` and
`published`. Configuration is the complete original saved configuration, not
current reader versions. Its digest uses the existing canonical codec. Pending
work is declared work minus exported confirmations, including confirmed failures
in the latter count. The caller can save the receipt with `canonical_json`.
Exporting two formats or saving that receipt is not a multi-file transaction.

The database remains authoritative for query bytes, attempts and resumability;
an exported file is not a run backup. Checksums express consistency, not
authenticity, chemical independence or biological validity. Callers retain
storage/disclosure authority over complete results and configuration.

## Filesystem and failure contract

Use a fresh destination in an existing directory. No parent directories are
created and existing files, directories or symlinks are never replaced. A closed
view is rejected before filesystem effects. The writer streams one outcome at
a time to a private file in the destination directory, closes and hashes it,
then publishes the complete file with an exclusive hard link. A concurrent
destination is also protected. Filesystems that do not support this operation
fail visibly; no weaker overwrite or partial-publication fallback is used.

Before publication, writing, iteration, hashing or link failure leaves no newly
published destination and attempts to remove the private file. Cleanup failure
is attached as a note to the original error; its path remains inspectable. After
successful publication, private-file cleanup failure raises `ScreeningRunError`
with `published=True`, `receipt` and `temporary_path` in its structured context,
and the cleanup error as cause. The destination then contains the complete
export. Normal success returns `published=True`. Interruptions propagate after
cleanup; they do not promise external exactly-once delivery. Disk power-loss,
hostile directory mutation, network filesystems and unexecuted platforms are
not qualified by these process-level controls.

ArgDigest owns definition-specific closed signatures/path admission; SMonitor
retains catalog errors and original causes. No new dependency is required.
The exporter owns PHMT evidence projection and uses standard-library I/O. The
shared tool catalogue and existing PHMT helpers expose no qualified reusable
saved-result exporter to delegate to. Molecular export/preparation remains
MolSysMT-owned. Existing result iteration remains available to expert callers.

Adding companion code changes the conservative scientific runtime binding.
Historical runs remain readable/exportable, but reexecution with changed code
can require a new linked run under the existing compatibility contract. This
increment does not implicitly migrate runs or relax their binding.

## Prospective receiving

The [plan](evidence/saved_result_exports_plan_20261107.json) fixes the intended
controls. Run new export controls and existing reader controls, then qualify a
single owned installed artifact outside the checkout using authenticated public
support payloads. Compare complete exports with original saved native records;
preserve failures, source identities and original producer declarations. No new
chemical-data acquisition, molecular preparation or scientific score is needed.
Full supported source/installed/public/platform/release gates remain separate.

## Source checkpoint

All15 export and21 existing reader controls pass, as do repository-wide Ruff
lint and formatting. The first source attempt passed14 export/21 reader bodies
and stopped at an unsorted test import; that failure is retained. The revised
attempt adds descriptor-open failure/cleanup coverage and passes15/21. Repeated
bodies are not additional distinct cases. Controls exercise actual files and
fresh processes; injected failures supplement ordinary successful export.

The original requested systemd scope could not start: this session has no user
bus/runtime directory. No tests executed in that launch. The actual fallback
uses CPU19, one backend thread, nice19/idle I/O and inherited per-process
`RLIMIT_AS=512MiB`. Aggregate memory, no-swap, tasks and CPU quota could not be
enforced; one-CPU affinity remains enforced. Available memory/pressure are checked
and actual limits are retained. This is no aggregate-memory/performance claim.
No shared prefix, provider, native binary or unrelated process is changed.

Local capsule: `build/phmt-saved-exports-20261107-0emth8zc` (ignored). It preserves
the failed launch, first lint failure, exact execution snapshots, commands and
outputs. Owned installed/export receiving is the next action; no new scientific
calculation is needed to receive opaque original saved evidence.
