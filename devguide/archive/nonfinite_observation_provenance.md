---
summary: Undefined aromatic measurements fail consumer quantity provenance serialization.
issue: uibcdf/pharmacophoremt#35
status: resolved
opened: 2026-10-03
closed: 2026-10-09
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


## Resolution — 2026-10-09

The existing consumer correction is reviewed and accepted. It was already
published in `fdb57dcbe8e4d9d8364d1dcf5199a7945bfd9a2f`; this closure changes
regression guards, maintained guidance and evidence, with no runtime or provider
code change. The original report above retains its historical measurements.

The fresh selected integration run passes **73 tests in 35.25 s** on normal
editable Python 3.14.7, based on `cdf79fdd725d2ec383103e4940073abface26e4b` plus
the recorded test overlay. Four real parallel native profiles now persist through
both JSON and YAML with pm/fs/degrees writing and angstrom/ps/radians reading.
The assertions inspect the saved model's actual measurement, independently
confirm its 0.02 nm radius, preserve original atom/frame maps and compare source
immutability through the same unit conversion. Sealed readback additionally
preserves NaN, positive/negative infinity, negative zero and original units;
finite 1/2 angstrom values independently decode as 0.1/0.2 nm with unchanged
JSON representation. Nonfinite molecular coordinates still raise.

The existing aromatic driver passes tracking off/on, 14 case/profile combinations
and both ligand roles per setting. Positive and saved-model fits remain one;
displaced negatives remain zero and the expected strict compound-cation mapping
failure remains distinct. All three cookbook blocks execute and strict isolated
rendering passes. Seven producer Python source snapshots remain unchanged during
execution; the loaded molecular extension identity is retained. All seventeen
earlier compressed archives preserve their exact Git bytes.

The distinct full output is
`devguide/evidence/nonfinite_provenance_review_py314.json.gz`; its checksums,
producer identities, focused command, cookbook observations and limits are in
`devguide/evidence/nonfinite_provenance_review_py314_summary.json`. The maintained
contract is `devguide/aromatic_interaction_workflow.md`. Reporting/index guards,
Ruff and whitespace checks pass before publication.

This resolves consumer quantity provenance only. #34's broader workflow review,
MolSysMT #323 environmental hydrogen refinement, hosted matrix and public artifact
qualification remain separate. No new codec, changed detection threshold,
nonfinite site geometry or biological/performance acceptance is introduced.
