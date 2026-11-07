# Complete saved-result exports

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108), mature-0.x milestone2.
This increment extends the [independent saved reader](public_prepared_runs.md).
The contract and prospective plan preceded execution under
[the owning issue](https://github.com/uibcdf/pharmacophoremt/issues/108#issuecomment-6709737215).
Source controls and one owned installed artifact pass the bounded receiving
below. [Receipt](evidence/saved_result_exports_20261107_summary.json).
Full supported installed/public gates remain separate.

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
outputs. The source checkpoint was followed by the installed receiving below;
no scientific calculation was repeated to receive saved evidence.

## Owned installed receiving

Frozen producer `4e8f26acc0a41e373afca400e0854966b66de5dd`; one wheel
`0.4.0+138.g4e8f26a`, SHA-256
`89fc667fac380609ee8e1a5c6eab5f7e811c05c3cbb9f863ba08237b61b6a61d`,
4514543 bytes. All209 wheel files except pip's rewritten RECORD match the owned
target, including the new exporter. All154 non-generated PHMT/companion Python
files match source. The original shared editable version cache remains distinct
at0.4.0+134.gee5d9fa; generated `_version.py` records are retained separately.
The build uses the existing owned versioningit2.3.0 overlay and changes no shared
prefix. This wheel is local receiving evidence, not a public release.

From an outside-checkout working directory, `-I -S -B` admits only the wheel,
stdlib and authenticated original public ArgDigest0.17.1/SMonitor0.22.1/
DepDigest0.11.0 payloads. All21 unchanged reader and15 export test bodies pass
again, with no skips. Two fixture routes are explicit: fresh children use those
same isolated roots, and synthetic legacy writing uses the installed storage
core rather than the unshipped development shim. All8 fresh-child guard records
verify their boundaries. No PHMT scientific, molecular, numerical, attribution
or development-support namespace is imported or attempted.

Four authentic original databases are compared with a direct read-only SQLite
payload/configuration oracle: source complete3 rows, installed complete3,
source partial1 with2 pending, and explicit legacy complete3. Full JSONL native
records/configuration equal the originals; CSV equals their literal scalar
projection. Original scores0/1/1 and the partial zero remain unchanged. The exact
standalone public cookbook block runs for all three public-format views; legacy
uses explicit admission. Every original database and runtime file stays intact.
No query, molecular input or producer installation is needed to export.

The initial post-build verifier mistakenly compared the generated version cache;
the one built wheel was retained, with both actual version records, and not rebuilt.
The initial installed finalizer then assumed lazy DepDigest had loaded after all
tests/exports passed. Its continuation verifies retained outputs and original
test/guard logs without repeating either operation. Installed metadata and
loaded-module state remain separate; individual child exit codes were asserted
by the passing tests but not independently retained before that finalizer failed.
Both original failures and continuations remain in the receipt. The first
distribution launch also retained a missing default SDK error (zero tests);
using the existing clean pinned SDK passes all24 distribution controls.

Distinct selected source cases total83:15 export,21 reader,24 distribution,
2 dependency,3 reporting and18 archive. The installed36 are repetitions, not
additional distinct bodies. Original-database observations and cookbook executions
are not extra test cases. Full Ruff/index/whitespace checks pass. Build/staging
uses per-process `RLIMIT_DATA=512MiB` instead of an address-space cap so Git's
file mappings remain possible; installed reading uses `RLIMIT_AS=512MiB`.
Neither replaces unavailable aggregate cgroup/no-swap/task/quota controls.

The next increment is an intuitive CLI export route composing these same public
methods, without a ranking criterion for complete-view export. General source
operations and MolSysMT#624 collections remain separate. No scale, performance,
biological, full dependency-solve or supported-platform gate is established here.
