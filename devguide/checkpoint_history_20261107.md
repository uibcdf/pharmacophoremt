# Checkpoint before the mature-0.x goal resumed

Recorded 2026-11-07 UTC. The following text preserves the pre-resumption
checkpoint at source `80dbd94389d4f3602c95b03ea16bdb3d94d7af87` verbatim.
Its pause and next-step statements are historical. Use [current checkpoint](checkpoint.md).

---

# Current development checkpoint

Maintained 2026-11-07 UTC after read-only saved-run inspection, owners LMMV/dprada.
Start with [onboarding](onboarding.md), [decisions/workstreams](decisions_and_workstreams.md)
and [migration](machine_migration.md). The former long log is preserved verbatim
after its preface in [checkpoint history](checkpoint_history_20261106.md).
This page is current; old dated "Next" paragraphs are historical observations.

## Pause checkpoint — 2026-11-07 UTC

Paused at Liliana's request after read-only exploration of feature reuse. Latest
implemented/checked source is `c816c8d958f00a976206ea942812f72d2bafc7c8`
([saved-run inspection](reference_run_inspection.md), 86 focused local tests).
No feature-reuse experiment, new molecular acquisition or new screening ran.

On resume, declare a small in-memory comparison of fresh versus reused
`get_features` inventories across two queries with the same requested families,
using existing public correspondence/alignment/placement operations. Preserve
post-fit re-extraction and compare complete native evidence for that subworkflow.
`RigidPoseSearch.evaluate` currently extracts its own inventory; do not claim
equivalence with its full search or add an API/cache/index before the experiment.
Same-source/selection/frame/state/chemistry/geometry is a caller precondition,
not authenticated by axis checks. Record requested families separately: absent
feature records do not prove a family was requested. Keep native units and
explicit state conventions. No performance benefit is established by fewer calls.

## Where we are

The library has native prepared/cached ligand-, interaction-, complex- and
receptor-based workflows, finite rigid search, pose/conformer screening, metrics
and native persistence. [Capability inventory](capability_inventory.md) names
actual routes/controls and limits. These analytical/preparation deliveries do
not establish predictive accuracy. Neither complete receptor-based biological
study under #103 has executed.

Actual release plan/latest GitHub Release remains **0.4.0**. Proposed0.5.0 is
reviewed, not frozen/published. The latest work records destination controls and
an offline assay-capacity tool and unshipped incremental/recovery controls;
public runtime/dependency/workflow contracts are unchanged.
The addon remains deferred; its source exists but live-browser acceptance is #58.

| Workstream | Current evidence | Next action |
| --- | --- | --- |
| #103 two receptor studies | Preparation/analytical controls exist; no full admitted biological study | Complete source/cohort/preparation admission, freeze the full comparison/evaluation plan, then execute |
| #66 ERalpha | Original Sun2006/Xin2023/Gungor2006/Scott2023 methods remain unresolved; original pools/thresholds/exposure retained | New authorized access lead; don't repeat exhausted routes or silently substitute a source |
| #106 BRD4 admission | All nine fixed leads have bounded method reviews; prior capacity/coupled outcomes and seven held sources remain distinct | Resolve source-specific material/data authority, especially experimental/predicted provenance in 1805218; no automatic activity admission |
| #108 public-library workflow | [Fixed PubChem3D pilot](pubchem3d_receiving_pilot.md), quantity correction and [read-only run inspection](reference_run_inspection.md): work coverage, stable bounded observed ranking and historical native evidence preserved | Receive provider collection/snapshot contract [MolSysMT #624](https://github.com/uibcdf/molsysmt/issues/624); qualify broader real inputs, reusable search assets and guided/expert API before managed-library/index promises |
| #128 tool-study registry | [Public index](https://github.com/uibcdf/pharmacophoremt/discussions/129) and ten documentary tool records, with forms/guidance in source | Follow [registry guidance](pharmacophore_tools_registry.md); distinguish documentary/executed/benchmark evidence and track actual template delivery/rendering in #128 |
| MolSysMT | #105 native aromatic-N received; #323/#375/#447 remain open at this handoff | Consume supported H-refinement/carboxylate/grouping contracts; report actual missing general tools there |
| #95/#10/#23 | Proposed intermediate release and separate public/installed/support gates remain partial | Qualify actual public provider capabilities and exact candidate/source/file/platform gates before freeze |
| #9 | Narrow local controls do not clear the full source backlog | Inspect exact hosted run/attempt IDs; retain failures/skips/pending evidence |
| #6/#41/#74 | Broader support adoption and bounded molecular/annotated-SDF migration debt remain | Use owning provider contracts; don't expand historical local compatibility code |

