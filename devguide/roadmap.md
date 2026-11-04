# Strategic Roadmap

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

## Cross-cutting audit priorities — 2026-11-04

The [evidence and verification addendum](audit_20261104_review.md) classifies
the 17 areas by observed status and impact, links method-level evidence and
defines operational completion checks and dependencies. It preserves the initial
assessment and does not convert proposed studies into completed validation.

See the [architectural, scientific and product audit](audit_20261104.md) for the
ordered 17-area improvement plan and completion criteria. Address #73 first,
then coordinate API/persistence/installed reproducibility with scientific study
design. Sensitivity analysis must preserve an independent final evaluation set;
optimization follows resource measurements. The list is a planning assessment,
not a declaration that every area is defective or already implemented. Earlier
dated milestones and their evidence remain preserved below.

## Native geometry contracts received; native loader options next — 2026-11-04

#6's [new receipt](evidence/native_geometry_contract_receiving_20261104_summary.json) qualifies definition-owned Point/Sphere/
SphereAndVector/Disk constructor contracts with real public ArgDigest 0.17.0.
All 1093 full-source test items pass; four owner guards fail original production
code, while 40 original behavior controls already pass. Two separate 85-control
runs pass with public/development providers. Exact dirty overlays and all attempts
remain retained; source/native/metadata identities stay stable.

Closed signatures require no invented domain/alias declarations. Metadata,
recipe, generated ordinary environments and both exact CI source routes now
require/support ArgDigest >=0.17.0; other pins and molecular operations are
unchanged. No shared prefix/provider edit or clean installed/all-platform claim.

**Next: #73 native loader option admission**, then #6's method-dependent model
forwarding and actual aliases. The loader reproducer confirms silent unknown-
keyword loss for native JSON/YAML. MolSysMT owns molecular loading and option
contracts. #6 stays partial; ArgDigest #46 owns optional-Beartype diagnostics.
#41/#19/#22/#23/#10/#9/#82/#60/#66 keep their existing gates; no new release or
addon priority. See [checkpoint](checkpoint.md) and [boundaries](support_library_boundaries.md).

## Support review delivers diagnostic fix; scoped argument contracts next — 2026-11-04

#6's [receipt](evidence/support_boundary_review_20261104_summary.json) retains
five failing original guards and 44 passing final attribution/contract controls.
#72 fixes hidden host diagnostic-emission failures while preserving science and
original errors; public SMonitor remains the normal emitter. Qualified source/
native/input/metadata identities remain stable. Conditional unit-form/persistence
probes and 8 environment/22 distribution controls pass; no full scientific suite
or installed/public/central adoption claim. The optional Beartype diagnostic
observation is handed to ArgDigest #46; no provider implementation is copied.

#6 stays **partial**: modern explicit function/domain/alias contracts are not yet
configured. Next adopt those ArgDigest declarations for a bounded native geometry
family, preserving inputs, quantities, diagnostics, compatibility and skip behavior.
Keep current supported tool pins and actual operator installations distinct from
guide delivery. Public/all-minor provider receiving, #19/#23/#10 delivery, #22 wider
science, #41 public/legacy migration (review 2026-11-11), hosted #9, workspace #82,
#60 and #66 retain their gates. Molecular operations remain MolSysMT-owned.
Addon/new release defer. See [checkpoint](checkpoint.md).

## Prepared ERalpha fragment accepted within scope; adoption next — 2026-11-04

#22's [receipt](evidence/eralpha_acceptance_20261104_summary.json) accepts its
declared 304–550/EST source/scientific workflow at clean b2b9528: 17 fresh controls,
the unchanged two-profile original CLI, all three recipe blocks, supplementary
tracking-independent diagnosis and strict isolated rendering pass. Loaded
source/native identities stay stable, but example distribution lookups switch to
four stale canonical records: the full-identity wrapper failure remains under #82. Four warnings are expected attribute drops. Current original native
artifacts, full outputs and original data/history/maps stay checksum-qualified.
Twelve observed hydrophobic contacts and five ligand-reference hypotheses retain
distinct roles; direction/normal/weight/exclusion and persistence controls pass.
No library/test/input/provider change, new full suite or biological claim.

**#22 stays partial/open** for full receptor/excluded residues, peptide stereo,
environmental preparation and biological acceptance. MolSysMT #323/#350 remain
open; the client uses public molecular tools and keeps the rejected-intersection
arithmetic solely as an independent fixed-case test oracle. No missing #66
binding method or physical cutoff preference is invented.

Next **#6 support-library/tool adoption review** should consolidate current
boundaries and actual evidence, then name concrete remaining qualification work.
Source acceptance cannot promote central states, public/provider floors or exact
installed/platform artifacts. #19 delivery/#23/#10, hosted #9, workspace #82 and
#41 public/legacy receiving (review 2026-11-11) remain separate. #60 keeps its own
consumer gate. Addon/new release defer. See [checkpoint](checkpoint.md).

## Attribution source/API accepted; real prepared case next — 2026-11-04

#19's [receipt](evidence/attribution_acceptance_20261104_summary.json) accepts the
source/API contract at clean 213df11: 39 fresh controls, off/on session/reuse/
branch/failure capsules, five saved-report formats, fresh no-engine/no-credit
reader, two unchanged examples and strict isolated rendering pass with stable
identities. Ten warnings are intentional failure controls. Cookbook prose now
distinguishes reached clique/G3PS stages from design-only papers. No runtime/test/
provider change or new full suite. Ackredit owns capture/reporting and MolSysMT
owns molecular work.

**#19 remains partial/open** for delivered PHMT/all-minor public-provider receiving
under #10/#23. The old public-provider receipt is verified as historical evidence;
current controlled source does not establish recommended public 0.12.1 receiving,
an installation extra, a new minimum floor or public/platform/hosted success.

Next review **#22's bounded prepared ERalpha workflow**: original data/preparation
and maps, observed versus hypothesized sites, independent geometry/exclusions,
persistence, attribution and current-provider guards/recipe. Preserve its remaining
full-receptor/preparation/biological gates and #66's missing endpoint methods;
analytical workflow controls are not biological enrichment. #41 public/legacy
receiving stays partial (review 2026-11-11), #60 keeps its concrete-consumer scope,
hosted #9 and workspace #82 remain separate. Addon/new release defer.
See [checkpoint](checkpoint.md).

## Observed placed-pose slice accepted; attribution review next — 2026-11-03

#13 is resolved with its [receipt](evidence/placed_pose_acceptance_20261103_summary.json).
At clean 1eea04d, 99 fresh controls, off/on actual-observation/placed capsules,
six round trips per profile, the unchanged example and strict isolated rendering
pass with stable identities. Repeated participant evidence collapses into one site;
source/frame/direction, essential/weight/assignment/exclusion and failed-versus-
negative accounting remain explicit. A real-provider declared-profile mismatch
confirms that observation roles do not guarantee SMARTS candidate acceptance.
Source domains/observations remain unchanged. Public MolSysMT owns molecular work.
No library/test/provider change, new full suite or biology/public-delivery claim.

Next review **#19 optional attribution**: activation and application sessions,
repeated detached references, reached branches, failure isolation and original
scientific errors, saved readers/reporting and cookbook. Use its existing public
receiving receipt; delivered-package/all-minor public qualification remains pending
unless independently verified. #22 pilot/#66 endpoint methods stay separate.
#41 public/floor/installed receiving and final legacy retirement remain partial
(review 2026-11-11); #60 keeps its own gate. Hosted #9, installed/public/platform
#23/#10 and workspace #82 remain independent. Addon/new release defer.
See [checkpoint](checkpoint.md).

## Reference construction accepted; observed placed poses next — 2026-11-03

#14 is resolved with its [receipt](evidence/reference_ligand_acceptance_20261103_summary.json).
At clean a3cd1f5, 53 fresh controls, off/on six-family/15-site capsules, JSON/YAML,
the unchanged example and strict isolated rendering pass with stable identities.
Known group centers/signs, donor direction, aromatic axis invariance, essential
constraints and visible failures retain source/provenance and physical units.
Initial one-off cross-unit exactness and temporary-renderer toctree failures are
retained and corrected without library/test/provider changes. Public MolSysMT
owns molecular work; PHMT owns pharmacophoric constraints and cached matching.
No new full suite, biology or public/installed closure is claimed.

Next accept **#13 observed-interaction extraction and already-placed pose evaluation**:
actual public MolSysMT observations, selected frame/state/source mappings, essential
and one-to-one constraints, exclusions, direction, shared rigid/unit invariance,
visible failures and historical entry-point migration. This does not introduce
implicit pose search or molecular preparation. Then accept #19 attribution.
#41 supported-public/floor/installed receiving and final legacy retirement stay
partial (review 2026-11-11); #60/#66 keep their own gates. Hosted #9,
installed/public/platform #23/#10 and workspace #82 remain separate. Addon/new
release defer. See [checkpoint](checkpoint.md).

## Rigid pose-search acceptance complete; reference construction next — 2026-11-03

#15 is resolved with its [receipt](evidence/rigid_search_acceptance_20261103_summary.json).
At clean 1e00aca, 68 fresh controls, off/on prepared rigid/termination/failure
capsules, two examples and strict isolated rendering pass with stable identities.
Ten warnings are intentional attribution-failure controls. No runtime/test/provider
change or new full suite is claimed. Public MolSysMT owns molecular work.

Valid coverage-one hits can prove the compatibility maximum despite incomplete
triplet enumeration, retaining the incomplete flag. A vetoed fit at one cannot;
unproven truncation is a PHMT-E105-caused failure. Explicit seeded-hit no-pose
negatives retain binary zero and no fabricated pose. Retrospective accounting
preserves classes, duplicate/generator indices and unscored failures. Native
persistence/unit and source-domain controls pass. Neither criterion guarantees
continuous/global poses or biological activity; #63 scoring consent stays explicit.

