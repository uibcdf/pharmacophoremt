# Bounded symmetric native model comparison

Owners LMMV/dprada; PHMT #205; implementation decision 2026-11-13.

## Public contract and compatibility

`pharmacophoremt.compare_pharmacophores(pharmacophore, other, *,
distance_tolerance='0.15 nm', max_sites=4096, max_matrix_entries=1000000,
skip_digestion=False)` is the independently useful report tool. Native
`similarity(other, tolerance_nm=.15, *, method='ordered_greedy',
skip_digestion=False)` retains the old default and numerical loop. Explicit
`method='maximum_cardinality'` returns the new tool's scalar similarity using its
default quotas; experts use the report tool for correspondence and budget control.
The scalar facade contributes to an active attribution session, while the report
tool retains its detached result attribution. No silent default migration occurs.

Both public tools have defining closed ArgDigest contracts and explicit controls.
The report tool's ordinary admission checks types without walking unbounded
models; native site/matrix quotas precede geometry and matrix processing. Native
model consistency, quantities, positive features and scientific invariants stay
active with bypass. The facade delegates through the child's ordinary admission;
the outer bypass is not blindly forwarded.

## Scientific definition

The first profile admits native positive Point/Sphere sites with finite 3D length
centers, known nonempty feature alternatives and valid declared site constraints.
Two sites have an edge when their feature sets intersect and their Cartesian
centers lie within the nonnegative length tolerance. Each local occurrence can
match once, including aliased occurrences. Volume constraints and all other
shapes are refused, including center-bearing directed/disk/Gaussian shapes.
Radius, weight and essential flags are retained in snapshots but do not weight
this explicitly unweighted site overlap.

For maximum cardinality k and input counts n,m, similarity=2k/(n+m); both-empty
is explicitly zero. Counts and score are invariant under input swap and site
permutation. One optimal pair map is returned in original local indices; tied
pair identities need not be invariant. This is a normalized overlap score,
not a guaranteed mathematical distance metric, pose fit, affinity or activity.

Coordinates must already share a caller-declared coordinate basis. No alignment,
molecular query, PBC correction or source/frame authentication is performed.
Original ref_struct values are retained; equal frame indices do not authenticate
a common basis and different indices do not forbid comparing prepared snapshots.

Center values and comparisons use explicit nm. Threshold records preserve the
submitted value/unit. Finite positive thresholds admit relative roundoff of
8*binary64 epsilon; tolerance zero admits only exact equality of represented
centers. Store this slack in criteria; do not rewrite source geometry/cutoffs.
Nested hypot avoids avoidable square overflow/underflow. Unrepresentably large
separations exceed every finite threshold and remain nonedges, not infinite
matched distances. Extreme coordinates still have ordinary floating precision.

## Solver and ownership

Reuse SciPy's supported rectangular
[`linear_sum_assignment(maximize=True)`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html),
already consumed by PoseEvaluator and feature-neighborhood assignment. Its
existing consumers solve different objectives and are not interchangeable model
comparison tools. The new PHMT-owned tool builds binary benefits (edge=1,
nonedge=0). Every valid partial matching extends to a full rectangular assignment
using zero-benefit fillers; maximizing total benefit therefore maximizes valid
cardinality. Filter selected zero-benefit pairs from the result. No local solver
or molecular implementation is introduced. Crouse's provider-documented reference
implementation and SciPy are credited only when assignment actually runs.

Bounds are positive max_sites per input and n*m matrix entries, including when
one partner is empty. Default benefit storage is at most8MB; backend copies and
O(n+m) snapshots add memory. Build distances one row at a time instead of an
n*m*3 tensor. Quotas bound declared dimensions, not elapsed time or every backend
allocation. PHMT-E111/ComparisonLimitError reports observed resource and limit
before allocation/solver; it returns no plausible partial score.

## Result, persistence and optional attribution

The versioned method `center_feature_maximum_cardinality_dice@1` report retains
executing PHMT version, complete=True, score/counts, original-index pair maps,
unmatched indices, declared criteria/limits and actual work counters. Input
snapshots detach ordered names/ref_struct and site geometry/features/ignored
constraints; they are not a full native model/provenance archive. Keep original
native models for root metadata, observations and prior bibliography. Quantity
fields use the existing public QuantityRecord codec; distances carry explicit nm.
Plain JSON save/read preserves records and adds no calculation credit.

The existing optional attribution machinery records actual NumPy/PyUnitWizard,
PHMT and reached SciPy/assignment branches, respects application sessions and
retains detached references. Completed-empty/no-edge comparisons have no SciPy
assignment credit. Absence/failure preserves science and original exceptions;
fresh saved-reference readers need no scientific engine and add no new usage.
No new dependency floor, optional engine or provider mutation is required.

## Acceptance and limitations

`tests/test_symmetric_comparison.py` enumerates all1296 two-site combinations
from a declared three-position/two-feature family with an independent recursive
partial-injection oracle. Separate rectangular permutations/swaps, ties,
alternatives/aliases/weights, empty inputs, unsupported shapes/volumes, numerical
boundaries/extremes, budget-before-axis, controls/inheritance and source custody
tests do not use the production assignment algorithm as their oracle.
`tests/test_symmetric_comparison_attribution.py` observes the real optional
provider, reuse/enclosing workflows, no-assignment branch, detached/fresh reading,
genuine unimportability and failure with warnings promoted to errors.

Retain the original API-absence/asymmetry probe and first48pass/4fail scientific
attempt. Those four failures were an incorrect new assertion that args-only
exception reconstruction preserves arbitrary structured fields; SMonitor's
guide section7/Check4 promises args idempotence, not that extra contract. The
corrected guard checks args/code/text and original structured fields separately.
No provider defect/workaround is inferred. Record source and exact-owned/public
receiving separately, including all scientific inputs/scripts/results/limits.
Use one CPU/thread, idle I/O/nice19 and finite limits after RAM/swap/PSI preflight;
preserve20% physical RAM plus1.5GiB. #148/#165 stay stopped. Broader#6, full
supported source/installed/public/platform, biological and scale gates remain
separate; no performance or new tag/publication claim follows.

## Source receiving — 2026-11-13

The [source receipt](evidence/symmetric_model_comparison_source_20261113.json)
passes237 selected cases (56new/181existing), six nm/pm public guide blocks and13
quality operations, including strict whole-site docs and27 distribution tests.
All1296 original exhaustive-family expected/observed outcomes are retained in
raw execution output. SciPy1.18.1/NumPy2.5.4 and actual other provider identities
are recorded. The bounded inventory has151 callables/40 explicit controls/124
plans; it does not certify complete API adoption. Exact-owned/public-provider
receiving follows a committed freeze. Initial diagnostic/collector/formatting
harness corrections stay separate from scientific/provider defects.
