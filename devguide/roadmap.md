# Strategic roadmap

Maintained 2026-11-07. Read [checkpoint](checkpoint.md), [capabilities](capability_inventory.md)
and [decisions](decisions_and_workstreams.md) first. The former detailed delivery
log/checklists remain in [roadmap history](roadmap_history_20261106.md); old
checkboxes record historical code, not current scientific/public qualification.

## Accepted destination: a mature pre-1.0 0.x

Liliana accepted the following staircase on 2026-11-07 and then resumed the work:
finish the pending increment and pursue a powerful, intuitive, scientifically
supported **0.x** product. The final minor number follows completed scope; it
may be 0.23, 0.40 or another 0.x. No final number, date, release freeze or automatic
1.0 transition is reserved. Milestones describe capabilities; versions group
useful delivered changes. One milestone may need several versions, and one
version may advance several milestones.

| Milestone | Usable result and acceptance | Current evidence and remaining work |
| --- | --- | --- |
| 1. Coherent classical core | Generation, composition, correspondence, alignment, evaluation and scoring preserve compatible feature, geometry, unit, identity and failure semantics. Public contracts and reproducible controls explain supported domains and incomplete answers. | Native routes and scoped controls exist in the [capability inventory](capability_inventory.md). The [feature-reuse subworkflow](feature_inventory_reuse.md) now has equal native evidence under its declared scope. Close remaining observed gaps before changing cache/search contracts. |
| 2. Complete public workflow | A user imports prepared data, builds/loads a query, inspects a plan, screens, resumes and exports through documented public operations. Guided and expert routes resolve to the same effective settings. | The [public iterator](public_prepared_screening.md) and [recoverable runs/independent reader](public_prepared_runs.md) pass their selected cases and source/owned installed recipes. Full guided/expert usability and supported installed/public gates remain open. |
| 3. Robust molecular collections | Provider-owned records, molecules, states, conformers and atom/source mappings have explicit resource, preparation, bounded iteration, snapshot and recovery contracts. | The fixed [PubChem3D case](pubchem3d_receiving_pilot.md) qualifies individual artifacts only. Receive the reusable boundary from [MolSysMT #624](https://github.com/uibcdf/molsysmt/issues/624); PHMT must not add a replacement molecular parser or collection. |
| 4. Progressively qualified public libraries | A common user journey supports selected sources and formats, with separately demonstrated discovery, download/import, preparation, screening and availability operations and their access conditions. | [Source assessments](public_library_registry.md) and the three-record pilot do not establish general connectors. Qualify each selected operation/source increment; the mature-release scope names the selected sources and remaining exclusions. |
| 5. Efficient repeated queries and screening | Reusable annotations, scans and indexes are compared on equivalent problems, including build/storage, cold/repeated-query cost, memory, invalidation and coverage. Acceleration addresses measured bottlenecks. | The [in-memory reuse experiment](feature_inventory_reuse.md) passes its equality controls and public recipe. No cache/index strategy or speedup follows from fewer outer requests; broader workload/resource evidence remains required. |
| 6. Reproducible scientific validation and comparisons | Admitted retrospective data, leakage controls, simple references, uncertainty and complete failure denominators support reproducible evaluations. Comparisons explain equivalent or differing scientific problems. | Neither #103 biological study is complete; #66/#106 source/admission limits below remain binding. [Tool records](pharmacophore_tools_registry.md) distinguish documentary study from executed comparisons. Product increments can progress while these independent scientific gates remain open. |
| 7. Mature usable pre-1.0 0.x | The selected classical scope, guided/expert workflows, source operations, traceable results and measured performance form a coherent installed product. Documentation and compatibility match actual public delivery. | Freeze a candidate only after its declared scope and exact source, dependency, installed/public/platform gates are satisfied under #9/#10/#23/#95. Source prototypes and selected local tests alone cannot establish this milestone. |

User experience, documentation, validation and implementation advance in parallel
from the first increment. The staircase orders dependencies and acceptance, not
seven isolated development phases. Molecular-provider work retains its owner;
an unresolved provider feature does not stop independent PHMT contracts, examples,
user testing or result interpretation.

Each intermediate version must let a user complete a concrete public task or
substantially improve one. Its preparation names scope and acceptance, public
API/examples, appropriate scientific or technical evidence, checked installation,
compatibility and migration limits. A prototype resolves uncertainty; once the
evidence suffices, integrate, simplify or retire it with a recorded reason rather
than making another prototype the only delivered result.

Every implementation increment leaves [checkpoint](checkpoint.md) usable for the
next session: actual implementation state, evidence/source identities and limits,
unresolved gates, and the next concrete action. Update owning contracts and
workstreams as their facts change; keep historical measurements and failures
under their original identities. Plans and successful narrow checks are not
completion evidence for the staircase. Routine `[skip ci]` delivery and deliberate
full validation checkpoints retain their separate authority.

## Acceptance across the staircase

- **Usability:** representative novice and expert users complete named tasks
  with the documented public interfaces. Record help needed, obstacles and
  recovery from errors; compare guided and expert effective settings/results.
  A short example alone is not evidence of an intuitive user experience.
- **Library coverage:** maintain a source-by-operation matrix for discovery,
  acquisition, import, preparation, screening and updates/availability. Each
  cell names its demonstrated scope, access conditions, unsupported cases and
  evidence. One successful source operation does not qualify all operations.
- **Scale:** declare representative workload sizes, query mixes, hardware and
  resource budgets before performance measurements. Retain build/storage cost,
  cold/repeated-query cost, omissions and failures; a three-record pilot does
  not establish large-library capacity.
- **Continuity:** declare API and saved-result compatibility as contracts mature.
  Test supported old readers/results, explicit migrations and incompatible-run
  rejection. Preserve original evidence and distinguish relocatable identity
  from byte provenance and chemical equivalence.

Releases are selected from completed useful tasks, such as public prepared-input
screening/export, recoverable runs, a first qualified source, a broader source
set or measured repeated-query improvements. These are candidate increments,
not reserved version numbers. Each release independently meets its declared
installation/distribution gates; passing one task does not close its milestone.

## Immediate product increment

The previously pending [feature-reuse experiment](feature_inventory_reuse.md) is
measured: 87 selected scientific cases, full native evidence equality for six
original-source/reference comparisons, and four executed public cookbook blocks.
It retains post-fit validation and distinguishes selected-prefix work from full
search. It adds no persistent cache/index or speedup claim.

The public gap audit selected a separate prepared-input iterator because the
existing facade owns global hit ranking and complete caches. `PreparedInput` and
`screen_prepared` now have one public runtime implementation, definition-owned
admission, structured diagnostics and actual per-evaluation attribution.89 source
controls and the query/prepared-file/export recipe pass. The identical owned wheel
also passes that recipe outside the checkout, as recorded in the
[public contract](public_prepared_screening.md). The separate
[public recovery/results task](public_prepared_runs.md) now passes197 selected
local cases, source/same-wheel installed interruption/resume/export, independent
guarded readers and the migrated original-input callback. Normal editable receiving
also passes with identical runtime code and no provider changes. The
[released-support reader receiving](reader_public_provider_receiving.md) now
measures four bounded cells and selects SMonitor>=0.22.1 from actual missing-error
observations on0.19. Guided/expert parity and query-error recovery are measured;
full source/installed/public gates remain separate.
Managed molecular collections
remain MolSysMT#624-owned; source work is not full milestone2 delivery.

The dated [pause record](evidence/reader_public_providers_20261107_checkpoint.json)
retains its pending-delivery state. Resumption verifies the saved source unchanged
and seals the [own/scalar receiving evidence](evidence/reader_public_providers_20261107_summary.json).
The [guided/expert comparison](guided_expert_journey_receiving.md) now preserves
full effective/native/export equality and fixes the observed cookbook query-error
retry trap in source and the same owned wheel. It is no human usability study.
The [complete-view exporter](saved_result_exports.md) passes15 export/21 reader
bodies from source and the same exact owned installed artifact. Four authentic
original saved databases retain full evidence/configuration and scalar projections.
Next expose CLI export through these same public methods, then continue broader
usable source operations from the [checkpoint](checkpoint.md). The public-support
reader slice does not qualify a full PHMT dependency solve or platform matrix.
No release or full supported gate is established by this reader increment.

## Current priority: classical consolidation

The accepted longer-term objective under [#103](pending_proposals/qualify_receptor_screening_studies.md)
is a reproducible prepared-receptor-to-pharmacophore-to-screening workflow,
evaluated on ERalpha and a scientifically justified second receptor. A third
party should recover inputs/plans/models/results and understand assumptions,
sensitivity, failures and useful or negative results. Neither study is complete.

1. **Restore a qualified development context after migration.** Follow
   [onboarding](onboarding.md) and [migration](machine_migration.md); preserve
   historical source/native identities and create fresh receiving evidence.
   Destination receiving passes23 scoped controls; global closure still has the
   known TopoMT/Numba gap. This does not recreate the historical fixed-source CI
   context or clear source/installed/public gates.
2. **Admit data before models/scores.** Keep #66's fixed method/exposure gates.
   #106 prioritizes BRD4, not an accepted target/cohort. Its
   [original-method review](receptor_study2_primary_method.md) supplies a
   [prospective single-source capacity plan](evidence/brd4_activity_capacity_plan_20261106.json).
   Its [executed outcome](receptor_study2_label_capacity_receiving.md) stops
   AID1805333 at32 eligible weak SIDs against50 required. Record that source stop
   before a new dated nomination; necessary capacity never proves independent groups.
   Follow-on [lineage review](receptor_study2_source_lineage_review.md) identifies
   1795677 as coupled publication evidence. The [1797292 method review](receptor_study2_third_source_method_review.md)
   leaves original units/material unresolved; resolve those before activities.
   The [PDF/PCT recovery](receptor_study2_pdf_recovery.md) now qualifies receiving
   and bounded visual review, while the original unit/material gap persists.
   The [1797167 review](receptor_study2_fourth_source_method_review.md) supports
   AlphaLisa method context and original micromolar table units, while material
   and individual-row provenance remain pending. The
   [2061300 review](receptor_study2_fifth_source_method_review.md) now supports
   FP-derived Ki in nM and parent Ki/30 min wording; material/tracer/row authority
   stays pending. The [1798835 review](receptor_study2_sixth_source_method_review.md)
   supports original BD1 TR-FRET Ki in µM while material/probe Kd/row authority
   remains pending. The [last three reviews](receptor_study2_remaining_sources_review.md)
   now complete the fixed nine-lead list. Resolve original material, controls and
   experimental/predicted provenance before activity admission; source 1805218
   has a 134-record table conflicting with its introductory prose. Draft curator
   questions are prepared, not sent. Any review of the 19 unresolved-domain
   census records is a separate declaration; prior outcomes remain intact.
   That [metadata continuation](receptor_study2_unresolved_domain_receiving.md)
   now verifies all 19 identities; domain-to-column authority stays unresolved.
3. **Qualify molecular/preparation correspondence through providers.** MolSysMT
   owns identity/scaffolds/states/formats/H/water/geometry. Receive its actual
   #323/#375/#447 contracts, with precise owning requests for uncovered needs.
   Explicit cached profiles are useful source controls, not automatic receptor
   preparation or pocket discovery. No local molecular fallback is allowed.
4. **Freeze the complete first study.** Declare source rights/exposure/labels,
   grouping/splits, receptor/preparation assumptions, required feature families,
   hypothesis choices/budgets, comparators, metrics/uncertainty and all original/
   evaluated/failure denominators before evaluation. Keep construction/tuning
   apart from the evaluation population.
5. **Execute, interpret and reproduce.** Retain original positive/negative/failed
   outcomes, unsupported families and incomplete searches. Compare against
   declared simple references and preparation sensitivity; a favorable score is
   not required. Publish only rights-qualified frozen inputs and original
   evidence through the existing validation collection.
6. **Repeat on the second admitted receptor.** Justify data quality and scientific
   contrast; don't choose a system because observed PHMT outcomes are favorable.
   Retain target-specific assumptions and test what actually generalizes.

## Consolidation and intermediate releases

Current source has native modeling/composition/curation, placed and finite rigid
screening, retrospective metrics, persistence and optional attribution. Consult
the maintained inventory for method-level coverage and limitations. Product work
continues on #6 support contracts, #41/#74 ownership debt, format fidelity and
clear public/install contracts alongside #103 science.

#95 owns proposed0.5 scope review. Actual plan/latest Release remains0.4.0.
Before freezing a new candidate, receive supported public dependencies, exact
source gates and same-file installed/public platform evidence under #9/#10/#23.
Source snapshots or narrow selected tests do not satisfy those gates. Publication
and the later suite notice require actual qualified delivery; migration publishes
no package or tag.

The two-study objective does not automatically become a0.5 requirement. Use as
many0.x releases as needed, including0.10/0.11 and later minors. The accepted
destination here is the mature pre-1.0 0.x described above; the separate 1.0
decision follows later review of agreed scope and evidence. The addon remains
deferred #58.

## Later directions: prospective, not implemented promises

| Direction | Condition before adoption |
| --- | --- |
| Measured Rust/GPU/distributed acceleration | Reference-equivalent scientific controls and representative bottleneck measurements; molecular kernels stay with MolSysMT |
| Dynamics/ensembles/MSM pharmacophores | Explicit state/occupancy/time/uncertainty contracts; molecular trajectory operations stay provider-owned |
| Peptide/covalent/water/quantum modeling | Concrete scientific use case and owning-provider readiness, not generic placeholder APIs |
| Graph/AI/generative methods and3D fingerprints | Declared data/leakage/baselines and genuine validation after classical foundations |

[Classical design catalogue](classical_workflow.md), [modeling strategies](modeling_strategies.md),
[dynamics](dynamics_and_msm.md), [specialized ideas](specialized_modeling.md) and
[AI planning](ai_and_data_science.md) retain design context. Their pseudocode,
future formats and old direct-backend sketches are not current operational APIs
or exceptions to component ownership.

## Public-library product work — 2026-11-06

The user requests both retrospective validation and new-library screening, with
powerful and friendly public-library management. The [primary-source provider
research](public_library_support_research.md) proposes discovery, activity-reference,
repurposing, natural-product and benchmark support through a common reproducible
workflow. Current ZINC acquisition is a stub and current batch screening
materializes inputs; no functioning multi-provider library service is claimed.
Prioritize bounded acquisition/import, manifest replay, provider-owned molecular
collection/preparation and incremental screening before advertising a connector.
Access agreements, 2D/3D states and actual end-to-end receiving remain explicit;
provider priorities are proposals, not a frozen API or release schedule.

[#108](pending_proposals/qualify_public_library_workflow.md) now owns this product
work. The [Discussions registry](https://github.com/uibcdf/pharmacophoremt/discussions/109)
retains resource assessments and dated revisit conditions under
[local registry guidance](public_library_registry.md); it does not replace
implementation issues or scientific admission.

The maintainer now requires the [comparative workflow survey](pharmacophore_library_workflow_survey.md)
before public-API design. It documents nine ecosystems and distinguishes source
collections, prepared variants, search assets, runs and grouped results. The next
design decision must compare incremental scans and reusable indexes, with a
friendly guided journey and deep public controls. Product power and performance
need scientific/resource evidence; quality takes precedence over delivery speed.

The [architecture proposal](public_library_architecture.md) now specifies that
lifecycle, identity/invalidation, guided/expert operation parity and explicit
commit/retry behavior. [Worked native controls](public_library_contract_examples.md)
separate existing evaluator semantics from proposed streaming/journal mechanisms.
The [unshipped incremental prototype](prepared_library_reference.md) now has a
separate [saved-query recovery experiment](prepared_library_recovery.md): ordered
manifest mapping, retained attempts, immutable confirmed outcomes and linked
repeat-query runs. Their original receipt records 48 selected scientific and 45
affected administrative passes; these historical counts do not qualify a later
head. Saved replay uses no molecular/citation provider. The later real-input case
below has its own execution identity. Provider collection/snapshot contracts,
public workflow integration and reusable-index decisions retain separate
acceptance; declarations alone do not authenticate prepared molecular content
or qualify production durability. Current actions are maintained in the resumed
increment above and [checkpoint](checkpoint.md).

The [fixed three-record PubChem3D case](pubchem3d_receiving_pilot.md) now supplies
the first bounded real-data receiving/import/snapshot/screening measurement.
It retains its initial public precision-keyword failure and corrected fixed-
float64 codec attempt. All original records are accounted for; no biological
labels or broad connector support follow. The missing reusable resource-owning
collection contract is handed to [MolSysMT #624](https://github.com/uibcdf/molsysmt/issues/624).
Broader source/format coverage and the guided/expert public workflow still need
qualification before index/performance claims.

The later quantity-report correction preserves that case's earlier evidence and
verifies explicit sealed coordinate records. [Read-only saved-run inspection](reference_run_inspection.md)
adds work/attempt coverage and bounded observed ranks, without current molecular
providers or new screening. Both remain scoped development evidence, not a
managed collection or a public workflow qualification.
