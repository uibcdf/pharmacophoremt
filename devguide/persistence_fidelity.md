# Pharmacophore persistence: fields, schema and ownership

## Native schema and writer receiving — 2026-11-04

[#76](https://github.com/uibcdf/pharmacophoremt/issues/76) completes the next native
slice: [native schema contract](native_schema.md), with 265 focused checks in the
[receipt](evidence/native_schema_writing_20261104_summary.json). New JSON/YAML are
tagged pharmacophoremt.native@1; explicit unknown schemas/fields fail and legacy
untagged files retain defaults. Producer versions remain independent. Writers
validate and fully encode before opening, preserving destinations on validation/
serialization failure; OS write/crash/concurrency guarantees are not claimed.
SDF source and historical private payload are unchanged; #74 remains pending.
The original matrix below describes its earlier #75 checkpoint; native schema,
unknown-field and writer rows are superseded by this dated contract.

Reviewed 2026-11-04 on base 83e13bd7d5fbcf42ca10dad1ebeb76cdfe47ae97 and the
[#75](https://github.com/uibcdf/pharmacophoremt/issues/75) validation overlay.
Owner: LMMV/dprada. This is the first bounded review for audit item 4; it does not
certify every translator, future schema or arbitrary Python extension.

## Molecular representation ownership

MolSysMT owns construction, reading, writing, inspection and manipulation of
molecular representations, including SDF/PDBQT and any other molecular format.
PHMT owns pharmacophore hypotheses and their schemas. A pharmacophore payload in
an SDF does not transfer ownership of its CTAB, atoms, bonds or SD-property engine
to PHMT. Generic `io.load` already delegates molecular formats to MolSysMT.

**Existing annotated SDF implementation is migration debt:** `io/sdf.py` directly
uses RDKit for its container. [#74](https://github.com/uibcdf/pharmacophoremt/issues/74)
tracks migration; [MolSysMT #215](https://github.com/uibcdf/molsysmt/issues/215)
has the concrete consumer handoff for public SD-property/record access. Read-only
review of provider 71fbe4f46d3c70e4e973c8025f01752a8c9b1084 finds public SDF
conversion but native SD-property storage explicitly pending. Identity copies
retain bytes without supplying the required property/construction API. No new
provider execution or public delivery is inferred from that source review.

Freeze the existing container implementation pending a compatible provider route;
do not extend it, use private CTFile helpers, discard its tags or implement another
local parser. Native JSON/YAML can progress independently. LMMV/dprada review this
debt on 2026-11-18 or when the provider exposes the route. This is a tracked
migration disposition, not an assertion of architectural compliance.

## Field and format matrix

| Field / contract | Native JSON and YAML | Annotated PHMT SDF @1 |
| --- | --- | --- |
| Format identity | `software: pharmacophoremt`; `version` describes the producer | Outer `PHARMACOPHOREMT_SCHEMA=pharmacophoremt.sdf@1`; `PHARMACOPHOREMT_MODEL` carries the native payload |
| Schema version | No independent native schema version/admission policy yet; producer version is not a schema version | Unknown outer schema refused; existing @1 scientific-field guards remain qualified separately from ownership |
| Name, description, score, reference indices | Written/read as existing native fields; optional fields retain historical defaults | Complete payload fields required by @1 |
| Model/site metadata | Detached native containers; quantities use portable PyUnitWizard records, literal strings retained; readers require dictionaries (None normalizes to empty) | Same native payload representation plus strict @1 field admission |
| Features, essential, weight | Public site validators now apply on read: known features, boolean essential, finite nonnegative weight. Existing normalization (such as feature deduplication) remains | @1 requires complete site fields; repeated/unsupported features and invalid constraints refused before reconstruction |
| Point, Sphere, SphereAndVector, Disk, GaussianKernel, Cylinder | Supported geometry reconstructed via public validators; finite 3-vectors, positive radii/sigma, nonzero valid directional vectors; constructor direction normalization retained | Six supported shapes in full-precision payload; independent rounded display anchor |
| Units | Saved lengths explicitly nm, directions dimensionless; incompatible declared units refused. Missing units retain documented historical nm/dimensionless convention | Both unit declarations required by @1 |
| Empty model and site order | Supported; historical missing site list still means empty | Supported; exactly one record, matching virtual-site count and order |
| Unknown native fields / future producer versions | Existing behavior unchanged: extra fields may be ignored, producer version is not an admission gate. Needs explicit schema/migration policy | Strict outer @1 field set; no silent extension |
| Molecular system / arbitrary attributes | Live molecular system and undeclared Python attributes are not serialized; indices do not recreate a molecular source | Same limit; virtual display atoms are not a prepared ligand |
| Writer validation of manually corrupted objects | Not qualified by #75; reader correction does not certify every writer failure/transaction path | Existing strict @1 validation before destination opening; container migration still pending #74 |

Legacy optional defaults remain: essential=True, weight=1, metadata={}, units
nm/dimensionless and empty site list. #75 does not claim strict required-field
admission for every historical native record. A rejected record yields no returned
partial model. Valid geometry can differ at floating roundoff after unit conversion;
controls use rtol=1e-13/atol=1e-14 for serialized geometry, exact supported scalar,
constraint, text and metadata checks otherwise.

Shapelet remains a placeholder outside the qualified six-shape scope. Other
translators (LigandScout/Pharmer/RDKit pharmacophore objects) need their own field
matrix. Availability of a class does not establish matcher/format support.

The [Pharm3D comparison](rdkit_bounds_comparison.md) explicitly configures bounds
after the existing center/family projection. [#140](pending_proposals/qualify_rdkit_projection.md)
now owns RDKit's preserved/projected/lost fields, admission and deliberate
compatibility decision; the comparison does not establish a constraint round trip.

## Executed checks and next steps

[#75 receipt](evidence/native_persistence_validation_20261104_summary.json):
207 focused source checks pass, including 48 new native persistence cases and
existing I/O/SDF/metadata/curation/site/shape controls. Initial original-production
run: 34 refusal guards fail, 12 positive guards have an overly exact floating-point
assertion, and two historical-default controls pass. Corrected geometry assertions
pass with numerical tolerance; every attempt is retained. One intermediate run's
identity changes only because the test correction was made before that run finished;
its runtime/provider sources remain stable. The final run has fully stable identity.
Linux/Python 3.14.7 with extracted public ArgDigest 0.17.0 and inherited scientific
dependencies; no full-suite, clean installed/all-platform or predictive claim.

Next: define native schema/version admission, unknown-field preservation/refusal
and a compatibility migration policy; assess writer rejection before file changes.
Keep those changes independently reviewable from the #75 validation repair. Resume
SDF migration only with the public provider contract and real consumer receiving.

## Native diagnostic receiving — 2026-11-04

[#81 contract](native_io_diagnostics.md) and
[receipt](evidence/native_io_diagnostics_20261104_summary.json) add coded owned
native I/O refusals (PHMT-E108/E109) while preserving ValueError/TypeError catch
compatibility, data admission and original parser/provider/filesystem errors.
243 selected cases pass; exact concrete types/wording migrate explicitly.
#6 dependency declarations align nglview and the existing direct PyYAML codec.
No native schema, scientific algorithm, molecular/SDF implementation or installed/
public qualification change; broader ArgDigest admission remains separate.

## RDKit projection source receiving — 2026-11-07

The [owning RDKit contract](rdkit_projection.md) now qualifies default point
projection, explicit sphere/radius exchange and detached field/loss/default
reports in source. Native formats retain complete native semantics; RDKit field
preservation does not establish matching equivalence. #140 remains partial
pending same-artifact installed receiving, separate from public/full platform gates.
