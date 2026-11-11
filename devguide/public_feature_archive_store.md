# Public feature-archive store: first bounded writer slice

Owners LMMV/dprada; PHMT#194; 2026-11-11 UTC. This contract selects the first
implementation slice. Implementation and exact receiving remain separate evidence.

## Selected scope and existing owners

Preserve and publish **whole existing public feature-archive generations**.
Retain every literal work/source/occurrence key, global ordinal, extraction record,
original payload-format declaration, byte sequence and producer reference. Do not
filter, renumber, extract molecules or rewrite quantities. The generation envelope
retains the existing public archive v1 schema; its new origin binds the copied
source generation with policy `explicit-original-generation-copy@1`.

The archive reader/schema and finite-JSON tool are already production-owned.
Reuse `_storage` read/layout checks, `_schema` validation and the scientific
#193 decoder; do not import `phmt_test_support`. The #186/#187 studies supply
algorithmic/interruption evidence, not runtime classes. Saved-run SQLite tables
represent different outcomes and are not reused as feature storage. MolSysMT#624
continues to own molecular collections, preparation and source mappings.

Creating new native payloads from live native inventories, arbitrary record
assembly and selected-subset export require subsequent API/format decisions.
This first whole-generation operation cannot silently change original ordinals.
It is useful for retaining an acquired generation and safely publishing a newer
one in an application-owned archive. It is not the complete #194 writer scope.

## Public operations

| Operation | Contract |
| --- | --- |
| `FeatureAssetView.payload_info(ordinal)` | Cold, detached generation/ordinal/hash/format/actual original-byte-count metadata; no quantity or payload interpretation. |
| `FeatureAssetStore.create(path, *, payload_profile)` | Explicitly create a new writer-owned archive; refuse an existing path. The admitted profile is exactly `snapshot-study-v1`. Never adopt or mutate a reader-only archive implicitly. |
| `FeatureAssetStore.open(path)` | Open only an existing supported writer-owned archive, acquiring one cooperating exclusive lease. Metadata opening does no scientific decoding. |
| `store.current()` | Current published SHA-256 or None before first publication. |
| `store.view(*, generation=None)` | Detached ordinary public view under the writer lease. None resolves current once; an explicit generation inspects an un/published candidate. Closing the writer does not close a detached view. |
| `store.stage(view, *, expected_generation)` | Borrow a public view, recheck its identity and copy the entire manifest/originals. Validate all ready payloads through the #193 quantity/native-domain owner before installing an immutable candidate. Incomplete rows retain original causes; staging does not publish. |
| `store.publish(generation, *, expected_current, retry_of=None)` | Revalidate the complete candidate afresh under the current unit policy, then compare and replace CURRENT. None explicitly means first publication. Incomplete candidates refuse. No cached validation passport or automatic retry. |
| `store.attempts()` | Bounded, validated detached started/terminal receipt history; missing terminal means unknown, not failed or completed. |
| `store.inspect_recovery(attempt)` | Inspect one retained publication and actual current visibility. Return an actionable decision, without native candidate validation or any write/retry. |
| `store.retry_publication(attempt)` | Link an eligible retained unknown/raised publication and call the same public publication validator. Already current/completed/displaced/unknown identities refuse. Earlier receipts stay original. |
| `store.close()` / context manager | Idempotent owned close, releasing only this lease. Later operations refuse; handles are process-bound. Calls within one owner process serialize. |

The writer export is lazy: importing the metadata reader does not load the writer,
fcntl or scientific modules. Requesting a writer class still imports no science;
only ready-payload staging/publication activates scientific quantity validation.
ArgDigest owns definition/value admission; SMonitor owns categorical diagnostics
and capture. Applications own policies, handlers and attribution sessions.

## Physical profile, finite bounds and mutation

Use existing trusted local POSIX directories, no-follow/nonblocking bounded regular
files, same-directory staging, exclusive immutable installation and atomic CURRENT
replacement. Readers need no writer lease. A distinct `WRITER.json` descriptor,
`.lock` and `attempts/` identify writer-owned archives without changing STORE.json
or breaking ordinary public readers. Check the supported profile before mutation.
Keep interrupted initialization/staging files for inspection; never delete an
existing archive, take over another writer or silently repair incompatible files.

The first profile fixes 64 records/candidate, 8 MiB repeated-original input,
the reader's 4 MiB unique original/8 MiB generation bounds, and 64 operation
attempts/store. No unlimited override is exposed. Refuse larger sources before
pulling payloads. Quota exhaustion preserves readable evidence and calls for a
new explicitly linked store, not automatic history deletion. This is not a scale
or throughput claim. Source views are detached/pinned; the caller owns closure.

Only stage/publish create attempt receipts, with a bounded ordinal and UUID,
operation, relevant generation identities and optional retry link. Persist the
started receipt before operation effects. Terminal completed/raised facts use safe
category/type fields; never stringify exceptions or attach raw payload/path/key
values automatically. Preserve native exceptions as causes. A missing terminal
or a caller exception after CURRENT replacement does not imply rollback.

Each attempt separately observes the installed distribution version and the
writer module's source-file SHA-256; unavailable observations stay None. These
observations neither authenticate running source nor replace original extraction
producer metadata. Later writers preserve earlier attempt observations unchanged.

Recovery inspection reports current visibility independently of receipt outcome.
It distinguishes already current, retry available, completed/displaced and unknown
attempts. A retry must name an actual retained publication, match its candidate
and expected-current identities, and validate again before replacement. It never
rewrites an older unknown/raised receipt into success.

No process crash, application exception or refused candidate should replace a
previous confirmed generation. A killed cooperating writer releases its lease;
old detached readers remain pinned. The profile claims neither power-loss/fsync
durability, hostile-directory safety nor network/distributed filesystem atomicity.

## Acceptance and next slices

The [first-slice receipt](evidence/feature_archive_writer_20261111.json) receives
source aad1de5 and its exact owned wheel: 150 selected cases each, 228 verified
payloads/173 runtime bodies, actual public quantity lower-bound bytes, original
references, cold metadata/recovery and real before/after-publication termination.
Source/owned executable guides under nm/pm and strict full docs pass. #194 stays
partial for broader assembly at that first checkpoint. The later
[native-v2 contract](native_feature_archive.md) and
[312-case source/owned receipt](evidence/native_feature_archive_20261111.json)
complete bounded native record assembly/lineage through the same writer tools;
#194/#195 reports are archived. Historical v1 remains unchanged and unsupported
mixed/cross-profile conversion refuses. Full delivery/scale gates stay separate.

Guard explicit creation/opening, same-source immutability, complete original-byte/
metadata/provenance preservation, invalid quantities/maps, empty/incomplete
candidates, expected-current/lease/lifetime and malformed receipts. Exercise real
owned before/after-replacement SIGTERM/SIGKILL in fresh processes and linked recovery.
Repeat fresh quantity validation under nondefault unit policies; reading/copying
old attribution must add no extraction credit. Test cold metadata/recovery and
application-restricted actual diagnostics. Execute friendly and expert examples
through the same public operations, from source and one exact owned artifact.

Keep first failed attempts, limits and old receipt identities. Supported/full
hosted/public/platform gates remain #9/#10/#23/#192-owned. Public native payload
production, larger collections, performance/scale, biological and human receiving
remain later work; #148/#165 stay stopped. No tag or publication follows from
implementing this local writer slice.
