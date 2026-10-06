---
summary: Search prepared rigid ligands using reusable correspondence and MolSysMT alignment tools.
issue: uibcdf/pharmacophoremt#15
status: active
opened: 2026-10-02
closed:
verification: measured
area: [screening, modeling, integration]
guard: tests/test_rigid_search.py
normative:
blocked_by: []
supersedes: []
---

# Native rigid pose search

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
