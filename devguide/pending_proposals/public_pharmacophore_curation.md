---
summary: Consolidate reusable cached-model selection, copying, extraction and constraint editing.
issue: uibcdf/pharmacophoremt#38
status: active
opened: 2026-10-04
closed:
verification: measured
area: [modeling, curation, provenance]
guard: tests/test_curation.py
normative: devguide/pharmacophore_curation_workflow.md
blocked_by: []
supersedes: []
---

# Independent hypothesis variants and explicit constraint curation

## What

Expose selection, copying, extraction and editing as separate reusable tools.
Class convenience methods delegate to the public editor. Keep Feature + Shape
geometry, source observations and original bibliography independently traceable.

## How

Use local site indices and exact cached names; deep-copy native sites and metadata,
retain the opaque molecular-system reference, and validate all edits before
committing in place. Extraction and editing retain a complete native source-model
snapshot and explicit site mapping, invalidate the score, and distinguish radius
from Gaussian sigma. Optional Ackredit captures actual edits; pure copying and
extraction preserve earlier citations without attributing another detection.

## Why

Classical modeling needs alternative constraints without silently changing the
original evidence or embedding molecular manipulation in PharmacophoreMT.
Weight, essential status and steric exclusion have independent meanings.

## What is measured and what is assumed

The initial focused run passes 54 tests in 42.68 s on Python 3.14.7: 36 curation
controls plus existing contracts and class controls. These include real native
MolSysMT observations, independent pose evaluation, atomic invalid-input rejection,
copy isolation, source-model history, non-default-unit JSON/YAML persistence,
actual Ackredit capture and genuine backend absence/failure. A YAML guard exposed
NumPy string scalars emitted as Python objects; the shared literal-text/native
serialization fix is tracked in PharmacophoreMT #25.

These are local development controls, not biological validation, weight learning,
performance benchmarking or distribution qualification. Three cookbook blocks
execute on Python 3.14.7 with unchanged recorded producer hashes, and strict
isolated rendering passes with existing Python 3.13 documentation tooling.
The retained original recipe audit includes the complete original/edited native
models, seven evaluation results, exact runner, source identities and actual
capture: two items/two uses for radius editing, no uses for cached steps. Its
summary is `devguide/evidence/curation_py314_summary.json`.

The complete suite passes 542 tests in 730.39 s with eight existing warnings.
Its separate source audit fails because Ackredit changes during execution;
PharmacophoreMT, the verified MolSysMT snapshot and PyUnitWizard remain unchanged.
The retained integration audit/log explicitly preserve this limitation. The
independently stable cookbook result qualifies its recorded producer sources;
the complete run is not fixed-provider qualification. Editable installation in
`molsyssuite@uibcdf_3.14` is confirmed without a PYTHONPATH override. Existing
historical archives remain unchanged; all fourteen original archives verify.
The result and review scope are synchronized in the
[owning issue comment](https://github.com/uibcdf/pharmacophoremt/issues/38#issuecomment-5978371613).

## Alternatives and refuted paths

Do not duplicate editor behavior in class setters, interpret Gaussian width as a
radius, infer a user's preferred weights, or treat a zero weight as removal of an
essential/steric constraint. Preserve caller alternatives rather than imposing an
automatic fit. Do not implement molecular copies or coordinate changes locally.

## Scope and exclusions

Native cached models with native-serializable history. No molecular preparation,
new detector, ligand geometry, consensus algorithm, fitting to activity labels,
shape evaluation extension or automatic repair of historical saved records.
Native bounded participant reuse precedes curation; generic keep composition
can combine curated models. No concurrent-thread atomicity claim.

## Acceptance criteria

Independent public tools with documented contracts; class delegation; complete
source evidence, before/after values and mapping; score invalidation; strict
quantity/boolean/weight/index validation; preservation of other shape parameters;
independent evaluation of geometric, essential, weighted and excluded constraints;
safe native persistence; honest optional attribution; executable cookbook and
integration evidence linked to the owning issue. Keep the report active for review.
