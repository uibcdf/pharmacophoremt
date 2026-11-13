---
summary: Complete explicit argument controls for cached curation and merge.
issue: uibcdf/pharmacophoremt#203
status: resolved
opened: 2026-11-12
closed: 2026-11-12
verification: measured
area: [api, modeling]
guard: tests/test_curation_argument_controls.py
normative: devguide/curation_argument_controls.md
blocked_by: []
supersedes: []
---

# Cached curation and merge argument controls

## What and why

At a50c16f, merge has no ArgDigest wrapper/control; cached selection/copy/
extraction already have the curation registry but omit the explicit parameter.
Editing already exposes it. Complete this bounded #6 slice with existing
validators and defining closed contracts; preserve native scientific bodies.
This is PHMT adoption rather than a demonstrated ArgDigest/provider defect.

## Acceptance and exclusions

Follow the [owning contract](../curation_argument_controls.md): explicit controls,
nm/pm default/False/True, inherited merge, native refusal/atomic ownership and
provenance, relevant existing cases, public recipes and source/exact-owned/
public-provider receiving. Record original failed attempts. Nested public tools
retain admission where their canonical contract is not yet established.

No scientific/molecular algorithm, wire schema, dependency, shared prefix,
performance claim or release change. Broader #6 and exact-head full #9/#10/#23
qualification stay independent; stopped #148/#165 remain stopped.

## Current evidence

The initial new guards produce 47 failures/9 passes before implementation,
including an incorrect iterable assumption in the test itself. The corrected
source guard passes 56 cases. Final serial [source receiving](../evidence/curation_argument_controls_source_20261112.json)
passes319 cases and13 quality operations. Exact-owned/public-provider receiving
follows committed freeze; original raw attempts remain retained.

## Executed resolution — 2026-11-12 local date

[Combined receiving](../evidence/curation_argument_controls_20261112.json) passes
319 source/owned cases each, including 56 new controls and 56 actual public-
ArgDigest cases per context, public PUW 0.28.1, public Pytest Receptor 1.2.2 and
18 public guide-block executions. All 240 artifact payloads/185 runtime bodies
and 167 target-only observed modules verify with actual SDK-staged support.

The c2ad4e6 wheel first passes 52/fails 4 new controls because their new oracle
requires exact floating-point equality across pm conversion. The corrected,
hashed unshipped test overlay compares only declared geometry in explicit nm
at rtol=0/atol=1e-14 nm; every other native/site/provenance/constraint field stays
exact. That same unchanged artifact and the source pass the corrected guard.
Original failures, source receipts and warnings remain. No provider defect is
inferred from ordinary roundoff; no runtime/source-data workaround occurs.

The guard checks the missing public controls and preserves native refusal,
source custody and independent outputs. Broader #6/full qualification remain
partial and separately owned; this bounded report can close.
