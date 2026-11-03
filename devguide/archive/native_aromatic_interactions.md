---
summary: Build aromatic and cation-pi hypotheses with shared geometry and explicit participant mapping.
issue: uibcdf/pharmacophoremt#34
status: resolved
opened: 2026-10-03
closed: 2026-11-03
verification: measured
area: [modeling, interactions]
guard: tests/test_aromatic_interactions.py
normative: devguide/aromatic_interaction_workflow.md
blocked_by: []
supersedes: []
---

# Native aromatic interaction hypotheses

## Resolution — 2026-11-03

Reviewed and incorporated as a bounded aromatic source/API workflow. Clean
receiving producer ee257a1aaec6ea02a185e6961b0deea9769f7fbf has exactly the same
runtime/helper/test/driver/workflow trees, actual loaded Python/native sources,
input hashes and distribution metadata as measured code 6a7537b. Its original
418-item execution includes all **46 aromatic controls** and existing native
hydrophobic/H-bond/ionic regressions, zero failures/errors/skips. The [new receipt](../evidence/aromatic_acceptance_20261103_summary.json)
verifies that reuse against the original archive and XML; no new pytest execution
is claimed for this review.

Fresh driver execution passes both tracking profiles: seven declared native
profiles over 14 case/profile combinations, 28 queries and 84 placed-pose
evaluations each. References/round trips fit one, displacements fit zero; source
atom identity/chemical state/coordinates and query metadata remain unchanged.
One expected strict compound-cation conversion per profile remains failed with
fit_value=None. Only the explicit containing_center policy produces its shared
positive center, retaining three original singleton observations and charges.
Scientific projections agree off/on; actual credits remain 6 items/11 uses off
and 14/30 on, with the provider-declared references, not executed reference engines.

All three existing cookbook blocks execute and strict isolated recipe rendering
passes with one neighboring exclusion-recipe link-target stub. Physical source/
native/helper/test/input and metadata identities stay equal in both fresh phases.
No runtime/test/fixture/expectation/provider/prefix/sibling changes are needed.
Ordinary editable PHMT 0.4.0+62.g6a7537b and controlled MolSysMT 0faf1584/native
remain unchanged. Exact rings/default charge membership, source/frame/state maps,
shared planes/charge centers, explicit partial-cation policy, failed-versus-negative
semantics and real attribution/persistence/absence/failure remain protected.
The #35 sealed nonfinite JSON/YAML guards are included in the 46 reused cases;
its resolved scope and original archives remain separate and unchanged.

The original October text/results below remain historical; pending review is
superseded by this acceptance. This is not biological/energy/performance,
universal fused-ring equivalence, fresh full-suite, clean installed/public/
platform or exact-head hosted qualification. Those boundaries remain #23/#10/#9
and inherited workspace #82. #41 stays partial for supported public-vector/floor/
installed migration and final legacy retirement (review 2026-11-11).
Next review #21 reference-anchored aligned consensus, then #24 alternative aligned
clique consensus, each against its own scientific contract. #66 still awaits four
original binding methods; addon/new release remain deferred. Owned root
/tmp/phmt34-acceptance-20261103-pxec9r01/, LMMV/dprada, review 2026-11-17.
No local process remains after closeout.

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
