---
summary: Delegate annotated pharmacophore SDF container handling to MolSysMT.
issue: uibcdf/pharmacophoremt#74
status: blocked
opened: 2026-11-04
closed:
verification: inspected
area: [architecture, io]
guard:
normative: devguide/persistence_fidelity.md
blocked_by: [uibcdf/molsysmt#215]
supersedes: []
---

# Delegate the annotated SDF molecular container to MolSysMT

## What

At 83e13bd, `io/sdf.py` directly constructs RDKit atoms/conformers, reads/writes
SD files/properties and inspects atoms/bonds/coordinates. PHMT should own only its
pharmacophore schema and payload. Molecular containers belong to MolSysMT.

## How

Consume a supported public MolSysMT record/property/construction route when
available. Keep both SD tags, site order, empty models, explicit geometry units
and existing @1 constraints. Use no provider-private helpers or local parser.

## Why

The maintainer explicitly includes every molecular form/format in MolSysMT's
responsibility. The previous #47 semantic fix does not establish this ownership.

## What is measured and what is assumed

Source inspection only for provider 71fbe4f46d3c70e4e973c8025f01752a8c9b1084:
`file:sdf` conversions exist but `_native.to_native` refuses properties without
explicit loss. An identity copy cannot create an annotated record or expose its
properties. Consumer requirements are handed to existing MolSysMT #215.
No provider source/environment is modified or a new installed route qualified.

## Alternatives and refuted paths

Do not discard tags, parse SD blocks locally, call private CTFile helpers, or
extend direct RDKit container code. Existing qualified files retain the legacy
reader pending a compatible replacement; native JSON/YAML remain independent.

## Scope and exclusions

Migrate molecular container operations, preserving PHMT's schema. No chemical
preparation, screening-library export, new SDF dialect or payload schema redesign.

## Acceptance criteria

Public provider construction/read/write/property/geometry/count inspection,
including zero sites; actual provider round trips; unchanged scientific payload
semantics; visible unsupported-input failure; no direct molecular backend here.
LMMV/dprada own migration. Review 2026-11-18 or at provider availability. Existing
implementation is frozen debt, not compliance. See ../persistence_fidelity.md.
