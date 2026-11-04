---
summary: Reject silently ignored options in native io.load routes.
issue: uibcdf/pharmacophoremt#73
status: open
opened: 2026-11-04
closed:
severity: medium
verification: measured
area: [api, io]
guard:
normative: devguide/support_library_boundaries.md
blocked_by: []
supersedes: []
---

# Native loader silently ignores extra options

## What

`io.load(file_name, **kwargs)` succeeds with an unknown keyword on native JSON
and YAML branches. Direct `load_json` and `load_yaml` reject it with TypeError.
The facade can therefore hide a typo while returning a plausible model.

## How

Write an empty Pharmacophore using `to_json`, then call
`load("empty.json", typo_probe_option="must refuse")`; it currently succeeds.
`load_json("empty.json", typo_probe_option="must refuse")` raises TypeError.
Repeat with `to_yaml`, `.yaml` and `load_yaml`: the same discrepancy occurs.
The [original receipt](../evidence/native_geometry_contract_receiving_20261104_summary.json)
retains load_options_probe.py, both inputs, hashes, full results and before/after
identities. No loader source is modified by the separate #6 geometry work.

## Why

Unknown public options should be refused visibly rather than silently discarded.
ArgDigest owns reusable admission/normalization; PHMT owns its format dispatch.

## What is measured and what is assumed

Both real native formats reproduce on unchanged io/__init__.py from b0a8f7e
with the exact #6 geometry overlay, public ArgDigest 0.17.0 and controlled inherited
scientific dependencies on Linux/Python 3.14.7. Source identities remain stable.
No molecular input or preparation is used. PML/Pharmer branches are inspected
candidates, not executed cases. No installed/all-minor qualification is inferred.

## Alternatives and refuted paths

The direct readers already refuse the unknown argument; the loss occurs in the
facade's dispatch. Do not repair it by accepting arbitrary options downstream.

## Scope and exclusions

Correct native pharmacophore format admission while preserving valid calls.
MolSysMT owns molecular loading/conversion and its supported options. Do not
copy its option registry or engine. Method-dependent model domains remain #6.

## Acceptance criteria

Add real JSON/YAML regression guards, assess other pharmacophore routes, visibly
refuse unknown options and preserve valid formats/direct-reader diagnostics.
Keep molecular calls delegated with meaningful provider failures. Close only
with the implemented guard and executed evidence; the current probe is a confirmed
finding, not a fix. Accountable maintainers: LMMV/dprada.
