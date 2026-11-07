# RDKit Pharm3D distance filtering versus native rigid placement

Owners LMMV/dprada; 2026-11-07 UTC;
[#128](https://github.com/uibcdf/pharmacophoremt/issues/128), mature-0.x milestones1/6.
This contract and [prospective plan](evidence/rdkit_bounds_plan_20261107.json)
precede scientific execution. The [execution receipt](evidence/rdkit_bounds_execution_20261107.json)
and [sealed owned evidence](evidence/rdkit_bounds_20261107_summary.json) now receive
all ten controls/186 assignments and106 selected source cases. The
[public case](../docs/content/validation/rdkit_bounds_comparison.md) explains the
actual answers and their limits. Original attempts retain their own identities.

## Dated boundary-fixture correction, 2026-11-07

The original receipt below remains historical. Frozen source489be12 CI42416657424
fails its upper-bound expectation on macOS; [#143](archive/analytical_upper_bound_platform.md)
owns the correction. Exact Decimal.from_float operands and100-digit square roots
show that the original upper/lower pair differences exceed0.25nm by approximately
3.33066907387547e-17/5.55111512312578e-18nm. Its stored decimal-generated coordinates
do not define an exact native endpoint independently of norm rounding. This does
not establish a NumPy/MolSysMT/RDKit defect or measure a macOS norm implementation.

Revision `binary-exact-nm@2` changes only those two synthetic boundary inputs to
an exactly representable3/4/5nm triangle, half/one-and-a-half scaling, and1.25nm
per-site tolerance. This preserves relative geometry/cutoffs and all eight
interior inputs. Independent Fraction guards require the actual binary inputs
to retain the Pythagorean ratio, squared lengths, exactly representable distance
and pair-difference equality; both guards fail on the original data. No production
predicate, scientific epsilon or matching definition changes. The full revised
14-case guard and ten-case/186-assignment driver pass locally, with unchanged
2/1native versus0/0RDKit boundary counts. Hosted acceptance of the revision is
now accepted for frozen8db2a53 across all eight Linux/macOS Python3.11–3.14
cells,2357tests per cell; the failed earlier run is never relabeled successful.
The [correction receipt](evidence/rdkit_boundary_correction_20261107_summary.json)
retains original/new inputs and original failures. Earlier source/RSS/attribution
counts below belong to their original producer and input hash.

## Question and common represented problem

Compare RDKit Pharm3D `CoarseScreenPharmacophore` with public native
`get_rigid_feature_correspondences(..., correspondence_strategy='association_cliques')`
on exhaustive assignments of fixed single-atom positive-charge features. Then
execute every native proposed mapping through `get_rigid_feature_placements`
and independently evaluate accepted poses with `PoseEvaluator` and
`checked_pose_coverage`. Compare filters as filters; a retained mapping does not
establish an accepted proper rigid placement.

Eight fixed analytical cases cover identity, translation, proper rotation plus
translation, equivalent angstrom input, permuted feature geometry, a stretched
nonmatch, a noncoplanar reflection and a coplanar reflection. Seven use four
single-atom ions; the coplanar case uses three. Enumerate all24 or6 full
assignments respectively, with no prefix selection. Expected interior filter
counts are1 per case except the stretched case0. Expected accepted placements
are1 except stretched/noncoplanar reflection0. Both filters retain a reflection
of the tetrahedron; proper rotation cannot reproduce its full reflected geometry
within the declared small tolerance. The planar reflection can be reproduced
by a proper three-dimensional rotation. These artificial point sets are not
chemical enantiomers, drugs, a sampled library or an activity cohort.

MolSysMT owns molecular construction/conversion and native fitting. Build the
fixed ions through public conversion and install explicitly unit-bearing fixture
coordinates. PHMT's actual recognition owns the shared feature inventory; this
does not compare RDKit's independent feature perception. Verify single-atom
feature/atom axes and source-coordinate immutability. Obtain the fixed conformer
distance matrix through RDKit's existing `Get3DDistanceMatrix`, not a new local
molecular geometry kernel. Use public PHMT `io.to_rdkit` for the query's
centers/family projection, then explicitly configure its pair-distance bounds.
That existing projection alone does not transfer the native radius contract.

## Tolerances, boundaries and complete denominators

Native association filtering admits `abs(d_ref - d_source) <= 2*delta`, a
necessary pair-distance condition for individual fitted displacements `<=delta`.
Therefore configure Pharm3D pair bounds `d_ref +/- 2*delta`, converting the
length explicitly through PyUnitWizard to RDKit's angstrom protocol. Interior
cases use delta0.001nm. All sites are essential and matched once; no directions,
aromatic groups, exclusions, alternate roles, weights or feature sharing enter
this represented problem. No RDKit embedding/optimization or topology-derived
flexibility is requested.

Source inspection of installed RDKit2026.9.2 shows strict interval-overlap checks;
native association checks are inclusive. Two additional3-site boundary controls
use a3-4-5 angstrom triangle, delta0.125nm and half/one-and-a-half scaling. The
identity assignment touches the lower/upper pair bound exactly. Declare the
expected native admission and RDKit rejection of that assignment; retain all6
filter decisions per control. Assign that one RDKit endpoint from the same
fixed source-matrix element to ensure exact machine equality; verify agreement
with the analytical interval within1e-12 angstrom and retain both original
values. This is an explicit boundary probe, not an epsilon added to a classifier.
These boundary controls do not assert equivalence
or a post-fit classification. No epsilon is introduced to conceal the difference.

Every case retains original/evaluated assignment counts, complete native
proposals, attempts/fits, accepted/rejected mappings, native evaluation evidence,
exceptions and its independent expected result. Ten controls check186 explicit
assignments in total (174 interior +12 boundary). Exceptions remain failures,
never manufactured nonmatches. Resource exhaustion remains a failed incomplete
calculation. Use max64 graph nodes,1000 maximal cliques,32 fits and1000000 matrix
entries, frame/state0, all atoms and explicit feature families.

## Sources, execution and acceptance

Primary documentation: [RDKit Pharm3D API](https://www.rdkit.org/docs/source/rdkit.Chem.Pharm3D.EmbedLib.html)
and [Pharmacophore API](https://www.rdkit.org/docs/source/rdkit.Chem.Pharm3D.Pharmacophore.html).
Installed Python/source/native hashes and provider versions, rather than the
unversioned documentation banner, identify the executed implementation. Preserve
external BSD ownership; publish links/hashes, not copied third-party source.
Inputs and comparison/control code are repository-owned synthetic material.

Use published Pytest Receptor for focused scientific controls, full Ruff and
affected reporting/archive/index checks. Run the complete fixed driver under an
application-owned Ackredit session and explicit PHMT attribution. Record actual
native attribution and the directly executed RDKit software/source separately;
do not claim instrumentation of every external internal call. This is an
unshipped case harness, not a production external-engine adapter or new provider
dependency. Existing molecular and optional-engine ownership remains unchanged.

Heavy execution is serial CPU19/backend1/nice19/idle I/O with pressure checks,
per-process512MiB data limit and a180s command bound. No own systemd runtime
exists; aggregate memory/no-swap/tasks/quota is unavailable and not claimed.
Defer under pressure or retain failure without increasing the resource budget.
No timing/memory benchmark or biological/public-platform qualification follows.
The live frozen4616c78 CI remains separate and is not restarted for this study.

## Explicit resource amendment before the second execution

The [dated amendment](evidence/rdkit_bounds_resource_amendment_20261107.json)
preserves the failed512MiB tests/driver and native-allocation probe. It revises
this self-imposed task data limit to1GiB before another run, with unchanged
scientific fixtures/expectations/budgets, entry available memory>4GiB and actual
whole-command peak RSS from `/usr/bin/time -v`. The initial instruction above
describes the original attempt, not a successful receiving or an immutable human
resource allowance. There is no repeated budget increase after this revision.
The invalid `rdkit` token in the case decorator is a harness mistake: the host's
software registry did not declare it. The corrected case uses the existing
native decorator; the driver records directly completed RDKit work through
Ackredit's public software/scope/track operations. No provider code is changed.

## Received result and next decision

All eight interior complete mapping sets agree. Five tetrahedral rigid/unit/
permutation positives and the coplanar reflection each produce one independently
checked pose with score1. Stretching has zero proposals; the noncoplanar
reflection retains one candidate but no valid placement. Lower/upper exact
boundary controls retain2/1 native candidates versus0/0 RDKit, including the
declared identity-mapping divergence. Boundary fits are explicitly not requested.
All source coordinates/inventories and observed package source digests remain
unchanged. Actual MolSysMT native SHA-256 remains
`2a79b9a83b0fe0b00a54c9b80f04bf6c9ace2b3473c53269edbfe29904f8930b`.

The source selection passes61 scientific cases (12 new),24 distribution,
3 reporting and18 archive; full Ruff/index/whitespace checks pass. The separate
complete driver has ten successful cases,14 actual attribution items/47 uses
and no input mutation. Recorded kernel peak RSS is391180288/475381760 bytes
for tests/driver under the revised data budget. These are not benchmarks.
The shared editable version remains its earlier134 identity; executed PHMT
source bytes belong to parente0a84ef plus the recorded unshipped case overlay.
Do not relabel that measurement as a later commit or full supported installation.

The [post-seal closeout](evidence/rdkit_bounds_closeout_20261107.json) receives
the new issue140 report/index and current reporting/archive/style checks. Its
first registration check caught the missing140 literal in the existing exact
issue-set guard; adding only that new identity restores all three reporting
cases. The original failure and sealed scientific archive remain unchanged.

The comparison motivates explicit projection/loss/boundary contracts. New
[#140](https://github.com/uibcdf/pharmacophoremt/issues/140) owns RDKit field and
constraint qualification; do not silently expand existing projection semantics.
The diagnostic masking seen in the old local MolSysMT9e1f1b1 context is related
to already-resolved [MolSysMT#601](https://github.com/uibcdf/molsysmt/issues/601).
Current owner source711717828 preserves operational causes; source inspection
does not receive that fix into this shared prefix. No new numerical-provider
bug is established by an allocation failure. All full source/installed/public,
biological and broad-tool comparison milestones remain separate.


[Corrected hosted receiving](evidence/boundary_ci_terminal_20261107.json) closes
#143 only for its declared boundary-fixture/source scope. The independent local
ten-case driver and actual attribution retain their original identities. No
package publication, biological equivalence or measured acceleration follows.
