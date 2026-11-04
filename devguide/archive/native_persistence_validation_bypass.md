---
summary: Validate external native pharmacophore shapes and sites on loading.
issue: uibcdf/pharmacophoremt#75
status: resolved
opened: 2026-11-04
closed: 2026-11-04
severity: high
verification: measured
area: [io, scientific]
guard: tests/test_native_persistence_validation.py
normative: devguide/persistence_fidelity.md
blocked_by: []
supersedes: []
---

# Native loading bypasses scientific value validation

## Resolution — 2026-11-04

Native reconstruction now calls the existing public shape/site constructors with
normal ArgDigest value validation, and reuses the metadata digester. Only adding
an already validated site keeps an internal bypass. No new validation engine or
molecular operation is introduced. 207 focused controls pass; 48 new cases cover
invalid values, six geometries, constraints, metadata, units and legacy defaults.
[Exact evidence and all attempts](../evidence/native_persistence_validation_20261104_summary.json)
retain the original probe, 34 original refusal failures, 12 initial floating-point
assertion mistakes, intermediate identity/test correction and stable final run.
The correction also applies when an already validated SDF payload reaches native
reconstruction; SDF container code is unchanged and migration remains #74.

## What

On base 83e13bd7d5fbcf42ca10dad1ebeb76cdfe47ae97, `_from_dict` creates shapes
and InteractionSite with skip_digestion=True. A measured four-case probe accepts
negative weight, string essential status, negative radius and two-component center.

## How

Mutate those fields in a valid native dictionary or JSON/YAML file and load it.
All four original cases return a one-site model. Public constructors already
provide the checks that were bypassed at this external-input boundary.

## Why

Malformed scientific constraints produce plausible objects; for example a string
"false" is truthy. File contents do not establish a validated internal object.

## What is measured and what is assumed

Linux/Python 3.14.7, extracted public ArgDigest 0.17.0 and inherited scientific
dependencies. Final source/native/metadata identities stay stable. Source receiving
does not establish full-suite, clean installed, all-platform or predictive results.

## Alternatives and refuted paths

Reuse public constructors/metadata validation, rather than duplicate their checks
or trust arbitrary files as prevalidated. MolSysMT is not responsible for PHMT
site constraints; it retains all molecular inspection/manipulation/format ownership.

## Scope and exclusions

Native reader scientific admission; valid fields, units and legacy defaults.
Producer versions remain separate from schema versions. No new file schema,
writer transaction policy, molecular parser or SDF container extension is claimed.

## Acceptance criteria

Real JSON/YAML refusal and valid six-shape/metadata/unit/default guards pass.
No returned partial model. Exact failures/overlays and unchanged provider identity
are retained. Broader native schema/fidelity policy stays audit item 4 follow-up.
