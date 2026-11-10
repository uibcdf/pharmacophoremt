# Immutable feature-manifest storage study

Owners LMMV/dprada; 2026-11-10 UTC;
[#186](https://github.com/uibcdf/pharmacophoremt/issues/186), implementing the first
bounded adapter under the [identity/lifetime contract](search_asset_identity_contract.md).
This is unshipped test support, not a supported API, production backend, molecular
collection or persisted lookup index. Scientific runtime/source and owned218
remain separately identified.

## Reused mechanisms and ownership

`phmt_test_support.feature_store` stores existing `FeatureSnapshotStudy` objects
as exact original bytes, using the public finite-JSON owner
`pharmacophoremt_results.canonical_json`. It introduces no quantity codec:
sealing/publication call the existing snapshot decoder, which performs public
PyUnitWizard QuantityRecord field/unit/dimension handshakes and geometry checks.
QuantityRecord remains provisional under its owner guide. Saved bytes retain
original maps, units, producer and attribution; hashes establish consistency,
not molecular origin or chemistry. MolSysMT#624 retains molecular collection,
preparation and lifetime ownership.

The shared-tool catalogue offers no feature-store adapter. Existing public
`ScreeningRunStore`/`ScreeningRunView` own run/outcome semantics and are not used
as private-table feature containers. The #183 application checkpoint is reused
by the opt-in receiving driver for progress/actual credit; it is not the store's
publication transaction.

## Finite physical profile

| Item | Declared behavior |
| --- | --- |
| Location | Caller-owned trusted local POSIX directory; no hostile-directory/race-proof security claim |
| Header | Canonical `STORE.json`, schema `pharmacophoremt.feature-store-study@1`, profile `local-posix-detached@1` |
| Bundle | Canonical JSON in `generations/<sha256>.json`; SHA-256 of its exact bytes is the generation identity |
| Manifest | At most12 ordered work/source/occurrence records; literal unique work keys, original parent bindings; repeated occurrences/payloads permitted |
| Payloads | Base64 exact canonical original F bytes, keyed by SHA-256; deduplicate payload bytes, never work positions or feature maps |
| Limits | 2 MiB originals summed over ready occurrences, 4 MiB encoded bundle, bounded text and fields; no streaming/scale claim |
| Incomplete entries | `failed`, `partial`, `unsupported`, `unattempted`, with explicit cause type/reason and no fabricated empty F |
| Publication | Separate canonical `CURRENT` pointer naming one generation and exact byte count; publish requires all records ready, with explicit expected-current comparison |
| Empty | An explicitly empty complete manifest is publishable; evaluated-empty families remain separate from unobserved families |
| Attempts | At most64 operations/128 bounded create-only canonical started/terminal receipts; retain attempts and generations, no automatic GC |
| Recovery | Reader/open never creates a store; create refuses any existing directory, even empty; partial initialization is retained for inspection and refuses normal open |

Generation identity includes manifest order/bindings and original payload
encodings, including original producer declarations. It excludes path, publication
alias and operational attempt UUIDs. Relocation preserves identity. This profile
stores no query, predicate qualification, postings or run resume state.

## Publication, interruption and close

A writer holds one nonblocking exclusive `fcntl.flock` on a fixed regular `.lock`
file. It refuses a second cooperating writer; readers take no lease. Open paths
use no-follow/nonblocking descriptors and require bounded regular files; store
subdirectories must be real directories. These are bounded local checks, not
protection against an adversary changing directory ancestors or bypassing the
cooperating-writer protocol.

A complete temporary file is installed by same-directory exclusive `os.link`;
an existing generation must match every original byte and is never overwritten.
Publication validates the candidate and quantities again, checks expected-current
again, then replaces `CURRENT` with `os.replace`. The
[Python OS documentation](https://docs.python.org/3.14/library/os.html#os.replace)
and [flock documentation](https://docs.python.org/3.14/library/fcntl.html#fcntl.flock)
describe these POSIX mechanisms; this study qualifies only the local context.
No fsync/power-loss, network filesystem, distributed visibility, multithreaded
shared-handle or noncooperating multiwriter guarantee follows.

Before the replacement boundary, failure/interruption leaves old CURRENT
untouched. After replacement, a killed process or exception may prevent a return
or completion receipt even though the new generation is published. Recovery
verifies CURRENT and its complete referenced bundle; a raised/unknown operation
never implies rollback. A started receipt without a terminal remains unknown.
Explicit retries link a retained attempt and revalidate; no exactly-once claim.
A terminal-receipt write failure can itself raise after publication. Failure to
retain an error receipt adds a note without replacing the original exception.
Orphan staging files remain nonauthoritative; there is no automatic cleanup of
crash remnants, old generations or failed attempts. The finite operation bound
requires a new study location when exhausted, retaining this evidence.

Readers copy and verify one entire bounded generation at open. They remain pinned
across publication, writer close and relocation. Metadata open validates canonical
structure, hashes, maps and original F envelopes, with scientific imports absent;
it does not interpret quantities or admit a scientific query. Every `inventory()`
call reconstructs quantities through the public handshake afresh. Closing drops
owned bytes; it is idempotent, subsequent operations and pending iteration refuse,
and already returned caller-owned inventories remain detached. Incomplete sealed
generations can be explicitly inspected but cannot replace CURRENT. Corrupt
attempt history refuses history/writing while an independently valid published
bundle remains readable.

## Receiving and limits

The [receipt and original archive](evidence/feature_store_20261110.json) retain
prospective contexts, original controls and outcomes. The focused guard is
`tests/test_feature_store.py`; the opt-in `devtools/qualify_feature_store.py` creates
one fresh store, closes/reopens it and feeds the exact restored work entries into
the unchanged six-family retrieval controls under both unit policies. The driver
reserves a new output, preserves checkpoints and actual attribution, and requires
an explicitly admitted/limited environment. It performs no molecular operations
or feature extraction. Native candidate-band versus rational-pair results retain
their distinct original meanings; captured-inventory scope is unchanged.

Received53controls per source/exact-owned218 context include four owned-child
termination cases (before/after replacement, SIGTERM/SIGKILL), local/separate-
process writer refusal, corruption and partial-install/failed-refresh controls.
Each cold reader verifies11original occurrences/10unique payloads with scientific
imports blocked and125public support payloads checked. Each reopened corpus
reproduces all72 prior#182 analytical rows exactly, including198strict comparisons,
66boundary observations and six original native/rational differences. Reading
under real Ackredit and PHMT attribution creates no new credit; new native
retrieval calls retain their actual original session attribution separately.

Each eleven-occurrence bundle occupies202213bytes in this profile, versus166473
original bytes by occurrence and149646unique original bytes. This is an actual
feature-bundle encoding size, not total directory allocation, persisted-index
size, speed, scaling or crossover evidence. Two ordinary store operations retain
separate receipts and CURRENT; their size is not folded into an index claim.

The initial47-control pass retains46passes/one collision failure: the replacement
alias chosen in a test already existed. Changing it to a distinct literal fixed
the test; duplicate-key refusal remains guarded. A later frozen-provider check
refused a newly added sibling file; a detached copy of the305originally admitted
TopoMT Python bodies preserves the original4594-provider-file context. The first
roundtrip controller had a syntax error before scientific execution; its logs and
correction remain local. Final lint-only import cleanup is received by AST equality
(after removing an unused constant import), with final53controls repeated in both
contexts. Original science, pre-cleanup fixtures and run identities remain intact.

Local storage/lifetime receiving does not qualify full-source-family negatives,
source authenticity, public quantity promotion, installed delivery of this study,
a production default, index persistence/cost/crossover, general public-library
import, human usability or biological screening performance. Full exact-head and
public/platform/release gates remain #9/#23; #148/#165 remain stopped.

Next qualify guided/expert operations and admission/refusal messages against this
bounded lifecycle before proposing a public surface. Declare persisted lookup
identity/size/rebuild compatibility separately; never treat feature-bundle bytes
as index-size evidence. Provider collection acceptance remains independent.
