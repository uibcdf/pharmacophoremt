---
summary: Receive MolSysMT chemical-domain separation with unchanged scientific profiles.
issue: uibcdf/pharmacophoremt#69
status: partial
opened: 2026-10-28
closed:
verification: measured
area: [integration, modeling, screening, validation]
guard: tests/test_conformer_screening.py
normative: devguide/chemical_domain_receiving.md
blocked_by: [uibcdf/pharmacophoremt#9]
supersedes: []
---

# Chemical-domain receiving preparation

## Provider correction received; exact candidate CI pending — 2026-11-03

MolSysMT #531 is closed. Clean consumer **7e5b5a5a3ee9c60528864928e56d1abac8aeaf9d**
on `receiving/chemical-domain-fixed-20261103` receives provider **0faf1584**.
The [new receipt](../evidence/chemical_domain_fixed_provider_receiving_20261103_summary.json)
records **1,009 source tests passed**, including all original 22 controls and the
four unchanged typed-preservation cases; a separate **110-case installed-wheel
selection passes** with actual installed origins/bytes checked before and after.
No consumer molecular fix or weaker scientific assertion is introduced.

Source/native/test bytes are stable; distribution-metadata lookup differences,
shared dependency conflicts and the bounded installed-wheel scope remain explicit.
This does not qualify clean public dependency closure or the full installed Conda
matrix. The 67 administrative controls pass after retiring only owned build/cache.

Main retains runtime/pins while [candidate CI 41674239397](https://github.com/uibcdf/pharmacophoremt/actions/runs/41674239397)
finishes: governance and Linux 3.13/3.14 pass at the receipt; six scientific cells
are still active/queued. #9 owns that receiving gate. Next inspect all eight actual
test steps at exact 7e5b5a5, integrate directly if green, update the durable guard
to the candidate's domain module and inspect main CI. #69 remains partial.
Later macOS 3.14 cancellation is a hosted runner-capacity failure before any step;
the [native addendum](../evidence/chemical_domain_ci_capacity_20261103.json)
retains the cause and rejected individual-rerun attempt. Recover that cell after
the active attempt settles; Linux 3.11 has now passed too. Historical receipts
and the earlier handoff below retain their original claims.

## Reviewed isolated candidate and typed-fidelity handoff — 2026-11-02

The owner's candidate is [43a258c](https://github.com/uibcdf/pharmacophoremt/commit/43a258c516ebb3c8f971ac45629a1a60b3871fab),
branch `receiving/chemical-domain-owner-20261102`; main runtime/pins are retained.
The [full source receipt](../evidence/chemical_domain_receiving_20261102_summary.json)
preserves 998 passes / 11 failures / zero skips, with all original 22 baseline
nodes passed. After client-side corrections, the
[clean candidate confirmation](../evidence/chemical_domain_candidate_confirmation_20261102_summary.json)
passes 73 focused controls. Its six added domain guards live in the candidate's
`tests/test_chemical_domain_receiving.py`, not the unchanged main runtime.

Four typed-state preservation assertions still fail on component_name/type dtype
changes after public extraction. [MolSysMT #531](https://github.com/uibcdf/molsysmt/issues/531)
owns the minimal public repro and required dtype disposition/correction, continuing
the [original #255 handoff](https://github.com/uibcdf/molsysmt/issues/255#issuecomment-6596125577).
The migration itself is merged on provider main at 00abb958 and #255 is closed;
reported runtime/test equivalence to executed de7ffad does not resolve this gap. Keep
these assertions and preserve original source/artifact evidence. No consumer
normalizer or xfail is introduced; no red source pair is integrated into main.
Source, installed/public and platform acceptance remain separate. #69 stays partial.

## What

Prepare the consumer transition under MolSysMT #255 and MolSysSuite #155 without
changing molecular ownership, scientific definitions or qualified dependency
routes. The provider's accepted pre-1.0 plan at 4e9bf09 is an advance notice;
the actual tested provider has no lowercase `chemical_states` module yet.

## How

The [receiving contract](../chemical_domain_receiving.md) inventories direct and
indirect callers and links existing scientific guards. One direct SMARTS call
must eventually move from `msm.topology` to `msm.chemical_states`; no client runtime
is edited before implementation receiving. Explicit state selection, prepared
maps, independent copies and persisted chemical/interaction evidence need actual
receiving, beyond namespace spelling.

## What is measured and what remains pending

The [separate receipt](../evidence/chemical_domain_readiness_20261029_summary.json)
records a bounded 288-file AST inventory and **22 passed / zero skipped** existing
tests on clean consumer 87de52f and clean editable provider 71fbe4f. Source/native/
test identities agree before and after. Five existing b_factor-drop warnings
and failed shared-environment pip check remain disclosed. Provider 4e9bf09 is
three commits ahead with the same tracked package tree; no sibling is pulled.

The [native CI receipt](../evidence/ci_methods_receiving_20261029.json) confirms
eight actual successful scientific cells on 87de52f using source pin 8ae160fc.
These are distinct baseline contexts. Neither qualifies the target cutover or
a new installed/public artifact. Runtime, fixtures, pins and scientific assertions
are unchanged; the reporting catalog registers this new issue. No new runtime
fallback, target test skip or weakened control is
introduced to claim compatibility.

## Scope and acceptance

Keep #69 partial until an identified provider implementation is received through
public APIs and the contract's state/absence/component/axis/copy/persistence
gates pass. Provider target guards and consumer reruns must retain profiles,
units, scientific failures, sparse/evaluated-empty evidence and producer history.
Then qualify source CI and installed/public bytes separately. No speculative
minimum, release or addon work follows from this advance notice.

Owners LMMV/dprada. Preserve the owned raw root recorded in the contract for
review on 2026-11-12. Original-method access under #66 remains separate; no new
activity or score is acquired by this preparation.
