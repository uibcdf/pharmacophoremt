---
summary: Build classical reference-ligand queries and evaluate them using shared MolSysMT chemical extraction.
issue: uibcdf/pharmacophoremt#14
status: active
opened: 2026-10-02
closed:
verification: measured
area: [modeling, screening, integration]
guard: tests/test_reference_ligand.py
normative:
blocked_by: []
supersedes: []
---

# Native reference-ligand workflow

## What and how

The local implementation adds public `modeler.get_features()` and
`modeler.from_ligand()`, plus `model(method='reference-ligand')`. Evaluation
consumes the same extraction tool. The six classical chemical families use
MolSysMT public recognition; aromatic planes and charge centroids are also
computed by MolSysMT. No direct chemical implementation has been added here.

The versioned definition and aromatic matching semantics are documented in
`../reference_ligand_workflow.md`. Results retain source/state/provider evidence
and declare actual matching method, CPU backend versions and precision.
`../extensible_modeling_contracts.md` records the accepted growth direction.

## Measured evidence

The guard uses real providers from the published pinned source snapshots listed
in `../placed_pose_workflow.md`, in the existing scientific environment. Analytical
controls exercise construction through retrospective ranking, aromatic orientation
and sign invariance, grouped charge centroids/sign, complete participant selection,
all six families together, units, persistence and unchanged source coordinates.
Tests do not establish biological enrichment, clean wheel builds or hosted CI.
On 2026-10-02 the complete local suite passed 87 tests, including the seven
reference-ligand controls. The documented example also passed independently.
Ruff, generated indexes, the three offline reporting checks and diff whitespace
validation passed. The working-tree changes remain uncommitted.

## Acceptance and bounds

Keep this report active for review of the API, scientific definition and controls.
The slice operates on prepared sources and existing poses; conformer generation,
alignment/search, consensus, structure-based construction and advanced backends
are subsequent work. Reusing legacy local chemistry was rejected because molecular
ownership belongs in MolSysMT. No commit or release closure is claimed.
