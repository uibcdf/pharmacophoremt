---
summary: Inspect all declared screening work through bounded command-line pages.
issue: uibcdf/pharmacophoremt#156
status: resolved
opened: 2026-11-08
closed: 2026-11-08
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

## Owned installed receiving, 2026-11-08

Implementation5d77c9cb46e48ebd915a35ad4d0f205ab6240603 owns the single
0.4.0+183.g5d77c9c wheel (4525665bytes, SHA-256
`a360c01c77e6f72cbb3f2d7ea5bbe6d8f6f8ec7dd1a35af055b5fe420e8e025b`).
The [separate installed receipt](../evidence/work_cli_installed_20261108.json)
passes the same69original bodies outside checkout with isolated/no-site startup,
published ArgDigest0.17.1/SMonitor0.22.1/DepDigest0.11.0 payloads and no source
runtime fallback. All211payload/156nongenerated runtime files, seven original
fixture files and seven loaded parent runtime modules verify. Only fresh-child
launch wiring changes; the original legacy fixture wrapper and test bodies stay
unchanged.59guarded children retain38successes/21expected refusals with no
scientific/attribution namespace import. Eight exact documented work commands
pass on four original historical databases with rows/identities/bytes unchanged.

Whole installed-command peak RSS61042688bytes includes guards/tooling/tests;
it is not incremental page allocation or performance evidence. Original512MiB
reader AS/DATA, one CPU/thread and low priorities remain; no aggregate local
cgroup is available. No environment transaction/shared-prefix mutation, native
execution or resource increase occurs. The bounded bridge resolves; supported
public PHMT dependency/installed/platform, biological, scale and release gates
remain separate. The source receipt preserves its original pending bridge state.
