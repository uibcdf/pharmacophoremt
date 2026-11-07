---
summary: Expose Point centers consistently in native geometry inspection.
issue: uibcdf/pharmacophoremt#142
status: partial
opened: 2026-11-07
closed:
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
