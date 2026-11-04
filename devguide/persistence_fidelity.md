# Pharmacophore persistence: fields, schema and ownership

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
