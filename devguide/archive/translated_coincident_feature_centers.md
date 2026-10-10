---
summary: Centroid roundoff admitted co-located feature centers as non-collinear rigid anchors.
issue: uibcdf/pharmacophoremt#31
status: resolved
opened: 2026-10-03
closed: 2026-10-10
severity: medium
verification: measured
area: [screening, geometry]
guard: tests/test_correspondence_geometry.py
normative: devguide/rigid_search_workflow.md
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


## Reviewed resolution — 2026-10-10

The implementation already published in `fdb57dcbe8e4d9d8364d1dcf5199a7945bfd9a2f`
was reviewed without changing runtime code. The public guard now has 60 cases:
three origins, four proposal routes (query, association cliques, triplet seeds and
ranked triplet seeds), reference order permutations, valid non-collinear identities
and degenerate candidate controls. Independent `math.dist` inequalities establish
that the loose candidate tolerances admit all pair-distance conditions; complete
empty proposals therefore protect the actual eligibility mechanism.

The focused guard passes 60 cases in 5.22 s. The complete scientific selection
`python -m pytest --receptor=llm` passes 680 tests in 1304.02 s on Python 3.14.7,
with 12 warnings: ten expected B-factor drops, one deliberate optional-attribution
failure control, and one unit-stripping warning in legacy screening. The separate
recorded audit executes 12 origin/route cases containing rejected references,
complete empty candidates and valid identities. Prepared observed EST self-motion
recovery gives the nondegenerate seed `[[0,0],[1,1],[4,4]]` under both final and
each_step policies, one placement / three fits / five matched features, unchanged
source coordinates and valid returned pairs.

The full detached result and inert execution source are retained in
`devguide/evidence/seed_eligibility_review_py314.json.gz`; the sibling
`seed_eligibility_review_py314_summary.json` records both archive SHA-256 digests,
producer/input identities and scope limitations. All seven Python producer
fingerprints and input hashes remain unchanged during the suite/audit. All 19
earlier gzip archives, including the prepared molecular artifact, retain their
exact committed bytes. This review does not qualify fresh hosted/installed
artifacts, numerical conditioning or biological performance.

The concurrent ownership audit in uibcdf/pharmacophoremt#41 found and independently
reproduced the corresponding mean-centering defect in MolSysMT's public
`least_rmsd_fit()` validation. It is reported as uibcdf/molsysmt#367 with nine
provider calls; no provider code or local molecular validator was added. #31 is
resolved for automatic pharmacophoric seed eligibility. Arbitrary caller-supplied
fit mappings still depend on the provider repair, and must not be described as
qualified by this closure. The maintained rigid-search contract records this
distinction and the guard.
