# Native provenance and persistence

Reviewed 2026-10-07 under
[#25](https://github.com/uibcdf/pharmacophoremt/issues/25).
The shared consumer boundary is `pharmacophoremt._private.molsysmt.detached()`;
native JSON/YAML writers call it for the complete model dictionary. It is an
implementation helper, not a new public metadata conversion API. Public model
persistence is provided by `pharmacophoremt.io.to_json`, `load_json`, `to_yaml`
and `load_yaml`.

## Literal text versus scientific quantities

Provenance strings retain their contents, including identifiers such as `a`,
`b`, `nm`, `s`, and text such as `1 nm`, `2 m` or `1 ps`. Being interpretable
as a unit expression does not make an identifier or note a physical quantity.
String subclasses, including NumPy text scalars, normalize to builtin `str`.
This happens before quantity-object detection. It does not change the provider's
valid parsing of explicitly supplied scientific arguments.

Actual quantity objects use PyUnitWizard's public `QuantityRecord` codec and
retain a value and negotiated unit. Metadata readers retain that portable
record rather than guessing its unit or automatically converting every field
to an active quantity. Decode a known quantity field with
`puw.QuantityRecord.from_dict(record).to_quantity()` and extract with an explicit
target unit such as `puw.get_value(quantity, to_unit='nm')`.

Nested dictionaries and list/tuple values detach recursively; NumPy numerical
arrays and scalar values normalize to native data. Detached containers are
independent of the producer's mutable inputs. This contract covers the supported
native metadata values; arbitrary Python objects are not promised a portable
serialization. It does not repair previously corrupted saved records.

## Model boundary and readers

The native dictionary writer detaches the whole payload, including root names,
description and metadata, each site's metadata and nested source-model history.
It does not alter the original model or molecular source. YAML uses `safe_dump`
and `safe_load`, without Python object tags. JSON and YAML preserve original
text and source/support identifiers rather than only agreeing with another
already transformed producer representation.

Supported native model geometry is written in explicit fixed `nm` lengths and
dimensionless directions. Readers verify the file's unit declaration, construct
geometry using those units and preserve physical values under a different
application standard-unit policy. Scientific metadata records carry their own
units; a session default does not replace them. Model geometry and metadata
records have distinct declared boundaries.

Undefined observation quantities use the existing sealed provider encoding;
that separate correction belongs to [#35](https://github.com/uibcdf/pharmacophoremt/issues/35).
This text does not relax finite molecular/site geometry or close that issue.
Native schema evolution, broader codecs and extension support remain separate.

## Independent guards and evidence

The owning regression is
`tests/test_contracts.py::test_detached_provenance_preserves_literal_strings_and_quantity_objects`:
original identifiers and normalized builtin text, independently decoded 0.12 nm
and unchanged detached arrays after source mutation. The additional
`test_native_saved_consensus_preserves_original_text_and_physical_units` checks
actual aligned consensus with original `a`/`b` sources and supporters through
both public formats. It writes under pm/fs/degrees and reads under
angstrom/ps/radians, checks literal values against caller expectations, verifies
root/site quantity records and analytically expected 0.17 nm center/0.06 nm
radius, and leaves the producer's NumPy text/arrays untouched by serialization.

`tests/test_curation.py` independently covers builtin NumPy text, safe YAML,
non-default-unit JSON/YAML and complete original observation/curation lineage.
`tests/test_aligned_cliques.py` and `tests/test_reference_ligand.py` retain
source, supporter and saved-model identity in real-provider native workflows.
The affected recipes are [aligned cliques](../docs/content/cookbook/aligned_cliques.md)
and [curation](../docs/content/cookbook/pharmacophore_curation.md).

The dated review receipt is
`devguide/evidence/literal_provenance_review_py314.json`. Original reports and
archives retain their producer identities and historical results. This review
qualifies the declared source persistence controls, not activity/biological
performance, a public release, a general arbitrary-object codec or historical
record recovery. No MolSysMT or PyUnitWizard implementation is modified.

### Undefined-quantity review — 2026-10-09

The separate correction in #35 is now reviewed and resolved. Actual saved native
aromatic JSON/YAML measurements preserve undefined quantities under changed
application units; finite metadata keeps its existing record representation.
The [aromatic persistence contract](aromatic_interaction_workflow.md#persistence-review--2026-10-09)
and [dated receipt](evidence/nonfinite_provenance_review_py314_summary.json)
record this additional evidence. Molecular and site geometry still require
finite values. The original #25 review and its evidence remain unchanged.
