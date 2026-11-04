---
summary: Resolve legacy merge metadata loss and explicit mutable-site ownership.
issue: uibcdf/pharmacophoremt#77
status: resolved
opened: 2026-11-04
closed: 2026-11-04
severity: medium
verification: measured
area: [api, ownership]
guard: tests/test_pharmacophore_merge.py
normative: devguide/pharmacophore_merge.md
blocked_by: []
supersedes: []
---

# Legacy Pharmacophore.merge metadata and site ownership

## Resolution — 2026-11-04

Pharmacophore.merge delegates to the public compose_pharmacophores tool with
self/other labels and duplicate_policy=keep, retaining the first name/description.
Every site occurrence and metadata tree is independent. Both input metadata,
scores and references are retained as component provenance; output score/ref_mol
remain None, common known ref_struct is retained and conflicting frames fail.
This explicitly migrates the former promise of first-root metadata to the
existing structured composer namespace, fixing loss without root-key collisions.
No molecular system is copied or queried; the first live reference remains.

[Contract](../pharmacophore_merge.md) and [receipt](../evidence/pharmacophore_merge_20261104_summary.json)
retain original failures and exact overlays. Guards cover six geometries, nested
metadata, duplicates/self/empty/chained input, frame/source policy, public delegation,
copy failures, molecular-operation prohibition and native persistence. Original
23 guard failures include new contract decisions, not 23 historical bug claims.
Original report text below is preserved verbatim. Installed/platform/full-suite/
predictive and SDF-provider gates stay separate.

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
