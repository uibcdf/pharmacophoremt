# Carbonyl acceptor directions in explicit receptor hypotheses

## Identity, question and original inputs

Measured 2026-11-05, owner LMMV/dprada,
[PharmacophoreMT #93](https://github.com/uibcdf/pharmacophoremt/issues/93).
This analytical source receiving study asks whether MolSysMT's two experimental
carbonyl directions can supply separate explicit ligand-donor pharmacophores,
preserving source/structure correspondence, geometry, units and missing outcomes.

The [protocol](https://github.com/uibcdf/pharmacophoremt/blob/b934471ac8ab8bdb1bd7646550ac23baeb07daa7/devguide/carbonyl_acceptor_receiving_protocol.md)
and [literal input/matrix](https://github.com/uibcdf/pharmacophoremt/blob/b934471ac8ab8bdb1bd7646550ac23baeb07daa7/tests/data/carbonyl_acceptor_receiving/plan.json)
predate execution. Plan SHA-256 is
`b0af26640c0b7ff6cadde2c7f7e499141921adc29fd2ec7f4c1666218be92340`.
The [original declaration receipt](https://github.com/uibcdf/pharmacophoremt/blob/b934471ac8ab8bdb1bd7646550ac23baeb07daa7/devguide/evidence/carbonyl_acceptor_plan_20261105_summary.json)
retains zero new molecular evaluations in #92; its historical claims remain.

Inputs are locally declared methodological fixtures, rather than downloaded
biological data: neutral aldehyde `CC=O`, two explicit coordinate frames in nm,
and indexed donor `[2H]O` witnesses. The second carbonyl frame is a fixed proper
90-degree z rotation and (.4,.5,.6) nm translation of the first. Reference
chemistry and `pbc=False` are explicit. Source structures [0,1,0] retain repeated
positions. Selecting only acceptor O2 keeps its external support [2,1,0].
No chemical preparation, H addition/refinement, observed-interaction detection,
activity labels or holdout is introduced.

Public MolSysMT owns representations, SMILES conversion, coordinate insertion,
selection, recognition, directions, construction, rotations and translation.
PHMT reads its cached result and composes existing explicit projections,
fixed-pose evaluation and native persistence. The unshipped runner computes no
molecular bond direction, plane, recognition rule or alignment kernel. This
does not change the default position-only acceptor inventory or the public
`donor_aromatic_faces` generation profile.

## Scientific choices and independent acceptance

MolSysMT's `ideal_local_geometry`/`smarts_donor_acceptor` result has experimental
schema `molsysmt.hbond_site_directions@1`. Original provider contract/API/model/test
bytes are bound to the reviewed clean source. Receiving checks source anchor,
role/model/status codes and meanings, full CSR support, ordered repeated structure
position, local multiplicity, finite unit vectors, physical origins and zero
nonperiodic image packing. Unsupported/undefined and operational failures remain
distinct; a finite donor vector cannot be substituted for a missing acceptor.

Each carbonyl lobe generates a **separate one-site ligand-donor hypothesis**
using `from_receptor_projections`. The .35 nm offset, .02 nm positional radius,
one-degree donor tolerance, minimum fit one, essentiality and weight one are
explicit PHMT choices. Target D→H axis -u is a declared hypothesis orientation,
where u is the selected provider lobe. Neither the offset nor that ligand
orientation is inferred as a provider chemical or electronic result.

Each lobe's indexed donor witness is aligned, reversed at the same center, or
displaced .10 nm along z. Public MolSysMT applies the declared transformations.
The test-only oracle independently derives ideal carbonyl axes from the original
literal coordinates and checks every provider/query/candidate geometry at
1e-12 nm/unit. It independently evaluates positional and angular compatibility,
source maps, exact fit arrays, missing essentials and assignments. JSON/YAML
geometry and assignment distances use the same 1e-12 physical tolerance; other
assignment fields and provenance stay exact.

## Execution and environment

From the qualified source checkout/environment:

```bash
python -m phmt_test_support.carbonyl_acceptor_receiving --output /path/to/result.json
python -m pytest devtools/tests/scientific/test_carbonyl_acceptor_receiving.py tests/test_carbonyl_acceptor_plan.py --receptor=llm
```

These are explicit scientific reexecution commands; ordinary tests retain cheap
declaration/evidence checks. The driver is not an installed public package API.
The [measured receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/carbonyl_acceptor_receiving_20261105_summary.json)
links the exact executed CLI argv, untouched scientific JSON, source/log archive
and before/after source/native/helper/test/input/distribution-metadata identities.
Actual execution uses Linux/Python 3.14.7, controlled MolSysMT
`0faf1584d05ac47ddcebfc20d9c9978b7f4f230e` and public ArgDigest 0.17.0 extraction.
This is source receiving, without a clean installed/public/platform claim.

## Measured results

Both physical policies (nm/ps/radians and pm/fs/degrees) and all three requested
source positions agree. **Six blocks, 12 models, 72 primary evaluations and
24 JSON/YAML recovery evaluations complete.** Two positive provider direction
calls preserve the repeated source axis; four additional negative source queries
produce no usable model or pose score.

| Candidate | Hypothesis0 fit | Hypothesis1 fit |
| --- | --- | --- |
| Lobe0 aligned | 1 | 0 |
| Lobe0 reversed | 0 | 0 |
| Lobe0 displaced | 0 | 0 |
| Lobe1 aligned | 0 | 1 |
| Lobe1 reversed | 0 | 0 |
| Lobe1 displaced | 0 | 0 |

All assignments use the original indexed donor O1/D0. Fit one is accepted;
zero fit is a valid evaluated negative. Each hypothesis contains one essential
site; the two lobes are not simultaneous constraints on one ligand donor.

Water's observed donor has role0/model1/status1 and one direction, while its
recognized acceptor has role1/model0/status0 and no direction. Collinear carbonyl
remains model2 with status2 undefined geometry and no direction. Both acceptor
cases remain unscored. Operational and malformed-cache controls fail explicitly
without a local repair or alternate model.

Complete source coordinates, chemistry/history, analyses, provider caches,
native inventories, candidates and application units remain intact. All native
roundtrips preserve geometry, original model/provider evidence and outcomes.
The two physical policies and repeated frames are replays, not independent
chemical or biological samples.

## Attempts, provenance and actual attribution

The first selection has nine passes, two failures and 26 fixture errors: the new
runner passes the protocol's descriptive unit map directly to a PyUnitWizard API
that accepts a list. It stops before any direction/model/pose calculation and
produces no full scientific result. Preserve the original source, logs and XML.
Converting the same declared map values to the required list fixes only that
adapter. Frozen scientific inputs/protocol/settings/predictions remain unchanged.

The corrected **37-control selection passes**, comprising 29 scientific/receiving
controls and eight offline declaration guards. Both phase identity comparisons
are stable. Two optional attribution absence/failure simulations each complete
their separate first block: two models, 12 primary/four recovery calls. They
retain the fixed answers; they do not qualify a fresh uninstalled provider.

Real capture preserves executed software, recognition, direction-model,
projection and evaluator references. The provider's reviewed RDKit source is
labeled `geometric_inspiration`, separately from executed software. No paper
is credited as proving this numerical profile or an energetic optimum. Local
literal inputs do not earn the unrelated prepared-ERα dataset credit. Reading
stored evidence does not register another calculation.

Full provider values, array shapes/dtypes, physical quantities and detached
provenance remain in the original output. Evaluator model metadata is stored
once per model alongside its indexed outcomes; together they reconstruct each
original response. Original #89–#92 scientific declarations/results remain.

## Limits and maintenance

This establishes the declared mechanical receiving/projection behavior for one
ordinary neutral aldehyde geometry and analytical donor controls. It does not
qualify other carbonyl environments, nitrogen/other acceptor models, PBC,
protonation, environmental H, electronic orbitals, energetic optima, physical
accessibility, ligand binding, affinity, activity, target breadth or performance.

Reexecute after the source/input/provider, receiving, projection, matching,
persistence or case changes. New scientific choices require a dated declaration
before evaluation and a distinct result identity. Public cached-acceptor contract
design is subsequent work; this case does not promote a production/default
profile or dependency floor. MolSysMT #375/#323, broader audit12/15,
#66/#82/#74/#215, optional pockets and hosted/installed/public #9/#23 retain
their separate acceptance gates. Addon/release remain deferred.
