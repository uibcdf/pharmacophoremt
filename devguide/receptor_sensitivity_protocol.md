# Prespecified receptor projection sensitivity controls

Owner LMMV/dprada, [#83](https://github.com/uibcdf/pharmacophoremt/issues/83),
2026-11-04. This is the first analytical slice of audit item 12, following
#79/#80. The protocol and [complete parameter declaration](../tests/data/receptor_sensitivity/plan.json)
are fixed before the first case execution and retained with its evidence.

## Question and scope

Do explicit receptor projection hypotheses respond to independently varied
placement, positional/angular tolerance, exclusions and curated constraints as
their documented geometric contracts predict? This assesses the existing
receptor-based infrastructure, not optimal pocket selection, interaction energy,
physical steric radii, ligand binding modes or predictive performance.

Use only the direct public receptor constructor/facade, exclusion builder,
curation tools and placed PoseEvaluator. Molecular construction, recognition,
selection, planes, coordinates and any transformation belong to MolSysMT.
No local chemistry, molecular direction inference, format parser or preparation
routine is introduced. MolSysMT #375/#323 and TopoMT pocket ownership remain.
ArgDigest #47/#48 and PHMT #82 are neither fixed nor bypassed by this study.

## Inputs fixed before evaluation

Two authored analytical systems use existing unshipped public-MolSysMT builders:

- `[Na+].[Na+].[Cl-]`, centers `(0,0,0)`, `(2,0,0)`, `(.5,0,0)` nm.
  The two sodium sites stand in for receptor positive-charge features; chloride
  is a placed negative-charge candidate. This disconnected geometry is a
  mathematical charge-complement control, not a receptor or salt binding model.
- Two parallel aromatic rings from the existing `aromatic_build_case('parallel')`
  fixture. The first ring supplies a cached receptor feature; the second is the
  placed candidate, with center displacement `.35 nm` along z. The known input
  plane is xy. Projection target normals are caller parameters, not molecular
  directions computed by PHMT.

All molecular inventories are obtained through existing get_features calls with
real MolSysMT recognition. Never replace recognition with an expected answer.
Preserve selected atom indices, frame zero, reference chemical state, cached
inventories and source coordinates. These inputs are authored under the
repository license; no external structures, activities or reserved cohort are
opened. Provider recognition attribution retains the actual executed sources.

## Complete matrix and independent expectations

Lengths below are nm, angles degrees. The exact decimal grid uses dyadic charge
lengths so the deliberate radial/exclusion boundary is representable in binary.
It is a numerical design choice, not a physically calibrated parameter grid.

| Family | Fixed settings per unit policy | Independent expected transition |
| --- | --- | --- |
| Placement/radius | Projection distances .25, .375, .5, .625, .75 crossed with radii .0625, .125, .25 | Candidate at .5: match iff absolute displacement is at most the site radius. Expected matching counts by radius: 1, 3, 5 |
| Sphere/Point contrast | Distances .25 and .375, fixed sphere radius .125, crossed with point_tolerance .03125, .125, .5 | Sphere outcomes stay negative and positive respectively; Point tolerance does not widen a Sphere |
| Exclusions | Exact positive query at .5, exclusion centered at receptor atom zero, radii .25, .5, .75 | Strict interior veto: no clash, no clash at equality, clash; positive fit stays one |
| Constraint ablation | Seven declared essential/weight/min-fit/site-removal variants of a two-site model | Distinguish weighted coverage, requiredness, minimum fit and removal; see the literal expectation rows in the declaration |
| Aromatic orientation | Target tilts 0, 15, 30, 45, 90, 150, 180 crossed with tolerances 15, 30 | Unoriented axis angle is min(tilt, 180-tilt); expected matches 3 and 5, with the documented cosine slack only at floating boundaries |

This is **45 valid placed evaluations per policy**, plus one real invalid-frame
failure. Run twice under nm/ps/radians and pm/fs/degrees: **92 attempts**, with
no input replacement or omitted failed cell. Inputs, placement and settings are
identical in physical units. Point tolerance and site radius retain distinct
semantics; positional/angular matches include their boundary, steric exclusions
use strictly inside. Geometry assertions use 1e-12 nm/dimensionless; no tolerance
is fitted to observed biological outcomes.

Each two-site constraint model projects the two source positives by .5 nm. Only
the first has a candidate. Removing or relaxing a site is an explicit curation
decision with a reason, source map and changed denominator. A zero weight does
not remove an essential requirement. These logical effects do not measure a
site's causal contribution to binding.

## Accounting and decision rules

Retain every model, setting, full native result, assignment, missing requirement,
clash, criterion and actual attribution payload. The invalid frame must remain
failed/unscored, with source-stage error and native cause; do not convert it to
a negative or include it in acceptance fractions. One candidate is reused in
each analytical cell; these are parameter settings, not independent molecules,
replicates or estimates of uncertainty. Report transitions rather than a pooled
success rate. No confidence interval or statistical hypothesis test is meaningful
for this fully specified deterministic matrix.

There is no search, fitting, seed selection, conformer generation or ranking:
search budget is zero and every declared fixed pose is evaluated once per cell.
Source coordinates and cached inventories must remain unchanged; application
unit configuration must be restored. A mismatch is an investigation, not license
to adjust the expected table or choose a favorable setting. Preserve initial
failures and every executed source/native/test/input identity.

## Qualification and continuation

Completion requires the declared analytical answers, unchanged-input controls,
full original results, focused regressions, existing receptor/exclusion/curation
compatibility and relevant documentation/report/archive checks. Source execution
does not establish installed/public/all-platform or hosted qualification.

Next extend to donor orientation and independently justified development inputs,
then predeclare preparation variants and finite-search budgets. MolSysMT owns
those molecular variants and identity/grouping. Keep final evaluation data
reserved; #66's original experimental-method gate remains independent. Automatic
pocket/hypothesis generation and the whole audit item 12 remain incomplete even
if this bounded slice passes. Addon/new release remain deferred.

The executable recorder and measured receipt are linked after the first run;
this original declaration remains unchanged when results are appended.

## Measured result — 2026-11-04

The original declaration above remains unchanged. The [recorder](../phmt_test_support/receptor_sensitivity.py)
and [independent guards](../tests/test_receptor_sensitivity.py) retain every cell.
The [case](../docs/content/validation/receptor_sensitivity.md) and
[receipt/full original evidence](evidence/receptor_sensitivity_20261104_summary.json)
link the complete producer history. Final scope: 245 passed in 198.40 s, including
49 new controls, zero failures/errors/skips. Five pytest and one standalone
recorder identity checks remain stable; the latter also executes all 92 attempts.

The protocol found #84, two radius-boundary decisions reversed by conversion
roundoff. The final positive-site comparison allows eight float64 epsilons
relative to the radius or Point tolerance, exposes this allowance in criteria
and uses a difference form that avoids radius-expansion overflow. This numerical
policy is not an extra physical tolerance. Strict exclusion/angle/assignment/
score semantics and all originally expected transition tables remain.

The first new guard had 21 wrong serialized-field expectations and two visible
boundary failures; public QuantityRecord decoding and the actual curation schema
correct the guard, revealing three failing controls for those same two cells.
A mistyped legacy selector exits 4 with zero cases. Both 245-case broad runs pass;
the final run uses the reviewed difference form. Every attempt/version is
retained. Source coordinates, inventories, curation source, application policy
and actual completed-evaluation attribution stay intact.

This completes the first analytical slice only. The next independent receptor
step is a new prespecified extension on the cached prepared-receptor case;
missing molecular directions/preparation remain with MolSysMT, pockets with
TopoMT. Full development uncertainty and biological validation are still open.
