# Native feature archive v2 and explicit record assembly

Owners LMMV/dprada; PHMT#194/#195; selected 2026-11-11 UTC toward 0.6.0.
This contract was selected before implementation. Receiving below records the
executed scope; no release is selected.

## Scope and compatibility

Add native-only archive v2 through the existing public reader/writer. Explicit
`FeatureAssetStore.create(..., payload_profile="native-classical-v1")` selects
this format; `snapshot-study-v1` still creates the unchanged historical v1.
Store and generation schemas use `pharmacophoremt.feature-archive@2` and
`pharmacophoremt.feature-archive-generation@2`, with profile
`declared-native-classical-inventory@1`. Writer/attempt schemas also use @2.
Old consumers refuse these markers rather than interpret them as historical v1.
New readers recognize both supported versions without migrating or changing bytes.

Native v2 accepts the [public standalone payload](native_feature_payload.md)
only. Cross-profile whole copying and borrowed record construction refuse;
mixed historical/native archives and automatic conversion are not implemented.
A caller can explicitly reconstruct old features and encode a new native payload,
retaining the original evidence separately. That operation does not invent an
enclosing archive record/ordinal binding for the newly encoded standalone object.

Reuse the [existing POSIX writer contract](public_feature_archive_store.md),
bounded regular-file checks, immutable candidate
installation, expected-current replacement, detached readers, retained attempt
history and explicit linked recovery. No second storage/quantity/recovery engine
or study runtime class is introduced. Molecular source/collection authority
remains MolSysMT#624; this is feature evidence, not a molecular collection.

## Public record operations

`FeatureAssetRecord` owns an immutable metadata encoding and optional original
payload bytes, no handles or source views. Its factories and metadata methods
remain scientifically cold; scientific admission happens at staging, publication
and explicit reuse through the same public payload/native validator.

| Operation | Meaning |
| --- | --- |
| `FeatureAssetRecord.from_payload(work_key, payload)` | Explicitly assign a new literal work key to a native `FeatureInventoryPayload`. Source/occurrence keys come from its declared parent. Preserve every original byte, extraction producer and serialization observation. No archive ancestor is claimed. |
| `FeatureAssetRecord.from_view(view, ordinal, *, expected_generation)` | Borrow one native-v2 record at its global ordinal. Recheck pinned identity, copy exact metadata/original bytes and append an origin anchor. Preserve any earlier anchors. The caller owns closing the view. |
| `FeatureAssetRecord.incomplete(work_key, source_key, occurrence_key, *, status, cause)` | Retain explicit failed/partial/unsupported/unattempted evidence with finite `type`/`reason`; never turn it into an empty successful payload. No native inventory is manufactured. |
| `record.describe()` | Fresh detached record metadata, including coverage and retained origin anchors. There is no destination ordinal yet. |
| `record.payload_bytes()` | Return original bytes for ready evidence or None for incomplete evidence. No quantity decoding or new extraction credit. |

Literal keys retain case, spaces and Unicode, with 512-byte limits. Repeated
source/occurrence identity is permitted under different work keys; it represents
repeated evidence, not distinct molecules or independent support. Duplicate work
keys within a generation refuse. Public record factories never rename a borrowed
work/source/occurrence key. A fresh from-payload assignment is explicitly new work.

## Staging and ordinal authority

`store.stage_records(records, *, ordinal_policy="preserve-original@1")` accepts
an explicit list/tuple of at most 64 public records, not an unbounded iterable.
Their sequence defines destination global ordinals 0..N-1. Every record and
payload is structurally checked again, all ready quantities/native geometry are
validated afresh, then an immutable candidate is installed without publication.
Incomplete candidates remain inspectable and cannot replace confirmed evidence.
The empty sequence is an explicit empty generation, not a scientific negative.

Default `preserve-original@1` refuses a borrowed record whose most recent source
ordinal differs from its proposed destination. Newly assigned records have no
earlier archive ordinal and can occupy new positions. Reordering or compacting a
subset requires explicit `ordinal_policy="explicit-rebase@1"`; the generation
records that decision and every old position remains in the record's lineage.
No selection silently overwrites an original ordinal.

Each ready row has work/source/occurrence keys, status, payload SHA, extraction
metadata and lineage; incomplete rows have the same common keys/lineage and a
cause instead of a payload/extraction. A ready extraction is exactly the native
payload's detached `describe()` metadata, including original producer and separate
serialization observations. Bind it to the actual original bytes at every read;
never treat a mutable dictionary or previous validation flag as admission.

