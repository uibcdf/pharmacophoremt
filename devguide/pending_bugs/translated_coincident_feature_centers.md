---
summary: Centroid roundoff admitted co-located feature centers as non-collinear rigid anchors.
issue: uibcdf/pharmacophoremt#31
status: active
opened: 2026-10-03
closed:
severity: medium
verification: measured
area: [screening, geometry]
guard: tests/test_correspondence_geometry.py
normative:
blocked_by: []
supersedes: []
---

# Translation-sensitive eligibility of rigid feature anchors

## What

Mean-centering represented float64 feature positions before matrix rank can
invent a second singular direction when two positions are exactly equal and
the coordinate origin is displaced. The public triplet proposal promises to
omit degenerate anchors but admitted three records occupying only two centers.

## How

The observed EST continuation under #22/#300 produced a ranked self-motion seed
`[[1,1],[3,3],[4,4]]`, containing donor and acceptor O17 at one exact center.
Its ambiguous three-record fit let final refinement recover five pairs in three
fits, while each_step rejected that initial fit in one fit. This was a shared
eligibility defect before either policy, not hydrogen preparation or scientific
evidence favoring one angular policy.

The independent public-proposal control uses two identical typed-feature centers
and one distinct center at three origins. Before correction, two shifted
degenerate controls failed and four controls passed. The private shared predicate
now subtracts an existing represented center before the same relative rank check.
Six controls pass after correction, including the valid non-collinear identities.
The observed ligand's ranked seed is then nondegenerate; both policies recover
all five selected features in three fits.

## Why and ownership

Feature-center eligibility belongs to PharmacophoreMT's correspondence tools;
the corrected primitive is an internal validation predicate, not a new molecular
geometry engine. Molecular fitting and transformations still use public MolSysMT.
The independently reusable proposal/evaluation/refinement operations remain the
public tools. No local Kabsch, hydrogen placer or independent molecular repair is
introduced. Existing reports/archives retain their original producer identities.

## Scope, alternatives and acceptance

This restores rejection of exactly co-located centers without a new physical
near-collinearity tolerance. It does not guarantee conditioning or invariance
below float64 representable resolution. It changes no ranking/angle policy and
does not discard either alternative. Review the public regression module and
full scientific suite before incorporation; retain the issue/report active until
that review. The guard must reject shifted two-center anchors and retain valid
three-center proposals. Donor-inclusive real-ligand evidence belongs to #22.

Verification: the complete suite passes 344 tests in 348.54 s on Python 3.14.7,
with the two earlier warnings and four expected H-builder B-factor-drop warnings.
All 25 focused controls and five new donor-route recipe blocks pass. Both corrected
rigid policies recover the observed fixture's five selected features in three fits;
the original before-correction controls retain their two failures in the local
reproduction log. The final full trace is frozen in
`devguide/evidence/eralpha_hydrogens_py314.json.gz` (decompressed SHA-256
`8c3c176c85f5f578ba6f7ccd850cf67c1ee3256417e898663e741c680c3e97e8`).
The [owning issue result](https://github.com/uibcdf/pharmacophoremt/issues/31#issuecomment-5973140527)
records the before/after public controls and remaining review state.
