---
summary: Expose explicit bounded receptor hypotheses from native cached features.
issue: uibcdf/pharmacophoremt#87
status: resolved
opened: 2026-11-05
closed: 2026-11-05
verification: measured
area: [modeling, api]
guard: tests/test_public_receptor_generation.py
normative: devguide/public_receptor_generation.md
blocked_by: []
supersedes: []
---

# Public cached receptor generation

Promote #86's bounded scientific profile into `modeler.from_receptor_features`,
composing the existing public projection constructor. Require an explicit profile,
unit-bearing distance choices/radius and finite budget. Enumerate all admitted
source occurrences with separate aromatic faces; record unsupported records and
budget completion without biological inference. MolSysMT retains all molecular
work. Existing facades and dependencies are unchanged.

Acceptance requires independent synthetic and unchanged prepared-case controls,
multiple source occurrences, a large bounded product, explicit units, invalid/
empty/unsupported cases, blocked molecular access, independent results, native
recovery, ArgDigest/SMonitor and actual optional attribution.

**192 selected controls pass in 218.87 s (54 new)**, zero failures/errors/skips.
Two unchanged prepared PHE404 unit-policy cases recover all eight models and
match the original independent coordinate oracles. A bounded 4^40 product
materializes only two hypotheses. All four cookbook blocks and a separately
captured three-hypothesis prepared replay execute, preserving coordinates,
chemical history, cached observations, unit policy and actual data/operation
credit. After a docstring-only clarification, 52 fast controls pass again.

The [receipt/full evidence](../evidence/public_receptor_generation_20261105_summary.json)
retains five stable source/native/helper/test/input/metadata before/after checks.
Initial 45-case execution passes six/fails 39 due to undeclared skip forwarding;
the public builders now explicitly declare the existing standard boolean control
while retaining scientific checks. The 54-case focus then passes 52/fails two
new guards expecting literal `nm` instead of canonical `nanometer`; the guard
now recovers QuantityRecords and checks the declared physical values. Numerical
oracles/tolerances are unchanged. Initial source, guards, logs and outputs remain.

Only this explicit cached profile is accepted. General molecular work stays in
MolSysMT, further acceptor geometry in #375 and optional pockets in TopoMT #101.
The package-resource inventory includes the two new runtime modules; its existing
22-case guard initially identified those missing entries and now passes.
No provider/pin/floor/package-publication/preparation change or full scientific/installed/
public/platform/hosted qualification follows. Next compose optional cached
receptor exclusions; broader #6/#82 and scientific/data gates remain separate.
Owners LMMV/dprada; capsule `/tmp/phmt-public-receptor-20261105-p20atfmx`, review
2026-11-19 or scientific/source change. No continuing local process required.