Next accept **#14 native reference-ligand construction**, independently reviewing
shared six-family chemistry/geometry, source/group mappings, generated constraints,
placed matching/persistence and its example. Then accept #13's observation/placed-
pose and #19's attribution contracts. Current MolSysMT tools support this work.
#41 public/floor/installed migration and legacy retirement remain partial, review
2026-11-11; #60/#66 retain their scopes. Hosted #9, installed/public/platform #23/#10
and workspace #82 remain separate; addon/new release defer. See [checkpoint](checkpoint.md).

## Ranked-seed acceptance complete; prepared rigid search next — 2026-11-03

#28 is resolved with its [receipt](evidence/ranked_seed_acceptance_20261103_summary.json).
At clean 9731e05, 82 fresh controls, off/on selection capsules (12 pose checks/two
round trips each), four unchanged cookbook blocks and strict isolated staged
rendering pass with stable identities. Recipe prose now links available refinement.
Molecular operations stay in MolSysMT; typed neighborhoods/selection remain in PHMT.

Both all-seed families preserve 16 proposals/eight accepted mappings. Selecting one
omits 15 and misses the known four-feature match. The original seven-case/two-
strategy driver runs after tests/docs finish: 14 isolated sequential workers,
one warmup/three timed calls/separate citation, all expectations/stability checks
pass (eight completed/five empty/one failed PHMT-E107). All 42 samples and honest
whole-worker RSS remain descriptive; different coverage/alternatives establish no
equivalent-recall speedup or default selection limit. No runtime/test/provider
change or new full suite is claimed. #29 refinement is already resolved.

Next accept **#15 prepared rigid pose search**: public correspondence/alignment
composition, search completion, legitimate maximum-coverage early stops, explicit
failed-search accounting and retrospective use. It can use current MolSysMT tools.
Then consolidate the remaining reference/placed-pose/attribution acceptance records
under #14/#13/#19, keeping actual biological pilot/endpoint gates independent.
#41 public/floor/installed receiving and legacy retirement remain partial, review
2026-11-11; #60/#66 retain their scopes. Hosted #9, installed/public/platform #23/#10
and workspace #82 remain separate; addon/new release defer. See [checkpoint](checkpoint.md).

## Modular strategy comparison accepted; ranked seeds next — 2026-11-03

#27 is resolved with its [receipt](evidence/rigid_comparison_acceptance_20261103_summary.json).
At clean 50776a1, 23 fresh controls, off/on same-domain objective capsules (nine pose
checks/two round trips each), three cookbook blocks and strict isolated rendering
pass. Generic RMSD and all molecular operations use MolSysMT. The corrected one-off
comparison excludes only direct/inherited bibliography; original attempts remain.

The original six-case/two-family comparison runs after all owned tests/docs end:
12 sequential isolated workers, one warmup/three measured calls/separate citation
call; all expectations and output stability checks pass. Five completed, five empty
and two expected failed records stay distinct. Source/native/metadata identities
remain stable. Warped-square association has zero models, triplets sixteen three-
site alternatives; current timings/RSS describe these different workloads and
establish no universal ranking or default change. No runtime/test/provider change
or new full suite is claimed.

Next accept **#28 ranked triplet seeds**: typed-neighborhood comparison, independent
assignment oracles, all-seed equivalence, finite-selection misses, allocation bounds,
consumer composition and reached adapted-stage credit. This is the G3PS seed stage;
other refinement/rescue/exclusion contracts retain their separate scopes.
#41 public/floor/installed migration and legacy retirement remain partial, review
2026-11-11. #60 independent-copy receiving and #66's original binding methods retain
their scopes. Hosted #9, installed/public/platform #23/#10 and workspace #82 remain
separate. Addon/new release stay deferred. See [checkpoint](checkpoint.md).

## Rigid unaligned source/API acceptance complete; comparison next — 2026-11-03

#26 is resolved with its [receipt](evidence/rigid_consensus_acceptance_20261103_summary.json):
95 fresh controls at clean 0bab03a, zero failures/errors/skips. Five analytical
cases under both families and host-tracking modes preserve proper rigid recovery,
reflection rejection, six symmetric alternatives, empty completion and failed
budgets. Per profile, 20 models pass 112 pose evaluations and eight JSON/YAML round
trips. Unplaced nonempty sources retain their original evidence and denominator.
Both cookbook blocks and strict isolated rendering pass; source/native/metadata
identities and molecular domains remain stable. Molecular operations use MolSysMT;
no runtime/test/input/provider change or new full-suite claim follows.

Next accept **#27 modular tools and reproducible strategy comparison**: inspect
its unchanged original opt-in driver and frozen warped-square counterexample,
objective/coverage differences, independent tools, source/input/provider identity,
isolated repeats/timing, memory scope and separate actual credit. Completed-empty
and failed cases must stay distinct; different output families do not establish
a universal speed winner. Ten modular controls passing in #26 are only part of
that independent acceptance. Then review #28's ranked proposal stage separately.

#41 public/floor/installed migration and final legacy retirement remain partial,
review 2026-11-11. #60 independent-copy receiving and #66's four original methods
retain their scopes. Hosted #9, installed/public/platform #23/#10 and workspace #82
remain separate; addon/new release stay deferred. See [checkpoint](checkpoint.md).

## Aligned clique source/API acceptance complete; next rigid consensus — 2026-11-03

#24 is resolved. The [receipt](evidence/aligned_clique_acceptance_20261103_summary.json)
records 60 fresh focused controls at clean 17fb209 (25 clique, 17 aligned, 18
contracts), zero failures/errors/skips. Independent clique/package oracles and
fresh off/on capsules retain absent-first-ligand discovery, ambiguous alternatives,
whole-package support, completed-empty versus failed budgets, six JSON/YAML round
trips and 29 pose evaluations per profile. Source domains and full identities remain
stable. Three cookbook blocks and strict isolated rendering pass. Initial script-only
cross-policy hash failures are retained and diagnosed; no runtime/test/provider
change or new full-suite claim follows. Molecular operations remain MolSysMT-owned.

Next accept **#26 prepared rigid unaligned consensus**: review both correspondence
families, provider-owned proper fits/molecular transforms, post-fit validation,
alternative placements, support including unplaced sources, bounds, persistence,
actual attribution and cookbook. Its explicit pivot and finite proposal families
remain distinct from continuous/global alignment. #24's maximal-site-clique family
is not all chemical patterns or a biological/performance claim.

#41 public/floor/installed migration and final legacy retirement stay partial,
review 2026-11-11. #60 concrete-copy receiving and #66's four original binding methods
retain their scopes. Hosted #9, installed/public/platform #23/#10 and workspace #82
remain separate; addon/new release stay deferred. See [checkpoint](checkpoint.md).

## Reference-anchored aligned method accepted; next clique discovery — 2026-11-03

#21 is resolved. The [receipt](evidence/aligned_reference_acceptance_20261103_summary.json)
verifies reuse of all 17 aligned-consensus controls from the original 418-item
run at code 6a7537b, with exact source/native/helper/test/input/metadata and tracked
tree identity at clean receiving head daae2d2. Fresh off/on capsule execution
retains center/support/dispersion, input domains, failed-versus-negative semantics,
matrix budget, radius-independent support and JSON/YAML outcomes across unit
policies. Eleven pose evaluations per profile, both cookbook blocks and strict
isolated rendering pass. Full identities are stable; no runtime/test/input/
provider changes or new pytest/full-suite execution are claimed.

Next accept **#24 aligned clique consensus**: review reference-independent
maximal-site discovery and alternative jointly supported hypotheses, unique
identities/occurrences, graph/clique budgets, rejection/completion evidence,
persistence and actual attribution plus its cookbook. Its completeness claims
remain distinct from #21's single reference and one chosen pairwise assignment.
All molecular operations remain MolSysMT-owned; PHMT matches/aggregates cached
pharmacophoric sites and retains reference orientations. No generic molecular
or angular averaging tool is copied here.

#41 public/floor/installed migration and final historical arithmetic retirement
stay partial, review 2026-11-11. #60 concrete-copy receiving and #66's four original
binding methods keep their scopes. Hosted #9, installed/public/platform #23/#10
and workspace #82 remain independent. #323/#375/#447 retain provider ownership;
addon/new release stay deferred. See [checkpoint](checkpoint.md).

## Aromatic source/API acceptance complete; next aligned consensus — 2026-11-03

#34 is resolved. The [receipt](evidence/aromatic_acceptance_20261103_summary.json)
verifies that clean receiving head ee257a1 has the exact runtime/helper/test/
driver/workflow trees, loaded sources/native bytes, inputs and metadata of code
6a7537b's original 418-item run, including all 46 aromatic controls. That test
execution is reused, not rerun. Fresh driver execution passes both tracking
profiles, each with seven profiles/14 case combinations/28 queries/84 evaluations,
original scientific outcomes and actual credit. Strict conversion failure remains
a null-score failure; explicit containing-center mapping preserves atomic evidence.
Three cookbook blocks and strict isolated recipe rendering pass. Full identities
remain stable; no runtime/test/input/provider change is needed.

Next accept **#21 reference-anchored aligned consensus**, then **#24 aligned clique
consensus**, each against its own matching/support/orientation/budget/rejection,
persistence and attribution contract plus executable examples. Current qualified
providers support this work. #34/#36/#37 and aggregate tests do not automatically
close those independent methods. Source/API evidence remains separate from
biological accuracy, profile superiority, energies, performance or universal
fused-ring equivalence. Original October/#35 evidence stays unchanged.

#41 supported-public/floor/installed migration and final historical arithmetic
retirement remain partial, review 2026-11-11. #60 concrete-copy receiving and
#66's four original-method inputs keep their scopes. Hosted #9, installed/public
#23/#10 and workspace #82 are independent gates. #323/#375/#447 stay with their
provider owners. Addon/new release remain deferred. See [checkpoint](checkpoint.md).

## Remaining observed donor caller migrated; next aromatic queries — 2026-11-03