## Latest BRD4 capacity outcome

[BRD4 capacity receiving](receptor_study2_capacity_receiving.md) stops the earlier
11 pending sources for this design: each has at most9 SIDs. AID1805333 is the
largest explicit isolated-BD1 method lead, with499 raw SIDs/494 CIDs; those counts
are not independent molecules or class balance.

The [original-method review](receptor_study2_primary_method.md) and
[receipt](evidence/brd4_primary_method_20261106_summary.json) now retain the actual
patent binding method, separate BRD4/cellular Table24 columns, source interval
legend and unchanged PubChem version3/revision2 descriptors. Incorporated human
construct information is documented, while exact transfer to the patent remains
an inference. No molecular sequence mapping, receptor preparation or score ran.

The [published activity-capacity plan](evidence/brd4_activity_capacity_plan_20261106.json)
has now executed on the destination. [Receiving and outcome](receptor_study2_label_capacity_receiving.md)
retain all five successful requests, unchanged before/after metadata and the
complete505-row/499-SID/494-CID accounting. There are382 strong occurrences,
32 weak occurrences and91 missing relations; blank relations are not inferred
as equality. Six duplicate strong SIDs and one missing CID leave375 strong and
32 weak eligible SID upper bounds. **The weak class is below50: stop this source
for the declared design.** No thresholds, sources or unresolved records are changed
to repair capacity.

A new source needs a new dated nomination and its own original-method/label/
rights/exposure admission; do not transfer this patent's method or pool AIDs.
The received CSV includes source SMILES strings, which were neither interpreted
nor displayed. Individual rows and source prose remain private; source-curation/
license version is unresolved for redistribution. No cohort/receptor/model/score
or complete biological study follows. Earlier ERalpha/exposure ledgers remain
intact, and no unseen-holdout claim is made.

## Follow-on original-source review

The [next-source comparison](receptor_study2_source_lineage_review.md) receives
AID 1795677 / US10023592B2 under a new dated nomination. Direct application
ancestry, the exact binding-method text and 514 matching document ordinals/four
literal result columns establish shared publication evidence with US10941160B2.
Different PubChem SID/CID totals remain a curation question; the earlier 32-weak
result is not transferred. No activities are requested for this coupled report.

The [third-source review](receptor_study2_third_source_method_review.md) receives
AID 1797292 / US10206931B2, version 2/revision 2, with 300 SIDs/300 CIDs. Its
BRD4 AlphaLisa method is distinct from the CBP and MYC endpoints. The reviewed
original HTML does not establish its table's reporting unit or experimental
species/accession. The comparison patent has separate TR-FRET and AlphaLisa
contexts; its explicit micromolar statement cannot repair the nominee's missing
unit authority. The first PDF attempt and its incomplete prefix custody remain
in the [original receipt](evidence/brd4_source_lineage_20261106_summary.json).

The [separate recovery](receptor_study2_pdf_recovery.md) now receives the complete
12,617,561-byte PDF with verified length/media/header/hash and inspects pages
176, 177, 183 and 213. The direct PCT original and its first/last table images
are also received and reviewed. No reporting unit is established in those bounded
locations; the material's human label remains a curated annotation rather than
authentication of the cloned species/accession. The source stays unadmitted.
The recovery corrects byte custody without replacing earlier failures or changing
labels/resource-memory budgets. Temporary renderers are removed, and the new
[receipt](evidence/brd4_pdf_recovery_20261106_summary.json) preserves all stages.
The [draft curator questions](receptor_study2_pdf_recovery.md)
seek original unit/conversion and experimental-material authority; no external
message was sent. No third-source activities, class projection, cohort or score
ran. Resolve the original unit/material and source-to-assay mapping before an
activity declaration.

The [fourth-source review](receptor_study2_fourth_source_method_review.md) now
receives AID1797167's description/summary once and reuses the already received
US9763922B2 HTML by hash. The fresh description exactly matches FormulaII
Example311 AlphaLisa, whose own table explicitly reports micromolar results.
FormulaI Example387 TR-FRET remains a separate context. Actual experimental
species/accession and individual-row/table provenance remain pending after the
bounded search; curator human annotation does not authenticate the cloned material.
No activities, class projection, cohort or score follows. That review identifies
AID2061300/US12286435B2 as the next fixed-order lead, addressed separately below. The
[fourth-source receipt](evidence/brd4_fourth_source_method_20261106_summary.json)
retains the two HTTP200 responses, documentary replay and finite review scope.

