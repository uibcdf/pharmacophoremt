# Native TYR dual-donor constraints

## Identity, question and preparation

Measured 2026-11-05, owner LMMV/dprada,
[PharmacophoreMT #91](https://github.com/uibcdf/pharmacophoremt/issues/91).
This paired analytical extension of the [PHE contribution study](receptor_contribution.md)
tests native N–H and O–H donor projections, separately and jointly with an
aromatic constraint. It asks how losing either corresponding ligand acceptor,
losing both, or rotating the ring changes fixed-pose compatibility. Two TYR
regions from one prepared ERα fragment are not independent ligands or targets.

The [frozen protocol](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/tyr_cardinality_protocol.md)
and [plan](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/data/tyr_cardinality/plan.json)
have plan SHA-256 `29b62982967e19855c0429716815a2c39f645cea7fd2042be0f86567925aac81`.
The original rule, timestamp and hashes are retained before measurement in the
[receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/tyr_cardinality_20261105_summary.json).
Public MolSysMT inspection finds all five source-ordered TYR groups eligible
for exactly two N/H and O/H donor records and one six-member ring; the first two
are **TYR328/TYR331**. Eligibility evaluates zero hypotheses or poses and retains
all five candidates, source atom maps and unfavorable/missing-input gates.

The unchanged original #52 H5MSM has SHA-256
`a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a`.
[Original input provenance](prepared_receptor_workflow.md#inputs-and-preparation)
owns acquisition, redistribution, chemistry and preparation limits. Frame zero,
reference chemistry and the original unrefined donor hydrogens remain unchanged;
no new interaction detection, pH preparation, activity labels or holdout is used.

MolSysMT owns source loading, representations, selections, recognition, coordinates,
vectors/planes, construction, transforms and merge. It builds disconnected
O/O/benzene witnesses with O centers projected .35 nm along the native N–H/O–H
directions and the ring translated .35 nm along its cached normal. Candidate
atom order, exact native acceptor/ring records and source/candidate maps are
checked before evaluation. These are geometric witnesses, without a realizable
ligand or optimized conformation claim. PHMT composes its existing generation,
matching and native persistence tools; no production API or provider is changed.

## Execution and independent controls

Each region and physical policy uses donor-only, ring-only and joint queries
with .35 nm distance choices, .02 nm radius, one-degree angular tolerance,
minimum fit one and budget two. All sites are essential, weight one. The existing
`donor_aromatic_faces` profile explicitly omits the native position-only source
acceptors. There are no exclusions, parameter fitting or budget sweeps here.
Both physical policies (nm/ps/radians and pm/fs/degrees) use identical data.

Five candidates are intact, only the N-target O, only the O-target O, ring-only,
and both O with a ring rotated 90 degrees about its provider-derived center.
The fixed proper rotation matrix is selected by the least absolute component
of the cached normal, with x/y/z tie order. The source-coordinate oracle checks
every query/candidate center and axis at 1e-12 nm/unit; test-only D→H normalization,
ring mean/SVD and exhaustive small injective assignment enumeration are independent
of the runtime matcher. All optimal typed geometric assignments are admitted;
neither N/O-specific slot restrictions nor one Hungarian tie order is assumed.

From the qualified source environment:

```bash
python -m phmt_test_support.tyr_cardinality --output /path/to/result.json
python -m pytest devtools/tests/scientific/test_tyr_cardinality.py tests/test_tyr_cardinality_plan.py --receptor=llm
```

These explicit scientific commands are separate from lightweight default
plan/evidence tests. The source-only driver reuses #90's unchanged cell executor.
The receipt retains actual CLI argv and Linux/Python 3.14.7 identities for twelve
loaded providers, Python/native source bytes, helper/test/input and distribution
metadata. It uses controlled MolSysMT `0faf1584d05ac47ddcebfc20d9c9978b7f4f230e`
and public ArgDigest 0.17.0 extraction. This is controlled source evidence;
installed/public delivery, full-suite and platform qualification remain separate.

## Measured results

All **12 cells, 20 models, 100 primary and 24 JSON/YAML recovery evaluations**
complete with no calculation failure or unscored primary slot. Both regions and
policies give the same fixed fit arrays. Source coordinates, complete chemistry/
history, original cached observations, inventories, candidates and application
units remain intact. Every representative native roundtrip preserves geometry
and scientific outcomes at the prespecified physical tolerance.

| Candidate | Donor-only fit | Ring +/− fits | Joint +/− fits |
| --- | --- | --- | --- |
| Intact | 1 | 1, 0 | 1, 2/3 |
| Only N-target O | 1/2 | 1, 0 | 2/3, 1/3 |
| Only O-target O | 1/2 | 1, 0 | 2/3, 1/3 |
| Ring only | 0 | 1, 0 | 1/3, 0 |
| Both O, rotated ring | 1 | 0, 0 | 2/3, 2/3 |

Only fit one without missing essentials is accepted. The joint query rejects
controls accepted by either single-family query. Losing one O is a valid negative
with partial fit, not a failed calculation. Fractions with different site
denominators do not establish relative model quality or affinity.

Every assignment agrees with the independent injective optimum. The two projected
donor targets are separated by approximately 1.288 nm (TYR328) and .746 nm (TYR331),
well beyond the .02 nm matching radius. Consequently this study does **not**
isolate record-reuse prevention for overlapping sites: geometry alone already
prevents one O filling both targets. The dedicated existing
[one-to-one guard](https://github.com/uibcdf/pharmacophoremt/blob/main/tests/test_pose_evaluation.py)
owns that synthetic overlapping-site mechanism. At-most-one capacity concerns
typed feature records, rather than a prohibition on multifunctional atoms.

## Attempts, attribution and evidence

The receipt links the untouched complete scientific JSON gzip and a separate
source/log/guard archive. Model metadata stored once per model by the shared
cell executor reconstructs every evaluator response with its outcome/model_index.
All original code, commands, eligibility output, snapshots and failed attempts
remain available with compressed, uncompressed and inner-file hashes.

The initial twelve-control selection has eight passes and four oracle failures:
the new oracle reads a sphere's nonexistent normal while examining an incompatible
ring record. Checking type and distance before orientation fixes only the guard.
The original full CLI and optional-provider simulations already completed. A
result/unchanged-driver/frozen-plan-bound reanalysis passes ten controls; the two
unchanged optional controls retain their original passing evidence. No driver,
plan, molecular input, model or measured output is changed or rerun to repair
that test-envelope defect. The existing overlapping-site one-to-one guard also
passes separately. All four phase before/after identities are stable.

A single enclosing PHMT attribution boundary retains the original prepared-data
credit and methods actually reached, without per-operation bibliography expansion.
The original real provider capture is stored; absence and failure simulations
each complete a separate two-model subset (10 primary plus two recovery calls)
with the declared fits. They do not establish a fresh uninstalled-provider or
all-platform qualification. Reading the archive does not register new usage.

## Limits and maintenance

This extends the declared source slice from PHE to native TYR N/O donors. It does
not establish chemical realizability, optimal offsets, physical accessibility,
biological essentiality, energetic importance, activity, affinity, uncertainty,
target breadth or prospective enrichment. Original H placement remains an
assumption. Timing and memory performance are not measured; replay counts are
not biological sample sizes.

Reexecute after input/provider, generation, matching, persistence, helper or case
changes. New scientific choices need a dated declaration before evaluation,
preserving this original run. Further MolSysMT acceptor directions #375 require
their own exact-provider/input receiving and independent angular controls;
environmental H refinement #323, optional pockets, audit12/15, biological #66,
ArgDigest receiving #82, SDF #74/#215 and hosted/installed/public #9/#23 retain
separate gates. Addon and release work remain deferred; no new package is claimed.
