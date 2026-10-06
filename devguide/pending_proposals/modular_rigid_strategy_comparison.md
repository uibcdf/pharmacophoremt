---
summary: Expose modular rigid placement steps and compare consensus strategies reproducibly.
issue: uibcdf/pharmacophoremt#27
status: active
opened: 2026-10-03
closed:
verification: measured
area: [validation, modeling, screening, benchmarks]
guard: tests/test_rigid_strategy_comparison.py
normative: devguide/rigid_strategy_comparison.md
blocked_by: []
supersedes: []
---

# Modular rigid tools and analytical comparison

## What

Make inventory-to-query construction, supplied-mapping fitting/verification and
result summaries public tools. Assemble consensus from them and compare its two
finite proposal families reproducibly.

## How

The [maintained contract](../rigid_strategy_comparison.md) defines ownership,
controls and measurement. Frozen JSON cases feed scientific regressions and a
sequential isolated-worker CLI. The modeler calls public placement; MolSysMT owns
all molecular manipulation. Summary reading adds no credit. Timing/citation runs
are separate, with original software versions and source/input hashes retained.

## Why

Users should choose and compose steps without a monolithic workflow or private
helpers. The warped-square control shows a least-RMSD maximal fit matching zero
features where triplet placements match three. Speed comparisons need the intended
scientific objective. This refines #26's declared limits, not a defect violating
its finite-family completion contract.

## What is measured and what is assumed

The complete local scientific suite passed 225 tests on Python 3.14.7 in 194.15 s
with the environment's providers and no PYTHONPATH overrides; the prior controlled
3.13 run also passed 225 tests. The new modular recipe executed three blocks and
the isolated cookbook passed strict Sphinx checking using the existing 3.13
documentation tools. Updated CI/recovery/reporting guards passed nine tests.
The [retained comparison](../evidence/README.md) has 12 passed analytical controls,
one warmup and three measured calls per worker, stable outputs and identical
provider source/extension hashes. All completed cases captured real Ackredit
attribution in a separate call; expected PHMT-E107 cases remain failed.
Analytical cases are not biological validation or representative universal timing.
Memory is whole-worker high-water RSS, not per-call incremental allocation. Source
and extension hashes remain distinct from distribution closure.

## Alternatives and refuted paths

Median time alone hides changes in coverage or retained alternatives. Failed
enumeration cannot become empty consensus. Seed and full-domain RMSDs are different
objectives. Best-placement-only output prevents other compositions. No additional
molecular solver, general benchmark framework or third-party algorithm dependency
is needed; task-specific fixture/timing orchestration stays local.

## Scope and exclusions

Reusable PHMT tools, consumer assembly, six analytical cases, objective guard,
opt-in comparison, portable evidence and cookbook. No G3PS implementation, external
tool speed comparison, biological validation, website or Rust/GPU acceleration.
#20 retains publication design and #26 retains rigid consensus acceptance.

## Acceptance criteria

Standalone contracts and consumer calls are guarded. Cached construction has no
molecular reads, placements preserve source/report ownership, and summaries retain
support while refusing incomplete evidence and adding no credit. Frozen cases and
same-domain RMSD controls pass. Comparison records actual outcomes, repeats,
hashes/environment and reached citations. Recipe/docs/reporting guards pass;
scientific/API and distribution review remain separate acceptance gates.