The [fifth-source review](receptor_study2_fifth_source_method_review.md) now
receives AID 2061300's metadata/US original and, under a new single-request plan,
its incorporated PCT original. The method calculates inhibitor Ki from FP
displacement IC50; Kd belongs to the protein–tracer pair. Table 1 explicitly
reports Ki in nM, separating BD1/BD2. Title/description identities match the census:
our old "KD title" characterization is corrected while original KO wording and
the old archive remain intact. The parent explicitly states Ki and 30 minutes,
with the same equation after whitespace normalization; US HTML `30 mM` is preserved.
Actual material, tracer identity/numerical Kd and individual-row provenance
remain unqualified. No activities, class projection, cohort or score follows. The
[receipt](evidence/brd4_fifth_source_method_20261106_summary.json) preserves the
four successful body requests and the separate failed curator-page observation.
That review identifies AID 1798835/US9957263B2 as the next lead, addressed below.
Earlier held sources stay separate.

The [sixth-source review](receptor_study2_sixth_source_method_review.md) receives
AID 1798835 version 3/revision 2 and the original US9957263B2 method. Canonical
metadata identities match the census; after HTML-entity/whitespace normalization,
the description exactly matches the original assay paragraph. Table 1 separates
BD1 K57–E168 Ki in µM from BD2 Ki and cellular EC50. The complete header spans
table blocks; the method/table BD2 boundary conflict remains explicit. Actual
experimental material, numerical probe Kd/conversion specification and row
authority remain pending. Other-entry human annotations are not accepted as
source-specific evidence. No activities, classes, cohort or score follows. The
[receipt](evidence/brd4_sixth_source_method_20261106_summary.json) retains the three
HTTP 200 responses, exact documentary checks and failed curator-page observation.
That review identifies AID 1805218/US10899769B2 as the next lead, addressed with
the final three fixed-order nominations below.

The [remaining-source review](receptor_study2_remaining_sources_review.md) now
records bounded original-method receiving for 1805218, 1805772 and 1804941:
nine HTTP 200 requests, unchanged source/census field identities, no activities.
Source 1805218's prose describes Examples 1–3 and other predicted compounds,
while Table 2 reports 134 distinct numeric-result labels. This is unresolved
experimental/predicted provenance, not a three-record capacity ceiling or proof
all 124 PubChem SIDs are invalid. Source 1805772 supplies its incorporated CBP
procedure, but actual vendor-material linkage and NaCl/control wording remain
pending. Source 1804941 supports original IC50 intervals in µM; its exact material
transfer and row authority remain pending. Original intervals are not PHMT labels.
The [combined receipt](evidence/brd4_remaining_sources_20261106_summary.json)
preserves separate runs, row-layout replay failure/correction and exposures.
All nine declared leads have now received bounded review; none is newly admitted.
Draft source-specific questions are prepared, not sent. The census's 19 unresolved
domain sources remain unresolved and require a new declaration for further review.

A [separate 19-source metadata review](receptor_study2_unresolved_domain_receiving.md)
now receives exact complete coverage in one request, with unchanged original
source identities and 76 canonical field identities. All 19 remain unresolved:
metadata do not establish AID–domain–original-column correspondence. Actual
Protocol keys are missing, while Description contains methods; canonical null
identity does not establish explicit null presence. The nine earlier outcomes
are unchanged. No new activities, cohort, quimioteca or scores were admitted.

The user explicitly wants both retrospective validation and new public-library
screening. These are separate scientific deliveries. The historical ESR1ago
pilot already executed ligand-reference screening; current receptor-source
admission does not erase that result or constitute new screening. The
[library support research](public_library_support_research.md) proposes ZINC,
PubChem and complementary discovery/reference/drug/natural-product catalogs,
with access terms, 2D/3D and implementation readiness distinguished. No new
connector or library acquisition is claimed by that research.

## Evidence and execution that must not be overstated

#105's original250 unique selected controls and #102's corrected111-control
selection retain their exact producers. The earlier complete hosted old-head
source run had2,071 passes/two failures; the two envelope-oracle failures were
subsequently repaired, but selected repair controls are not a full current suite.
The later local full attempt stopped at its1GiB cap after1,428 passing reports.
Do not launch a larger whole-suite retry on this shared machine.

The public MolSysMT0.23.0 receiving record has203 selected passes and18 capability
skips, not modern-provider or full installed/public qualification. Controlled
source MolSysMT0faf1584 is distinct from the preserved sibling checkout71fbe4f.
The historical controlled prefix/SDK/native binary are now absent; reconstruct
their declared sources/environment and record fresh native/import receiving.

