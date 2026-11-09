---
summary: Browse exact original source labels and declared work through the saved reader.
issue: uibcdf/pharmacophoremt#170
status: open
opened: 2026-11-09
closed:
verification: asserted
area: [results, usability, screening]
guard:
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
retain12failures/2passes. Exact owned installed receiving remains pending.
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
