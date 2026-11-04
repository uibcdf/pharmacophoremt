# Native constraint semantics

Reviewed 2026-11-04 under [#79](https://github.com/uibcdf/pharmacophoremt/issues/79),
following audit items 8–9. This contract describes the existing native method;
it does not introduce a new matching algorithm or binding model.

## Meaning of a site and an assignment

For Point and Sphere sites, `features` lists **alternatives**. A site containing
`["positive charge", "negative charge"]` accepts either compatible kind within
its positional tolerance. It emits one assignment and contributes its weight
once. It does not require both kinds, accept an unlisted neutral kind or give
extra coverage for satisfying multiple alternatives. Feature order has no
priority meaning. Different sites retain their own constraints: every essential
site is required, including sites of weight zero.

The assignment unit is a **typed feature record**, not an atom, molecule or
spatial center. One record fills at most one site. Distinct recognized roles
may share atoms: an oxygen can supply a donor record and an acceptor record;
distinct indexed hydrogens yield distinct donor–H records sharing their donor.
The native method permits these records to satisfy separate sites. Their
co-occurrence is a geometric hypothesis, not proof that simultaneous receptor
contacts are physically realizable. There is no global atom-capacity rule.

Donor assignment `atom_indices` already includes the indexed hydrogen. A real
two-H probe retained `[1,0]` and `[1,2]`; suspected donor identity loss was
refuted. No candidate index or molecular identity scheme is added.

`criteria.site_feature_logic="any_of"` and
`criteria.assignment_unit="typed_feature_record"` now make these existing
choices explicit alongside `assignment="one_to_one"` and `essential="all"`.
These are additive explanatory fields. The method identifier remains
`essential_then_weighted_one_to_one@1`; numerical matching, defaults, decisions,
assignment selection and weighting are unchanged.

## Shapes, search and composition

| Native shape | Accepted interpretation |
| --- | --- |
| Point / Sphere | One typed record with any listed compatible kind; center within tolerance / radius |
| SphereAndVector | Exactly donor-H; position plus directed donor–H angle |
| Disk | Exactly aromatic ring; center distance within radius plus unoriented plane-axis angle |
| Excluded-volume Sphere | Standalone exclusion; any selected heavy-atom center strictly inside vetoes the pose |
| GaussianKernel / Cylinder | Representable by native persistence; not supported by this placed-pose evaluator |

Exclusion weights do not contribute to coverage. Exclusions cannot be mixed
with positive site alternatives. Disk matching does not implement disk thickness
or point-in-disk intersection. Feature presence and center coincidence do not
override angular constraints. The existing float64 cosine slack remains.

`get_correspondences()` and `align_to_pharmacophore()` use the same any-kind
compatibility and unique record indices. Triplet proposal additionally needs
three non-collinear essential centers. Atom overlap does not waive these
geometric conditions. MolSysMT owns every molecular fit and transformation.
The new real charge-triplet control exercises both signs and both feature-list
orders; it does not constitute exhaustive equivalence of every search method.

Model composition is a separate decision. `duplicate_policy="keep"` retains
independent constraints which may compete for one candidate. Existing
`same_participant` composition reuses compatible typed constraints with declared
source/frame identity and retains labelled observations without adding weight.
Neither policy invents evidence of independent energetic contributions.

## From evidence to a hypothesis

| Construction | Source evidence | Query decisions and retained explanation |
| --- | --- | --- |
| `from_ligand` / `from_feature_inventory` | Recognized source feature inventory | All emitted sites initially essential, weight one; caller chooses radius. Model retains inventory, definition, frame/state and recognition; each site retains membership/geometry indices |
| `from_interactions` | Evaluated native cross-boundary contacts | Same typed participant becomes one site with all observations, occurrence/relation indices, measures and detector criteria. All emitted sites initially essential, weight one; radius is independent of detector cutoffs |
| `from_receptor_projections` | Cached receptor inventory and caller declarations | Explicit complementary feature, projection direction/distance/label and target orientation where required. Sites initially essential, weight one; inventory, supplied/normalized specifications and radius survive |
| `edit_pharmacophore` | Existing native hypothesis | Explicit caller choices, reason, change list, site map and source-model snapshot; source score invalidated in the variant and retained in history |

Essential/unit-weight defaults are construction conventions, not measured
binding importance, probabilities, confidence or free-energy estimates.
Repeated contacts or repeated detectors do not increase weight automatically.
Projection labels/evidence remain caller declarations. Current weights and
essential flags are stored as site fields; constructor method/source identifies
their initial convention. No new policy metadata schema is introduced.

Use the existing curation tool when a recoverable decision history matters.
Direct attribute edits remain possible but do not automatically produce that
history. The caller is responsible for scientific reasons and common molecular
origin; source labels and equal axes cannot authenticate a source. Empty
observations, uncovered frames and calculation failure retain their distinct
existing outcomes. Cached evidence does not assert a new recognition run.

## Qualification and remaining work

[Executable controls](../tests/test_constraint_semantics.py) use analytical
coordinates and real public MolSysMT construction, recognition and movement.
They protect alternative kinds, single-record capacity, shared atom roles,
distinct donor–H identity, shape restrictions and correspondence/alignment
admission. JSON/YAML controls preserve both alternatives and representative
recognized/contact/projection origins plus deliberate essential/weight edits
under nm/radian and pm/degree policies. Existing pose, reference, ionic,
aromatic, composition, curation and search controls supply the wider regression
scope. See the [original evidence](evidence/native_constraint_semantics_20261104_summary.json)
for exact commands, producer/native identities, results and all attempts.

This is source-level analytical qualification, not biological predictive or
clean installed/public/all-platform validation. Audit items 8–9 remain partial:
consensus support/participant reuse and algorithm-specific evidence-to-constraint
choices still need their own review; external translators and legacy methods
retain their declared limits. Arbitrary user edits are not automatically audited.
Next review consensus/redundancy (audit 8/13) against its existing independent
oracles before designing parameter sensitivity/ablation controls (audit 12).
Original binding protocols under #66 remain a separate data-access gate.

No molecular routine, preparation/format engine, provider/prefix/dependency or
scientific definition changes. SDF ownership migration remains #74 / MolSysMT
#215. Addon and a new release are deferred; public release remains 0.4.0.

Temporary receiving capsule: `/tmp/phmt-semantics-20261104-gamhmcnp`, owned by
LMMV/dprada, review 2026-11-18. Original scientific outputs are archived; retain
this capsule for follow-up until reviewed. Borrowed scientific and public
ArgDigest prefixes remain unchanged. No background local test or build is
required after closeout.
