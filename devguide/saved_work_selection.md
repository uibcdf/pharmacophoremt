# Select saved work by status

Owners LMMV/dprada; 2026-11-08; [#158](https://github.com/uibcdf/pharmacophoremt/issues/158).
The [plan](evidence/work_selection_plan_20261108.json) precedes implementation.

## Public tool and ownership

`ScreeningRunView.work_items(*, status=None)` returns the same detached
manifest_ordinal/work_key/source_key/occurrence_key records, in original order.
The default None preserves the original all-work path. Exact matched,
not_matched and failed values select confirmed native statuses; pending selects
work without a published terminal outcome. Input strings are not normalized.
Status is unrelated to a chemical activity label or an active worker.

The existing owned core selects/decodes confirmed records and keeps the original
unfiltered metadata path. Pending iteration needs only publication membership
after admission; it does not decode unpublished drafts. Confirmed filtering
reuses the original outcome decoder one record at a time. The same core status
validator is used by the public definition-owned ArgDigest digester. The existing
SMonitor error boundary, caller-owned connection, lifetime/thread/deferred errors
and explicit legacy admission remain. Iteration retains at most the current
original payload/record; complete opening still verifies all evidence. No new
molecular, quantity, optional-engine or attribution boundary exists.

## Command and response compatibility

Use `--work-items --status STATUS`, with optional positive --limit and
nonnegative --offset. Status is valid only in that mode; argparse refuses syntax
conflicts before opening the database. The caller selects which saved statuses
to inspect, not a scoring criterion or new scientific evaluation.

Filtered pages use a separate `pharmacophoremt.screening-work-selection@1`:
original run_id/run_format/work_sha256, global declared_work, selected_work,
exact status, offset/limit/next_offset and original records. Offset/next_offset
address the selected ordered stream; each record's manifest_ordinal remains
global. Existing public progress counts from that same verified read-only
snapshot supply selected_work, without reimplementing the counters. Empty or
beyond-end selections return no records and next_offset null. Clamp the iterator
window to the selected count, including integers beyond sys.maxsize.

Each command opens a new verified snapshot. After the writer resumes and
publishes more outcomes, restart selection at offset0: a filtered offset is
not a durable cursor across changes to the set of confirmations.

Without --status, preserve the complete ordinary work-page@1 bytes. Scalar ranks,
progress, exact-key detail and outcome exports remain unchanged. Filtered metadata
contains no query/context/native evidence; use the existing exact-key detail for
original confirmed bodies. Status selection, paging and view closure complete
before JSON success output. Handled errors exit2 without success JSON.

The requested page bounds retained records, not complete opening/count work or
largest decoded original payload. Selection can scan confirmed outcomes and
offset prefixes; this does not qualify an index, incremental memory or scale.
Persisted schemas, source/chemical identities, score definitions, dependencies
and launchers stay unchanged. Changed producer bindings can require a fresh linked
scientific run; historical independent reading remains supported.

## Receiving state

The [source receipt](evidence/work_selection_source_20261108.json) retains
99 passing selected bodies (14 new/85 original), unchanged ordinary command
bytes, strict documentation and local governance. One exact owned installed
receiving remains pending. Preserve original failures and separate producer
identities. Full exact-head source, complete public
dependency/installed-platform, biological, human-usability and release gates
retain their independent acceptance.
