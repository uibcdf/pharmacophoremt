# Development Checkpoint

## Public cached receptor generation qualified — 2026-11-05

[#87](https://github.com/uibcdf/pharmacophoremt/issues/87) delivers
`modeler.from_receptor_features` in development source. The [contract](public_receptor_generation.md)
requires `receptor_profile='donor_aromatic_faces'`, explicit-unit donor/aromatic
distance choices, radius and finite budget. Every admitted donor/ring occurs once
per joint hypothesis; faces and caller choices remain separate. The lazy product
records exact total/remaining/completion and omitted families. Invalid admitted
geometry fails before any model, including with zero budget. Chemical features
and excluded-volume inventories retain separate domains.

**192 selected controls pass in 218.87 s, including 54 new**. Both unchanged
prepared-input unit-policy replays match independent frozen oracles and recover
all eight models. After a docstring-only clarification, 52 fast controls pass.
Four cookbook blocks and a separately captured three-hypothesis prepared replay
execute, preserving original coordinates, chemical history, observations and
units. [Original evidence](evidence/public_receptor_generation_20261105_summary.json)
retains initial skip-declaration failures, the corrected unit-spelling guard,
exact identities and actual input/operation credit. Historical #86 bytes remain.

ArgDigest owns signature/value admission; SMonitor supplies PHMT-E102,
PyUnitWizard carries units and optional Ackredit retains actual model/report
credit. The projection constructor now declares the standard boolean skip
control; its scientific checks and facade defaults remain. No optional backend,
provider source/pin, dependency floor, published package or preparation changes.
The package-resource inventory now requires both new runtime modules.

Next compose optional receptor exclusions through the existing cached-volume
contract, with explicit radii/frame/state and independent hypotheses. Further
acceptor profiles remain MolSysMT #375 receiving; TopoMT #101 is optional and
#323 environmental H refinement stays separate. ArgDigest #47/#48 are source-fixed
at `7fdf726d984553c9d89efc08abc2016f46ef41aa`; public 0.17.0 is unchanged and #82
awaits published receiving under MolSysSuite #164. Broader #6/audit 12, #66,
#74/#215 and full-suite/installed/public/hosted gates remain independent.
Addon/release deferred, public 0.4.0 unchanged. Owned capsule
`/tmp/phmt-public-receptor-20261105-p20atfmx`, review 2026-11-19 or scientific/source
change; no continuing local process required. Earlier next steps are historical.

## Cached receptor hypothesis-generation pilot qualified — 2026-11-04

[#86](https://github.com/uibcdf/pharmacophoremt/issues/86) qualifies the first
[prespecified generation pilot](receptor_hypothesis_pilot_protocol.md): the
unchanged prepared PHE404 inventory supplies one indexed donor and one ring.
MolSysMT owns source loading, selection, chemistry, vectors and planes. PHMT
declares distances/radius, complements the donor and enumerates both ring faces
as separate two-site hypotheses. The position-only acceptor is explicitly omitted.
This is unshipped case support; no public runtime/API, provider, pin or floor changes.

**110 selected controls pass in 191.26 s, including 34 new guards**, zero
failures/errors/skips. Eight alternatives have independent raw-coordinate oracles
and supplied-pair positive/negative controls; budgets 8/3/0 retain completion and
remaining 0/5/8. JSON/YAML preserve all evidence and constraints, with geometry
within the frozen 1e-12 tolerance. Literal pm roundtrip equality can differ by
ordinary float64 rounding; exact flags and original initial failures are retained.
The standalone command also completes both unit-policy runs. All three source/
native/test/input/metadata identity checks are stable, with original coordinates,
full chemical history, cached observations, inventories and application units intact.
[Original evidence](evidence/receptor_hypothesis_pilot_20261104_summary.json) and
[case interpretation](../docs/content/validation/receptor_hypothesis_pilot.md)
retain actual input/operation credit and the three corrected harness assumptions.

Provider review is complete for this scope. Requests are published in
[MolSysMT #375](https://github.com/uibcdf/molsysmt/issues/375#issuecomment-6648409054)
and [TopoMT #101](https://github.com/uibcdf/topomt/issues/101); #323 remains separate
environmental H refinement. Next design the explicit public cached-generation
contract from this fixed pilot, including profile/parameter choices and budget/
unsupported outcomes. Further acceptor chemistry requires its own admitted
provider profile and declaration; TopoMT stays optional. Neither complete DFND
nor universal acceptor coverage blocks this donor/ring development route.

Broader audit item 12, #66, #74/MolSysMT #215, #82/ArgDigest #47/#48 and #6 retain
their scope; installed/public/full-suite/hosted qualification stays separate.
Addon/new release deferred; public 0.4.0 unchanged. Owned capsule
`/tmp/phmt-receptor-pilot-20261104-gmfqhead`, review 2026-11-18 or scientific/source
change; no continuing local process is required. Earlier next steps are historical.

## Prepared ERalpha receptor sensitivity qualified — 2026-11-04

[#85](https://github.com/uibcdf/pharmacophoremt/issues/85) extends #83 on the
unchanged #52 prepared fragment: [prespecified protocol](prepared_receptor_sensitivity_protocol.md),
[original evidence](evidence/prepared_receptor_sensitivity_20261104_summary.json)
and [case](../docs/content/validation/prepared_receptor_workflow.md#prepared-receptor-sensitivity-extension).
Each final matrix retains 62 valid placed settings and two actual failed/unscored
frames under nm and pm. PHE404 copies use public MolSysMT rotation/translation;
they are methodological controls, not new ligands or binding predictions.
Native decoding, selection, recognition and geometry remain MolSysMT-owned.

The fixed placement/radius bands, separate faces, strict exclusion vetoes and
unoriented-axis angle transitions agree with independent original-coordinate
oracles. Exclusion radii .01/.20/.40 nm yield 0/5/47 clash pairs on 0/3/11 atoms
with positive fit one. The rotated axis angle is about 36.07 degrees. Explicit
exclusion removal records its source and reason; it does not infer binding
importance. Source coordinates, full chemical history, cached contacts, native
inventories and application units stay unchanged; actual input credit is saved.

**288 selected cases pass in 442.24 s, including 43 new guards**. The documented
standalone recorder also executes all 64 attempts; all three recorded identities
are stable. Final pytest/CLI include 12 source/native provider identities. Two
initial new assertions assumed a tagged internal history snapshot; only that
guard expectation changes, preserving every field and the declared oracle/grid.
No runtime, provider, prefix, dependency, workflow or old evidence changes.

**Next:** inspect actual TopoMT pocket/MolSysMT geometry contracts and declare a
receptor hypothesis-generation pilot before implementing orchestration. Missing
reusable provider operations go to their issue boards. Automatic generation,
real cohorts, preparation/search uncertainty and whole audit item 12 remain open.
#375/#323, #66, #74/MolSysMT #215, #82/ArgDigest #47/#48 and broader #6 remain
independent. Installed/public/hosted/full-suite qualification stays separate.
Addon/new release deferred; public 0.4.0 unchanged. Owned capsule review:
2026-11-18 or scientific/source change; no continuing local process. Earlier
dated next-step statements below retain their historical scope.

## First receptor sensitivity slice qualified; unit boundary repaired — 2026-11-04

[#83](https://github.com/uibcdf/pharmacophoremt/issues/83) completes the first
analytical receptor-based sensitivity slice: [prespecified protocol](receptor_sensitivity_protocol.md),
[case](../docs/content/validation/receptor_sensitivity.md) and
[original receipt/full evidence](evidence/receptor_sensitivity_20261104_summary.json).
The complete grid predates execution. Each final matrix retains 90 valid
fixed-pose settings and two deliberate failed/unscored frames under two unit
policies; settings are not independent molecules or activity measurements.
Placement/radius, Point-versus-Sphere tolerance, strict exclusions, curated
essential/weight/removal choices and unoriented aromatic axes have known answers.
All molecular construction/recognition/inspection uses existing MolSysMT tools.

The protocol exposes and repairs [#84](https://github.com/uibcdf/pharmacophoremt/issues/84):
ordinary unit-conversion roundoff could flip two inclusive positive-site radius
equalities. PoseEvaluator now compares excess distance against eight float64
epsilons times the radius/Point tolerance and records that numerical policy.
No physical cutoff tuning, molecular change, provider edit or altered exclusion/
angular/assignment/scoring semantics. The difference form avoids radius expansion
overflow. The original matrix and all failed outputs remain unchanged/archived.

**245 selected controls pass in 198.40 s, including 49 new guards**, with zero
failures/errors/skips. Five pytest and one standalone-recorder identity checks
are stable. The documented recorder also executes the full 92-attempt matrix;
sources, inventories, curation inputs and application units remain intact.
Actual attribution is retained for the 90 completed evaluations. Initial wrong
guard-field assumptions, three genuine failing guards for the two cells and
one selector usage failure are retained separately. No full-suite, clean
installed/public/all-platform, biological or performance claim follows.

**Next:** prespecify a development-only extension of the cached prepared-receptor
case, keeping molecular direction/preparation needs with MolSysMT (#375/#323)
and actual pockets with TopoMT. Audit item 12 remains partial for real development
cohorts, preparation/search variability and uncertainty. #66's original-method
gate and #74/MolSysMT #215 remain. #82 stays blocked on ArgDigest #47/#48; broader
#6 stays partial. Addon/new release deferred; public version remains 0.4.0.
Owned capsule review: 2026-11-18 or source/scientific change; no continuing local
process. Earlier dated next-step statements below remain historical.

## Native I/O ArgDigest handoff published; adoption gated — 2026-11-04

[#82](https://github.com/uibcdf/pharmacophoremt/issues/82) now tracks two
provider gates: [ArgDigest #47](https://github.com/uibcdf/argdigest/issues/47)
can drop a literal kwargs option or overwrite an explicit source, including the
current model dispatcher; [#48](https://github.com/uibcdf/argdigest/issues/48)
requests TypeError-compatible contract refusal for existing closed I/O APIs.
The user authorized both publications after reviewing their exact drafts.
**No runtime migration or fix is activated.** Generic binding belongs in
ArgDigest; molecular forms, inspection and manipulation remain MolSysMT-owned.

[Readiness and next receiving steps](native_io_admission_readiness.md),
[original evidence](evidence/native_io_admission_readiness_20261104_summary.json)
and [published proposal record](evidence/native_io_argdigest_issue_drafts_20261104.json)
retain the two failing candidate probes and actual current-dispatcher effect.
All three recorded identities are stable. **260 selected legacy compatibility
cases pass in 7.23 s, including 41 new controls**, with no failures/errors/skips.
They protect existing paths, TypeError refusals, option identity and provider
delegation; they do not establish a repaired provider or scientific validity.

**Next for #82:** wait for supported published ArgDigest correction/policy,
receive exact bytes, rerun adversarial source/keyword and exception-family
probes plus legacy guards, then consider bounded native I/O activation. #82 is
blocked; broader #6 stays partial. Independent product work can resume the
development-only sensitivity/ablation protocol described under #80, preserving
reserved evaluation data. #66, #74/MolSysMT #215 and installed/public/hosted
gates remain separate. Addon/new release deferred; public version stays 0.4.0.
No continuing local process. Owned evidence capsule review: 2026-11-18 or
provider readiness. Earlier next-step statements below remain historical.

## Native I/O diagnostics and dependency declarations repaired — 2026-11-04

[#81](https://github.com/uibcdf/pharmacophoremt/issues/81) closes the owned native
I/O diagnostic gap; [contract](native_io_diagnostics.md) and
[original evidence](evidence/native_io_diagnostics_20261104_summary.json) retain
**243 passing selected cases in 25.53 s, including 45 new guards**. All six
attempt identities remain stable; the final identity includes actual PyYAML
6.0.3 source/native bytes. Ten intentional attribution-failure warnings remain.
New PHMT-E108/NativeFormatError and PHMT-E109/ArgumentTypeError preserve ValueError/
TypeError catch compatibility; exact types and wording intentionally change.
Typed context, args-only/profile rendering, original finite-value cause,
PHMT-E102 scientific validation and writer destination protection pass.

Parser/encoder/unexpected runtime/filesystem and MolSysMT provider exceptions
retain their contracts. Data admission, native schema, scientific algorithms,
SDF container/payload and source pins are unchanged. #6 also aligns mandatory
nglview classification and declares the existing YAML codec directly as
PyYAML>=5.1 (API floor for sort_keys=False). Metadata/Conda recipe and three SDK-
generated ordinary environments agree; no real environment is changed or public
package newly qualified. Other provider floors, scientific commands and source pins remain; three scientific
CI environment selectors now enforce the same PyYAML floor.

**#6 stays partial. Next:** bounded ArgDigest native I/O argument/admission
contracts, preserving direct-reader Path support, dispatcher string-only
compatibility, reader option refusal and molecular delegation. Then resume the
development-only sensitivity/ablation protocol; scientific data/holdout gates
remain. #74/MolSysMT #215, #66 and installed/public/hosted #10/#23/#9 retain their
scope. Addon/new release deferred, public version still 0.4.0. Earlier dated
next-step statements below remain historical.

## Consensus support and redundancy reviewed — 2026-11-04

[#80](https://github.com/uibcdf/pharmacophoremt/issues/80) qualifies the bounded
native comparison: [support/method matrix](consensus_support_review.md) and
[original evidence](evidence/consensus_support_review_20261104_summary.json).
**126 selected cases pass in 160.40 s, including 28 new controls.** The original
probe and selected run both retain stable source/native/test/input/metadata
identities. Existing independent assignment, clique, package and rigid oracles
remain unchanged and green. No runtime/helper/provider/input,
scientific method, weighting or dependency changes are needed.

The reference method requires support per site; clique hypotheses require the
intersection across all their sites, and rigid consensus applies that condition
within each accepted pivot layout. Repeating a known source under a new ID can
change eligibility and the unweighted feature mean without changing site weight.
Shared donor/acceptor atoms remain valid distinct typed occurrences. Native
JSON/YAML retain these member/support/initial-constraint decisions under changed
unit policies. Existing counts of equivalent rigid proposals are preserved.

Audit 8–9/13 remains **partial** for real chemical-series redundancy, development
cohort balancing, model complexity and empirical importance. **Next:** define a
bounded development-only sensitivity/ablation protocol for emitted radius,
matching tolerances and curated constraints, starting with analytical controls.
Keep reserved evaluation data unused; preparation/identity/grouping stays in
MolSysMT. Do not add a local molecular deduplication or grouping routine.
#66, #74/MolSysMT #215, broader #6 and installed/public/hosted gates remain separate.
Addon/new release defer; public version remains 0.4.0. Earlier dated next steps
below remain historical.

## Native constraint semantics qualified — 2026-11-04

[#79](https://github.com/uibcdf/pharmacophoremt/issues/79) records a bounded
scientific review of audit items 8–9: [contract](native_constraint_semantics.md),
[user interpretation](../docs/content/user/constraint_semantics.md) and
[original evidence](evidence/native_constraint_semantics_20261104_summary.json).
**368 focused cases pass in 174.42 s, including 40 new controls**; both attempt
source/native/test/metadata identities remain stable. Point/Sphere feature lists
are alternatives; capacity is per typed record, allowing shared atoms across
roles and indexed donor-H pairs. Existing donor assignments already preserve
hydrogen identity; the suspected loss was refuted. Shape restrictions and
correspondence/alignment compatibility remain. Two additive result criteria
explain this method; matching/scoring/defaults and algorithm ID are unchanged.

Recognized features, observed contacts and caller projections retain distinct
origins, unit-weight/essential construction defaults and deliberate curation
history through JSON/YAML under nm/radian and pm/degree policies. Those defaults
are hypotheses, not measured binding importance; repeated observations do not
inflate weights. Arbitrary direct edits do not create a decision history.

Audit items 8–9 remain **partial**, not globally completed. **Next:** review
consensus support, participant reuse and redundancy (audit 8/13) against existing
independent oracles; then design informative parameter/constraint sensitivity
controls (audit 12). Do not claim missing functionality before inspecting the
existing tools. Molecular operations stay with MolSysMT; #74/MolSysMT #215 and
#66 keep their separate gates. #6 remains partial; full-suite/installed/platform/
predictive qualification, addon and a new release are separate. Earlier entries
retain their historical next-step statements. Public release remains 0.4.0.

## Nested facade admission and skip control received — 2026-11-04

#6's [nested contract](nested_facade_contracts.md) and [receipt](evidence/nested_facade_contracts_20261104_summary.json)
qualify ligand-consensus/screening constructor domains derived from existing
endpoint signatures. **167 focused controls pass** (39 new), with all three
source/native/test/metadata identity checks stable. No method, score, preparation
or molecular routine changes. Definition ownership and mandatory bypass checks
are preserved. #78 fixes explicit True/False VirtualScreening controls leaking
to native constructors; nonboolean values are refused.

Two old min_sites/min_support tests now expect earlier UnknownArgumentError.
Three intentional unknown-run-option warnings remain; run/cache order is unchanged.
#6 stays partial for broader public/batch/support and delivery receiving. Source
qualification is separate from full-suite/installed/platform/predictive evidence.

Next product review: audit items 8–9, multi-feature/shared-participant semantics
and traceable observation-to-constraint choices. Inspect existing definitions and
controls before changing science. Molecular gaps belong in MolSysMT; #74/#215,
#66, addon/new release and other gates retain their existing scope. Earlier dated
checkpoints remain historical.

## Merge delegates to public composition — 2026-11-04

[#77](https://github.com/uibcdf/pharmacophoremt/issues/77) is fixed with a small
facade change: [compatibility contract](pharmacophore_merge.md) and
[receipt](evidence/pharmacophore_merge_20261104_summary.json). All constraints stay
in order without deduplication; sites/metadata are independent. Both metadata,
scores and references live in labelled component provenance. The first name,
description and live molecular reference remain; the output score/ref_mol are
None, common known ref_struct is retained and conflicts raise. No molecular
inspection, copying, detection, fitting or local composition engine is added.

**202 broad compatibility controls and 28 final merge guards pass**; all three
attempt identities remain stable. The composer-only post-broad change is a
docstring clarification, with final chained/failure guards separately qualified.
The metadata namespace/site-alias/frame changes are explicit. Native persistence
and nested provenance remain covered; directly related planning examples now
separate concatenation, averaging and consensus. Source receiving and hosted/
installed/platform/predictive qualification remain separate. Earlier dated
entries below retain their historical pending statements.

Next: bounded #6 review of nested ligand-consensus and screening facade admission,
using the existing scientific methods and provider contracts. Audit scientific
semantics/provenance/study design remains independent; #74/MolSysMT #215 and #66
retain their gates. Addon and new release stay deferred.

## Live-reference/native-copy review qualified — 2026-11-04

[#60](https://github.com/uibcdf/pharmacophoremt/issues/60) closes its reviewed
source/API scope: [ownership contract](live_reference_ownership.md) and
[receipt](evidence/live_reference_ownership_20261104_summary.json) retain **199
passing controls**, including ten new integration cases. Pure pharmacophore copies
keep live molecular references while owning independent native data. Explicit
molecular variants/edits use MolSysMT; owner-local invalidation, maps, quantities,
failed operations, retained historical results and no-new-credit copying pass.

No runtime implementation, provider source/prefix or dependency floor changes.
Earlier #60 incomplete-provider warning is superseded: MolSysMT #121 is closed.
Executed provider is 0faf1584; newer sibling 71fbe4f is read-only contract context.
Two aromatic NaN measurement positions caused eight initial comparison-guard
failures; corrected exact comparisons preserve missing values. Both attempt
identities stay stable. Source receiving only; full-suite/installed/platform/
performance/predictive and broader provider #408/#122 claims remain separate.

**Next: #77**, confirmed legacy Pharmacophore.merge metadata loss plus measured
shared sites requiring an explicit compatibility/ownership decision. Reuse public
composition/copy tools; do not infer molecular source/frame identity or implement
molecular copying here. #74/MolSysMT #215, #6 and #66 retain their gates; addon and
new release defer. Earlier dated checkpoints retain their original statements.

## Native schema and writer preparation received — 2026-11-04

[#76](https://github.com/uibcdf/pharmacophoremt/issues/76) introduces
[pharmacophoremt.native@1](native_schema.md) for new JSON/YAML, independently
of the producer package version. Unknown explicit schemas and model/site/shape
fields are refused. Historical untagged data keeps its defaults and limits.
Writers validate and fully encode before opening a destination; invalid scientific
values or serialization errors preserve existing bytes and absent paths. Disk
I/O/crash/concurrent-writer atomicity is outside the guarantee.

**265 focused checks pass**, including 58 new guards. [Receipt](evidence/native_schema_writing_20261104_summary.json)
retains original failures, the six SDF-envelope comparison updates, exact overlays
on base 0413e6c and all three stable identity comparisons. SDF container source
and historical private payload are unchanged; #74 waits on MolSysMT #215.
Source receiving only; no full-suite/clean installed/platform/predictive claim.

Next: #60 / audit item 5, live source references, independent pharmacophore copies
and explicit molecular variants. Molecular copying/inspection must remain public
MolSysMT operations. Audit item 4 still has translator-specific fidelity and
provider-backed SDF migration; #6 nested contracts/#66 study gates remain separate.
Addon and new release defer. Earlier dated checkpoints retain their original scope.

## Native persistence validated; SDF container migration tracked — 2026-11-04

[#75](https://github.com/uibcdf/pharmacophoremt/issues/75) fixes external
JSON/YAML reconstruction bypassing public shape/site validation. **207 focused
checks pass**, including 48 new persistence cases; valid six-shape geometry,
constraints, metadata, units and historical defaults remain supported.
[Receipt](evidence/native_persistence_validation_20261104_summary.json) retains
all attempts and a fully stable final source/native/metadata identity. One initial
floating-point assertion correction and intermediate test-source drift are explicit.
Source receiving only; no full-suite/installed/platform/predictive qualification.

The [field/schema and ownership matrix](persistence_fidelity.md) identifies
existing direct RDKit SDF container operations as migration debt, independently
of #47's semantic fidelity. **#74 waits for public property/record support under
MolSysMT #215**, with a concrete consumer handoff. All molecular representation,
inspection, manipulation and formats (including SDF/PDBQT) belong to MolSysMT.
SDF container source and sibling/provider environments are unchanged.

Next: explicit native schema/version and unknown-field compatibility policy,
plus writer validation/transaction review. Resume SDF migration only through the
public provider route; no local parser/property engine. #6 stays partial; addon
and new release defer. Earlier dated checkpoints retain their original claims.

## Capability inventory and model dispatch contracts — 2026-11-04

The [current capability inventory](capability_inventory.md) separates executable
routes, partial integrations, planned capabilities and scientific/delivery limits.
It maps the six generic modeling methods, direct consensus tools, screening,
validation, persistence and provider ownership to maintained contracts and tests.
It does not promote analytical controls into predictive evidence.

#6 now declares a scoped ArgDigest method domain and the existing `system` /
`mol_sys` aliases for `model`. Admitted keyword names come from actual PHMT
endpoint signatures, including builder frame options and the ligand consensus
union. The ligand facade retains its narrower method checks. Unknown keywords
are rejected before endpoint work; conflicting source aliases can no longer
silently overwrite input. Existing defaults, individual aliases, explicit True/
False digestion controls and method diagnostics are preserved. No molecular
engine, provider implementation, dependency floor or scientific method changes.

[Receiving evidence](evidence/model_dispatch_contract_20261104_summary.json) records **290 passing focused controls**, exact
source/test/resource overlays on base `1c6a03479bd0514a5d5988a8134b8359bca837b9`,
all failed attempts and stable runtime identities. Initial fixture/expected-error
mistakes, declaration discovery correction, warning-contract updates and an
explicit False bypass-admission correction remain visible. Existing real workflow
assertions are unchanged; eight legacy warning expectations now enforce early
refusal without a missing-digester warning. Twenty-two distribution controls,
three reporting checks, Ruff and index checks pass. This is Linux/Python 3.14.7
source receiving with public ArgDigest 0.17.0 and inherited dependencies, not
full-suite/installed/all-platform or predictive qualification. Hosted CI stays #9.

**Next:** audit item 4, document and check field/schema fidelity of native
JSON/YAML and explicit annotated SDF. #6 remains partial: nested consensus and
screening facade contracts require their own review. #60 identity/copy semantics
and #66 experimental study design remain separate. Addon and new release defer.
Earlier dated checkpoints below retain their original statements.

## Native loader admission fixed — 2026-11-04

#73 is resolved: `io.load` forwards options to its selected JSON/YAML/YML,
LigandScout or Pharmer reader, whose closed signature rejects unknown keywords.
Valid reads retain the direct reader's results. Molecular formats and options
remain delegated to public `molsysmt.convert`; its original exceptions now
propagate instead of being replaced by a generic format error. No provider,
chemical preparation, molecular parser or dependency is changed.

The [receiving receipt](evidence/native_loader_dispatch_20261104_summary.json) retains source/test bytes on base
`4a471bc2630d3db95bc9009689450391f1987f91`, all attempts and stable before/after
source/native/metadata identities. Corrected guards reproduce six original
failures and eight passes; **77 focused checks pass** after the fix. Two initial
positive-control fixture rejections remain recorded. This is Linux/Python 3.14.7
source receiving with public ArgDigest 0.17.0 and inherited scientific dependencies;
no new full-suite, installed, hosted or predictive qualification is claimed.

**Next:** audit items 2–3: inventory actual public capabilities and select one
method-dependent dispatcher for #6's option/domain/alias review. Preserve current
scientific contracts; do not invent a second molecular option registry or assume
all planned formats exist. #6 remains partial. Item 10's experimental study design
can proceed independently of API work; unavailable original methods remain #66.
The addon and a new release remain deferred. Earlier dated entries below retain
their original next-step statements as history.

## Audit evidence and acceptance criteria expanded — 2026-11-04

The [audit addendum](audit_20261104_review.md) preserves the initial 17-point
assessment and adds coverage/exclusions, classified findings with evidence,
impact-based priorities, a scientific method matrix and operational closure
checks/dependencies. Existing tie-aware metrics and independent scientific
oracles are recognized, not proposed as absent functionality. No new scientific
tests, installation or predictive validation were executed for this review.
Next remains #73, then bounded #6 work; study design can proceed in parallel.

## Comprehensive audit recorded — 2026-11-04

The [dated architectural, scientific and product audit](audit_20261104.md)
preserves the revised list of 17 improvement areas discussed with the maintainer.
It distinguishes confirmed defects, audit targets and proposed experiments.
Immediate work remains #73, followed by bounded API contracts under #6, while
experimental study design can proceed alongside technical consolidation.
Public 0.4.0 installed qualification and the earlier 1093-case source run retain
their original scope; this documentation review executes no new science.
Molecular operations remain MolSysMT-owned; addon and advanced methods defer.

## Definition-owned native geometry contracts received — 2026-11-04

#6 adopts scoped public ArgDigest contracts for Point, Sphere, SphereAndVector
and Disk. Each defining module owns its constructor's signature through
`DigestConfig(contract_owner="definition")`; application subclasses and mixins
keep that identity while refusal messages retain the runtime class. Existing
value digesters, normalization hook, optional type checks, PyUnitWizard policy
and `skip_digestion` remain active. Closed signatures need no extra Domain or
AliasTable: no shape-specific aliases are supported or introduced, and center
and position stay distinct. Other callables keep their existing configuration.

The [receipt](evidence/native_geometry_contract_receiving_20261104_summary.json) retains the exact published ArgDigest 0.17.0 Conda file
(SHA-256 9c35fa297b5a85dc65ac49ccd108f60f08dbeac4f745d6c369a767c0a0b3a3e1),
source/test/metadata overlays on b0a8f7e and every attempt. Corrected guards fail
four owner checks and pass 40 behavior checks on original production code.
One initial wrapper-attribute test mistake and its correction remain visible.
The final full source suite passes **1093 actual test items** in 1401.42 s,
with zero failures/errors/skips; original warnings and XML counters are retained.
The 85-control scope also passes separately with public 0.17.0 and the normal
0.17.0+5 development provider. All five source/native/metadata identity checks
remain true. This is Linux/Python 3.14.7 source receiving with extracted public
ArgDigest and inherited scientific dependencies, not a clean public installation,
all-minor/platform matrix or hosted qualification.

ArgDigest **>=0.17.0** is now explicit in metadata, Conda recipe and generated
ordinary environments. Both controlled CI manifests/inventory use the published
source c7128f09b2fe064b6c5603d1077dbd2cec52223d, replacing 0.15.0 source
5c6711e. Other provider pins, scientific commands, SDK and frozen workflow
pins are unchanged. The new private module is in the package resource inventory.
Eight environment/22 distribution checks and declaration/generation checks pass.
Initial generation correctly refused stale input hashes before their reviewed
update; this attempt is retained. The borrowed prefix is unchanged. The sibling
ArgDigest clone is clean but six commits behind its remote and remains untouched.

The raw JUnit aggregate says 1110 tests while its actual testcase elements and
receptor say 1093; the existing #71 counter discrepancy is preserved. Twenty-one
warnings in seven original groups remain visible. After that measured full run,
the new #73 queue entry required a one-line reporting-test issue inventory update;
its initial failure and three passing final reporting controls are separate
closeout evidence, not another full-suite run.

**#6 remains partial. Next fix [#73](https://github.com/uibcdf/pharmacophoremt/issues/73):**
real native JSON/YAML `io.load` calls silently discard unknown options, whereas
the direct readers refuse them. Preserve valid format contracts and delegate
molecular conversion/options to MolSysMT; do not copy its option registry or
engine. Then review method-dependent model dispatcher domains and real aliases.
Public 0.17.0 Beartype absence still succeeds with ERROR + WARNING; ArgDigest #46
remains owner. #41 (review 2026-11-11), #19/#22, #23/#10, hosted #9, workspace #82,
#60 and #66 retain their independent gates. Molecular operations remain MolSysMT;
no release/addon or central adoption-state change. Owners LMMV/dprada, temporary
capsule /tmp/phmt6-geometry-20261104-2f7oq6kg, review 2026-11-18.

## Support review fixes hidden diagnostic loss; explicit contracts next — 2026-11-04

#6 is partial with [current boundaries](support_library_boundaries.md),
[report](pending_proposals/review_python_ecosystem_policy_adoption.md) and
[receipt](evidence/support_boundary_review_20261104_summary.json). #72 fixes a real
host optional-attribution defect found during review: warning construction/emission
errors were silently lost. SMonitor remains the normal public catalog path;
unexpected failures now retain tracking/diagnostic context and a structured stderr
fallback. Broken output is retained in the failed payload, preserving science and
original scientific errors. No molecular/provider engine is implemented locally.

Five new guards fail on original cbdee9a code; final exact source overlay passes
44 attribution/contract controls in 17.87 s, zero failures/errors/skips. Ten
intentional existing tracking warnings retain five groups. Exact patches, all
original attempts, source/native/input/metadata identities and original/fixed
scientific payloads remain archived. Qualified/verification full identities pass;
prior #22/#32 metadata lookup discrepancies remain under #82, not repaired.

Conditional real OpenMM/Astropy/unyt length inputs and JSON recovery preserve an
application's unyt policy. This is bounded source receiving for #127, not public/
all-minor qualification or a new mass API. Optional Beartype absence still permits
normal product use but records ERROR-level required-library diagnostics plus a
WARNING that checks are optional; owner follow-up is ArgDigest #46. No local
suppression, provider patch or mandatory Beartype dependency is introduced.

Accepted SDK 1c248b6 validates declarations/generated environments; eight environment
and 22 distribution controls pass. The initial missing-default-SDK launch is
unqualified; the existing immutable #69 SDK is reused through the documented
override. Local GHR 1.0.0 accepts four rules; delivered guide 1.4.0 does not imply
an operator upgrade. Old hosted/test-tool/version evidence is not relabeled.
Strict isolated updated cookbook rendering passes; its two code blocks stay
unchanged, without a new recipe/full-site execution claim. No new full suite.

**Next: scoped ArgDigest function/domain and alias adoption for native geometry.**
The current root lacks FUNCTION_SOURCE/DOMAIN_SOURCE/NORMALIZATION_SOURCE; value
checks and curation registry are not full two-axis adoption. Preserve real public
inputs, explicit physical units, host diagnostics, aliases and skip behavior;
start with a bounded family and its existing guards. Central review states,
installed/public #23/#10, hosted #9, workspace #82, #19 delivery, #22 science,
#41 public/legacy receiving (review 2026-11-11) and #66 endpoint methods remain
independent. MolSysMT owns every molecular operation. Addon/new release defer.
Owned /tmp/phmt6-review-20261104-wsgvlcbl/, LMMV/dprada, review 2026-11-18; borrowed
#69 scientific prefix/SDK are unchanged. No local process remains after checkpoint.

## Bounded prepared ERalpha chain accepted; adoption review next — 2026-11-04

#22 is now **partial/open**: its declared fragment source/scientific contract
is accepted, while full-receptor/preparation/environment/biological gates remain.
See [report](pending_proposals/native_eralpha_validation.md),
[contract](eralpha_validation.md) and
[receipt](evidence/eralpha_acceptance_20261104_summary.json). At clean receiving
**b2b952873db709dbb40d66ae20848a5f8b71b3cc**, 17 fresh controls pass in 480.51 s
(three input/audit, eight interface, six diagnostic), zero failures/errors/skips;
four expected B-factor-drop warnings. No new full suite is claimed.

The unchanged original CLI independently prepares both host-attribution profiles,
retaining 4,047 atoms/4,088 bonds, 1,995 observed heavy atoms, 2,052 local H and
the declared 304–550 fragment/EST. Original source identity/maps/coordinates stay
unchanged. Twelve frozen hydrophobic pairs and independent distances give six
observed sites; empty H-bond/pi-pi families retain coverage. Five ligand-reference
sites remain hypotheses. The 11-site essential model preserves declared weights,
reference/displaced fit 1/0, donor/orthogonal-normal negatives 7/8 and normal-sign
invariance. An independent 153-sphere exclusion collision veto retains fit one.
H5MSM history/unknowns/maps/analyses, JSON bibliography and unit-policy recovery pass.
Both profiles share scientific hash `e57e345f637cd7e71979ebf2faff31582753d6681b75687814571affae6282ba`;
actual credit is 5 items/25 uses host-off and 16/64 host-on. Both original native artifacts are retained verbatim
in separate checksum-qualified gzip archives.

All three unchanged cookbook blocks pass, including diagnosis. Supplementary
off/on diagnoses reuse the exact prepared recipe input: eight candidate triples,
fixed H-bond counts 0/6/2/0/1, 29 rings/28 pair distances and aromatic counts
0/0/1. Actual diagnostic credit is 5 items/11 uses host-off and 8/14 host-on; science/source/cached
observations remain unchanged. Loaded source/native/helper/test/input and runtime
versions stay stable. Full identity is true for focused/driver and false for
examples: four stale canonical distribution metadata/direct_url lookups trigger
the original wrapper exit 1 after science completes. Both snapshots and the exact
changes remain under workspace #82; no prefix repair, scientific rerun or false
full-identity pass is claimed. Strict isolated original-page rendering uses two neighbor stubs.
Initial temporary external-link staging/missing-config render failures and their
correction are retained. No scientific correction or runtime/test/input/provider/
prefix/sibling change is needed; source/runtime remains 0.4.0+62.g6a7537b.

MolSysMT owns molecular preparation/inspection/recognition/geometry/motion/native IO.
PHMT owns explicit case declarations, pharmacophoric interpretation/curation and
matching. General rejected-reference diagnostics (#350) and environmental H (#323)
were observed open; the independent intersection oracle remains only in a fixed-
case test. The legacy snapshot's derivation, excluded residues/full receptor,
peptide stereo, environmental refinement and biological enrichment remain pending.
Do not repair chemistry locally, infer missing #66 binding protocols or relabel
geometry controls as biological negatives. Original October evidence stays historical.

**Next: #6 support-library/developer-tool adoption review.** Inspect current
ArgDigest/PyUnitWizard/SMonitor/DepDigest boundaries and actual pinned tool evidence;
reuse valid #19/source receipts with explicit limits. Identify concrete remaining
work and keep source review, public/provider floors, exact installed artifacts and
central adoption states separate. #19 delivery, #23/#10/#9 and workspace #82 keep
their gates; #41 public/floor/installed receiving and historical donor-absence
retirement remain partial (review 2026-11-11). #60 retains its concrete-consumer
scope. Addon/new release defer. Owned /tmp/phmt22-acceptance-20261104-vuaam0td/,
LMMV/dprada, review 2026-11-18; borrowed #69 prefix/providers/native unchanged.
No local process remains after checkpoint.

## Optional attribution source/API accepted; package receiving pending — 2026-11-04

#19 is now **partial**, not closed: the source/API review is accepted, while its
delivered-package/all-minor public-provider gates remain under #10/#23. See the
[maintained report](pending_proposals/native_ackredit_attribution.md) and
[new receipt](evidence/attribution_acceptance_20261104_summary.json). At clean
**213df1116163419e3164df4dc0673c56f178b2a2**, 39 fresh controls pass in 17.52 s
(21 attribution, 18 contracts), zero failures/errors/skips. Ten intentional warnings
retain five original groups; no new full suite is claimed.

Fresh host-off/on workflows preserve scientific outcomes, original molecular
domains and analytical retrospective scores [1,1,0] with perfect known ranking.
Application sessions remain intact; off/on workflow capture has 3 items/6 uses
and 12/39 respectively. Host-off does not disable upstream attribution. Independent
pose results retain the same 11 items/15 uses despite reuse; mutating one leaves
the other unchanged. Host suspension, successful empty recognition, JSON/YAML and
five saved-report formats pass. A fresh engine-blocked reader preserves original
records, all five reports and identical BibTeX with zero new credit.

Reached-method controls credit mixed-class BEDROC, nonempty clique enumeration
and adapted G3PS seed ranking/assignment; undefined single-class metrics, empty
graphs and empty neighborhoods do not claim those unreached branches. Contexts
retain adaptations/omitted stages. Design-only papers stay absent. Cookbook prose
now distinguishes delivered clique/G3PS stages; both Python blocks stay unchanged
and pass. Refreshed original/provider citation checks retain their bounded sources.

Global real-provider registration failure under warnings-as-errors retains the
scientific result, original scientific error and session, with observed MSM-WARN-
ATTR-001/PHMT-W102. Tracking is failed with no complete references. Strict isolated
reviewed-page rendering uses four neighbor stubs; full source/native/helper/test/
input/metadata identities stay stable in four phases. No runtime/test/provider/
prefix/sibling change is needed. All initial owned execution attempts pass.

The verified 2026-10-13 public 0.23.0/0.12.0 receipt remains historical; it is not
current/all-minor/installed qualification. Current controlled Ackredit source is
not evidence of recommended public 0.12.1 receiving. Public extra/floor/support/
release/platform/hosted claims remain unchanged. Ackredit owns capture/rendering/
sessions; MolSysMT owns molecular work; PHMT owns optional activation and its
scientific branch declarations.

**Next: #22 bounded prepared ERalpha source/scientific acceptance.** Review its
current maintained fragment chain, original input/map/preparation receipts,
independent deposited-contact and directional/exclusion controls, persistence,
actual attribution, recipe and qualified provider identity. Preserve unresolved
full-receptor/preparation/biological gates explicitly; do not guess missing #66
binding protocols or implement molecular preparation in PHMT. #19 delivery resumes
only through exact-candidate #10/#23 gates; no release/addon is requested now.
#41 public/floor/installed migration and historical donor-absence retirement remain
partial, review 2026-11-11; #60 keeps its concrete-consumer scope. Hosted #9 and
workspace #82 remain separate. Owned /tmp/phmt19-acceptance-20261104-aqj9ubv7/,
LMMV/dprada, review 2026-11-18; borrowed #69 prefix, normal editable PHMT
0.4.0+62.g6a7537b and providers/native unchanged. No local process remains after
checkpoint. Historical evidence and metadata findings retain their original scope.

## Observed extraction and placed poses accepted; attribution review next — 2026-11-03

#13 is resolved with its [archive](archive/molsysmt_placed_pose_workflow.md) and
[receipt](evidence/placed_pose_acceptance_20261103_summary.json). Clean receiving
**1eea04d6f92b2e58d8603aa95e204f3e9fa0caf2** passes 99 fresh controls in 16.66 s:
14 pose, eight retrospective, 44 metric, 18 contract and 15 observed donor-geometry
controls; zero failures/errors/skips/warnings. No new full suite is claimed.

Fresh off/on real-provider capsules collapse repeated observations into one site
per participant while retaining both evidence records. Donor/local/source/frame
mappings, atomic acceptors, direct/dispatcher equivalence and shared public MolSysMT
motion pass. Wrong frame/direction and displaced poses reject. Essential priority,
zero-weight essential requirements, one-to-one assignment, optional weights,
minimum coverage and heavy-atom exclusions remain distinct. Covered-empty models
are not valid queries. Unsupported kinds/nonzero periodic images are explicit
native-record controls, without a new molecular implementation.

Batches preserve matched/failed/matched/not_matched at [0,1,2,3]; failure has fit None
and source-stage/cause evidence. The explicitly placed facade retains every result
and returns hits [0,2]. Retrospective generators preserve original classes 3/2,
failures [0,4], evaluated [1,2,3], scores [1,1,0], AUC/BEDROC one. Six JSON/YAML
round trips per profile, molecular domains and original observations stay unchanged;
actual credit is 3 items/12 uses off and 12/43 on. Off/on scientific outcomes agree.

Accepted chemistry boundary: observed roles and evaluation SMARTS are distinct
definitions. A caller-declared explicit C-H donor geometric observation converts
but is rejected with zero coverage under smarts_donor_acceptor; it is not a
conventional hydrogen-bond claim. Profile-control credit is 4 items/5 uses off,
12/22 on. The unchanged example passes (11/23); strict isolated original-page
rendering uses six neighbor stubs. Full identities stay stable in four phases.
One supplementary oracle initially used the wrong recognition key; original/log
and key-only correction are retained. No runtime/test/input/provider/prefix/sibling
change is needed. The normal editable runtime stays 0.4.0+62.g6a7537b.

**Next: #19 optional attribution contract review**: lazy activation/absence,
application-owned sessions, detached payloads and repeated references, reached-
branch method/software credit, provider-failure isolation and original scientific
errors, saved-reader/reporting without new credit, cookbook and current guards.
Read its 2026-10-13 public receiving receipt before choosing new checks. Preserve
its delivered-package/all-minor public receiving as pending unless separately
qualified; local source acceptance alone cannot close that scope. #22's biological
pilot and #66's missing original binding methods remain independent.

MolSysMT owns all molecular work; PHMT owns pharmacophoric interpretation/matching/
accounting. Historical modeler/screener migration is delivered under its own issues;
no implicit preparation/search is added. #41 public/floor/installed receiving and
historical donor-absence retirement remain partial, review 2026-11-11. #60 keeps
its concrete consumer gate; hosted #9, installed/public/platform #23/#10 and workspace
#82 remain separate. Addon/new release defer. Owned /tmp/phmt13-acceptance-20261103-k2desp6c/,
LMMV/dprada, review 2026-11-17; borrowed #69 prefix/providers/native unchanged. No
local process remains after closeout. Historical evidence keeps its original scope.

## Native reference-ligand construction accepted; placed observations next — 2026-11-03

#14 is resolved with its [archive](archive/native_reference_ligand_workflow.md)
and [receipt](evidence/reference_ligand_acceptance_20261103_summary.json). Clean
receiving **a3cd1f5ec6da2b4ee81e17605290e02815ad3dfb** passes 53 fresh controls
in 18.54 s: seven reference, 14 provider-route, 14 pose and 18 contract controls;
zero failures/errors/skips/warnings. No new full suite is claimed.

Fresh host-off/on fixed prepared inputs cover six families and 15 essential,
unit-weight sites. Direct/cached/dispatcher sites agree. Known donor vector,
unoriented aromatic normal, grouped charge participant/geometry memberships,
centroids and signs pass. Reference/displaced/chemistry-absent scores remain 1/0/0;
reversing only explicit donor H preserves its center but gives coverage 14/15,
not_matched. Partial groups, unsupported features and empty queries fail visibly.
JSON/YAML unit-policy round trips preserve constraints, provenance, geometry and
pose outcomes. Source atom/state/coordinate domains and tracking-independent science
remain unchanged; actual credit is 3 items/6 uses host-off and 11/25 host-on.

The unchanged documented block passes with credit 12 items/36 uses. Strict isolated
original-page rendering uses four neighbor stubs. Full source/native/helper/test/
input/metadata identities remain stable in all three phases. The initial capsule
failed a cross-policy exact dictionary oracle; independent saved-query diagnosis
shows roundoff at most 2.220446049250313e-16 nm with exact constraints/provenance.
Only the one-off physical-comparison assertion changes (1e-12 tolerance). The first
renderer needed its temporary stubs added to a hidden toctree. All attempts and
original outputs are retained; no runtime/test/input/provider/prefix/sibling change
is needed. MolSysMT owns molecular work; PHMT owns pharmacophoric constraints,
cached inventories, matching and provenance. The historical #41 absence branch
is not retired by this acceptance; atomic acceptors do not imply ideal #375 geometry.

**Next: independently accept #13 observation-to-query and already-placed pose
evaluation.** Review actual MolSysMT observations, selected frame/state/source
mappings, directional versus positional constraints, essential/one-to-one/excluded-
volume semantics, shared rigid/unit invariance, recorded failures and legacy-entry
migration. Reuse delivered provider tools and existing analytical/recipe guards;
do not add molecular implementations or turn placed evaluation into implicit search.
Then accept #19 attribution. #41 supported-public/floor/installed receiving and
legacy retirement remain partial, review 2026-11-11. #60/#66 retain their gates;
hosted #9, installed/public/platform #23/#10 and workspace #82 stay separate.
Addon/new release defer. These are source/API analytical controls, not biological,
performance or published-delivery qualification.

Owned /tmp/phmt14-acceptance-20261103-wi6edou1/, LMMV/dprada, review 2026-11-17.
Borrowed #69 venv remains normal editable PHMT 0.4.0+62.g6a7537b with unchanged
controlled providers/native. No local process remains after closeout. Earlier
reports/evidence/metadata findings keep their dated scopes.

## Prepared rigid pose search accepted; reference construction next — 2026-11-03

#15 is resolved with its [archive](archive/native_rigid_pose_search.md) and
[receipt](evidence/rigid_search_acceptance_20261103_summary.json). Clean receiving
**1e00aca9a9f389adbeca41ff00388ce02570b895** passes 68 fresh controls in 42.89 s
(13 rigid, 26 seeded scoring, eight retrospective, 21 attribution), zero failures/
errors/skips. Ten intentional optional/cross-provider attribution-failure warnings
retain their original groups/logs. No new full suite is claimed.

Fresh off/on prepared controls recover moved poses, reject reflection/distortion/
missing chemistry, and compose independent proposals/public MolSysMT alignment.
Admissible identity and fitted unit-coverage hits preserve incomplete enumeration
with zero/one fit, while legitimately proving the compatibility maximum. Exclusion
veto at fit one is not such a proof; unfinished unproven work retains search_budget/
PHMT-E105 failure. Explicit seed-only no-pose negatives retain fit None, no invented
assignments and binary zero; failed searches remain separately unscored. Compatibility
partial coverage remains pose evidence, with explicit retrospective scoring consent.

A six-input analytical full retrospective run retains repeated/generator identity,
three active hits and AUC/BEDROC one. The limited run preserves original classes
3/3, failures [1,3], evaluated indices [0,2,4,5], scores [1,1,0,0] and two evaluated
inputs in each class. JSON/YAML round trips under changed units preserve metadata
and outcomes. Source domains stay unchanged under like-unit-policy comparisons;
off/on science agrees with credit 3 items/6 uses host-off and 13/50 host-on. Both original
example blocks pass (13 items/50 uses); strict isolated rendering uses three neighbor
stubs. Full identities are stable in focused/workflow/example phases. A first
wrong-path launcher exited before imports/tests and is retained separately.

No library/test/input/scientific-definition/provider/prefix/sibling change is needed.
All molecular construction/inspection/motion/fit/copy/get/set/RMSD use MolSysMT;
PHMT owns pharmacophoric proposals, pose constraints, termination/score interpretation
and failure accounting. These are finite prepared fragment controls, not biological,
performance, continuous/global or published-delivery qualification.
**Next: #14 reference-ligand source/API acceptance**, reviewing six-family shared
recognition/geometry, grouped participant mappings, query construction, placed
matching, persistence and its example. Then consolidate #13 observation/placed-pose
and #19 attribution contracts. #63's independent binary criterion stays intact.
#41 public/floor/installed receiving and legacy retirement stay partial (review
2026-11-11); #60/#66 retain their gates. Hosted #9, installed/public/platform #23/#10
and workspace #82 remain separate; addon/new release defer.

Owned `/tmp/phmt15-acceptance-20261103-yioexkdv/`, LMMV/dprada, review 2026-11-17.
Borrowed #69 venv remains normal editable PHMT 0.4.0+62.g6a7537b with unchanged
controlled providers/native. No local process remains after closeout. Historical
reports/evidence/metadata findings retain their original scopes.

## Ranked-seed stage accepted; prepared rigid search next — 2026-11-03

#28 is resolved with its [archive](archive/g3ps_ranked_seed_tools.md) and
[receipt](evidence/ranked_seed_acceptance_20261103_summary.json). Clean receiving
**9731e054b9eb56b5b9a121dd889af214773b0643** passes 82 fresh controls in 23.11 s
(22 ranked, 60 geometry), zero failures/errors/skips. No new full suite is claimed.
Cached typed assignment/ranking, independent oracles, empty/unequal axes, identity/
unit/motion invariance, ownership, saved reports, preflight budgets, consumer calls
and actual adapted-stage attribution retain guards.

Fresh off/on capsules preserve plain/ranked-all's 16-seed family and eight accepted
mappings/geometries, with 16 fits each. One selected seed omits 15, performs one fit
and completes without models, missing a known four-feature solution. Computation
limits fail explicitly; they cannot silently select fewer guesses. Twelve pose
checks and two JSON/YAML round trips per profile pass. Original reflected poses
remain partial nonmatches (.75), references and public MolSysMT replay match (1).
Source domains remain unchanged under like-unit comparisons; off/on science agrees.
Credit is 0 items/0 uses host-off and 14/77 host-on; four cookbook blocks pass (14 items/70 uses)
and summary rereading adds no credit. The page fixes stale refinement prose; every
Python block is unchanged and the published page matches strict isolated staged
rendering with two neighbor stubs. Primary section 2.2.1 is freshly accessible at
PMC; earlier access failures remain historical. Stage-only adaptation stays explicit.

The original comparison runs after owned tests/docs end: 14 sequential isolated
workers, seven frozen cases/two strategies, one warmup/three timed calls/separate
citation. All expectations/stability checks pass: eight completed/five empty/one
failed PHMT-E107 record. All 42 samples, sources/native/environment and actual
references remain archived. Timed ranked calls select one seed; ranked-all is not
timed. Whole-worker RSS (302.3–507.1 MiB) includes setup/warmups.
Costs with changed coverage/alternatives do not justify a universal ranking,
equivalent-recall speedup or new default seed limit. Full identities stay stable
in all four phases; no runtime/test/input/provider/prefix/sibling change is needed.

All molecular operations use MolSysMT; PHMT owns cached pharmacophoric neighborhoods
and selection, SciPy generic assignment. **Next: #15 prepared rigid pose-search
acceptance**, reviewing independent public proposals/alignment, search completion,
valid maximum-coverage early stops, failure accounting and retrospective composition.
#29 refinement is already resolved; rescue needs its separate scientific/provider
contract. #41 public/floor/installed receiving and final legacy retirement remain
partial (review 2026-11-11). #60/#66 retain independent gates; hosted #9,
installed/public/platform #23/#10 and workspace #82 remain separate. Addon/new
release stay deferred.

Owned `/tmp/phmt28-acceptance-20261103-guahqzj6/`, LMMV/dprada, review 2026-11-17.
Borrowed #69 venv remains ordinary editable PHMT 0.4.0+62.g6a7537b with unchanged
controlled providers/native. No local process remains after closeout. Original
historical evidence and earlier metadata findings retain their dated scopes.

## Modular comparison accepted; ranked seeds next — 2026-11-03

#27 is resolved with its [archive](archive/modular_rigid_strategy_comparison.md)
and [receipt](evidence/rigid_comparison_acceptance_20261103_summary.json). Clean
receiving **50776a15dd2cb103a7b56d65834f2f1d202651e6** passes 23 fresh controls
(13 objective/frozen-case, 10 modular), no failures/errors/skips, in 52.85 s.
No new full suite is claimed. Public cached query/explicit placement/saved summary
contracts retain their molecular-access, source ownership, completion and credit guards.

Fresh same-four-pair MolSysMT RMSD capsules give .11 nm/zero matches for full mapping
and .21865464043704247 nm/three matches for a triplet. The four-essential-site query
remains not_matched at partial fit .75. All nine pose checks/two JSON/YAML round
trips per tracking profile pass; source domains and off/on science stay unchanged.
Actual credit is 3 items/3 uses host-off and 12/47 host-on. Three cookbook blocks pass
(13 items/58 uses); summary rereading adds no credit, strict isolated rendering uses two
neighbor stubs. An initial one-off comparison included inherited bibliography;
its failed script/log/queries and diagnosis remain preserved, with all unfiltered
outputs retained. Only the two bibliography fields are excluded from science.

After those tasks finish, the unchanged CLI passes all 12 controls across six
frozen cases/two families: five completed, five completed-empty and two expected
PHMT-E107 failures. Each isolated sequential worker has one warmup, three timed
calls and separate actual citation. All 36 samples and complete original outputs
are archived; source/native hashes agree across workers and all four phases.
No owned test/build/benchmark load overlaps measurements. Current observed times
and whole-worker RSS (302.0–506.9 MiB) remain descriptive; outputs
differ, RSS includes setup/warmups, and no universal ranking/default change follows.
Association yields four fits/zero warped-square models, triplets sixteen fits/
sixteen three-site alternatives, without a distinct-binding-mode claim.

No runtime/test/input/scientific-definition/provider/prefix/sibling change is needed.
All molecular operations and generic RMSD use MolSysMT; PHMT owns pharmacophoric
query/proposal/acceptance/summary/assembly. Clean installed/public/platform/hosted
qualification remains #23/#10/#9, and inherited workspace #82 is independent.
**Next: #28 ranked triplet seeds**, reviewing typed neighborhoods/assignment,
independent oracles, all-seed family equivalence, limited-seed false negatives,
resource-before-allocation, consumer composition and actual adapted-stage credit.
#41 public/floor/installed receiving and legacy retirement stay partial (review
2026-11-11); #60 and #66 retain their independent gates. Addon/new release defer.

Owned `/tmp/phmt27-acceptance-20261103-p_h5tcap/`, LMMV/dprada, review 2026-11-17.
Borrowed #69 venv remains ordinary editable PHMT 0.4.0+62.g6a7537b with unchanged
controlled providers/native. No local process remains after closeout. Historical
reports/evidence and earlier metadata findings retain their original scopes.

## Prepared rigid unaligned consensus accepted; comparison next — 2026-11-03

#26 is resolved with its [archived report](archive/native_rigid_consensus.md) and
[new receipt](evidence/rigid_consensus_acceptance_20261103_summary.json). Clean
receiving head **0bab03aaa089418be11d2be2efb3c8bd6f7ff29e** passes 95 fresh
controls in 50.44 s (25 rigid, 10 modular, 60 correspondence geometry), without
failures/errors/skips. No new full suite is claimed. Both finite proposal families,
independent mapping oracle, degenerate/reflected geometry, six symmetric mappings,
explicit source/frame/pivot, budgets, provider errors and actual credit retain guards.

Fresh off/on capsules execute five frozen analytical cases with both methods.
Typed recovery adds a nonempty unplaced charge source and retains its original
feature/support denominator (2/3). Atom coordinates recover within 1e-12 nm.
Association uses one fit/model; triplets eleven fits/seven models. Symmetry retains
six mappings/layouts/models per family. Reflection and empty source complete
without models; the exhausted fit budget fails PHMT-E107/complete=False. Each
profile records four completed, four completed-empty and two expected failures,
20 models, 112 passing pose evaluations (56 positives/56 negatives) and eight
JSON/YAML round trips across units. Original frames remain unchanged and fail
queries in the pivot frame; public MolSysMT placement replay passes. Off/on
science agrees. Credit is 3 items/6 uses host-off and 16/75 host-on; both cookbook
blocks pass (16 items/68 uses), as does strict isolated rendering with four
neighbor stubs. Full identities are stable in all three phases.

No library/test/input/scientific-definition/provider/prefix/sibling changes are
needed. All molecular conversion/inspection/motion/fitting/copy/set/RMSD/replay use
MolSysMT. PHMT owns pharmacophoric proposal/acceptance and bounded assembly;
NetworkX owns generic clique enumeration. The October strategy survey remains
dated; fresh primary-text access is limited and transparently retained in the
receipt, with no full re-review or external implementation/performance claim.

**Next: #27 modular tools and reproducible strategy comparison**, reviewing the
standalone report/placement contract, unchanged original opt-in driver, frozen
warped-square counterexample, source/input identities, isolated timing/repeats,
honest memory scope and actual attribution separately from timing. The ten modular
guards passing here do not close that broader comparison. #26 is one pivot with
finite proposal families, not a continuous/global optimum or biological validation.
#41 public/floor/installed receiving and final legacy retirement remain partial
(review 2026-11-11). #60 independent-copy receiving and #66's four original binding
methods retain their scopes. Addon/new release remain deferred; hosted #9,
installed/public/platform #23/#10 and workspace #82 retain their gates.

Owned `/tmp/phmt26-acceptance-20261103-o71te38f/`, LMMV/dprada, review 2026-11-17.
Borrowed #69 venv remains ordinary editable PHMT 0.4.0+62.g6a7537b with unchanged
controlled providers/native. No local process remains after closeout. Original
historical reports/evidence retain their identities and scopes.

## Aligned clique consensus accepted; rigid unaligned method next — 2026-11-03

#24 is resolved with its [archived report](archive/native_aligned_clique_consensus.md)
and [new receipt](evidence/aligned_clique_acceptance_20261103_summary.json).
Clean receiving head **17fb209ed38924af1ea9dc5b5ceb359bfb4b51bc** passes 60
fresh focused controls in 16.54 s (25 clique, 17 aligned, 18 contracts), no failures/
errors/skips. Independent subset oracles cover maximal cliques and jointly supported
disjoint packages. Typed orientations, reordering, source/frame/state, bounds,
empty/failure separation and real optional attribution/readers retain their guards.
No new complete full-suite execution is claimed.

Fresh off/on analytical capsules pass absent-first-ligand discovery, center .17 nm,
RMSD .02 nm, support 2/3, two overlapping alternative models and exactly three
whole-supported two-site packages (AC, BC, CD), with no unsupported triple. Empty
molecular discovery emits no model; each budget raises PHMT-E107/complete=False
without partial success. Three models pass six JSON/YAML round trips; all 29 pose
evaluations per profile pass (18 positive, 11 negative). Narrower radius rejects
contributors while retaining support. Source molecular domains remain unchanged
within each unit policy. Off/on science agrees; actual credits are 3 items/6 uses
off, 15/37 on. Three unchanged cookbook blocks and strict isolated rendering pass
(one attribution link-target stub), with actual recipe credit 12/30. Full identities
are stable in all three phases.

The initial capsule/diagnostic fail a cross-unit-policy byte hash; a no-model
experiment reproduces rounding up to 5.55e-17 nm. Scripts/logs are preserved as
failed attempts. The final script compares identical policies and also checks exact
default-policy before/after equality. No library/test/input/tolerance/provider/
prefix/sibling change is needed. All molecular operations use MolSysMT; PHMT owns
cached pharmacophoric compatibility/aggregation/packages, NetworkX generic cliques.

**Next: #26 prepared rigid unaligned consensus**, independently reviewing both
correspondence proposal families, proper MolSysMT fitting/transformation, accepted
placements/alternatives, post-fit geometry, support including unplaced sources,
budgets, persistence and actual attribution plus its cookbook. Current #24 success
does not close that distinct method or establish continuous global optimality.
#41 remains partial for supported-public/floor/installed receiving and final legacy
retirement (review 2026-11-11). #60 is available for a concrete independent variant;
#66 awaits four original binding methods. Addon/new release remain deferred.
Hosted #9, installed/public/platform #23/#10 and inherited workspace #82 retain
their gates. These analytical controls are not biological/performance qualification.

Owned root `/tmp/phmt24-acceptance-20261103-vw26hupl/`, LMMV/dprada, review
2026-11-17; borrowed #69 venv remains normal editable PHMT 0.4.0+62.g6a7537b,
with unchanged controlled providers/native. No local process remains after closeout.
All historical evidence and original October report text remain unchanged.

## Reference-anchored aligned consensus accepted; clique method next — 2026-11-03

#21 is resolved with its [archived report](archive/native_aligned_consensus.md)
and [new receipt](evidence/aligned_reference_acceptance_20261103_summary.json).
Clean receiving head **daae2d226f17f91e521425abfb779268bfad4b7e** exactly matches
code 6a7537b's runtime/helper/test/driver/workflow trees, actual loaded sources/
native bytes, helper/input hashes and metadata. The prior 418-item execution,
including all **17 aligned-consensus controls**, is verified/reused with its
original receipt hash/XML. No fresh pytest or complete full-suite run is claimed.

Fresh analytical off/on workflows pass: independent center .17 nm, RMSD .02 nm,
support 2/3 including the empty-feature ligand. The base .06 nm query accepts
both contributors and rejects sodium (fits 1/1/0); a .005 nm query retains support
two yet rejects both contributors. Matching/aggregation compose, unsupported
construction fails PHMT-E102/null fit, and matrix budget exhaustion fails
PHMT-E106/null fit. JSON/YAML under different unit policies retain metadata/radius
and all pose outcomes. All 11 evaluations per tracking profile pass; declared
atom identity/chemical state/coordinates remain unchanged. Off/on science agrees,
with actual capture 3 items/3 uses off and 11/29 on. Both cookbook blocks and
strict isolated rendering pass (two neighbor stubs), with actual recipe credit
11/22. Full identities are stable in both fresh phases.

**Ownership:** all molecular conversion/translation/inspection/recognition and
geometry/state access use MolSysMT. PHMT's public tools match and aggregate
cached pharmacophoric features, counting declared IDs and retaining reference
orientation; no molecular/angular kernel or hidden preparation/alignment is added.
No library/test/fixture/scientific-definition/provider/prefix/sibling change is
needed. A missing import in the first one-off acceptance script is retained as an
incomplete attempt, corrected only in that script.

**Next: #24 aligned-clique acceptance**, independently reviewing reference-free
site discovery, alternative jointly supported hypotheses, graph/clique budgets,
occurrence conflicts, rejection/completion evidence, persistence and actual
attribution plus its executable example. Current tools support that work. #21 is
not a claim of exhaustive search, ligand chemical uniqueness, affinity, biology
or performance. #41 remains partial for supported-public/floor/installed migration
and final historical fallback retirement (review 2026-11-11). #60 is available for
a concrete independent variant; #66 awaits four original binding methods.
Addon/new release remain deferred; hosted #9, installed/public/platform #23/#10
and inherited workspace #82 keep their gates.

Owned root `/tmp/phmt21-acceptance-20261103-7sqezsdu/`, LMMV/dprada, review
2026-11-17. Borrowed #69 venv still resolves editable PHMT 0.4.0+62.g6a7537b with
unchanged controlled providers/native. No local process remains after closeout.
Original archives/provider/warning history remain unchanged.

## Aromatic workflow accepted; aligned consensus next — 2026-11-03

#34 is resolved with its [archived report](archive/native_aromatic_interactions.md)
and [new receipt](evidence/aromatic_acceptance_20261103_summary.json). Source
receiving head **ee257a1aaec6ea02a185e6961b0deea9769f7fbf** is clean and matches
measured code 6a7537b across tracked runtime/helper/test/driver/workflow trees,
actual loaded sources/native bytes, helper/input hashes and metadata. Its prior
418-item execution includes **46 aromatic controls**, zero failures/errors/skips;
that original receipt/XML is verified and reused, not called a new pytest run.

Fresh execution passes both aromatic driver profiles: seven native profiles,
14 case/profile combinations, 28 queries/84 evaluations each. Source atom
identity/chemical state/coordinates and native persistence remain unchanged.
Reference/round-trip positives fit one; displacement negatives fit zero. The one
expected strict compound-cation failure per profile retains fit_value=None; the
explicit containing-center alternative retains three original observations/charges.
Off/on science agrees; actual credit is 6 items/11 uses off and 14/30 on. All three
cookbook blocks and strict isolated rendering pass (one exclusion link-target
stub). Full identities are stable in both fresh phases. No runtime/test/input/
expectation/provider/prefix/sibling changes are required. October/#35 archives
and earlier #32/#82 workspace findings retain their original identities/scopes.

**Next: #21 reference-anchored aligned consensus**, reviewing matching/unique-
identity support, center aggregation/reference orientation, rejection/budget
semantics, provenance/persistence, actual attribution and its cookbook; then
#24's distinct aligned clique discovery. Both use current qualified molecular
operations and can advance now. Neither should be closed from aggregate counts
alone. #41 remains partial only for its supported-public/floor/installed migration
and final historical arithmetic retirement (review 2026-11-11); ideal acceptor
models remain separate #375 science. #60 is available for a concrete independent
variant; #66 still awaits four original binding methods. Addon/new release defer.

Owned root `/tmp/phmt34-acceptance-20261103-pxec9r01/`, LMMV/dprada, review
2026-11-17. The borrowed #69 venv still resolves editable PHMT 0.4.0+62.g6a7537b
and unchanged controlled providers/native. No local process remains. Hosted #9,
clean installed/public/platform #23/#10 and inherited workspace #82 remain
separate; no new full suite, biological, energy or performance claim is inferred.

## Observed donor vectors delegated; aromatic acceptance next — 2026-11-03

Clean code **6a7537beb5747f8f455c489f0908ce4c46b90fd6** migrates the identified
from_interactions H-bond vector to public MolSysMT and shares bounded receiving
validation with get_features. Recognition/profile, ordered participants, local/
source/frame axes and repeated observation evidence are preserved. Modern donor
sites add detached geometry/route provenance; errors or invalid provider output
propagate. One labeled genuine-old-provider absence branch retains historical
arithmetic. No provider/native/pin/floor or chemical/scientific definition changes.

The [receipt](evidence/observed_donor_receiving_20261103_summary.json) records
**418 modern controls**, zero failures/errors/skips (327.52 s), including all 15
new donor guards. **14 original-public-payload controls** pass without skips.
The frozen 0.23.0 Conda SHA and all 3,213 extracted files match before/after; this
uses inherited dependencies and is not clean ordinary installed qualification.
Both original drivers pass with tracking off/on: composition retains 23
observations/nine sites/nine evaluations; CCD eight roles/48 evaluations per
profile, original directional/steric/persistence outcomes and unchanged complete
chemistry/coordinates/bytes. Actual credits remain complete. Full physical and
metadata identities agree in all four phases. No new complete suite is claimed;
previous full-suite and #32/#82 metadata results retain their dated scopes.

Fourteen new-contract controls fail before the migration; two refine the existing
coincident-input rejection diagnostics. One no-donor control already passes.
An initial fixture-threshold error and incomplete quota attempts are retained
separately. The normal editable refresh succeeds only after actual quota recovery;
complete pre/post manifests prove provider/native equality. PHMT runtime is now
0.4.0+62.g6a7537b in the owned #69 venv. Only completed own build/HTML derivatives
(58,728,806 bytes) and its task-only download cache are retired; all source/config/
logs/scientific originals, the frozen wheel, providers/native and environments
remain. Exact driver JSON bytes are kept in verified gzip to limit scratch usage.
Canonical prefix and sibling worktrees are untouched.

**Next: #34 aromatic acceptance**, independently checking its profile/participant
mapping, geometry, empty/failure/persistence and actual attribution, driver and
cookbook. The #41 modern caller migration is received; #41 stays partial for
supported public delivery, justified floor/installed receiving and final historical
fallback retirement, review 2026-11-11 (LMMV/dprada). Ideal acceptor models remain
separate #375 science. #60 is available for a concrete independent variant; #66
still needs four original methods. Addon/new release remain deferred. Hosted gates
stay #9, installed/public/platform #23/#10 and inherited workspace #82.

Owned root `/tmp/phmt41-donor-20261103-v7u6z70u/`, LMMV/dprada, review 2026-11-17.
No local process remains after closeout. These are analytical/source controls,
not biological or performance qualification. Original archives remain unchanged.

## Ionic acceptance complete; remaining donor-vector caller next — 2026-11-03

#33 is resolved with its [archived report](archive/native_ionic_interactions.md)
and [new receipt](evidence/ionic_acceptance_20261103_summary.json). Clean producer
**16614ae7cc0f32544badea0b6de6770e1a64edce** passes **45 focused controls**, zero
failures/errors/skips, in 19.88 s (24 ionic, 14 pose, seven reference). Both
original driver profiles pass six queries/18 evaluations each. Three cookbook
blocks and strict isolated recipe rendering pass without neighbor stubs. Whole
charge membership, provider centroids, repeated contacts, state/source/unit maps,
negative poses and native persistence retain original expectations. Actual credit
is nine items/18 uses enabled and one provider item/use host-disabled. Physical
and metadata identities are equal in all three phases. Earlier #32/#82 metadata
lookup differences remain their original unresolved observations.

**Next implementation: #41's newly identified H-bond donor-vector caller.** The
ionic audit finds direct coordinate subtraction in from_interactions' H-bond
branch. get_features delegates vectors correctly, but that prior gate did not
cover every molecular caller. Migrate this existing branch to already available
public MolSysMT vectors with shared bounded validation and unchanged observed
profile/ordered participant/frame semantics. Do not swap chemistry definitions
or fallback after available-provider failure. Owners LMMV/dprada, review
2026-11-11; current H-bond pose regressions are interim functional controls.
This source migration can proceed now; public-minimum/old-public retirement and
ideal acceptor models remain separate. Then accept #34 aromatic queries.

No runtime/test/input/provider/prefix/sibling changes are needed for #33. The
owned #69 venv remains ordinary editable PHMT 0.4.0+56.g9387852 with controlled
MolSysMT 0faf1584/providers/native unchanged. Owned root
/tmp/phmt33-acceptance-20261103-rk5qeyp_/, LMMV/dprada, review 2026-11-17.
No local process remains. Original archives remain unchanged; the old full-suite
baseline is not a new complete run. #9 hosted, #23/#10 clean installed/public/
platform and #82 inherited workspace gates remain separate. #60 is available for
an actual independent-variant consumer, #66 awaits four original methods, and
addon/new release remain deferred. No biological/performance qualification follows.

## Exclusion construction accepted; ionic query review next — 2026-11-03

#32 is resolved with its [archived report](archive/public_excluded_volume_sites.md)
and [new receipt](evidence/exclusion_acceptance_20261103_summary.json). Clean
producer **25d41077a238cd3f5b54e235011df3e5b276531f** passes **26 owning controls**,
zero failures/errors/skips, in 26.06 s. Both unchanged driver profiles and all
three cookbook blocks pass. Strict isolated recipe rendering passes with two
neighboring link-target stubs; no full-site claim. Original source/ligand/heavy
pose, 153 exclusions over 19 residues, source index spaces and native persistence
are preserved. The one-clash and 12-clash vetoes both retain positive fit 1.
Actual enabled credit is 15 items/39 uses; disabled host tracking retains reached
provider credit (4/13). Original evidence and expectations are unchanged.

**Identity boundary:** loaded module versions/source/native/helper/test/input
identities remain stable in all three phases. Distribution-record lookups switch
to older canonical PHMT/MolSysMT/Viewer/DepDigest records; strict full equality
and metadata equality remain **false**, with exact original differences retained.
This is the inherited workspace limitation tracked with #82, not clean installed
closure. No provider/prefix repair or source change is made. Current structure
facade already delegates exclusions under #44; the old Oct03 migration statement
is historical, not an outstanding local kernel.

**Next: #33 ionic observation queries**, then #34 aromatic queries. Check their
own participant mapping, source/frame/state and explicit scientific semantics,
empty/failure behavior, persistence, actual attribution, drivers and cookbooks.
Current providers suffice. #41 public-vector migration stays partial (review
2026-11-11); #60 is available for a concrete independent-variant consumer. #66
still awaits four original binding methods through a new authorized lead. Addon
and a new release remain deferred.

Owned root `/tmp/phmt32-acceptance-20261103-1_kyuklf/`, LMMV/dprada, review
2026-11-17. The owned #69 venv remains ordinary editable PHMT
0.4.0+56.g9387852 with controlled providers/native unchanged. Canonical prefix and
sibling trees are untouched. A transient pre-science sandbox startup quota error
is retained; default execution recovered without cleanup. No runtime/test/fixture
changes or local process remain. #23/#10 installed/public/platform and #9 hosted
gates remain separate. The old full-suite baseline is not a new complete run;
no biological or performance qualification is inferred.

## Prepared CCD foundation accepted; exclusion boundary next — 2026-11-03

#30 is resolved with its [archived report](archive/prepared_ccd_ligand_validation.md).
Clean source **54df39ca4956335cf0d408b02a61f73ce97a0a96** passes all **23 owning
controls**, zero failures/errors/skips, in 75.27 s. The unchanged driver passes
all 12 comparisons under both host tracking profiles: four self controls, two
prepared-frame screens and six cross-ligand hypotheses. All four cookbook blocks
execute. Strict isolated recipe rendering passes with a neighboring notebook
link-target stub; actual notebook/full-site execution is not claimed.

Original EST/DES bytes, chemical identity, H/charge/stereo/bond endpoints and
coordinates are preserved. Raw readiness rejection remains visible; all original
feature/self/cross outcomes pass without changing expectations. Actual attribution
has 21 items/99 uses, including both datasets and distinct resource/method uses.
The [new receipt](evidence/prepared_ccd_acceptance_20261103_summary.json) retains
full outputs, commands/logs/XML and source/native/helper/test/input plus metadata
identities, equal before/after in every phase. October originals stay unchanged.

**Next: #32**, review public native heavy-atom exclusion-sphere construction,
source/selection/frame/state axes, unit-aware centers/radii, empty/invalid inputs,
detachment and attribution; then #33 ionic and #34 aromatic acceptance. Each issue
keeps its own guards, driver and cookbook requirements. #30 needs no code changes.
Current providers suffice for this next local work. #41 stays partial for public
vector delivery/installed qualification, review 2026-11-11; #60 is available for
an actual independent-variant consumer. #66 still awaits four original methods.
Addon and new release remain deferred.

Owned root `/tmp/phmt30-acceptance-20261103-2mheqiv3/`, owners LMMV/dprada,
review 2026-11-17; borrowed #69 prefix remains ordinary editable PHMT
0.4.0+56.g9387852 with unchanged controlled providers/native. Canonical prefix and
sibling trees are untouched. Shared conflicts stay #82; installed/public/platform
receiving stays #23/#10 and exact-head hosted gates #9. No complete new-source
suite, biological or performance qualification is inferred. The old 1,020-item run
is its original baseline. No local scientific process remains after closeout.

## #41 review complete; public migration remains pending — 2026-11-03

Clean producer **37052f7bb7190046997ba96955d4dea154cf3a91** passes all **165**
designated feature/reference/pose/attribution/conformer/consensus/curation controls,
zero failures/errors/skips, in 127.55 s. Both modern MolSysMT APIs are required
before testing. Controlled provider 0faf1584 and actual editable PHMT
`0.4.0+56.g9387852` are unchanged; all physical and metadata identities agree.
The [receipt](evidence/molsysmt_feature_review_20261103_summary.json) preserves
original snapshots, log/XML, GitHub responses and failed channel requests.

Latest visible GitHub MolSysMT release/tag remains 0.23.0. Official Anaconda
package/main-repodata requests return no contents before timing out; current
channel inventory is unverified. Do not infer absence of newer packages or clean
installed compatibility. Current CI already pins the modern provider; the
Oct28 older-pin statement below is historical. Python/Conda runtime declarations
both have bare `molsysmt`, so 0.23.0 is not a declared floor. #23/#10 retain
delivered-floor/newer-public compatibility qualification. #41 stays partial:
owner LMMV/dprada, existing review **2026-11-11**, removal after identified
supported public vectors and source/installed/public receiving. #375 acceptor
models are separate. No runtime, pin, bound, provider or molecular-kernel change.

**Next local segment: #30 prepared CCD acceptance**, then #32 exclusions, #33
ionic and #34 aromatic queries, each against its own original criteria, driver,
cookbook and source evidence. Recent #36/#37 results support those reviews but
do not close them automatically. #60 can receive native copies for an actual
independent-variant consumer; it is not waiting for #121 implementation. #66
still needs four original binding methods through a new authorized lead.
No new study rules, addon or release. #9 exact-head CI and #23/#10 installed/
public delivery retain their independent gates.

Owned review root `/tmp/phmt41-public-review-20261103-icry1l76/`, LMMV/dprada,
retention review 2026-11-17. Borrowed #69 venv/providers/native bytes and canonical
prefix/sibling trees are unchanged; no public environment is created. Shared
conflicts remain MolSysSuite #82. At this review, all three runs for 37052f7
(CI 41711171488, policy 41711172638, Conda governance 41711172542) remain queued;
this local result does not qualify those hosted gates. No local process remains
from the completed source gate or failed network queries.

## Composition and complete-CCD source/API acceptance complete — 2026-11-03

#36 and #37 are resolved with their [composition](archive/native_interaction_composition.md)
and [CCD](archive/ccd_interaction_composition.md) reports archived. Clean producer
9387852af67a17f59e48d14fc78260ffc4320650 passes 219 coupled source controls,
zero failures/errors/skips, including 41 composition and all 30 CCD cases. The
cached provenance fix rejects inconsistent geometry/source maps and optional site
states before reuse. Eight counterexamples fail before the fix; all nine new
controls pass after it, preserving valid reordered/nonidentity maps and inputs.
No molecular algorithm, detector/profile, geometry, weight or essential semantics
change. #37 needs no additional code or fixtures.

The [composition receipt](evidence/composition_acceptance_20261103_summary.json)
retains two profiles/nine evaluations each, 23 original observations, nine reused
versus eleven kept constraints and actual credits. The [CCD receipt](evidence/ccd_interaction_acceptance_20261103_summary.json)
retains eight role hypotheses/48 evaluations per profile, unchanged complete EST/
DES chemistry, atom/bond/source axes, coordinates and file bytes, empty charge
families, directional controls, rigid covariance and the DES steric veto. Six
cookbook blocks and both strict isolated page builds pass; adjacent link-target
stubs bound those rendering checks. Full code/native/helper/test/input and metadata
identities stay equal in every current phase. Historical original archives remain
unchanged. The 1,020-item full run at 96f917a is a baseline, not execution of the
new correction; no complete new-source suite rerun is claimed.

**Next:** review #41's bounded old-public donor-geometry exception by 2026-11-11.
Check actual supported public vector delivery and source/installed/public receiving
before choosing its retirement/floor migration. Current source already delegates
to MolSysMT; ideal acceptor geometry is a separate #375 scientific contract.
#60 can receive the delivered #121 copy contract when a workflow needs independent
molecular variants; keep model references explicit and do not add a local copy
engine. Other already implemented native slices (#30/#32/#33/#34 and consensus)
retain their own independent acceptance review; aggregate passes do not close
them automatically. #66 still needs the four original binding methods via a new
authorized lead. No study-rule changes or repeated exhausted searches. #323/#375/
#447 keep their provider scopes. Addon/new release remain deferred.

Owned roots: `/tmp/phmt36-acceptance-20261103-1lir6w0a/` and
`/tmp/phmt37-acceptance-20261103-a5qoieik/`, owners LMMV/dprada, review 2026-11-17.
The shared owned #69 venv now imports ordinary editable PHMT
`0.4.0+56.g9387852` after its normal isolated-build refresh. Controlled MolSysMT
0faf1584/Viewer ca7ebea6/DepDigest 13cc7378 and native bytes stay unchanged;
canonical prefix and sibling trees are untouched. Old installed-wheel and earlier
source receipts remain historical. Shared pip conflicts stay #82; source-free
installed/public/Conda/platform qualification remains #23/#10 and exact final-head
CI/recovery #9. These source controls are not biological/performance acceptance.
No local background job is needed after this closeout.

## Composition acceptance: cached provenance correction in progress — 2026-11-03

#36 review reproduced participant reuse with a geometry/source map disagreement
and an unchecked optional site chemical state. The scoped correction validates
declared geometry pairs and site state before reuse; eight new counterexamples
fail before the fix and all nine new controls pass afterward. The positive control
preserves reordered geometry with a nonidentity source map. Generic keep and all
scientific geometry/weight/essential definitions remain unchanged. No molecular
operation or provider implementation is added.

Next qualify the complete composition/coupled source selection, existing driver
with tracking off/on and three cookbook blocks against a clean committed producer.
Preserve prior baseline/source identities; the 1,020-case run below belongs to
96f917a and does not execute this new correction. After #36 acceptance, continue
with #37 complete CCD workflows. #41 review by 2026-11-11, #60 receiving, #66's four
original methods and hosted/installed/public gates keep their separate scopes.

Artifacts are in `/tmp/phmt36-acceptance-20261103-1lir6w0a/`, owners LMMV/dprada,
review 2026-11-17. The existing owned #69 venv is reused; refresh only the ordinary
editable PHMT install after this candidate is committed. Controlled provider/native
installs, canonical prefix and sibling worktrees stay unchanged. Final-head CI #9
and shared conflicts #82 remain separate from local functional acceptance.

## Rigid-refinement source/API acceptance complete; interaction workflow next — 2026-11-03

#29 is resolved with its [archived report](archive/public_rigid_refinement.md)
and [current receipt](evidence/rigid_refinement_acceptance_20261103_summary.json). Clean producer
**96f917a7287fdd69e2a8b1a7c6600f975a745e6a** passes **1020 complete local
source tests**, zero failures/errors/skips, after 165 owning controls pass.
All five cookbook blocks and six original comparisons pass with identical
scientific reports with tracking off/on and actual policy attribution. No runtime
or test change is needed. Physical loaded-module/source/native/helper/test/input identities and actual module versions are equal in every phase. Full-run distribution-metadata lookups instead switch to older canonical PHMT, MolSysMT, Viewer and DepDigest records. Strict full equality remains false for that run; focused, cookbook and comparison full equality remain true. The original differences are retained separately, without claiming clean dependency closure.
Both final/each_step remain available; reciprocal counterexamples and valid
checkpoint retention are protected. Old performance archives remain unchanged.

**Next product segment: #36, then #37.** Accept public common-frame composition
and named native interaction collections first, then replay the complete EST/DES
CCD joint-interaction workflow with the same controlled providers. Review source
axes/frame/state, participant reuse versus explicit keep, incompatible constraints,
evaluated-empty/failed analyses, steric/directional negatives, persistence and actual
credits. Reuse the complete source result while its runtime/test/input/provider
identities remain applicable; run the owning drivers/examples for fresh full
workflow evidence. See the ordered [roadmap](roadmap.md). Adjacent #30/#32/#33/#34
acceptance can be reconciled as their independent contracts are reviewed, not
closed automatically from an aggregate count.

**Parallel boundaries:** #41's historical-public donor arithmetic exception needs
review by 2026-11-11; current source already uses public MolSysMT generic vectors.
Public capability delivery/receiving is separate from ideal acceptor geometry.
MolSysMT #121 is CLOSED and its copy decision is an ancestor of controlled 0faf1584;
[#60's status correction](https://github.com/uibcdf/pharmacophoremt/issues/60#issuecomment-6613270157)
replaces provider-implementation waiting with scoped consumer receiving when an
independent molecular variant is needed. Intentional live model links stay explicit.
#66 still needs the four original binding methods via a new authorized access lead.
#323 environmental H, #375 directions/delivery and #447 identity/scaffold retain
their distinct provider scopes. No local molecular kernel or study-rule change.
Addon and new release remain deferred; #9 hosted CI and #23/#10 installed/public
delivery remain independently owned.

Artifacts stay in `/tmp/phmt29-acceptance-20261103-o7s59ui_/`, owners LMMV/dprada,
review 2026-11-17. The owned #69 venv/providers/native bytes are reused unchanged;
ordinary editable PHMT still identifies runtime `0.4.0+52.g404aa38`, with tracked
runtime/support/test/tool/workflow trees equal to measured 96f917a. No canonical
prefix or sibling worktree is modified. Shared dependency conflicts remain #82.
The isolated strict cookbook-page render uses a neighboring link-target stub.
The local suite and analytical receipts do not establish clean installed/public/
Conda/platform or biological/performance qualification. Prior-head 96f917a CI
41699308864 has all eight scientific jobs queued at the retained receptor query;
that is not green evidence. Final-head receiving/recovery stays #9. No local
background job is required to resume #36 after this closeout.

## Prepared-conformer source/API acceptance complete; rigid refinement next — 2026-11-03

#17 is resolved with its [archived report](archive/native_conformer_screening.md)
and [current acceptance receipt](evidence/conformer_acceptance_20261103_summary.json).
Clean source **3ecfe23cbab455226ab48c99248f7c9c127b6d8c** passes **95 controls**,
zero failures/errors/skips: all 20 prepared-conformer cases plus rigid, seeded,
facade, retrospective and composed-attribution consumers. The workflow example
and five current cookbook blocks pass. No runtime or test change is required.

Five full analytical ensembles retain complete negatives, unresolved/entirely
failed ensembles, a unit-coverage maximum with another frame failed, and a binary
hit at .75 optional coverage with an actual missing state on another frame.
Every failure stays explicit. The retrospective record preserves repeated input
IDs and excludes the unresolved input: original scored indices [0, 1, 3], three
evaluated inputs, one failed input. Actual references/uses and unchanged source
atom/coordinate/chemical-state/frame-association fingerprints are retained.
Full source/native/helper/test and metadata lookup identities are stable across
all three phases. A strict isolated cookbook-page render passes with an adjacent
link-target stub; this does not qualify the full documentation site.

**Next:** functional/API acceptance of [#29](https://github.com/uibcdf/pharmacophoremt/issues/29).
Review the public supplied-correspondence evaluator/refiner, both `final` and
`each_step` orientation policies, rejected-trial rollback, retained best accepted
states, resource/provider failures, immutable sources and actual attribution.
Execute its existing analytical/workload guards and cookbook before archival.
Preserve measured cases favoring either policy; do not infer a universal winner
or require a new timing benchmark to accept scientific behavior. Molecular
recognition, fitting and transformation remain in MolSysMT; missing capabilities
go through provider issues. #66 still awaits the four original binding methods;
no new search lead or study change has arrived. Addon/new release stay deferred.

Artifacts remain in `/tmp/phmt17-acceptance-20261103-pqipkabu/`, owners LMMV/dprada,
review 2026-11-17. The unchanged owned #69 venv still imports ordinary editable
PHMT `0.4.0+52.g404aa38`; measured main 3ecfe23 has identical tracked runtime,
support, test, tool and workflow trees. Actual providers/native bytes, sibling
worktrees and canonical prefix are unchanged. Explicit checkout helper routing
is retained in the original runner. Shared pip-check conflicts stay #82.
This is bounded source/API qualification, not full current-suite or clean
installed/public/Conda/platform/biological/performance qualification. Prior-head
3ecfe23 policy and Conda governance pass; its scientific CI 41696393621 is still
pending at the receipt. Exact final-head receiving and recovery stay #9, separately
from #23/#10 delivery. No local background job is needed to resume #29.

## Curation source/API acceptance complete; prepared-conformer review next — 2026-11-03

#38 is resolved with its [archived report](archive/public_pharmacophore_curation.md)
and [current acceptance receipt](evidence/curation_acceptance_20261103_summary.json).
Clean code producer **404aa3829ac8d43bd6cb3c883f5547eb460857b0** passes **84**
owning curation/contracts/model/site/pose controls, zero failures/errors/skips.
The eleven new controls protect atomic rejection of partial in-place shared-site
edits and valid independent/all-occurrence alternatives; nine fail before the fix.
All three existing cookbook blocks reproduce seven expected evaluation outcomes,
native persistence, source mappings and actual attribution. Full code/native/test/
helper and metadata identities are stable in both phases. Original October and
pre-fix evidence is retained. The isolated page render passes after supplying a
stub for its adjacent attribution link; full-site rendering is not inferred.

**Next:** review acceptance of [#17](https://github.com/uibcdf/pharmacophoremt/issues/17)
against the current public prepared-frame/state, score-resolution and failure
contracts. Inspect implementation, execute its existing real-provider guards and
cookbook, and resolve concrete gaps before archival. Then review #29's supplied
correspondence refinement and alternative orientation policies. No conformer
generation or molecular repair belongs here; any missing reusable molecular
capability goes to MolSysMT through an issue. #66 still needs a new authorized
route to the four original binding methods; do not repeat exhausted searches or
change its study rules. #60, #323/#375/#447, addon and release priorities remain
separate; addon/new release stay deferred.

The owned work root `/tmp/phmt38-acceptance-20261103-q_sscz2e/` retains execution
artifacts, owners LMMV/dprada, review 2026-11-17. The #69 venv now contains an
ordinary editable PHMT install at measured version `0.4.0+52.g404aa38`, replacing
the previously measured local wheel; that original wheel/artifact receipt is
unchanged. Actual provider roots/pins/native bytes and the shared canonical prefix
are unchanged. Helper imports explicitly add the source checkout after resolving
PHMT through its editable install. Shared pip-check conflicts remain #82; these
84 passes and recipes do not qualify clean installed/public dependency closure,
the complete current suite/platform matrix or biological performance. Exact
final-head CI remains #9. No local background job is required to resume #17.

## Cached-model curation acceptance in progress — 2026-11-03

The next independent MVP segment is functional/API acceptance of #38 while
#66 awaits the four original binding methods. Review reproduced a partial
in-place edit changing an unselected index when two indices share a native site.
The scoped correction rejects that ambiguous selection atomically; independent
edits and selection of all shared occurrences remain valid. Nine new regression
cases fail before the correction, and all eleven new controls pass afterward.
No molecular implementation, provider source or #60 molecular-copy policy changes.

Next qualify the complete curation/owning integration selection and the existing
three-block cookbook against this committed producer, then archive #38 only if
its acceptance conditions hold. Follow with separate acceptance review of #17
prepared-conformer screening and #29 rigid refinement; addon/release stay deferred.
The current work root is `/tmp/phmt38-acceptance-20261103-q_sscz2e/`, owners
LMMV/dprada, review 2026-11-17. Its receipts preserve the original alias
reproduction and pre/post regression outputs. The previously owned #69 venv
now installs this checkout editably with ordinary pip build isolation; its prior
7e5b5a5 installed-wheel receipt/artifact remains historical. Provider/native
installs and the canonical shared prefix are unchanged. Final-head CI stays #9.

## Original-paper access handoff ready; last unreviewed support checked — 2026-11-03

#66's [clickable access handoff](https://github.com/uibcdf/pharmacophoremt/issues/66#issuecomment-6611742289)
lists Sun 2006, Xin 2023, Güngör 2006 and Scott 2023 with full titles, direct DOI
links and required biological binding-method sections. The maintainer currently
has no new route and will check ordinary authorized access. No human scientific
validation is needed before source review; the original experimental text is missing.

The explicitly unreviewed official Güngör supporting document provided one
bounded new route. Its identity is verified and all nine pages visually/textually
reviewed: chemical/analytical characterization, including LC/MS instrumental
conditions, supplies no receptor-binding protocol. This finding is limited to
that supplement, not the unretrieved main article. The
[new manual receipt](evidence/esr1_gungor_support_review_20261103_summary.json)
retains factual review and exposure; prior records remain unchanged. Raw source
PDF/text/renderings stay private in `/tmp/phmt66-gungor-support-20261103-crebhpm_/`,
owners LMMV/dprada, review 2026-11-17.

**Next input:** original main binding methods through a new authorized access
lead for those four papers. The article searches and this support route are
exhausted; do not repeat them without a new lead, request individual activity
tables, change study rules or score an unqualified cohort. Newly observed
chemical/analytical source content remains exposed development evidence; no
aliases, class counts, computational molecular systems or scores are created.
#66 stays partial. #9 owns the separate new-main CI; #69 source adoption remains
resolved, and installed/public delivery, addon and new-release priorities are unchanged.

This documentation/data-only followup uses one bounded `[skip ci]` checkpoint
while unskipped integrated-source CI **41688951342** at **0485c17** remains active.
No runtime, helper, test implementation, workflow or dependency input changes;
the only new test-tree input is the manual factual/exposure projection. Local
method/report guards, archive/projection identity, indexes, Ruff and whitespace
cover the changed scope. #9 retains final-head/daily-backlog recovery; that older
head's eventual result is not relabeled as execution of this documentation head.

## Chemical-domain source adoption complete — 2026-11-03

The reviewed chemical-domain adaptation is integrated through code merge
**76f43ffa6663f4a3c85ef27c27d212d773d55442**, preserving the later main checkpoints.
Its six tracked runtime/support/test/tool/workflow trees are identical to measured
candidate **7e5b5a5a3ee9c60528864928e56d1abac8aeaf9d**. Provider **0faf1584**,
Viewer **ca7ebea6** and DepDigest **13cc7378** are now the controlled source inputs.
No molecular implementation, scientific profile, fixture or public minimum changes.

[Hosted adoption receipt](evidence/chemical_domain_hosted_adoption_20261103.json)
verifies all **eight actual Linux/macOS Python 3.11–3.14 scientific test steps**.
The first attempt's seven passes and macOS 3.14 runner-capacity cancellation remain
original evidence. Attempt 2 recovers that cell successfully; inherited successful
jobs are not described as newly executed tests. The unused backlog-decision skip
remains visible. The redundant old-runtime documentation matrix was deliberately
cancelled to free capacity and is not called passing.

The [local receiving receipt](evidence/chemical_domain_fixed_provider_receiving_20261103_summary.json)
retains 1,009 complete local source passes, all original 22 controls/four typed
CCD cases, and the separate 110-case installed local-wheel pass. Full metadata
lookup equality remains false after pytest while physical source/native/test
bytes remain equal; shared conflicts stay MolSysSuite #82. These exact source and
bounded wheel results do not qualify public dependency closure, the complete
installed Conda/platform matrix or a new release/minimum.

#69's source receiving is resolved and its report is
[archived](archive/receive_chemical_domain_separation.md), guarded by
`tests/test_chemical_domain_receiving.py`. The guard exercises absent/zero/unknown
versus known-empty chemistry, ambiguous/explicit states, extraction/copy/H5MSM
and state-local components versus stable molecules. The four unchanged CCD typed
preservation controls independently protect the provider correction. Ordinary
post-integration exact-head CI remains #9; inspect it separately, without relabeling
candidate CI as a new main run. The unskipped integration supersedes the prior
bounded documentation-only skip; daily recovery and weekly full matrices remain.

**Next:** return to MVP scientific validation under #66. Its four original binding
protocols still need a new authorized access lead; do not repeat the exhausted
public searches or acquire activities/scores before eligibility is established.
#23/#10 own future exact installed/public delivery; #323/#375/#447 retain their
separate scopes. Addon and a new release remain deferred. No human validation
is outstanding for this source adoption.

Retain `/tmp/phmt69-integration-20261103-dh5mbdjd/` and the earlier source/wheel
roots through review on 2026-11-17, owners LMMV/dprada. Original producer failures,
versions, source/native hashes and artifacts remain unchanged. The earlier venv
contains the local installed wheel; source replay requires selecting/reinstalling
the identified source. No sibling source or shared prefix is modified.

## Provider defect received; local source and installed receiving pass — 2026-11-03

MolSysMT #531 is closed and its correction is received on exact provider
**0faf1584d05ac47ddcebfc20d9c9978b7f4f230e**. The reviewed consumer is clean
**7e5b5a5a3ee9c60528864928e56d1abac8aeaf9d**, published on
`receiving/chemical-domain-fixed-20261103`. Viewer ca7ebea6 and DepDigest 13cc7378
remain the compatible source inputs. Main still retains its prior runtime/pins;
the candidate is isolated until its required source matrix is checked.

The [new receipt](evidence/chemical_domain_fixed_provider_receiving_20261103_summary.json)
records **1,009 passed / zero failures, errors or skips** in the complete local
`tests` selection (1,455.25 seconds). Every original 22-node baseline and all four
unchanged EST/DES typed-preservation controls pass. A preceding four-case replay
passes independently. The earlier de7ffad failures and corrective measurements
below remain historical; no assertion, fixture, feature/profile or scoring
definition is weakened. Molecular implementation stays in MolSysMT.

A separate **110-case installed-wheel selection passes**, zero skips, outside
the source checkout. It covers the complete CCD, chemical-domain, cached-receptor
and ERalpha-template modules. Wheel SHA-256 is
`4bbec721da449c3c9195296895cc2ef09d5f7e526639cfc8e1b97e9b3a4b8155`.
Every wheel member except pip-rewritten RECORD matches installed bytes before
and after; loaded runtime roots stay inside the owned prefix and outside source.
The immutable SDK stages and retires the unshipped support namespace/data.
This is bounded PHMT-wheel receiving against editable source providers, not a
full installed Conda/public/platform gate or a published package.

Source/native/test bytes remain stable. Full-run distribution-metadata lookups
again differ after pytest; full equality remains false, while physical identity
equality is true. Python 3.14.7/Pandas 2.3.3/RDKit 2026.3.1 and shared pip-check
conflicts retain the disclosed #82 boundary. Fresh Rust is built with debug
symbols/incremental output disabled after an owned quota failure; its actual
hash and initial failure are retained. All 67 administrative controls pass on
retry after only owned Cargo products/cache are retired. No sibling worktree or
shared prefix is modified.

**Current gate:** [exact candidate CI 41674239397](https://github.com/uibcdf/pharmacophoremt/actions/runs/41674239397),
attempt 1 at 7e5b5a5, is still pending. At this receipt, governance and Linux
Python 3.13/3.14 pass; Linux 3.11/3.12 and macOS 3.11/3.12/3.13 are active,
macOS 3.14 is queued. The skipped backlog-decision job is retained. Previous
main 23c0648 passes all eight scientific cells on its **older** source pins;
that does not qualify the new pair. #531 is no longer the blocker. #69 stays
partial and #9 owns remaining hosted receiving.

**Later native capacity update:** macOS 3.14 job **126050438777** is cancelled
without executing steps. [Native job/annotation receipt](evidence/chemical_domain_ci_capacity_20261103.json)
records that no hosted runner acquired the job despite multiple attempts, with
explicit macOS ARM64 capacity notices. Linux 3.11 has meanwhile passed; this is
not a scientific failure or a complete matrix pass. An individual rerun attempt
returns `job 126050438777 cannot be rerun` while the workflow remains active.
After the current attempt settles, retry the unexecuted cell through the supported
rerun route, retaining earlier successful jobs and checking actual retry steps.

**Resume:** recover that cell and inspect all eight actual `Run tests` steps in 41674239397 at exact
7e5b5a5; diagnose failures if any. Once green, integrate the published candidate
directly into main, preserving current checkpoint/evidence, update this report's
guard to the candidate domain module and inspect the resulting main CI. Keep
installed/public dependency delivery under #23/#10 separate; no new public
minimum, package, tag or release is implied. No human scientific validation is
pending for this receiving step. #66/#323/#375 and addon priorities are unchanged.

Retain `/tmp/phmt69-fixed-20261103-q6cirii4/`, owners LMMV/dprada, review
2026-11-17. Its venv now contains the local **installed wheel**, not the original
editable PHMT; reinstall/select exact candidate source before replaying source
tests. The clean `wheel-source` clone preserves 7e5b5a5. The archived installed
runner binds support to a checkout at that commit. Both local scientific
processes have completed; only the remote matrix remains active.

The capacity-note followup is documentation/evidence only and uses one bounded
`[skip ci]` checkpoint to avoid adding another eight-cell queue during this
observed runner shortage. Main's unskipped 53c1541 CI **41679560745** remains
active on its unchanged old runtime/pins. #9 retains recovery/daily-backlog
ownership; candidate integration must finish on an unskipped main head. Local
report/index/whitespace checks cover this note; no scientific evidence is relabeled.

## Owner receiving candidate reviewed; four typed-column checks pending — 2026-11-02

MolSysMT #255 is implemented and closed: the provider has announced main merge
**00abb958fb93649131d5ce5fe5e12e90cf4900e9**, with runtime/test trees identical
to the executed de7ffad checkpoint. That equivalence is provider-reported, not
a fresh local run on the merge commit. The remaining provider defect is
[MolSysMT #531](https://github.com/uibcdf/molsysmt/issues/531); #69 no longer
waits for the migration implementation. The owner's reviewed candidate is
**43a258c516ebb3c8f971ac45629a1a60b3871fab**, branch
`receiving/chemical-domain-owner-20261102`. Main retains its previous runtime,
pins and scientific assertions while the candidate has a known provider gap.
See [the contract](chemical_domain_receiving.md) and
[full original receiving receipt](evidence/chemical_domain_receiving_20261102_summary.json).

The candidate adopts MolSysMT **de7ffad2aef18ff3bccd184133dc69e081cb506e**, Viewer
**ca7ebea6** and DepDigest **13cc7378** in controlled source routes, the public
chemical_states SMARTS tool and actual helper/route hashes. It corrects the
prepared-workflow and cached-receptor negative spies and the source-drift tests'
stale pin literal. The strict template guard uses canonical `unspecified` for
undeclared stereo, keeping every assigned R/S value exact. No fixture/population,
feature/profile, query, geometry criterion or scoring definition is changed.

The original full source run reports **998 passed / 11 failed / zero skipped**;
JUnit includes additional unittest-subtest records. All original 22 baseline
nodes pass. Corrective runs pass the complete receptor module (66), strict stereo
guard (1) and six new real state/absence/component/extraction/copy/persistence
controls. A separate [clean-candidate confirmation](evidence/chemical_domain_candidate_confirmation_20261102_summary.json)
passes **73 controls, zero skips**, at exact 43a258c. This is a focused confirmation,
not a claim that the four outstanding full-suite failures passed.

**Provider gap:** complete EST/DES merge/extraction fails four exact typed-state
preservation checks. The isolated public `CC.CC` repro changes component_name/type
descriptors from `string` to `object`; the inspected values and atom identities
are preserved. [MolSysMT #531](https://github.com/uibcdf/molsysmt/issues/531)
continues the [original #255 handoff](https://github.com/uibcdf/molsysmt/issues/255#issuecomment-6596125577)
and asks for the intended typed contract or correction. Keep the four assertions;
do not normalize these chemical payloads locally, xfail them or integrate a red
controlled-source pair into main. #69 remains partial. Draft #70's earlier green
22-case claim is bounded, and its earlier hosted failure is preserved separately.

Source receiving uses Python 3.14.7, Pandas 2.3.3 and RDKit 2026.3.1 in an owned
system-site venv, with exact editable provider installs and a newly built Rust
extension. Actual module/Python/native/test bytes remain stable in the full run;
distribution-metadata lookups differ after pytest and are explicitly retained.
The strict runner flag remains false for that metadata distinction. This is not
clean installed/public/platform qualification. Shared dependency conflicts remain
MolSysSuite #82; canonical 67 administrative controls and declared-only route
audit pass. Only owned Cargo build/cache directories were retired after quota
exhaustion; native binary/source/logs remain. No sibling source is modified.

**Next:** receive provider dtype disposition/correction, update the isolated
candidate and rerun the four failed controls plus applicable unchanged guards.
Then complete source CI and separately installed/public qualification before
main integration or any new minimum/release claim. Keep the owned root
`/tmp/phmt69-receiving-20261102-t6z6qujh/` for review on 2026-11-16, owners
LMMV/dprada. Its editable PHMT link follows this checkout: select the identified
candidate source before resuming tests in that venv. #66 original methods,
#323 refinement and #375 geometry retain their separate limits. Addon and a new
release remain deferred; public 0.4.0 is unchanged.

## Chemical-domain receiving prepared; current baselines pass — 2026-10-29

New [#69 receiving contract](chemical_domain_receiving.md) prepares the
maintainer-approved pre-1.0 MolSysMT #255 separation, coordinated by MolSysSuite
#155. The provider plan at 4e9bf09 records target ownership/API contracts with
runtime implementation not started. Keep client code and dependency pins as
they are until an identified implementation is ready for receiving.

The bounded 288-file AST inventory finds one direct graph call to migrate:
`phmt_test_support/diagnose_eralpha_interface.py:172`, currently
`msm.topology.get_substructure_matches`. Target: the delivered
`msm.chemical_states.get_substructure_matches`, preserving SMARTS/profile, atom
scope and explicit intended state/frame. No direct Topology chemical facade or
literal Topology conversion target is found in this scan. Native feature/state
selection, preparation, copies and persisted interaction/history evidence still
need indirect receiving; a namespace-only edit is insufficient.

The [source baseline receipt](evidence/chemical_domain_readiness_20261029_summary.json)
records **22 passed, zero failures/errors/skips** on clean consumer **87de52f**
and clean editable MolSysMT **71fbe4f46d3c70e4e973c8025f01752a8c9b1084**.
Consumer/provider Python, native and test identities are stable before/after.
The provider is preserved three commits behind fetched 4e9bf09; its tracked
package tree is identical at inspection. The target lowercase `chemical_states`
module is absent. Five existing b_factor-drop warnings and shared pip-check
conflicts remain disclosed. This is current-behavior source evidence, not target
cutover or clean installed/public qualification. No sibling or environment is
changed, and no molecular operation is implemented here.

The [native hosted receipt](evidence/ci_methods_receiving_20261029.json) now
confirms all **eight actual Linux/macOS Python 3.11–3.14 Run tests cells** in
original push CI **40764900309** for exact source 87de52f. Its provider pin is
8ae160fc, separate from the editable 71fbe4f baseline. The skipped recovery job
is retained as a non-scientific job. Prior queued observations remain historical;
this new result does not qualify a future head or the chemical-domain cutover.

**Next:** receive MolSysMT #255's identified implementation and migration map;
check state/absence/component/axis/copy/persistence contracts, migrate the one
graph caller and rerun the unchanged scientific guards. Separately qualify
required source CI and exact installed/public artifacts before changing supported
minimums. #69 stays partial. #255 precedes provider #447 identity/scaffolds;
#323 refinement and #375 geometry remain distinct. #66 still needs the four
original protocols or a separately justified design; no repeated source searches,
activities or scores are acquired in this readiness step. Addon/new release
remain deferred; public 0.4.0 is unchanged. Final-head receiving stays #9.

Keep `/tmp/phmt69-readiness-20261029-pee7tccd/`, owners LMMV/dprada, review
2026-11-12. Original plan, source inventory, verified public reporting wheel,
runner and complete outputs are retained. The current baseline is measured;
new target contracts are intentionally unqualified until delivered.

Local closeout passes 67 administrative controls, three reporting tests, generated
indexes, evidence/source-identity checks, whole-tree Ruff lint/format and whitespace.
The reporting catalog now includes #69; its initial missing-entry failure and
corrected result remain in the owned raw root. That administrative registration
does not change the scientific guards or the recorded clean 87de52f producer.

## Original-method follow-up complete; full articles still needed — 2026-10-28

#66's [Scott supplement follow-up and four-article handoff](esr1_binding_pool3_methods.md#scott-supplement-and-access-follow-up--2026-10-28)
visually reviews S53/S55 and reads S54/S65 from the unchanged official supplement.
S53 supplies binding/degradation results and errors, not the complete binding
protocol. S55's L536S belongs to crystallography and is not transferred to the
binding receptor. Four original journal binding methods remain unresolved;
no source is accepted for detailed activity acquisition. Forty table positions
do not establish forty independent groups or the required class balance.

Newly observed development evidence includes Scott labels 2–41's activity values
and chemical strings, plus unsolicited search snippets including literal
BDBM50180465. The [portable exposure projection](../tests/data/esr1_binding_evaluation/pool3_methods_followup_20261028.json)
and [separate manual-review receipt](evidence/esr1_binding_methods_followup_20261028_summary.json)
retain that exposure without molecular alias mapping. No direct activity-resource
request, molecular-system construction, class count, pharmacophore query change
or score is performed. Original ledgers/results and the fixed study rules remain.

Three search batches/twelve queries and five web-tool open attempts yield no
original main methods; four opens report 403, one tool-level inaccessibility.
Search snippets/support descriptions are not retrieved full methods. Earlier
batches are manual summarized observations; only the final tool response is
saved in full. Review starts at clean 0fbba04 and remains manual source analysis,
not a clean automated molecular validation claim. Keep original private source
root and `/tmp/phmt66-methods-followup-20261028-eg5fjg0r/`, owners LMMV/dprada,
review 2026-11-11. No environment or provider implementation changes.

**Next:** obtain the four listed original protocols through ordinary authorized
institutional/author/publisher access; do not repeat the same searches without
a new access lead. Review experimental suitability before a new finite activity
declaration. A different study design requires separate justification/declaration;
keep all existing exposure history. No scientific-method approval is outstanding,
but original source text is needed to resolve these methods.

**MolSysMT waiting points:** #375 public generic-vector delivery/version and
later source/installed/public migration, with a separate acceptor-direction
contract; #447 reusable molecular identity/scaffold overlap for a future eligible
cohort; #323 environmental fixed-state H refinement. These do not solve original
article access. #41's implementation and historical exception below remain
unchanged. Hosted receiving stays #9. Addon and a new release remain deferred;
public 0.4.0 is unchanged.

Local closeout passes all 67 administrative unittest controls, three reporting
tests, generated indexes, archive/projection/prior-declaration identities,
whole-tree Ruff lint/format and whitespace checks. No runtime implementation or
documentation-site input changes; no fresh molecular matrix, installed-package
or biological qualification is inferred. Final-head hosted receiving remains #9.

## Provider feature receiving implemented; historical minimum retained — 2026-10-28

#41 now receives public `interactions.hbonds.get_hbond_sites` and delegates
nonempty donor-H directions to `structure.get_vectors` when available. Actual
routes and detached vector provenance are retained. Available-provider failures
propagate, coincident D/H remains invalid, and acceptors stay position-only under
unchanged `classical_atomic_formal@1`. No sibling code, dependency minimum or CI
provider pin changes. See [the contract](molsysmt_feature_receiving.md) and
[complete receipt](evidence/molsysmt_feature_receiving_20261028_summary.json).

Source MolSysMT **3781031d0c1d08f34b2aa966ad0b82bf3b64a31d** passes all 160
selected scientific tests across the integration and ERalpha-diagnostic runs,
with zero skips. Earlier missing-namespace failures and two stale test probes
remain in the evidence; the corrected checks preserve their scientific assertions.
All 67 administrative controls pass after refreshing the changed test-support
file's declared digest. Shared dependency conflicts remain MolSysSuite #82,
so these are bounded source results, not a clean installed-package qualification.

The original public MolSysMT 0.23.0 payload initially passes nine compatibility
controls in a separate process with shared transitive dependencies. An ordinary fresh public
environment fails before testing because of host disk quota exhaustion. Preserve
both outcomes without promoting the payload import into normal installation
evidence. Public 0.23.0 and the existing CI provider pin lack vectors; #41 remains
**partial/open**, retaining only their existing donor arithmetic with an explicit
legacy label. Exception owner LMMV/dprada, review **2026-11-11**, removal after
qualified public-vector delivery and source/installed/public receiving permit
migration. #375's broader direction contract and #323/#447 remain distinct.

**Next:** verify exact-head hosted receiving (#9), then qualify the provider
delivery chosen by its owners through clean source/installed/public routes and
retire the exception when possible. The newer fetched provider main 1f0bef2 is
preserved, 32 commits ahead of the actual tested sibling; it is not qualified by
these runs. #66 still needs four original journal binding protocols or a separately
justified study design; no further detailed activities, molecular inputs or scores
were acquired here. No human scientific-method approval is outstanding. Addon,
broader algorithms and a new release remain deferred; public 0.4.0 is unchanged.
Keep `/tmp/phmt41-receiving-20261028-89triy8l/` for receiving/evidence review,
owners LMMV/dprada, review 2026-11-11. Failed task-owned environment/cache paths
were retired with a receipt; no shared environment or cache was changed.

**Committed-source confirmation:** consumer **f815d4de2a95cd869a6f90c60f0fb17b946dd996**
passes 27 modern-provider controls and 11 old-public-payload controls, zero skips,
with clean consumer/provider worktrees and identical Python/native/test identities
before and after. The [new receipt](evidence/molsysmt_feature_receiving_clean_20261028_summary.json)
is separate from the preserved exploratory archive. Implementation-head policy
40759846827 and Conda governance 40759846929 pass; scientific CI 40759846097 is
queued at observation. This closeout head's receiving remains #9 independently.

## Methods review: no accepted source; four original protocols unresolved — 2026-10-28

The [six-source methods review](esr1_binding_pool3_methods.md) and
[manual-review receipt](evidence/esr1_binding_pool3_methods_20261028_summary.json)
retain every candidate. The first patent reports only 23 α-table positions
(including repeated controls), insufficient for forty independent groups despite
69 database records. Method 16 in the other patent uses CHO cytosol and leaves
the binding receptor's species/isoform/construct unresolved; a human-receptor
sentence in a different method is not transferred to it. The four journal
candidates still need their original full binding methods. The open Scott
supplement and two successful metadata-only publisher XML responses do not close
that gate. No source is accepted for detailed activity acquisition.

**Document/search activity information is now observed.** The new ledger retains
the seen patent tables/names/CAS and abstract/search snippets, including literal
CID 10399473 outside the original 8,099 CID ledger. CID 5870 is already historical;
SID 46517467 is also retained. No chemical aliases are inferred. Future declarations
and post-tuning independence audits must preserve this exposure. Earlier ledgers
and queries/rules are unchanged. No activity-resource table, computational
molecular system, class-count calculation or new pharmacophore score is acquired.

Source acquisition starts in clean declaration context
`70c340cbe5c60c6ec7867e7709c8fc5ddbf3b5f2`; the manual review retains its later
untracked-metadata overlay. It is not an automated clean-source scientific run.
Raw review SHA-256:
`22bcc8e394bc4f95a312aaa9d03bd6a4eec89988c44a9b22499f7ae094f0cc1e`.
Twelve ChEMBL responses are portable. The 35 manual HTTP attempts and private
documents/errors remain identified separately from web observations. Keep
`/tmp/phmt66-methods-20261028-f1n4twnm/` for qualification/source review, owners
LMMV/dprada, review 2026-11-11. No environment or sibling is changed.

**Next:** obtain the four original journal protocols or declare a separately
justified study design; do not download individual activities under unresolved
source gates. Independent #41 provider-API receiving is available while source
access is pending. MolSysMT still owns geometry, identity/scaffold and preparation;
source access and reported panel size are not MolSysMT implementation blockers.
No human scientific-method approval is outstanding. Hosted receiving remains #9;
public 0.4.0, addon deferral and the two earlier terminal pools are unchanged.
Final local gates pass 67 administrative unittest controls, three reporting tests,
generated indexes, whole-tree Ruff lint/format and whitespace checks. Prior
capacity closeout c42d91e now passes all eight actual test cells in CI 40738760689;
the [native observation](evidence/ci_pool3_receiving_20261028.json) keeps that
identity separate. Methods declaration 70c340c policy 40750615075 and Conda
governance 40750614288 pass, while CI 40750612798 is in progress at observation.
New-head and installed/public receiving remain separate.

## Six-source methods review declared — 2026-10-28

The [methods declaration](esr1_binding_pool3_methods.md) fixes the six candidates
and their capacity-derived order before further original-document reading.
Next acquire official assay/document metadata and review original methods,
beginning with CHEMBL5725373 / CHEMBL5730671. No activity-resource, molecular
input or score is requested in this stage. Full documents may contain potency
tables/compound identities; retain potential and actually inspected exposure
instead of calling visible data unseen. Methods, not class balance, determine
experimental suitability. Another finite declaration is required before
detailed activities. Earlier census/results and all molecular-provider gates
remain unchanged.

## Complete capacity census: fifteen sources need experimental review — 2026-10-28

#66's [third source census](esr1_binding_pool3.md) completes every declared request:
475 ID-only capacity responses plus status, without acquisition failure. Fifteen
assays contain at least 40 raw records (largest 439); 460 fail that necessary
condition. No detailed values, compound information, molecular preparation or
scores are acquired. All fifteen remain pending experimental review; the largest
two are coactivator experiments as described, and several others have relative
or single-concentration wording. Capacity is not class balance or cohort readiness.

Clean acquisition and independent offline replay both identify producer
`751f7f4208186db401c6de373f826abf439ff695`; all fields except replay timestamp agree.
The [portable receipt](evidence/esr1_binding_pool3_20261028_summary.json) retains
original bytes and all pending survivors, raw SHA-256
`1797393a5b553e0149de4c77c77cf27b1d65e0651ff5782bccc018308ccac1e9`.
Both previous pools, query hashes, thresholds, no-pooling and all exposure history
remain unchanged. No provider implementation or public release changes.

**Next:** review original experimental documents for the six candidates without
an explicit metadata warning, starting with CHEMBL5725373 / CHEMBL5730671. Keep
the complete pending list/rejection evidence. Declare a finite detailed-source
pool and budget before individual activity requests; qualify class balance and
then MolSysMT #447 identity/scaffold/preparation gates before freezing a cohort
or scoring. #41/#375 receiving stays separate. No human approval is outstanding.

Keep the owned raw root `/tmp/phmt66-pool3-20261028-o60k3mue/` (LMMV/dprada,
review 2026-11-11). Shared environment conflicts are handed to MolSysSuite #82;
no environment mutation or clean-install claim. Producer CI 40734597561 remains
in progress at observation; policy 40734598454 and Conda governance 40734598539
succeed. Final-head receiving remains #9, separate from the earlier green sources.
Final local gates pass 64 administrative unittest controls, three reporting tests,
generated indexes, whole-tree Ruff lint/format and whitespace checks. The strict
full-Sphinx guard passed at declaration with unchanged documentation inputs.
No new full scientific/installed/public qualification is inferred.

## Resumed: complete remaining single-protein capacity nomination — 2026-10-28

Main receives the three published governance commits by fast-forward through
`9eb6787f11e32a927950d8c53e097949556d83e1`. The [new pool-3 declaration](esr1_binding_pool3.md)
nominates all **475 remaining single-protein assays** from the frozen metadata,
without pool 2's description filter. Acquire only status and ID-only capacity
responses after committing the declaration. No detailed activity values,
compound information, molecular inputs or scores are authorized by that run.
Every capacity must resolve before ranking; survivors remain pending experimental
review and a separate detailed-acquisition declaration. Existing thresholds,
queries, no-pooling and all previous exposure/results remain unchanged.

The [new native CI observation](evidence/ci_receiving_20261028.json) closes the
earlier pending observations: pool-2 closeout CI 40388775895 passes all eight
actual test cells, scheduled retry 40353440186 attempt 2 is successful, and
governance head 9eb6787 passes its eight actual cells in 40612031912 plus policy
40612032102 and Conda governance 40612032124. Later nightly 40711753014 executes
the decision/governance only and intentionally skips science; it is not another
matrix. Preserve the earlier failed attempt and dated pending records under #9.
These results do not qualify a future head or installed/public bytes.

**Next:** commit this declaration/support change, acquire the capacity census in
a new owned directory, retain every response/failure and qualify the offline
result before choosing experimental sources. Molecular identity/scaffolds remain
MolSysMT #447. Newer H-bond API receiving remains separate in #41/#375; addon,
new release and molecular-provider modifications remain deferred.

## Second binding-source pool stopped at capacity — 2026-10-26

The [second predeclared source pool](esr1_binding_pool2.md) nominates 42 assays
from retained metadata before new activity requests. All 42 ID-only capacity
responses complete under ChEMBL_37; the largest contains **26 raw records**.
None can supply the fixed twenty groups per class. No detailed activity values,
new compound information, molecular preparation or score is acquired. This
bounded metadata filter is not a conclusion about every binding source.

Acquisition `eef3fa82abcf3e22ca0c1974948fc577a3f1b42c` is clean and preserved,
including every response and request URL/time/hash in the case directory.
The offline reader's status-counter/list mismatch is fixed with an original-
response guard, without repeating requests. Corrected clean-replay evidence
is retained for producer `992df4e31131e2435821b73c5cf6901f6913e407` in the
[pool-2 summary](evidence/esr1_binding_pool2_20261026_summary.json), raw SHA-256
`f64b56923aa564d742bc4b16d457400c43c3412ead0b9c02284de807811cc9c5`.
The original acquisition remains eef3fa8, and all source files/old exposure
records are unchanged. Final local qualification passes 62 tests / 56 subtests,
including strict Sphinx and original-response/clean-replay guards, plus reporting,
index, Ruff and whitespace checks. New-head hosted/installed receiving remains
separate under #9. Keep the owned raw root
`/tmp/phmt66-pool2-20261026-4qpzxx/` for qualification, review 2026-11-09.

**Next:** broaden metadata nomination under a new dated declaration before
more activity queries. Retain both terminal pools and the original fixed
queries/thresholds/no-pooling rule; MolSysMT owns identity/scaffold/aliases and
preparation for a future eligible cohort. #66 stays partial.

CI receiving for 59c98d6 is now verified: original push 40150094066 succeeds
with governance and all eight actual Linux/macOS Python 3.11–3.14 test steps.
Policy 40150094121 and Conda governance 40150094315 succeed. A later scheduled
run 40353440186 attempt 1 fails before tests only in macOS/Python 3.13 because
ambermd repodata download times out; the other seven scientific jobs pass.
Native `rerun --failed` was requested without changing routes/pins/workflows;
the retry remains separately observed under #9, not automatically successful.
Its macOS/Python 3.13 environment now installs successfully and actual tests
are running at the later observation; completion is still pending.
Public 0.4.0 remains unchanged; no new package/release is produced.

## First fresh-binding source pool stopped — 2026-10-24

#66's two predeclared sources fail the fixed population floor. The
[source review](esr1_binding_source_review.md) checks original experimental
methods/α-column tables and complete official activity pages, acquired only
after protocol commit `acfbe85b812eb6bd32f9682ac2fd86824ebeaff9`.
CHEMBL3382763 has 15 IC50 source identifiers: **6 positive / 2 weak / 7 unresolved**.
CHEMBL3705057 has 10 Ki identifiers: **10 positive / 0 weak**. These precede any
old-ID exclusion or molecular grouping. Neither can supply 20 groups per class.

The unchanged first pool is terminally stopped. No new query, threshold, source
replacement, mixed endpoint, molecular preparation or pharmacophore score is
introduced. All rows, flags, null values and the 25 new ChEMBL identifiers are
retained. This result is independent of MolSysMT #447; that provider's future
identity/scaffold tools cannot create missing source classes.

**Next:** design a new dated source pool before inspecting further activities,
with larger, documented binding populations and measured weak comparators.
Retain the fixed-query/threshold protocol, earlier 8,099 CID and 149 unresolved-
row ledger, and all 25 newly exposed ChEMBL IDs. MolSysMT still owns later
identity/alias/scaffold and molecular preparation. #66 remains partial for a
suitable cohort. Clean producer `c744df9a6d050486bfeb96a55d4233ecfab5f649` has
a [measured terminal result](evidence/esr1_binding_source_qualification_20261024_summary.json),
raw SHA-256 `bca7028c5e8c661ecec151f514d9a2ba46d7a3a465bb0b33b38c3467ff7298f8`.
All original rows and the 25 source identifiers are retained; prior metadata
records and all #62/#64/#65 outputs remain unchanged. Final local qualification
passes 57 tests / 49 subtests, plus reporting/index/Ruff/whitespace checks.
Producer CI 40149799918, policy 40149800151 and Conda governance 40149800161
are queued at observation; final-head receiving remains #9. The older #65 CI
is still running, so no new complete source matrix is claimed here.
Raw article/patent/document sources remain in the owned
`/tmp/phmt66-source-qualification-20261024-ormfxb58/`; activity pages/GET receipt
are portable in the case directory. No environment is created/removed and the
public release stays 0.4.0.
The final gates include strict Sphinx and censor/quality/replicate/primary-table
controls. No public runtime module changes.

## Fresh binding evaluation protocol and source triage — 2026-10-24

[#66](pending_proposals/esr1_binding_evaluation_readiness.md) is the next local
scientific segment. The [pre-data protocol](esr1_binding_evaluation_plan.md)
keeps both #64 queries and native scoring fixed, declares endpoint/quality/
censored-label/duplicate policies and sampling/failure gates before acquiring
individual activities or molecular structures. No new cohort is frozen yet.

Metadata review covers PubChem AIDs 1223/625258/2051711 and all 1,485 records of
the current ChEMBL_37 human CHEMBL206/B/9 assay query (two pages). These flags do
not guarantee tracer displacement. The fixed next source pool is CHEMBL3382763,
then CHEMBL3705057, with original experimental/document review still required.
No source has yet qualified for a new chemically independent cohort.

The conservative exposure audit excludes all 8,099 valid CIDs in the previously
read full Tox21 table, containing all 4,402 Bath CIDs and all prior requested IDs,
including failures. Another 149 rows lack a CID and retain row indices/SIDs as
unresolved identities. This literal identifier ledger does not establish molecular
or series independence. MolSysMT #447 remains open; #219/#366/#375 remain provider
responsibilities. No local chemistry or molecular-I/O workaround is introduced.

Nine original metadata responses remain in the task-owned
`/tmp/phmt66-binding-metadata-20261024/`, with checksums/URLs in
`tests/data/esr1_binding_evaluation/source_inventory.json`. Keep them for source
qualification (owners LMMV/dprada, review 2026-11-07). Only factual projections,
checksums and the case-specific review are published; full raw metadata
redistribution remains separate. No environment has been created or removed.

The protocol/reader is committed at clean producer
`507ca37d8f21815bb29c0a34f8ccf3b020edbacf`. Its
[measured review](evidence/esr1_binding_metadata_review_20261024_summary.json)
retains metadata identities, complete pagination, every excluded CID and all 149
unresolved row indices/SIDs. Raw result SHA-256 is
`4c43930e138a4904f0950e4b547ef34202bde3dec225aed3db96065c5241ab43`.
It reports `metadata_review_only` / `not_ready`, with no cohort, new activities,
molecular inputs or scores. Aggregate-count wording is subsequently clarified
without changing the predeclared source order, thresholds or sampling rules.

**Immediate next:** qualify the CHEMBL3352633 and CHEMBL3638543 source documents,
then the two nominated activity schemas under these committed rules. Metadata-
only acquisition must precede individual activity curation; provider identity/
scaffold, exact cohort and preparation gates must pass before scoring. The
current reader has no activity/structure acquisition or molecular route.
The final complete local administrative run passes 52 tests / 26 subtests,
including strict Sphinx and both historical-source/clean-receipt guards; three
reporting tests, indexes, Ruff and whitespace checks pass. Declaration 507ca37
CI 40148673520 is queued, with policy 40148673714 / Conda 40148673624 successful;
final-head receiving remains separate. Source attribution/terms remain in the
[review notice](evidence/esr1_binding_metadata_review_20261024_NOTICE.md).
Older fc9f14b CI 40145759546 is now successful; #65 implementation e32c80e CI
40147016165 is in progress and closeout d2e82e8 CI 40147294367 is queued. Both
#65 policy and Conda controls succeed. Exact-head receiving remains #9; public
0.4.0 and its existing release notice remain unchanged.

## Native saved-result reporting complete — 2026-10-24

**#65's local API and real-consumer criteria are complete.** Implementation
`e32c80e0cbc9837e8badcda2b7c93f22d30f1ddc` is pushed to main. Public
`validation.summarize_screening_results` and `compare_screening_results` compose
existing score/metric tools, retain all original indices/classes/unscored causes
and recompute paired metrics on exactly the common scored subset. No molecular
operation moves into PHMT. The [API](../docs/api/saved_results.md),
[recipe](../docs/content/cookbook/retrospective_validation.md) and
[resolved owner report](archive/native_retrospective_result_summaries.md) document
the reusable contracts, ambiguous-input rejection and attribution separation.

A new clean-head consumer reads the immutable #64 archive and reproduces all
64/45/19 counts, original mappings, native scores, arm metrics, common AUC delta
and binary missing-score sensitivity. The
[derived summary](evidence/esr1_saved_summary_replay_20261024_summary.json) qualifies
the new result, raw SHA-256
`d8104d4019c908dfd01345158e7440880d2a26c3e356662248b5322196005da4`.
Original query/input/search outputs, producer and source attribution are retained
unchanged. New attribution records only the newly reached summary/scoring/metric
operations. The old case-specific ledger remains solely for historical replay;
new statistical consumers use the public tool.

Canonical Python 3.14.7 passes 84 selected scientific tests; the final complete
administrative run passes 50 tests plus 26 subtests, including strict Sphinx and
the new replay archive guard. Three reporting tests, indexes, Ruff and whitespace
checks pass. The replay
records current editable provider versions/origins separately from the original
scientific providers. No extra environment, molecular experiment, complete new
hosted/installed matrix or public package/release is claimed.

**Next:** inspect exact implementation/final-head CI through #9; implementation
CI 40147016165 is queued, policy 40147016265 / Conda governance 40147016227
succeed at this observation. Older fc9f14b CI 40145759546 remains in progress.
Keep public-delivery/installed receiving separate. Before stronger biological
claims, review endpoint and fresh data suitability and predeclare an unexposed
evaluation set; these 64 outcomes cannot be reused as unseen validation after
tuning. Receive molecular identity/scaffold/conformer/state tools through #41
and their provider issues, without local replacements. Addon, broader release
infrastructure and a new release remain deferred.

## Native saved-result summaries implemented; clean receipt pending — 2026-10-24

#65 now has public `validation.summarize_screening_results` and
`validation.compare_screening_results`, documented in the
[API](../docs/api/saved_results.md) and
[recipe](../docs/content/cookbook/retrospective_validation.md).
They compose the existing native score reader and metrics with explicit original
cohort, index mapping and upstream causes. Native evaluation failures retain
their own cause/evidence; unavailable inputs never become negatives. Repeated
source IDs remain distinct original samples. New metric attribution stays
separate from immutable source attribution. No molecular-provider code changes.

Local canonical Python 3.14.7: 84 saved-result/metric tests pass, including real
Ackredit and optional-provider controls; 49 administrative/documentation tests
plus 24 subtests pass, including strict Sphinx. Three reporting tests, generated
indexes, whole-tree Ruff and whitespace checks pass. A preliminary derived replay
of #64 reproduces all counts, scores, original mappings, metrics and missing-score
sensitivity. Permanent clean-producer receipt is still pending. No full source
matrix, installed/public package or new molecular experiment is claimed.

**Immediate next action:** commit this implementation, execute
`python -m phmt_test_support.replay_esr1_saved_results --output /new/path.json`
from that clean head, retain its new derived evidence separately, then finish
#65's owning report/issue. Historical #64 results/drivers remain unchanged.
Follow #9 for the implementation head's hosted receiving. No extra environment
has been created; public 0.4.0 and its MolSysSuite notice remain unchanged.

## Paired comparison complete; next native reporting segment — 2026-10-24

**#64 is complete as a bounded exploratory comparison.** Clean producer
`012544472e8eca27d1646a6e8065ee22872d4368` uses both committed queries and all
64 unchanged evaluation inputs, without new training, parameter changes or
replacement. 45 SDFs are available and all pass public MolSysMT preparation;
19 HTTP 404 responses remain unscored (4 active / 15 inactive). Both arms
score the same 45 prepared systems: 12 actives / 33 inactives, no search failures.

| Common-subset result | Reference | Consensus |
| --- | ---: | ---: |
| AUC | 0.4848484848 | 0.5530303030 |
| BEDROC, alpha 20 | 0.1757153729 | 0.4589315704 |
| Tie-aware EF10% | 0.8181818182 | 1.6829268293 |
| Active / inactive geometric hits | 0 / 1 | 2 / 2 |

Descriptive AUC difference is +0.0681818182 on those same 45 inputs. Missing-
binary-score hypothetical full-cohort AUC ranges are 0.3333–0.6146 and
0.3854–0.6667, not imputed observations or confidence intervals. The observed
difference is modest; 12 scored actives, ties, unavailable structures, supplied
single conformers/states, a cellular rather than direct-binding endpoint and
unqualified chemical-series independence prevent predictive acceptance. These
64 outcomes are now exposed development evidence for any further method tuning.

The [paired summary](evidence/esr1_paired_evaluation_20261024_summary.json)
qualifies full original output (raw SHA-256
`610b418d88707132d40b4ef5fd534a04498c1389f8b73c5e1ca1d4db39c1d1f9`),
preparation and both-arm journals, acquisition/execution logs and qualification/
cleanup records. All 64 original responses, exact query input copies and receipt
are portable under `tests/data/esr1_consensus_comparison/paired_evaluation_20261024/`.
Original training declarations/stops/ready query and earlier #62/#63 outputs
remain unchanged. The [case](../docs/content/validation/esr1_consensus_comparison.md)
and [resolved owner report](archive/esr1_consensus_comparison.md) explain the full
ledger versus native prepared-batch index mapping and all failure denominators.

Actual library/provider files match qualified training exactly; before/after
producer audit and public MolSysMT state/coordinate/atom integrity checks pass.
The unchanged library metadata remains `0.4.0+17.g25a49f5`; the evaluation driver
has its separately committed source identity. Linux/Python 3.14.9 retains all
325 Conda records, MolSysMT 0.23.0 and PyUnitWizard 0.29.0. Actual Ackredit:
60 items / 89 uses. Independent pairwise AUC, boundary-tie EF and exponential-
rank BEDROC oracles confirm both arms/common subset and missing-score scenarios.
All 103 selected scientific controls pass with 312 historical public MolSysMT
warnings retained. No new full hosted/installed matrix, public package or timing
benchmark is claimed; native receiving remains #9.
Closeout passes 49 administrative/documentation tests plus 24 subtests, including
strict Sphinx and the independent paired-result oracle, plus three reporting
tests, whole-tree Ruff, generated-index and whitespace checks.

The environment previously retained at
`/tmp/phmt64-readiness-20261024-4ceLcb/environment` is now retired after evidence
verification. Its creation prefix and 325 records were checked before scoped
filesystem removal of only that task-owned directory; no uninstall hooks,
shared-environment target/repair or global-cache cleanup runs. The earlier native
hook investigation remains MolSysSuite #139. Raw inputs/results/logs remain in
the owned training and `/tmp/phmt64-paired-20261024-qKYX7C` roots and permanent
archives. Recreate the recorded providers/library/driver separately for a new
historical replay, as documented; archive reading needs no molecular execution.

Previously pending training head `30de2b9bdce57658d445ec53265fd0144ae4afe3`
now has CI 40142394506 reporting/all eight scientific jobs and their actual
test steps successful; policy 40142394713 and Conda governance 40142394824
succeed. This does not qualify the new evaluation/archive head. Follow #9 for
its own native receiving and Documentation when available.

**Next concrete product work: [#65](https://github.com/uibcdf/pharmacophoremt/issues/65).**
Review and expose reusable native retrospective summaries of saved evaluations
with an explicit original cohort, upstream unscored causes and native/original
index mapping. Compose existing score/metric tools and common-subset comparison
without rerunning molecular search; preserve actual producer attribution. This
belongs in PHMT validation and needs no MolSysMT implementation change. #64's
case-only ledger is an explicitly tracked interim consumer; owners LMMV/dprada,
review 2026-11-07, migrate future consumers when the public contract is qualified
while retaining immutable historical driver commits.

Further biological claims require a newly declared unexposed evaluation set.
MolSysMT owns identity/scaffold (#447), conformer/state/stereo and general
preparation capabilities; receive them through #41 rather than filling gaps
here. Addon, broader docs/release infrastructure and a new public release stay
deferred; delivered public 0.4.0 and its original notice are unchanged.

## Consensus query ready; evaluation unopened — 2026-10-24

**#64 attempt 2 has a usable frozen training query.** Clean producer
`25a49f5322a06c1deeff95b396cf194fc5d8f9b6` executes the separate 12-candidate
readiness declaration, reusing all three original responses and making only
nine new requests. Eight SDFs are available; all eight prepare and pass every
MolSysMT preservation check. Four original 404 responses are retained.
The fixed first-success rule selects **31477, 6293, 9818306**, pivot 31477.
All candidate outcomes remain recorded; no score/feature-count filtering occurs.

Native consensus completes 146 fits, two layouts and three hypotheses. The
declared model ordering selects model 0, `layout_00000 / hypothesis_00000`:
two acceptors and one aromatic site, jointly supported by 31477/9818306.
All sites are essential with weight one and radius 0.15 nm. Training-only
seed-hit readiness scores are 1, 0, 1. The zero-scoring active 6293 is unplaced
to the pivot within this finite proposal family; it is not erased from source
evidence or the three-input denominator. No alternate trio/pivot/model is tried.

The outcome is `ready`, `training_complete`, **evaluation unopened**. No structure
or score from the 64 reserved inputs is acquired/computed. Original attempt 1
and all #62/#63 outputs remain intact. This is training readiness, not biological
discrimination, affinity or predictive acceptance.

Use the existing checksum reader to restore the two frozen query archives:

- Baseline: `evidence/esr1_activity_pilot_20261023_summary.json`,
  `saved_query_archive`, raw SHA-256
  `c165f3755e1a76603a69f7fd1c24259e8f4706c20407eb3fdf653a4b5f7804f3`.
- Consensus: `evidence/esr1_consensus_readiness_training_20261024_summary.json`,
  `saved_query_archive`, raw SHA-256
  `f80a09a68e21a8826a399467bb449082765e10328c8480717811049aa1d93a6d`.

The [new summary](evidence/esr1_consensus_readiness_training_20261024_summary.json)
qualifies original full output (raw SHA-256
`608b0f41f7ee181785cccbfcde65bf758e7dd056b0b179815d4991028144d8f6`),
query, logs, native environment creation and test receipt. All 12 original
response identities and failures are portable under
`tests/data/esr1_consensus_comparison/readiness_training_20261024/`, with notice.
Actual Ackredit captures retain 26 items / 86 uses, with no evaluation credit.
The [case](../docs/content/validation/esr1_consensus_comparison.md) explains both
attempts and their distinct scientific limits.

Actual Linux/Python 3.14.9 uses the same exact 325 public Conda records, MolSysMT
0.23.0, PyUnitWizard 0.29.0 and editable PHMT `0.4.0+17.g25a49f5`. Source/native
hashes and before/after producer audit are stable. All 51 selected scientific
controls pass with 232 historical public MolSysMT warnings retained. No new
full hosted/installed suite or public package is claimed.
Closeout passes 46 administrative/documentation tests plus 24 subtests, including
strict Sphinx and the frozen-query/selection guard; three reporting tests,
whole-tree Ruff, generated-index and whitespace checks pass. The original
attempt/declaration archive guards remain active. No new full scientific suite
is inferred from these selections.

**Next:** after committing these query/training records, implement/execute the
unchanged paired evaluation on all 64 reserved inputs. Native PHMT loads the
checksum-restored queries; public MolSysMT owns all molecular I/O/preparation
and fits. Keep exact declared screening settings, retain every acquisition/
preparation/search failure without replacement or inactivity imputation, and
report per-arm plus common-evaluable counts/metrics and missing-score sensitivity.
No tuning on evaluation outcomes. #64 remains partial for that comparison.

The owned public-provider environment is retained for this pending phase at
`/tmp/phmt64-readiness-20261024-4ceLcb/environment`, with raw logs/inputs beside it.
It is intentionally still useful; no retirement hook or shared/global-cache
cleanup is run. MolSysSuite #139 remains the owning cleanup diagnostic. Recheck
actual source/runtime identity before the next calculation; do not confuse the
base PHMT 0.4.0 Conda record with the editable source overlay.

Previously pending `cca31420cecb64c21bfeeff735d02fa2e443e9ce` now has CI
40134459469 reporting/all eight scientific jobs green, with actual dependency-
context/install/import/test steps verified; policy 40134459652 and Conda
governance 40134459644 succeed. This historical receiving does not qualify the
new training/archive head; follow #9 for its separate native checks/Documentation.
No addon, new release or broader documentation infrastructure is introduced.

## Second training attempt predeclared — 2026-10-24

The [new declaration](../tests/data/esr1_consensus_comparison/readiness_declaration.json)
fixes a 12-candidate training pool and provider-readiness policy under #64.
SHA-256 `b8ff6305ed7527289dad6ee13f7992b74928d93738c6f290fbdeff4099b1757e`.
It preserves the original 64 evaluation entries, baseline query, molecular
preparation route, native consensus/scoring parameters and model selection.

Reuse all three original acquisition responses exactly, including the 404;
request only the other nine predeclared candidates. Prepare all 12 with public
MolSysMT and retain failures. Select the first three successful preparations
in fixed order, without feature-count, geometry, support or score thresholds.
No alternate trio/pivot/model or increased budget follows failure. A valid
selected query and full training receipt must be committed before evaluation
acquisition/scoring. Attempt 1 remains terminal and its files are unchanged.

The [protocol](esr1_consensus_comparison.md)
links commands, source identity, cap and stop rules. The existing runner accepts
the two frozen declarations explicitly and checks original response reuse.
New guards protect unchanged evaluation/methods, the fixed candidate order,
exactly nine new requests, retained failures and score-free eligibility.
All 45 administrative/documentation tests plus 24 subtests, three reporting
tests, strict Sphinx, whole-tree Ruff and generated-index checks pass.

Next is executing only this new training stage in the same exact public-provider
environment, then archiving its measured outcome. Evaluation remains unopened;
this declaration itself produces no molecular/scoring result.

## Original training attempt stopped — 2026-10-24

**#64's declared training gate has executed and stopped honestly.** Clean source
`5242ca63eb239aaecb95ae782304dbeca7b53135` acquires only the three fixed training
inputs: PubChem supplies SDFs for 31477 and 6293, but 24633 returns HTTP 404
`PUGREST.NotFound`. Both available systems prepare successfully with public
MolSysMT 0.23.0 and pass every byte/state/atom/stereo/coordinate preservation
check. This is an unavailable acquisition, not a MolSysMT rejection or inactivity.

The all-three requirement stops this attempt at `stage='preparation'`.
**No consensus call, selected query, readiness score or evaluation exists.**
All 64 reserved evaluation CIDs remain without acquired structures or scores.
Do not replace CID 24633, relax parameters or assign a missing input a negative
score. The original declaration and original prior #62/#63 outputs remain intact.

The [summary](evidence/esr1_consensus_training_20261024_summary.json) qualifies
the full original output (raw SHA-256
`98f8320431c0b12397729f69034623cc80b41c8ca973e76915d79605443c6df6`),
execution/acquisition logs, environment creation, qualification and cleanup.
Both original SDFs, the 82-byte 404 and acquisition receipt are retained in
`tests/data/esr1_consensus_comparison/training_20261024/`, with a scoped notice.
The [case](../docs/content/validation/esr1_consensus_comparison.md) states the
measured preparation counts, zero evaluation denominator and actual 12-item /
14-use Ackredit payload without unexecuted consensus/screening credit.

Linux/Python 3.14.9 uses the same explicit 325-package public provider set as
the prior seeded replay, with exact editable source installed after provisioning.
Actual PHMT metadata `0.4.0+13.g5242ca6`, module origins, all source/native hashes
and unchanged before/after producer audit are retained. This is not a new public
package. All 51 selected rigid-consensus/scoring controls pass; 232 historical
public MolSysMT Pandas warnings remain recorded. A separate exposed-reference
control reproduces archived counts/features/states/RMSD after sharing the prior
preparation orchestration. No full scientific suite is rerun for this case-only
change or new hosted/installed matrix inferred.
Closeout passes 43 administrative/documentation tests plus 24 subtests, including
the archived-stop guard and strict Sphinx; three reporting tests, whole-tree
Ruff, generated-index and whitespace checks pass.

The owned environment is retired; raw responses/logs remain under the recorded
owned `/tmp/phmt64-training-20261024-SxBHSJ` root and are portable in the archives.
Retirement reports native success and removes its prefix, but the OpenCL hook
attempts a shared active-prefix path; the file is absent and deletion fails.
The original mixed log/JSON receipt is retained and routed to
[MolSysSuite #139](https://github.com/uibcdf/molsyssuite/issues/139). Do not treat
native cleanup success as proof of hook scope or infer a root cause. No shared
repair/global-cache cleanup is attempted; molecular results are unaffected.

Previously pending `b4565a15d211b162acff6be88e7c68620a4386ba` now receives CI
40129944533 with reporting and all eight Linux/macOS Python 3.11–3.14 science
jobs successful; their actual dependency-context/install/import/test steps are
verified natively. Policy 40129944770 and Conda governance 40129944824 succeed.
Declaration head `d53654fad6a448105f26d344f6c99bc306988e23` CI 40132174230 is
still running, with policy 40132174354 and Conda governance 40132174378 green.
These do not qualify the final training/archive head; follow #9 for its own
native receiving, including Documentation when available.

**Next:** #64 remains partial because no discrimination comparison was possible.
The original attempt is terminal under its frozen declaration. Predeclare a
distinct attempt with a bounded training-candidate/readiness policy before any
new acquisition, preserving the still-unopened evaluation cohort and scientific
method parameters. Readiness must use provider-owned molecular operations; do
not silently substitute an input, generate conformers locally or tune against
evaluation. MolSysMT #447 remains a separate molecular-overlap proposal and is
not the cause of this stop. New addon/release infrastructure stays deferred.

## Training-only comparison declared — 2026-10-24

The next scientific segment is [#64](archive/esr1_consensus_comparison.md).
Its [protocol](esr1_consensus_comparison.md) and
[frozen declaration](../tests/data/esr1_consensus_comparison/declaration.json)
are fixed **before new structure acquisition or molecular scoring**. They
compare the unchanged original #62 query against one native rigid consensus
learned from three new actives. All molecular work remains MolSysMT-owned.

The source is the original archived AID 743075 v2 concise response. Exclude all
4,402 CIDs in the entire Bath table and all 370 assay CIDs with conflicting
outcomes, including inconclusive. Use lowest-SID representatives and a distinct
SHA-256 order. Of 338 eligible actives / 2,749 inactives, reserve three actives
for training (31477, 24633, 6293); the next 16 actives and first 48 inactives are
the 64 evaluation inputs. All 67 CIDs are distinct. Labels inform stratification;
new molecular features/scores have not been examined. Same-assay CID separation
does not establish chemical-series or independent-assay validation.

The method, finite budgets, training-only model choice, readiness check,
failure/no-replacement rules, baseline query hash and comparison denominators
are frozen in the JSON. The standard-library declaration driver reproduces it
from checksum-qualified original sources and refuses output overwrite. Two
offline guards verify that mechanism, synthetic label conflicts, row-order
independence and changed-source refusal. This is not a scientific run; no new
conformer, query, evaluation score or public artifact is produced.
The declaration SHA-256 is
`a1a476e7e94fd3480ee3845fbc5cca138221c4052eb7165a254499fd526ff647`.
All 40 administrative/documentation tests plus 24 subtests and three separate
reporting tests pass; strict Sphinx, whole-tree Ruff and generated-index checks
pass. No molecular suite or original scientific output is rerun for this slice.

**Next action:** acquire only the three training SDFs, retain their original
responses/failures and qualify preparation with public MolSysMT 0.23.0 in an
owned environment. Execute the declared native consensus and save all original
evidence. A valid selected query and training receipt must be committed before
evaluation structures or scores are opened. If training prerequisites fail,
retain the outcome and keep evaluation unopened; do not replace inputs or tune
the declared method. The protocol links the existing exact provider environment
and source-overlay route; no new environment has been created yet.

Source/issue inspection identified a missing reusable molecular identity/scaffold
overlap route; the proposal is
[MolSysMT #447](https://github.com/uibcdf/molsysmt/issues/447). It does not block
this explicitly CID-only comparison. Do not implement that molecular analysis in
PHMT or promote the split into a chemical-series independence claim.

Previous head `b4565a15d211b162acff6be88e7c68620a4386ba` receiving remains partial:
CI 40129944533 has reporting and both Python 3.14 science cells green, with six
remaining science cells running. Policy 40129944770 and Conda governance
40129944824 succeed. Documentation was not yet listed. Local declaration checks
do not establish this or the next head's full hosted matrix; follow #9 receipts.
Addon, additional release and wider documentation work remain deferred.

## Portable pilot inputs — 2026-10-24

**#62's bounded activity pilot is complete.** The exact original 35-file input
bundle is now portable in this repository, with its original SHA-256 and a
[scoped rights/attribution notice](evidence/esr1_activity_pilot_inputs_20261023_NOTICE.md).
The [snapshot summary](evidence/esr1_activity_pilot_inputs_20261023_summary.json)
qualifies the 12,495,338-byte archive and the unchanged original query archive.
Old manifests/results and their dated narrower publication statements are not
rewritten. The [resolved report](archive/esr1_activity_pilot.md) records closeout.

The current unshipped driver restores 35 inputs plus the original saved query
without network or molecular dependencies:

```bash
python phmt_test_support/esr1_activity_pilot.py \
  --data-dir /tmp/esr1-original-inputs --restore-archive
```

Use a new destination. The operation checks the compressed/raw archive and all
original file identities, rejects substitutions and preserves all five failed
HTTP responses. It reuses the existing evidence reader; molecular operations
remain in MolSysMT. Seven offline case guards pass, including reconstruction of
the original Bath split and primary-assay labels. This does not rerun or upgrade
the dated scientific evidence. The [case](../docs/content/validation/esr1_activity_pilot.md)
now shows how current offline restoration feeds each recorded scientific producer.
Verification totals: 38 administrative/documentation tests plus 24 subtests,
18 archive-reader tests and three reporting tests pass in their separate CI
process contexts. Strict Sphinx, whole-tree Ruff and generated-index checks pass.

**Next:** declare a new scientific comparison with prepared training inputs and
an actually unexposed evaluation cohort. #62 is exposed development data; its
binary replay is not new biological validation. Keep provider receiving under
#41 and conformer/stereo/H needs in MolSysMT. The addon and further release or
documentation infrastructure remain deferred; public 0.4.0 is unchanged.
The detailed #63 source/environment checkpoint below remains applicable.

Hosted receiving for source `481855e7e9de745793d8cd36296ff9be81e99094` is still
partial at this inspection: CI 40127949298 has reporting and Linux/macOS Python
3.14 green; the six Python 3.11–3.13 science cells are running. Documentation
40128123736, Conda governance 40127949565 and suite policy 40127949623 succeed.
Do not claim full-matrix qualification until native completion. This retention
change will receive its own unskipped push and native checks.

## Current MVP checkpoint — 2026-10-24

**#63 is implemented and locally qualified.** Its
[resolved report](archive/rigid_negative_ranking_contract.md) and
[contract](seeded_ranking_workflow.md) separate raw checked-pose coverage from
explicit `search_method='seeded_hit'` molecular ranking. The new criterion tests
fitted triplet seeds only: hit one, completed negative zero, failed/unresolved
input unscored. It excludes the arbitrary supplied placement. Negative ties
do not use partial coverage. When no pose is fitted, no coverage or coordinates
are invented. This is a bounded binary search criterion, not a graded partial
optimum, exhaustive continuous-pose search, affinity or predictive qualification.

The direct compatibility search defaults remain. Retrospective/facade consumers
now require explicit `score_method='checked_pose_coverage'` to rank legacy
rigid/conformer evidence; placed evaluation retains its declared-frame default.
Public `get_screening_score` is reused across consumers. Exports distinguish
criterion, molecular score and raw `fit_value`. All molecular operations stay in
public MolSysMT; no provider implementation or dependency requirement is changed.

Clean implementation/replay producer is
`c80325c5c3851691bcc0a993d1e73eaf294654f6`. The complete source suite passes
**949 tests** on Linux/Python 3.14.9 with public MolSysMT 0.23.0, PyUnitWizard
0.29.0 and the declared test extras. All 223 recorded runtime/test/support Python
hashes remain unchanged through the source commit and suite. Warnings are
retained, including historical public MolSysMT deprecations and intentional
attribution-failure controls. The new code is **development source after 0.4.0**;
no new package/release is produced and public 0.4.0 keeps its original API.

The [replay summary](evidence/esr1_seeded_hit_replay_20261024_summary.json) qualifies
original full output, preparation journal/log, unchanged original query archive
and source qualification receipt. Its declaration was fixed before new scores.
All 32 input identities/order and query bytes are unchanged: 25 evaluate (6 active
/ 19 inactive), six remain unscored (1 / 5), and the same active CID 24964624 hits.
Binary AUC is 0.5833333333, BEDROC(alpha=20) 0.6496274186 and EF at 10%
1.9675925926. Twenty-four scores tie at zero; 23 valid negatives have no fitted
pose. The original continuous-coverage run is preserved. These are different
criteria and recorded runtimes on exposed data, not a biological improvement or
fresh independent holdout.

Actual source origins/hashes distinguish the editable PHMT overlay from the base
Conda package record. Editable version metadata was generated before the source
commit; it is not executed-source identity. The 325-package
[Linux explicit environment](evidence/seeded_ranking_environment_20261024_explicit.txt)
retains public URLs and SHA-256, is parsed in a successful native Mamba dry run,
and must be followed by installing the recorded source producer. Do not treat
that base environment as a new PHMT public artifact.

### Where to continue

1. **#62:** resolve portable long-term original-input retention. Originals remain
   in `/tmp/phmt-ligand-pilot-20261023`, including the hashed 35-file bundle in
   the prior checkpoint. Raw input redistribution is not claimed; strict restore
   refuses refreshed upstream bytes. Original and replay outputs are archived
   independently here with checksum-qualified readers.
2. Declare the next scientific comparison on reviewed prepared training inputs
   and a genuinely unexposed evaluation set. Do not tune against #62's observed
   outcomes or call the development replay independent validation. Binary hit
   classification is now usable; graded partial ranking is not supplied by #63.
3. **#41 / provider receiving:** qualify newer molecular contracts separately.
   Existing conformer/stereo needs remain MolSysMT #219/#215/#299. Environmental
   H refinement #323 and newer directional-contract #375 receiving do not block
   this completed local scoring slice. Do not fill their molecular gaps here.
4. New addon work and broader documentation/release infrastructure remain deferred.
   The only documentation changes here explain the delivered source contract and
   executed scientific cases. Public 0.4.0 / MolSysSuite #131 is unchanged.

The previously pending source `29000c36a9375082e7f950ff78210dd7f7bdc27a` receiving
is now verified: CI 40019851558 has all eight science cells and reporting green;
policy 40019851935, Conda governance 40019852035 and Documentation 40019903965
succeed. That does not qualify this new implementation/final head. The final
unskipped push receives its own native gates; local receipts do not claim their
completion. Follow the owning #63/#9 run receipts for unfinished hosted evidence.

Temporary qualification prefix/output ownership and retirement are recorded in
the replay summary. The shared development environment and caches are not cleanup
targets. Recreate an environment from the explicit provider file and overlay the
recorded source when replaying; keep original data and original output archives.

## Current MVP checkpoint — 2026-10-23

The maintainer resumed the scientific MVP and deferred deeper documentation and
addon work. [#62](archive/esr1_activity_pilot.md) now has an executed,
pre-score frozen ligand-reference ERα signaling-assay pilot. The protocol/driver
producer is `ee064102f3701a280297e01ec0c549207f10bfd3`; the runtime is installed
public PharmacophoreMT 0.4.0 / MolSysMT 0.23.0, Linux/Python 3.14.9, with all
311 Conda records and native-extension identities in the full output. No runtime
or molecular-provider code is changed.

The [summary](evidence/esr1_activity_pilot_20261023_summary.json) qualifies the full
result, saved query, preparation journal and log. Four contradictory-label CIDs
were excluded before any scores. Of the 32 selected inputs, one is the reference;
seven active and 24 inactive inputs are held out. Five lack PubChem 3D records;
MolSysMT rejects one further stereo interpretation. **25 inputs are evaluated
(6 active / 19 inactive), six remain unscored (1 / 5)**. AUC is 0.5614, EF at
10% 1.69, one active hits and 23 scores tie at zero. The missing-score hypothetical
AUC range is 0.4494–0.6280. This is weak exploratory evidence, not a predictive
qualification; exact CID disjointness does not establish independent series.

The [case](../docs/content/validation/esr1_activity_pilot.md) supplies executable
commands, original labels and method/units/attribution boundaries. Three cheap
offline guards check original identities, failures/denominators and independent
pairwise AUC/tie-aware EF arithmetic. They do not rerun molecular science.

### Next steps

**First local MVP priority is now [#63](archive/rigid_negative_ranking_contract.md).**
A separate source control reproduces partial negative coverage 1/3 → 0 under
MolSysMT translation of the same propane input. Both searches remain completed
negatives. Define/qualify the molecular ranking contract before expanding activity
claims; this is local PharmacophoreMT work, not blocked by MolSysMT. The
[original probe](evidence/rigid_negative_frame_probe_20261023.json) is distinct
from the frozen public-runtime assay experiment and does not overwrite it.

1. Preserve the frozen query and original run. Do not tune it on the exposed
   held-out outcomes. The native reference has two acceptors and one aromatic
   site; no donor is emitted, and no donor-bearing query acceptance is inferred.
2. Resolve portable long-term retention of original input bytes under #62. The
   owned `/tmp/phmt-ligand-pilot-20261023` retains source archives, primary assay
   description/table and 27 SDFs; the committed manifest has URLs/hashes. Raw
   input redistribution is not claimed. Strict restore refuses refreshed
   responses; preserve originals if upstream bytes change.
3. Follow consumer evidence in provider-owned MolSysMT #219 (missing conformers)
   and #215/#299 (explicit stereo rejection); do not repair molecules here.
4. Declare a distinct next comparison using reviewed training/evaluation data,
   conformer policy and frozen parameters. These exposed outcomes are development
   evidence, not a fresh independent test set. No addon is needed for this step.

Provider handoffs are delivered in [MolSysMT #219](https://github.com/uibcdf/molsysmt/issues/219#issuecomment-6373946367)
and [#215](https://github.com/uibcdf/molsysmt/issues/215#issuecomment-6373947311).
Original inputs are additionally bundled locally as
`/tmp/phmt-ligand-pilot-20261023/original-inputs-20261023.tar.gz` (35 files,
12,495,338 bytes; SHA-256
`fc6a5295bbf4dbd9743f31a7f54d396b09578e60754ebcabd4388a588252e995`).
This is local retention, not public redistribution or a long-term archive service.

Local acceptance passes: three pilot guards, 18 existing archive-reader tests,
three reporting tests, all 33 administrative controls with immutable SDK
`1c248b67d1daea256ed7c7f6172c6addb3f0b08f`, whole-repository Ruff and complete
strict Sphinx build (one test, 7.73 s). The first SDK control run caught the new
guard importing the unshipped namespace before its staging test; loading the
canonical standalone reader without namespace registration repairs isolation.
No scientific rerun or data/score change is involved.

The isolated environment has been **retired after successful execution**; all
27 original SDF checksums were reverified before cleanup. Original inputs and
outputs remain in the owned directory, with portable output archives committed.
No shared environment/cache is touched by cleanup. Prior public 0.4.0 delivery
and central follow-ups remain
unchanged; no new release or MolSysSuite availability notice is required here.

Native receiving at scientific/evidence source
`598d3744dc5348b497747d68f3a22a4c5d14ae53`: policy **40018408199**, Conda
governance **40018408302** and Documentation **40018949108** succeed. CI
**40018407677** has successful reporting governance; its eight scientific cells
are still in progress at this observation. The push-only daily backlog detector
is inapplicable/skipped, not executed acceptance. Do not claim eight-cell or
exact-final-head completion from this snapshot. The documentary qualification
and #63 inventory change pass all 33 local administrative controls, reporting,
Ruff and complete strict Sphinx (7.81 s); the final unskipped push receives its
own native gates. Follow the owning runs/#9 for unfinished native evidence.

## Current documentation outcome — 2026-10-23

The first documentation foundation is complete. The inherited identity (#4) and
reader-entry work (#61) are resolved in the [identity archive](archive/documentation_project_identity.md)
and [entry-point archive](archive/documentation_reader_entry_points.md).
About, landing, user/developer/showcase portals and the cookbook introduction now
describe PharmacophoreMT's delivered routes and point to the existing recipes,
API and evidence. The theme/configuration and runtime code are unchanged.

The [local receipt](evidence/documentation_foundations_20261023.json) records the
complete strict Sphinx guard, six rendered page checks and preserved notebook
execution material. The [native receipt](evidence/documentation_publication_20261023.json)
binds source `7aa33cd88806dcde05a01a9416df11d844cb9b62` to successful Documentation
40011094526, policy 40011098877, Conda governance 40011103894 and administrative
probe 40011110286. Six pages were read from immutable gh-pages
`c869f6ed18a4dc8ee510efea4d5cf979e8cc0ef0`; Pages reports the site built.
The probe omits science, and this work executes no notebook or molecular workload.
No new package, scientific/provider, visual/browser or documentation-badge
acceptance is inferred. The closure commit changes only reports/indexes/evidence;
the published documentation content remains that reviewed source.

Next local documentation work can develop the user guide's concepts and worked
routes beyond these portals, with new examples executed only in an explicitly
qualified context. Reuse the existing cookbook/validation collection; keep
molecular operations with MolSysMT. #41/provider receiving and #20/#22 scientific
validation retain their independent scopes; new addon work remains deferred.
Public 0.4.0 and its central delivery follow-ups remain in the prior checkpoint.

Local HTML and review records remain in the owned
`/tmp/phmt-docs-foundations-20261023` directory for optional human preview. Durable
JSON receipts are committed here; there is no new environment, cache or server to
keep running. Documentary skip/recovery remains tracked under #9.

## Prior documentation preparation — 2026-10-23

The maintainer resumed documentation work using MolSysMT/MolSysViewer's existing
Sphinx/MyST/PyData pattern as reference. #4 owns the inherited PocketMT identity;
#61 owns reader entry points. About now describes PharmacophoreMT and its molecular
ownership boundary; landing/user/developer/showcase pages lead into existing
recipes, API and evidence. `docs/README.md` supplies the local contributor route.

The complete strict Sphinx guard passes after including that new guide in the
developer toctree. The landing notebook's code, outputs and metadata are preserved;
no notebook or molecular calculation is executed for this narrative slice. Native
publication and report archival are the next closeout steps. These are documentation
controls, not a new release or an extension of the scientific/provider acceptance
record. New addon work remains deferred.

This documentation checkpoint uses a conditional `[skip ci]` after the local
strict/rendering and reporting checks; native documentation publication and
administrative checks follow on its committed head. Full scientific backlog
remains #9's scope and is not cleared by those documentation controls.

## Prior delivery checkpoint — 2026-10-23

**0.4.0 is public**: [GitHub Release](https://github.com/uibcdf/pharmacophoremt/releases/tag/0.4.0)
and [official Conda package](https://anaconda.org/uibcdf/pharmacophoremt).
The tag points to original producer
`60b21b7d183217d50c29ea3e6bc0d05fb5b797a2`. One original
`pharmacophoremt-0.4.0-py_0.tar.bz2` was promoted from staging to main with SHA-256
`e5ed3a7c20ec36b9938fee51a6a9e0dc1654d7709d0d26ad75e49babac5d59a4`.
Historical tags are unchanged. The maintainer's requested availability notice is
[MolSysSuite #131](https://github.com/uibcdf/molsyssuite/issues/131).

The [source/staging receipt](evidence/conda_040_staging_20261023_summary.json)
retains all eleven required executed source/control jobs, recipe tests, producer
39996616723 and the independently downloaded original archive. The
[delivery receipt](evidence/conda_040_delivery_20261023_summary.json) retains
installed run 39997342556 (**8/8 cells, 921 passing items each**), all four required
phases, eight support execution/cleanup receipts, promotion/public-verifier run
40002784859 and fresh normal public receiving on Linux/Python **3.14.9**.
Normal Python bounds are honored. SDK call reports include unittest subtests and
are distinct from the reported 921 test items. Existing warnings are retained.

Producer and installed workflow head
`c0f6ac65aad6fa7e1018636e6b0756668aed5459` adds only contributor/guide notices;
the source, workflows, tests and support remain those of the original producer.
The native binding and common verifier explicitly retain both identities. The
accepted SDK remains `1c248b67d1daea256ed7c7f6172c6addb3f0b08f`; no later SDK
capability or newer MolSysMT development API is adopted by this release.

### What remains and where to resume

1. **MolSysSuite #131 / #45:** receive the delivery and triage the automatic
   Release-event route. Run 40004204755 is **failure**: the shared publisher rejects
   a staged plan at the metadata-freeze guard. Build and upload steps are skipped;
   this is separate from successful staging, installed science and promotion.
   #10 remains partial for that route disposition; do not rebuild/overwrite 0.4.0
   or move its tag to make this extra event green.
2. **MolSysSuite #131 / #51 and local #23:** review central public Python admission
   and generated badge/inventory updates. Four-minor installed evidence is now
   delivered; the existing centrally admitted badge is retained pending disposition.
3. **Local #41 / MolSysMT #375:** qualify the newer H-bond namespace/directional
   contract separately, using provider-owned geometry. The release's qualified
   public molecular-provider context is MolSysMT 0.23.0. Its retained pandas
   warnings belong to the historical public version; #431/#386 have source fixes
   and this receipt does not establish a regression against them. Environmental
   hydrogen refinement #323 remains independent upstream work.
4. **#20/#22:** continue the independent scientific/biological validation with
   declared inputs and controls. New addon work remains deferred; #58 and its
   viewer-owned blocker are not closed by package publication.

Read the current owning issues before starting another segment. Public release
availability does not establish biological/activity discrimination, newer-provider
compatibility, public PyPI delivery or live-browser/hardware acceptance.

### Closeout evidence and resources

The final public receiving succeeds after an owned disk-quota cleanup and two
corrections to the one-off audit script (external-provider recursion and optional
test-extra metadata). These failed attempts are retained separately; no runtime
package code, required gate or warning filter was changed to obtain the result.

Completed historical/current receiving and build environments/caches were retired
under the task-owned temporary roots. Shared user environments/caches are untouched.
Original archive, clean producer clone and receipts remain under
`/tmp/phmt-conda-040-20261023`; the accepted SDK and historical wheel/receipts remain
under `/tmp/phmt-installed-qualification-1wwqno5j`. The old `public-env`, build envs
and caches listed in the dated pause below no longer exist. Durable compressed
receipts are committed here, so resumption does not depend on `/tmp` surviving.

This documentation/evidence closeout uses `[skip ci]` after its applicable local
checks. Ordinary CI debt and nightly/weekly/manual recovery remain owned by #9;
it does not acquire the exact-source qualification of `60b21b7`. Current native
documentation/coordination receipts are linked from #10 and MolSysSuite #131.

## Prior resumption checkpoint — 2026-10-23

The maintainer resumed work and confirmed the proposed **0.4.0** candidate by
instructing continuation after the explicit version question. The active segment
remains #10/#9/#23; new addon work stays deferred. The reviewed real
[`release_plan.toml`](../devtools/conda-build/release_plan.toml) selects version
0.4.0, build 0, one noarch archive and the staged route. Its eight installed cells
and eleven required source/control jobs preserve the existing contracts.
`dependencies_public = false` conservatively retains unqualified candidate
closure; the prior public-provider wheel result is not candidate qualification.

Next, obtain exact-source native gates for the committed plan, establish staging
access, build one original archive and execute the eight installed cells before
reviewing public promotion. Candidate SHA, filename, digest and native run IDs
will be recorded after execution; no public tag or GitHub Release is selected by
this plan commit. Follow [publication operations](../devtools/conda-build/README.md)
and the ordered steps in the dated pause record below.

During the pause, MolSysSuite independently received the source/helper milestone;
see [the central receipt](https://github.com/uibcdf/molsyssuite/blob/338a4fceb81a11e3eec89635bb9d8ae0b054de65/devguide/rollouts/pharmacophoremt_support_receiving_45_20261021.json).
The source gates and support hashes were verified; central did not reinstall the
original wheel or qualify a Conda candidate. Shared #92 advance notices are
available for later deliberate review; they do not require replacing the
already-qualified immutable SDK for this candidate.

## Prior pause checkpoint — 2026-10-20

The maintainer requested a pause. Resume with this section and the
[current roadmap](roadmap.md), then consult the
owning reports linked below. No build, test, upload or publication task needs to
continue during the pause. New addon work remains deferred.

### What we were doing

The active segment is distribution and installed qualification under
[#10](pending_proposals/noarch_distribution_adoption.md), with source CI in
[#9](pending_bugs/full_ci_routes_and_skipped_push_recovery.md) and public/Python
delivery in [#23](pending_proposals/adopt_required_python_314.md).
The implementation is committed as `636373d3c5c24a1eff6d2bec5f3eceb6ce018ba4`;
the subsequent evidence-only checkpoint is
`63b9ef67e54102a83b688b5cbf2dea79e054a57d`. Both are on upstream main. This pause
update changes documentation only; it does not acquire the implementation's
exact-source CI identity. Its `[skip ci]` handoff retains ordinary CI debt and
daily/weekly/manual recovery under #9; local index/reporting checks cover this
documentation change.

- Packaging metadata #57 is resolved and archived, with isolated sdist/wheel
  builds using setuptools 77.0.3 and 84.2.0; see
  [the result](archive/packaging_license_metadata.md).
- MolSysSuite #117 is adopted at
  `1c248b67d1daea256ed7c7f6172c6addb3f0b08f`. Scientific helpers are explicitly
  staged from the unshipped `phmt_test_support` namespace. The real isolated
  development wheel passes **921 tests** on Linux/Python 3.14.8 with public
  providers, including MolSysMT 0.23.0. All 179 runtime paths match and staged
  support resources/imports are retired; see
  [the receiving receipt](evidence/installed_support_adoption_20261020_summary.json).
  The separate preparation record preserves the original six failed cases.
- Source CI at `636373d` passes **8/8** Linux/macOS arm64 × Python 3.11–3.14
  scientific cells plus reporting, policy and Conda governance: eleven required
  executed jobs. See [the exact-source receipt](evidence/source_ci_receiving_20261020_summary.json).
  CI run 39478128959, policy 39478129327 and Conda governance 39478129573 belong
  to that implementation, not to later documentation commits.

### Decision still pending

The maintainer initially selected **0.1.0**, but that upstream tag already points
to historical commit `f0810257a8ed05897643d6303e264adb2697b727`. Remote inspection
on 2026-10-20 confirms tags 0.1.0, 0.2.0 and **0.3.0** (the highest version;
`efb18c28b23e8c017a9c420fa7cf91dc54997ace`), with no GitHub Releases listed.
**0.4.0 is proposed, not approved.** Confirm the maintainer's collision-free
version choice on resumption; preserve the historical tags.

There is still no actual `devtools/conda-build/release_plan.toml`, original Conda
candidate, staged upload, eight-cell installed Conda result or public promotion.
The example's 0.0.0 is illustrative. Repository-level inspection found no
`ANACONDA_UIBCDF_TOKEN`; inherited organization access and validity remain
unknown. Source CI and the development wheel do not qualify a Conda candidate.

### Resume in this order

1. Check the worktree and upstream main for changes, read the current #10/#9/#23
   issue updates and confirm the version choice. Read
   [publication operations](../devtools/conda-build/README.md) and
   [release titles](release_titles.md) before preparing the real plan.
2. Commit a reviewed `release_plan.toml` with the selected version, actual build
   number, staged route, responsible maintainer/date and required gates. Obtain
   the required source gates for that exact new candidate SHA; do not reuse
   `636373d` as if it contained the new plan.
3. Establish staging access and build/upload one original archive using
   `build_and_upload_conda_packages.yaml` with the reviewed `candidate_sha` and
   `version`. Retain the original filename, SHA-256 and producer receipts.
4. Run `test_installed_conda_package.yaml` for that exact SHA/file/digest across
   all eight supported cells. Require installation, installed-file validation,
   complete scientific tests and the post-test provenance recheck in every cell.
5. Review the publication decision only after qualification. Promotion preserves
   those exact bytes; public-label/index and clean receiving checks remain
   separate #10/#23 evidence. Update owning reports/issues with actual results.

The maintainer permits direct commits/push to main; no PR is required for this
internal route. General molecular manipulation remains MolSysMT-owned and
missing provider capabilities are proposed through provider issues.

### Independent follow-ups and local resources

[#41](pending_proposals/retire_legacy_molecular_operations.md) remains partial:
the newer sibling MolSysMT source moved H-bond APIs to `interactions.hbonds` and
exposes directions, but that namespace/directional contract is not yet qualified
by PHMT. Its exploratory shared-editable run failed; use the report's provider
identity and evidence when reviewing migration. Do not treat it as the passing
public MolSysMT 0.23.0 context or restore local molecular algorithms. Provider
#375 qualification and environmental H refinement #323 are separate follow-ups.
After the distribution segment, #20/#22 retain independent scientific-validation
work; addon #58 remains lower priority with its provider-owned viewer blocker.

Owned temporary resources are intentionally retained at
`/tmp/phmt-installed-qualification-1wwqno5j` (also recorded by
`/tmp/phmt-installed-qualification-path`): `public-env`,
`build-envs/phmt-candidate-build`, `sdk-installed`, `support-artifacts` and
`final-receptor`. Their presence was checked at pause. The build environment was
created with qualified Mamba 2.9.0/declared-only channels. Recheck these resources
before reuse; `/tmp` can disappear. Durable receipts are committed under
`devguide/evidence/`, so resumption does not depend on those directories.
Review owned temporary-resource cleanup when the candidate segment closes.

## Prior pause checkpoint — 2026-10-13

The implementation checkpoint is `eca174b`, published on the official
`uibcdf/pharmacophoremt` main branch. Use the [current roadmap](roadmap.md)
and the [pending issue indexes](pending_proposals/README.md) for resumption;
the chronological observations below preserve their original dates and scopes.

The minimal viewer addon (#56) and panel feedback/teardown (#59) are resolved.
#59's [archived report](archive/viewer_panel_feedback.md) links the final
14-control live-browser record and 23 native addon tests. #58 remains partial:
its [current-provider receipt](evidence/current_viewer_addon_20261013_summary.json)
reproduces the molecular-free workspace blocker owned by MolSysViewer #240.
The later panel run uses the development provider and does not change that
installed-provider record or qualify public browser delivery.

At this checkpoint, policy and Conda governance runs for `eca174b` succeeded;
[scientific CI 38438999594](https://github.com/uibcdf/pharmacophoremt/actions/runs/38438999594)
was observed queued, so its complete matrix is not claimed to have passed.
This is a dated observation, not a current run-status monitor.

Remaining work is already owned: #57 packaging metadata, #10/#23 installed/public
delivery with MolSysSuite #117 helper isolation, and #58 receiving after the
MolSysViewer fix. Molecular preparation and remaining #41 geometry delegation
stay with MolSysMT. No development task needs to remain running during the pause.

## Historical implementation observations

**Original status (2026-10-03):** Gen 1b classical consolidation. The immediate
priority is executing traditional workflows, with the growth contracts needed
for later scientific methods and measured acceleration.

## Verified local scope

The [observed-complex route](placed_pose_workflow.md) consumes native MolSysMT
hydrophobic/H-bond, [ionic observations](ionic_interaction_workflow.md) and
[pi-pi/cation-pi observations](aromatic_interaction_workflow.md).
The [reference-ligand route](reference_ligand_workflow.md)
builds queries from six classical chemical families. Both use public MolSysMT
recognition; aromatic planes and charge geometry also come from MolSysMT.
Pose evaluation has explicit essential, weight, direction/normal and exclusion
semantics. Native JSON preserves the delivered definitions and provenance.
The [rigid-search route](rigid_search_workflow.md) composes reusable correspondence
and alignment tools with that evaluation. MolSysMT performs molecular fitting
and coordinate installation. Unresolved search budgets retain failure state. The
[prepared-conformer route](conformer_screening_workflow.md) searches requested
frames and retains their states, pose coordinates and failures. Only resolved
molecule scores enter retrospective metrics.

Metrics and retrospective accounting now distinguish scientific negatives from
failed calculations and preserve input identity and ranking ties. Guards are
`tests/test_pose_evaluation.py`, `tests/test_reference_ligand.py`,
`tests/test_retrospective.py`, `tests/test_validation_metrics.py`,
`tests/test_contracts.py`, `tests/test_rigid_search.py` and
`tests/test_conformer_screening.py`. Verification uses pinned provider source trees
with existing scientific dependencies; see the workflow documents for limits.
The complete local suite passed 118 tests; the reference-ligand, rigid-search and
prepared-conformer documentation examples and offline reporting/quality checks
also passed.
User-facing executable recipes now live in the
[cookbook](../docs/content/cookbook/index.md), linked from the documentation
navigation and user guide.

After native Ackredit integration, the complete local suite passed **132 tests**
(including 14 attribution controls) on Python 3.13.14 with the controlled source
providers. Both attribution cookbook code blocks executed successfully. Ackredit
is pinned to `584328de6efc07cee3a5ddf3ecda2d2e08cc72b4` for controlled development
verification; this is not published-wheel or hosted-matrix closure.
The isolated cookbook Sphinx build passed with nitpicky checking and warnings
treated as errors. This is a cookbook build, not full-site build acceptance.
Cross-provider failure isolation under warnings-as-errors awaits the observed
MolSysMT attribution-warning correction in `uibcdf/molsysmt#295`.

The first native [aligned-ligand consensus](aligned_consensus_workflow.md) is now
implemented locally: reusable fixed-frame feature matching and explicit-group
aggregation feed a reference-anchored model builder. It retains one contribution
per declared ligand, correspondence/source evidence, mean feature centers,
reference orientations, dispersion, rejected groups and Ackredit metadata.
After this slice the full local suite passed **149 tests**, including 17 consensus
controls. Both aligned-consensus cookbook blocks executed successfully; the
independent reporting/index checks and Ruff also passed.

These local changes await review. They do not establish published-wheel,
hosted-matrix, free-screening or biological-pilot success. Historical existence
of the legacy modelers and utilities is not evidence of complete consolidation.

## Owning work and next steps

Issues `#12`, `#13`, `#14` and `#15` own ranking/accounting, the first native complex
slice, native reference-ligand construction and native rigid pose search.
`#2`, `#6`, `#9` and `#10` retain diagnostic, support-library, CI and distribution work.
Issue `#16` tracks the locally corrected zero-angle normalization-roundoff defect.
Issue `#17` owns prepared-conformer screening and per-frame score resolution.
Issue `#18` owns the measured legacy distance/clique defects and native consensus
replacement; the [literature and ownership review](clique_consensus_review.md)
and bounded executable audit are delivered locally. Issue `#19` owns deferred
native Ackredit capture, detached bibliography and report integration, now
implemented with real-provider controls and a cookbook recipe. Distribution and
hosted-matrix acceptance remain pending.
Issue `#20` records the future decision between a documentation validation/
benchmark section, dedicated website or common evidence collection with both
views, including reproducible notebooks and publication/update policy.
Issue `#21` owns the reference-anchored aligned consensus, its independently
reusable matching/aggregation tools and the executed cookbook recipe.
Issue `#22` owns the [ERalpha input audit and native validation gate](eralpha_validation.md).
The checksum-qualified real fixture has incomplete declared chemistry; public
PDB-text/RDKit conversion does not supply supported bond orders. Native recognition
rejects it explicitly. Molecular template application is tracked in
`uibcdf/molsysmt#298`; positive native ERalpha validation and verified derivation
from the historical 1QKU dataset label remain pending. The case now has an audit
guard and a cookbook notebook, distinct from the retained legacy regression.
The two ERalpha tests passed with the controlled source providers; the notebook's
three code cells executed successfully and its schema/output checks passed.
The audit CLI emitted valid JSON, the isolated cookbook build passed strict
Sphinx checking, and the three reporting tests, generated indexes and Ruff passed.
The latest complete-suite result remains the 149-test run above; this slice was
verified with its focused tests and documentation rather than a new full run.

On **2026-10-03**, the next slice added independently acquired RCSB 1QKU/CCD EST
source bytes with URLs, checksums, entry revision and exact ligand identity.
The selected label chain D (author chain A, residue 600) has 20 observed heavy
atoms; the CCD definition also has 24 H whose complex coordinates remain absent.
Native chemical preparation is still pending. The minimum read-only assessment
and transactional template-application contract is now specified in the owning
MolSysMT #298 proposal; it is not an implemented public API.
All **three ERalpha tests** passed under the controlled source providers, and the
updated cookbook notebook executed **four code cells** without errors. Both
repositories' generated proposal indexes/guide checks and the three local
reporting tests passed; the strict isolated cookbook build, Ruff and whitespace
checking also passed. No new full-suite,
positive native ERalpha or biological result is claimed.

On **2026-10-03**, the independent next slice added
[aligned clique consensus](aligned_clique_consensus_workflow.md), owned by #24.
Reusable feature-clique discovery, aggregation/hypothesis packaging and the
prepared-ligand model builder discover sites absent from a reference and retain
alternative models. Hypotheses require disjoint occurrences and a common ligand
support intersection. NetworkX owns generic enumeration; optional Ackredit credits
the executed Bron--Kerbosch/Tomita implementation references and the provider's
description/software versions, with detached bibliography in each saved model.
The executed cookbook exposed a provenance defect (#25): literal IDs such as
`a` and `b` were parsed as units. The owning copier now preserves strings before
quantity-object sealing, guarded against the original IDs rather than only output
roundtrip equality. The final complete local suite passed **177 tests** in 114.94 s,
including 25 clique controls and the literal-string/quantity regression. Two
warnings remain: the deliberate Ackredit-failure control and the existing legacy
screening unit-stripping path; neither is new clique-method failure evidence.
All **three aligned-clique cookbook code blocks** executed successfully. The strict
isolated cookbook Sphinx build passed, as did the three offline reporting tests,
generated indexes, Ruff and whitespace checks. This verifies the source checkout
under the existing controlled provider pins; it does not establish whole-site,
installed-wheel, hosted-matrix or biological acceptance. Molecular preparation
remains with MolSysMT #298/#300.

On **2026-10-03**, #26 adds [prepared rigid unaligned consensus](rigid_consensus_workflow.md)
with an explicit pivot and reusable association-clique or typed-triplet proposals.
All molecular fits/transforms remain in MolSysMT. Absolute post-fit geometry and
injective matching are checked; accepted alternatives feed separate aligned
consensus layouts. Unplaced ligands retain source evidence and input support
denominators. The [primary-source strategy survey](pharmacophore_search_strategies.md)
compares efficient published alternatives and records G3PS, safe RDP/frequent-clique
conformer discovery, triangle indexing and Gaussian overlap as distinct future
comparisons. Runtime Ackredit credits executed clique/assignment solvers and the
provider-documented Kabsch criterion, rather than unimplemented design references.
The complete suite passed **202 tests** in 180.84 s, including 25 new rigid consensus
controls. The two new cookbook blocks executed successfully. The isolated strict
cookbook build, three reporting tests, generated indexes, Ruff and whitespace
checks passed. The same two pre-existing warnings remain. Source-provider pins
are unchanged; these are analytical/integration controls, not comparative timing,
biological, installed-wheel, whole-site or hosted-matrix acceptance.

On **2026-10-03**, #27 adds the public
`from_feature_inventory()`, `get_rigid_feature_placements()` and
`summarize_rigid_consensus()` tools. Native consensus calls the placement tool;
cached queries avoid molecular reads, explicit proposals remain selectable and
saved summaries add no scientific credit. The [modular cookbook recipe](../docs/content/cookbook/modular_rigid_tools.md)
executed all three blocks. The complete scientific suite passed **225 tests**
on Python 3.14.7 in 194.15 s using the installed development environment's
providers without PYTHONPATH overrides; the earlier controlled Python 3.13 run
passed 225 in 218.11 s. These durations use different providers and are not an
interpreter performance comparison. The two previously described warnings remain.

The workspace now uses `molsyssuite@uibcdf_3.14`. Ordinary no-dependency editable
installation succeeds with metadata `>=3.11,<3.15`. The relevant published #23
adoption changes are incorporated across CI, recovery, recipes and installed
qualification, preserving the scientific changes. Nine focused CI/recovery/
reporting tests passed after incorporation. Public-delivery qualification remains
with #23; earlier hosted matrix evidence does not certify this scientific checkout.

All **12 analytical strategy controls** passed in isolated sequential workers,
with one warmup, three timed calls, stable outputs, identical provider hashes and
separate real Ackredit capture for completed calls. The [retained evidence](evidence/README.md)
and [comparison contract](rigid_strategy_comparison.md) record costs and limitations.
The warped square produces zero models from maximal mappings and 16 three-site
alternatives from triplets. Same-domain RMSD controls protect the objective
distinction; those baseline calls execute no G3PS stage. The strict isolated cookbook build passed
with the existing 3.13 Sphinx tools because Sphinx is absent from the 3.14 runtime
environment. This is neither whole-site nor biological acceptance.

On **2026-10-03**, #28 adds [G3PS seed-stage tools](ranked_seed_workflow.md):
`get_feature_pair_dissimilarities()` compares typed distance environments and
`rank_rigid_feature_correspondences()` ranks supplied triplets. The named
ranked_triplet_seeds consumer composes them with existing proposals, MolSysMT
placement and consensus. Default methods are preserved. All seeds retain the
original triplet family; a finite n_seeds records scientific selection, rather
than avoiding an exhausted computation budget. A real-provider reflected typed
tetrahedron proves that one selected seed can miss an existing four-feature fit.
Ackredit credits the adapted G3PS section 2.2.1 and actual SciPy assignment,
with excluded refinement/rescue stages identified in the citation context.

All **22 new controls** passed, including an independent permutation oracle;
the complete scientific suite passed **248 tests** in 209.61 s on Python 3.14.7
using the installed environment providers without PYTHONPATH overrides. The
same two existing warnings remain. The new cookbook executed **four blocks**,
and the isolated strict Sphinx build passed with the existing 3.13 documentation
tools. Index/reporting guards, Ruff and whitespace checks also passed. A controlled
comparison passed all 14 controls, including the intentional baseline budget
failure and ranked selection false negative. Stable outputs, matching worker
source/extension hashes, timings and real citations are retained in
[the evidence archive](evidence/README.md) and the owning workflow. No complete
G3PS, biological, hosted-matrix or public-package acceptance is established.

On **2026-10-03**, #29 delivers [public greedy refinement](rigid_refinement_workflow.md)
and explicit-pair geometric evaluation, shared with ordinary placement. Both
final and each_step angular policies remain available; their counterexamples
favor different policies. Best fully evaluated accepted checkpoints are preserved.
Consensus selects refinement explicitly and summaries count every initial/trial
fit against the remaining global allowance. Actual Ackredit records G3PS section
2.2.2 with the executed policy and excluded rescue/fitting stages.

The complete suite passed **274 tests** in 246.00 s on Python 3.14.7, including
**26 new controls**, with the same two existing warnings. The recipe executed
**five blocks** and the isolated strict Sphinx build passed with existing 3.13
documentation tooling. All **six scientific policy comparisons** passed with
stable traces, unchanged source hashes and real citation capture; their
[retained evidence](evidence/README.md) is a count comparison, not a timing or
memory benchmark. No full-G3PS, biological or public-delivery claim is added.

The expanded refinement validation now passes **22 workload controls**, bringing
the full suite to **296 tests** in 282.81 s on Python 3.14.7 with the same two
known warnings. Eleven workloads vary seeds, angular/spatial tolerances, mixed
classical families, reflection and six/twelve-donor 3D arrangements. All **22
runtime/memory comparisons** passed with one warmup, three timed calls and a
separate real attributed call, stable traces, unchanged inputs/provider sources
and identical worker source/extension identities. The
[measured table and contract](rigid_refinement_workflow.md#measured-expanded-controls-python-3147)
record coverage beside fits, timing and scoped worker RSS. The new retained
archive supplements the original count-only comparison. Both policies remain
available; no universal winner or biological claim is added. Cookbook rendering
passes with the existing 3.13 documentation tooling.

Issue `#30` now owns [prepared real-ligand CCD controls](prepared_ccd_validation.md).
Untouched ideal EST/DES SDFs have source URLs and checksums, and explicit
MolSysMT preparation preserves atom/hydrogen identity, declared stereo/charge,
connectivity and coordinates. Native input recognition retains its missing
aromatic-metadata rejection; the public sanitizing conversion supplies a ready
reference system. Twenty-three new guards bring the full suite to **319 tests**
in 346.44 s on Python 3.14.7 with the same two known warnings. Both refinement
policies recover the selected 5/6 self features. Public consensus and prepared
frame screening work with these real chemical components; three declared
cross-ligand hypothesis choices have different outcomes. All **12 scientific
comparisons** pass with attribution-independent science, preserved inputs,
unchanged sources and actual whole-workflow resource/method citations. Four
new cookbook blocks execute and strict rendering passes with 3.13 tooling.
This retained evidence is count-only and uses ideal reference coordinates;
experimental receptor/preparation, conformer-energy and biological acceptance
remain separate gates.

The observed 1QKU EST ligand now consumes the provider's public chemical-template
assessment/application tools under #22. The frozen MolSysMT-curated artifact
preserves 20 heavy-atom identities and deposited coordinates. The selected
acceptor/aromatic hypothesis has three essential sites; self-placement,
displacement, normal-sign/orthogonal-normal and molecular/query persistence
controls pass. Eight new guards cover preparation, failure, units and actual
Ackredit input/analysis references. The complete suite passes **327 tests** in
333.34 s on Python 3.14.7 with the same two known warnings. Three cookbook blocks
execute on Python 3.14,
with strict isolated rendering using the existing 3.13 tooling. Both host-tracking
profiles produce identical science; full evidence and actual bibliography are
retained in [the evidence archive](evidence/README.md). Stored H counts do not
provide donor geometry; #300 remains the provider's fixed-state H-placement gate.
Receptor, biological and historical OpenMM derivation acceptance remain open.

The next observed-ligand slice consumes the resolved MolSysMT #300 fixed-state
RDKit operation. It adds 24 H to the declared EST state, preserving the 20 observed
heavy-atom identities/coordinates, and returns 44 atoms/47 bonds with two indexed
directional donors. The five essential donor/acceptor/aromatic sites pass self,
position/normal/direction, heavy-only missing-geometry and persistence controls.
Both rigid angular policies recover all five matches in three fits. The expanded
copy's B-factor drop is explicit; original source annotations remain available.
No environment or energy refinement occurs.

The independent eligibility defect under #31 was found and corrected: numerical
mean-centering could treat co-located features as non-collinear at a shifted origin.
Six public-proposal controls now reject those anchors and retain valid identities.
Eleven donor-route guards bring the complete suite to **344 passing tests** in
348.54 s on Python 3.14.7. Six warnings comprise the two existing warnings and four
expected B-factor-drop diagnostics. All 25 focused controls and five new cookbook
blocks pass; strict rendering uses the existing 3.13 tools. Actual bounded Ackredit
captures and identical tracking-independent science are retained in the seventh
evidence archive. Original archives remain unchanged. The provider's legacy session
role/context omission is handed to its existing #27 integration theme; the native
H report retains its original roles/versions. Receptor readiness, environmental
H orientation and biological acceptance remain open under #22.

The observed receptor audit now consumes the resolved MolSysMT #217/#218 public
diagnostics. Label-chain A has 1,990 atoms and 250 groups: 247 assessed and three
heavy-incomplete groups. All 12/19/23 residues in 0.4/0.5/0.6 nm observed-ligand
shells have no reported heavy gap, but still lack complete declared chemistry.
Receptor-only recognition and two full-source detector calls remain genuinely
blocked, with original diagnostics and unevaluated counts. No preparation,
protonation, ligand reinsertion or biological result is inferred. This locates
the next provider requirement in #298: reusable residue/polymer/terminal chemical
assignment, explicit states, inter-group coverage, conflicts and source maps.

Eight new guards bring the complete suite to **352 passing tests** in 376.12 s
on Python 3.14.7, with the same six warnings. Twenty-seven focused receptor/
template/H controls and the final eight receptor guards pass. Three new cookbook
blocks execute on 3.14, and strict isolated rendering passes with existing 3.13
tools. Ruff and offline reporting/index/whitespace checks pass. Actual observed-
data-only Ackredit capture, source preservation and tracking-independent science
are retained in the eighth archive; all seven earlier original archives verify.
No runtime/memory is measured. The library remains installed editable in
`molsyssuite@uibcdf_3.14`; receptor/biological acceptance and review remain open.

The public `get_excluded_volume_sites()` builder under #32 now constructs
independent Sphere constraints from cached native heavy-atom inventories. It
performs no molecular access, enforces explicit uniform radius choices and
retains source correspondence, detached geometry/report data and actual producer
versions independent of optional attribution. Composition reuses public query
methods and the existing strictly-inside heavy-center veto, with no positive
fit weight. Molecular geometry/selection/physical radii remain MolSysMT's domain.

Twenty-two constructor and four observed controls pass. The 153 heavy atoms in
the 19-residue receptor shell yield 153 spheres. A 0.1 nm choice admits observed
EST; a controlled O3-to-OE2 translation is vetoed by one clash while retaining
five positive matches. A 0.35 nm choice vetoes the reference with 12 clashes.
The broad 0.4 nm positive radius isolates this analytical effect; neither radius
is physically or biologically validated. Both alternatives remain explicit.
Native query persistence and source/ligand preservation pass. Receptor chemistry
and successful interaction recognition remain under MolSysMT #298/#22.

The complete suite passes **378 tests in 473.81 s** on Python 3.14.7 in the
confirmed editable `molsyssuite@uibcdf_3.14` environment. Eight warnings are the
six previous warnings plus two expected B-factor drops from the new H-prepared
controls. The final 26 focused controls also pass after adding producer versions
to construction reports independent of optional tracking. Three cookbook blocks
execute on 3.14 and strict isolated rendering passes with existing 3.13 tooling;
Ruff and offline reporting/index/whitespace checks pass. Both driver profiles
preserve science and producer/input identities; the enabled capture retains
15 items/39 uses, including three actually used input datasets. No G3PS or receptor
interaction detector runs. The ninth original evidence archive is retained and
all eight earlier archives verify. No runtime/memory is measured. Review and
public dependency qualification remain open.

The native [ionic observation continuation](ionic_interaction_workflow.md) under
#33 now constructs positive/negative spheres through the shared public feature
inventory. Whole participant membership and geometry membership remain separate;
compound centers, state, actual charge and source geometry mapping are retained.
Repeated contacts aggregate into one site. Existing pose evaluation, persistence
and the independent public exclusion builder compose without a new screening
implementation. Molecular recognition/detection/centroid calculation remain in
MolSysMT; incompatible definitions, cut centers and nonzero images are rejected.

Twenty-four ionic controls bring the complete local suite to **402 passing tests
in 401.75 s** on Python 3.14.7, with the same eight warnings. The expanded 77-test
set passes in 46.14 s. All three cookbook blocks execute under 3.14; strict
isolated rendering passes with existing 3.13 tools. Ruff, reporting/index, three
offline reporting tests and whitespace checks pass. The editable installation
in `molsyssuite@uibcdf_3.14` is confirmed without a PYTHONPATH override.

The driver retains atomic/carboxylate/guanidinium controls in both ligand roles:
six queries and 18 pose evaluations per tracking profile, all reference/round-trip
positives at fit one and displacement negatives at zero. Both profiles preserve
scientific results, coordinates and producer sources. Enabled capture records
9 items/18 uses, without a named ionic-criterion paper; cached detector origin
retains its original bibliography without a new detection claim. The tenth
original archive is retained and all earlier archives verify. No biological or
runtime/memory claim follows. Native aromatic interaction construction remains
the next observed-complex extension; receptor preparation remains with MolSysMT.

The native [aromatic observation continuation](aromatic_interaction_workflow.md)
under #34 now converts pi-pi/cation-pi observations from seven declared profiles.
It reuses public feature inventory construction and the existing placed-pose
evaluator; exact ring membership and explicit singleton-to-compound cation
mapping preserve original roles, charges and observation criteria. The query
geometry remains the shared classical contract, distinct from detector planes
and all-atom cation points. Undefined diagnostic quantities persist through the
supported sealed PyUnitWizard record encoding (#35); site geometry remains finite.

The focused 97-test run passes in 59.37 s on Python 3.14.7. Three cookbook blocks
execute on 3.14 and strict isolated cookbook rendering passes with existing 3.13
tooling. The driver retains 14 case/profile combinations, 28 successful queries
and 84 pose evaluations per tracking profile, plus a separately retained strict
compound-cation conversion failure. Source atom identity, chemical state and
coordinates, as well as producer source hashes, are unchanged. Tracking off/on
preserves science with 6 items/11 uses and 14 items/30 uses respectively, including
the provider-declared method references where actually used. The eleventh original
archive is retained; all ten earlier originals verify. These controls establish
no biological accuracy, universal fused-ring mapping or performance ranking.

The complete local suite now passes **444 tests in 436.36 s** on Python 3.14.7
with the same eight known warnings (six structural B-factor drop controls, one
optional tracking failure and one legacy unit warning). Ruff, reporting indexes,
three offline reporting tests and whitespace checks pass. The editable
`molsyssuite@uibcdf_3.14` installation is confirmed without a PYTHONPATH override.
Review and public dependency qualification remain open; receptor preparation
continues under MolSysMT #298. Combining multiple interaction families in a
prepared complex is a natural next classical composition step.

## Joint native interaction composition (2026-10-04)

The [composition continuation](interaction_composition_workflow.md) under #36
provides independent public `compose_pharmacophores()` and
`from_interaction_collection()`. The latter calls the existing native adapter
and standalone composer; the dispatcher exposes `interaction-collection`.
Default native participant reuse preserves one compatible constraint/weight and
all labeled observations. Generic `keep` remains available. Source/constraint
conflicts raise without silent averaging, weight inflation or partial hypotheses.
Copies and component snapshots are independent; no molecular access occurs during
cached model composition. Molecular operations remain in MolSysMT.

The driver passes actual five-family detection, an alternative pi-pi profile and
a covered-empty ionic analysis: seven analyses, 23 observations and nine reused
constraints, compared with eleven explicit kept constraints. Both tracking
profiles retain nine independent pose/persistence/veto evaluations; producer
sources, declared atom identity/state/coordinates and metadata remain unchanged.
Real capture retains 5 items/21 uses off and 13 items/50 uses on, including
actually reached provider references. The twelfth original evidence artifact is
retained. Three cookbook blocks execute on Python 3.14.7 and strict isolated
rendering passes with existing Python 3.13 tooling. These disconnected controls
are not a chemical ligand or biological binding complex.

The corrected complete local tree passes **476 tests in 452.91 s** on Python
3.14.7, including all 32 composition controls, with the same eight known warnings.
Ruff, generated indexes, three offline reporting tests, whitespace checks and all
twelve original archive hashes pass. The editable `molsyssuite@uibcdf_3.14`
installation is confirmed without a PYTHONPATH override. Review/incorporation,
public dependency delivery and biological complex acceptance remain separate.

## Complete CCD interaction continuation (2026-10-04)

The [complete CCD continuation](ccd_interaction_workflow.md) under #37 applies
the existing public observation, collection/composition and pose-evaluation tools
to full EST/DES graphs in two explicit rigid-copy placements. Public MolSysMT
owns source preparation, shared feature geometry, translation, merge and component
projection. Both full molecule roles preserve states, explicit H, atom identity,
bonds, coordinates and source bytes. Six named analyses retain neutral empty
ionic/cation-pi families and original alternative ring-profile evidence. No new
product API, molecular reconstruction or borrowed placement/composition citation
is introduced.

The four pairs produce 10/11 EST and 16/18 DES sites in either role. Positive
references fit one; displacement gives zero. Keep and participant reuse remain
explicit different hypotheses. Donor-H negatives fail one directional essential
while the unchanged acceptor role passes. DES ring-offset retains its actual
single .05 nm exclusion clash in both roles despite full positive fit; the radius
is not changed to force acceptance. These designed ideal-coordinate pairs are
not protein complexes or biological benchmarks.

Thirty controls pass on Python 3.14.7 in 129.47 s. Concurrent live MolSysMT edits
invalidate the source-stability gate of the initial driver runs despite passing
science. A complete-file-verified temporary MolSysMT package snapshot therefore
qualifies the definitive evidence; installed version metadata alone does not
identify its dirty origin. The same 30 controls pass there in 137.39 s.
PharmacophoreMT remains the editable package in `molsyssuite@uibcdf_3.14`.

The definitive driver passes eight primary role hypotheses and 48 pose evaluations
per tracking profile, with identical science, unchanged producer sources,
input fingerprints and metadata. Actual captures retain 9 items/28 uses off and
17 items/57 uses on, including consumed CCD data and reached method references.
The thirteenth original evidence artifact and summary are retained; all thirteen
archives verify. Three cookbook blocks execute on 3.14 and strict isolated cookbook
rendering passes with existing Python 3.13 tooling. Provider source identity and
scope are recorded in the [evidence index](evidence/README.md).

The complete live-checkout suite passes **506 tests in 634.91 s** with the same
eight known warnings. Its explicit source audit fails because MolSysMT changed
during the run; the supplemental audit/log preserve this result, which is not
fixed-provider qualification. The definitive driver and 30 focused controls use
the independently verified stable snapshot. Ruff, generated indexes, three offline
reporting tests and whitespace checks pass. Review/incorporation, public dependency
delivery and the actual ERalpha complex acceptance gate under MolSysMT #298 remain
open.

The next classical steps also include provider-supported conformer preparation and
ligand/complex consensus. Prepared multi-conformer screening is delivered locally;
conformer and chemical-state generation remain the molecular provider's
responsibility.
Reference-anchored consensus over prepared aligned ligands is delivered locally.
Bounded aligned clique discovery with alternative jointly supported models is
also delivered locally. The first explicit-pivot rigid unaligned workflow is now
delivered with two baseline proposal families and explicit ranked-triplet selection.
Review these contracts and compare tolerance-valid coverage and resource costs
before expanding to translation rescue or prepared
multi-conformer consensus. Global continuous/multiple-pivot alignment and geometric
deduplication need independently declared methods and controls.
Structure-based hypotheses need the TopOMT/MolSysMT boundary. Direct molecular
operations remaining in legacy code must be migrated to MolSysMT; missing
provider capabilities must be tracked there, never copied here.

The [roadmap](roadmap.md) gives the current implementation order.
[Growth contracts](extensible_modeling_contracts.md) record the accepted separation
of scientific method, compute backend and execution plan. Dynamic, specialized
and generative approaches remain objectives after the classical acceptance gate.

## Cached-model curation continuation (2026-10-04)

The [curation contract](pharmacophore_curation_workflow.md) under #38 introduces
public local-site selection, independent copying, extraction and explicit
constraint editing. Class setters delegate to the editor. Molecular-system links
remain references; no molecular query, copy or transformation runs in curation.
Extraction/editing retain complete native source snapshots, mappings and original
observations/bibliography, invalidate score, and nest earlier changes. Copying
preserves score. Atomic input validation, independent shape geometry, actual
radius versus Gaussian width and essential/weight/exclusion meanings are guarded.

The focused run passes 54 tests in 42.68 s on Python 3.14.7, including 36 new
curation controls. Three cookbook blocks execute with stable recorded producer
sources. Strict isolated rendering passes with existing Python 3.13 documentation
tooling. The fourteenth original evidence artifact retains complete original and
edited models, seven evaluations, actual capture, original logs and the exact
executed runner. Pure cached steps add no new citation use; length editing
captures two items/two uses, with original bibliography retained in history.

Native YAML controls additionally exposed NumPy literal strings emitted as Python
objects. The #25 correction normalizes builtin text at the shared portable
boundary and uses safe YAML output, preserving literal content and quantity
objects independently. No existing saved record is rewritten. These are local
curation controls, not biological validation, automatic weight fitting or a
performance ranking. Bounded native participant reuse precedes curation; generic
keep composition retains explicit curated alternatives.

The complete tree passes **542 tests in 730.39 s** on Python 3.14.7, with eight
existing warnings. Its explicit source audit fails because Ackredit changes
during the run; PharmacophoreMT, the verified MolSysMT snapshot and PyUnitWizard
remain unchanged. This successful test run is not four-provider fixed-source
qualification. The original failed audit and passing test log are retained
separately from the stable cookbook result. All fourteen original archives verify;
the editable installation is confirmed without a PYTHONPATH override. Review,
public distribution and biological acceptance remain separate.

## Publication integration checkpoint (2026-10-06)

The accumulated native modeling/screening/attribution/curation work, ERalpha
pilot, cookbook, frozen inputs and fourteen original evidence archives are
integrated with the sixteen intervening upstream governance commits. The current
canonical guides, suite-policy caller and Python 3.11–3.14 contract are preserved.
Git attributes retain checksum-qualified input/evidence bytes, including original
logs; all fourteen archives and original input/evidence bytes verify unchanged.

Owner adoption of #39 separates invariant chemistry from appended operation
history and strengthens the original-source guard. Current MolSysMT #346 query
vocabulary is consumed through public between_selections; detector selection
semantics and saved scientific metadata are unchanged. CI source pins identify
the current providers selected for native integration without bypassing metadata.

The three ERalpha pilot modules pass 27 controls in the initial selection, which
also exposes ten curation setup errors from the retired query name. After its
migration, all 164 affected interaction/composition/CCD/curation controls pass
in 231.78 s. The strengthened repeat-H guard and six CI controls pass seven
tests in 7.26 s. Ruff, reporting/index and whitespace checks pass. Execution uses
normal editable installation in molsyssuite@uibcdf_3.14 without PYTHONPATH overrides.
The original logs and provider/file identities are retained in
`evidence/publication_20261006.json`. Historical full-suite results remain dated;
today's selected checks do not certify the new full hosted matrix.

Whole-workspace pip check reports unrelated installed auxiliary-package conflicts,
handed to the owning shared workspace in MolSysSuite #52. Its
[receipt](https://github.com/uibcdf/molsyssuite/issues/52#issuecomment-6026983063)
does not identify a PharmacophoreMT dependency failure or qualify the canonical
environment recipe. Hosted exact-head evidence remains tracked by #9/#23;
public package delivery and biological acceptance remain separate.

## Working references

Read the repository tooling guides and [API standards](api_design_standards.md).
Use the active issue-backed queues for current work and the reporting protocol
for acceptance/archival. The older detailed classical specification retains a
backlog catalog; its local chemistry/automatic preparation directions are
superseded by the current ownership contracts.