#41 source migration now covers the observed H-bond caller as well as
get_features: code 6a7537b shares validation of public MolSysMT vectors, retains
the original chemical profile/ordered pairs/frame, reuses repeated-pair geometry
and seals provider provenance. No available-provider error is replaced locally.
The [receipt](evidence/observed_donor_receiving_20261103_summary.json) retains
418 passing modern controls, 14 passing original-public-payload controls and both
affected driver profiles (composition and complete CCD) with original scientific
outcomes, source preservation and actual credit. Full physical and metadata
identities remain stable in every phase. No provider/native/pin/floor change.

Next accept **#34 aromatic queries** against its independent profile/participant
mapping, geometry, empty/failure/persistence and attribution contract, driver and
cookbook. The source implementation task below is now received. #41 remains
partial only for its supported-public delivery/installed receiving and final
historical arithmetic retirement (review 2026-11-11, LMMV/dprada). Ideal acceptor
models retain #375's separate scientific scope. The original 0.23.0 payload was
byte-verified, but this is not clean ordinary installation or current channel
inventory. No complete new-source full suite, biological or performance claim.

Actual quota failures and initial fixture/parser corrections are retained with
successful reruns. Completed owned build/HTML derivatives alone are retired;
scientific/source/log/config/wheel/provider/native/env resources remain. The
normal owned editable refresh identifies PHMT 0.4.0+62.g6a7537b. #9 hosted and
#23/#10 installed/public gates stay separate; #82 inherited findings stay open.
#60 concrete copy receiving and #66's four original-method inputs retain their
scopes. #323/#447 remain provider-owned. Addon/new release stay deferred.

## Ionic queries accepted; finish the remaining vector caller before aromatic review — 2026-11-03

#33 is resolved: 45 focused controls (24 ionic plus pose/reference regressions),
six queries/18 evaluations in each original tracking profile, three cookbook
blocks and strict isolated recipe rendering pass on clean source 16614ae7.
The [receipt](evidence/ionic_acceptance_20261103_summary.json) retains source/unit/
state maps, provider compound geometry, repeated contacts, original expectations,
negative poses, persistence and actual credit. Full physical and metadata
identities are stable in each phase. No runtime/test/input/provider changes.

The architecture review finds another existing donor-vector caller under #41:
from_interactions' H-bond branch still subtracts molecular donor/H coordinates.
Previous modern-vector receiving qualified get_features, not every caller.
**Next migrate this branch to existing public MolSysMT vectors**, preserving the
observed profile, ordered participants, frames and failure behavior; reuse bounded
validation and retain historical compatibility only for genuine capability absence.
Owner LMMV/dprada, review 2026-11-11. This source work can proceed now; public floor/
legacy retirement and ideal acceptor models remain separate. Then accept #34's
already implemented aromatic mappings against their independent contract.

#60 native-copy receiving remains available for a concrete consumer; #66 needs
the four original binding methods. Hosted gates stay #9, clean installed/public
qualification #23/#10 and inherited workspace findings #82. Prior #32 metadata
mismatches remain unresolved, not relabeled by this stable ionic run. #323/#447
retain provider ownership. Addon/new release remain deferred. See [checkpoint](checkpoint.md).

## Exclusion-sphere acceptance complete; ionic and aromatic queries next — 2026-11-03

#32 is resolved after all 26 owning controls, both original observed-driver
profiles, three cookbook blocks and strict isolated recipe rendering pass on
clean source 25d4107. Original source geometry/chemistry/bytes, source indices,
153 exclusions/19 residues, exact-boundary semantics, one/12-clash vetoes with
fit 1, native persistence and actual attribution remain intact. The [receipt](evidence/exclusion_acceptance_20261103_summary.json)
retains new measured results beside untouched originals. No runtime/test/input/
provider changes are needed. Loaded physical identities remain stable; strict
full/metadata equality is false because lookups switch to older canonical records.
The inherited workspace boundary is explicit, not clean installed qualification.

Next accept **#33 ionic queries**, then **#34 aromatic queries**, using their own
participant/source/frame/state, geometry and weighting, empty/failure,
persistence and attribution contracts plus their driver/cookbook controls.
Current molecular tools support those reviews; #32/#36/#37 results do not close
these independent issues automatically. #44's cached exclusion delegation is
already delivered; the original Oct03 legacy statement is historical.

#41 retains public delivery/installed receiving and its 2026-11-11 review; #60
native-copy receiving is available for a concrete consumer; #66 needs the four
original binding methods. #323/#375/#447 retain provider ownership. Hosted gates
stay #9, installed/public qualification #23/#10 and workspace limitations #82.
Addon/new release remain deferred. See [checkpoint](checkpoint.md).

## Prepared CCD acceptance complete; next exclusions and interaction queries — 2026-11-03

#30 is resolved: 23 owning controls, all 12 driver comparisons with tracking
off/on, four executed cookbook blocks and strict isolated recipe rendering pass
on clean source 54df39ca4956335cf0d408b02a61f73ce97a0a96. Full identities are
stable and original chemistry/bytes, readiness failure, frame accounting and
finite self/cross-ligand outcomes are preserved. The [receipt](evidence/prepared_ccd_acceptance_20261103_summary.json)
retains actual attribution and new measured outputs beside untouched originals.
No runtime, fixture or expectation changes are needed.

Next review **#32 exclusion-sphere construction**, followed by **#33 ionic** and
**#34 aromatic** query acceptance, against each issue's own molecular-source axes,
geometry, empty/failure semantics, detached evidence and actual attribution.
Current public source tools support those reviews. Aggregate passes and #30/#37
closure do not close these independent contracts automatically. Native copy
receiving #60 remains available for a concrete independent-variant consumer.

#41's historical-public vector exception remains partial, review 2026-11-11;
identified public delivery/installed receiving is still needed. #66's four original
binding methods remain an external-input gate. #323/#375/#447 retain provider
ownership. Hosted gates stay #9, clean installed/public qualification #23/#10 and
shared conflicts #82. Addon/new release remain deferred. These CCD controls do not
establish biological prediction, generated conformers or computational performance.

## #41 reviewed; next accept the prepared CCD foundation — 2026-11-03

#41's designated modern-provider source gate passes **165 controls**, zero
failures/errors/skips, with stable physical and metadata identities. Current CI
already has vectors. The [delivery review](molsysmt_feature_receiving.md) finds
GitHub release/tag 0.23.0 still latest; failed official Anaconda metadata queries
leave channel inventory unverified. Keep the bounded historical fallback and
2026-11-11 review until supported public vector delivery and source/installed/
public qualification permit migration. No dependency floor or provider pin change.

| Order | Next result | Boundary |
| --- | --- | --- |
| 1 | #30: review and accept the prepared EST/DES CCD foundation using its own preservation, self/cross-ligand, attribution, driver and cookbook criteria. | Available with controlled providers; #37's workflow evidence supports, but does not replace, this independent review. |
| 2 | #32, then #33/#34: reconcile public exclusion, ionic and aromatic query acceptance. | Preserve original source/frame/state, participant, empty/failure, geometry and attribution contracts. Reuse applicable results without closing from aggregate counts. |
| Provider delivery | #41/#375: identify supported public generic vectors and qualify migration; #23/#10: justified floors and newer-public compatibility. | Existing source delegation is complete; clean installed/public delivery remains unqualified. Acceptor models are separate science. |
| When a consumer needs it | #60: qualify native copies for independent molecular variants. | #121 is delivered; intentional model references remain explicit. |
| External scientific input | #66: receive the four original binding methods through a new authorized lead. | Preserve fixed study rules and prior exposure; no repeated exhausted searches. |

Exact-head hosted gates remain #9; shared dependency conflicts #82. #323/#447
retain provider ownership. Addon and a new release stay deferred. See the
[checkpoint](checkpoint.md) and [dated receipt](evidence/molsysmt_feature_review_20261103_summary.json).

## Composition and full-CCD source/API acceptance complete — 2026-11-03

#36 and #37 now join #38/#17/#29 as reviewed source/API slices. The corrected
cached map/state guard and all 219 coupled controls pass, including 41 composition
and 30 CCD cases. Both original drivers retain their expected scientific results
with tracking off/on, unchanged inputs and actual attribution; all six cookbook
blocks pass. [Composition evidence](evidence/composition_acceptance_20261103_summary.json)
and [CCD evidence](evidence/ccd_interaction_acceptance_20261103_summary.json)
retain exact source/native/input identities and original before/after failures.

The next bounded architecture task is #41's compatibility review by 2026-11-11:
verify supported public generic-vector delivery/receiving before removing the old-
public arithmetic exception or raising a floor. Current source already uses the
provider tool; general molecular geometry remains in MolSysMT, with ideal acceptor
models separate. In parallel #60 can qualify explicit molecular variants against
the already delivered #121 copy contract when needed, preserving intentional model
references. Reconcile adjacent native preparation/interaction/consensus issues
only against their own contracts; do not close them from the aggregate test count.

#66's four original binding methods remain the independent scientific access gate.
Preserve the fixed study and all earlier exposure; no new lead or cohort is
inferred from these analytical controls. #323 environmental H, #375 directions/
delivery and #447 molecular identity/scaffolds retain separate provider ownership.
Exact-head CI stays #9; clean installed/public qualification #23/#10. The prior
1,020-item run belongs to its original producer and is not relabeled as execution
of the new correction. Addon/new release remain deferred. See [checkpoint](checkpoint.md).

## Rigid-refinement accepted; next consolidate complete interaction workflows — 2026-11-03

#38 curation, #17 prepared-frame screening and now #29 supplied-seed rigid
refinement have reviewed source/API acceptance. #29 passes the 1020-item complete
local source suite, including the 165-case owning selection also run separately,
all five cookbook blocks and six policy comparisons with actual attribution.
The [receipt](evidence/rigid_refinement_acceptance_20261103_summary.json)
preserves exact producer identities, outputs and original historical comparisons.
No scientific default, runtime or test changes are needed for this acceptance.

