# Development Checkpoint

**Current status (2026-10-03):** Gen 1b classical consolidation. The immediate
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
