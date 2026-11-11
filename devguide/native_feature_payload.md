# Native feature payload: first standalone producer

Owners LMMV/dprada; PHMT#195; selected 2026-11-11 UTC, toward 0.6.0.
This contract precedes the new-format implementation. Source/installed receiving
is recorded separately; no tag, public package or platform qualification follows.

## Ownership and selected boundary

`modeler.get_features` owns native feature extraction. Its inventory preserves
selected local atom indices, one frame/state, recognition and optional attribution,
but does not record the effective requested families. Feature presence cannot
establish evaluated-empty coverage. Require that declaration from the caller;
never infer it from recognition metadata or fabricate a completed extraction.

Native pharmacophore JSON/YAML (`pharmacophoremt.native@1`) stores modeled sites,
shapes and tolerances. It is not an extraction inventory and cannot preserve the
same participant/geometry maps through a model projection. The historical
snapshot decoder remains explicitly `snapshot-study-v1`; historical bytes are
never rewritten or silently reclassified. The new consumer-owned codec uses
public PyUnitWizard records and existing native geometry validation, with no
test-support import or competing general quantity codec.

The first public operation is a standalone, bounded `FeatureInventoryPayload`
in `pharmacophoremt_features`. It serializes **already captured complete native
inventories**. Molecular access, selection resolution, preparation, current source
authentication and collection mapping remain MolSysMT-owned (#624). Existing
archive staging/publication/recovery remains #194-owned. New-format admission
into archives and arbitrary/subset generation assembly need a subsequent explicit
lineage contract; this first producer does not change the old archive format.

## Public operations and lifetime

| Operation | Contract |
| --- | --- |
| `FeatureInventoryPayload.from_inventory(inventory, evaluated_families, *, parent, extraction_producer, payload_profile)` | Require explicit `native-classical-v1`, the complete captured inventory, evaluated-family declaration and original producer metadata (explicit None means unknown). Check layout/maps/budgets, encode quantities and reconstruct through the same validator before returning. No extraction, feature filtering or new extraction credit. |
| `FeatureInventoryPayload.from_bytes(raw, *, payload_profile)` | Require the explicit new profile; check canonical finite JSON, envelope digest, structural layout/maps/coverage and bounds. Preserve original bytes. Quantity records remain opaque; this is not scientific admission. |
| `payload.to_bytes()` | Return original immutable bytes for caller-owned storage/transport; no file creation or overwrite. |
| `payload.describe()` | Return detached metadata, original extraction producer, separate serialization observations, raw SHA/size, coverage and explicit cold validation scope. No scientific imports or changed policy. |
| `payload.to_inventory(*, required_families)` | Refuse unobserved families, then reconstruct and validate every feature afresh, including families beyond the requested coverage check. Return a fresh complete native inventory; no partial return or cached validation passport. |

The payload owns bytes and no open handles. Returned dictionaries/quantities are
independent of input and of other reads; callers own any files and original
inventories. Metadata stays cold before and after scientific use. The class is
exported lazily; importing it or parsing/inspecting bytes does not activate the
main scientific package, unit backends, molecular tools or attribution provider.
This standalone object assigns no archive work key or global ordinal. A caller
borrowing an archive occurrence retains that archive's original record binding;
assembly must name the old binding and any new position explicitly in its later
contract. Encoding an inventory alone does not preserve an enclosing archive.

## New versioned wire contract

Canonical UTF-8 finite JSON uses envelope keys `schema`, `payload`,
`payload_sha256`. Schema is `pharmacophoremt.native-feature-payload@1`; the digest
covers canonical payload bytes. The required payload keys are `profile`, `parent`,
`evaluated_families`, `coverage`, `inventory`, `extraction_producer`, `serialization`.
The inner profile is `classical-single-frame@1`. This is a new development format;
PyUnitWizard's consumed record API remains provisional. Unknown formats/profiles
refuse; there is no automatic historical/native-model migration or autodetection.

`parent` has exactly `source_key`, `occurrence_key`, `artifact_sha256`,
`artifact_bytes`, `n_atoms`, `preparation`, `mapping_policy`. Keys are literal
nonempty UTF-8 text (512 bytes); no unit parsing, Unicode normalization or path
access. Artifact SHA/positive byte count are both supplied or both None. Unknown
remains unknown. Preparation is bounded text or None. Mapping policy is exactly
`caller-declared-local-atom-axis@1`; this records a declaration, not authentication.
The local source atom axis is 1–256 atoms. A nonempty unique selected axis may be
a subset, with original order/indices retained; no renumbering occurs. Feature
participant and geometry maps are nonempty, unique and inside that selected axis.
Source identity and map truth cannot be established without a molecular owner.

The inventory retains exactly the existing native fields (definition, features,
recognition, selected_atom_indices, structure_index, chemical_state) and optional
attribution. Preserve a nonnegative integer frame and explicit native state
(nonnegative integer, `reference`, `structure` or None); booleans are refused.
One Cartesian frame with no imaging and definition `classical_atomic_formal@1`
is admitted. All six classical families are supported; included-volume or other
definitions need a separate profile and are refused rather than dropped.

Every feature retains kind, participant/geometry maps, center, direction, normal
and charge. Centers are explicit length vectors of shape (3,). Donor directions
and ring normals are explicit dimensionless, finite nonzero vectors of shape
(3,); preserve their captured magnitudes rather than replacing them by normalized
copies. Direction exists only for donors; normal only for rings. Elementary
charge is a finite nonzero scalar with the declared sign and exists only for
charge families. Existing native validation owns centers/orientation; this
payload also checks geometry maps and charges. Neither map/shape validation nor
internally consistent quantities establishes correct molecular origin.

Each non-None scientific field is a sealed public `QuantityRecord` bound to
`features[i].field`. Write the quantity's own explicit unit; read with that exact
field and explicit nm/length, dimensionless or e handshake. No bare-value units
come from session defaults. Cross-field substitution, wrong units, malformed
seals, invalid shapes and nonfinite/zero/sign-invalid values refuse. Recognition,
optional original attribution and extraction producer are bounded detached finite
JSON provenance, not recursively decoded scientific quantities or authentication.

Evaluated families are explicitly declared, unique and stored in canonical six-
family order. Counts are recounted from **all** retained features. Each declared
family is `completed` with a positive count or `evaluated_empty` with zero. Every
feature belongs to a declared family. A missing family is unobserved; a partial,
failed, unsupported or unattempted extraction cannot be encoded as complete.
Those occurrence states belong to future archive assembly, with their causes.
The producer cannot independently prove the truth of a caller's declaration.

Original `extraction_producer` is opaque JSON mapping or explicit None; preserve
unknowns and original versions without inventing a new producer. Optional native
attribution is retained unchanged. `serialization` separately observes the
PharmacophoreMT distribution version, codec-file SHA and selected operation.
Unavailable observations are None; they do not authenticate running code, replace
extraction versions or claim a scientific method was executed again.

## Bounds, diagnostics and support contracts

Per payload: 64 features, 256 atoms and 2 MiB canonical bytes. Provenance trees
admit at most 16,384 nodes, depth 24 and 128 KiB aggregate UTF-8 text, including
keys; validate before detaching. No unlimited override or iterable materialization
is supplied. These are result/input admission bounds, not process-memory or
throughput guarantees for arbitrary external quantity backends. Larger native
collections require explicit future profiles/batching, not silent truncation.

ArgDigest owns closed public signatures and argument admission. DepDigest gates
explicit PyUnitWizard activation. SMonitor owns categorical diagnostics and
application capture policy; never stringify native errors or attach raw payloads
automatically. Retain native causes. New categories distinguish structure (E330),
unsupported format (E331), native quantity/geometry failure (E332), budget (E333)
and missing evaluation (E334); argument/capability categories remain E301/E312.
All dictionaries and quantities are checked again at scientific consumption.

Public PyUnitWizard >=0.28.1 supplies the selected record operations; actual floor
payload receiving remains required, separate from source pins and guide delivery.
No new engine, backend, network provider or dependency-floor change is selected.
Ackredit remains application-owned: serialization/reading retain existing
references without registering new extraction/software-method credit, enabling
hooks, starting replacement sessions or enriching bibliographies.

## Receiving and remaining integration

The [receiving receipt](evidence/native_feature_payload_20261111.json) receives
source 92d97fb and its exact owned wheel: 245 selected cases each, including 95
new payload controls and 150 earlier writer/reader/native cases. All 232 wheel
payloads/177 runtime bodies verify, with 168 loaded PHMT modules from the target.
Actual public PyUnitWizard 0.28.1 bytes, eight source/owned nm/pm guide blocks and
strict full docs pass. The first task-owned launcher omitted its spawn main
guard; the original 234-pass/four-failure run, guarded 238 passes and expanded
245 passes remain distinct. No writer assertion was relaxed to receive them.

Receive source and one exact owned artifact, all six families and original frozen
inventories, nondefault nm/pm policy, explicit empty and unobserved coverage,
subset/nonzero frame/state maps, detached ownership, wrong sealed units/field/
shape/charge/map inputs, finite bounds, actual diagnostics and no-new-credit
original-reference equality. Receive fresh cold inspection with scientific
imports blocked and application policy retained. Execute a friendly and expert
recipe through the same public operations. Preserve first failed attempts.

Archive integration must use this same validator at stage and publication; it
cannot copy a prior success flag. Specify how a new record's source/occurrence
and archive ordinal are assigned and how earlier originals/global ordinals are
preserved before implementing arbitrary/subset assembly. #194/#195 stay partial
until those separately identified operations are received. Full exact-head/
platform/public delivery (#9/#192/#10/#23), molecular collection (#624), biological,
representative human and scale gates remain independent; #148/#165 stay stopped.
