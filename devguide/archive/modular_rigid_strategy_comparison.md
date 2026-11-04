---
summary: Expose modular rigid placement steps and compare consensus strategies reproducibly.
issue: uibcdf/pharmacophoremt#27
status: resolved
opened: 2026-10-03
closed: 2026-11-03
verification: measured
area: [validation, modeling, screening, benchmarks]
guard: tests/test_rigid_strategy_comparison.py
normative: devguide/rigid_strategy_comparison.md
blocked_by: []
supersedes: []
---

# Modular rigid tools and analytical comparison

## Resolution — 2026-11-03

Reviewed and incorporated as the modular tools and bounded analytical comparison.
The [new receipt](../evidence/rigid_comparison_acceptance_20261103_summary.json)
records clean receiving head **50776a15dd2cb103a7b56d65834f2f1d202651e6**.
All **23 fresh controls** pass in 52.85 s without failures/errors/skips: 13 objective/
frozen-case controls and 10 modular-tool controls. Cached construction requires no
molecular reads, placements retain source/report ownership, saved summaries add no
credit and refuse incomplete/inconsistent evidence, and the consumer calls the
public placement tool. No new full suite is claimed.

Fresh host-off/on objective capsules compare the same four feature pairs through
public MolSysMT Structures/get_rmsd: the full-mapping fit has RMSD .11 nm with
zero tolerance-valid matches; a selected triplet has RMSD .21865464043704247 nm
with three. The original four-essential-site query gives fits 1, 0 and .75 for
reference/full/triplet poses; the partial match remains not_matched. Nine pose
checks and two JSON/YAML round trips per profile pass across unit policies.
Source atom identity/state/coordinates remain unchanged; off/on science agrees.
Actual credit is 3 items/3 uses host-off and 12/47 host-on. An initial one-off comparison
incorrectly includes inherited source_attribution bibliography. Its failed script,
log, original queries and isolated difference are preserved; only the two defined
bibliography fields are excluded in the corrected science comparison. Complete
unfiltered results remain retained. No library/test/input/tolerance change follows.

All three unchanged cookbook blocks execute (13 items/58 uses); an additional saved-summary
read adds no credit. Strict isolated Sphinx rendering passes with two neighboring
link-target stubs. All owned tests/capsules/rendering finish before measurements.
The unchanged original CLI then runs six frozen cases/two baseline families in
12 sequential isolated workers, one warmup, three measured calls and a separate
citation call each. All 12 expected-outcome controls pass with identical summaries
across calls: five completed, five completed-empty and two expected PHMT-E107
failures. The latter have no completed attribution payload, rather than a successful
negative. Every completed/empty record captures actual attribution. All 36 timing
samples, 12 warmups, reached references, source/input/provider/native identities,
thread settings and original outputs remain in the checksum-qualified archive.

Workers observe CPU/parallel=False/one-thread policy, with all source/loaded-native
hashes equal across workers and to the controller's before/after identities.
All four phase source/native/helper/test/input/metadata comparisons are stable.
The supported 300 s per-worker wall allowance covers imports/five calls and does
not alter scientific graph/fit/layout budgets. No owned test/build/benchmark
runs overlap measurement; machine-wide exclusive execution is not claimed.
Whole-worker high-water RSS after measurements ranges 302.0–506.9
MiB, including setup/warmups; it is not per-call incremental allocation. Observed
times are descriptive local costs. Different model/coverage counts prevent an
unqualified speed ranking or equivalent-workload speedup. Defaults are unchanged.
The current table and exact samples are in the maintained contract/receipt;
October measurements below remain historical, including their original load caveat.

MolSysMT owns molecular construction/inspection/fitting/transformation/copy/set
and generic RMSD, including the new one-off objective measurement. PHMT owns
cached pharmacophoric query construction, correspondence acceptance and summary/
consensus assembly. No generic molecular kernel or benchmark framework is added;
no runtime/test/fixture/scientific-definition/provider/prefix/sibling change is needed.

This resolves #27's source/API and declared analytical comparison, not biology,
energetics, universal performance, continuous/global optimality, clean installed/
public/platform/hosted qualification (#23/#10/#9; workspace #82). #41 remains
partial for public/floor/installed receiving and final legacy retirement, review
2026-11-11. Next #28 independently receives typed-neighborhood dissimilarity and
ranked triplet seeds, especially all-seed equivalence versus finite-selection
misses, bounded allocation and actual adapted-stage credit. #60 and #66 retain
their scopes; addon/new release stay deferred. Owned root
/tmp/phmt27-acceptance-20261103-p_h5tcap/, LMMV/dprada, review 2026-11-17;
no local process remains after closeout. Original report text below is preserved;
its uncommitted/pending-review statements are historical.

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
