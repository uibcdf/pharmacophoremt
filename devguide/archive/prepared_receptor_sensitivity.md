---
summary: Qualify prespecified sensitivity on the cached prepared ERalpha receptor geometry.
issue: uibcdf/pharmacophoremt#85
status: resolved
opened: 2026-11-04
closed: 2026-11-04
verification: measured
area: [modeling, screening]
guard: tests/test_prepared_receptor_sensitivity.py
normative: devguide/prepared_receptor_sensitivity_protocol.md
blocked_by: []
supersedes: []
---

# Prepared receptor sensitivity

## What, how and why

Extend #83/#84's analytical sensitivity to #52's unchanged prepared ERalpha
fragment. Prespecify placement, radius, exclusions, rotated aromatic orientation,
original-pose contrast and exclusion-removal choices before evaluation. Reuse
the existing native archive loader and public MolSysMT molecular operations;
PHMT constructs/evaluates/curates the explicit pharmacophoric hypotheses.

The [original protocol](../prepared_receptor_sensitivity_protocol.md) and
complete parameter declaration are fixed before execution. Independent test-only
coordinate/plane/distance oracles do not feed expected answers to recognition.
No molecular kernel, format/preparation routine, provider edit or runtime API
change is introduced.

## Measured and assumed

Each complete matrix has 31 valid fixed-pose settings plus one actual failed
frame per unit policy: 64 attempts under nm and pm. Transformed PHE404 is a
methodological candidate, not another ligand/conformer or predicted binding
pose. The fragment's historical preparation and full-receptor/environmental-H
limits remain. Molecular input SHA-256 is preserved; all source coordinates,
chemical-state history, cached observations and native inventories are unchanged.

Exclusion radii .01/.20/.40 nm yield 0/5/47 sphere-atom clash pairs, involving
0/3/11 candidate atoms; positive coverage remains one. Both axes of the rotated
aromatic control follow the independently calculated folded angle about
36.07 degrees: 1/30-degree tolerances refuse and 60/90 accept. Removing the
exclusions preserves coverage and records the deliberate hypothesis change.
Neither a clash count nor these cutoff transitions estimates physical preference.

**288 selected controls pass in 442.24 s, including 43 new guards**, zero
failures/errors/skips. The standalone command independently executes all 64
attempts. Three recorded identities remain stable: initial pytest uses the
inherited nine-provider footprint; final pytest/CLI additionally record NumPy,
SciPy and RDKit source/native identities (12 providers). The initial 43 controls
pass 41/fail two solely because the new guard compares an internal legacy
snapshot against the tagged export. Correcting only that envelope comparison
preserves every model field and all independent oracle code/expected tables.
Original guards, outputs and correction are retained in the
[receipt/full evidence](../evidence/prepared_receptor_sensitivity_20261104_summary.json).

## Alternatives, acceptance and remaining work

No failed cell is replaced, imputed inactive or pooled as an independent molecule.
No arbitrary local direction, first-neighbor fallback, new H refinement or pocket
detector is used. Source bytes, native causes, actual input-data/operation credit,
curation source and application policy are preserved. The declared analytical
transitions and existing receptor/sensitivity/exclusion/curation regressions pass.

This completes only the bounded prepared-geometry slice. Audit item 12 remains
partial for real cohorts, molecular preparation/search variability and uncertainty.
Next inspect actual TopoMT pocket and MolSysMT geometry contracts before declaring
a receptor hypothesis-generation pilot; missing reusable capabilities go to their
owning issues. #375/#323, #66, #74/MolSysMT #215, #82/ArgDigest #47/#48 and broader
#6 retain their separate scope. Source evidence is not full-suite, clean
installed/public/all-platform, hosted, biological or performance qualification.

Owners LMMV/dprada; capsule `/tmp/phmt-prepared-sensitivity-20261104-nnrjbt1y`,
review 2026-11-18 or source/scientific change. No continuing local process.
