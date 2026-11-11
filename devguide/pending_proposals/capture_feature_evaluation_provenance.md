---
summary: Retain executed feature-request and evaluation provenance in native results.
issue: uibcdf/pharmacophoremt#196
status: open
opened: 2026-11-11
closed:
verification: asserted
area: [api, modeling, persistence]
guard:
normative: devguide/native_feature_payload.md
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
