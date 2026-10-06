---
summary: Build alternative native consensus models from prepared rigid unaligned ligands.
issue: uibcdf/pharmacophoremt#26
status: active
opened: 2026-10-03
closed:
verification: measured
area: [modeling, consensus, attribution]
guard: tests/test_rigid_consensus.py
normative: devguide/rigid_consensus_workflow.md
blocked_by: []
supersedes: []
---

# Prepared rigid unaligned consensus and comparable proposal strategies

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
