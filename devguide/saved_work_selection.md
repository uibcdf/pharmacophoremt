# Select saved work by status or original source

Owners LMMV/dprada; 2026-11-08; [#158](https://github.com/uibcdf/pharmacophoremt/issues/158).
The [plan](evidence/work_selection_plan_20261108.json) precedes implementation.

## Public tool and ownership

`ScreeningRunView.work_items(*, status=None, source_key=None)` returns the same detached
manifest_ordinal/work_key/source_key/occurrence_key records, in original order.
The default None preserves the original all-work path. Exact matched,
not_matched and failed values select confirmed native statuses; pending selects
work without a published terminal outcome. Input strings are not normalized.
Status is unrelated to a chemical activity label or an active worker.

## Exact source selection — #166, 2026-11-09

Optional `source_key` selects the exact original nonempty opaque string and
intersects with `status`. None leaves source unrestricted; unknown keys return
no records. Preserve literal whitespace/case/Unicode/punctuation, repeated
occurrences and global ordinals. Reuse the store's key validator through the
definition-owned ArgDigest contract. No compound alias or chemical grouping is
inferred. The existing SQLite tables select by a bound parameter before decoding
confirmed outcomes; no schema/index or provider collection is added.

`--source-key KEY` is valid only with `--work-items`. Empty keys and syntax/mode
conflicts refuse before file access. Attach leading-dash values using `=`.
Source-selected CLI pages use `pharmacophoremt.screening-work-selection@2`, with
the original run/hash and global declared_work, exact source_key, nullable status,
intersection selected_work and selected offsets/limit/next_offset. One complete
selected iteration in one verified snapshot supplies both count and page;
retained records are bounded by the requested page. Failures after the page fills
still refuse success. Full-file verification and the largest original payload
retain their original costs. Existing all-work/status-only response bytes remain
separate @1 contracts. The [public recipe](../docs/content/cookbook/saved_work_inspection.md#find-all-work-for-one-original-source)
shows both routes. No reexecution, new attribution, chemical independence,
large-library speed or new provider/library connector is qualified.

The [prospective plan](evidence/work_source_selection_plan_20261109.json) records
the unchanged resource limits and MolSysMT#624 collection boundary. The
[source receipt](evidence/work_source_selection_source_20261109.json) receives
120selected cases (13new/107existing), eight unchanged ordinary command outputs,
strict full docs and local governance. One exact owned installed receiving
remains pending.

## Original status-only contract — #158

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

Without either filter, preserve the complete ordinary work-page@1 bytes. Scalar ranks,
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
bytes, strict documentation and local governance. The
[installed receipt](evidence/work_selection_installed_20261108.json) receives
the same99bodies from the exact153ea50 owned wheel outside the checkout, with
93guarded children, eight documented commands on four unchanged historical
databases and verified runtime/fixture/public-support identities. The bounded
bridge resolves; the original source receipt keeps its then-pending state.
Preserve original failures and separate producer identities. Full exact-head
source, complete public
dependency/installed-platform, biological, human-usability and release gates
retain their independent acceptance.