| Order | Work and deliverable | Readiness / owner |
| --- | --- | --- |
| 1 | #36: accept public hypothesis composition and named interaction collections; preserve labeled observations, common source/frame/state, keep/reuse semantics, empty/failure behavior and independent constraints. | Can proceed now with the current MolSysMT tools and controlled providers. Execute its existing guards, driver and cookbook. |
| 2 | #37: accept the complete frozen EST/DES CCD interaction workflow, both roles and explicit placements, original chemistry/bytes, directional and steric negatives, unit persistence and attribution. | After #36 review, reuse public molecular preparation/translation/merge; designed controls are not observed biological complexes. Reconcile #30/#32/#33/#34 only after their own contracts are checked. |
| Parallel, by 2026-11-11 | #41: review the bounded old-public donor arithmetic exception and receive a supported generic-vector delivery before retiring it. | Current source already delegates vectors to MolSysMT. Public dependency/installed receiving remains #23/#10; ideal acceptor models remain separate #375 science. |
| Parallel, when a variant is needed | #60: receive native copy ownership for explicitly independent molecular variants and caches. | MolSysMT #121 is CLOSED; decision 655892f is included in controlled 0faf1584. Test the PHMT consumer profile; preserve intentional model references. No automatic default/API/minimum migration. |
| Scientific access gate | #66: obtain and qualify the original binding methods of Sun, Xin, Güngör and Scott before the next fixed-protocol data stage. | Needs a new authorized access lead. Preserve exposure, thresholds, sampling and no-pooling; #447 molecular/scaffold independence and #323 environmental H remain separate provider work. |
| Independent receiving | #9 exact-head CI/recovery; #23/#10 clean installed/public delivery when that milestone is selected. | Local source success does not close remote/platform/dependency/public gates. Addon and a new release stay deferred. |

**Immediate recommendation: proceed with #36, then #37.** Reuse completed source
checks only while the relevant code, test, input and provider identities remain
applicable. Keep the original evidence and run the owning workflow demonstrations;
aggregate passes do not automatically close all older issues. General molecular
operations and provider gaps stay in MolSysMT via issues; pharmacophoric composition,
interpretation and evaluation stay in PHMT. See [checkpoint](checkpoint.md).

## Prepared-conformer acceptance complete; qualify rigid refinement — 2026-11-03

#17's source/API scope is resolved without runtime/test changes. All 95 owning
controls and six workflow/cookbook blocks pass with stable producer identities.
The [receipt](evidence/conformer_acceptance_20261103_summary.json) additionally
retains five full ensembles, actual frame failures and attribution, immutable
inputs and retrospective exclusion of an unresolved molecule. #38 remains resolved.

Next accept #29's existing public rigid pair evaluator and supplied-seed greedy
refinement, both orientation policies and retained best accepted states. Review
rollback, counts, resource/provider failures and current examples; preserve
evidence favoring either policy without claiming universal superiority. Reuse
existing analytical/workload guards rather than adding molecular operations.
#66 still needs its four original binding methods through a new authorized route.
Exact-head CI remains #9 and installed/public delivery #23/#10. Addon and a new
release stay deferred; see the [checkpoint](checkpoint.md) for the exact handoff.

## Accept classical MVP segments while original methods are awaited — 2026-11-03

#38's cached-model curation source/API acceptance is complete: 84 owning tests
pass, all three cookbook blocks reproduce seven expected outcomes, and current
producer identities remain stable. Its shared-site partial in-place mutation is
corrected and guarded; [the receipt](evidence/curation_acceptance_20261103_summary.json)
preserves pre-fix failures and all earlier evidence separately.

Next perform functional/API acceptance of #17's existing prepared-conformer
screening: current state/frame access, explicit failed-conformer accounting,
resolved scores, unchanged inputs, portable best poses and retrospective use.
Then review #29's explicit rigid refinement/orientation alternatives. Reuse existing
guards and recipes; propose any missing molecular operation to MolSysMT by issue.
#66's four original binding methods remain an independent access gate. No exhausted
search repetition, study redesign, addon or new release is needed for these steps.
Source/API acceptance and #9/#23/#10 hosted/installed/public qualification retain
their separate scopes. See the [checkpoint](checkpoint.md) for exact resumption.

## Await original binding methods; official access handoff is concrete — 2026-11-03

