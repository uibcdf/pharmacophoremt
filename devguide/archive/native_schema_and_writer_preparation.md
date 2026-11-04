---
summary: Version native schemas and encode pharmacophore exports before destination opening.
issue: uibcdf/pharmacophoremt#76
status: resolved
opened: 2026-11-04
closed: 2026-11-04
severity: medium
verification: measured
area: [io, api]
guard: tests/test_native_schema_writing.py
normative: devguide/native_schema.md
blocked_by: []
supersedes: []
---

# Native schema admission and writer preparation

## Resolution — 2026-11-04

New JSON/YAML use pharmacophoremt.native@1 with explicit complete model/site/shape
fields. Unknown explicit schemas and unknown/missing fields are refused, while
untagged historical files retain their compatibility path. Producer version is
not schema version. Writers validate through existing native/public value checks
and completely encode text before opening a destination. No general filesystem
transaction framework is introduced. SDF source/private legacy payload unchanged.

[Receipt](../evidence/native_schema_writing_20261104_summary.json) retains 265
passing focused cases, exact overlays and stable identities for all three runs.
Original guards: 48 fail / 4 pass; first broader run: 253 pass / 6 comparisons
need separate native/SDF envelopes. Those tests retain all scientific-field
comparisons and explicitly guard unchanged SDF payload. Final 58 new cases include
tagged nonfinite rejection and untagged extension compatibility. Source receiving
only; full-suite, installed, platform and predictive gates remain separate.

## What

Base 0413e6c uses producer version without native schema admission. Extra fields
can be ignored. JSON/YAML writers open destinations before encoding finishes,
so an unsupported metadata object can truncate an existing file or leave a partial
new destination. Mutated invalid scientific values may also be saved.

## How

Give a valid model an object-valued metadata item and attempt export over known
bytes or an absent destination. Native guarded files also accept an explicit
unknown schema marker or ignore new model/site/shape fields on original code.

## Why

Silent field loss and overwritten saved work compromise reproducibility.
Pharmacophore schema/constraint validation belongs to PHMT; molecular formats
and operations remain MolSysMT-owned.

## What is measured and what is assumed

Real JSON/YAML encoding and file checks, six-shape/native metadata/unit/default/
SDF compatibility controls; Linux/Python 3.14.7 with public ArgDigest 0.17.0 and
inherited scientific dependencies. No provider source/environment is changed.

## Alternatives and refuted paths

Do not treat producer versions as schema identifiers or silently revise SDF @1.
Use existing scientific validators; no duplicated molecular parser or new generic
filesystem transaction engine. Historical untagged compatibility stays explicit.

## Scope and exclusions

Tagged native admission and destination preservation for validation/serialization
errors. Disk/write failures, crash durability and concurrent writers are excluded.
Unknown legacy fields still lack a lossless automatic migration guarantee.

## Acceptance criteria

Tagged fields/version/schema/metadata and legacy compatibility guards; invalid
export preserves existing bytes/absent paths; successful calls keep API behavior;
SDF source/payload unchanged; exact evidence and maintained native schema contract.
Broader translator field fidelity and #74/MolSysMT #215 remain separate work.
