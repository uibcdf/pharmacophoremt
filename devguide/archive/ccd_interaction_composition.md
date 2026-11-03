---
summary: Validate joint native interaction hypotheses with complete prepared CCD chemical components.
issue: uibcdf/pharmacophoremt#37
status: resolved
opened: 2026-10-04
closed: 2026-11-03
verification: measured
area: [validation, interactions]
guard: tests/test_ccd_interactions.py
normative: devguide/ccd_interaction_workflow.md
blocked_by: []
supersedes: []
---

# Real chemical components in controlled interaction workflows

## Source/API acceptance resolved — 2026-11-03

All 30 original CCD guards pass within the one 219-case coupled source selection
at clean producer **9387852af67a17f59e48d14fc78260ffc4320650**, receiving #36's cached
provenance correction. This is not a separate standalone 30-case execution. No
additional runtime/test changes or molecular implementation were needed for #37.
The [new receipt](../evidence/ccd_interaction_acceptance_20261103_summary.json)
retains the unchanged coupled run and fresh complete driver/cookbook evidence.

The driver passes both host-tracking profiles with eight primary role hypotheses
and 48 pose evaluations each. All four EST/DES/placement cases retain original
chemistry, explicit H, source atom/bond identities, coordinates and file bytes,
neutral covered-empty charge families, profile reuse and independent essential/
steric semantics. DES ring-offset still has one exclusion clash in either role
despite positive fit one. Donor-H negatives and the unchanged partner control,
fresh common-frame detection and nondefault-unit persistence all pass. Scientific
projections agree across tracking; actual captures retain 9 items/28 uses off and
17 items/57 uses on. All three existing cookbook blocks execute and the isolated
strict page build passes with adjacent link-target stubs.

Full code/native/helper/test/input and metadata identities are stable in the
current workflow/cookbook and original coupled-test phases. This uses ordinary
editable PHMT `0.4.0+56.g9387852` with controlled MolSysMT 0faf1584, Viewer ca7ebea6,
DepDigest 13cc7378 and unchanged native bytes in the owned #69 venv. The earlier
anonymous provider snapshot and failed live-source stability audits remain their
original historical evidence, not descriptions of this current source route.
No canonical-prefix/sibling mutation or new provider minimum is introduced.

The durable guard is `tests/test_ccd_interactions.py`, with the maintained
[workflow](../ccd_interaction_workflow.md). Original October source/data/results
remain unchanged. The full 1,020-item baseline at 96f917a does not execute #36's
new correction; current receiving is the 219-case selection plus the complete
recorded driver/examples. Exact-head hosted CI remains #9; clean installed/public/
Conda/platform gates stay #23/#10 and shared conflicts #82. Designed CCD pairs
are not observed biological complexes, pH choices or performance benchmarks.

## What

Extend the public joint interaction workflow from disconnected fragments to
complete checksum-qualified EST and DES CCD molecules.

## How

Reuse the existing CCD preparation client, public MolSysMT rigid translation,
merge and extraction, existing named detector recipe and public collection/
composition tools. Declare ring-offset and donor-contact placements and retain
component correspondence, chemistry, coordinates and original data identities.

## Why

Classical modeling needs to work with full graphs, hydrogens and multiple
features while preserving independent geometric, essential and steric semantics.
Neutral charge families can be evaluated empty without being discarded.

## What is measured and what is assumed

Thirty controls pass in 129.47 s on Python 3.14.7. The four pairs produce 10/11 EST
and 16/18 DES sites for ring/donor placements in both molecular roles, preserving
complete component chemistry, atom identity, coordinates and input bytes. The DES
ring-offset reference retains one explicit .05 nm exclusion clash in either role
despite full positive fit. This result is preserved without changing the radius
to force acceptance. Three cookbook blocks execute on Python 3.14; strict isolated
rendering passes with existing Python 3.13 documentation tooling. The maintained
contract records the execution identities and distinguishes local validation from
biological and distribution qualification.

The definitive driver uses a hash-verified MolSysMT package snapshot because the
live checkout was changing concurrently. Thirty controls pass on that snapshot
in 137.39 s. Tracking off/on passes eight primary role hypotheses and 48 pose
evaluations each, preserves scientific results and producer hashes, and captures
9 items/28 uses and 17 items/57 uses respectively. The thirteenth original evidence
artifact and summary are retained; all thirteen archives verify. Initial driver
runs with provider-source drift are not used as the definitive artifact.

The complete live-checkout suite passes 506 tests in 634.91 s with eight known
warnings. Its separate source audit fails because MolSysMT changed during the
run, so it is not fixed-provider qualification. The supplemental audit/log retain
that limitation alongside the successful snapshot controls and driver. Ruff,
reporting indexes, three offline reporting tests and whitespace checks pass.
The measured result and review scope are synchronized in the
[owning issue comment](https://github.com/uibcdf/pharmacophoremt/issues/37#issuecomment-5977950024).

## Alternatives and refuted paths

Do not implement molecular preparation or ring/donor geometry locally, borrow
a citation for fixture placement, guess a charged state to populate ionic families,
or call an ideal designed pose an observed protein complex.

## Scope and exclusions

Two frozen CCD sources, two explicit rigid placements and both molecule roles.
Protein receptor preparation remains with MolSysMT #298, observed OPEN on
2026-10-04. No bioactivity, affinity, pH, conformer-energy or timing/memory claim.

## Acceptance criteria

Independent merge/identity, original chemistry and source preservation, both role
queries, repeat-profile reuse, neutral empty families, displacement/direction/
rigid-motion controls, explicit steric veto, non-default-unit persistence, actual
resource/method attribution and scientific stability across tracking profiles.
Executable recipe, retained original evidence and owning issue result remain linked.
