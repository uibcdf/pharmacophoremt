# Pharm3D distance filtering and native rigid placement

Case `rdkit-bounds-20261107`; owners LMMV/dprada;
[#128](https://github.com/uibcdf/pharmacophoremt/issues/128).
This is an executed **analytical comparison**, with ten fixed synthetic controls
and186 exhaustive assignments. It compares distance filters on shared features,
then tests every native proposed rigid placement. It is separate from chemical
perception, flexible embedding, large-library performance and activity prediction.

The [prospective contract](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/rdkit_bounds_comparison.md)
and [original execution](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/rdkit_bounds_execution_20261107.json)
retain exact input/code/provider/native hashes, full local results, reached
attribution and original failures. The [sealed receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/rdkit_bounds_20261107_summary.json)
publishes owned controls and scalar/hash/citation evidence.

## Boundary correction and current scope

A later full-source checkpoint found that the original decimal-generated
boundary coordinates were not exact native endpoints on all platforms. The
original measurements below are preserved. [Issue143](https://github.com/uibcdf/pharmacophoremt/issues/143)
records that failure and the independent high-precision diagnosis.

The current boundary fixture revision uses exactly representable3/4/5nm geometry,
half/one-and-a-half scaling and1.25nm per-site tolerance. Eight interior inputs
and production predicates are unchanged. Rational guards verify the actual
binary coordinates rather than accepting an approximate triangle. The revised
14 focused guards and ten-case/186-assignment driver pass locally, retaining
2/1native versus0/0RDKit boundary mappings. This later input has its own
[receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/rdkit_boundary_correction_20261107_summary.json);
corrected source controls now pass in all eight Linux/macOS Python3.11–3.14
cells at frozen8db2a53, with2357tests per cell. The [terminal receipt](https://github.com/uibcdf/pharmacophoremt/blob/main/devguide/evidence/boundary_ci_terminal_20261107.json)
preserves exact identities. Public installed/platform delivery remains separate.
This corrects a
fixture exactness claim, not an activity-validation result.

## What is compared

MolSysMT constructs three/four disconnected single-atom ions with declared
coordinates and supplies native fitting. PHMT recognizes their positive-charge
features. Both filter arms use these same single-atom feature identities and
the same fixed conformer, without a separate RDKit feature-perception step.
The query's centers/families use the existing public RDKit projection.

Native filtering permits pair-distance differences up to twice the per-site
fit tolerance. We explicitly set the corresponding RDKit bounds after converting
lengths to angstroms through PyUnitWizard. This configured comparison is not an
implicit translation of every native constraint. The
[RDKit Pharm3D API](https://www.rdkit.org/docs/source/rdkit.Chem.Pharm3D.EmbedLib.html)
documents filtering and embedding as distinct operations; this case executes
the actual installed2026.09.2 filter and does not request embedding/optimization.

All interior cases use0.001nm per-site tolerance, all atoms, frame/state0 and
complete24-assignment enumeration (6 for the three-site planar case). Every
native proposed full mapping is fitted. Accepted poses are independently checked
with `PoseEvaluator`/`checked_pose_coverage`; each has score1. No prefix is ranked
or substituted for an exhaustive answer.

## Actual answers

| Fixed geometry | RDKit / native retained mappings | Accepted native placements |
| --- | --- | --- |
| Identity | 1 / 1 | 1 |
| Translation | 1 / 1 | 1 |
| Proper rotation and translation | 1 / 1 | 1 |
| Equivalent angstrom input | 1 / 1 | 1 |
| Permuted feature geometry | 1 / 1 | 1 |
| Stretched tetrahedron | 0 / 0 | 0 |
| Reflected noncoplanar tetrahedron | 1 / 1 | 0 |
| Reflected coplanar triangle | 1 / 1 | 1 |

The reflected tetrahedron preserves internal distances but cannot satisfy all
sites after a proper rigid rotation within this tolerance. Its retained mapping
is a candidate, rather than a hit. The planar reflection admits a proper
three-dimensional rotation. These artificial point sets do not establish
chemical enantiomer behavior or receptor binding.

Two further3-site controls test exact lower/upper boundaries, with a3-4-5angstrom
triangle and0.125nm per-site tolerance. Native filtering retains respectively2
and1 mappings; RDKit retains0 in both cases. The identity assignment is included
by the native inclusive test and rejected by RDKit's strict interval test. One
RDKit endpoint is explicitly set to the actual source-distance value to probe
machine equality, after checking the analytical endpoint within1e-12angstrom.
Both values remain recorded. No epsilon adjustment hides the difference, and
these two controls do not claim common filter semantics or a post-fit answer.

## Reproduce and interpret

From the source checkout in a qualified environment, run:

```bash
python -m devtools.compare_rdkit_bounds --output NEW-comparison.json
```

The output must be fresh. It retains every case, complete native evidence,
failures and actual provider/source identities. Rerun when input/preparation,
feature definitions, filter boundaries, projection, fitting or provider behavior
changes. Source controls live in `tests/test_rdkit_bounds_comparison.py` and reuse
the unshipped case harness; the driver additionally captures actual attribution.

The source selection passes61 scientific controls (12 new),24 distribution,
3 reporting and18 archive cases. The complete fixed driver is separate from
that106-case count. Its application-owned session retains14 attribution items
and47 uses. Public RDKit software credit covers directly completed filter cases;
this is not instrumentation of every external internal call.

Original512MiB data-limited attempts fail and remain preserved. An explicit
prospective resource amendment uses a1GiB per-process data limit, one CPU/backend
thread and low CPU/I/O priority. Kernel-observed whole-command peak RSS is
391180288 bytes for scientific tests and475381760 for the driver. Those are
execution observations, not incremental memory allocations or benchmarks.
There is no aggregate memory/no-swap/task/quota enforcement without an owned
cgroup. No provider prefix, source or native artifact is changed.

The comparison supports retaining post-fit validation and making tolerance/
boundary policies explicit. It also identifies the separate public
[RDKit projection qualification task#140](https://github.com/uibcdf/pharmacophoremt/issues/140).
It establishes no general RDKit/PHMT feature, query, search, score or biological
equivalence, no speed advantage and no installed/public-platform qualification.
