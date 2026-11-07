# Fresh versus reused feature inventories

Owners LMMV/dprada; 2026-11-07 UTC;
[#108](https://github.com/uibcdf/pharmacophoremt/issues/108).
This closes the bounded in-memory experiment left at the pause checkpoint and
advances the [mature-0.x staircase](roadmap.md). It qualifies a public modular
subworkflow; no runtime signature, persistent cache/index or provider changes.

## Declared question and implementation

The [prospective plan](evidence/feature_reuse_plan_20261107.json) was
[declared before execution](https://github.com/uibcdf/pharmacophoremt/issues/108#issuecomment-6701310593).
Its SHA-256 is `eeea9d49ae9c00d096d64b1ed2e00a8bb8ae6e463cb0afb3723dac4ff724e98f`.
The [execution overlay](evidence/feature_reuse_execution_20261107.json) fixes the
source files and test selection. The comparison harness lives in unshipped
[`feature_reuse_experiment.py`](../phmt_test_support/feature_reuse_experiment.py);
[`test_feature_reuse_experiment.py`](../tests/test_feature_reuse_experiment.py)
provides 17 new controls within the 87 selected scientific cases.

For one unchanged prepared source, extract the same explicitly requested families
once for reuse and once per query for the fresh arm. Both use identical public
`get_rigid_feature_correspondences` and `get_rigid_feature_placements` calls.
The placement tool retains its native post-fit re-extraction and identity checks.
Accepted placements are separately checked through public `PoseEvaluator` and
`get_screening_score(..., score_method='checked_pose_coverage')`.

Full detached proposal reports, placement reports and checked-pose evidence must
be equal across the two arms. The existing quantity detacher seals physical
quantities in PyUnitWizard records; no coordinate parser, local molecular fit,
replacement matcher or saved-inventory decoder is introduced. Failures propagate.

## Inputs and resource domain

Reuse the three original, byte-verified H5MSM snapshots from the
[PubChem3D pilot](pubchem3d_receiving_pilot.md), retaining all old measurements:
CID1983, CID2244 and CID2519 have respectively 2, 4 and 3 native acceptor features.
References are caffeine and aspirin acceptor inventories. Every request uses
`features=['hb acceptor']`, `selection='all'`, frame0 and explicit chemical state0.
No source acquisition, new state/H/conformer generation or provider update occurs.

Association-clique proposals use length tolerance `0.15 nm`, `min_matches=3`,
64 graph nodes, 1000 cliques, 10000 triplet trials and 1000000 matrix entries.
Direction tolerance is `30 degrees`. Each arm fits only its first canonical
mapping (`max_placements=1`). Counts and completion retain the resulting scope.
Scientific executions are serial, CPU19/quota100%, one backend thread,
nice19/idle I/O, 512MiB cgroup, no swap and bounded180s wall time.

Requested families remain explicit because an absent record cannot establish
that a family was requested. Source/selection/frame/state/chemistry/geometry
must remain unchanged. Axis checks and consistency hashes do not authenticate
source origin or chemical correctness. The harness checks coordinate and
inventory immutability; the caller still owns the chemistry/source precondition.

## Actual result

All six source/reference comparisons retain exactly equal native evidence.
The table counts proposals / selected mappings / accepted placements in either
arm; they are work counts, not independent molecules.

| Source CID | Caffeine reference | Aspirin reference |
| --- | --- | --- |
| 1983 | 0 / 0 / 0 | 0 / 0 / 0 |
| 2244 | 24 / 1 / 0 | 24 / 1 / 1 |
| 2519 | 6 / 1 / 1 | 24 / 1 / 0 |

Both self-cases have a checked-pose match with score1. The two cross-reference
prefixes have no accepted placement, but omit23 mappings each. They must not be
reported as compound negatives. Three-site placement acceptance would also not
establish every essential site of a four-site aspirin query. No whole-source
ranking is computed. Native family completion and supplied-mapping completion
remain separate from omitted work and the full rigid-search stopping contract.

Outer source extraction requests total fresh6 versus reused3. This excludes
reference construction, native post-fit recognition and final pose evaluation;
it is not a total provider-call or speedup measurement. The original H5MSM,
old capsule directory identities, source coordinates and cached inventories remain
unchanged. Complete native geometry-bearing outputs remain local.

## Public composition and attribution

The [existing public recipe](../docs/content/cookbook/modular_rigid_tools.md#reuse-one-prepared-source-across-queries)
now demonstrates two different reference geometries reusing one source inventory.
All four Python blocks were executed in order through public scientific APIs.
The original analytical charge triangle yields six fits; the changed-distance
query yields zero proposals/fits. This recipe fits its entire proposal set within
its budget; the real-input experiment's one-mapping prefix is a distinct scope.
Neither execution qualifies an installed package or performance claim.

The real-input run uses an application-owned Ackredit session and explicit PHMT
attribution. The outer comparison capture preserves software/method records for
actually reached native branches, without changing the two report bodies.
The session retains16 items/49 contextual uses. Manual input provenance remains
linked to the original PubChem receipt; complete source/provider instrumentation
is not asserted. Citation reading is not another scientific calculation.

## Evidence, publication and next increment

The [receipt](evidence/feature_reuse_20261107_summary.json) links raw control logs,
JUnit/event records, exact source/runtime/native identities, full local outputs
and a verified public scalar/code/citation projection. Native source/query/feature/
placement geometry and H5MSM bodies remain local under the original publication
restrictions. These are the same three supplied conformers, not six independently
sampled compounds or activity validation.

Use this result to integrate a selected complete public task under #108/#95.
The next action is a concrete native workflow/API gap audit against the current
incremental/recovery/inspection contracts, then public integration with its
appropriate source/installed gates. Avoid another cache/index abstraction until
it has a measured scientific/workload reason. Reusable molecular collections
remain [MolSysMT #624](https://github.com/uibcdf/molsysmt/issues/624)-owned;
#103/#66/#106 biological admission and #9/#23 full delivery remain separate.
