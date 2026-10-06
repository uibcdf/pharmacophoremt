---
summary: Undefined aromatic measurements fail consumer quantity provenance serialization.
issue: uibcdf/pharmacophoremt#35
status: active
opened: 2026-10-03
closed:
severity: medium
verification: measured
area: [provenance, quantities]
guard: tests/test_aromatic_interactions.py::test_sealed_nonfinite_provenance_preserves_values_and_finite_compatibility
normative: devguide/aromatic_interaction_workflow.md
blocked_by: []
supersedes: []
---

# Preserve undefined observation quantities

## What

Native parallel aromatic profiles return an undefined intersection distance as
NaN. PharmacophoreMT's detached quantity provenance used the default JSON record
encoding, which rejected that measure and prevented otherwise valid construction.

## How

Use `QuantityRecord.from_quantity(value).to_dict(encoding='base64')` only for
nonfinite quantities, through the existing shared detached-provenance utility.
Leave finite quantities in their existing JSON representation. Public provider
observations and the sealed reader remain the source of values and units.

## Why

An undefined diagnostic measure is not a missing molecular site, a zero distance
or a reason to lose other contact measurements. Sealed binary records already
support these values, so no new codec or provider workaround is needed.

## What is measured and what is assumed

The focused 97-test run passes on Python 3.14.7, including actual parallel native
observations and sealed NaN/infinity/signed-zero round trips. Finite representation
compatibility, units, literal strings and finite molecular geometry guards are
checked. The full local integration suite passes 444 tests in 436.36 s with
eight known warnings. The reproducible driver passes tracking off/on; all three
cookbook blocks execute and strict isolated rendering passes. Complete original
evidence, source identities and hashes are retained with the owning workflow.

The [owning issue result](https://github.com/uibcdf/pharmacophoremt/issues/35#issuecomment-5974432239)
records the executed correction and checks.

## Alternatives and refuted paths

Do not replace NaN with zero/null, relax finite site geometry, emit nonstandard
bare JSON NaN, or add an unrelated bespoke quantity encoding. Encoding belongs
to `to_dict()`, not `from_quantity()`.

## Scope and exclusions

Consumer provenance quantities only. This does not license nonfinite molecular
coordinates or change detection criteria. General bare array encoding is outside
this fix; detached native driver measurements have explicit quantity-column units.

## Acceptance criteria

Actual native observations construct/persist, sealed readback preserves values
and units, finite metadata retains its prior representation, and scientific
geometry still rejects nonfinite inputs. Keep active pending review.
