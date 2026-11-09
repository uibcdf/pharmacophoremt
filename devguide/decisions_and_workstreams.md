# Decisions and active workstreams

Handoff reviewed 2026-11-07 UTC. Use the [checkpoint](checkpoint.md) for current
actions and [roadmap](roadmap.md) for order. Owning contracts/issues and original
evidence retain finer-grained authority than this orientation page.

## Decisions to retain

| Decision | Reason and consequence | Authority |
| --- | --- | --- |
| General molecular tools stay in MolSysMT | Chemistry/formats/preparation/geometry must serve other consumers; request missing tools in their owner | [Suite map](../MOLSYSSUITE_GUIDE.md#component-responsibility-map), [capabilities](capability_inventory.md) |
| Explicit native methods replace defective legacy automation | Prepared inputs and chosen rigid/aligned/cached methods prevent hidden scientific substitutions | [Ligand transition](ligand_based_workflow.md), #18; [structure workflow](structure_based_workflow.md), #44 |
| Hypotheses and completeness remain inspectable | Preserve alternatives, omissions, finite budgets and failures instead of silently switching methods | [Generation](public_receptor_generation.md), [semantics](native_constraint_semantics.md) |
| Cache consistency is not authenticated provenance | State/frame/unit/selection checks cannot prove the cache came from its claimed source | [Provenance](native_provenance_persistence.md), #89 |
| Separate analytical, preparation, biological and performance evidence | Correct geometry or a successful build cannot establish predictive power | [Collection](validation_collection.md), [audit](audit_20261104.md), [addendum](audit_20261104_review.md) |
| No mandatory favorable EF/AUC/LOO outcome | Scientific quality comes from declared labels, comparators, leakage controls, uncertainty and honest negative/inconclusive results | [Two-study objective](pending_proposals/qualify_receptor_screening_studies.md), #103 |
| The active destination is a mature pre-1.0 0.x | Liliana accepts seven capability milestones and as many useful intermediate versions as needed (2026-11-07). The final minor may be0.23,0.40 or another0.x; versions group delivered work, and the1.0 decision is separate and later | [Accepted staircase](roadmap.md#accepted-destination-a-mature-pre-10-0x), [readiness](release_0_5_0_readiness.md), #95 |
| Every implementation increment leaves a usable developer-guide checkpoint | Liliana requires actual implementation/evidence/limits and the next concrete action to remain recoverable from devguide. Update the owning contract/workstream with changed facts and preserve historical measurements; a plan or narrow green check is not completion evidence | Maintainer instruction2026-11-07, [checkpoint](checkpoint.md), [local instructions](../AGENTS.md) |
| Each intermediate release solves a usable public task | Guided use, detailed public composition, documentation and checked installation grow together. Integrate, simplify or retire prototypes after their decision evidence is sufficient; validation and product work proceed in parallel | [Milestone acceptance](roadmap.md#accepted-destination-a-mature-pre-10-0x), #108/#95 |
| Addon work is deferred | Source/payload code exists; live-browser qualification remains separate | #58, [viewer planning](visualization_strategies.md) |
| Principal-maintainer delivery uses direct commit/push and deliberate CI checkpoints | Liliana explicitly authorizes this route and requests `[skip ci]` for routine/small commits (2026-11-06); batch pushes and retain scope-appropriate local checks, with pending exact-head evidence under #9 | [Local instructions](../AGENTS.md#principal-maintainer-delivery-instructions), [checkpoint policy](../MOLSYSSUITE_GUIDE.md#direct-pushes-and-validation-checkpoints), #9 |
| Controlled source is distinct from public delivery | A passing subset/provider source cannot qualify a public package or full installed/platform matrix | [Public receiving](public_dependency_receiving.md), #10/#23/#95 |

## Current workstreams

[#165 pinned r95 build](pharmer_r95_build_receiving.md) advances source/diagnostic
readiness for milestones1/6:66original files and15private dependency artifacts
are received; the legacy-ABI/SDF dependency probe passes. Both core/GCC collector
profiles reach the unchanged group512MiB monitor limit. No Pharmer binary or
engine result exists. Keep165partial, stop both compiler routes and receive a
distinct managed resource context; continue independent library/provider work.

[#164 external P1preparation](pharmer_p1_external_admission.md) freezes build/CLI/
resource/output admission and three real MolSysMT exports without changing runtime
code or external execution. The same17original source/existing-owned-wheel198cases (5new/12P1) and complete
three-case export driver pass. All214payload/159runtime files,14fixtures and
155loaded runtime origins verify without checkout fallback; preparation resolves. This advances comparison readiness for
milestones1/6, without qualifying the unavailable build, perception or native maps.

2026-11-09: [#163 supported Pharmer profile](pharmer_interoperability.md) adds
warn/raise/ignore, detached reports and persisted loss audit, while retaining
#162 omission and correcting inactive vectors. Source141selected cases pass
(48new/93existing);35original red guards are preserved. Actual public donor
evaluation confirms off/on behavior. The same141original bodies, three ordinary profiles and complete P1driver also
pass from exact b4b062a owned wheel198:214payload/159runtime files,12fixtures and
155loaded runtime origins verify. The bounded bridge resolves; external engine
qualification remains separate.

2026-11-09: [#162 enabled-point import](pharmer_interoperability.md) now omits
disabled points before parsing, defaults missing flags to true and rejects other
types with the existing catalog diagnostic. Filtered-only metadata records dense
site/original-point mapping; native persistence preserves it. All34 selected source
cases pass,22new/12P1, and two ordinary profiles retain exact native JSON bytes.
The unchanged example has ten enabled of19original points; legacy count assertions
are corrected. Original red/unit-control identities and the full-attachment
resource gate stay separate. The same34original cases, two ordinary
profiles and complete P1driver pass from exact0407e20 owned wheel196, with211
verified payload files, nine fixtures and152loaded runtime origins. The bounded
source/installed bridge resolves. The supported scientific import/admission profile is received separately under#163; no external engine
execution or general field-equivalence claim follows.

2026-11-09: [#161 P1 preparation](pharmer_p1_comparison.md) freezes an exact
three-site query, two proper-motion/permutation positives and a provably
impossible stretch. All29 final selected source cases pass,12new/17existing,
including enabled/disabled attribution; the driver retains three correct answers
and actual nine-item/22-use attribution. The original legacy-scope memory refusal,
private whole-file native hashing failure and extra-metadata comparison error
remain recorded. Recovery preserves frozen inputs, runtime and budgets; actual
current provider metadata is pinned separately. The same
29 original cases and complete driver pass around owned wheel192; 152 loaded
runtime origins and eight fixture files verify. The initial stale Sabueso finder
refusal and current provider mappings retain separate identities. Preparation#161
resolves; actual Pharmer perception/search
is unexecuted and separately gated. Public disabled-point loss is recorded in
[#162](archive/pharmer_disabled_points.md), outside P1's enabled subset.

2026-11-09: [#160 numerical candidate admission](pair_distance_pruning.md)
corrects PHMT's pair filter conservatively without changing final matching or
physical radii. All116 selected source cases pass,12ordinary outputs/counters
remain identical, and the original public ion body fails with the old module
and passes with the corrected one. Source evidence preserves the explicit
DATA512/AS1GiB/observed-group-RSS512 local profile and prior mapping failures;
this does not qualify#148. The same116bodies pass from exact65991c3 owned
wheel192; the [installed receipt](evidence/pruning_slack_installed_20261109.json)
retains the original post-suite path-comparison failure and successful separate
metadata/origin/native postcheck. Twelve ordinary outputs remain equal;211payload
files and150loaded runtime origins verify. The bounded#160bridge resolves.

2026-11-09: [Pharmer query/pruning review](pharmer_query_pruning_review.md)
authenticates24official standalone r95files and retains12unexecuted comparator
cases. Query meaning, candidate filtering, final acceptance, scoring, numerical
representation and limits remain distinct. Three stdlib/Fraction controls confirm
PHMT's literal site/pair allowance mismatch under#160. The original study leaves
public/native reproduction/correction/guard/installed receiving pending; the
subsequent correction above has separate evidence. Canonical
Discussion#131 publication is separately recorded in#128. No competitor,
molecular, benchmark, index/adapter or dependency-adoption result follows.

2026-11-09: [#159 complete inspection journey](archive/document_saved_inspection_journey.md)
executes public progress/status/detail together in one snapshot.40distinct
parameter cases pass from source and the unchanged owned188reader,80accepted
executions with five unchanged files and30original full details per context.
Eight accepted fresh commands include the expected two ambiguous-key refusals;
explicit equals values retain opaque/zero-match identities. Strict docs/Ruff pass.
No runtime/API/dependency change or new wheel is introduced. The initial private
SDK-checker dependency-admission failure is preserved; only failed installed
receiving repeats using the existing QA route. MolSysSuite#176 receives the
nonblocking tool improvement. Full supported/biological/scale gates remain open.

2026-11-09: [#166 exact source selection](saved_work_selection.md#exact-source-selection--166-2026-11-09)
adds source/status intersections on original work mappings through the owned
reader and CLI. Source120selected cases and eight unchanged original command
outputs pass; owned installed receiving remains pending. Provider collections
remain MolSysMT#624-owned; neither a connector nor scale qualification follows.

2026-11-08: [#158 saved-work status selection](archive/select_saved_work_status.md)
adds a public metadata-only iterator filter and independent command. Four exact
statuses preserve original manifest positions, pending drafts and valid-zero
distinctions. Source99bodies (14new/85original), four unchanged ordinary outputs,
strict docs and local governance pass. The same99bodies pass from exact153ea50
owned installed receiving, with93guarded children/eight documented commands on
four unchanged historical files. The bounded bridge resolves. No collection,
scoring, molecular acquisition or performance claim
follows; filtered offsets belong to one verified snapshot.

2026-11-08: [CDPKit lifecycle study](cdpkit_library_update_review.md) authenticates
ten source blobs at v1.3.0/a8c7985 and refines earlier update/duplicate uncertainty.
Nine unexecuted cases distinguish provider collection policy from PHMT feature/
search-asset compatibility. This is documentary/source receiving under#128, not
an engine adoption, runtime/collection implementation or scientific benchmark.
Reporting/index/link and source-integrity checks pass; canonical publication
readback is separately owned by#128. The original outdated #140 report link is
corrected without changing its archived evidence.

2026-11-08: [#157 single-work detail](archive/inspect_saved_work_item.md)
adds the public exact-key reader and command. Confirmed match/zero/failure and
pending work retain original evidence/status/attempt meanings; drafts stay hidden.
The final85source case scope includes16new and69original controls. Strict docs/
local governance pass. The same85 bodies pass from exact3e45a58 owned installed
receiving;72guarded children and eight documented commands preserve four original
historical files. The bounded bridge resolves. No molecular,
scale, biological or full public delivery claim follows.

2026-11-08: [#156 bounded work inspection](archive/inspect_declared_work_cli.md)
exposes original manifest mappings, including unconfirmed work, through a
paginated independent command. Source69 selected controls, strict full docs and
local governance pass. The same69 original bodies also pass from the exact
5d77c9c owned wheel;59guarded children and eight documented commands on four
unchanged historical databases verify. The bounded installed bridge resolves.
Complete verification and original reader/ranking/export behavior stay intact;
no molecular calculation, new acquisition route or scale claim follows.

2026-11-08: [#155 BEDROC precision](archive/bedroc_small_alpha.md) corrects
underflow for valid tiny alpha using the existing ROC-AUC limit. Six original
failures/23 passes become 179 selected numerical/saved-analysis passes; 138
ordinary outputs and the original exponential AST remain unchanged. Strict
documentation passes. The same 179 bodies/138 exact ordinary values also pass
from the owned 0.4.0+181.gc8c4dfd wheel outside checkout, with runtime/fixture/
provider identities verified. The bounded bridge resolves; no molecular,
biological, supported public-platform or performance claim follows.

2026-11-08: [serial acquisition terminal receiving](feature_reuse_measurement.md#serial-acquisition-limit-received-2026-11-08-utc)
at b1139d0/run42494894038 verifies actual manager identity/effective1/1settings,
but extraction still fails within the unchanged memory/task envelope. No native
case executes. Stop the exhausted profiles and hand the measured limit to the
environment/resource owners; independent product work remains active.

2026-11-08: [serial acquisition](feature_reuse_measurement.md#serial-acquisition-prepared-2026-11-08-utc)
is prepared through the same SDK, with effective extraction/download settings
of one and early official-manager identity checks.46focused cases/21admission
guards and a real config-only consumer probe pass; actual transaction/native
receiving remains pending. Resource budgets, pins and original failures remain.

2026-11-08: [#153 fixture lifetimes](archive/administrative_sqlite_lifetimes.md)
are corrected after tracing 15 warnings to five owned connections. Original
transactions/assertions remain; 42 selected and 156 full administrative cases
pass under unchanged local limits, without SQLite warnings. Separately,
[native admission recovery](feature_reuse_measurement.md#bootstrap-admission-and-transaction-limit-2026-11-08-utc)
receives actual bootstrap kernel controls/cleanup at d95617d/run42461400749,
resolving #154. Package extraction then exceeds the unchanged acquisition
budget; the whole run fails and molecular tests remain skipped. Inspect manager
concurrency before further requests; retain both failures and all original inputs.

2026-11-08: the first native request at cdb9d45/run42460786720 fails before
service admission; no molecular case executes. The
[#154 correction](archive/native_qualification_service_oom.md) uses supported
OOMPolicy=kill and prepares only the private manager root for cleanup. The
original failure and unchanged resource/scientific declaration remain explicit;
real hosted recovery is pending.

2026-11-08: [native fixture admission](feature_reuse_measurement.md#native-fixture-admission-prepared-2026-11-08-utc)
is implemented as a fixed manual workflow/common-SDK client, with2GiB acquisition
separate from512MiB native87-case scope. Local154administrative cases/16admission
guards pass; actual hosted native execution remains pending. #151workflow
classification and#152complete-CSV memory defects are resolved without data or
budget changes; original failures and#153SQLite warnings remain visible. No
measured arm, original-input pilot or molecular performance is inferred.

2026-11-08: [#148 hosted scope qualification](feature_reuse_measurement.md#hosted-scope-probe-declared-2026-11-08-utc)
receives exact9a0ed14/run42453432613/attempt1 using standard systemd controls in
one managed VM. The fixed512MiB/zero-swap/32-task/one-CPU kernel limits, actual
affinity/priorities and parent/child membership verify; the24MiB smoke passes.
Its cumulative peak at held-payload samples is separate from lifetime/RSS or
performance evidence. Native context, authorized input handoff, shared arm and
two-arm pilot remain pending. No shared-workstation control/provider is changed.

2026-11-08: the [next accumulated source checkpoint](plan_api_ci_checkpoint.md)
accepts27c1178 for147/150and148/149developer controls with unchanged acquisition,
workflows and policy. Source42451906584/attempt1 passes2505full-suite cases in
each of all eight Linux/macOS arm64 Python3.11–3.14cells, with zero reported
skips/43warnings per cell. Reporting, policy42451909669 and no-build publication
governance42451913187 succeed. Full commands, acquisition, architecture/interpreter
and all106-file XMLs verify. Original initial/frozen runs retain their identities;
no redispatch occurs. Public/installed delivery, native measurements, biology and
mature0.x gates remain separate. Next qualify the existing87public-fixture
native controls inside a newly verified512MiB scope before a measured shared arm.

2026-11-08: [#150 plan inspection](archive/inspect_prepared_run_plans.md)
adds `PreparedRunPlan.describe()` and compact repr, with22selected source cases
and the exact public metadata-only recipe passing. Fields/schemas and15existing
construction/resume bodies remain unchanged. One owned wheel passes the same22
bodies/recipe with150loaded runtime modules verified; the bounded bridge resolves.
Original source/owned version-file fingerprints remain distinct, and changed
source identity still affects conservative reexecution binding.

2026-11-08: the [chemical-library user guide](../docs/content/user/chemical_libraries.md)
connects the source-operation matrix and guided/expert plan/run/resume/inspect/
export routes. Existing executable examples are unchanged; strict rendering and
the corrected link retain their own receipt. No named connector, new calculation,
human-usability or installed/public qualification is inferred.
The actual-link audit also resolves[#149](archive/docs_contributor_footer.md),
with four template guards and82real footer targets verified.

2026-11-08: [#148 molecular feature-reuse measurement](feature_reuse_measurement.md)
declares48balanced pairs with charged inventory build cost and a separate
two-arm pilot.22offline guards and three original snapshot hash checks pass.
Native driver, safe route and measurements remain pending. The original native/
DATA failure is not retried or enlarged; independent#108coverage work continues.

2026-11-08: [#147 paired saved-run comparison](archive/compare_saved_screening_runs.md)
is implemented after31missing-operation failures/one positive old-batch control.
It reuses the existing public summary and exact old paired tail, with32initial
focused passes and256distinct selected passes including33new guards. The exact
public recipe, strict docs and administrative checks pass:301distinct selected
cases overall. Exact owned installed receiving passes the same256bodies/35guarded
children and recipe; real optional attribution retains4items/13uses. The bounded
bridge resolves; original fixture/Ruff/old-plan harness failures are preserved.

2026-11-08: [accumulated source checkpoint](saved_run_ci_checkpoint.md) accepts
frozen5c3cd64/attempt1 for#144/#145/#146. Source42436392248 passes2430cases per
eight Linux/macOS Python3.11–3.14cells, with reporting/policy42436396390 and
publication governance42436399981successful. Native full commands, interpreter/
architecture/acquisition and106-file qualified coverage are verified. Later147
is outside that frozen scope and has separate27c1178 receiving above; no existing
run is restarted/relabelled.

2026-11-08: [public provider revalidation](evidence/public_molsysmt_availability_20261108_summary.json)
still identifies the same0.23.0main artifact and older missing-modern-API gate.
Actual Linux/macOSarm64 release/index rows verify;1.0.0remains staging-only.
No provider execution/solve/floor change occurs. Wait for an identified supported
new main file/owner handoff before repeating public receiving; independent product
and measured molecular-reuse work retain their own next actions.

2026-11-08: [saved-run cohort analysis](saved_run_analysis.md) under#146 passes
268selected source cases, one exact analytical recipe and strict source/Sphinx
rendering. It reuses existing metrics and preserves native evidence; pending,
native failure and upstream unavailability remain separate. Exact installed
receiving passes223same bodies/the recipe and75overlapping independent-reader
bodies/16commands, with4actual attribution items/12uses. The original broader
local native/resource failure stays under#9/#23,
with older-provider diagnostic evidence reported to existing MolSysMT#601.

2026-11-08: [immutable saved-progress reuse](saved_progress_reuse.md) resolves#145
with175selected source cases, nine declared pairs and67same-body owned installed
cases. Repeated10000-record progress medians497.892380→0.103223ms apply only to
an already-open synthetic snapshot; first admission/scan and full supported gates
retain their cost/scope. [Checkpoint](checkpoint.md) owns the next concrete action.

| Lane | Actual state | Next evidence |
| --- | --- | --- |
| Mature pre-1.0 0.x staircase | Public runs/released-reader support, guided/expert parity and API/CLI complete exports received in bounded contexts | Deliberate exact-head validation of accumulated changes; retain every unresolved gate in [roadmap](roadmap.md) and [checkpoint](checkpoint.md) |
| #103 receptor-to-screening studies | Objective accepted; neither full biological study is complete | Admit original methods/data/cohort/preparation, freeze receptor/comparator/evaluation and execute |
| #66 ERalpha binding | Frozen source pools/exposure persist; original Sun2006, Xin2023, Gungor2006 and Scott2023 methods unresolved | New authorized access lead; don't repeat exhausted routes or alter frozen queries/thresholds |
| #106 second-target admission | Nine fixed leads reviewed; capacity/coupled outcomes and seven held sources remain separate | Resolve original material/data/curation authority; further unresolved-domain review needs a new declaration; no activities admitted |
| #108 public-library workflow | Public runs, reader support, guided/expert parity, exports/progress, single/paired analysis and plan inspection received in bounded source/owned installed contexts;27c1178 full source accepted | Broader human usability/source operations and [MolSysMT #624](https://github.com/uibcdf/molsysmt/issues/624) remain; no blanket connector/index/durability/biological promise |
| #142 native inspection | Resolved: Point center alias and empty-coordinate shape corrected; same338 source/owned-wheel bodies and two isolated children pass | Full supported source/installed/public gates remain separate |
| #143 analytical boundary | Resolved: original fixture exactness defect preserved; revision2/14guards/ten-case driver and frozen8db2a53 full2357-case/eight-cell source gate pass | Later helpers/tests and full installed/public/platform delivery retain separate#9/#23 scope |
| #144 saved-reader performance | Resolved: three reader cells/75baseline samples and reusable copied-fixture recovery received with22guards | Preserve failed original preparation; extra25samples stay separate. Review shared scan cost before any cache/index/molecular throughput claim |
| #148 molecular feature-reuse performance | Partial: fixed prospective schedule/control and original input integrity verified | Receive a safe native route and qualify a shared arm, then separate pilot/measurements; no speed or library-capacity claim |
| #128 tool-study registry | Dedicated public index, one [executed Pharm3D analytical comparison](rdkit_bounds_comparison.md) and nine documentary records | Public RDKit fields are received in source/one owned wheel under resolved#140; corrected8db2a53 source passes all eight cells under resolved#143, preserving failed489be12. Broader comparison/biological gates remain |
| Molecular providers | #105 receives native aromatic-N; carboxylate, constrained H refinement and grouping retain specific gaps | MolSysMT#375/#323/#447; supported provider operations, no local replacement |
| #95 intermediate release | Proposed0.5 reviewed; actual plan/tag/Release0.4.0 | Public provider capability and exact source/installed/public gates before a freeze |
| #9/#10/#23 CI/support/distribution | [Frozen27c1178](plan_api_ci_checkpoint.md) passes all8 source cells/2505cases each plus reporting/policy/publication controls; later9a0ed14 OS probe has its separate manual receiving | Full installed/public/package and later-head gates stay separate; no repeated frozen run |
| #6/#41/#74 ecosystem debt | Partial support adoption; bounded old-provider donor compatibility and SDF container migration remain | Receive owning provider contracts; annotated-SDF delegation is MolSysMT#215 |
| #43 historical resources | Some `/tmp` producers/papers are absent; tracked support is intact | [Migration inventory](machine_migration.md): distinguish reconstruction from original recovery |

TopoMT pockets are optional to current cached hypotheses. DockingMT integration,
dynamics/MSM/AI and accelerated/distributed methods are future lanes, not hidden
prerequisites or delivered functionality. Support libraries follow their canonical
guides; [support boundaries](support_library_boundaries.md) tracks actual adoption.

## Resume science deliberately

Migration alone does not execute a scientific plan. Deliberate resumption now
received #106's declared single-AID capacity, after verifying the published plan
and unchanged source identities. Strong IC50≤0.5 versus weak IC50>5 micromolar
remain assay-specific reported potencies, not general inactivity or independent
molecules. AID1805333 stops:32 eligible weak SIDs cannot meet50 per class. Preserve
the91 missing relations rather than assuming equality, and record the stop before
a new source nomination. A passing later raw count would still need MolSysMT
chemical/state/series grouping, preparation, and complete PHMT material/exposure/
interference admission before receptor/comparator choices and scores are frozen.
Do not pool patents, tune on outcomes, relax labels or replace failures. Both
studies remain open until the complete declared evidence actually exists.

The [follow-on review](receptor_study2_source_lineage_review.md) records shared
publication evidence for AID 1795677 without transferring the earlier class
counts or asserting molecular equivalence. AID 1797292's original method is now
received, but original table units and material/species are unresolved; a failed
PDF receiving attempt does not qualify a page or authorize unit/species transfer.
A [separate recovery](receptor_study2_pdf_recovery.md) now verifies the complete
PDF and bounded visual review; original table-unit and actual material authority
still require source clarification before activities.
The [fourth-source review](receptor_study2_fourth_source_method_review.md) reuses
the originalUS9763922 HTML and verifies fresh1797167 metadata. Its exact AlphaLisa
method correspondence and explicit FormulaII table units are positive documentary
evidence; experimental material and individual-row mapping remain unresolved.
The [2061300 review](receptor_study2_fifth_source_method_review.md) now supports
original FP-derived inhibitor Ki in nM, distinct from tracer Kd. The incorporated
PCT states Ki/30 min; historical metadata hashes support a dated correction
of our old "KD title" description without changing original KO/US `30 mM` bytes.
Material, tracer and individual-row authority remain pending. The
[1798835 review](receptor_study2_sixth_source_method_review.md) now supports the
BD1 K57–E168 TR-FRET Ki column in µM and preserves the separate BD2/cellular
contexts and literal BD2 boundary conflict. Actual material, probe Kd/calculation
and row authority remain pending; unrelated curator annotations do not fill them.
The [last three reviews](receptor_study2_remaining_sources_review.md) now cover
1805218/1805772/1804941. Source 1805218 has conflicting predicted/experimental
prose and a 134-record numeric table; no three-record capacity bound follows.
Actual material/controls/curation and source-specific interval transfer remain
pending. All nine fixed leads have bounded outcomes, with no newly admitted
activities. Draft authority questions remain unsent; 19 unresolved-domain records
are not silently excluded or promoted.

## Public libraries and complete unresolved metadata receiving — 2026-11-06

The [19-source receiving](receptor_study2_unresolved_domain_receiving.md) verifies
all source identities/fields in one response; all remain domain-unresolved and
the nine earlier outcomes stay intact. No new activity cohort is admitted.
The user also requests both retrospective validation and new-library screening.
[Provider research](public_library_support_research.md) proposes a common library
workflow and records access/3D/implementation limits. It is a product design
input, not implemented library support, new scoring or retrospective acceptance.
Generic molecular collection reading/preparation remains MolSysMT-owned.
