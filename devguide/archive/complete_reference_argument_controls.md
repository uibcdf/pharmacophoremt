---
summary: Complete explicit argument controls for native reference-query construction.
issue: uibcdf/pharmacophoremt#198
status: resolved
opened: 2026-11-12
closed: 2026-11-12
verification: measured
area: [api, modeling]
guard: tests/test_reference_argument_controls.py
normative: devguide/reference_query_argument_controls.md
blocked_by: []
supersedes: []
---

# Reference-query argument controls

## What and why

Complete the explicit expert construction route under #6/#108 with keyword-only
`skip_digestion=False` on `from_feature_inventory` and `from_ligand`. Both ordinary
calls already enforce native value contracts, but explicit False/True currently
fail at argument admission/Python invocation. Preserve native scientific admission
when completing bypass. The [owning contract](../reference_query_argument_controls.md)
defines the bounded change and receiving; no molecular/provider workaround is needed.

## Measured and refuted paths

On cb6af7168aa3ffb6b5a91a83242d2b007cc24e42, direct native calls with False receive
UnknownArgumentError; True receives TypeError. The initial suspicion of missing
ordinary inventory validation is refuted: package discovery already rejects wrong
definitions, out-of-selection participants and negative frames. Original probes
remain retained with the receiving receipt. This is an API improvement, not a
reported new ArgDigest defect or a claim of accepted invalid ordinary inputs.

## Acceptance and exclusions

Explicit defining-owner contracts, compatible default/False/True results under
nm/pm, invalid-control/closed-call and native semantic refusals, preserved metadata,
source custody and nested public admission, source and exact-owned receiving,
documented public composition and appropriate local checks. Scientific methods,
molecular ownership, native formats, dependencies and full supported/public gates
retain their independent scope. #6/#108 remain partial; #148/#165 remain stopped.

## Executed resolution — 2026-11-12 local date

The [combined receipt](../evidence/reference_argument_controls_20261112.json)
receives corrected source9158c71 and its exact isolated wheel:272 source/owned
cases each,37 public-ArgDigest cases per context, public PUW0.28.1, twelve
guide-block executions and162 distribution controls. Original failed hypotheses,
controllers/artifact and input identities are retained. No full supported/public
qualification or completion of umbrella#6 is inferred.
