---
summary: Expose Point centers consistently in native geometry inspection.
issue: uibcdf/pharmacophoremt#142
status: resolved
opened: 2026-11-07
closed: 2026-11-07
severity: medium
verification: reproduced
area: [core, geometry, inspection]
guard: tests/test_point_geometry_inspection.py::test_native_queries_preserve_known_centers_and_three_four_five_distance
normative: devguide/native_geometry_inspection.md
blocked_by: []
supersedes: []
---

# Point centers in native inspection

At64a8a5d (runtime1040dbb), ordinary public center/distance queries succeed for
two native Spheres but fail for two Points or a mixed Point/Sphere model. Actual
error PUW-ERR-FORM-001 reports NoneType because InteractionSite.center sees no
Point.center and passes None to the units provider. The supplied positions are
valid; this is a PHMT query/representation defect, not a PyUnitWizard failure.
Empty center extraction also returns shape(0,) rather than(0,3).

The read-only reproduction and exact source hashes remain in
`build/phmt-point-inspection-20261107-w70p6o5n`. The
[prospective contract](../native_geometry_inspection.md) selects a read-only
alias to canonical Point.position and explicit empty coordinate columns. No
Cylinder center, Point radius, new molecular geometry implementation or changed
distance/scoring definition is introduced. The source correction passes338 selected cases (including16 new regressions);
exact owned installed receiving remains next. The earlier plugin-autoload
bootstrap failure,13 failing/3 positive before-correction cases and all source
hashes remain preserved. Current full-source acceptance stays separate; the separate current CI targets unchanged489be12.


## Resolution received 2026-11-07

Producer858fe5a4d3d4ea61649479802721c80476ae4925 exposes the canonical Point
position as a read-only center alias and returns explicit empty(N,3)center columns.
The named guard protects ordinary public queries for points, spheres and mixed
models under two unit contexts, checking known coordinates and distances without
a digestion bypass. Native fields and source coordinates remain unchanged.

[Source receiving](../evidence/point_inspection_source_20261107_summary.json)
passes338library cases plus24distribution/3reporting/18archive controls. The
[same-artifact installed receipt](../evidence/point_inspection_installed_20261107_summary.json)
passes the same338 original bodies, two guarded original subprocess bodies and
one unchanged RDKit recipe outside the checkout. Owned wheel0.4.0+151.g858fe5a
SHA25637a2c25dcdbd10ca702439330611eb4f8999b55506ca8234898f8138e44b3e97
retains210verified payload files and155nongenerated runtime files equal tosource;
141main file modules/three namespaces resolve to the installed target.

The first installed attempt passed337bodies but its receiving harness rejected
an additional original curation subprocess that had not yet been admitted. The
corrected harness admits exactly both unchanged original scripts with isolated
startup; the same wheel and tests then pass338. Preserve the first failure;
this is a receiving-control mistake, not a provider or library defect. Shared
provider file hashes and MolSysMT native2a79b9a8 remain unchanged. No public
package/platform/dependency/full-source/biology/performance acceptance follows.
#9/#23 retain those gates; CI489be12 predates this correction and its separate
analytical boundary failure is owned by#143.
