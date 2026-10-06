---
summary: Construct native charge queries from ionic observations through shared feature tools.
issue: uibcdf/pharmacophoremt#33
status: active
opened: 2026-10-03
closed:
verification: measured
area: [modeling, interactions]
guard: tests/test_ionic_interactions.py
normative: devguide/ionic_interaction_workflow.md
blocked_by: []
supersedes: []
---

# Native ionic observation queries

## What

Extend the reusable public `from_interactions()` tool with essential positive/
negative charge spheres from native MolSysMT ionic observations.

## How

Validate the provider's explicit formal-charge rule/state, whole cross-boundary
participants and recorded ligand charge. Call public `get_features()` for shared
membership and geometry through MolSysMT; retain detached observation/recognition
evidence and aggregate repeated contacts. Compose with existing PoseEvaluator,
native query persistence and public exclusions.

## Why

Charge features already exist in reference-ligand modeling and evaluation. This
extension lets observed-complex hypotheses select charge sites using detected
contacts without creating a separate chemical definition or screening route.

## What is measured and what is assumed

The initial 33 focused tests (23 new ionic controls and 10 existing placed-pose
controls) pass on Python 3.14.7 in 21.05 s. Final exclusion composition, cookbook,
retained driver evidence and broader regression verification are recorded below
after execution. No biological or performance claim follows from analytical
fixtures; source identity and unchanged common frame remain caller declarations.

## Alternatives and refuted paths

Using the first charged atom or the full membership centroid fails the compound
geometry contract. Local charge recognition/detection would duplicate MolSysMT.
Minimum-contact distance and pharmacophore matching radius remain independent.
Alternative future chemical definitions need their explicit contracts; rejecting
an incompatible rule is not evidence that its scientific approach is inferior.

## Scope and exclusions

Prepared native ionic observations and their pharmacophoric interpretation.
No receptor preparation, energy scoring, conformer generation, automatic method
registration, new aromatic mapping or migration of legacy direct-RDKit routes.
The native minimum-distance criterion has no declared method paper; actual
software references and cached provider bibliography are retained without
inventing method credits.

## Acceptance criteria

Whole atomic/compound centers in either role, shared provider geometry, repeated
contact aggregation, independent pose negatives, incompatible-input guards,
unit-policy and persistence controls, actual optional attribution/reuse/readers,
executed cookbook recipe, reproducible analytical evidence and retained existing
hydrophobic/H-bond behavior. Review/incorporation and public qualification remain
open after local execution.

## Executed verification — 2026-10-03

The final ionic module contains **24 controls**, including the independent public
exclusion composition and source geometry mapping. The expanded set passes
**77 tests in 46.14 s**, with the two pre-existing attribution/legacy-unit warnings.
The complete suite passes **402 tests in 401.75 s** on Python 3.14.7, with the
same eight warnings: six expected B-factor drops, one deliberate attribution
failure and the legacy unit-stripping warning.

All three cookbook blocks execute on Python 3.14.7. Strict isolated cookbook
Sphinx rendering passes with the existing Python 3.13 documentation tools.
Ruff, reporting/index, three offline reporting tests and whitespace checks pass.
The editable installation is confirmed in `molsyssuite@uibcdf_3.14`.

The driver builds six queries and evaluates 18 poses per host-tracking profile:
all reference/round-trip controls match at fit one, and all displacements are
valid negatives at fit zero. Geometry, membership, repeated-contact evidence and
JSON metadata persist; input coordinates and producer sources stay unchanged.
On/off profiles retain identical scientific results. The enabled capture has
9 items/18 uses; the host-disabled profile retains the provider's one item/one
use. Optional host tracking is distinct from global provider tracking.

Original retained evidence: `devguide/evidence/ionic_interactions_py314.json.gz`,
uncompressed SHA-256
`e5d39bfd99cbb34cf52accd25ed22211e28d7491abde52958775e5262a913118`.
Its summary preserves original producer/extension/source identities and compact
outcomes. All ten original archives verify; earlier evidence was not overwritten.
No runtime/memory benchmark, biological result, public wheel or hosted matrix is
qualified. Scientific/API review and incorporation remain open.
