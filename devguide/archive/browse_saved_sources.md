---
summary: Browse exact original source labels and declared work through the saved reader.
issue: uibcdf/pharmacophoremt#170
status: resolved
opened: 2026-11-09
closed: 2026-11-09
verification: measured
area: [results, usability, screening]
guard: tests/test_public_source_inventory.py
normative:
blocked_by: []
supersedes: []
---

# Browse original declared sources

## What

Add `ScreeningRunView.source_items()` and CLI `--sources`, returning exact
source labels, their first original manifest ordinal and all declared work
counts in first-encounter order. This makes source selection discoverable before
the user has to inspect every work entry.

## How and ownership

Compose the existing owned stdlib store and definition-owned public reader.
Keep all original publication/identity/validation/lifetime boundaries. SQL groups
literal source labels; it does not infer compound, state or chemical equivalence.
No schema/index, molecular reader/collection, counter store or provider operation.

CLI source-page@1 counts one inventory stream in one verified snapshot, retaining
only the requested prefix. Full admission/grouping/sorting may scan/use temporary
storage beyond the displayed prefix; no scale or constant-memory claim follows.

## What is measured and what is assumed

The [prospective plan](../evidence/source_inventory_plan_20261109.json) freezes
scope/resources and independent controls before runtime edits. The
[source receipt](../evidence/source_inventory_source_20261109.json) receives
134cases (14new/120existing), thirteen original command-byte controls, strict
full docs and25distribution/local reporting checks. Original red controls
retain12failures/2passes. The [installed receipt](../evidence/source_inventory_installed_20261109.json)
receives the same134bodies from source adbecee / owned208,157guarded children,
24documented commands on four historical stores and thirteen ordinary outputs
with exact source bytes. All214wheel payloads/159runtime files and seven loaded
reader origins verify; no scientific namespace is imported.
The af408e7 full-CI/single-cell recovery keeps its original independent identity;
it cannot qualify this later implementation.

## Alternatives and limits

Do not materialize/group molecular objects or infer aliases. An exact label can
own repeated occurrences and every work state; publication must not change this
immutable-manifest inventory. No new citation, scientific or source connector
capability is earned by reading the metadata. MolSysMT#624 owns collections.

## Acceptance criteria

Independent original order/count/opaque-key/all-state/after-publication controls;
empty/legacy/lifetime/thread/error/corruption boundaries; original command bytes;
same bodies from one exact owned source-free artifact with scientific imports
blocked; API/docs/checkpoint/report/index evidence. Full discovery-to-detail
composition follows separately. #148/#165 remain stopped.

## Received 2026-11-09 UTC

The original red control retains12failures/2passes. Independent manual literal
oracles cover nonadjacent repeats, every work state, opaque/Unicode/zero/NUL keys,
publication stability and full admission/lifetime/error boundaries. The CLI
counts a single source stream and emits no success on late failure. Existing
response bytes remain unchanged. The same original134test bodies/identities pass
from source and one owned artifact; guarded child expected refusals remain
observed (125exit0,32exit2). Eight source-inventory, eight status and eight
source/status documented commands agree with independent original SQL/JSON
oracles on four unchanged historical files. Thirteen ordinary source outputs
also agree byte-for-byte.

Strict full docs/rendered API/navigation,25distribution, declared routes,
generated environments, Ruff/format and reporting/archive checks pass. Hash-bound
full evidence retains executable controls and original failures. Reader peaks
are approximately109/126MiB under the original DATA512MiB/AS1GiB serial envelope;
separate docs peak is approximately289MiB. One CPU/thread and low priorities,
host reserve/pressure monitoring remain; no kernel aggregate reservation exists.

The bounded reader increment resolves; full discover/select/detail composition
is separately tracked by#171. Later-head full source/public/platform, human
usability, biological, performance and release acceptance remain separate.
