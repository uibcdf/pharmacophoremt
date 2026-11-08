---
summary: Inspect one exact saved work item and its original confirmed evidence.
issue: uibcdf/pharmacophoremt#157
status: resolved
opened: 2026-11-08
closed: 2026-11-08
verification: measured
area: [results, usability]
guard: tests/test_public_work_item.py::TestPublicWorkItem::test_original_outcomes_and_pending_work_remain_distinct
normative: devguide/saved_work_item_inspection.md
blocked_by: []
supersedes: []
---

# Inspect one declared input without scanning exported outcomes

Public manifest pages expose identities but omit statuses/native evidence.
Progress is aggregate and ranked inspection omits failures. Add an explicit
detail operation so a user can inspect one original key through both the public
API and command, without rerunning science or parsing an exported file.

`ScreeningRunView.work_item(work_key)` and `--work-key WORK_KEY` compose the
owned reader/core, existing key admission, confirmed-outcome decoder and
meta-only attempt iteration. The new detached format preserves one mapping,
original run/work identity, confirmation/status, retained attempt counts and
complete original confirmed evidence. Pending work has no outcome; unpublished
payloads remain hidden. Attempts do not prove that a worker is currently active.

The [owning contract](../saved_work_item_inspection.md) and
[prospective plan](../evidence/work_item_plan_20261108.json) fix independent
original-row/count/evidence oracles, original read-only bytes, exact keys,
whole-file verification, detachment, lifetime/thread and public admission,
guarded source commands and the same owned installed test bodies. Existing
rank/progress/page/export routes, legacy admission, units and attribution stay
unchanged. ArgDigest/SMonitor retain their boundaries; argparse owns CLI syntax.

No molecular/parser/collection, new dependency, schema migration, environment
transaction or scientific credit is introduced. Selected detail intentionally
contains full original native evidence; the caller owns disclosure. Tests remain
serial with one CPU/thread, low priorities and 512 MiB reader limits. This is
milestone2/#108 product work; #148 and full public/platform/release gates remain.

## Source implementation received

The core now reuses confirmed decoding and metadata-only attempt iteration;
the public method has a definition-owned ArgDigest contract and the command
delegates directly. All 85 selected cases pass, including 16 new guards and
69 original reader/CLI/page/progress/export cases. The initial 15-case missing-
capability run retains 12 failures/three passes and its subtests. An earlier
84-case pass remains separate; the final extra guard checks original failure
details without emitting the stored error again. Old API/core methods except
command orchestration remain AST-identical; formatting preserves tested ASTs.
Strict full documentation, the method/recipe anchors and library link, full
Ruff/format, indexes and three reporting tests pass. The
[source receipt](../evidence/work_item_source_20261108.json) retains exact limits,
original outcomes/counts and the distinct earlier scope. Exact owned installed
receiving remains pending; no public/platform claim follows.

## Exact owned installed receiving, 2026-11-08

Implementation3e45a58592d2a71c647ee052d304d1a74438d59c owns the single
0.4.0+185.g3e45a58 wheel (4526305 bytes, SHA-256
`0ee478f475d4ef8d04b27218a91dfe9f0e4d05f35ecace5255bdbcf5823ec509`).
The [installed receipt](../evidence/work_item_installed_20261108.json) passes
all 85 same original bodies outside checkout using authenticated published
ArgDigest0.17.1/SMonitor0.22.1/DepDigest0.11.0 payloads and isolated/no-site
startup.211payload/156nongenerated runtime files, eight original fixture files
and seven loaded parent runtime modules verify.72guarded children retain
46successes/26expected refusals. Eight exact documented detail commands preserve
original rows/outcomes/attempts/identities and bytes in four historical databases.
The source receipt retains its original pending bridge state; this separate
receiving resolves the bounded task. No original test body/legacy wrapper changes;
only subprocess launch wiring selects admitted installed roots.

No scientific/attribution namespace loads or source runtime fallback occurs.
Whole installed-command peak62259200bytes includes guards/tests/tooling; it is
not detail allocation or performance evidence. Reader AS/DATA remains512MiB,
one CPU/thread and low priorities; no aggregate local cgroup is enforced. Shared
prefix/public support and QA bytes stay unchanged; no new manager transaction,
molecular execution or resource increase occurs. Full-source exact-head,
complete public PHMT dependency/installed-platform, human usability, biological,
scale/performance and release gates remain separate.
