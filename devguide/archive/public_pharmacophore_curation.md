---
summary: Consolidate reusable cached-model selection, copying, extraction and constraint editing.
issue: uibcdf/pharmacophoremt#38
status: resolved
opened: 2026-10-04
closed: 2026-11-03
verification: measured
area: [modeling, curation, provenance]
guard: tests/test_curation.py
normative: devguide/pharmacophore_curation_workflow.md
blocked_by: []
supersedes: []
---

# Independent hypothesis variants and explicit constraint curation


## Source/API acceptance resolved — 2026-11-03

Functional acceptance is complete on clean producer
**404aa3829ac8d43bd6cb3c883f5547eb460857b0**. The
[new acceptance receipt](../evidence/curation_acceptance_20261103_summary.json)
retains **84 passed / zero failures, errors or skips** in the complete curation,
argument-contract, native model/site and pose-evaluation selection. Its eleven
new alias controls include nine failures before the correction and eleven
passes afterward. Default independent edits isolate repeated occurrences;
in-place edits require all occurrences of each selected shared object and retain
native identities. Invalid partial edits preserve sites, shapes, metadata, name
and score, even with optional digestion skipped and through the class setter.

All three existing cookbook blocks execute, preserving the seven original
status/coverage expectations, full source/model mappings, non-default-unit
persistence and actual attribution (zero cached uses, two edit items/two uses).
Full source/native/helper/test and distribution-metadata identities are unchanged
before/after both acceptance phases on current controlled providers. The strict
isolated curation-page build passes with an adjacent link-target stub; its initial
missing-target harness failure is retained. The complete archive retains runners,
models, evaluations, actual credits, source identities, initial install/helper
failures and original regression outputs. Historical October evidence below is
unchanged, including its failed full-suite Ackredit stability audit.

The durable guard is `tests/test_curation.py`, with the maintained
[curation contract](../pharmacophore_curation_workflow.md). This resolves #38's
cached-model source/API scope, not full current-suite, clean installed/public
Conda/platform, biological or performance qualification. Shared dependency
conflicts remain MolSysSuite #82; final-head hosted receiving remains #9.
#60's intentional molecular links and any independent molecular copying remain
separate MolSysMT-owned work. No provider source, dataset, science profile,
public dependency floor, addon or release changes. Earlier active/next statements
below retain their original dated context and are superseded by this resolution.

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

## Functional acceptance in progress — 2026-11-03

The authorized acceptance review found that repeated references to the same
native InteractionSite at distinct model indices allowed a partial in-place
edit to change an unselected occurrence. The public add method permits those
references. Nine new regression cases fail against the original implementation;
two companion controls already pass. The scoped contract now rejects partial
in-place alias selections before mutation, including through a class setter and
with optional digestion skipped. Default independent edits and in-place selection
of every occurrence remain supported, preserving source history and identities.
All eleven focused controls pass after the correction. The maintained workflow
and cookbook document the boundary; #60's molecular-link policy is unchanged.

Next run the complete curation/owning integration controls and all three existing
cookbook blocks against a committed producer, retaining current source/native
identities and separate historical receipts before deciding closure.
