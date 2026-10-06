# ERalpha input audit and native validation gate

The owning issue is [#22](https://github.com/uibcdf/pharmacophoremt/issues/22).
The first slices audit the existing regression input and separately acquired
observed coordinates. Public MolSysMT template application now supports the
bounded observed-ligand controls below. The fixed-state hydrogen continuation
also delivers donor-inclusive geometric controls. Receptor preparation,
environment refinement and biological acceptance remain pending.

## Executed input evidence

`tests/data/eralpha_audit.json` qualifies the selection with SHA-256
`90e3159bc03424d976742c96c8cc2d2b32c9e1abf140d4652b70518b06a775f1`.
`devtools/audit_eralpha.py` and the cookbook notebook use public MolSysMT
conversion, extraction, selection, attribute access and chemical-state codecs.
The small aggregates describe this fixture; they do not implement a general
readiness detector. That provider capability is already proposed in
[MolSysMT #217](https://github.com/uibcdf/molsysmt/issues/217) and
[#218](https://github.com/uibcdf/molsysmt/issues/218).

| Observation | Measured result |
| --- | --- |
| Snapshot header | OpenMM 7.6, 2021-10-06 |
| Total atoms / frames | 54,437 / 1 |
| Protein atoms / bonds in provider graph | 4,058 / 4,096 |
| Unnamed ligand atoms / bonds | 44 / 47 |
| Ligand selection / source indices | `group_index == 8076` / 27528–27571 inclusive |
| Ligand elemental composition | C18 H24 O2 |
| Automatic small-molecule selection | Empty |
| Native declared connectivity | Partial; bond orders and formal charges absent |
| Public PDB-text/RDKit roundtrip | Same counts; complete flag but all bond orders zero |
| Native classical recognition, both routes | `MSM-ERR-STRUCT-003` |

Counts and connectivity describe MolSysMT's loaded graph, which may use the
provider's default connectivity reconstruction; they are not claims that the PDB
declared every bond. Neither conversion is accepted as chemically ready. Input
coordinates and chemical-state payload remain unchanged during the audit.
The guard intentionally fails when this measured gate changes, so the case must
be reviewed rather than silently inheriting a new preparation policy.

Provider source revisions for this evidence are MolSysMT
`4d490427e38c5836be82472348fdf61934442bda` and PyUnitWizard
`2ffe1885675f47c76af03c08e51bc889a5e99a05`, with Python 3.13.14 and the
existing scientific dependencies. This does not establish published-wheel
availability, a hosted matrix or a speed comparison.

## Origin and interpretation

The dataset description associates ERalpha with
[PDB 1QKU](https://www.rcsb.org/structure/1QKU), the wild-type human estrogen
receptor ligand-binding domain with estradiol. The local solvated OpenMM snapshot
does not record the deposition or its preparation history. Its derivation from
that entry, ligand mapping and stereochemical identity remain unverified.
[CCD EST](https://www.rcsb.org/ligand/EST) is a potential authoritative chemical
template; it has not been applied. Matching an elemental formula does not verify
chemical identity. The associated publication is
[Gangloff et al. (2001)](https://doi.org/10.1074/jbc.M009870200); it is background
context, not evidence that this fixture validates an interaction hypothesis.

The old `test_eralpha_pharmacophore_extraction` still protects historical feature
recovery using the legacy modeler. It establishes feature presence in that path,
not correctness of the native boundary, binding affinity or enrichment.

## Traceable source curation — 2026-10-03

A separate input is now retained in `tests/data/eralpha_rcsb/`, with a versioned
manifest, source URLs, byte counts and SHA-256. It contains the deposited 1QKU
mmCIF (revision 1.4, 2024-05-08), CCD EST and the unmodified ModelServer SDF for
the chosen instance. This establishes the new input's acquisition provenance;
it does not establish the old OpenMM snapshot's derivation.

Public MolSysMT conversion reads 6,596 atoms, 1,343 groups and one frame. The
selected ligand is label asymmetry ID D, author chain A, residue 600. The native
selection is `group_name == "EST" and chain_id == "D"`; its 20 heavy atoms occupy
source indices 5940–5959 inclusive. Their names agree with current CCD EST,
including O3/O17. The old snapshot instead uses O1/O2. A name match alone is not
accepted chemical mapping evidence. Native loading reconstructs a 23-bond graph
for this ligand but retains partial declared connectivity; recognition rejects it.

The CCD definition has 44 atoms/47 bonds, including 24 H absent from the observed
ligand coordinates. Template model/ideal H positions have not been substituted.
The new case therefore makes chemical assignment and hydrogen generation
separate explicit preparation steps. The proposed minimum contract is recorded
in the owning provider theme, `uibcdf/molsysmt#298`: read-only template assessment
and transactional application with an exhaustive explicit atom map, conflict
evidence, native chemical-state assignments and retained template provenance.
These are proposed tools; no public template implementation is claimed.

`devtools/audit_eralpha_sources.py` and
`test_eralpha_rcsb_source_identity_and_preparation_gate` guard acquisition identity,
label/author chain distinction, missing observed H, source/byte preservation and
the exact native preparation rejection. The cookbook notebook executes this new
audit alongside the historical snapshot audit. Controlled verification uses the
same MolSysMT/PyUnitWizard source revisions stated above.

The auxiliary ModelServer SDF has an unversioned CTAB counts line; the native SDF
probe at clean MolSysMT source `e9f135c2962aeefdb08135a7bc567d2d08bf27c5` rejects
it. CCD-only native structure conversion is also unsupported; its chemical
categories are inspected through the supported PDBx data-container form. Neither
raw file is silently edited or presented as a ready template. The first public
implementation must consume supported explicit chemistry and expose unsupported
format/coverage conditions.

## Next acceptance controls

1. Recover and document preparation provenance, or adopt an independently
   sourced replacement. Choose the intended ligand state and hydrogen model.
2. Use an explicit provider-supported template/preparation route. Review the
   atom map, conflicting/unassessed fields, orders, aromaticity, charges and
   coordinate preservation; do not modify completeness flags to bypass a gate.
3. Build a native reference-ligand query and review its families, essential sites,
   weights, units and evidence. Request aromatic/H-bond/hydrophobic families
   explicitly; acknowledge that chemical features alone are not binding roles.
4. Require unit self-fit for the reference placement; require essential-site
   rejection after a 2 nm displacement in the same frame. Rigid search may recover
   that pose, so displacement is a control for placed evaluation only. Add shared
   rigid-transform invariance and dedicated direction/normal controls.
5. Check native serialization and detached Ackredit references. Keep reference-data
   provenance separate from executed software/method attribution. A failed
   recognition attempt must not claim a completed pharmacophore calculation.
6. Evaluate provider-observed receptor interactions with named criteria and
   evaluated coverage, then curate the hypothesis. Resolve receptor chemistry
   coverage separately; do not infer a valid receptor from ligand readiness.

Initial geometric controls may use a declared 0.10 nm site radius and 20 degree
direction tolerance, with sensitivity checks at 0.15/0.20 nm. These are proposed
test parameters, not validated biological cutoffs. Expected native site counts
must be reviewed after the chemical state is justified, not copied from the
legacy inference output.

## Observed-pose template integration — 2026-10-03

`devtools/prepare_eralpha_ligand.py` consumes the public
`msm.physchem.assess_chemical_template()` and `apply_chemical_template()` tools
delivered in the provider's development checkout under #298. The frozen provider
artifact and original manifest live in `tests/data/eralpha_template/`; acquisition
metadata records source HEAD, curation-script and artifact hashes. Runtime
validation needs no sibling fixture or repeated chemistry curation.

The coordinate-free template has 20 heavy atoms, 23 bonds and 24 stored H counts.
Its source/CCD hashes match the separately acquired files above. Its explicitly
chosen CACTVS canonical descriptor supplies C8 R, C9 S, C13 S, C14 S and C17 S;
the manifest retains the CCD atom-level C8 S discrepancy. These are the provider's
curated declarations and independent controls, not new downstream stereochemical
inference. Current native artifact loading does not execute the historical RDKit
curation again. No molecular fields are assigned in PharmacophoreMT.

Assessment is compatible and transactional application is applied. All 20
source atom IDs, the 23-bond graph and the deposited pose are preserved; the
original complete-system coordinates and source chemistry remain unchanged.
The raw ligand retains its recognition failure. The prepared inventory contains
9 atomic hydrophobic participants, 2 acceptors and 1 aromatic ring. Directional
donor geometry is unavailable: stored H counts do not create explicit H atoms.

The declared test hypothesis selects acceptors/aromatic ring only, three
essential sites of radius 0.02 nm, a 10-degree unoriented normal tolerance and
minimum fit 1. Its original pose matches with fit 1; a 2 nm translated copy has
fit 0 and fails. Reversing the query normal still matches; an orthogonal normal
has fit 2/3 and fails the essential ring. These are fixed-frame geometric controls,
not evidence of affinity, free-screening discrimination or receptor interactions.

Public H5MSM and native query JSON roundtrips preserve coordinates, chemical
values, query metadata and the positive result. H5MSM normalizes only the two
component-text column dtypes from object to string in this fixture's state codec.
The control retains both actual state payloads and permits exactly those recorded
representation changes; every other value, null mask, index and dtype is compared.
The detached preparation report stays beside the saved molecule, as required by
the provider contract; molecular H5MSM does not embed that provenance.

`tests/test_eralpha_template.py` adds eight guards: positive/negative geometry,
normal orientation, persistence, explicit donor absence, malformed/conflicting
map failure without source mutation, checksum rejection, nondefault units and
real Ackredit session credit. The application records the observed entry, CCD
definition and curated template as distinct input datasets. Curation software
remains historical provenance; no G3PS branch runs or receives credit here.
The complete suite passes 327 tests in 333.34 s on Python 3.14.7, with the same
two known warnings. All three recipe blocks execute; strict isolated cookbook
rendering passes using the existing 3.13 documentation tools. Ruff and offline
index/reporting checks also pass. The
[consumer result](https://github.com/uibcdf/pharmacophoremt/issues/22#issuecomment-5970551189)
is linked to provider feedback under
[#298](https://github.com/uibcdf/molsysmt/issues/298#issuecomment-5970558997) and
[#300](https://github.com/uibcdf/molsysmt/issues/300#issuecomment-5970559168).

Reproduce with `python -m devtools.validate_eralpha_template --output FILE`.
The driver runs one workflow with host tracking disabled and one enabled,
retains full actual provider/results/citations, checks unchanged producer sources
and input bytes, and compares scientific payloads excluding attribution nodes.
The retained archive is documented in [evidence/README.md](evidence/README.md).
The [cookbook recipe](../docs/content/cookbook/observed_est_template.md) exposes the
public preparation/model/evaluation stages with explicit application sessions.

This advances only the separately sourced observed ligand. The historical
OpenMM fixture is neither repaired nor newly attributed. Complete donor-inclusive
acceptance remains dependent on [MolSysMT #300](https://github.com/uibcdf/molsysmt/issues/300),
and receptor preparation/environment refinement and biological acceptance remain
separate. Provider working-tree integration is not immutable public delivery.
No timing or memory measurement is claimed.

## Fixed-state H placement and donor-inclusive controls — 2026-10-03

MolSysMT #300 is resolved with its public experimental fixed-state extension of
`build.add_missing_hydrogens`. `devtools/prepare_eralpha_hydrogens.py` consumes that
tool after the independent template stage; no new molecular preparation algorithm
is implemented here. The call explicitly selects `mode='fixed_chemical_state'`,
`pH=None`, `engine='RDKit'`, reference chemistry, frame zero and report retention.
It expands the existing neutral CCD-derived state, without protonation selection.
The provider's actual [RDKit coordinate-generation route](https://www.rdkit.org/docs/source/rdkit.Chem.rdmolops.html#rdkit.Chem.rdmolops.AddHs)
is local H placement rather than environment or energy refinement.

The result has **44 atoms, 47 bonds and 24 added H**. The original 20 atom IDs,
indices, declared charges/stereo and observed heavy-atom coordinates are preserved;
the prepared heavy-only input remains unchanged. Original-to-output and parent-H
maps retain separate domains; generated H do not acquire deposited source indices.
The five declared/coordinate CIP centers agree with the selected descriptor,
including C8 R. Virtual H counts become zero. Public hydrogen inventory reports
no missing H, and public MolSysMT distances place generated C-H/O-H bonds within
the independent broad intervals used in the controls. The full feature inventory
has 9 hydrophobic participants, 2 donors, 2 acceptors and 1 aromatic ring.

The provider identifies indexed donor pairs `[3,22]` and `[18,40]` (O3 and O17
parents; newly generated H indices). The explicit intersection attribute policy
drops the expanded copy's B-factor domain, emits its catalog diagnostic and names
the drop in the detached report. The original source/retained mmCIF preserves its
annotations. The strict-policy guard rejects this input without source mutation;
no experimental annotation for new H is invented. A second H addition returns
an unchanged independent copy with zero added atoms.

The selected donor/acceptor/aromatic hypothesis uses **five essential sites**
of radius 0.02 nm, 10-degree direction/normal tolerance and minimum fit 1:

| Control | Status / weighted geometric fit |
| --- | --- |
| Self-placement | matched / 1 |
| 2 nm displacement | not_matched / 0 |
| Reversed aromatic normal | matched / 1 |
| Orthogonal aromatic query normal | not_matched / 0.8 |
| One reversed query donor direction | not_matched / 0.8 |
| Same query against heavy-only input | not_matched / 0.6; two required donors unavailable |
| H5MSM molecule / native JSON query reload | matched / 1 |

Heavy-only missing geometry and deliberately perturbed queries are controlled
scientific inputs, not activity labels. Persistence retains chemical values,
coordinates and query metadata, with the same bounded component-text dtype
normalizations described above. Template and H reports remain separately retained;
H5MSM does not embed preparation-history provenance. Nondefault pm/fs policy
preserves source geometry and the declared state.

Rigid-motion recovery uses one ranked triplet, a 0.02 nm spatial tolerance,
20-degree angular tolerance and all five required pairs. Both final and each_step
policies recover one placement with five pairs in three fits. The two frames are
different rigid placements of one conformation. The fixture motion helper now
preserves an existing box and does not invent an ID domain when the original
frame IDs are absent. Search uses nonperiodic geometry explicitly.

This revealed the independent eligibility defect in [#31](https://github.com/uibcdf/pharmacophoremt/issues/31):
centroid roundoff admitted a donor and acceptor at the exact same physical center
as non-collinear anchors at a displaced origin. Before correction, final recovered
five pairs and each_step rejected the ambiguous initial fit. Those observations
are not evidence ranking the policies. The shared predicate now anchors differences
to an existing represented center; six public proposal controls protect degenerate
rejection and valid proposals at three origins. No new physical near-collinearity
tolerance or local molecular fitting engine is introduced. Both alternatives stay.

`tests/test_eralpha_hydrogens.py` supplies **11 new guards**, while #31 adds six.
All 25 focused controls (including the eight earlier template controls) pass.
The complete suite passes **344 tests in 348.54 s** on Python 3.14.7: its six
warnings are the two existing warnings and four expected B-factor-drop diagnostics.
Five [new recipe blocks](../docs/content/cookbook/observed_est_hydrogens.md) execute
on 3.14, and strict isolated Sphinx rendering passes with existing 3.13 tooling.
Ruff and offline reporting/index checks pass. These are local consumer controls,
not immutable public delivery or full platform-matrix qualification.

`python -m devtools.validate_eralpha_hydrogens --output FILE` composes public
preparation, placement, donor negatives, persistence and both rigid policies.
One workflow per host-tracking profile yields identical scientific payloads.
Actual bounded application captures retain input datasets, the provider's executed
RDKit/CIP references and adapted G3PS stages that the rigid branch actually reaches.
The provider H report retains its own criterion/software roles and versions;
legacy session use entries from that builder currently omit contextual roles.
Both detached report and enclosing capture are retained without rewriting provider
provenance. Full source/input/extension identity and original JSON are archived in
[the evidence collection](evidence/README.md). No timing or memory is measured.

The molecular #300 gate is no longer blocking this observed ligand. Its generated
OH directions are not experimentally observed or receptor-optimized; fixed-state
environment refinement is a separate future provider operation. Receptor readiness,
interaction detection criteria/coverage, conformer/state choices and biological
validation remain open under #22. The independent old OpenMM fixture is not repaired
or newly attributed. Neither input is a validated enrichment benchmark.

The [consumer outcome](https://github.com/uibcdf/pharmacophoremt/issues/22#issuecomment-5973121783)
and [provider confirmation](https://github.com/uibcdf/molsysmt/issues/300#issuecomment-5973140309)
retain the handoff. The contextual-role limitation is reported in
[MolSysMT's existing Ackredit theme](https://github.com/uibcdf/molsysmt/issues/27#issuecomment-5973140086).

## Observed receptor coverage and detector gates — 2026-10-03

`devtools/audit_eralpha_receptor.py` consumes the public provider diagnostics
delivered under the now-resolved #217/#218 themes. The selected receptor is label
chain A (1,990 observed atoms in 250 groups); the EST ligand is label chain D,
source indices 5940–5959. Both map to author chain A in the original mmCIF.
The complete asymmetric unit retains three protein copies, three ligands and
water. The chosen scope excludes the other copies and water; no bioassembly or
symmetry mate is constructed. Source sequence completeness is not assessed.

The provider finds 247 assessed and three incomplete receptor groups: SER301
lacks OG, and each of LYS302/LYS303 lacks CG/CD/CE/NZ. Whole-residue nonperiodic
shells at 0.4/0.5/0.6 nm around the observed ligand contain 12/19/23 groups, all
without a reported heavy-atom gap. The incomplete groups are outside these
shells. The shell radii describe inspection scopes, not validated interaction
cutoffs. Exact standard-residue template matching does not certify chemical
validity or environmental protonation.

Even the 19-group central shell has no indexed H, missing formal charges and
atom aromatic flags, and partial declared connectivity. Standard amino-acid
reference order comparison remains unassessed because the provider's legacy
database lacks reference orders; protonation/hydrogen variants and valence remain
unassessed. No neutral charge, bond-order completion or terminal interpretation
is supplied by the consumer. Receptor chemistry remains a preparation gate.

Three actual public calls reject the current input with `MSM-ERR-STRUCT-003`:
isolated receptor feature recognition, full-source between-selection hydrophobic
detection and the ProLIF hydrogen-bond detector. Requested detection uses the
explicit SMARTS hydrophobic profile/0.45 nm cutoff and ProLIF 0.35 nm/130 degrees,
frame zero, nonperiodic geometry and no completeness assumption. The chemical
gate prevents their successful execution. Blocked observations are `None`,
not zero interactions or negative scores. The full source still holds the raw
observed ligand and other unprepared components; the independently prepared
ligand has not been inserted. Full-source recognition precedes selection, so
the receptor-only control also isolates the receptor's own failure.

Eight case guards protect chain/index domains, heavy gaps, nested shell coverage,
stored chemical limits, failure accounting, exact source preservation, real
Ackredit capture and explicit-unit scope under pm/fs/degree standards. The
application credits only the observed entry actually used; attempted unsuccessful
detectors do not generate successful method credits. The input-credit helper now
allows explicit dataset roles while preserving its three-input default for the
existing ligand route. No chemistry algorithm or preparation policy is duplicated.

Reproduce with `python -m devtools.audit_eralpha_receptor --output FILE`. Its two
host-tracking profiles preserve identical scientific reports, all original provider
coverage/diagnostics and source/input identities. Original evidence, actual loaded
extension identities and dependency versions live in
[the evidence collection](evidence/README.md); no runtime/memory is measured.
The [three-block cookbook](../docs/content/cookbook/observed_receptor_coverage.md)
shows the public stages. Preparation remains with MolSysMT #298: reusable residue/
terminal chemical assignment with explicit states, inter-group coverage, maps,
conflicts and honest unassessed fields. Resolved diagnostics are sufficient for
this audit and are not reopened. Successful receptor observations and biological
acceptance remain open under #22.

Verification: **352 tests pass in 376.12 s** on Python 3.14.7 in the editable
`molsyssuite@uibcdf_3.14` environment, with the same six warnings as the prior
slice. All 27 focused receptor/template/H controls pass; the final eight receptor
guards also pass after adding explicit requested-cutoff QuantityRecords. Three
new recipe blocks execute on 3.14 and strict isolated rendering passes with the
existing 3.13 tools. Ruff, index/reporting and whitespace checks pass. All eight
original evidence archives verify, including the seven earlier archives.

The [consumer result](https://github.com/uibcdf/pharmacophoremt/issues/22#issuecomment-5973351237)
and [provider preparation follow-up](https://github.com/uibcdf/molsysmt/issues/298#issuecomment-5973354053)
retain the evidence and reusable molecular contract. No new diagnostic issue or
local molecular workaround is introduced.

## Independent receptor exclusion geometry — 2026-10-03

The reusable public constructor under [#32](https://github.com/uibcdf/pharmacophoremt/issues/32)
now advances the geometric part while receptor chemistry remains pending.
`get_features(..., features=['included volume'])` obtains the raw source's
19-residue shell with 153 heavy-atom centers through MolSysMT. The standalone
`get_excluded_volume_sites(..., radius=...)` constructs sites from that cached
inventory without molecular access, inferred physical radii or ligand pruning.

The prepared EST and raw receptor keep their shared deposited heavy frame and
separate atom-index spaces. A 0.1 nm uniform exclusion admits the reference.
A controlled public MolSysMT translation puts candidate O3 index 3 on complete-
source receptor OE2 index 394 and yields one steric veto. All five positive
feature matches remain because the declared 0.4 nm query radius isolates this
effect. This is a different analytical query from the earlier 0.02 nm recovery
hypothesis. Widening exclusion radii to 0.35 nm vetoes the original reference
with 12 clashes; both choices remain explicit alternatives, without a physical
cutoff or biological preference claim.

Native query JSON retains geometry/metadata and the original reference/collision
outcomes. Source/state/identity fingerprints, original heavy coordinates and the
prepared ligand stay unchanged. No receptor chemical assignment or interaction
detector runs. H are generated local ligand geometry, without environmental
refinement. This is not receptor chemical acceptance, affinity or enrichment.

`tests/test_eralpha_exclusions.py` adds four controls to the 22 standalone
constructor controls. The [workflow contract](excluded_volume_workflow.md),
[cookbook](../docs/content/cookbook/excluded_volumes.md) and ninth retained
[evidence archive](evidence/README.md) describe the composed stages, actual
citation capture, original input identities and tracking-independent science.
No timing/memory measurement is taken. Molecular preparation remains under
MolSysMT #298; this independent geometric step does not bypass its chemistry gate.

The [observed-case result](https://github.com/uibcdf/pharmacophoremt/issues/22#issuecomment-5973670489)
links the [independent tool delivery](https://github.com/uibcdf/pharmacophoremt/issues/32#issuecomment-5973661182)
and its scientific/attribution/persistence controls.

## Owner publication and repeat-H history — 2026-10-06

The #39 provider handoff is adopted in the owner regression. Repeated fixed-state
H placement must preserve the complete original source payload/history and
coordinates, return an independent copy with identical chemical assignments, and
append exactly the unchanged terminal-attachment and hydrogen-addition reports.
History is tested separately from assignments; none of the original preservation
or zero-added-H assertions are removed. The strengthened guard and six CI
route/backlog controls pass seven tests in 7.26 s on Python 3.14.7.

The initial publication selection passes all 27 ERalpha pilot controls but reports
ten curation setup errors from the separate retired Interactions.between call.
The shared native adapter now consumes public between_selections, following
MolSysMT #346, with the same selected atoms/frame and original scientific
evaluation metadata. Its affected ionic/aromatic/composition/CCD/curation consumers
pass 164 tests in 231.78 s. Controlled CI source pins identify the tested current
provider revisions while preserving all required Python minors and full collection.
Historical evidence is unchanged; today's selected tests do not replace a full
matrix or biological acceptance. The publication receipt and original logs are
retained in `devguide/evidence/publication_20261006.json`.
