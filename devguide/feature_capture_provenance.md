# Source-owned feature capture and evaluation provenance

Owners LMMV/dprada; PHMT#196; selected 2026-11-11 UTC toward 0.6.0.
This contract precedes implementation. Qualification and release remain separate.

## Compatibility decision and ownership

Add `modeler.capture_features` as composition around exactly one existing public
`modeler.get_features` execution. Keep `get_features`' signature, native result,
definition, ordering, quantity forms/units, recognition and attribution unchanged.
Do not insert new keys into the inventory: the native payload's existing strict
field set remains unchanged. Use a separate runtime capture envelope instead.

The new operation records the effective normalized requested families, not a
guess from present features or broader intermediate provider recognition. A
donor-only request remains donor-only even if its provider also recognizes
acceptors. Each requested family is completed with its actual returned count or
evaluated_empty with zero. Unrequested families remain absent. Exceptions propagate
without manufacturing an empty, failed or partially completed successful capture.

MolSysMT owns molecular access, selected local indices, frame/state and source
axes. Reuse public `get(..., n_atoms=True)` for bounded input admission and the
existing feature extractor for all chemistry/geometry; do not add a parser,
preparation routine or source authenticator. Optional Ackredit attribution comes
from the actual extraction, under the application's activation/session. Capture
and later serialization add no duplicate extraction credit.

## Public operations and finite profile

Later #6 follow-up (2026-11-11): the additive
[argument-control contract](feature_argument_controls.md) explicitly extends
`get_features` and `from_inventory` with keyword-only `skip_digestion=False`.
The signature-preservation statements below describe this original #196 slice;
the later change has separate receiving and does not alter captured inventory or
wire schemas. Its bypass retains native/profile validation.

`capture_features(molecular_system, *, selection="all", structure_index=0,
chemical_state="reference", features=CLASSICAL_FEATURES, skip_digestion=False)` has the existing
extractor's argument meanings. ArgDigest owns signature/value normalization.
Canonicalize the effective family set in extractor order; retain all seven
supported families, including included volume, when requested. Duplicate requests
mean one effective family, as in the extractor's existing set semantics.

The legacy extraction and serialization signatures do not expose ArgDigest's
explicit `skip_digestion` parameter. Their ordinary public digestion remains
active: do not unwrap decorators or invent another bypass. Adding that parameter
requires separate signature/closed-contract receiving under PHMT#6; this slice
preserves the existing public signatures.
The two new public operations expose the standard boolean `skip_digestion=False`
control, with strict boolean digestion; an internal literal True bypasses argument
digestion only. Capture/content/native checks are always performed.

The first capture profile admits 1–256 total source atoms, at most 64 feature
records and 2 MiB for the sealed inventory observation. Use existing bounded
finite-JSON provenance limits before detaching metadata. Refuse an oversized
source before extraction and oversized/malformed output without returning a
partial capture. These are admission bounds, not a process-memory or throughput
guarantee for arbitrary molecular/quantity backends. The caller keeps its prepared
source unchanged across provider calls; this is not an atomic molecular snapshot.

Return a new runtime dictionary with exactly `schema`, `inventory`, `evaluation`,
`producer`, `capture_sha256`. Schema is `pharmacophoremt.feature-capture@1`.
`inventory` remains an ordinary native result usable by existing modeling tools.
It contains live explicit-unit quantities; the envelope is not a new file format.
Use the supported payload writer to persist it, rather than raw JSON or pickle.

Evaluation metadata has its own `pharmacophoremt.feature-evaluation@1` schema,
completed status, actual get_features operation, definition, canonical families,
recounted coverage, total atom count, resolved selected indices, frame/state and
Cartesian no-imaging convention. Raw selection expressions are not reinterpreted
or serialized; effective resolved maps are retained. Observe extraction software
versions and the extractor file SHA separately at execution, preserving unknown
observations as None. They describe observed software, not authenticated running
source, a molecular identity or a new bibliographic calculation.

Bind inventory, evaluation and producer through canonical finite JSON of the
existing unit-preserving `detached`/public QuantityRecord representation. Store
its SHA as `capture_sha256`; no new quantity codec or bare-unit convention is
introduced. The binding detects accidental post-capture edits before encoding.
It is not a signature or execution/source authentication; a reconstructed caller
dictionary cannot prove that an extraction happened. Never use a mutable success
flag or digest as a scientific validation passport.

## Native payload/archive composition

`FeatureInventoryPayload.from_capture(capture, *, parent, payload_profile, skip_digestion=False)`
requires the existing explicit `native-classical-v1` profile. Recheck envelope,
coverage, selected/frame/state identities, bounded original content and digest;
validate every native quantity/map afresh. Require the declared parent's total
atom count to match the capture observation. Parent source/occurrence/artifact/
preparation declarations retain their existing meaning and are not authenticated.

Delegate to the existing public `from_inventory` serializer, using the observed
family request and original capture producer/evaluation evidence as detached
`extraction_producer` provenance. Keep inventory recognition/attribution intact
and keep later serialization observations separate. No new outer payload keys,
archive schemas, format autodetection or implicit migration are introduced.
Original payload/archive bytes remain original.

Included-volume captures remain complete and usable as native inventories, but
the existing classical payload profile refuses any included-volume evaluation,
including evaluated-empty. Never silently filter that family or relabel it as
unobserved. An unsupported larger inventory still uses the existing get_features
route or a separately chosen later profile. Historical inventories keep the
explicit from_inventory(evaluated_families, extraction_producer) path; no capture
receipt is fabricated for them.

Public metadata readers remain scientifically cold. Only explicit capture/native
encoding activates scientific tools; application unit/capture policies stay
authoritative. Add categorical E339 for capture/evaluation/content disagreement;
reuse existing argument, unsupported-profile, native-quantity and budget categories.
Do not stringify native failures or attach raw scientific inputs to diagnostics.

## Receiving and next work

Receive actual extraction on small prepared analytical sources for default,
explicit/subset/duplicate/evaluated-empty/included-volume requests, one-call
execution, source immutability, nondefault units and native geometry/map equality.
Observe genuine provider failures and oversized admission without successful
capture, mutation/content/request/parent mismatches, original software/reference
retention and no-new-credit serialization. Exercise real optional attribution,
absence/failure and enclosing application captures through its owning tools.

Receive the source and an exact owned artifact with the actual public quantity
floor, all earlier native payload/archive guards, executable friendly/expert
examples and strict docs. Preserve every first failure and exact context. Source
evaluation provenance does not complete MolSysMT#624 collections/authentication,
full hosted/public/platform (#9/#192/#10/#23), biological/human/scale or stopped
#148/#165 work. No new tag or public package is selected here.

## Received bounded implementation — 2026-11-11 UTC

Source f722b45 and the exact isolated development wheel are
[received](evidence/feature_capture_20261111.json): 394 selected cases each,
238 verified payloads/183 source-equal runtime bodies, actual public quantity
floor and all 175 loaded PHMT modules from the target. All twelve guide-block
executions and strict full docs pass across source/owned and nm/pm. Original
failed attempts and resource limits stay retained. #196's bounded scope is
resolved; the full supported/public, molecular, human/biological/scale and stopped
workstream limits above remain authoritative. See the [0.6.0 scope review](release_0_6_0_scope_review.md)
for the next candidate-preparation action.
