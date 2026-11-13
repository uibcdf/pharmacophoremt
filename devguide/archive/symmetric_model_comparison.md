---
summary: Define a symmetric comparison alongside the legacy ordered greedy score.
issue: uibcdf/pharmacophoremt#205
status: resolved
opened: 2026-11-12
closed: 2026-11-13
verification: measured
area: [modeling]
guard: tests/test_symmetric_comparison.py
normative: devguide/symmetric_model_comparison.md
blocked_by: []
supersedes: []
---

# Symmetric model comparison proposal

## Observed behavior and ownership

At 878864e, hydrophobic Point models A with x=[0.1,0]nm and B with x=[0,0.3]nm
give A.similarity(B,0.21)=0.5 and B.similarity(A,0.21)=1.0. Greedy allocation
matches its described ordered loop, but the generic Dice label does not establish
a symmetric maximum-matching coefficient. #204 preserves the loop, clarifies
its name and records the original probe; it does not resolve this proposal.

PharmacophoreMT owns feature compatibility, site interpretation and this score.
No ArgDigest or molecular-provider defect is inferred. Radius, orientation,
weight, essential/exclusion meanings and centerless sites need declared scope.

## Proposed direction and acceptance

Define an explicitly named symmetric comparison with maximum-cardinality
one-to-one compatible matching. Decide public method/default/version migration
instead of silently changing legacy results. Reuse appropriate owned matching
tools and check independent exhaustive small oracles, swap/permutation symmetry,
ties, alternatives, empty/aliased/centerless inputs, fixed units/inclusive
thresholds, common-frame authority and denominator/unsupported semantics.

Declare workload/memory limits for large cases and qualify source/exact-owned/
public-provider examples. Activity/biological/performance and full supported
platform gates remain independent. A new algorithm and its compatibility
decision remain unimplemented; the reproduction is not a symmetric-method gate.

## Reproduction received — 2026-11-13 local date

[#204 receiving](../evidence/cached_inspection_controls_20261112.json) repeats the
0.5/1.0 counterexample in source and exact-owned/public-provider controls and
all six nm/pm guide contexts. The legacy allocation loop remains identical.
Existing SciPy assignment consumers are `screening.pose_evaluation` and
`screening.feature_neighborhoods`; inspect their actual contracts before reuse.
This adds reproduction evidence, not implementation or acceptance of a new
similarity method. The proposal remains open.

## Selected implementation — 2026-11-13

The [owning contract](../symmetric_model_comparison.md) selects an explicit new
public report tool and scalar method option, preserving the old default. The
original proposal/reproduction above stays historical. Point/Sphere positive
center overlap, finite dimensions, quantity/feature semantics, SciPy binary
assignment, tie/count invariance and genuine optional-attribution receiving now
have executable controls. Source receiving passes237 selected cases (56new),
including1296 independently enumerated two-site workloads. Exact-owned and
public-provider receiving follow a committed freeze before closure.

## Executed resolution — 2026-11-13

The [combined receipt](../evidence/symmetric_model_comparison_20261113.json)
receives237 selected cases per source/owned context (56new),56 actual public-
ArgDigest cases per context, public PUW0.28.1/Pytest Receptor1.2.2 and18 guide
blocks. Exact source6e409d8 has242 verified payloads/187 equal runtime bodies/
169 target-only observed modules, actual SDK staging and unchanged tests.
Four contexts retain all1296 expected/observed finite-family outcomes each.
The API/numerical/shape/frame/budget/attribution contract is implemented for its
explicit positive Point/Sphere profile; the legacy default remains unchanged.

The initial four failures concern an incorrect new args-only diagnostic-state
expectation; SMonitor's documented args/code/text guard passes without provider
change. The older owned pose group first exhausts512MiB DATA and passes unchanged
14/14 at1GiB, with original incomplete output retained. The scientific guard
protects independently optimal cardinality, swap/order count invariance, native
scope/units/budgets and real optional-provider outcomes. This closes the bounded
#205 proposal; wider shape comparison and biological/scale/full public gates are
not claimed. Broader#6/#108 and #9/#10/#23 remain separately owned.