An origin anchor contains source generation SHA, source global ordinal, original
work/source/occurrence keys and SHA of the complete source row (excluding the
public view's added `work_ordinal`). Preserve all existing anchors and append the
immediate source anchor. At most 16 anchors/record are admitted; no history is
silently trimmed. Anchors bind declared content identities without authenticating
a molecule or guaranteeing that an external source archive remains available.

Assembly origin records exactly policy `explicit-native-record-assembly@1` and
the selected ordinal policy. Existing `stage(view, expected_generation=...)`
copies an entire generation only within the same archive profile. Its origin
keeps `explicit-original-generation-copy@1` and source identity; rows, lineages,
global positions and payloads stay unchanged. This distinct whole-copy operation
cannot be used to smuggle an implicit profile conversion or subset renumbering.

## Cold reading and explicit native reuse

`FeatureAssetView` reports the actual stored schema/profile and retains its
ordinary detached/pinned lifetime, pagination, original bytes and global ordinals.
Native-v2 reading structurally binds native payload metadata, coverage, maps and
provenance through the public payload parser; it does not decode quantity records
or activate the scientific stack. Report this as `native-layout-only` payload
interpretation with `quantity_semantics_checked=False`. Historical v1 remains
opaque with its original flags. Metadata structure checks are not scientific
validation, source authentication, query admission or binding prediction.

`screening.reuse_feature_inventories(..., payload_profile="native-classical-v1")`
explicitly selects native v2, checks generation/selected completion/evaluation,
reconstructs all original fields through `FeatureInventoryPayload.to_inventory`,
and retains work/source keys, destination ordinal, extraction and original lineage.
Historical profile selection still admits v1 only. Do not choose a decoder from
an arbitrary format label or silently fall back between profiles.

## Resource, receipt and diagnostic contracts

Keep 64 records, 8 MiB repeated original input, 4 MiB unique payloads, 8 MiB
generation bytes and 64 attempts/store; individual native payload bounds remain
unchanged. Check list/count/repeated/unique budgets before scientific decoding
and installation. Generation identities include full row/lineage/order/policy.
Whole-copy and record assembly use the same immutable installation boundary.

Version2 attempt receipts distinguish `stage`, `stage_records` and `publish`.
Record-assembly starts bind candidate SHA, count and ordinal policy before
scientific validation or candidate installation. Terminal result must match that
candidate. Preserve unknown/raised attempts; do not infer rollback from missing
terminal or errors after replacement. Retry still applies only to actual retained
publication attempts and runs the same fresh validator. Old @1 receipts remain
unchanged and readable only under their owning v1 writer descriptor.

ArgDigest owns closed record/stage arguments, DepDigest explicit scientific
availability, SMonitor categorical diagnostics and application capture, and
PyUnitWizard all quantities. Add E335 invalid record/lineage, E336 archive/profile
mismatch, E337 missing rebase consent and E338 lineage budget. Retain native
causes without formatting private payloads. Original attribution survives without
new extraction/software-method credit; no new dependency floor or source pin.

## Receiving and further work

Source `c900da477090c260bf8d4b408697cd89f7039dfc` and its exact owned wheel
receive [312 selected cases each](evidence/native_feature_archive_20261111.json):
67 native archive/lineage and 245 earlier payload/writer/reader/native controls.
All 235 wheel payloads/180 runtime bodies verify; 171 loaded PHMT modules originate
in the installed target. Actual public PyUnitWizard 0.28.1 bytes, twelve native
guide-block executions plus eight prerequisite blocks across source/owned and
nm/pm, and strict full docs pass. Four native and four earlier v1 real publication
interruption cases preserve their original identities and linked recovery.

The initial 295-pass/four-failure run used a v1 CURRENT pointer in native-v2
corruption fixtures; the explicit fixture schema correction keeps every E335
assertion. The corrected 311-case run and final 312-case public-page ordinal guard
remain separate originals. Ten initial quality checks include 161 administrative
controls; seven current-source checks refresh the final guard/reporting scope.
Resources remain serial CPU19/thread1, low priority and monitored/bounded, without
reservation or aggregate cgroup enforcement. This receives the selected bounded
public profiles under #194/#195, not supported/public/platform or scale readiness.

[#196](pending_proposals/capture_feature_evaluation_provenance.md) owns the next
source-owned effective evaluation provenance contract. Old captures keep their
explicit declaration route; no historical evidence is reclassified automatically.

Receive source and one exact owned artifact with actual public PyUnitWizard
0.28.1, original native inventories, nm/pm, evaluated-empty/unobserved/incomplete
states, exact-byte/metadata and multi-step lineage equality, default-preservation
refusal/explicit rebasing, detached lifetime and genuine no-new-credit references.
Receive malformed/resealed metadata, wrong quantities/maps, budgets, stale
publication, unknown receipts and real native-v2 before/after-replacement
SIGTERM/SIGKILL with linked recovery. Keep earlier v1/payload controls and every
first failure; receive fresh cold readers/recovery and application unit/capture
policy. Execute friendly/expert guide blocks and strict docs from both contexts.

Mixed-format migration, molecular collections/authentication, performance/scale,
biological and representative human evidence remain separate. Full supported
hosted/platform/public receiving stays #9/#192/#10/#23-owned; #148/#165 stay
stopped. Preserve immutable 0.5.0 and publish no new tag or package here.
