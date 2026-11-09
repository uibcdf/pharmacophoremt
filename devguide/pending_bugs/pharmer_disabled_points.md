---
summary: Preserve or explicitly refuse disabled-point meaning during Pharmer JSON import.
issue: uibcdf/pharmacophoremt#162
status: partial
opened: 2026-11-09
closed:
severity: medium
verification: measured
area: [io, screening, semantics]
guard: tests/test_pharmer_enabled.py::test_disabled_point_is_omitted_with_original_point_mapping
normative: devguide/pharmer_interoperability.md
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

## Source correction — 2026-11-09

The [enabled-point contract](../pharmer_interoperability.md) now omits false
points before feature/geometry parsing, defaults missing flags to true and
refuses nonboolean flags using the existing structured type diagnostic. Filtered
imports retain original point/survivor mappings; ordinary imports keep metadata
unchanged. The original bundled JSON has ten enabled and nine disabled points,
so expected enabled counts are corrected from19to10without changing its bytes.

All34 selected source cases pass (22new/12original P1), including actual two-ion
evaluation, public routes/unit policy, metadata persistence and explicit attached-
ligand delegation. Two frozen ordinary19point all-true/missing profiles produce
byte-identical complete native JSON before/after. The first red run contains20
policy/omission failures plus two overly strict test unit-conversion comparisons;
corrected ordinary controls pass before runtime mutation. Preserve those identities.
Full historical unlabelled attachment remains separately unqualified under this
small profile. The [source receipt](../evidence/pharmer_enabled_source_20261109.json)
receives strict docs, full Ruff / 439 formatted files, index / three reporting
and18archive tests. Exact owned installed receiving is pending.
The broader import/loss policy is separately open as#163; no external execution
or other field equivalence is inferred.
