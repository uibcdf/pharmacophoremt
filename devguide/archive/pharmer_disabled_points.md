---
summary: Preserve or explicitly refuse disabled-point meaning during Pharmer JSON import.
issue: uibcdf/pharmacophoremt#162
status: resolved
opened: 2026-11-09
closed: 2026-11-09
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

## Bounded installed closeout — 2026-11-09

The [installed receipt](../evidence/pharmer_enabled_installed_20261109.json) pins
source0407e20b26cd0d60528a56f90f471a1fa257d0c9 and exact owned wheel
0.4.0+196.g0407e20 (4528075bytes, SHA-256
33f919fdbe7e26af2fc6841ce1394c287b0d4ad3c55ccc235c150aaca364d03b).
The same34original test bodies pass,22new/12P1, with no skips/reported warnings.
All211payload/156runtime files and nine original fixtures verify;152loaded
runtime origins are in the owned prefix with no PHMT checkout fallback.

The public guard above directly checks omission and original point mapping;
the independent actual two-ion evaluation also protects the former spurious
required-site veto. Two all-true/missing ordinary19point outputs retain identical
source native JSON bytes; installed scientific payloads equal those originals
with generated versions retained and compared separately. The complete P1driver
also passes all three original answers in source and installation, preserving
nine actual attribution items/22uses and refusing overwrite of original output.

Original red/over-strict unit-control results remain archived. The source tests
use explicit unit tolerance without changing physical radii or evaluator slack.
The original bundled file remains unchanged with10true/9false point flags;
existing legacy count assertions become10, with historical full unlabelled
attachment still separately unexecuted under this profile. A real explicit
one-ion attachment passes. Do not promote it into that wider legacy gate.

Scientific receiving retains DATA512MiB/AS1GiB/observedRSS512, CPU19/thread1/low
priorities and20percent host reserve; actual installed sampled own-group peak is
363839488bytes. No kernel aggregate MemoryMax/swap/tasks/quota guarantee, budget
raise, environment acquisition, provider/native/shared-prefix update or148retry.
This closes162within its bounded source/owned-installed scope. Broader profile163,
actual external128and full source/public/platform/biology/performance/release
qualification remain separate open work. Earlier receipts retain original states.
