---
summary: Respect an already loaded Pint registry during unit-policy initialization.
issue: uibcdf/pharmacophoremt#191
status: resolved
opened: 2026-11-11
closed: 2026-11-11
severity: medium
verification: reproduced
guard: tests/test_unit_bootstrap.py
normative: devguide/release_0_5_0_source_cut.md
area: [interoperability, api]
blocked_by: []
supersedes: []
---

# Preserve an application-created registry

PHMT requested Pint disk caching after the registry was already constructed when
an application created a quantity before selecting standard units. The actual
provider warned and changed the requested setting without changing that registry.
The public loaded_libraries report now guards only the existing cache opt-in;
PHMT still selects its baseline when no policy exists, and preserves active
application policies and quantities. No numerical conversion or provider pin/minimum
changes. Molecular behavior is not executed by this focused receiving.

Three real fresh-process controls cover unloaded, preloaded/no-policy and active
nondefault application states. The first run contained one incorrect expected
unit-label assertion; it is preserved. The corrected original-code run has one
real preloaded-registry failure and two passes; all three pass after repair.
See the [original preparation receipt](../evidence/release_050_preparation_20261111.json).

The canonical PyUnitWizard guide was received from published owner
9f59894e0d803abbfba84cc84bf9111c51bb3f7d through the central synchronizer and an
isolated owner checkout. The live sibling and shared environment were untouched.
The seven guide copies match fresh connected canonical blobs. Guide delivery
is separate from adopting 0.29.2 or its cutoff-conversion behavior; controlled
scientific source pins remain unchanged. MolSysSuite#180 owns the guide handoff.
Full exact-candidate source receiving remains with #95/#9.
