---
summary: Complete explicit argument controls for native interactions and composition.
issue: uibcdf/pharmacophoremt#200
status: resolved
opened: 2026-11-12
closed: 2026-11-12
verification: measured
area: [api, modeling]
guard: tests/test_interaction_argument_controls.py
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

## Executed resolution — 2026-11-12 local date

The [combined receipt](../evidence/interaction_argument_controls_20261112.json)
receives source148f3ba and its exact isolated wheel with267 selected source/owned
cases each,51 public-ArgDigest controls per context, public PUW0.28.1 and24
guide-block executions. The old artifact receives all12 corrected oracle cases
while its original1failed/11passed result stays unchanged. Native inputs and
scientific bodies retain their scope; broader#6/full supported/public gates remain
independent. All initial failed probes/harnesses remain recorded.
