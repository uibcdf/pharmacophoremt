# Annotated pharmacophore SDF persistence

Owned by [PharmacophoreMT #47](https://github.com/uibcdf/pharmacophoremt/issues/47).
`pharmacophoremt.io.to_sdf(model, path)` and `load_sdf(path)` persist one PHMT
pharmacophore. `Pharmacophore(path, form='sdf')` uses the same reader. Generic
`io.load()` continues to delegate molecular SDF input to MolSysMT; it does not
infer a pharmacophore from molecular atoms.

## Version 1 contract

The SDF contains two required SD properties:

- `PHARMACOPHOREMT_SCHEMA`: exactly `pharmacophoremt.sdf@1`.
- `PHARMACOPHOREMT_MODEL`: the complete JSON object produced by the existing
  native PHMT serializer used for JSON/YAML. Its software version describes
  the producer; the separate schema tag identifies this SDF format.

The payload is authoritative for reconstruction. It retains feature lists,
weights (including zero), essential status, full supported geometry, model name,
description, score and reference indices, and model/site metadata. Lengths in
that object are explicitly nm; direction/normal vectors are dimensionless.
Portable quantity records and literal strings in metadata follow the native
serializer's existing contract. The live `molecular_system` is not saved, as
with native JSON/YAML; reference indices alone do not recreate it.

| Supported shape | Saved geometry | Display anchor |
| --- | --- | --- |
| Point | position | position |
| Sphere | center, radius | center |
| Sphere and vector | center, radius, direction | center |
| Disk | center, radius, normal | center |
| Gaussian kernel | center, sigma | center |
| Cylinder | start, end, radius | start |

One unbonded helium virtual atom per site displays the anchor in angstroms, in
site order. This is a display carrier, not a prepared molecule. Its mol block
can round coordinates; exact supported geometry comes from the JSON payload.
The reader checks atom count/type, absence of bonds and agreement of anchors
within 0.000051 angstrom (V2000's four-decimal rounding). An empty model is
supported. Multiple records are rejected rather than silently selecting one.

Required model/site/shape fields cannot be omitted or extended under this schema;
missing weights or essential status never acquire silent defaults. Unknown
schemas/shapes, malformed records, non-finite numbers, invalid constraints or
inconsistent display atoms fail explicitly. Export checks and JSON encoding
happen before opening the destination. Shapelets are unsupported by this format.
Read failures return no partially restored model.

## Historical compatibility and ownership

The former unversioned `SITE_i_FEATURES/SHAPE/RADIUS` representation omitted
weights, essential status and directional geometry; its reader also ignored the
shape tag. Those files, and foreign molecular SDFs, are rejected with an actionable
message. Regenerate from the original model or retain native JSON/YAML. There is
no automatic lossless migration from absent information. External tools that
strip the SD payload or move virtual atoms cannot preserve this format's contract.
No third-party pharmacophore SDF interoperability is claimed.

JSON/YAML remain the native persistence routes without an SDF display carrier.
This change reuses their model serialization/reconstruction and the owning
feature validator; it does not change their format or promise to serialize every
custom Python attribute. General molecular conversion, preparation and library
collection/property fidelity remain MolSysMT responsibilities. In particular,
`VirtualScreening.to_sdf()` remains retired pending provider-owned molecular
collection capabilities (#215 follow-up / #223).

## Verification

`tests/test_io_sdf.py` independently checks all six supported geometries, weights,
essential status, feature order, literal/provenance metadata, non-default unit
contexts, precision beyond the mol block, the constructor, empty/multiple sites,
unsupported export without destination changes, historical input and malformed
schema/constraint/anchor controls. A real MolSysMT-recognized prepared donor
checks placed-pose directional acceptance, weighted coverage and missing mandatory
sites before and after persistence. These are analytical controls, not biological
validation, full-suite qualification or released-artifact evidence. The new review
archive is linked from the resolved owning report; the original failing probe
remains unchanged in the #46 archive.
