---
summary: Inspect all declared screening work through bounded command-line pages.
issue: uibcdf/pharmacophoremt#156
status: partial
opened: 2026-11-08
closed:
verification: measured
area: [results, usability]
guard: tests/test_public_work_cli.py::TestPublicWorkCLI::test_pages_preserve_all_original_work_including_unconfirmed_entries
normative: devguide/saved_result_cli.md
blocked_by: []
supersedes: []
---

# Inspect declared work without writing Python

The independent reader already streams `ScreeningRunView.work_items()`, but
the command exposes only progress counts, ranked confirmations and outcome
exports. Pending and unpublished mappings cannot be inspected from the terminal.
Milestone2/#108 needs an accessible route to original work/source/occurrence
correspondence, without inferring chemical identity or repeating screening.

Add mutually exclusive `--work-items`, with default ten records, positive
`--limit` and nonnegative `--offset`. Return one versioned finite JSON page with
minimal original run/manifest identity, declared count, offset/limit, nullable
next_offset and unchanged original-order work records. Use verified immutable
work_count for continuation; consume only the selected prefix/window of the
existing iterator and close it explicitly. Page memory depends on the selected
limit; offset traversal is linear, and opening still verifies the complete run.
This does not qualify large-library performance or add a complete manifest export.

Argparse owns syntax/refusals before database I/O. The existing ArgDigest/
SMonitor view owns admission/storage errors. Summary/export/scoring conflicts,
nonpositive work limits and offsets outside this mode are refused. Existing
ranked defaults/zero limit/output, summary and export semantics remain. Legacy
admission is explicit. No query/context/native payload or scientific/attribution
import is added. There is no molecular parser/collection or new dependency.

The [prospective plan](../evidence/work_cli_plan_20261108.json) fixes independent
manifest/page oracles, original bytes, fresh guarded commands, empty/partial/
complete/legacy/Unicode cases, unconfirmed work, lazy iteration/closure, full
verification beyond the page and no success JSON after iteration/close failure.
Receive original CLI/reader/progress/export controls and one exact owned wheel
outside checkout. Use one CPU/thread, low priorities and512MiB local limits;
native acquisition/#148 and full public/platform/release gates remain separate.

## Source implementation received

The command now returns the declared bounded page by composing the existing
public configuration and manifest iterator. The same fully verified read-only
snapshot supplies the immutable count and original run/work identities; no
lookahead or storage/codec duplication is needed. Original store, digester,
scoring and main scientific modules remain unchanged.

All69 selected reader/CLI/export/progress cases pass, including12 new controls.
The original nine failures/three passes and three failed subtests are retained
without counting subtests as additional bodies. Source formatting leaves the
complete tested ASTs unchanged. Strict full documentation, rendered anchor/link,
full Ruff/format, index and three reporting controls pass. A read-only HTML checker
initially mistakes the valid encoded @ entity for a missing literal; stdlib
unescaping corrects that check without changing the rendered output. The
[source receipt](../evidence/work_cli_source_20261108.json) retains its failure.
Exact owned installed receiving remains pending and will be recorded separately;
no supported public/platform claim. Changed scientific producer bindings may
require a fresh linked run for reexecution; original independent reading remains.
