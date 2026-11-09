---
summary: Preserve or explicitly refuse disabled-point meaning during Pharmer JSON import.
issue: uibcdf/pharmacophoremt#162
status: open
opened: 2026-11-09
closed:
severity: medium
verification: measured
area: [io, screening, semantics]
guard:
normative:
blocked_by: []
supersedes: []
---

# Disabled Pharmer points become required PHMT sites

During#161P1 preparation, the actual public `io.from_pharmer` operation imports
three sites, all essential, after changing only the first point's `enabled`
field to false in the original three-point query. The caller dict remains
unchanged. The current implementation loops over all point entries without
examining `enabled`; the authenticated standalone r95JSON reader skips false
entries. No Pharmer executable is run and no external bug is alleged.

See the [measured probe](../evidence/pharmer_disabled_point_20261109.json) and
the narrow [P1profile](../pharmer_p1_comparison.md). P1has every point explicitly
enabled, so its analytical preparation is unaffected. Existing broad sample
loading does not assert disabled-field behavior. Its separate local resource
failure while loading an attached ligand/form adapter does not explain or
qualify this small successful semantic probe.

Preserve the omitted-point meaning under the supported profile, or explicitly
refuse the unsupported query; do not silently add a required constraint. Review
the existing public import contract before choosing behavior. Missing/true/false
controls, input immutability, geometry/units, original point/site mapping and
source/owned installed receiving are required for closure, with a durable public
guard and maintained format documentation. Optional/negated/vector/size/export
meanings and attached-ligand integration retain their separate scope. No new
engine, provider/parser fork, tolerance change or resource increase is needed.
