---
summary: Annotated pharmacophore SDF silently loses directional geometry, weight and essential status.
issue: uibcdf/pharmacophoremt#47
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: medium
verification: measured
area: [io, modeling, scientific_integrity]
guard: tests/test_io_sdf.py::test_original_directional_donor_regression
normative: devguide/pharmacophore_sdf_persistence.md
blocked_by: []
supersedes: []
---

# Scientific site fields lost by the pharmacophore SDF codec

## What

An executed analytical round trip changes a donor query site from sphere-and-vector,
weight 2, optional, direction `[1,0,0]` to a sphere, weight 1, essential, with no
direction. This is PHMT-owned virtual-site persistence, separate from provider-owned
molecular SDF library ingestion/export.

## How

Construct `InteractionSite(SphereAndVector('[0,0,0] nm', '.1 nm', [1,0,0]),
'hb donor', weight=2, essential=False)`, write through `io.sdf.to_sdf()` and read
through `io.sdf.load_sdf()`. The codec source is unchanged from
`0f5819d79877288c7436ba2daf4cb6d222cd9cbe`; the normal editable Python 3.14.7
probe measures the above fields. The writer's `SITE_0_SHAPE` is ignored by a
reader that unconditionally constructs `Sphere`. Other measured fields are not
serialized or restored. Original driver, SDF and before/after output are retained
with the linked #46 review evidence; this finding remains independently open.

## Why

Reloading changes angular constraints, weighted coverage and mandatory-site status.
Keeping the operation in its correct component does not prove its persistence
contract. Native JSON/YAML fidelity and molecular collection codecs are separate.

## What is measured and what is assumed

One synthetic directional donor site's real round trip, not all shapes/fields,
foreign SDF interoperability, downstream biological outcomes or released artifacts.
The completed probe's temp context is removed. An earlier probe's diagnostic
serialization failed on a dimensionless Quantity; the corrected probe explicitly
extracts dimensionless values. That harness correction is not a codec repair.

## Alternatives and refuted paths

Do not move pharmacophore semantics into MolSysMT or conflate this with molecular
collection/property requests. Do not claim simple sphere round trips preserve
all site constraints. Do not silently restore unsupported geometry as a sphere.

## Scope and exclusions

Define this format's supported schema and legacy compatibility separately from
general molecule preparation, state manipulation or molecular library conversion.
#46 retires obsolete general modules and does not resolve this persistence defect.

## Acceptance criteria

Preserve supported scientific fields, or reject unsupported input before silent
loss. Independently guard direction, weights, essential status, non-default units
and explicit unsupported/legacy-format handling under the accepted codec contract.

## Original measurement

The [#46 review summary](../evidence/molecular_utility_retirement_review_py314_summary.json)
links the original probe driver, SDF text/checksum and before/after record under
`independent_sdf_finding` in the gzip archive. The codec is unchanged from the
recorded source base. Probe provenance was captured after execution, not frozen
beforehand; the exact source/measurement scope is retained explicitly. The
[#46 completion receipt](../evidence/molecular_utility_retirement_completion.json)
retains wrapper output and task resource cleanup. This bug remains open.


## Resolution — 2026-10-10

The versioned `pharmacophoremt.sdf@1` carrier stores the complete existing native
model JSON record, reusing the JSON/YAML model serializer and reconstruction.
All six supported native geometries, feature lists, weight, essential status,
model fields and model/site portable metadata are retained. Virtual helium atoms
show anchors in angstroms; authoritative geometry in the payload uses nm and
dimensionless directions. The reader validates the complete supported record and
consistent virtual atoms before reconstructing. Unversioned/foreign files,
unknown schemas/shapes, omitted scientific fields and multiple records fail
explicitly. Unsupported export is checked before opening the destination.

Historical SDFs lack required information and must be regenerated from an
original model or native JSON/YAML, rather than silently assigning default
constraints. This is an intentional compatibility correction. The live linked
molecular system remains outside the native persistence contract. Molecular
library conversion/preparation and `VirtualScreening.to_sdf()` are unchanged;
provider collection/property work remains separate.

`tests/test_io_sdf.py` guards the original reproduction, all supported geometries
across pm/degree and angstrom/radian contexts, exact payload precision, metadata,
empty/multiple-site order, invalid/legacy input and untouched destinations on
unsupported export. Independent placed-query controls exercise real MolSysMT
recognition for direction, weighted coverage and mandatory-site behavior. The
[new review summary](../evidence/pharmacophore_sdf_review_py314_summary.json)
links original focused/admin output, JUnit, producer/source/binary/input identities,
review driver and the initial test-development failures. Those failures were
incorrect fixture/oracle assumptions (site API rejects Shapelet; a query without
assignments is `not_matched` even with all sites optional), not a measured codec
repair. Their original output is retained. No full suite, hosted matrix, foreign
interoperability, release artifact or biological/performance qualification follows
from this local review. The original #46 failure record above remains unchanged.
