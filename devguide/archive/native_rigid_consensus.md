---
summary: Build alternative native consensus models from prepared rigid unaligned ligands.
issue: uibcdf/pharmacophoremt#26
status: resolved
opened: 2026-10-03
closed: 2026-11-03
verification: measured
area: [modeling, consensus, attribution]
guard: tests/test_rigid_consensus.py
normative: devguide/rigid_consensus_workflow.md
blocked_by: []
supersedes: []
---

# Prepared rigid unaligned consensus and comparable proposal strategies

## Resolution — 2026-11-03

Reviewed and incorporated as the prepared rigid unaligned source/API method.
The [new receipt](../evidence/rigid_consensus_acceptance_20261103_summary.json)
records clean receiving head **0bab03aaa089418be11d2be2efb3c8bd6f7ff29e**.
All **95 freshly executed controls** pass in 50.44 s without failures/errors/skips:
25 rigid-consensus, 10 modular tools and 60 correspondence-geometry controls.
They protect an independent injective oracle, both baseline families, six symmetric
mappings, noncoplanar reflection/distortion, degenerate centers, explicit pivot/
selection/frame/units, unplaced support, preflight budgets, public-tool composition,
provider error propagation, actual attribution and native persistence. No new full
suite is claimed.

Fresh host-off/on capsules use five frozen analytical cases with both baseline
strategies. Typed recovery explicitly adds one nonempty, unplaced charge source:
its original feature remains in evidence and support stays 2/3. Every accepted
typed placement recovers the original atom coordinates within 1e-12 nm. The
association family attempts one fit and retains one model; triplets attempt eleven
fits and retain seven. Six symmetric mappings/layouts/models per family remain
separate. Reflected feature geometry and an empty source each complete with no
models; the reflected case retains rejected fits, not chemical-absence evidence.
The exhausted fit budget raises PHMT-E107/complete=False without a query.

Per tracking profile, the ten case/strategy records contain four completed,
four completed-empty and two deliberately failed calculations; twenty models
pass 112 pose evaluations (56 matched, 56 valid negatives), including public
MolSysMT replay of retained placements and rejection of the original unaligned
frame. Eight JSON/YAML round trips under changed unit policies preserve model
metadata and outcomes. All declared molecular domains remain unchanged within
both pm and default unit-policy comparisons. Off/on scientific projections agree;
actual prepared-input credit is 3 items/6 uses host-off and 16/75 host-on. Reached
least-RMSD, clique and assignment references are retained; unexecuted RDP/frequent-
clique/G3PS methods receive no runtime credit.

Both unchanged cookbook blocks execute with application-owned capture
(16 items/68 uses); strict isolated Sphinx rendering passes with four neighboring
link-target stubs. Full loaded source/native/helper/test/input and metadata
identities are stable in focused, capsule and cookbook phases. No library/test/
fixture/scientific-definition/provider/prefix/sibling change is needed.

MolSysMT owns conversion, molecular inspection, motion, native anchor clouds,
proper least-RMSD fitting, copy/set/replay and RMSD. PHMT proposes and validates
pharmacophoric correspondences and assembles bounded placement/layout/hypothesis
alternatives. NetworkX supplies generic clique enumeration. No local molecular
solver, conformer generation, hidden preparation or fitted-pose early stop is added.
Completion remains one pivot and its declared finite family; maximal mappings
exclude submappings. Equivalent poses from different seeds remain separate, and
support does not imply affinity, chemical uniqueness or distinct binding modes.

The dated October primary-source survey remains linked and its objectives and
ownership distinctions are reviewed. Current accessible primary texts confirm
the frequent-clique/conformer-support and Pharmer index distinctions. Several
other endpoints are inaccessible or challenged; the receipt retains those exact
access limitations. No new complete literature replication review, latest external
software qualification, external-algorithm equivalence or speed ranking is claimed.
This closes the documented comparison/source-API slice without converting design
citations into executed implementations.

