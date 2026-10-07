---
summary: Audit the ERalpha snapshot and migrate its regression to a reproducible native workflow.
issue: uibcdf/pharmacophoremt#22
status: active
opened: 2026-10-02
closed:
verification: measured
area: [validation, molecular-preparation]
guard: tests/test_validation_eralpha.py
normative: devguide/eralpha_validation.md
blocked_by: []
supersedes: []
---

# Native ERalpha validation case

## What

Audit the real prepared snapshot and establish a native MolSysMT preparation,
recognition, query and geometric-control workflow. Retain the historical feature-
presence regression as legacy evidence until the replacement is accepted.

## How

A checksum-qualified fixture manifest, executable case-specific audit and native
rejection guard use public MolSysMT APIs. An executed cookbook notebook records
the input findings and the next acceptance controls. Molecular template application
is requested in the owning provider, with linked consumer evidence in
[MolSysMT #298](https://github.com/uibcdf/molsysmt/issues/298).

## Why

The legacy test recovers chemistry inside PharmacophoreMT. Passing it does not
establish native recognition or verified biological/reference-data provenance.
An unresolved chemical input must not be reported as a zero fit or an empty model.

## What is measured and what is assumed

The 54,437-atom, one-frame snapshot has a 44-atom/47-bond unnamed ligand at
`group_index == 8076`; automatic small-molecule selection is empty. C18/H24/O2
is compatible with estradiol but does not establish its identity or stereochemistry.
Native input has partial connectivity, missing declared orders and formal charges.
The public PDB-text/RDKit roundtrip retains ligand/protein counts but gives order
zero for every bond; MolSysMT recognition rejects both routes explicitly.
The audit checks the unchanged source coordinates and chemical-state payload.
The two ERalpha tests passed locally, and the notebook executed all three code
cells without errors. The audit CLI produced JSON; strict isolated cookbook
rendering and the three offline reporting tests also passed.

Measured provider: MolSysMT `4d490427e38c5836be82472348fdf61934442bda`.
The historical dataset label is 1QKU; derivation from that entry is unverified.
No positive native pharmacophore, biological enrichment or timing benchmark is
claimed. Diagnostic/schema observations are revision-qualified, not universal
properties of all PDB readers or future provider versions.

## Alternatives and refuted paths

Public conversion alone is not chemical preparation. Do not mark connectivity
complete manually, guess neutral charge, copy legacy RDKit inference into the
native path or mistake explicit hydrogens for complete chemistry. A curated
chemical template needs independently checked atom correspondence.

## Scope and exclusions

One real input audit and subsequent native ligand/observed-complex validation.
Readiness reporting and molecular preparation belong to MolSysMT; evidence
publication architecture belongs to #20. The existing synthetic geometric tests
remain independent controls; they are not ERalpha binding validation.

## Acceptance criteria

The audit, manifest and notebook execute reproducibly. A reviewed provider route
must retain atom correspondence, coordinates and declared chemical provenance;
then native construction/evaluation must pass self-placement, displaced-pose,
geometry/orientation, persistence and citation controls. Receptor observations
must name their detector criteria and coverage. Verified fixture derivation or a
replacement with documented origin is required for a biological reference claim.
Input audit is delivered; preparation and positive native acceptance remain open.

## Source curation and provider contract — 2026-10-03

A separately acquired 1QKU/CCD EST case now records the original bytes, URLs,
checksums, observed entry revision and exact selected ligand. Its deposited
coordinates have 20 heavy atoms and no ligand H; the CCD has 44 atoms/47 bonds.
The new guard distinguishes label chain D from author chain A and verifies that
source-data identity does not imply completed chemistry or hydrogen preparation.
The historical snapshot remains independent and has not been replaced or
retroactively attributed to the new deposition.

The minimum assessment/application contract is specified under the provider's
#298 proposal: an exhaustive explicit map, state resolution, supported chemical
fields, conflicts, coordinate preservation, native assignments and provenance.
No template application or hydrogen-generation implementation is claimed by this
slice. Positive native construction/evaluation remains pending.

Verification for this slice: three ERalpha tests passed, the updated notebook
executed all four code cells without errors, and both repositories' reporting/
index checks passed. Source conversion and case guards used the same controlled
provider revisions as the original audit; format probes additionally used clean
MolSysMT source `e9f135c2962aeefdb08135a7bc567d2d08bf27c5`.
The isolated cookbook also built successfully under strict Sphinx checking.

## Observed-ligand consumer integration — 2026-10-03

The provider's #298 development template tools are now consumed by
`devtools/prepare_eralpha_ligand.py`. A frozen coordinate-free curated EST template,
its original manifest and acquisition hashes are retained locally. Public
assessment/application preserve the deposited 20-heavy-atom pose and source IDs;
the unprepared input and complete system remain unchanged. The provider's
canonical-descriptor stereochemical choice and CCD C8 discrepancy are explicit.

Eight additional guards in `tests/test_eralpha_template.py` protect selected
acceptor/aromatic self-fit, displacement and normal controls, two-format
persistence, checksum/map failure, units, actual resource/method attribution and
tracking-independent science. Stored H counts remain distinct from explicit
donor geometry. The recipe and retained evidence are linked from the normative
ERalpha document. Preparation and selected-family geometry advance locally;
donor-inclusive and receptor/biological acceptance remain open. Fixed-state H
placement is the next provider gate in #300; #298 remains the template owner
and its public delivery/review is not inferred from this local run.

Verification: eight new controls pass, and the complete suite passes 327 tests
in 333.34 s on Python 3.14.7 with the same two known warnings. Three recipe blocks,
strict isolated Sphinx rendering with existing 3.13 tooling, Ruff and offline
reporting/index checks pass. Full original evidence SHA-256 is
`da21115b170d05fbac23f5956c0b47f8829bfcd54b341c3e0708d02b052c1cbd`.
The [owning issue result](https://github.com/uibcdf/pharmacophoremt/issues/22#issuecomment-5970551189)
retains the outcome and remaining gates; review/incorporation remain pending.

## Fixed-state H consumer acceptance — 2026-10-03

MolSysMT #300 is resolved, and its public fixed-state RDKit extension is now
consumed after the independent chemical-template stage. The result has 44 atoms,
47 bonds and 24 added H while preserving the observed heavy pose and selected
state. The source remains unchanged; strict/intersection annotation behavior is
explicit. Two actual indexed donor-H pairs now supply directional features.

The five-essential-site donor/acceptor/aromatic query passes self-placement,
displacement/normal/donor-direction negatives, two-format persistence and
nondefault-unit controls. Both rigid angular policies recover all five matches
in three fits after the independent seed-eligibility correction under #31.
The source and provider preparation reports remain separate from generated H
geometry and receptor/environment refinement. Actual bounded Ackredit captures
retain resource and reached RDKit/CIP/G3PS references; the native provider report
also retains its original roles, which its legacy session credits omit.

Eleven additional donor-route guards and six #31 guards bring the full local
suite to 344 passing tests on Python 3.14.7 (348.54 s); six warnings are the two
earlier warnings and four expected B-factor-drop diagnostics. All 25 focused
controls and five new recipe blocks pass. Strict isolated rendering uses existing
3.13 documentation tooling. Retained original evidence is linked from the
normative ERalpha guide. The resolved molecular capability is removed from
blocked_by; receptor/biological acceptance and incorporation remain open.

The [consumer result](https://github.com/uibcdf/pharmacophoremt/issues/22#issuecomment-5973121783)
is confirmed in the
[resolved provider issue](https://github.com/uibcdf/molsysmt/issues/300#issuecomment-5973140309).
The shared credit adapter's missing contextual roles are handed to
[MolSysMT #27](https://github.com/uibcdf/molsysmt/issues/27#issuecomment-5973140086),
and the numerical correction has its own
[result under #31](https://github.com/uibcdf/pharmacophoremt/issues/31#issuecomment-5973140527).

## Receptor diagnostic consumption — 2026-10-03

The public MolSysMT #217/#218 diagnostics now support an executed chain-A receptor
audit. It separates 247 assessed and three heavy-incomplete groups from the
12/19/23 heavy-complete residues in 0.4/0.5/0.6 nm observed-ligand shells. Label
chain A receptor and label chain D EST share author chain A; all indices retain
the complete source domain. No water, other protein copy or symmetry mate is
silently included, and reference-sequence completeness is not assessed.

The central shell still lacks formal charges, atom aromatic flags and indexed H;
connectivity is partial and reference bond-order/protonation comparison remains
unassessed. Actual receptor-only recognition and two full-source detector calls
fail with their provider diagnostic, retained as unevaluated observations. No
ligand has been reinserted and no preparation or biological result is inferred.

`tests/test_eralpha_receptor.py` adds eight guards, including unit policy,
preservation and actual observed-data-only credit. Full reports and tracking
independence are retained in `devguide/evidence/eralpha_receptor_py314.json.gz`
with decompressed SHA-256
`dfc329348c4c67329984ea5360d58c3512fe45cdc8f86a757c73d301a4fcda07`.
The normative ERalpha guide and new cookbook describe the case and remaining
provider preparation contract under #298. Incorporation, successful observations
and biological validation remain open; diagnostic delivery is not chemical
preparation delivery.

Verification: 352 complete-suite tests pass on Python 3.14.7 (376.12 s), with
the same six warnings. All 27 focused receptor/template/H controls and final
eight receptor guards pass; three cookbook blocks execute on 3.14 and strict
isolated rendering passes with existing 3.13 tooling. Ruff, offline reporting/
index and whitespace checks pass. All eight original evidence archives verify.

The [owning result](https://github.com/uibcdf/pharmacophoremt/issues/22#issuecomment-5973351237)
and [provider follow-up](https://github.com/uibcdf/molsysmt/issues/298#issuecomment-5973354053)
retain the receptor assignment requirements and original diagnostic evidence.

## Independent exclusion-geometry continuation — 2026-10-03

The [public constructor under #32](https://github.com/uibcdf/pharmacophoremt/issues/32#issuecomment-5973661182)
now composes raw receptor heavy geometry with the separately prepared observed
EST. The 19-residue shell supplies 153 spheres; declared 0.1/0.35 nm choices and
an independently translated collision demonstrate the exclusion veto without
resolving receptor chemistry. Positive fit remains 1 in the colliding control;
candidate index 3 and complete-source receptor index 394 retain separate domains.
The broad 0.4 nm positive radius isolates this analytical effect and is not the
earlier recovery hypothesis or a biological cutoff.

The complete suite passes 378 tests on Python 3.14.7 (473.81 s), with the six
previous warnings and two additional expected B-factor drops. All final 26 new
focused controls pass; three new cookbook blocks execute on 3.14 and strict
isolated rendering passes with existing 3.13 tooling. Native query persistence,
source/ligand preservation, actual attribution and tracking-independent science
are retained in the ninth original archive. All earlier archives verify.
No runtime/memory or biological acceptance is measured. Ruff and offline
reporting/index/whitespace checks pass; editable 3.14 installation is confirmed.

The [consumer continuation](https://github.com/uibcdf/pharmacophoremt/issues/22#issuecomment-5973670489)
links the reusable tool, case guards and retained evidence. Receptor preparation,
successful interaction observations and biological acceptance remain open.

## Declared prepared interface acceptance — 2026-10-07

The current MolSysMT source contract supports a declared closed fragment of
label-chain A residues 304–550 plus observed EST. The new local recipe
`devtools/prepare_eralpha_interface.py` consumes public peptide-template,
aromatic-normalization, chemical-template application, fixed-state H placement,
merge and detector tools. It reuses the checksum-qualified local deposition and
EST preparation rather than importing provider developer scripts or temporary
artifacts. The case manifest fixes HIE histidines, charged fragment termini,
the inspected ARG NH1/NH2 map and reviewed peptide graph. No chemistry algorithm
is implemented in this consumer.

The prepared graph has 4,047 atoms, 4,088 bonds and one frame, retaining 1,995
observed heavy atoms and adding 2,052 local H. Original heavy identities and
coordinates and the unprepared source remain unchanged. Three cached analyses
retain 12 hydrophobic observations and evaluated-empty H-bond/pi-pi families.
Their parameters, source maps and evaluated frame remain explicit. Twelve frozen
deposited atom pairs and independent coordinate-distance assertions guard the
participant/geometry contract separately from model self-placement.

`devtools/validate_eralpha_interface.py` composes six observed participant sites
with five separately labeled ligand-reference donor/acceptor/aromatic sites.
The curation tool assigns declared hydrophobic weight 0.5 while every positive
site remains essential. Self-placement has fit 1; a 2 nm displacement has fit 0.
Reversed donor direction and an orthogonal ring normal each miss one essential
site at fit 7/8; normal-sign reversal still matches. The observed 19-residue shell
supplies 153 exclusions. An independent broad-radius collision control preserves
fit 1 while the receptor-exclusion veto changes status to not_matched.

Native H5MSM recovery preserves chemical values, original preparation history,
typed unknown orders and cached analysis maps/coverage. Curated JSON recovery
preserves metadata and detached bibliography; a fresh-process reader earns no
new calculation credit. Evaluation and rebuilding also pass under pm/fs with
explicit angle/charge standards. The CLI performs both full preparation/control
runs with host attribution disabled/enabled and obtains identical scientific
SHA-256 `005172703f05546b658ad54327dd71da4063ea077c6c7e611e3f61085149435f`.

Seven focused guards in `tests/test_eralpha_interface.py` pass on local normal
editable Python 3.14.7 (441.60 s), with two expected B-factor-drop diagnostics.
Both cookbook blocks execute, isolated strict Sphinx rendering and Ruff pass.
Full JSON evidence, its summary and the original native artifact are retained
under `devguide/evidence/eralpha_interface_*`. The JSON intentionally summarizes
aromatic normalization; original numerical unknowns remain in the retained native
history. Earlier evidence and historical claims are preserved.

This accepts the bounded prepared-interface analytical chain, not the complete
receptor. Residues 301–303 remain excluded; histidine/terminal choices, unspecified
peptide stereo and locally generated H remain declared limitations. Environmental
refinement, biological enrichment, public installation and performance acceptance
remain open. Existing shared-environment pip-check conflicts remain independently
owned by MolSysSuite #52; local source evidence does not certify a clean install.
No new provider defect/capability proposal or shared-policy change is inferred.

## Empty-family diagnostic continuation — 2026-10-07

The maintained [diagnosis](../eralpha_interaction_diagnostics.md), driver
`devtools/diagnose_eralpha_interface.py`, separate case declaration and guard
`tests/test_eralpha_interaction_diagnostics.py` inspect the current bounded
interface without replacing its cached observations or curated model.

Public SMARTS recognition retains both EST hydroxyl roles and nearby receptor
sites. Eight donor/H/acceptor triples lie within the fixed 0.40 nm diagnostic
radius; six satisfy the original 0.35 nm D–A limit, and all six fail its
130-degree D–H–A limit. Fixed distance/angle comparisons yield counts
0, 6, 2, 0 and 1; widening distance alone admits EST O3/LEU387 O rather than
repairing the nearby GLU353/HIS524 geometry. No H or chemical state is changed.

The 29 recognized SMARTS rings include PHE404 and EST. Only PHE404 is within
the reference 0.65 nm centroid range (0.499967 nm). The independent fixed-case
reference-plane oracle checks passing edge distance/angular gates but a
0.264394 nm intersection distance, exceeding the 0.15 nm cutoff. The alternate
aromatic-cycle reference profile remains empty; an explicitly declared
least-squares distance/angle/offset profile yields one observation. These
different methods are sensitivity controls, not improved biological results.

Environmental H refinement remains owned by uibcdf/molsysmt#323. The missing
public surface for rejected reference-pair measurements is now requested in
uibcdf/molsysmt#350 with linked consumer evidence. The production diagnostic
composes public provider tools; reference intersection arithmetic stays solely
in an independent frozen-case test oracle. Original evidence remains unchanged.
Biological discrimination, complete receptor acceptance, public installed
qualification and performance remain open.

Six focused diagnostic guards pass in 106.07 s on local editable Python 3.14.7,
including independent coordinate/angle/intersection oracles and nondefault-unit
records. Both independently prepared host-attribution settings pass with common
scientific SHA-256
`74bfb5d171409bb1eb2ec3b500664ad68a604bd0418b8387861810c63310bb33`.
The original full driver output and compact summary are retained as
`devguide/evidence/eralpha_interaction_diagnostics_py314*`. Strict isolated
cookbook rendering, Ruff, generated report-index checks and three offline
reporting tests pass. No full scientific-suite or required-hosted-matrix result
is inferred from this focused selection.
