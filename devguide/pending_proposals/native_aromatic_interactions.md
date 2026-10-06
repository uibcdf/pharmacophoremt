---
summary: Build aromatic and cation-pi hypotheses with shared geometry and explicit participant mapping.
issue: uibcdf/pharmacophoremt#34
status: active
opened: 2026-10-03
closed:
verification: measured
area: [modeling, interactions]
guard: tests/test_aromatic_interactions.py
normative: devguide/aromatic_interaction_workflow.md
blocked_by: []
supersedes: []
---

# Native aromatic interaction hypotheses

## What

Extend public `from_interactions()` to native pi-pi and cation-pi observations
with shared aromatic/positive-charge feature geometry and explicit participant
mapping. The provider's alternative detection profiles remain selectable.

## How

Call public MolSysMT recognition through `get_features()` once and compose sites
through `from_feature_inventory()`. Require exact ring and default charge
membership. Opt-in containing-center mapping accepts only the declared ProLIF
singleton cation into one unique shared positive center and checks its actual
atomic charge through MolSysMT. Preserve original measures, states, parameters
and references and separate query geometry from observation geometry.

## Why

The next classical complex families should compose with independent placed-pose
evaluation, persistence and exclusions without duplicated molecular algorithms.
The same fixed-frame evaluator must interpret construction and candidate sites.

## What is measured and what is assumed

The focused suite passes 97 tests on Python 3.14.7 (59.37 s). Controls cover all
seven supported native profiles, both ligand roles, orientation/displacement,
charge validation, persistence and actual optional attribution. The retained
driver passes both tracking profiles with 14 case/profile combinations, 28
queries and 84 evaluations per profile; the full integration suite passes 444
tests in 436.36 s with eight known warnings. Three recipe blocks, strict isolated
cookbook rendering and offline quality/reporting checks pass. The full original
evidence and hashes are retained in the evidence index. No biological acceptance,
speed or universal fused-ring equivalence is inferred.

The [owning issue result](https://github.com/uibcdf/pharmacophoremt/issues/34#issuecomment-5974431950)
records the executed checks and acceptance limits.

## Alternatives and refuted paths

Keep upstream three-atom/SMARTS plane criteria as observation evidence instead
of changing shared query geometry. Reject silent partial-cation expansion;
offer an explicit policy. Do not implement molecular recognition locally or
credit a cached detector as newly executed.

## Scope and exclusions

Prepared sources, declared compatible native profiles and one common frame.
Provider-owned receptor preparation and alternative fused-ring membership
policies remain separate work. Undefined quantity provenance is owned by #35.

## Acceptance criteria

Shared-tool composition and independent controls pass, exact failure remains
distinct from geometric negatives, on/off tracking preserves science, source
state/geometry remain unchanged, and the executable cookbook explains the
mapping and evidence limits. Keep active pending review and incorporation.
