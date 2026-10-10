---
summary: Qualify cached ERalpha receptor projections, exclusions and observed-contact model reconstruction.
issue: uibcdf/pharmacophoremt#52
status: resolved
opened: 2026-10-10
closed: 2026-10-10
verification: measured
area: [modeling, screening, validation, io]
guard: tests/test_prepared_receptor_workflow.py
normative: devguide/prepared_receptor_workflow.md
blocked_by: []
supersedes: []
---

# Prepared receptor continuation

## What

Review explicit cached receptor hypotheses and observed-contact reconstruction
on the existing checksum-qualified prepared ERalpha fragment.

## How

Public MolSysMT reads the archived H5MSM, selects PHE404/EST, extracts native
ring/heavy-atom observations and translates synthetic controls. Existing PHMT
projection, exclusion, complex-facade, persistence and placed-evaluation tools
consume those observations. Reuse the existing workflow recorder.

## Why

Prepared receptor routes need independent placement, exclusion-veto and original
map controls in addition to known site counts. Empty native families and failed
uncached-frame rebuilds must not be disguised as successful positive queries.

## What is measured and what is assumed

Seven corrected new guards pass (122.44 s); 133 unchanged relevant controls
passed in the initial broader selection, whose seven setup failures remain
retained as history. The client initially expected a PHMT exception for the
provider out-of-range frame; correct provider propagation is now captured and
existing-frame native invalidation is independently checked. Original fragment/chemical-state/template/H-generation
choices remain historical provenance; this stage consumes the prepared artifact,
without repeating preparation, detection or environmental refinement.

## Alternatives and refuted paths

No direction inference, molecular kernel, implicit pocket detection, hydrogen
regeneration or binding-mode optimization is added. Synthetic moved PHE404 is a
methodological candidate, not an activity-labeled ligand.

## Scope and exclusions

Bounded cached prepared-fragment acceptance, not full receptor/biological,
performance or hosted/public qualification. MolSysMT #375/#323/#350/#367 and
PHMT #23 remain separate. Maintainers LMMV/dprada own the case.

## Acceptance criteria

Independent original atom/geometry/projection/exclusion controls, unchanged
native chemistry/history/observations, cached empty-family reconstruction,
empty-versus-failed model semantics, codec/unit/fresh-reader maps, actual input
attribution and a new immutable original run identity preserving prior archives.

## Measured completion — 2026-10-10

The [new original summary](../evidence/prepared_receptor_workflow_py314_summary.json)
links full reports/outcomes/artifacts, executed developer/test source overlay,
original initial failed-selection/client/guard history and actual references.
Both host tracking modes pass with stable scientific fields and unchanged
producer/input identities. Positive placement, original/opposite negatives,
coverage-one exclusion veto, native contact/source-distance controls, empty/
exclusion-only refusal and three cleared-result failure routes pass. Twelve
saved models retain maps across codecs/units and fresh readers register zero uses.

Both public recipe blocks and reviewed installed-development preflight pass.
The reusable stdlib archive-byte operation delegates existing identity checks;
MolSysMT performs all molecular decoding. All 31 original JSON gzip archives and
the prepared native input are byte-identical. Host-on captures twelve items/36
uses and the actual artifact dataset; host-off three provider items/three uses.
Final reporting/archive/rendering and source/native rechecks are retained in
the completion receipt. No runtime scientific or sibling source changes occur.
