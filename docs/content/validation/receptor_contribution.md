# Receptor constraint-contribution comparison

## Identity, question and input

Measured 2026-11-05, owner LMMV/dprada,
[PharmacophoreMT #90](https://github.com/uibcdf/pharmacophoremt/issues/90).
This is a paired analytical development study on one historically prepared
ERα fragment, using PHE337/367/404. It asks how donor, ring and joint constraints,
excluded volumes, positional tolerance and finite enumeration change geometric
compatibility with fixed controls. These are not independent ligands, targets,
biological replicates or affinity/activity evidence.

The [frozen protocol](https://github.com/uibcdf/pharmacophoremt/blob/1ce8d31763d54dee4b9cc0efa0ce6e6c97a00384/devguide/receptor_contribution_protocol.md)
and [explicit plan](https://github.com/uibcdf/pharmacophoremt/blob/1ce8d31763d54dee4b9cc0efa0ce6e6c97a00384/tests/data/receptor_contribution/plan.json)
predate evaluation. SHA-256 is
`4358f73bf84aa334bf1b69822558860bc1f7cc6c0c071c1ad0dcc58978923981`.
A separate source-order eligibility audit selected three regions from all seven
eligible PHE groups, before any pose result. The unchanged #52 native input has
SHA-256 `a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a`;
[the original case](prepared_receptor_workflow.md#inputs-and-preparation) retains
acquisition, redistribution, source maps, chemistry and preparation limitations.
No new preparation, H refinement, detector run, activity labels or holdout is used.

MolSysMT owns loading, selection, recognition, coordinates, vectors/planes,
construction and transforms. The seven-heavy-atom disconnected O/benzene witness
uses source coordinates and declared provider translations/rotations. It is a
methodological geometry control without a realizable ligand/conformer claim.
PHMT composes existing public feature, generation, fixed-pose and persistence tools.
All positive sites are essential/weight one; exclusions have zero positive weight.
Uniform radii are explicit query choices, without physical-radius assignment.

## Execution and independent controls

Six paired variants compare donor-only, ring-only, joint, and joint plus
.01/.20/.40 nm exclusions. The same five candidates per region/policy are intact,
O-displaced, ring-displaced, both-displaced and ring-rotated. Base query radius
is .02 nm, direction tolerance one degree and budget eight. Separate joint-only
blocks use .08/.12 nm tolerance or 3/0 budget. Both physical unit policies
(nm/ps/radians and pm/fs/degrees) use the same molecular data and settings.

Independent original-coordinate D→H normalization and ring mean/SVD verify every
query/candidate geometry at 1e-12 nm/unit. All strict-inside pairs are enumerated
independently with math.dist, preserving exact source/candidate/global indices.
Every positive-fit array is checked against the frozen declaration. Essential
sites, complete/truncated/zero enumeration, failures and unscored slots remain
separate. No fitting, ranking, pose optimization or molecular geometry kernel
is implemented in the case runner.

From the qualified source checkout/environment:

```bash
python -m phmt_test_support.receptor_contribution --output /path/to/result.json
python -m pytest devtools/tests/scientific/test_receptor_contribution.py tests/test_receptor_contribution_plan.py --receptor=llm
```

These are explicit scientific reexecution commands. The ordinary pytest profile
keeps lightweight plan/evidence controls; it does not repeat this large experiment
on every push. The unshipped driver is not an installed public package command.
The receipt retains exact executed argv/environment and Linux/Python 3.14.7
source/native/helper/test/input/metadata identities, including controlled MolSysMT
`0faf1584d05ac47ddcebfc20d9c9978b7f4f230e` and public ArgDigest 0.17.0 extraction.
This is not clean installed/public/all-platform or full-suite qualification.

## Measured outcomes

All **60 generation cells, 342 models, 1,710 primary and 108 recovery evaluations**
complete. Six zero-budget cells retain 30 unscored candidate slots. Source
coordinates, complete chemical history, original cached observations, inventories,
candidates and application units remain intact. Both policies give identical
fits, acceptance and clash-pair counts. Real input/operation credit is retained.

Donor-only queries also accept the displaced/rotated-ring controls; ring-only
queries also accept displaced O. Joint queries accept only the intact control
before exclusions, demonstrating complementary restrictions for this design.
A partial fit of .5 with a missing essential is rejected. This does not establish
binding importance or superiority across different constraint denominators.

For the intact fully positive joint reference, both unit policies give:

| Region | Exclusion radius (nm) | Positive fit | Clash pairs | Outcome |
| --- | --- | --- | --- | --- |
| PHE337 | .01 | 1 | 0 | Matched |
| PHE337 | .20 | 1 | 2 | Vetoed |
| PHE337 | .40 | 1 | 33 | Vetoed |
| PHE367 | .01 | 1 | 0 | Matched |
| PHE367 | .20 | 1 | 0 | Matched |
| PHE367 | .40 | 1 | 20 | Vetoed |
| PHE404 | .01 | 1 | 0 | Matched |
| PHE404 | .20 | 1 | 0 | Matched |
| PHE404 | .40 | 1 | 21 | Vetoed |

Positive fit stays one while exclusions can veto acceptance. The .20 nm choice
is region-dependent in this controlled geometry; neither favorable nor unfavorable
results are removed or used to select a radius. These are selected heavy-center
vetoes, not whole-pocket steric accessibility or van der Waals overlap.

Joint tolerances .02/.08/.12 nm admit 1/2/4 fully positive hypotheses out of eight.
Budgets three/zero omit the compatible index-four hypothesis and remain explicitly
incomplete; neither is an exhausted negative search. JSON/YAML recover all 54
selected representative models (108 roundtrips) and their scientific outcomes.

## Attempts, attribution and original evidence

The [receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/receptor_contribution_20261105_summary.json)
links the untouched complete scientific result gzip and a separate archive of
original code, logs, sources, guards and supplemental outputs, with byte hashes.
Repeated evaluation model metadata is stored once per model as
`evaluation_model_metadata`; each outcome's model_index/result reconstructs the
complete original evaluator response. Nothing is replaced by declared answers.

The first 28-control selection has 27 passes and one new guard failure: a native
roundtrip changes an assignment distance from zero to 2.22e-16 nm, so literal
QuantityRecord/digest equality is inappropriate. Comparing physical distances
at the already declared 1e-12 nm tolerance corrects only that guard. Other
assignment fields and scientific statuses stay exact. A first saved-result
reanalysis misses a Path import; its original failure is preserved and corrected.
Final source/plan/result-bound reanalysis passes 26 controls. Two unchanged
optional-availability/failure controls pass in both earlier attempts. Their
supplemental replays remain separate from the main 1,710/108 workload.

No model, molecular input, driver, radius, expected transition or scientific
output changes during those corrections. Recorded validation is bound to the
original result hash, unchanged driver hash and frozen plan hash; it is not a
second molecular measurement. Dataset/operation references reflect actual usage,
with no new preparation or interaction-detection credit. Provider-unavailable/
failure simulations preserve science; they are distinct from a fresh uninstalled
provider/platform qualification.

## Limits and maintenance

This establishes the declared numerical/composition/robustness behavior on three
PHE regions of one prepared protein. It does not establish chemical realizability,
physical accessibility, optimal parameters, causal importance, binding affinity,
predictive uncertainty, target breadth or biological accuracy. No timing/memory
benchmark or statistical sample-size claim applies.

Reexecute after input/fixture, provider, query generation, matching, exclusion,
persistence or case-driver changes. New scientific choices require a dated
amendment before evaluation; preserve this original run. Wider chemistry or
preparation sensitivity needs a separate declaration; biological #66,
ArgDigest receiving #82, molecular ownership #74/#215, provider #375/#323,
optional TopoMT #101 and hosted/installed/public #9/#23 retain separate gates.
