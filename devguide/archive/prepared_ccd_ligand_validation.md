---
summary: Traceable CCD ideal ligands for native preparation, refinement and consensus controls.
issue: uibcdf/pharmacophoremt#30
status: resolved
opened: 2026-10-03
closed: 2026-11-03
verification: measured
area: [modeling, screening, validation, attribution]
guard: tests/test_prepared_ccd_ligands.py
normative: devguide/prepared_ccd_validation.md
blocked_by: []
supersedes: []
---

# Prepared CCD ligand validation

## Resolution — 2026-11-03

Reviewed and incorporated as a source/API workflow. Clean producer
54df39ca4956335cf0d408b02a61f73ce97a0a96 passes all **23 owning controls**, zero
failures/errors/skips, in 75.27 s. The unchanged original driver passes all
**12 comparisons**, each replayed with host tracking disabled and enabled:
four self-recovery, two prepared-frame screening and six cross-ligand controls.
All four existing cookbook blocks execute and the strict isolated recipe renders.
The neighboring notebook is a link-target stub; actual notebook/full-site
execution is outside that render check.

Both original SDFs/manifest retain their checksums. Public MolSysMT preparation
preserves 44/40 atoms, 24/20 explicit H, charges, stereo, bond endpoints and
coordinates; raw aromatic-readiness rejection stays MSM-ERR-STRUCT-003. The same
14/20 full inventories, 5/6 self matches with 3/4 fits, requested frame accounting
and three bounded cross-ligand outcomes pass without expectation changes.
Scientific outputs agree with tracking off/on. Actual capture retains 21 items,
99 uses, both checksum-qualified CCD datasets and separate resource/method uses.

The [new receipt](../evidence/prepared_ccd_acceptance_20261103_summary.json)
retains complete driver output, actual citations, snapshots, commands and logs/XML.
Physical source/native/helper/test/input and distribution-metadata identities
remain equal in all three phases. The owned #69 system-site-packages venv resolves
ordinary editable PHMT 0.4.0+56.g9387852, controlled MolSysMT 0faf1584 and its
unchanged native extension. No runtime, test, input, expectation, provider, shared
prefix or sibling changes are needed. The Oct03 results below and dirty-producer
limits in the collection record remain historical; the instruction to await
review is superseded by this resolution.

This closes #30's prepared-input analytical/source acceptance. Ideal CCD geometry
remains distinct from experimental conformers, biological/affinity validation and
performance evidence. Shared dependency conflicts stay MolSysSuite #82;
source-free installed/public/Conda/platform qualification stays #23/#10 and
exact-head hosted receiving #9. The earlier 1,020-item full run is a dated baseline,
not execution of every later correction. #22/#66 and provider #323/#375/#447 retain
their separate scientific/delivery boundaries. Temporary root
/tmp/phmt30-acceptance-20261103-2mheqiv3/, owners LMMV/dprada, review 2026-11-17.

## What

Qualify untouched EST/DES CCD ideal SDFs and compose native traditional tools
on real molecular chemistry with explicit source, preparation and method evidence.

## How

Use public MolSysMT SDF/stereo conversion and its sanitizing RDKit roundtrip.
Audit molecular identity, chemical declarations and coordinates. Exercise public
feature extraction, ranked seeds, both refinement policies, explicit pair
evaluation, consensus and prepared-frame screening. The maintained contract
records exact hypotheses and expected outcomes.

## Why

Disconnected analytical controls cannot establish behavior on real donor/aromatic
chemistry. Input readiness and model-family/tolerance choices must be separately
reviewable before biological pilots or speed rankings.

## What is measured and what is assumed

All 23 real-provider controls pass in 74.99 s on Python 3.14.7, including prepared
frame screening and independent-step actual-tracking stability. Public preparation
retains 44/40 atoms and 24/20 explicit hydrogens; classical inventories contain
14/20 features. Both refinement policies recover 5/6 selected features under
proper motion with 3/4 fits. Cross-ligand hypotheses differ with families and
tolerances, as recorded in the contract. These are computational observations,
not biological truth labels, experimental conformations or a timing benchmark.

The full suite passes **319 tests in 346.44 s**, with the same two known warnings.
All four cookbook blocks execute on Python 3.14; strict isolated rendering passes
with existing 3.13 documentation tooling. All 12 retained comparisons pass with
stable attribution-excluded scientific projections, unchanged input/provider
source hashes, preserved preparation/source state and coordinates, and real
resource/method citations. Full evidence and its checksum-qualified summary are
stored under `devguide/evidence/`. The four earlier archives remain unchanged.
Results are synchronized in
[the owning issue's evidence comment](https://github.com/uibcdf/pharmacophoremt/issues/30#issuecomment-5970332874).
The issue remains open pending review/incorporation of the working changes.

## Alternatives and refuted paths

Native SDF reading alone retains unknown aromatic metadata and rejects classical
recognition. PHMT must not fill flags or sanitize outside the provider. Removing
donors or relaxing angular constraints changes the hypothesis rather than proving
the stricter one valid. Citation nodes attached by independent public steps must
be preserved in full evidence and excluded from a scientific-only comparison.

## Scope and exclusions

Traceable independent ligand reference data, public molecular preparation,
traditional tool composition and actual data/method attribution. No repair of
the experimental 1QKU ligand, new hydrogens, de novo conformers, docking,
receptor validation, biological enrichment or public distribution qualification.

## Acceptance criteria

Source/identity/chemistry preservation and both self policies pass; input
readiness failure never becomes a score; public consumers retain frame identity
and accounting; declared cross-ligand controls pass; actual citations and
attribution-independent science are retained; execute cookbook blocks and pass
scientific/reporting/quality checks. Keep the issue open until review/incorporation.
