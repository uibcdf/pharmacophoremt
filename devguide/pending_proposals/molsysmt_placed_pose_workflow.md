---
summary: Deliver a bounded MolSysMT-backed interaction-to-pharmacophore and pose-evaluation workflow.
issue: uibcdf/pharmacophoremt#13
status: active
opened: 2026-10-02
closed:
verification: measured
area: [modeling, screening, integration]
guard: tests/test_pose_evaluation.py
normative:
blocked_by: []
supersedes: []
---

# MolSysMT-backed placed-pose workflow

## What

Provide independently usable interaction extraction and evaluation of existing
poses while keeping all molecular-system operations in MolSysMT. The first
slice supports hydrophobic contacts and hydrogen bonds, explicit frame/state
selection, source-index provenance and inspectable matching results.

## How and evidence

`modeler.from_interactions()` and `model(method='interaction-based')` consume
native observations. `screening.PoseEvaluator` obtains chemical features through
public MolSysMT tools and assigns each candidate to at most one site. Essential
sites, directed donor-H geometry, heavy-atom exclusions and weighted coverage
have explicit semantics. Native metadata and detached provider bibliography
survive round trips; physical result fields use QuantityRecords.

`tests/test_pose_evaluation.py` exercises real MolSysMT interaction calculations
and independent analytical geometry controls. `tests/test_contracts.py` protects
invalid quantities/vectors, non-default unit policy and optional-viewer absence.
No biological pilot success or private evidence is claimed.

## Scope and exclusions

Unsupported kinds and periodic image reconstruction raise. No alignment,
hydrogen addition, protonation repair or conformer generation is performed.
The legacy modelers/screener are not fully migrated. The controlled dependency
route uses a published review snapshot, not a verified stable release closure.

## Acceptance and next review

The guard and `../placed_pose_workflow.md` define the delivered local slice.
Keep this proposal active during review and discussion of the scientific/API
contracts. Further families and adapters require their own controls. No commit
or hosted CI pass is claimed for this local implementation.
