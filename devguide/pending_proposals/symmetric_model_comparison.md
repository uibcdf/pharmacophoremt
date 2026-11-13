---
summary: Define a symmetric comparison alongside the legacy ordered greedy score.
issue: uibcdf/pharmacophoremt#205
status: open
opened: 2026-11-12
closed:
verification: measured
area: [modeling]
guard:
normative:
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
