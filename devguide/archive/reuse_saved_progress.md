---
summary: Reuse verified criterion-independent counts within one immutable saved view.
issue: uibcdf/pharmacophoremt#145
status: resolved
opened: 2026-11-08
closed: 2026-11-08
verification: reproduced
area: [performance, results, inspection]
guard: tests/test_saved_progress_reuse.py
normative: devguide/saved_progress_reuse.md
blocked_by: []
supersedes: []
---

# Immutable saved-progress reuse

The [#144 baseline](../saved_run_scaling.md) measures repeated progress at
477.276802ms median on10000declared/7000confirmed synthetic records. The owning
[contract and prospective experiment](../saved_progress_reuse.md) preserves full
admission, detached outputs, writer freshness, thread/lifetime checks, explicit
legacy admission, ranking/exports and original input bytes.

Only the validated read-only factory may enable private in-memory count reuse.
Existing writer views remain fresh; no persisted index, schema, provider or
molecular collection changes. This saved-result operation belongs to PHMT.
MolSysMT#624 retains molecular-collection ownership.

Acceptance requires meaningful before/after guards, the declared paired
same-input experiment and same-artifact owned installed receiving. Current-head
full source#9 and full supported installed/public delivery#23 remain separate.
Changing companion source changes conservative prepared-run bindings; retain
the explicit fresh-linked-run requirement. Owners LMMV/dprada.

## Source receiving, 2026-11-08

Ten new before/after guards pass (original five failures/five positive controls
retained); all130selected reader/store/profile cases pass. Nine declared pairs
with18fresh arms preserve every input and exact progress/full ranks/exports.
Repeated progress benefits are bounded to an already-open immutable snapshot;
first open/first scan and whole-process RSS remain explicit in the owning
contract. No molecular performance or single-use CLI claim follows. Exact
owned-wheel receiving remains required before closure.

The [source receipt](../evidence/saved_progress_reuse_source_20261108_summary.json)
retains175distinct selected cases, all raw paired observations, actual resources
and119owned evidence files with a verified archive envelope. Source/runtime
hashes are exact; the baseline parent is not relabeled as changed code.

## Resolution received, 2026-11-08

The [installed receipt](../evidence/saved_progress_reuse_installed_20261108_summary.json)
receives all67unchanged public reader/export/CLI/progress/reuse bodies,51guarded
fresh children and16documented commands on four original same-byte historical
databases. Producer2a0c4469e2aaeb257c8eca7a77e394711abbcd6f builds one owned
wheel0.4.0+160.g2a0c446 (4520580bytes, SHA-256
`b91d0882eb3520be9de58336fd02ca04362d8a6ce9abf752c591b260b4f3eea7`).
All210wheel payload files/155nongenerated runtime files authenticate. Published
support payloads remain separate from source-provider performance identities;
the installed reader imports no scientific/main package or checkout runtime.
The prior qualified isolated receiving control retains its explicit fresh-child
and private legacy-fixture mapping; all original test bodies remain byte equal.

The module guard asserts no saved table reads on repeated progress while
preserving exact counts, empty/complete/explicit legacy behavior, detached nested
returns, failed-first-scan retry, writer updates, independent snapshots and
closed/native-closed/wrong-thread refusal. Existing full-admission, corruption,
ranking/export/CLI guards also pass. This resolves the bounded immutable-progress
theme. Full current-head source#9, supported installed/public/platform#23,
scientific validation and the mature0.x staircase remain open. No full dependency
solve, native execution, release or one-shot/writer/molecular speed claim follows.
