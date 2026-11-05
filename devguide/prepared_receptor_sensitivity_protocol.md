# Prespecified sensitivity on the prepared ERalpha receptor fragment

Owner LMMV/dprada, [#85](https://github.com/uibcdf/pharmacophoremt/issues/85),
2026-11-04. This extends #83/#84 using the original #52 prepared geometry.
The [complete parameter declaration](../tests/data/prepared_receptor_sensitivity/plan.json)
and independent oracle definitions below are fixed before evaluation.

## Question and scientific boundary

Does the explicit receptor projection workflow preserve its declared geometric
meaning when placement, positional/angular tolerance, exclusions and exclusion
removal vary on the cached prepared PHE404 geometry? This is an analytical
development control on a real prepared fragment. A transformed PHE404 candidate
is neither a new ligand/conformer nor a predicted binding pose. No biological
labels, optimal physical parameters, statistical uncertainty or performance
claim follows from deterministic parameter cells.

## Frozen input and provider ownership

Load the unchanged H5MSM through the existing #52 archive loader and public
MolSysMT conversion. Native SHA-256 is
`a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a`.
The original summary, fragment manifest, deposition/redistribution references,
historical producer identities and preparation limits stay authoritative. Do
not regenerate H, refine its environment, redetect cached contacts or silently
promote this fragment to complete-receptor readiness.

Select PHE404 with public MolSysMT `select`: ring atoms 796–801, heavy atoms
791–801, original full-system selection including nine H 2772–2780, frame zero,
reference chemical state. MolSysMT supplies recognition, centers, ring axes,
native decoding and all molecular translations/rotations. PHMT supplies the
explicit pharmacophoric hypotheses, exclusions, curation and placed evaluation.
No new molecular geometry, format, preparation or pocket routine is introduced.

## Prespecified candidates and complete grid

Build one candidate by translating a copy of the complete source by
`[0,0,.35] nm`, evaluating only the original PHE404 selection. A second candidate
is a public MolSysMT proper +90-degree rotation around global x about the cached
provider ring center, then that same translation. The exact matrix is in the
declaration. These are methodological transformations, not experimental poses.

| Family | Cells per unit policy | Fixed design and independent expectation |
| --- | --- | --- |
| Placement/radius | 18 | Separate +z/-z hypotheses, distances .25/.35/.45 nm, radii .02/.08/.12 nm. Translated center is +.35 nm: positive-face matching counts by radius are 1/1/3; opposite face has none |
| Exclusions | 3 | Exact positive query, cached 11 heavy-atom exclusions with radii .01/.20/.40 nm. Positive coverage stays one; compare every clash against the independent original-coordinate distance oracle |
| Aromatic orientation | 8 | Exact positive center, cached target axis or its negative, evaluated on the rotated/translated candidate under 1/30/60/90-degree tolerances. Compare against the folded axis angle from the independent original-ring plane and declared proper rotation |
| Original-pose contrast | 1 | Untranslated PHE404 is .35 nm from the exact positive query, outside radius .02 nm |
| Exclusion-removal ablation | 1 | Explicitly extract site zero from the .40 nm excluded model with a recorded reason/source map. Removing the veto preserves positive coverage and allows the declared candidate |

Thus each policy has **31 valid fixed-pose settings plus one real invalid-frame
failure**. Execute nm/ps/radians and pm/fs/degrees: **64 attempts per complete
matrix**, no replacement or silently omitted cell. There is no fitting, search,
conformer generation or ranking; search budget is zero. The angular hypotheses
remain separate models, rather than simultaneous essential alternatives.

## Independent oracles and accounting

The guard computes its original-ring center and plane from frozen original
coordinates using test-only mean/SVD arithmetic, independently of the provider's
feature output. The original center is
`[10.3282,1.9207666666666665,2.0210166666666667] nm`.
Expected placements use the declared translations. The angular oracle rotates
the original plane axis with the literal matrix and folds its angle using the
absolute dot product; target-axis reversal is equivalent. Its calculation is
only a test oracle, not a reusable molecular routine in PHMT.

The clash oracle enumerates original selected heavy-atom centers and original
centers plus the fixed translation using `math.dist`, comparing strictly inside
the declared exclusion radius. It preserves exact source/site indices and all
clashes, rather than matching only a count. It does not use evaluator outputs,
copy its assignment implementation or infer a physical van der Waals radius.

Position/plane/unit comparisons use 1e-12 nm/dimensionless. Existing #84 numerical
positive-boundary and angular-slack criteria stay explicit; no physical cutoff
is fitted to these outcomes. Keep missing/failed frames unscored with native
causes, distinct from valid negative poses. Settings reuse one prepared source;
do not pool them as independent molecules or calculate a biological hit rate.

Preserve all native models/results/actual attribution, source coordinates,
complete chemical-state history, cached observations, selection/frame/state,
curation source and restored application unit configuration. Record the actual
loaded derived artifact as input data; no new preparation/detection credit.
Every run retains source/native/test/input identity and original failures.
Unexpected results require investigation, not changing the declared oracle to
obtain a pass.

## Completion and remaining scope

Completion requires the declared transitions and custody checks, full original
evidence, focused existing receptor/sensitivity/exclusion/curation compatibility
and relevant documentation/report/archive controls. Retain all original #52/#83
evidence and declaration bytes. Runtime/provider/prefix/dependency changes are
not proposed for this case.

This closes only a prepared-geometry analytical slice of audit item 12. Real
development cohorts, empirical importance, preparation/search variability and
uncertainty remain. MolSysMT #375/#323, TopoMT pocket generation, #66's original
methods, #74/MolSysMT #215, #82/ArgDigest #47/#48 and broader #6 retain their scope.
Hosted, installed/public/all-platform, full-suite, predictive and performance
qualification are separate. Append measured results after the first execution;
preserve this original protocol text.

## Measured extension — 2026-11-04

The original declaration above remains unchanged. The [recorder](../phmt_test_support/prepared_receptor_sensitivity.py)
and [independent guards](../tests/test_prepared_receptor_sensitivity.py) execute
all 64 attempts; [full original evidence](evidence/prepared_receptor_sensitivity_20261104_summary.json)
retains every run and original source/native/test/input identity. Final selected
scope: 288 passed in 442.24 s, including 43 new controls, zero failures/errors/skips.
The standalone command independently executes the same complete matrix.

Exclusion radii .01/.20/.40 nm produce 0/5/47 clash pairs on 0/3/11 distinct
candidate atoms, respectively, while positive fit stays one. The independent
folded aromatic axis angle is about 36.07 degrees; both axis signs refuse under
1/30-degree tolerance and accept under 60/90. Placement bands and original-pose
contrast agree with the fixed table. Removing the exclusions preserves full
positive fit and records the hypothesis change. No physical optimum is inferred.

All three recorded source/native/test/input checks are stable. Initial pytest
records nine inherited providers; final pytest and CLI also record NumPy/SciPy/
RDKit source/native identity. Initial scope: 41 pass/two fail because the new
history guard assumed the public export tag inside a legacy embedded snapshot.
Only that envelope expectation changes; AST comparison preserves all independent
oracles and every model data field. Recorder/runtime/provider/prefix/dependency
and original expected settings stay unchanged. Actual input and operation credit,
source coordinates/history/cached contacts, native inventories, curation source
and application policy remain intact. Failed frames remain unscored.

Next inspect actual TopoMT pocket and MolSysMT geometry contracts before declaring
an automatic receptor hypothesis-generation pilot. The complete sensitivity/
uncertainty audit, real cohorts, preparation/search variability, #375/#323 and
other named scientific/delivery gates remain independent.