The [#66 handoff](https://github.com/uibcdf/pharmacophoremt/issues/66#issuecomment-6611742289)
now names all four original articles with clickable DOI links and required
biological-method sections. A bounded review of the previously unreviewed
Güngör supporting document finds chemical/analytical characterization, not the
missing receptor-binding protocol. The [manual receipt](evidence/esr1_gungor_support_review_20261103_summary.json)
preserves this result and the newly observed source corpus; no source is accepted.

Next obtain the four main methods through a new authorized route. Do not repeat
exhausted discovery or infer a cohort from analytical data. #69 is resolved;
source/public-artifact qualification and molecular-provider science keep their
separate owners. The [checkpoint](checkpoint.md) records the exact pause boundary.

## Chemical-domain source adoption complete; return to MVP validation — 2026-11-03

#69's reviewed candidate **7e5b5a5** is integrated through code merge **76f43ffa**
after all eight actual Linux/macOS Python 3.11–3.14 source test steps pass,
including the recovered macOS 3.14 cell. The original cancelled attempt and
inherited successful executions remain separate in the
[hosted receipt](evidence/chemical_domain_hosted_adoption_20261103.json).
1,009 local source and 110 bounded installed-wheel passes keep their declared
limits. Ordinary new-head receiving stays #9; public artifact/minimum delivery
stays #23/#10. No new release or scientific profile is inferred.

The next product segment remains scientific validation under #66: obtain the
four original binding protocols through a new authorized access lead, qualify
eligibility, then follow the fixed pre-data declaration before any activity
acquisition or scoring. Repeating exhausted searches or silently replacing the
study design is not the next action. #323/#375/#447 retain their independent
provider boundaries. Addon work remains deferred; see the [checkpoint](checkpoint.md).

## Finish hosted receiving of the corrected chemical-domain candidate — 2026-11-03

MolSysMT #531 is resolved and received on source 0faf1584. Candidate **7e5b5a5**,
`receiving/chemical-domain-fixed-20261103`, passes **1,009 complete local source
tests**, all original 22 controls and all four unchanged typed CCD checks.
Separately, 110 installed local-wheel tests pass with checked origins and bytes;
shared/editable dependency limitations remain explicit in the
[receipt](evidence/chemical_domain_fixed_provider_receiving_20261103_summary.json).

The next gate is our [eight-cell source CI 41674239397](https://github.com/uibcdf/pharmacophoremt/actions/runs/41674239397),
still pending at this receipt. Verify every actual scientific test step for exact
7e5b5a5, then integrate directly into main and inspect main receiving under #9.
The later macOS 3.14 cancellation occurred before any step because GitHub could
not supply a hosted ARM64 runner. Recover that cell after the active attempt
settles; its rejected individual retry and native annotations are in the checkpoint.
Main runtime/pins are preserved until that result; no provider implementation or
human scientific validation is currently awaited for this step. Keep installed
Conda/public qualification and any future minimum/release separate. Addon and
broader scientific segments remain deferred; see the [checkpoint](checkpoint.md).

## Resolve typed component preservation before integrating #69 — 2026-11-02

Owner review is published in candidate **43a258c**, isolated from main. It receives
the implemented de7ffad chemical-domain API, current controlled source pins,
negative-spy corrections, real pin-mutation counterexamples and six new consumer
domain controls. All 22 original baseline nodes pass; clean candidate confirmation
passes 73 focused controls. The full original source run still identifies four
typed-component preservation checks after the seven client corrections.

MolSysMT #255 is now closed after main merge 00abb958; the provider reports
runtime/test trees identical to executed de7ffad. No fresh merge execution or
package qualification is inferred. The remaining defect is separately tracked.

Next obtain [MolSysMT #531's typed-column disposition/correction](https://github.com/uibcdf/molsysmt/issues/531),
receive it and rerun those unchanged assertions. Main's working source route is
preserved; do not integrate a known-red pair or add a local chemical normalizer.
Complete source/installed/public qualification separately. The
[checkpoint](checkpoint.md) links the exact candidate, full failures, corrections
and source/environment limits. No new dataset, scientific profile, package floor,
addon work or release is authorized by source receiving.

## Prepare and receive the chemical-domain cutover — 2026-10-29

[#69's receiving contract](chemical_domain_receiving.md) inventories the one direct
SMARTS namespace move plus indirect state, preparation, copy and persistence
boundaries. The new 22-test current-behavior source baseline passes on exact
provider 71fbe4f; original source 87de52f also passes eight actual hosted scientific
cells on its separate qualified pin. Neither executes the target migration.

Next receive the maintainer-approved MolSysMT #255 implementation through the
MolSysSuite #155 coordination route. Preserve scientific definitions, source
maps, units, failures and saved producer evidence; require real state/absence/
component/copy/codec receiving before source and installed/public compatibility
claims or dependency migration. Runtime/client edits and speculative floors are
not part of advance-notice preparation. General molecular operations stay in
MolSysMT; PHMT does not add a chemical graph or state engine.

#255 precedes the provider's #447 identity/scaffold work. #66's original-method
access remains independent; retain the four-article handoff and all observed
exposure. #323/#375 have their own scientific/delivery scope. Addon, broader
algorithms and a new release remain deferred. See [checkpoint](checkpoint.md).

## Original binding protocols need a new access route — 2026-10-28

#66's [supplement follow-up](esr1_binding_pool3_methods.md#scott-supplement-and-access-follow-up--2026-10-28)
confirms that Scott S53 supplies results/errors and S55 specifies a crystallography
variant, without resolving the binding protocol. Four journal methods remain
unresolved after bounded ordinary discovery. Obtain their original methods
through authorized access; repeat public discovery only with a new lead. Preserve
the newly observed S53 activity/S54 chemical-string and search-snippet exposure
in subsequent declarations. No source is accepted or scored, and no activity
classes are inferred from the visible table.

An alternative study design needs its own scientific justification/declaration.
Molecular identity/scaffold (#447), environmental H refinement (#323) and public
generic-vector delivery (#375/#41) remain provider coordination, independent of
current source access. Keep CI receiving under #9; addon and a new release remain
deferred. The [checkpoint](checkpoint.md) contains the exact handoff and evidence.

## Receive provider delivery and remove bounded legacy geometry — 2026-10-28

#41's [feature API integration](molsysmt_feature_receiving.md) now uses the public
new H-bond namespace and general Cartesian vectors when available, with explicit
provenance and visible provider failures. Source-provider integration and the
ERalpha diagnostic pass 160 selected tests. The historical public payload passes
its compatibility controls, while an ordinary fresh environment is unqualified
after host quota exhaustion. No provider floor or CI pin changes.

Next complete #9 exact-head hosted receiving and clean source/installed/public
qualification of a provider delivery confirmed by its owners. Then remove the
old donor arithmetic, retained only for the supported provider without vectors.
#41 stays partial; owner LMMV/dprada reviews that exception by **2026-11-11**.
Do not adopt ideal acceptor geometry or close #375 from generic donor-vector
evidence. No molecular algorithm is added locally or implemented in a sibling.

#66's four unresolved original journal protocols remain an independent useful
next scientific segment; preserve the original-method and exposure gates before
detailed activity acquisition. Addon, broader algorithms and a new release stay
deferred. See the [checkpoint](checkpoint.md) for exact execution/environment
boundaries and retained failures.

## Original-method qualification remains open; independent receiving available — 2026-10-28

#66's [six-source review](esr1_binding_pool3_methods.md) accepts no source for
detailed activities. The first patent's 23 reported α positions fail the minimum
population upper bound, independently of 69 database records. The other patent's
CHO-cytosol method does not qualify the primary receptor/format. Four journal
protocols remain unresolved after ordinary publisher/locator/supplement review;
HTTP success, abstract pharmacology and an open data supplement are insufficient.
Keep those sources unresolved, without substitutes or relaxed scientific rules.

Document/search potency and compound information has now been observed; preserve
the explicit new exposure ledger, including CID 10399473, alongside earlier
history. No activity-resource tables, computational molecular inputs, new class
counts or scores are acquired. Fixed queries and earlier source results remain.

Next obtain those original protocols or predeclare a separately justified study
design. The independent #41 review of newer public-provider site recognition and
general donor geometry can proceed while source access is pending. Do not
implement molecular operations locally or confuse those access/population limits
with provider #323/#375/#447. Addon, broader algorithms and a new release remain
deferred; exact-head source receiving remains #9.

## Fifteen capacity survivors; original methods review next — 2026-10-28

#66's [complete pool-3 census](esr1_binding_pool3.md) retains all 475 capacity
responses plus status and an independently reproduced clean-source receipt.
Fifteen sources have at least 40 raw records; none is yet an experimentally or
molecularly qualified cohort. The largest two describe coactivator experiments;
relative and single-concentration metadata are also explicit warnings. No detailed
values, compound information, structures or scores are acquired.

Next review original methods for the six descriptions without those explicit
warnings, starting with CHEMBL5725373 / CHEMBL5730671, and retain the other
survivors/rejection reasons. Commit another finite detailed-source declaration
before activity tables. Keep original queries/class thresholds/no-pooling and
all historical exposure/results. Later identity/scaffold/preparation gates remain
MolSysMT-owned. Source-count review can advance without #323/#375/#447 delivery;
a chemically independent scoring cohort cannot be claimed from those counts.
Addon, wider algorithms and a new release remain deferred.

## Next bounded step: remaining single-protein capacity census — 2026-10-28

#66 now has a [third pre-data declaration](esr1_binding_pool3.md): all 475 remaining
single-protein assays in the retained metadata, without a description filter.
First acquire ID-only capacity metadata, retaining every failure. Rank only after
all capacities resolve; no detailed activity table or molecular/score acquisition
is part of this declaration. Capacity survivors need original experimental review
and another dated detailed-source decision. Keep thresholds, fixed queries,
no-pooling and all historical exposure/outcomes. Provider #447 remains a later
molecular-independence gate, not a source-count blocker.

Previously pending source CI/retry observations are now successful; see the
[dated native receipt](evidence/ci_receiving_20261028.json). New-head receiving
remains #9. The separate #41/#375 provider-API integration review is still useful;
source code availability does not itself qualify its scientific contract.
Addon, expanded algorithms and a new release remain deferred.

## Broader source nomination needed after capacity-only stop — 2026-10-26

#66's [second declared pool](esr1_binding_pool2.md) screens 42 metadata-nominated
human binding assays without activity values or compound/structure data.
All raw counts are below 40 (maximum 26), making twenty groups per class
impossible. No detailed table or score is acquired; both prior result sets and
exposure inventories are unchanged. The result is bounded by its metadata
heuristic and cannot reject the remaining ChEMBL/source universe.

Next expand metadata nomination through another dated pre-data declaration,
keeping scientific/class and fixed-query rules intact, or review a separately
declared study design. Molecular identity/scaffold and preparation remain in
MolSysMT. Hosted recovery/receiving remains #9; addon and a new release stay
deferred.

The [clean corrected replay](evidence/esr1_binding_pool2_20261026_summary.json)
preserves the original acquisition, all capacity responses and unchanged compound
exposure inventory. Final local qualification passes 62 tests / 56 subtests;
exact-head hosted and installed receiving remain separate. Do not discard the
bounded negative source result when broadening the next nomination rule.

## First binding source pool exhausted; redeclare sources next — 2026-10-24

The [#66 source qualification](esr1_binding_source_review.md) stops both fixed
candidates under the unchanged pre-data protocol. Their complete tables have
15 IC50 identifiers (6 positive / 2 weak / 7 unresolved) and 10 Ki identifiers
(10 positive / 0 weak), before molecular audits. Neither can meet the minimum
20 groups per class. No missing value becomes inactive; no molecular preparation
or scoring is run. This is a source-readiness failure independent of MolSysMT.

Next declare a new dated source pool with adequate measured weak comparators
before inspecting more activities. Keep both original queries and the first
terminal result, and include the 25 new ChEMBL IDs in historical exposure checks.
MolSysMT remains responsible for aliases/identity/scaffold and preparation;
#66 remains partial for an eligible fresh cohort. #9 retains exact-head CI
receiving. No addon, new package or release work is added.

The clean c744df9 source/label
[receipt](evidence/esr1_binding_source_qualification_20261024_summary.json)
retains the terminal stop and every original source record. Final local gates
pass 57 tests / 49 subtests; hosted/installed receiving is separate. This
result must stay visible when selecting a new source population.

## Fresh binding challenge in design/source qualification — 2026-10-24

[#66](pending_proposals/esr1_binding_evaluation_readiness.md) now owns the next
evaluation segment. Its [committed protocol](esr1_binding_evaluation_plan.md)
preserves the two frozen queries and fixes endpoint, activity/censor/quality,
exclusion, sampling and failure rules before new individual activity/structure
acquisition. Discovery metadata covers 1,485 ChEMBL assays and three PubChem
alternatives; CHEMBL3382763 then CHEMBL3705057 form the next bounded source pool.
Metadata nomination does not qualify a dataset or freeze a cohort.

Clean producer `507ca37d8f21815bb29c0a34f8ccf3b020edbacf` retains the
[measured metadata/exclusion review](evidence/esr1_binding_metadata_review_20261024_summary.json),
explicitly not ready for scoring. Next inspect the nominated source documents
and qualify individual activity schemas under the committed protocol; no new
activity values or molecular inputs have yet been acquired.

The historical exposure inventory covers every known prior-source CID (8,099),
including all Bath and requested inputs, plus 149 unresolved blank-CID rows/SIDs.
MolSysMT #447 is still needed for molecular identity/scaffold independence; general
preparation/state/conformer work stays with its provider. Local source review and
activity-schema qualification can proceed in parallel with those provider needs.
No score is computed or missing input converted to inactivity. #65 supplies the
later native original-cohort and common-subset reporting tools. #9 retains exact-
head receiving; addon and a new public release remain deferred.

## Native reporting delivered; receiving and scientific design next — 2026-10-24

[#65](archive/native_retrospective_result_summaries.md) now delivers reusable
saved-result summaries and paired common-subset comparison in PHMT validation.
The [new derived receipt](evidence/esr1_saved_summary_replay_20261024_summary.json)
reproduces unchanged #64 counts, scores, metrics and provenance from clean
implementation `e32c80e0cbc9837e8badcda2b7c93f22d30f1ddc`. It performs no
molecular work. New statistical consumers use the native tool; the original
case driver/output retain their historical producer. 84 selected scientific
tests and administrative/strict-docs/archive guards pass locally; full
exact-head hosted and installed receiving remain separate under #9/#23.

Next verify exact-head hosted receiving and review the design of fresh,
unexposed biological evaluation data before further predictive claims. The
observed 64-input comparison is development evidence, with 19 unavailable
structures and unqualified chemical-series independence. Existing MolSysMT
identity/scaffold/conformer/state proposals remain provider-owned and received
through #41. No local molecular workaround, addon work or new release is added.
Public 0.4.0 and its original release-specific suite notice are unchanged.

## Current priorities — 2026-10-24

**#64's bounded paired comparison is complete.** The
[resolved report](archive/esr1_consensus_comparison.md),
[measured case](../docs/content/validation/esr1_consensus_comparison.md) and
[paired summary](evidence/esr1_paired_evaluation_20261024_summary.json) preserve
the original training stop, separately declared ready query and fixed evaluation.
Both queries score the same 45 prepared inputs (12 active / 33 inactive); 19
original HTTP 404 inputs remain unscored. Reference/consensus AUC is
0.4848484848 / 0.5530303030, with descriptive common-subset difference
+0.0681818182. EF10% is 0.8182 / 1.6829. This is modest same-assay exploratory
evidence with missing inputs, extensive ties and unqualified chemical-series
independence, not predictive acceptance. Future tuning cannot reuse these 64
now-exposed outcomes as unseen validation.

All molecular operations remain in public MolSysMT. Source/provider hashes match
qualified training and state/coordinate/atom observations stay identical across
arms. Original full outputs, all response failures, native/preparation journals,
exact query hashes, actual attribution and independent metric oracles are retained.
103 selected scientific controls and the documented administrative/strict-docs
gates pass. These are separate from final-head hosted/installed/public receiving.

The earlier #63 explicit binary ranking contract and #62 frozen pilot/replay/input
retention remain delivered. Their old results are not overwritten. Public 0.4.0
is unchanged; no new package/release is produced.

**Next product segment: [#65](https://github.com/uibcdf/pharmacophoremt/issues/65).**
Generalize the demonstrated original-cohort/saved-result/unscored-input accounting
into independently useful native PHMT validation tools. Reuse existing score and
metric contracts; support explicit native/original index mapping and common-subset
comparison without rerunning molecular search. Keep source preparation in MolSysMT
and preserve original producer attribution. #64 provides concrete consumer evidence
and independent oracles. This local API work does not wait for a molecular-provider
change and does not add another ad hoc scientific-case implementation.

Before stronger biological-performance claims, review endpoint/data suitability
and predeclare fresh training/evaluation data. Molecular identity/scaffold overlap
belongs to MolSysMT #447; conformer/state/stereo needs remain in their existing
provider issues, received through #41. Do not implement those molecular operations
here or infer chemical-series independence from different external CIDs.

The owned #64 environment is retired after evidence capture via scoped filesystem
removal of its verified task-created prefix. No uninstall hook/shared repair/
global-cache cleanup runs; earlier native hook behavior remains MolSysSuite #139.
New addon work and wider documentation/release infrastructure remain deferred.
Follow #9 for this head's native receiving; older successful matrices remain dated.

## Current priorities — 2026-10-23

The maintainer has resumed the **MVP scientific workflow**, with addon and deeper
documentation deferred. [#62](archive/esr1_activity_pilot.md) executes
an independent ligand-reference ERα assay pilot: a pre-score frozen cohort,
published 3D conformers, public MolSysMT preparation and native held-out screening.
Keep preparation/search failures distinct from inactivity, and do not tune the
query against held-out outcomes. Receptor refinement and newer-provider receiving
remain separate; this pilot does not depend on MolSysMT #323.

The first #62 run is measured: 25 evaluable held-out compounds, six unscored,
AUC 0.5614 and 23 zero-score ties. Preserve the original weak result and frozen
query; it is not predictive acceptance. Next resolve durable original-input
retention and receive provider-owned conformer/stereo capabilities (#219/#215)
before declaring a new comparison. Do not retune on the observed held-out set.

**Next local scientific task: [#63](archive/rigid_negative_ranking_contract.md).**
A separate analytical source probe confirms that completed negatives can retain
frame-dependent partial coverage. Define and qualify the ranking contract before
extending comparative activity claims. Molecular transforms already use MolSysMT;
this PharmacophoreMT scoring task does not depend on upstream preparation work.

The first documentation foundation is delivered: inherited project identity (#4)
and landing/user/developer/showcase entry points (#61) are corrected, strictly
built and natively published. The [checkpoint](checkpoint.md) and archived reports
link source/rendering/publication evidence. Notebook execution material and
molecular ownership are preserved; no runtime API, package or viewer feature is
added. Deeper user-guide concepts and worked routes can follow measured MVP needs.

**0.4.0 is delivered** through the official Conda channel and GitHub Release.
The [delivery checkpoint](checkpoint.md) links original source/staging, all eight
installed cells (921 passing items each), same-byte public promotion and fresh
normal Linux/Python 3.14.9 receiving. The requested release-specific notice is
[MolSysSuite #131](https://github.com/uibcdf/molsyssuite/issues/131).

Next, receive central public admission/badge disposition under #23/#131 and the
shared automatic Release-event route under #10/#131. That extra event rejects
the staged plan before build/upload; it does not invalidate the separately
verified staged promotion. Preserve the original tag/file. Independent work can
resume at #41's newer-provider receiving or #20/#22's scientific validation;
general molecular work stays with MolSysMT and new addon work remains deferred.

## Prior candidate decision — 2026-10-23

The maintainer resumed the distribution segment and confirmed **0.4.0**. The real
[`release_plan.toml`](../devtools/conda-build/release_plan.toml) selects build 0,
one noarch archive and staging, retaining all eight installed cells and eleven
required native source/control jobs. Next acquire the committed candidate's
exact-source gates, establish staging access, build the original archive and
qualify it before reviewing publication. Existing source/wheel evidence and
MolSysSuite's independent receiving of that milestone do not qualify new bytes.
See the [current checkpoint](checkpoint.md). New addon work remains deferred.

## Prior checkpoint — 2026-10-20

Work is paused at the maintainer's request. The [pause checkpoint](checkpoint.md)
records implementation/evidence identities, retained resources and the ordered
restart procedure. Version 0.4.0 is a proposal awaiting confirmation; no actual
Conda candidate is selected.

The maintainer has deferred new addon work. The current segment is distribution
and installed qualification under #9/#10/#23. Packaging metadata #57 is resolved:
both the minimum compatible setuptools 77.0.3 and current 84.2.0 build license-bearing
sdists and wheels; see [the archived result](archive/packaging_license_metadata.md).

MolSysSuite #117 is delivered at immutable provider
`1c248b67d1daea256ed7c7f6172c6addb3f0b08f`. The component now adopts its explicit
unshipped support contract and all-runtime-root guard, retaining the addon payload
already shipped under #56. The scientific fixture implementations move to
`phmt_test_support`; general molecular operations remain MolSysMT-owned.
Development command wrappers remain available. The complete selection now passes
**921 tests** from a real isolated development wheel on Linux/Python 3.14.8 with
public providers. All 179 runtime payload paths match, and the shared runner
verifies then retires its staged support resources/imports. See the
[full receiving receipt](evidence/installed_support_adoption_20261020_summary.json);
the original 915-pass/six-failure attempt remains in its separate preparation
record. This is independent of any Conda candidate and its eight native cells.

Source implementation `636373d` now passes all eight Linux/macOS × Python
3.11–3.14 cells, including installed-provider preflight and full tests. Reporting,
policy and Conda governance also pass: eleven required executed jobs across the
three workflows. See the [exact-source receipt](evidence/source_ci_receiving_20261020_summary.json).
The daily-only backlog detector is inapplicable to this push and is not counted
as executed recovery. These source gates do not qualify a Conda artifact.

The next steps are:

1. Select a real release version and committed plan under #10. The illustrative
   0.0.0 plan is not a candidate.
   The requested 0.1.0 already names a historical upstream tag; the maintainer's
   collision-free version decision is pending. Repository-level token inspection
   does not establish available staging credentials.
2. Establish staging access, build one original Conda archive and execute all
   eight installed cells with both provenance checks, retaining the new candidate's
   exact source, dependencies, file and digest. Earlier source/wheel evidence
   does not replace those candidate-bound gates.
3. After that qualification, review the publication decision and public receiving
   evidence under #23; do not infer it from a source or wheel-only result.
4. Resume the independent scientific validation segments #20/#22 with declared
   controls and existing evidence tools. MolSysMT #375 remains a provider-owned
   follow-up under #41; environmental hydrogen refinement #323 stays upstream.

The 2026-10-13 priorities below retain their original checkpoint. Their addon-first
ordering and pending #117 status are superseded by this dated update.

## Prior checkpoint — 2026-10-13

The native class/default routes now require prepared input and explicit scientific
choices: ligand consensus (#18), observed-complex construction (#42), cached
receptor projections (#44), and placed/rigid/prepared-conformer screening (#45).
Orphaned general molecular utilities and the historical library reader are
retired (#46). Versioned pharmacophore SDF persistence preserves its declared
six-shape/native-payload contract (#47); the attribution subprocess import guard
is repaired (#48). General molecular preparation, geometry and molecular library
I/O remain MolSysMT responsibilities.

The authored-diagnostic rendering and zero-angle comparison corrections are
reviewed under #2/#16 with fresh controls and archived reports. Their original
archive checkpoints retain their dated evidence. These narrow closures do not
close every implemented workflow's scientific/API review.

The prepared end-to-end control (#49) now reviews cached inventory construction,
explicit ring/hydrophobic curation, JSON/YAML/versioned PHMT SDF recovery and
ranked placed screening on public CCD EST. Independent displacement, exclusion,
failure and stable-tie controls pass with preserved maps/history and detached
readers; see [the contract](prepared_end_to_end_workflow.md). This advances the
bounded analytical acceptance gate while MolSysMT #375 remains post-1.0 work.
It does not establish biological discrimination or close every classical route.

The rigid/frame continuation (#50) adds explicit non-collinear essential anchors,
saved-query proper-motion recovery, complete selected-participant negatives and
budget-failure/ensemble-resolution controls; see [the contract](prepared_search_workflow.md).
It reuses existing tools and keeps 29 prior evidence archives unchanged. These
prepared placements do not supply generated conformers or activity validation.

The distinct-ligand continuation (#51) reviews EST/DES joint support, original
occurrence/atom/frame maps, completed impossible-site-count empty hypotheses and
failed facade rebuilds; see [the contract](prepared_consensus_workflow.md).
Molecular operations remain MolSysMT-owned; ideal-coordinate consensus does not
establish biological discrimination.

The cached-receptor continuation (#52) reviews separate PHE404 projection
alternatives, explicit exclusion vetoes, retained native ERα observations and
empty/failed facade semantics; see [the contract](prepared_receptor_workflow.md).
It consumes the archived prepared artifact without hydrogen regeneration or
contact redetection. Synthetic geometric controls do not qualify binding poses.

The ordinary environment review (#10/#23) now executes public-dependency
production/development Python 3.14 and docs Python 3.12 checks on Linux x86_64,
with exact editable PHMT source and 119 passing selected controls across separate
invocations. The whole-site documentation repair (#53) passes strict builds on
both reviewed interpreters. See
[the original receipt](evidence/ordinary_environment_review_20261010_summary.json).
This does not qualify a public PHMT artifact or the full installed matrix;
effective-channel reporting is proposed in MolSysSuite #116.

The installed candidate review (#10) corrects the frozen workflow's evidence-step
contract under #54. Before an actual artifact, resolve scientific helper
namespaces via MolSysSuite #117 and review addon delivery plus the existing
#110 all-root guard. Public test inputs are reviewed below under #55. See
[the readiness receipt](evidence/installed_candidate_readiness_20261010_summary.json).

The public test-input qualification (#55) now declares MolSysViewer 0.24.0,
Ackredit 0.12.0, Beartype 0.22.9 and OpenMM 8.6.1 through the shared installed-test
descriptor. All 899 source tests pass with public providers on Linux/Python 3.14.8;
eight dependency dry solves cover the supported minors and Linux/macOS arm64
(the latter assumes macOS 15). See [the original receipt](evidence/public_test_dependencies_20261010_summary.json).
These are observed versions, not compatibility minima or complete installed
qualification. Addon payload/distribution and browser work subsequently advanced
under #56/#58/#59 below. MolSysSuite #117 still blocks the complete isolated
installed science gate; this dependency review did not execute browser rendering.

The attribution continuation (#19/#6) now verifies public MolSysMT 0.23.0 and
Ackredit 0.12.0 failure isolation with 39 passing attribution/contract controls
on Linux/Python 3.14.8, plus the same local development selection. MolSysMT #295
is removed from active blockers; original failure evidence remains historical.
See [the public review receipt](evidence/public_attribution_review_20261013_summary.json).
Optional viewer absence and support-library boundaries are reviewed separately
from addon/browser delivery. Whole #6/#19 and installed/public qualification
remain partial; the prior `e912093` source matrix's eleven required jobs are
independently verified without claiming that they ran these new guards.

The minimal viewer addon continuation (#56) bundles the integration and its module
entry point in PharmacophoreMT. Twenty-two controls pass from a normal isolated
wheel installation with public MolSysViewer 0.24.0 on Linux/Python 3.14.8 and in
development. Sphere-only geometry, explicit units, honest panel failures and exact
owned-tag clearing have independent controls. See
[the contract](viewer_addon_workflow.md) and
[the original receipt](evidence/minimal_viewer_addon_20261013_summary.json).
The public provider's root-export discovery cycle is reported in MolSysViewer
#233; PHMT uses the public module directly. Build metadata maintenance is tracked
in local #57. Browser interaction/rendering advanced under #58 below. This bounded
wheel proof does not close the full installed/public matrix or MolSysSuite #117;
publication workflows still need reviewed all-root helper adoption.

The live viewer continuation (#58) passes nine real Jupyter/Chrome controls with
the native molecular demo: panel state, Render/Clear, repeat/remount, visible
spheres, unsupported input and recoverable failure/disable cleanup. The same
cached model without a molecular system reveals a hidden addon workspace behind
the welcome state; MolSysViewer #240 owns that blocker. See
[the original live receipt](evidence/live_viewer_addon_20261013_summary.json).
The [separate installed current-source receipt](evidence/current_viewer_addon_20261013_summary.json)
repeats the nine molecular-scene controls and the shape-only blocker with viewer
`76c8cee1`, public MolSysMT 0.23.0 and Python 3.14.8. It preserves the generated
viewer overlay and original wheels; it is not published-viewer browser proof.
The operation warning and lock audit findings belong to MolSysViewer #239/#242.
#58 remains partial; no dummy molecule or local generic host workaround is added.
Local #59 resolves empty/absent/error panel feedback and explicit frontend
teardown; its [fresh receipt](evidence/viewer_panel_feedback_20261013_final_summary.json)
keeps that development-panel qualification separate from the provider blocker.
Its final 14 browser controls and 23 native addon tests cover input-state
distinctions, payload/action errors and explicit teardown; #59 is closed.
Public browser, session persistence and hardware/Qt remain separate gates.

The next steps are:

1. Finish the browser contract in #58 after MolSysViewer #240 is resolved, and
   repeat the changed consumer/provider controls with fresh producer identities.
   Local packaging metadata work remains in #57.
2. Complete inspection of the applicable hosted matrix and installed/public
   delivery gates under #9/#10/#23. A passing focused run or one matrix cell
   cannot stand for all Python versions/platforms or a public artifact.
3. Extend the bounded prepared native workflow review to independently declared
   activity-based validation or remaining classical-route cases. Reuse existing
   method/recipe/evidence tools; define independent positive/negative controls
   and preserve original inputs, states, mappings and failures. The collection
   and the ERα continuation remain tracked in #20/#22. Prepared/analytical
   controls do not by themselves establish biological or activity-based success.
4. Finish the remaining consumer migration in #41 when MolSysMT #375 supplies
   a qualified public geometry contract. Its only retained molecular arithmetic
   is the bounded donor-H displacement/normalization in `get_features()`; do not
   recreate missing provider geometry in PHMT. Independent preparation (#219),
   molecular collection/property correspondence (#215 follow-up / #223) and
   environmental H refinement (#323) stay with their provider owners.

Automatic pocket/direction hypotheses, viewer/docking integration, biological
pilots and strategy/performance comparisons remain separate acceptance work.
Advanced dynamic or accelerated methods follow the classical acceptance gate.

## Historical checkpoints

The dated checkpoints below record the state and then-next step at each
measurement. Current priorities above supersede completed next-step instructions;
original provider limitations and measurements keep their original scope.

**2026-10-10 utility retirement (#46):** The orphaned molecular utility package
and name-grouped SDF reader are removed, with matching distribution inventory
updates. Retained `openpharmacophore` notebooks are explicitly historical;
their original data/output bytes stay unchanged. See [the retirement contract](molecular_utility_retirement.md).
#41 remains partial for donor-H geometry delegation to MolSysMT #375; provider
preparation/collection/environment-refinement requirements stay in their owners.

**2026-10-10 screening transition (#45):** `VirtualScreening` now requires an
explicit placed/rigid/prepared-conformer method and delegates to native tools;
see [the contract](virtual_screening_workflow.md). Legacy preparation/matching,
implicit validator fallbacks and local molecular SDF export are retired.
CSV contains scalar hit evidence. #41 remains partial for unused generic
utilities/library ingestion and donor geometry delegation (MolSysMT #375).
Next local work is that bounded utility/caller inventory and retirement; provider
#219/#215/#223/#323 remain independent capabilities, not local implementation tasks.

**2026-10-10 structure transition (#44):** Structure-based construction now
consumes cached receptor inventories and explicit pharmacophoric projections;
see [the contract](structure_based_workflow.md). The old local recognition,
selection and neighbor/+z inference are retired. Automatic pocket hypotheses
remain future work. Donor-pair/local acceptor geometry is requested in MolSysMT
#375, including the outstanding donor-vector migration in `get_features()`.
#41 remains partial; next local work is legacy screening/preparation retirement.

**2026-10-10 complex transition (#42):** `ComplexBasedModeler` and the default
`model()` now require prepared native observations and an explicit ligand
selection. The old preparation/detection engine is retired; see the
[migration contract](complex_based_workflow.md). This supersedes the default-route
finding in the earlier audit checkpoint below. #41 remains partial; next local
work is structure-based provider consumption and legacy screening retirement.
Provider #323/#350/#367 remain independent limitations.

**2026-10-10 ownership review:** The
[molecular ownership audit](pending_proposals/retire_legacy_molecular_operations.md)
tracks remaining reachable legacy preparation/recognition/I/O under #41. Native
workflows delegate molecular operations to MolSysMT, but `model()` still defaults
to the legacy complex builder. Next local work is its explicit prepared-input
transition, followed by structure-based provider consumption and legacy screening
retirement. Do not extend local molecular utilities. Conformer generation remains
provider #219; optional standardization is proposed in #366, and a reproduced
public-fit degeneracy defect is #367. The #31 automatic seed guard is reviewed
with 60 focused cases and 680 full-suite tests; it does not repair arbitrary
provider fits. Existing #323/#350 limitations remain explicit. Docking-specific
contracts belong to DockingMT; no new docking-owned gap was identified in this
source audit.

**2026-10-07 ERα checkpoint:** The maintained declared 304–550 fragment/EST
chain and its independent placed/exclusion/persistence controls are delivered.
[Empty-family diagnosis](eralpha_interaction_diagnostics.md) now distinguishes
recognized participants from geometric rejection: local generated H fail the
declared H-bond angular gate; PHE404/EST fail the reference pi-pi intersection
gate. Environmental H refinement remains MolSysMT #323, and public rejected-pair
geometry diagnostics are requested in #350. These controls do not establish
complete receptor preparation or activity-based validation; Gen 1b remains the
current acceptance focus.

**2026-10-02 review checkpoint:** Traditional workflows are the immediate
acceptance gate. The native [observed-complex slice](placed_pose_workflow.md) and
[reference-ligand slice](reference_ligand_workflow.md) are implemented locally
with analytical controls. [Growth contracts](extensible_modeling_contracts.md)
record the accepted ownership and method/backend/execution separation. Local
verification does not qualify legacy routes or establish biological-pilot success.

The development of PharmacophoreMT is divided into generations. **Gen 1b** has been added between the original Gen 1 and Gen 2 after an audit revealed that the classical pharmacophore workflow was incomplete and required consolidation before advancing to dynamic modeling.

---

## Gen 1: Historical Foundation Deliveries
These historical delivery marks mean code exists, not that all scientific or
integration contracts have passed the current classical acceptance gate.

- [x] Refactor from `openpharmacophore` to `pharmacophoremt`.
- [x] Integration with `molsysmt`, `pyunitwizard`, `argdigest`, and `smonitor`.
- [x] Complete Pharmer and LigandScout I/O.
- [x] Official `molsysviewer` integration (RFC-001, `add_interaction_sites`).
- [x] High-Resolution modeling triad: `ComplexBasedModeler`, `LigandBasedModeler` (consensus), `StructureBasedModeler` (projections).
- [x] `InteractionSite` composition pattern (Feature + Shape) with full arsenal of shapes and features.
- [x] `ConformerGenerator` utility.
- [x] Rescue and migration of all logic from legacy repositories.

---

## Gen 1b: Classical Consolidation (Current Focus)

**Goal:** Make the classical pharmacophore workflow — ligand-based, structure-based, and complex-based modeling through to virtual screening and validation — complete, robust, and scientifically rigorous.

The accepted implementation order is below. The older detailed feature catalog
in [`classical_workflow.md`](classical_workflow.md) retains scientific backlog
ideas; its direct-RDKit and hidden-preparation proposals are superseded.

### 1. Shared chemical definitions and placed-pose controls
- [x] Strict explicit units, validated geometry, essential/weight/site metadata.
- [x] Observed-complex construction for native hydrophobic/H-bond interactions (#13).
- [x] Reusable chemical extraction and reference-ligand queries with six classical families (#14).
- [x] Shared pose evaluation, directional/plane controls, one-to-one assignments and exclusion veto.
- [x] Retrospective ROC/AUC, BEDROC and EF with correct ties and explicit failure accounting (#12; reviewed closure 2026-10-07, independent ranking and native/legacy accounting guards).
- [x] Source/state/method provenance and native persistence for these delivered slices.
- [ ] Scientific/API review and biological-pilot validation of these slices.
- [ ] General extension registration, stable site identity and complete portable codecs.

### 2. Native traditional workflows
- [x] Bounded rigid triplet search and prepared-ligand alignment through MolSysMT (#15); continuous exhaustive search remains outside this method.
- [x] Screen prepared multi-frame conformers with best-pose/state evidence and explicit failure accounting (#17).
- [ ] Provider-supported conformer preparation; resolve missing tools in MolSysMT.
- [ ] Ligand/complex consensus with coverage, explicit frames and curated essential/weight policies.
- [x] First reference-anchored consensus from prepared aligned ligands, with reusable matching/aggregation, unique ligand support and portable evidence (#21).
- [x] Bounded aligned clique discovery and alternative jointly supported hypotheses, with reusable tools, independent subset controls and executed-method attribution (#24).
- [x] First prepared rigid unaligned consensus with explicit pivot, maximal association mappings or triplet seeds, MolSysMT fits and alternative layout evidence (#26); see [the contract](rigid_consensus_workflow.md).
- [x] Public inventory-to-query, explicit-mapping placement and saved-report summary tools; six frozen analytical comparison controls (#27), with [modular contracts](rigid_strategy_comparison.md) and an [executable recipe](../docs/content/cookbook/modular_rigid_tools.md).
- [x] Typed-neighborhood comparison and supplied-triplet ranking tools, consumed by ranked_triplet_seeds with explicit selection/false-negative controls (#28); this is the G3PS seed stage, not full greedy refinement.
- [x] Public pair evaluation and greedy rigid refinement with final/each_step angular policies, best valid checkpoint retention and reciprocal analytical controls (#29). Both variants remain available; eleven seed/tolerance/mixed-family/3D workloads now have retained coverage, runtime and scoped-memory comparisons.
- [x] Traceable prepared real chemical components (CCD ideal EST/DES) with public MolSysMT preparation, refinement/consensus/frame-screening controls, retained hypotheses and actual resource/method citation capture (#30). This does not establish experimental conformer or biological performance.
- [x] Observed 1QKU EST heavy-atom template integration through public MolSysMT assessment/application, with selected acceptor/aromatic placed controls, persistence and actual input citations (#22). Receptor/biological acceptance remains pending.
- [x] Explicit fixed-state H placement through the resolved MolSysMT #300 tool, with donor-inclusive observed-pose evaluation, persistence and both rigid recovery policies (#22). Local generated H geometry does not establish environment refinement or biological acceptance.
- [x] Observed receptor residue/readiness audit through public MolSysMT #217/#218 diagnostics, with declared spatial scopes, preserved detector failures and actual-data-only credit (#22). The declared fragment adopts delivered MolSysMT #298 template preparation; complete-receptor acceptance remains open.
- [x] Maintained declared receptor-fragment/EST composition, independent placed/orientation/exclusion/persistence controls and fixed empty-family diagnosis (#22). Recognition and geometric rejection are distinguished without changing the original observations; environmental H refinement remains provider #323.
- [ ] Compare G3PS, safe RDP/frequent-clique conformer discovery and triangle indexing on controlled workloads; see [the primary-source survey](pharmacophore_search_strategies.md).
- [x] Review recursive partitioning/clique literature and execute bounded legacy counterexamples (#18); see [the consensus review](clique_consensus_review.md).
- [x] Retire the defective legacy ligand consensus builder; preserve its audit and expose explicit rigid/aligned native choices through the class and dispatcher (#18); see [the migration contract](ligand_based_workflow.md).
- [x] Extend native complex construction to aromatic/charge interaction families with independent controls.
  The first ionic extension now calls shared public charge-feature tools and
  retains compound membership/geometry, contact evidence and actual attribution
  (#33; [contract](ionic_interaction_workflow.md)). Pi-pi/cation-pi conversion now
  supports seven declared profiles, shared geometry and explicit atomic-to-compound
  cation mapping (#34; [contract](aromatic_interaction_workflow.md)). Prepared
  analytical controls do not establish biological complex validation.
- [ ] Native structure-based hypotheses using TopOMT pockets and MolSysMT molecular geometry.
  The explicit cached hypothesis constructor and historical facade transition
  are delivered under #44. Automatic provider-informed directions/pockets and
  biological qualification remain separate from this controlled projection tool.
- [x] Public common-frame hypothesis composition and named native interaction-collection conversion (#36), with labeled evidence, explicit keep/participant-reuse policies, independent controls and preserved empty/failure semantics. Disconnected prepared controls do not establish biological complex acceptance.
- [x] Joint native interaction controls with complete frozen CCD EST/DES molecules (#37), two caller-declared rigid placements and both participant roles. Existing public tools retain neutral empty families, duplicate-profile evidence, directional controls and an independent DES steric veto; designed CCD pairs do not establish biological complex acceptance.
- [x] Independent cached-model selection, copying, extraction and explicit constraint editing (#38), with class delegation, source-model history, score invalidation, distinct radius/sigma semantics and independent essential/weight/exclusion controls. Source/API acceptance was resolved on 2026-11-03; activity-based comparison remains open.
- [x] Standalone exclusion-sphere construction from cached MolSysMT heavy-atom geometry, with explicit constant-radius choices, independent veto controls, native persistence and an observed receptor continuation (#32). Physical-radius/surface/pruning strategies and biological validation remain open; do not infer steric volumes from inactive-only features.
- [ ] Refinement, validated I/O and inspectable MolSysViewer/DockingMT workflow integration.
- [ ] Execute the chosen public vertical pilots with declared preparation, independent controls and no leakage.

### 3. Product and ecosystem closure
- [ ] Complete molecular geometry delegation to MolSysMT (#41 / #375).
  Prepared class/default transitions and obsolete utility/reader retirement are
  delivered under #18/#42/#44/#45/#46. The remaining bounded donor-H arithmetic
  in `get_features()` is limited to the qualified historical public provider without
  vectors. Current source consumes public `structure.get_vectors`; removing the
  compatibility branch requires supported public delivery/receiving (#41 review
  2026-11-11). Ideal acceptor geometry and provider scientific acceptance retain
  their separate contracts.
- [x] Implement own deferred native Ackredit capture and portable bibliography (#19); see [the cookbook](../docs/content/cookbook/attribution.md).
- [ ] Review the attribution contract and verify optional-integration distribution support (#6, #19).
- [ ] Confirm production dependency/distribution closure (#10) and required hosted CI evidence (#9).
- [ ] Verify independent routes for all three traditional modeling approaches before claiming consolidation.
- [x] Collect validation/benchmark cases through the existing documentation and original evidence archives (#20; publication/layout decision, contribution template, ownership/execution policy and frozen CCD demonstrator).

### 4. Measured acceleration and future contracts
- [ ] Profile representative matching/search workloads after establishing reference equivalence guards.
- [ ] Introduce Rust for measured pharmacophoric bottlenecks; molecular kernel ownership stays in MolSysMT.
- [ ] Design bounded arrays/membership data and deterministic reductions for parallel/distributed or GPU execution.
- [ ] Extend relations, uncertainty, coordinate frames and ensemble contracts as advanced methods need them.

Scientific method, compute backend and execution plan remain independent axes.
No Rust, GPU or distributed PHMT implementation is claimed by the current slice.

---

## Gen 2: Dynamic Modeling (Dynophores)
- [ ] `TrajectoryExtractionPipeline`: generate pharmacophore lists from MD trajectories.
- [ ] Native MSM engine: pharmacophore objects as nodes in a kinetic network.
- [ ] PCCA+ for metastable macrostate discovery.
- [ ] Vectorized `molsysviewer-pharmacophoremt` UI add-on.

## Gen 3: Specialized Horizons
- [ ] Peptide and macrocycle hierarchical modeling (backbone motifs + sidechain hotspots).
- [ ] Covalent pharmacophores (Warhead features with reaction geometry).
- [ ] Water-Replacement modeling from solvent MD (high-energy hydration sites).
- [ ] Quantum-Enhanced Pharmacophores (QEP): ESP integration.

## Gen 4: AI & Generative Synergy
- [ ] 3D Spatial Graph exports for GNNs.
- [ ] Diffusion-based generative blueprints (tensor/voxel representations).
- [ ] Multi-objective optimization (Anti-Target negative pharmacophores for toxicity).
- [ ] Ultra-large scale screening using 3D Pharmacophore Fingerprints (3DPFs).