This resolves #26, not clean installed/public/platform/hosted (#23/#10/#9),
inherited workspace (#82), biological or performance qualification. #41 remains
partial for supported-public/floor/installed receiving and final legacy retirement
(review 2026-11-11). Next #27 independently accepts the modular comparison driver,
its warped-square objective counterexample and honest timing/memory scope. Its
ten modular guards passing here do not close that broader comparison. #60 retains
independent-copy receiving; #66 still awaits four original binding methods.
Addon/new release remain deferred. Owned /tmp/phmt26-acceptance-20261103-o71te38f/,
LMMV/dprada, review 2026-11-17; no local process remains after closeout. Original
October claims below retain their identities; pending-review statements are historical.

## What

Support prepared rigid ligand frames without caller pre-alignment. Preserve finite
mapping/placement alternatives, explicit pivot and support evidence while molecular
fitting/transformation remains in MolSysMT. Review efficient published alternatives.

## How

The reusable get_rigid_feature_correspondences tool separates invariant association
maximal-clique and typed triplet proposal families. The modeler composes the existing
MolSysMT-supported alignment, native extraction, absolute matching and aligned
clique/hypothesis operations. Accepted placements feed separate bounded layouts.
Source evidence includes unplaced ligands in the input support denominator.
The [workflow contract](../rigid_consensus_workflow.md) defines completion and bounds;
the [primary-source survey](../pharmacophore_search_strategies.md) defines future
comparison priorities and required scientific/performance evidence.

## Why

Prepared aligned consensus (#21/#24) and best-hit rigid screening (#15) are not a
multiple-ligand unaligned consensus workflow. A best-hit coverage early stop loses
alternatives needed for model discovery. The first two proposal families provide
reference implementations for comparison without copying provider molecular kernels.

## What is measured and what is assumed

**Measured, 2026-10-03:** The complete local suite passes **202 tests** in 180.84 s,
including 25 rigid consensus controls. Both new cookbook Python blocks execute
successfully and the isolated cookbook Sphinx build passes with nitpicky checking
and warnings treated as errors. The three offline reporting tests, generated
indexes, Ruff and whitespace checks pass. The two warnings are the pre-existing
deliberate Ackredit-failure control and legacy screening unit-stripping path.

Verification uses Linux/Python 3.13.14 with NumPy 2.4.6, SciPy 1.18.0 and NetworkX
3.6.1. Controlled source providers: MolSysMT
`4d490427e38c5836be82472348fdf61934442bda`, PyUnitWizard
`2ffe1885675f47c76af03c08e51bc889a5e99a05`, Ackredit
`584328de6efc07cee3a5ddf3ecda2d2e08cc72b4`. Captured runtime producer versions
are retained independently of these source pins. Reproduce with those provider
source trees on PYTHONPATH and the existing scientific environment:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest --receptor=llm -p no:cacheprovider -p no:rerunfailures tests/test_rigid_consensus.py
```

Literature claims refer to original methods, not measured PHMT speedups or latest
commercial release behavior. Prepared inputs, selected pivot and ligand identities
remain caller declarations. Source-provider integration does not qualify published
distribution, full-site documentation, hosted CI or biological pilots. Local work
awaits scientific/API review and commit; the report remains active.

## Alternatives and refuted paths

Invariant distances alone cannot certify proper fits. Minimum RMSD is not maximum
tolerance-valid feature coverage. Pairwise support is not hypothesis-wide support.
Forcing all sources to place silently changes the denominator or hides unsupported
sources. A maximal mapping family is not all submappings or continuous alignments.
Future G3PS, safe RDP, frequent-clique ensembles, indexed triangles and Gaussian
overlap require their own precise method and measured comparisons before adoption.

## Scope and exclusions

One prepared frame per ligand, one explicit pivot, two bounded proposal families,
proper MolSysMT fitting, post-fit validation, alternative layouts/native models,
portable evidence, optional actual-branch attribution and cookbook. No preparation,
conformer generation, flexible/global multiple alignment, geometric deduplication,
Rust/GPU/distributed implementation or biological validation closure.

## Acceptance criteria

Both methods recover declared rigid controls. Independent injective mapping oracles,
reflection/distortion controls and symmetric mapping alternatives protect mechanism
claims. Unplaced/empty inventories preserve support and source records. Limits and
provider failures cannot become scientific negatives. Real Ackredit records reached
solver branches, provider-documented least-RMSD criterion and producer versions, with
native persistence. Execute the cookbook and repository guards; scientific/API and
broader distribution review remain separate from local implementation delivery.
