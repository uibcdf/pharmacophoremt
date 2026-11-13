---
summary: Declare Pandas ownership for the public table APIs.
issue: uibcdf/pharmacophoremt#206
status: open
opened: 2026-11-13
closed:
severity: medium
verification: inspected
area: [packaging, dependencies]
guard:
normative:
blocked_by: []
supersedes: []
---

# Pandas dependency ownership

Pharmacophore.to_dataframe and VirtualScreening.to_dataframe directly import
Pandas. The package runtime dependencies, Conda recipe run requirements and
DepDigest library inventory do not declare this consumed provider. Test
environments and MolSysMT's dependency can mask the missing direct ownership.
No fresh public installation failure is claimed from this static observation.

Choose a hard dependency or a documented optional boundary guarded through
DepDigest. Justify the supported floor from consumed APIs and actual receiving;
do not infer it from the workstation version. Align metadata, recipe, maintained
environments and the applicable dependency inventory/central graph, then verify
the public table route without borrowing test-only/transitive availability.
This issue changes no shared prefix, provider, runtime floor or release gate.
It remains separate from #207's controlled native-reader recovery and #10/#23's
complete installed/public closure.
