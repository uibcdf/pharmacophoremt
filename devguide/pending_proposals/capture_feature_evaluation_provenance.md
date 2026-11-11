---
summary: Retain executed feature-request and evaluation provenance in native results.
issue: uibcdf/pharmacophoremt#196
status: partial
opened: 2026-11-11
closed:
verification: measured
area: [api, modeling, persistence]
guard: tests/test_feature_capture.py
normative: devguide/feature_capture_provenance.md
blocked_by: []
supersedes: []
---

# Source-owned feature evaluation provenance

After the native payload/archive work under #194/#195, reduce repeated caller
declarations without fabricating provenance for historical captures. Current
`modeler.get_features` returns native geometry, selected local atom indices,
frame/state, recognition and optional attribution, but not a source-owned
effective requested-family/evaluation receipt. Feature presence cannot establish
evaluated-empty coverage. The explicit caller declaration used by the current
native payload remains the honest compatibility route for old inventories.

Choose the public extraction/capture result and compatibility contract before
changing runtime types/fields. Capture the effective request and completed or
evaluated-empty coverage at the PHMT branch that actually executes, preserve
failures and unsupported/included-volume distinctions, and retain all native
geometry/maps/units/order and original producer/attribution versions. A request
receipt is executed-software provenance, not molecular authentication or a
mutable validation passport. Do not rewrite historical payloads or infer old
coverage merely from present features.

Compose with the supported native payload/archive tools and provide a concise
recipe plus complete expert operations. MolSysMT#624 keeps selection/frame/state/
source/collection authority; Ackredit keeps optional original credit and application
session ownership. No sibling implementation, new quantity codec, dependency pin,
release or benchmark is selected by this proposal.

Acceptance requires the reviewed public/compatibility contract, actual extraction
for default/subset/evaluated-empty requests and failed/unsupported boundaries,
preserved nondefault unit policy/native maps and original/no-new-credit references,
source/exact-owned examples and retained historical payload/archive controls.
Full hosted/platform/public, biological/human/scale and stopped #148/#165 remain
independent. Next review existing extraction/inventory callers and choose how to
add source-owned evaluation provenance without silently changing persisted v1/v2.

## Selected additive implementation — 2026-11-11 UTC

The [capture contract](../feature_capture_provenance.md) precedes the additive
implementation. Existing get_features/native inventory and persisted schemas
remain original. Capture records effective requested families and completed/empty
counts around one actual extraction; from_capture revalidates native content,
compares the original binding and delegates to the existing serializer. Bounds
and included-volume refusal are explicit. Source/owned receiving is in progress;
no complete release/delivery or molecular authentication claim is selected.

Source receiving passes 394 selected cases in three serial processes (312 prior,
54 capture/provider, 28 attribution), six nm/pm recipe block executions, strict
full docs and ten quality checks including 161 administrative controls. Genuine
optional absence, poisoned provider errors and original no-new-credit archive
round trips pass. Initial incorrect fixture/policy assumptions, the unsupported
legacy bypass experiment, bounded-memory aborts and controller/import corrections
remain original evidence. Exact-owned receiving and durable evidence closeout
are the next action; broader gates remain independent.
