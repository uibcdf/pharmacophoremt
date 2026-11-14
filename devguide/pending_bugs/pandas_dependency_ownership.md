---
summary: Declare Pandas ownership for the public table APIs.
issue: uibcdf/pharmacophoremt#206
status: active
opened: 2026-11-13
closed:
severity: medium
verification: measured
area: [packaging, dependencies]
guard:
normative:
blocked_by: []
supersedes: []
---

# Pandas dependency ownership

## Implementation receiving — 2026-11-13 local date

Choose a direct hard dependency, `pandas>=2.3.3`, retaining the two existing
Pandas-returning APIs and CSV behavior. The floor is justified by the
[provider's Python 3.14 compatibility statement](https://pandas.pydata.org/pandas-docs/version/2.3/whatsnew/v2.3.3.html),
not the workstation version. Metadata, recipe, DepDigest and all seven
runtime/scientific/public receiving profiles now declare that floor. The
production/development/docs profiles use the accepted generator; build/setup
and the historical importable fixture retain their distinct scope.

The private public-PyPI wheel and installed payload bytes for Pandas 2.3.3,
Pandas 3.1.1 and the older branch's required `pytz` are authenticated. The
focused source selection passes 95 existing tests with Pandas 2.3.3, including
nm/pm quantities, empty tables, cell identities and native hit/CSV behavior.
All 163 administrative controls and the declared-route preflight pass. A new
regression protects direct required ownership and its floor; the existing
editable-provenance negative control now uses an admitted simulated Pandas
version so it still reaches its intended rejection.

Three preparation attempts stopped before test execution: a copied bootstrap
resolved an unintended editable provider; the minimum's missing `pytz` was
refused; source test support was already resolvable and could not be staged
again. The corrected source route uses ordinary source support. The first
administrative run rejects the stale simulated version; original outputs stay
in the task capsule. No provider behavior was patched to hide these failures.

The live central graph policy, Git blob
`704045ff35a203db6503d55c2a60ba640149171b`, explicitly excludes third-party
packages. Pandas therefore adds no registered-component edge and needs no
graph regeneration. No registered provider, pin or acquisition route changes.

Next freeze this implementation, build its exact owned wheel, and run the same
95 tests with each authenticated Pandas version outside the source checkout.
Keep the issue active until that receiving is complete. This is not complete
public dependency closure or supported installed/platform qualification.
Future alternative-engine evaluation remains separate under #210/MolSysMT#749.

## Original observation

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
