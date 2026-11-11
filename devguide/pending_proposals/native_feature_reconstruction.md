---
summary: Qualify explicit native reconstruction from saved feature archives for 0.6.0.
issue: uibcdf/pharmacophoremt#193
status: active
opened: 2026-11-11
closed:
verification: asserted
area: [api, persistence, screening]
guard:
normative: devguide/native_feature_reconstruction.md
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

## Selected implementation — 2026-11-11 UTC

The [native reconstruction contract](../native_feature_reconstruction.md) selects
explicit `payload_profile="snapshot-study-v1"` compatibility with original bytes,
not a new writer or automatic promotion of study APIs. The public scientific
operation uses fresh PyUnitWizard handshakes and the existing native geometry
owner. Selected metadata/content bindings, global ordinals, extra features,
empty/partial states and original provenance remain explicit. A bounded batch
admits at most 64 occurrences/8 MiB of repeated-original input bytes.

The verified original public PyUnitWizard 0.28.1 archive provides the qualified
capability floor; source pins and the shared environment remain unchanged.
First receiving passes 109 reader/native controls with that actual public payload.
Two earlier new-test assumptions were corrected: the expected projection needed
detachment before mutation, and the real quantity integrity field is `digest`.
Neither first failure was a runtime decoder defect. Later guards and exact-owned
receiving remain pending until their final receipts are attached.
