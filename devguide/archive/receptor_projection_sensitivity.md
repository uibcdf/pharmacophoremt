---
summary: Qualify the first prespecified analytical receptor projection sensitivity matrix.
issue: uibcdf/pharmacophoremt#83
status: resolved
opened: 2026-11-04
closed: 2026-11-04
verification: measured
area: [modeling, screening]
guard: tests/test_receptor_sensitivity.py
normative: devguide/receptor_sensitivity_protocol.md
blocked_by: []
supersedes: []
---

# Analytical receptor projection sensitivity

## What and why

Continue audit item 12 with explicit receptor projection hypotheses. Distinguish
placement from matching tolerance, angle conventions, exclusions, requiredness,
weights and removal before interpreting real development results. Automatic
pockets, donor/acceptor geometry, preparation uncertainty and biological validity
are not delivered by a passing analytical case.

## How

Fix the complete declaration before execution. Reuse public receptor projection,
curation, exclusion and PoseEvaluator operations plus real MolSysMT recognition.
The unshipped case recorder reads settings, not expected answers; the guard checks
independent literal transitions. No molecular kernel, preparation/format routine,
provider patch, activity labels, search, replacement or holdout access.

## Measured and assumed

The [original protocol](../receptor_sensitivity_protocol.md) and parameter JSON
predate the first execution. Each policy has 45 valid cells and one actual failed
frame; 92 attempts are retained. Two authored disconnected charge/aromatic source
templates are mathematical controls, not independent receptor/ligand samples.
The observed unit-policy boundary failure is #84, not a fitted biological cutoff.

Final selected scope: 245 passed in 198.40 s, including 49 new guards, zero
failures/errors/skips. All five attempt source/native/test/input identity checks
remain stable. The full case preserves models, native results/attribution, source
coordinates, inventories, curation source and restored application units.

The first guard had incorrect QuantityRecord/curation field assumptions (23
failures/12 passes); corrected public-codec assertions leave three genuine unit
boundary failures/32 passes. A mistyped existing selector then exits 4 with zero
cases. Both broad corrected implementations pass 245 controls; the final review
uses the difference comparison to avoid expanding a maximal finite radius to
infinity. Original failures, exact test versions and both implementation overlays
remain in the [receipt/full evidence](../evidence/receptor_sensitivity_20261104_summary.json).

## Alternatives and limits

Do not tune the declared table, silently drop a failed cell, pool settings as
independent molecules or infer binding importance from removal. A radius is not
a physical atomic radius; coverage is not affinity. Molecular geometry stays
with MolSysMT; pocket detection with TopoMT. ArgDigest #47/#48 remain independent.

## Acceptance and continuation

The first analytical matrix and existing receptor/exclusion/curation contracts
pass with the original declaration unchanged. This resolves only this bounded
slice. Audit item 12 stays partial for real development cohorts, molecular
preparation variants, finite search and uncertainty. Next extend the declared
prepared-receptor case under a new prespecified development-only protocol;
provider #375/#323 and #66's experimental-method gate retain their scope.

Linux/Python 3.14.7 controlled-source evidence is separate from full-suite,
clean installed/public/all-platform, hosted and predictive qualification. Owners
LMMV/dprada; owned capsule `/tmp/phmt-receptor-sensitivity-20261104-ibrz8n8r`,
review 2026-11-18 or scientific/source change. No continuing local process.