For source head7395ad004dc08c0442572a12f3e952d59c5fdec4, the latest migration
observation records CI42197647509 still queued; policy42197647866 and publication
governance42197647985 succeeded. This is not a complete source-matrix pass.
The final documentation head's exact observation belongs in #9/#107; consult
those run/attempt records rather than restarting old work because a poll expires.

## Receiving the new machine

All59 declared support files are tracked/hash-correct. Tracked evidence archives
are portable; ignored raw papers/controllers/environments are not supplied by a
clone. [Migration inventory/checklist](machine_migration.md) marks available BRD4
capsules, absent old #66/controlled-source roots and reconstruction authority.
Do not overwrite old receipt paths/hashes or copy credentials/native binaries.

Use Python3.14, the exact SDK/selected dependency context, `pip check`, import/
native identities and scoped checks from onboarding. Heavy work remains serial,
one actual allowed CPU/backend thread, low priority and512MiB/no swap where
enforceable. Old method-review phases had a one-CPU quota but CPUs0–19 affinity;
preserve that fact. Use explicit taskset and verify affinity on subsequent Linux
checks; CPU19 is historical, not a destination requirement.

Fresh shared-environment receiving now verifies Python3.14.10, the editable PHMT
origin and the local MolSysMT Rust-extension identity. All23 selected metric,
unit/persistence, native geometry/provenance and failure-accounting controls pass
under one CPU,512MiB/no swap (peak306,360,320bytes; no OOM/limit events).
The [new receipt](evidence/brd4_label_capacity_20261106_summary.json) retains this
context separately from old controlled-source and public artifacts. Whole-environment
`pip check` still fails because the installed TopoMT requires absent Numba;
[TopoMT#93](https://github.com/uibcdf/topomt/issues/93) owns that known boundary.
Optional Ackredit and Beartype are absent; selected checks do not require them.
The historical fixed-source CI context and full/public qualification remain
unexecuted here. No local scientific task remains running.


## Superseded checkpoint section before progress-reuse closeout, 2026-11-08

This is a historical snapshot, superseded by the current checkpoint. Pending
installed receiving in this snapshot is subsequently completed under#145.

## Last received increment and next action

The latest increment corrects two analytical boundary fixtures under
[#143](archive/analytical_upper_bound_platform.md). The
[receipt](evidence/rdkit_boundary_correction_20261107_summary.json) passes59selected
cases, including14analytical guards and the separate ten-case/186-assignment
driver. Exact rational controls fail on the old data; production runtime and
eight interior cases are unchanged. Corrected hosted acceptance is received at
frozen8db2a53; its terminal evidence appears below.

The received runtime correction fixes [native Point center inspection](native_geometry_inspection.md)
under[#142](archive/point_center_inspection.md): a read-only alias exposes the
canonical position, ordinary point/mixed center-distance queries now work, and
empty/filtered center arrays keep shape(0,3). The
[source receipt](evidence/point_inspection_source_20261107_summary.json) passes338
selected cases, including16new regressions with the original13failing/3positive
controls preserved. Native point fields, radius absence and existing distance
implementation remain unchanged. [Exact owned installed receiving](evidence/point_inspection_installed_20261107_summary.json)
passes the same338bodies/two original isolated children and the unchanged RDKit
recipe from wheel0.4.0+151.g858fe5a;210payload/155runtime files authenticate.
#142 resolves this bounded defect; full supported gates remain separate.

The [accumulated checkpoint](projection_ci_checkpoint.md) has completed at exact
489be1213a92e33be84204d2e0fd2f5f9b9c10e1/attempt1. Its
[terminal receipt](evidence/projection_ci_terminal_20261107.json) preserves source
CI42416657424: all four Linux cells pass2339cases each; all four macOS cells
pass2338/fail1 at the original analytical upper-bound fixture. The source gate
is not accepted. Policy42416661473/publication governance42416665708 pass.
Independently, all four Linux XML outputs retain105distinct qualified file paths
and correct namespaces; native Linux3.13 uploads pass, resolving#141. No later
Point or boundary revision is covered by this frozen run.

The received RDKit increment implements the [public RDKit projection contract](rdkit_projection.md):
legacy point targets and fixed-radius reading remain available; explicit spheres,
radius=None reading, detached field/loss reports and warn/strict/ignore choices
are now public. Full preflight rejects unsupported alternatives, invalid/overflowed
geometry and invented radius inference before target construction. Its
[source receipt](evidence/rdkit_projection_source_20261107_summary.json) passes271
selected local cases, the existing ten-case analytical driver and the exact
[public recipe](../docs/content/user/rdkit_interoperability.md). [Same-artifact
outside-checkout receiving](evidence/rdkit_projection_installed_20261107_summary.json)
passes the same214 original bodies, one guarded diagnostic child and the exact
public recipe from owned wheel0.4.0+148.g1040dbb. All210 payload files and155
nongenerated runtime files authenticate;140 imported main modules/three namespaces
resolve to that target. [#140](archive/qualify_rdkit_projection.md) closes only
this field contract. No new provider/prefix/native modification, public release, general
library connector or scientific-equivalence claim follows.

Earlier evidence remains under its original producer and scope:

- [Frozen4616c78 terminal receiving](evidence/accumulated_ci_terminal_20261107.json):
  all eight source cells pass2259tests each, with reporting/policy/publication
  steps. Its original namespace-collision XML is retained; the
  [#141 correction](coverage_xml_identity.md) passes111 selected local cases and
  is independently received from all four newer Linux cells.
- [Pharm3D comparison](rdkit_bounds_comparison.md): ten analytical cases/186full
  assignments,106 selected source cases and complete driver. Interior filters,
  proper-fit reflection rejection and strict/inclusive boundary differences keep
  their declared limits. Original512MiB failures and the1GiB amendment remain.
- [Saved progress](saved_run_progress.md):102source cases and the same57bodies,
  51guarded children and16documented commands from producer1950421's owned144wheel.
  API/CLI/export/reader and [guided/expert receiving](guided_expert_journey_receiving.md)
  retain their own artifacts, original databases and scope. None becomes current
  full-platform/public evidence by being linked here.

The [accumulated preparation](accumulated_ci_checkpoint.md) and
[checkpoint history](checkpoint_history_20261107.md) retain earlier observations,
including scheduled42383495995/654586f's original governance failure and its
separate recovery. [Current guide audit](evidence/projection_ci_guide_audit_20261107.json)
compares all seven real canonical texts at exact owner revisions; all match.
The frozen policy-v1.5.4 caller remains separate and unchanged.

The [recovery checkpoint](boundary_ci_checkpoint.md) is complete at exact
8db2a53f91a3686088874f965d389e636003d990/attempt1. Its
[terminal receipt](evidence/boundary_ci_terminal_20261107.json) receives source
CI42421360591 with2357tests passing in each of eight Linux/macOS Python3.11–3.14
cells, plus successful reporting/policy42421364958/publication42421369303 native
steps. All eight XMLs retain105qualified files; native Linux3.13 uploads pass.
The [canonical RDKit record correction](evidence/rdkit_record_correction_20261107.json)
is independently read back and preserves the original analytical update.
#143 resolves the boundary fixture. Preserve failed489be12, successful8db2a53 and
later profiling/recovery producer identities separately. [Guide revalidation](evidence/boundary_ci_guide_audit_20261107.json)
retains its dated owner-head/local-byte observations, separately from frozen policy.

The [#144 saved-reader baseline](archive/profile_saved_run_scaling.md)
now receives three synthetic reader cells,75repeated samples and three first-open
observations. Its [receipt](evidence/saved_run_scaling_20261107_summary.json) keeps
all exact accounting/export/byte controls and the original10000preparation timeout.
A separate verified-copy public recovery preserves6784confirmations and fills216;
only that recovered reader phase then completes. No library runtime/provider/native change,
cache/index or molecular-throughput claim follows. The [reusable recovery driver](evidence/saved_run_recovery_20261107_summary.json)
now passes22case guards and the exact copied10000case;#144 resolves its bounded
engineering scope. Extra receiving samples retain a separate identity.

[#145 immutable-snapshot progress reuse](saved_progress_reuse.md) is declared and
implemented for factory-opened read-only views. All10new guards pass after the
original five repeated-read failures; all130selected reader/store/profile cases
pass; its [source receipt](evidence/saved_progress_reuse_source_20261108_summary.json)
receives175distinct cases including governance/distribution. Full admission,
detached counters, thread/lifetime refusal and fresh writer
operations remain guarded. Nine declared same-input pairs pass exact outputs,
complete ranks/exports and original-byte checks. Repeated10000-record progress
medians are497.892380ms baseline and0.103223ms reuse; full open/first-scan costs
remain. Exact owned-wheel receiving is pending.

**Next concrete action:** receive the unchanged original reader/export/progress
controls and10new guards from one exact owned installed artifact. The measured
benefit applies only to repeated same-snapshot synthetic progress. Later runtime,
profiling/recovery helpers and tests retain current-head source debt under#9;
frozen8db2a53 is not relabeled.
MolSysMT#624 collections, full installed/public dependency/platform delivery,
biology, comparison/performance and mature0.x acceptance retain separate gates.
