---
summary: Search prepared rigid ligands using reusable correspondence and MolSysMT alignment tools.
issue: uibcdf/pharmacophoremt#15
status: resolved
opened: 2026-10-02
closed: 2026-11-03
verification: measured
area: [screening, modeling, integration]
guard: tests/test_rigid_search.py
normative: devguide/rigid_search_workflow.md
blocked_by: []
supersedes: []
---

# Native rigid pose search

## Resolution — 2026-11-03

Reviewed and incorporated as the prepared rigid pose-search source/API method.
The [new receipt](../evidence/rigid_search_acceptance_20261103_summary.json)
records clean receiving head **1e00aca9a9f389adbeca41ff00388ce02570b895**.
All **68 fresh controls** pass in 42.89 s without failures/errors/skips: 13 rigid-
search, 26 explicit seeded-scoring, eight retrospective and 21 attribution controls.
The ten warnings are intentional optional/cross-provider attribution-failure
controls, retained with their original groups/log. These protect proper motion,
reflection/distortion, source/selection/frame preservation, donor/aromatic geometry,
zero-angle precision, essential/optional/weight/exclusion semantics, independent
provider tools, failure causes, scoring consent, stable input accounting and real
optional attribution. No new full suite is claimed.

Fresh host-off/on capsules verify five typed prepared inputs, standalone proposals/
MolSysMT alignment and an ionic triangle. Reference identity placement fits one
without a molecular fit; a moved ligand recovers fit one with recorded provider
alignment. Missing chemistry is a complete checked-pose negative at zero.
A one-product budget returns an admissible identity maximum despite incomplete
enumeration, retaining enumeration_complete=False/n_fitted=0. A six-product ionic
case reaches an admissible fitted maximum, retaining incomplete enumeration and
n_fitted=1. Neither result claims full alternative enumeration or minimum RMSD.
Without an admissible maximum, the same unfinished work raises PoseEvaluationError
at search_budget, with PHMT-E105 retained as its cause and no returned result.

Full enumeration with an exclusion can retain positive coverage one while remaining
not_matched. Truncating that vetoed search is a failure, not a proven maximum.
The separate explicit seeded_hit criterion retains a complete no-seed negative
with pose_evaluated=False, fit_value=None, no assignments and ranking_score=0;
that legitimate zero remains distinct from status=failed. A fitted admissible
binary hit terminates at hit_found and scores one. Compatibility partial coverage
remains pose evidence and requires explicit checked_pose_coverage consent for
retrospective ranking; no frame-independent molecular score is inferred from it.

The full six-input generator/repeated-input retrospective control has perfect
analytical AUC/BEDROC and three active hits. Its limited counterpart retains
original class counts 3/3, two evaluated inputs per class, failures at indices
1/3, evaluated indices [0,2,4,5] and scores [1,1,0,0]. Failed searches retain
fit_value=None and PHMT-E105; they are excluded from metrics without changing
input identities or becoming negative scores. Two JSON/YAML round trips under
changed unit policies retain metadata and reference/moved/chemistry-negative
outcomes (1/1/0). Source atom identity/state/coordinates remain unchanged under
each identical unit policy; off/on scientific projections agree. Actual capture
is 3 items/6 uses host-off and 13/50 host-on.

Both unchanged documented Python examples execute with application-owned capture
(13 items/50 uses). Strict isolated Sphinx rendering of the original maintained page
passes with three neighboring link-target stubs, not full-site/neighbor qualification.
Full loaded source/native/helper/test/input and metadata identities are stable in
focused, capsule and example phases. No library/test/fixture/scientific-definition/
provider/prefix/sibling change is needed. An initial launcher used the wrong
temporary basename and exited before imports/tests; its unqualified attempt is
recorded separately and only the launch path was corrected.

Molecular construction, chemical/coordinate inspection, motion, native point-cloud
least-RMSD fitting, copy/get/set and RMSD remain public MolSysMT operations. PHMT
owns pharmacophoric proposals, pose constraints, termination/score interpretation
and retrospective failure accounting. No molecular solver or preparation engine
is added. Prepared frames/states and finite triplet families remain explicit;
these fragment controls do not establish biological enrichment or continuous/
conformational completeness, physical inactivity, global optimum or performance.

This resolves #15 source/API acceptance. #63's separate binary-ranking contract
is preserved; source receiving does not qualify clean installed/public/platform/
hosted gates (#23/#10/#9) or repair inherited workspace #82. #41 remains partial
for supported-public/floor/installed receiving and final legacy retirement, review
2026-11-11. Next #14 independently accepts shared classical reference construction/
geometry and its placed-pose route, followed by #13/#19 owning observation/attribution
contracts. #60/#66 retain their gates; addon/new release defer. Owned root
/tmp/phmt15-acceptance-20261103-yioexkdv/, LMMV/dprada, review 2026-11-17;
no local process remains after closeout. Original October/provider/future-work
statements below retain their historical identities and are superseded where noted.

## What and how

The local slice adds public `get_correspondences()`, `align_to_pharmacophore()`
and `RigidPoseSearch` in screening. Consumers compose chemical extraction,
essential-center triplet proposals, public MolSysMT point-cloud fitting and
placed-pose evaluation. Retrospective validation accepts the search tool and
shares stable batch/failure accounting with PoseEvaluator.

## Evidence and limitations

The guard tests real-provider motion recovery, mirror/distortion negatives,
independent tool use, preserved source/selection/frame data, physical units,
essential/optional rules, exclusions and explicit incomplete-search failures.
The selected molecular fitting route is CPU/double; MolSysMT owns its kernel.
Verification uses published pinned provider sources plus existing dependencies.
No clean-wheel, hosted-matrix, biological-pilot or accelerated-backend success
is claimed. The implementation remains uncommitted and open for review.
On 2026-10-02 the full local suite passed 98 tests, including eleven rigid-search
and precision controls; both documented examples also passed. Ruff, generated
indexes, three offline reporting tests and whitespace checks passed. The adjacent
zero-angle roundoff correction is independently tracked in `#16`.

## Acceptance and next steps

`../rigid_search_workflow.md` states the method, bounds and reproducible example.
At least three essential non-collinear centers are required. A complete discrete
triplet search is not an exhaustive continuous pose solver. No conformers or
torsions are generated. Incomplete enumeration raises unless a valid unit-fit
hit demonstrates maximum coverage; failed calculations are not scientific
negatives. Prepared multi-conformer workflows and consensus are subsequent work.
