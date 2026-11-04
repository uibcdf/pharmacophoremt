---
summary: Qualify intentional molecular references and explicit independent source variants.
issue: uibcdf/pharmacophoremt#60
status: resolved
opened: 2026-10-21
closed: 2026-11-04
verification: measured
area: [architecture, integration]
guard: tests/test_live_reference_ownership.py
normative: devguide/live_reference_ownership.md
blocked_by: []
supersedes: []
---

# Live references and independent native molecular variants

## Resolution — 2026-11-04

Existing PHMT semantics are adequate in the reviewed scope: curation copies
independent pharmacophore data while retaining the intentional molecular source.
Explicit independent molecular variants use public MolSysMT operations. No runtime
repair or new molecular code is necessary. #121 is now closed; the earlier
provider-readiness notice is superseded by current source receiving.

[Contract](../live_reference_ownership.md) and [receipt](../evidence/live_reference_ownership_20261104_summary.json)
record 199 passing focused controls, including ten new integration cases, both
unit policies, bidirectional edits, owner-local analysis invalidation, historical
queries, failure preservation and real pure-copy attribution. Eight initial guard
failures were a NaN-equality test mistake; all attempts/probes are retained.
Provider 0faf1584 and consumer eb39eef are exact source identities; the newer
sibling guide/checkout is read-only context, not substituted runtime evidence.
Installed/public/platform/performance/predictive claims remain separate.

## What

Review intentional live molecular references versus independently editable
molecular variants, without changing all pharmacophore copy operations.

## How

Inspect curation/builder contracts and current provider ownership, then execute
real prepared source copies, controlled edits, named analyses and PHMT models.
Test errors and original/bidirectional preservation, using provider public APIs.

## Why

Source maps, units, reference axes, caches and original bibliography must remain
unambiguous. A molecular copy is neither a new scientific result nor an implicit
consequence of copying a pharmacophore.

## What is measured and what is assumed

Linux/Python 3.14.7 source receiving with extracted public ArgDigest 0.17.0 and
inherited dependencies. Both attempt identities stable. Prior provider-incomplete
warning is historical; broader provider/client coverage remains #408/#122.

## Alternatives and refuted paths

No local molecule deepcopy/inspection/invalidation engine, no implicit source
clone and no adoption of deferred-copy optimizations. Cached dictionaries/models
are not authenticated automatically against a changed live source.

## Scope and exclusions

Reviewed native curation and explicit eager molecular-copy source contract;
legacy Pharmacophore.merge loss/alias review is separate #77. No blanket library
correctness, raw mutation guarantee, arbitrary extension or released dependency
compatibility is inferred.

## Acceptance criteria

Meaningful real consumer guards protect independence, intentional references,
metadata/maps/units/attribution, invalidation and failure preservation. Document
source identity and hand results to central #122/provider #408. Maintain #77 as
an independent finding; historical results and original issue record remain.
