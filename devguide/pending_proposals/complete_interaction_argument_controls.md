---
summary: Complete explicit argument controls for native interactions and composition.
issue: uibcdf/pharmacophoremt#200
status: active
opened: 2026-11-12
closed:
verification: measured
area: [api, modeling]
guard:
normative: devguide/interaction_query_argument_controls.md
blocked_by: []
supersedes: []
---

# Native interaction argument controls

## What and why

Extend #6's explicit public-control rule to `from_interactions`,
`from_interaction_collection` and `compose_pharmacophores`. At2feb44c,
explicit False/True calls fail with UnknownArgumentError/TypeError. Ordinary
calls and native scientific guards already work. This is API adoption, not a
new ArgDigest or molecular-provider defect.

The [contract](../interaction_query_argument_controls.md) preserves closed
defining-owner contracts, native validation, original evidence and independent
outputs. The collection's established canonical adapter/composer calls may use
explicit True without blindly forwarding the outer flag or bypassing science.

## Acceptance and exclusions

Signature/contract and default/False/True controls under nm/pm; native profiles,
source/state/maps/coverage, constraint and empty-query refusals; keep/reuse
semantics, recorded internal forwarding, source custody and saved readback;
source/exact-owned/public-provider receiving and public recipes. Preserve every
original failed attempt and separate supported source/installed/public gates.
No scientific algorithm, molecular implementation, native schema, dependency,
prefix or performance claim changes. Broader #6 and merge/curation facades remain
partial; #148/#165 remain stopped.
