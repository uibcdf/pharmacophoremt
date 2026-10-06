---
summary: Provenance serialization interprets literal identifiers as physical quantities.
issue: uibcdf/pharmacophoremt#25
status: active
opened: 2026-10-03
closed:
severity: high
verification: reproduced
area: [persistence, provenance]
guard: tests/test_contracts.py::test_detached_provenance_preserves_literal_strings_and_quantity_objects
normative:
blocked_by: []
supersedes: []
---

# Literal identity strings become quantity records in provenance

## What

`detached()` replaces literal strings that a unit parser recognizes with physical
quantity records. Source ligand IDs `"a"` and `"b"` become year and barn records.
An aligned-clique recipe therefore fails the independent assertion that its
prepared sources retain those declared identities in the returned joint supporters.

## How

The metadata copier calls `pyunitwizard.is_quantity(value)` before preserving
strings. That public predicate legitimately accepts unit expressions; metadata
serialization is not an input boundary declaring those strings to be quantities.

Bounded reproduction in the controlled source environment:

```python
from pharmacophoremt._private.molsysmt import detached
assert detached({'ligand_ids': ['a', 'b']})['ligand_ids'] == ['a', 'b']
```

The assertion failed before the local correction. Preserve immutable strings
before quantity-object detection; validated scientific quantities still use
PyUnitWizard's portable QuantityRecord. Test the owning copier plus delivered
reference/clique workflows and native saved models against the original IDs.

## Why

Source/support identities become corrupted even when a roundtrip test passes:
comparing loaded output to already corrupted producer metadata is insufficient.
The original labels must remain explicit strings across supported workflows.

## What is measured and what is assumed

**Reproduced, 2026-10-03:** Executing the first aligned-clique cookbook block failed
its `joint_ligand_ids == ['a', 'b']` assertion. Inspecting the returned records
showed units `year` and `barn`, each value 1. This is an observed local metadata
defect, not a PyUnitWizard predicate defect. After the local correction, all
three aligned-clique cookbook blocks execute successfully and the strict isolated
cookbook build passes. The final full suite passes **177 tests**, including the
regression guard and original-ID assertions for reference/clique models and native
persistence. The fix awaits review/commit; no historical saved record is rewritten.

Reproduce the guard with the checkpoint's controlled source providers on
`PYTHONPATH`:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest --receptor=llm -p no:cacheprovider -p no:rerunfailures tests/test_contracts.py::test_detached_provenance_preserves_literal_strings_and_quantity_objects
```

Provenance: local Linux source verification, 2026-10-03, Python 3.13.14;
PyUnitWizard source `2ffe1885675f47c76af03c08e51bc889a5e99a05`. The regression
compares original literal IDs and an independently decoded physical distance;
it does not merely compare two serialized copies.

**Additional reproduction and correction, 2026-10-04:** Native curation observations
contain NumPy string scalars. Preserving their subclass causes the old YAML writer
to emit Python object tags, which the safe reader rejects. The owning copier now
normalizes string subclasses to builtin strings without parsing their contents;
the native dictionary boundary detaches the full payload and YAML uses safe_dump.
The new original-text guard in `tests/test_curation.py` checks `"2 m"` and `"1 ps"`
as literal strings, portable YAML and complete original observation history.
Together with existing contract and class guards, 54 tests pass in 42.68 s on
Python 3.14.7. Historical evidence above remains unchanged. This extension is
linked in the [owning issue](https://github.com/uibcdf/pharmacophoremt/issues/25#issuecomment-5978214043).

The subsequent full tree passes 542 tests in 730.39 s on Python 3.14.7. Its source
audit detects concurrent Ackredit edits, with unchanged PharmacophoreMT,
MolSysMT snapshot and PyUnitWizard; the passing test result does not establish
four-provider fixed-source qualification. The three curation cookbook blocks
retain unchanged sources independently. Original audit, logs and complete model
evidence are indexed in `devguide/evidence/curation_py314_summary.json` and the
maintained curation contract.
The measured result is synchronized in the
[owning issue follow-up](https://github.com/uibcdf/pharmacophoremt/issues/25#issuecomment-5978374683).

## Alternatives and refuted paths

Changing fixture IDs avoids this example but leaves valid caller names vulnerable.
Loaded-versus-produced metadata equality alone cannot detect the corruption.
Restrict quantity interpretation at the owning serializer; do not change the
provider's valid string-expression API or special-case selected ligand names.

## Scope and exclusions

Consumer-owned provenance copying, identity-preservation guards and native model
evidence. No provider unit parser changes or repair of historical saved records.

## Acceptance criteria

Literal strings, including unit-looking text and NumPy string scalars, remain
strings. Real quantity objects remain portable with their physical values/units;
containers detach from inputs. Native consensus outputs and saved models preserve
original ligand IDs. Execute the regression guards and affected cookbook.
