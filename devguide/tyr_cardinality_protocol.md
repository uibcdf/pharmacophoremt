# Prespecified native TYR donor-cardinality study

Owner LMMV/dprada, [#91](https://github.com/uibcdf/pharmacophoremt/issues/91),
2026-11-05. Freeze [the matrix](../tests/data/tyr_cardinality/plan.json) before
new hypotheses or poses. This extends #90's PHE controls to native N/O donor
chemistry using the existing `donor_aromatic_faces` profile, without a new API.

## Question and source selection

Can one native acceptor record fill two essential projected acceptor sites?
How does the joint donor/aromatic query behave when a candidate lacks either
acceptor, lacks both, or has an unfavorable ring orientation?

Use original #52 H5MSM, SHA-256
`a42ef9868578ba16c62d52a1267d24160b973dca0d50dbc804ca46b6b2fe316a`,
frame zero/reference chemistry. The [original case](../docs/content/validation/prepared_receptor_workflow.md)
owns input acquisition, redistribution, preparation and unrefined-H limits.
No new chemistry preparation, H refinement or interaction detection is performed.

The [rule](../tests/data/tyr_cardinality/eligibility_rule.json), frozen before
inspection, requires exactly two explicit donor–H records with provider-declared
N/H and O/H elements, and one six-membered aromatic record. Audit every TYR in
source order through public MolSysMT and retain the first two eligible groups.
If fewer than two qualify, block this design rather than change the chemistry.
The [actual eligibility ledger](../tests/data/tyr_cardinality/eligibility.json)
finds five eligible groups and retains **TYR328/TYR331**. No model or pose has
been evaluated during eligibility. Preserve every candidate and source atom map.

## Fixed queries and five common candidates

Use the same native whole-region selection for donor-only, ring-only and joint
inventories. Joint includes native position-only acceptors; the profile must
explicitly omit them. Select one .35 nm donor distance and one .35 nm aromatic
distance, with separate +/− faces, .02 nm matching radius, one-degree angular
tolerance, minimum fit one and budget two. All positive sites are essential and
weight one. No excluded volume, radius fitting or budget sweep is introduced.
Complete hypothesis counts per region/policy are 1/2/2, with 2/1/3 positive sites.

Create one O component at each original N/O donor position and one benzene
component at the original indexed ring coordinates through public MolSysMT
SMILES conversion/native coordinate insertion. Public MolSysMT translates each
O by .35 nm along its cached donor–H vector, and the ring by .35 nm along its
cached positive normal. Merge the chosen components in N-target O, O-target O,
ring order, retaining source provenance separately from candidate indices.
This disconnected witness is an analytical control without a realizable-ligand
or optimized molecular-geometry claim.

Use these identical candidates across all three paired query variants:

1. `intact`: both O components plus ring, eight heavy atoms.
2. `nitrogen_target_only`: only the N-target O plus ring, seven heavy atoms.
3. `oxygen_target_only`: only the O-target O plus ring, seven heavy atoms.
4. `ring_only`: no O component, six heavy atoms.
5. `ring_rotated`: both O components and a 90-degree rotated ring, same centers.

The rotation uses the three fixed proper Cartesian matrices from the plan,
choosing the least absolute component of the cached normal (ties x/y/z), about
the provider-derived candidate ring center. Public MolSysMT applies it. Its
unoriented-axis cosine is at most 1/3, outside the one-degree tolerance.
Preflight exact candidate atom order, native acceptor count and ring membership;
an unexpected recognition result is a failed preflight, not a reason to invent
or duplicate feature records. Source positions, types, recognition, vectors,
planes, construction, transforms and merge remain MolSysMT-owned.

## Independent predictions and workload

The two projected acceptor sites have the same ligand feature kind. Native
candidate identity does not force N/O-specific pairing; any geometrically valid
injective assignment is allowed. A single record can fill at most one site.

| Candidate | Donor-only fit | Ring +/− fits | Joint +/− fits |
| --- | --- | --- | --- |
| intact | 1 | 1, 0 | 1, 2/3 |
| nitrogen_target_only | 1/2 | 1, 0 | 2/3, 1/3 |
| oxygen_target_only | 1/2 | 1, 0 | 2/3, 1/3 |
| ring_only | 0 | 1, 0 | 1/3, 0 |
| ring_rotated | 1 | 0, 0 | 2/3, 2/3 |

Missing any essential remains a valid negative even with partial positive fit.
Cardinality and geometry contribute separately; fractions across models with
different site denominators do not measure affinity or relative model quality.

Tests independently normalize original D→H vectors and use ring mean/SVD,
aligning only the unoriented-axis sign convention to the provider. Compare all
query/candidate centers and normals at 1e-12 nm/unit. Exhaustively enumerate small
typed injective assignments from original-coordinate predictions, preserving
all optimal alternatives rather than assuming one Hungarian tie-break order.
Check reported assignments belong to that optimum, every declared fit, missing
essentials and complete enumeration. These test-only oracles are not molecular
or matching kernels in the runtime/experiment driver.

Two regions × two physical policies × three variants give **12 cells, 20 models
and 100 primary pose evaluations**. Both policies (nm/ps/radians, pm/fs/degrees)
are equivalent replays. Recover the first fully positive intact model in every
cell through JSON/YAML and reevaluate intact: 24 further evaluations. Compare
native geometry/derived distances physically at 1e-12 nm, keeping other fields
exact; opaque quantity digests need not remain identical after float roundtrip.

Preserve source coordinates, complete chemical history, original cached
observations, native inventories, candidates and application units. Retain all
failures distinctly, actual input/operation attribution and source/native/helper/
test/input/distribution-metadata identities. Provider failure/absence must not
erase scientific outcomes. Do not tune parameters or change predictions after
seeing results; an amendment needs a dated new identity and preserved old output.

## Scope and execution route

Reuse #90's pharmacophore cell execution/persistence helpers and existing public
PHMT operations; only new case orchestration and independent guards are needed.
Heavy scientific reexecution stays explicit; routine artifact/plan guards remain
cheap. The result/commands/evidence will be published separately after execution;
all counts/predictions above are prospective at declaration.

This is two TYR regions on one prepared protein, no independent biological
ligands, activity labels or holdout. Native donor presence does not establish
importance or justify essentiality biologically. No physical-accessibility,
optimal-offset, binding, pH, energetic, target-breadth or performance claim follows.
Ideal acceptor directions (#375), environmental H refinement (#323), optional
pockets, #66/#82/#74/#215 and hosted/installed/public #9/#23 remain separate.
