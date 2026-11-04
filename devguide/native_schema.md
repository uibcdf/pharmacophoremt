# Native pharmacophore JSON/YAML schema

Owned by [#76](https://github.com/uibcdf/pharmacophoremt/issues/76), reviewed
2026-11-04. This contract describes pharmacophore data. All molecular-system
representations, format operations and inspection remain MolSysMT-owned.

## Admission and compatibility

New `io.to_json` / `to_yaml` exports use **schema: pharmacophoremt.native@1**.
`version` remains the producing package version, independent of schema admission.
A future producer version with the known schema is accepted. An explicit unknown,
null or malformed schema marker is rejected; it never falls back to historical
interpretation. Metadata may contain its own arbitrary schema/provenance labels.

JSON and YAML represent the same native record. Tagged data must have exactly
these model fields (all required, including fields whose value may be None):

`schema`, `software`, `version`, `name`, `description`, `score`, `ref_mol`,
`ref_struct`, `metadata`, `units`, `interaction_sites`.

`software` must be pharmacophoremt and `version` a string. `interaction_sites`
is an ordered list. Every site requires exactly `features`, `essential`, `weight`,
`shape`, `metadata`. Shape fields are:

| Shape type | Required fields, in addition to type |
| --- | --- |
| point | position |
| sphere | center, radius |
| sphere and vector | center, radius, direction |
| disk | center, radius, normal |
| gaussian kernel | center, sigma |
| cylinder | start, end, radius |

Unknown/missing fields at these three levels fail visibly. Shapelet remains
outside this schema's supported geometry. Extensions carrying new scientific
meaning require an explicitly reviewed schema/compatibility change; they cannot
be added as fields that old readers would silently ignore. Application provenance
belongs in metadata, where unknown keys are retained. Use JSON object string keys
and supported native scalar/list/mapping values for portable metadata. Arbitrary
Python objects are not a promised serialization domain.

The envelope is finite and JSON-encodable, including when represented as YAML.
Raw NaN/Infinity and unsupported YAML/Python values fail in tagged records.
PyUnitWizard portable quantity records retain their explicit units and encoding;
the host does not implement a new quantity codec. Length geometry is fixed nm,
directions dimensionless; incompatible unit declarations are refused. Public
shape/site/model value validators supply scientific checks and their existing
normalization (including directions and feature names), rather than a second
validator implementation here. Thus field completeness is distinct from raw
Python type identity or a promise to preserve invalid manually edited state.

Historical **untagged** records keep their existing admission and defaults:
missing units mean nm/dimensionless; essential=True, weight=1, metadata={} and
missing site list means empty. Scientific value validation from #75 still applies.
Legacy extra fields can be ignored as before. This is backward compatibility,
not a promise to retain unknown legacy extensions through load/re-save. Inspect
such extensions before migration. Current tagged exports do not change the bytes
of historical files; older readers cannot be retroactively made schema-aware.

## Writer failure boundary

Both writers first detach the model, add the native schema marker, validate via
existing native reconstruction/public value checks, and completely encode the
text. Only then do they open the destination. Scientific validation, unsupported
objects and serialization failures therefore leave an existing destination's bytes
unchanged and do not create an absent file. Successful calls still return None
and support existing/new string or Path destinations. Files use explicit UTF-8.

This is an in-memory validation/encoding boundary. It does not promise atomic OS
replacement, crash/power-loss durability, concurrent-writer coordination or
protection from a disk error after opening. No generic filesystem transaction
framework or performance advantage is introduced.

## Relationship to annotated SDF

The private `_to_dict` historical payload is unchanged. The native JSON/YAML
schema tag is added only at their export boundary. `pharmacophoremt.sdf@1` keeps
its existing outer schema and untagged internal payload; its six-shape controls
compare every pharmacophore field after separating the native JSON envelope.
No SDF container operation or provider implementation changes. The direct RDKit
container remains migration debt in #74, waiting for public MolSysMT #215 record/
property support. This native schema does not authorize extending that code.

## Verification and remaining scope

[Receiving receipt](evidence/native_schema_writing_20261104_summary.json) retains
265 passing focused controls (58 new schema/writer cases), exact bytes on base
0413e6cc4c8aeb28822b00a379c61fbe3294ee87, original failures and all attempts.
Original-production guards: 48 failures / 4 passes. First broader run: six SDF
comparison assertions expected identical envelopes; all other 253 controls passed.
Those six now require equal complete pharmacophore payloads plus distinct correct
schema envelopes. Final runtime/source/native/test/metadata identity stays stable.
Linux/Python 3.14.7 source receiving with extracted public ArgDigest 0.17.0 and
inherited scientific dependencies; no full-suite, clean installed, all-platform
or predictive qualification.

Audit item 4 still needs per-format translator fidelity (LigandScout/Pharmer/
RDKit pharmacophore objects) and the provider-backed SDF migration. Native schema
admission and validation/encoding-before-open are the completed bounded slice.
Next independent audit theme is #60's live molecular references and independent
variants; molecular copying itself must use supported MolSysMT operations.

## Native diagnostic receiving — 2026-11-04

[#81 contract](native_io_diagnostics.md) and
[receipt](evidence/native_io_diagnostics_20261104_summary.json) add coded owned
native I/O refusals (PHMT-E108/E109) while preserving ValueError/TypeError catch
compatibility, data admission and original parser/provider/filesystem errors.
243 selected cases pass; exact concrete types/wording migrate explicitly.
#6 dependency declarations align nglview and the existing direct PyYAML codec.
No native schema, scientific algorithm, molecular/SDF implementation or installed/
public qualification change; broader ArgDigest admission remains separate.
