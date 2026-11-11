---
summary: Define the minimal feature-asset API and qualify argument/diagnostic admission.
issue: uibcdf/pharmacophoremt#188
status: resolved
opened: 2026-11-11
closed: 2026-11-11
verification: measured
guard: tests/test_feature_asset_admission.py
normative: devguide/feature_asset_public_api.md
area: [screening, interoperability, api]
blocked_by: []
supersedes: []
---

# Minimal public feature-asset API design

Use the existing cold result reader and prepared-run patterns to define the
minimal feature-asset surface, selection/generation policy and staged delivery.
Qualify real ArgDigest/SMonitor admission and diagnostics in an unshipped study,
then compose admitted requests with the unchanged #187 workflow. No public
namespace, stable format, production scale or molecular collection is introduced.
Keep original science/evidence and separate provider/public/human gates intact.

## Resolution — 2026-11-11 UTC

The [minimal API proposal](../feature_asset_public_api.md) and
[receipt/archive](../evidence/feature_asset_api_20261111.json) receive namespace/
signatures, generation/selection/page meaning, source ownership, staged format/
writer/native-delivery gates and registered admission/diagnostic boundaries.
A16-file source audit explains the cold-reader choice without creating it.

The unshipped admission study passes76controls per source/exact-owned218 context:
44argument/provider controls and32unchanged workflow regressions. Real ArgDigest
logical owners preserve caller-dependent None, literal keys, finite selections,
integer pages and native/provider TypeError semantics. Six real catalog error
categories emit through SMonitor in two cold receivers with125public support
payloads verified, application policy unchanged and no rejected marker captured.
Actual Ackredit sessions compose admitted nm/pm reuse of the three original
positions1/6/10, retain native maps/producers and create no new credit. Matching,
feature generation and molecular operations remain zero.

The initial69passes/four failures retain two incorrect control assumptions:
all call-shape TypeErrors need not inherit DigestError, and a decorator's internal
skip mechanism is forwarded to the underlying callable rather than removed.
The corrected controls preserve native exceptions and keep proposed public
signatures closed; neither provider, admission implementation nor runtime changed.
Original inputs/results remain intact.

This resolves the design/admission increment only. No proposed public namespace,
public format/writer, installation promise, scale claim or new supported artifact
is introduced. Next implement/qualify the read-only view under its own format/
profile contract. Native reconstruction, writer/recovery, human and full delivery
gates remain separate; MolSysMT#624 unreceived, QuantityRecord provisional and
#148/#165 stopped.
