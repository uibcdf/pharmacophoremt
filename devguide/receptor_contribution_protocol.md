# Prespecified receptor constraint-contribution study

Owner LMMV/dprada, [#89](https://github.com/uibcdf/pharmacophoremt/issues/89),
2026-11-05, following #87/#88 and audit items 12/15. This deliverable freezes the
protocol and [explicit matrix](../tests/data/receptor_contribution/plan.json).
**Comparison outcomes have not been measured.** Workloads and fit arrays below
are prospective analytical expectations, not executed results or validation.

## Question, input and eligible regions

How do donor, aromatic and joint constraints, optional exclusions, positional
tolerance and finite enumeration change compatibility with controlled candidates?
This is a paired analytical development study on one historically prepared
protein fragment. It does not estimate biological importance or predictive accuracy.

Use the original #52 H5MSM, native SHA-256
`a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a`,
frame zero/reference chemistry. Original provenance, redistribution sources,
304–550 fragment boundaries, excluded residues, HIE/terminal choices and local
hydrogen limitations remain in [the original case](../docs/content/validation/prepared_receptor_workflow.md).
No new preparation, detector run or environmental H optimization is prescribed.

Before generating/evaluating any new model, freeze [the eligibility rule](../tests/data/receptor_contribution/eligibility_rule.json):
inspect every PHE in source order through public MolSysMT. Require one indexed
donor–H pair, one six-membered aromatic record and a compatible nonempty singleton
heavy inventory. Retain PHE404 plus the first two other eligible groups; block
the design if unavailable. Do not substitute from favorable pose results.

The executed [eligibility ledger](../tests/data/receptor_contribution/eligibility.json)
records seven eligible groups: 337, 367, 404, 425, 435, 445, 461. It deterministically
retains **337, 367, 404**, each with one donor–H, one ring, one position-only
acceptor and eleven heavy records. The actual source/producer/operation evidence
is retained separately from future comparison results in
[the prespecification receipt](evidence/receptor_contribution_plan_20261105_summary.json).

| Region | Donor–H source atoms | Six ring source atoms |
| --- | --- | --- |
| PHE337 | 251, 2223 | 256–261 |
| PHE367 | 486, 2461 | 491–496 |
| PHE404 | 791, 2772 | 796–801 |

These are three regions of one input and one residue chemistry. Neither the
regions, unit replays, hypotheses nor perturbations are independent ligands or
biological replicates. Holdout access and activity-label counts are zero.

## Shared query choices and paired variants

Use public `get_features` with the same whole-region selection/frame/state for
chemical and heavy inventories. Request the family's features explicitly; the
joint request includes acceptors, whose omission must remain reported. Call
public `from_receptor_features` with profile `donor_aromatic_faces`, donor choices
.28/.35 nm, aromatic choices .35/.45 nm and separate +/− faces, in that order.
Every positive site is essential and weight one; exclusions have weight zero.
The source order is donor, position-only acceptor, ring. Preserve local-to-source
indices when the single-family inventories have different feature-list indices.

| Variant | Positive constraints | Exclusion radius | Complete hypothesis count |
| --- | --- | --- | --- |
| donor | Ligand acceptor from receptor donor | None | 2 |
| ring | Aromatic disk on either face | None | 4 |
| joint | Both | None | 8 |
| joint_ex01 | Both | .01 nm | 8 |
| joint_ex20 | Both | .20 nm | 8 |
| joint_ex40 | Both | .40 nm | 8 |

Base positional matching radius is .02 nm, direction tolerance one degree,
minimum fit one and budget eight. Distances/radii are declared query choices,
without physical-radius assignment, optimization or energetic ranking.
Exclusions do not prune generation or change positive weights/enumeration.

## Five common analytical candidates

Construct a disconnected O/benzene witness through public MolSysMT SMILES
conversion, native coordinate insertion, translation and merge. Do not import
RDKit directly or add a molecular constructor/parser/geometry kernel here.
Use the original indexed donor coordinate for O's starting point and original
six ring coordinates for benzene, obtained through MolSysMT. Translate O by
.35 nm along the cached donor–H direction and benzene by .35 nm along the cached
positive ring normal. Preserve candidate atom order: O first, then six carbons;
require seven heavy atoms, no explicit H, one recognized acceptor and one ring.
An unexpected recognition result is a failed preflight, not a reason to edit
the candidate or expected answer silently. This witness is not a chemical ligand.

Create the five controls once per region/unit policy and reuse identical
candidate inputs across all paired query variants:

1. `intact`: the two components at those declared positions.
2. `donor_displaced`: translate only O by [1,0,0] nm through MolSysMT.
3. `ring_displaced`: translate only benzene by [1,0,0] nm.
4. `both_displaced`: translate both components by [1,0,0] nm.
5. `ring_rotated`: retain both centers; rotate benzene 90 degrees about the
   Cartesian axis least aligned with its cached normal, ties x/y/z. Choose among
   the three fixed proper matrices in the plan and apply public MolSysMT `rotate`
   about its provider-derived ring center. The unoriented-axis cosine is at most
   1/3, hence its mismatch exceeds one degree. This is a control choice, not a
   molecular direction-inference implementation.

MolSysMT owns every molecular read, selection, recognition, center/plane/vector,
construction, coordinate operation and merge. PHMT owns projection choices,
query composition, fixed-pose matching and interpretation. Missing provider
capabilities must be reported to their owner; do not substitute a local kernel.

## Independent expectations and endpoints

Check generated centers against test-only original D→H normalization and ring
mean/SVD; compare axes up to sign and physical geometry within 1e-12 nm/unit.
This arithmetic is an independent oracle, never a molecular implementation in
the experiment driver or runtime. Check all source maps and individual sites.

The one O acceptor and one ring have distinct kinds, giving an unambiguous
one-to-one assignment. A donor offset matches intact O when |d−.35| is within
the query radius. An unrotated ring matches when its face is positive and
|r−.35| is within that radius. A displaced component is at least .2 nm from any
declared compatible center, beyond even the largest .12 nm matching radius.
The exact prospective arrays for every returned model/control are in the plan.

At .02 nm, intact donor/ring/joint variants have respectively one fully positive
hypothesis among 2/4/8. Joint fit counts are 3 at zero, 4 at .5 and 1 at one.
Displacing O removes its contribution; displacing/rotating the ring removes its
contribution. Fit .5 with a missing essential is not acceptance. Fewer constraints
can admit more controls; that is not evidence of a scientifically superior model.

For every excluded model, independently enumerate ALL candidate-heavy/source-heavy
strict-inside pairs with original coordinates, declared public transformations
and `math.dist < radius`. Compare exact candidate/source/global indices, not a
fitted count. Radius equality is permitted. Exclusions preserve positive fit
but may veto acceptance. Do not presume zero collisions at .01/.20 nm. At .40 nm
the fully positive intact reference has at least seven self-corresponding pairs:
O and the six carbons each moved .35 nm from an included source heavy center.
Source-context declarations alone do not authenticate cache identity or coverage;
the execution must check original input/custody and the ledger explicitly.

Per cell/control report actual assignments, fit, missing essentials, full clash
pairs and status for every returned hypothesis. Aggregates retain best positive
fit, any acceptance, fully positive/vetoed counts, failed attempts and completion.
Fit denotes geometric coverage, never affinity. Do not conflate different site
denominators or call an any-compatible result energetic ranking. Failed source,
recognition, generation or evaluation operations stay distinct from valid negatives.
An aggregate with failures is partial; zero-budget controls are unevaluated,
not scored zero or exhausted negatives.

## Separate sensitivity blocks and planned workload

The baseline is a complete paired 3 regions × 2 policies × 6 variants.
Use nm/ps/radians and pm/fs/degrees; these are the same physical inputs.
Add only two prespecified blocks on the joint no-exclusion variant:

- Matching radii .08/.12 nm, budget eight: intact joint fully positive counts
  are 2/4 of eight, compared with one at .02 nm. No cutoff is selected from this.
- Budgets three/zero at .02 nm: total eight, remaining five/eight, incomplete.
  The intact compatible hypothesis is index four and omitted by either prefix.
  This is a controlled opportunity loss, not a negative exhaustive search.

| Block | Generation cells | Returned models | Primary pose evaluations |
| --- | --- | --- | --- |
| Baseline | 36 | 228 | 1,140 |
| Tolerance | 12 | 96 | 480 |
| Budget | 12 | 18 | 90 |
| Total planned | 60 | 342 | 1,710 |

Six zero-budget cells additionally retain 30 unevaluated cell/control slots.
For each of 54 nonempty cells, recover the first fully positive intact model,
or the first returned model if none qualifies, through JSON/YAML: 108 roundtrips
and 108 additional intact post-recovery pose evaluations. Choose by positive fit,
not favorable exclusion acceptance. Preserve all native content; compare physical
geometry at 1e-12 and other fields exactly, retaining actual operation attribution
separately from scientific equivalence. All counts here are planned workloads.

## Execution handoff, custody and scope

The execution driver and its measured comparison are the next deliverable; no
operational command for that future driver is claimed here. The current guard is:

```bash
python -m unittest discover -s tests -p test_receptor_contribution_plan.py
```

Before execution verify the plan/ledger/rule hashes in the receipt. Record exact
driver, source/native-extension, helper/test/input/distribution-metadata identities
and all commands/attempts. Preserve original coordinates, full chemical history,
cached hydrophobic/H-bond/pi observations, native inventories and application units.
Capture only actually used derived input and reached method/software references;
no new preparation/detection or borrowed literature claim follows. Optional
attribution absence/failure must preserve scientific outcomes.

Retain complete actual outputs, expected-versus-observed comparisons, all failures
and denominators. Changing any region, candidate, parameter, budget, oracle or
exclusion rule requires a dated amendment/new identity before rerunning; preserve
this declaration. Do not tune parameters to force a match or consult a holdout.
Future unexpected source/API behavior belongs in the provider's issue when reusable.

No inference about physical accessibility, binding importance, affinity,
uncertainty across targets, statistical efficacy, optimal radii or computational
performance is planned. No timing/memory benchmark or new preparation variant is
included. Broader audit12/15, #66, #82, MolSysMT #375/#323, optional TopoMT #101,
SDF #74/#215 and #9/#23 hosted/installed/public gates remain independent. This
stage changes no production API, molecular routine, dependency floor/pin or release.
