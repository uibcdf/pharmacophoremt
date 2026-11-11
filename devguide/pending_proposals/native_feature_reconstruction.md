---
summary: Qualify explicit native reconstruction from saved feature archives for 0.6.0.
issue: uibcdf/pharmacophoremt#193
status: open
opened: 2026-11-11
closed:
verification: asserted
area: [api, persistence, screening]
guard:
normative: devguide/feature_asset_public_api.md
blocked_by: []
supersedes: []
---

# Native feature reconstruction

The [0.5.0 cut](../release_0_5_0_source_cut.md) delivers read-only archive metadata
and exact opaque originals. The next 0.6.0 slice follows the staged
[#188 API proposal](../feature_asset_public_api.md) without silently making study
classes or codecs a supported public format.

First decide and document accepted original payload formats/profiles: an explicit
compatibility decoder or a separately versioned public native payload. Runtime
must not import phmt_test_support, rewrite historical captures or infer admission
from producer-declared metadata. Require the expected generation; borrow the
caller's view; preserve literal keys, global ordinals, complete inventories,
maps and original attribution. Incomplete extraction and missing family
evaluation must remain distinguishable from evaluated-empty inventories.

Reconstruct quantities afresh through public PyUnitWizard, validating field,
unit/dimension and native geometry/map constraints under nondefault policies.
Establish the actual published provider/version boundary; QuantityRecord remains
provisional. ArgDigest owns argument constraints, SMonitor diagnostic categories
and application capture, and Ackredit attribution. Reading original features
must not create extraction credit. Source authentication, query/index admission
and MolSysMT#624 molecular collections stay independently owned.

Acceptance requires the reviewed format/admission/lifetime contract, real source
and exact-owned controls, unsupported/corrupt quantity and literal/empty/partial
selection cases, actual restrictive diagnostics and original-reference/no-new-
credit receiving. Metadata reading must remain scientifically cold. Receive a
guided/expert example using the same public operations. No decoder, stable format
or schedule is claimed here. Public writing/recovery, biological, human and
scale qualification remain later work; #148/#165 remain stopped.
