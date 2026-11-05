---
summary: Qualify bounded receptor hypotheses from cached native donor and ring geometry.
issue: uibcdf/pharmacophoremt#86
status: resolved
opened: 2026-11-04
closed: 2026-11-04
verification: measured
area: [modeling, validation]
guard: tests/test_receptor_hypothesis_pilot.py
normative: devguide/receptor_hypothesis_pilot_protocol.md
blocked_by: []
supersedes: []
---

# Receptor hypothesis-generation pilot

## What, how and why

Prespecify and execute a fixed PHE404 receptor hypothesis-generation case after
#85. Existing cached MolSysMT donor vectors and aromatic axes supply geometry;
PHMT supplies complementary pharmacophoric projection choices and separate
alternatives. No molecular capability is duplicated.

The [protocol](../receptor_hypothesis_pilot_protocol.md) and complete declaration
fix eight joint hypotheses, full/truncated/zero budgets, unit policies and
independent original-coordinate controls before evaluation. One position-only
acceptor is explicitly omitted; ideal acceptor adoption and optional pockets
retain MolSysMT #375 and TopoMT #101 ownership. No public runtime/API, dependency
or preparation change is planned in this bounded case.

## Measured acceptance and original failures

**110 selected controls pass in 191.26 s, including 34 new guards**, zero
failures/errors/skips. All eight separate two-site hypotheses follow independent
raw-coordinate vector/plane oracles. Synthetic supplied-pair controls each match
one .35/.35 face alternative; reversed axes preserve answers and incompatible/
orthogonal controls fail. Budgets 8/3/0 retain remaining 0/5/8 and distinguish
incomplete empty output from exhausted or inapplicable cases. Cached generation
works with molecular access blocked and independent result metadata.

The standalone runner also completes both unit-policy cases. JSON/YAML preserve
exact evidence/constraints and geometry within 1e-12 nm/unit. Original coordinates,
full chemical history, cached observations, inventories and application units
remain unchanged. Three complete before/after identity checks are stable.
The [receipt/full original evidence](../evidence/receptor_hypothesis_pilot_20261104_summary.json)
retains actual input/registered-operation credit, native geometry provenance,
complete and truncated runs, literal persistence flags and real failed frames.

Initial selection: 31 pass, three new harness assertions fail; exact identities
remain stable. Geometric oracles and pair outcomes pass. The replay guard wrongly
treats serialized QuantityRecord metadata as a hydrated native cache; it now
obtains a real public producer inventory before blocking molecular access.
The pm roundtrip differs only by ordinary float64 center roundoff (an inspected
example changes 1.765312249432465 to 1.7653122494324647 nm). Reuse the established
exact-evidence/1e-12-geometry oracle, retaining literal-equality flags separately.
The attribution guard now checks actual captured provider/software credit and
the separate native vector provenance, without assuming an unregistered function
is present in the credit tree. Frozen declarations and independent geometric
expectations remain unchanged. Original
failures stay in the receipt. Settings and feature clouds establish no biological
validity or sample size.

## Remaining scope

This completes only the fixed unshipped generation pilot. Next design the explicit
public cached-generation contract; further direction chemistry requires a new
admitted provider profile/declaration. TopoMT #101 is optional; MolSysMT #323
environmental refinement is separate. No runtime/provider/pin/floor/preparation
change or new biological/installed/public/hosted qualification occurs. Broader
audit 12 and #6, #66, #74/MolSysMT #215 and #82/ArgDigest #47/#48 stay open.

Owners LMMV/dprada; capsule `/tmp/phmt-receptor-pilot-20261104-gmfqhead`, review
2026-11-18 or source/scientific change. No continuing local process is required.
