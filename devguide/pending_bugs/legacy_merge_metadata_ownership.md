---
summary: Resolve legacy merge metadata loss and explicit mutable-site ownership.
issue: uibcdf/pharmacophoremt#77
status: open
opened: 2026-11-04
closed:
severity: medium
verification: measured
area: [api, ownership]
guard:
normative: devguide/live_reference_ownership.md
blocked_by: []
supersedes: []
---

# Legacy Pharmacophore.merge metadata and site ownership

## What

`Pharmacophore.merge` promises self's name and metadata, but a model with nested
metadata yields merged.metadata={}. Both merged sites are identical mutable
objects to their input sites. Metadata loss is confirmed; site sharing is
measured but the existing docstring does not promise independent site storage.

## How

The [#60 receipt](../evidence/live_reference_ownership_20261104_summary.json)
retains merge_probe.py/json on eb39eef: two native sphere models, no molecular
input. Source metadata contains identity/items; output metadata is empty, and
both site identity checks are True.

## Why

Losing declared metadata erases context. Shared sites make variant ownership
ambiguous; settle the compatibility contract rather than infer a new guarantee.

## What is measured and what is assumed

Original source behavior reproduced in the inherited receiving environment.
No runtime fix or scientific-frame equivalence is established by this probe.
#60's qualified native curation/copy tools do not qualify legacy merge.

## Alternatives and refuted paths

Review public compose_pharmacophores and existing copy tools before adding any
implementation. Do not create a second composition engine or infer a shared
molecular source/frame. Molecular operations remain MolSysMT-owned.

## Scope and exclusions

Legacy API metadata and explicit site ownership; no chemical/molecular copy
routine or new pharmacophore scientific method.

## Acceptance criteria

Independent nested metadata preservation guard; settle/test aliases, repeated/
self/empty inputs, scores/references/provenance/frame policy and failure atomicity;
keep or explicitly migrate no-dedup semantics; document delegation/deprecation
against existing public composition. LMMV/dprada own this independent next theme.
