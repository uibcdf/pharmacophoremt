# Search-asset acceptance examples

Owners LMMV/dprada; #185; 2026-11-10 UTC. Follow the
[identity/coverage/lifetime contract](search_asset_identity_contract.md).
The table separates newly executed primitive controls, source-inspected existing
run behavior and required future storage-adapter probes. It is not a claim that
a persistent search-asset format or reader exists.

## Primitive controls received in this increment

| Scenario | Expected boundary |
| --- | --- |
| Copy the same original canonical bytes to a new path | Exact-byte and payload identity stay unchanged; this alone authenticates no origin. |
| Re-indent the current JSON envelope while keeping its payload | Current canonical format refuses it before old-manifest binding checks. A future representation migration needs a distinct explicit contract. |
| Replace an occurrence with another unit encoding of the same declared points | Explicit nm/pm reader conversion can agree within 1e-12 angstrom, while original encoded identity and old-manifest compatibility remain different. |
| Reorder original occurrences | New manifest/lookup identity; rebuilt postings retain original work keys with their new ordinals. |
| Rename an original work key | New manifest binding. This is not a presentation-only rename. |
| Reseal a synthetic claimed producer string | Structural consistency is not authenticated execution; the helper admits no query or match. Original captures remain unchanged. |
| Put a valid sealed time quantity in a center | Structural/family inspection stays distinct; the explicit length handshake refuses scientific reconstruction under nm and pm policies. |
| Empty capture evaluated aromatic rings only; require donor/charge families | Those families remain unobserved, with no zero count or match outcome substituted. |
| Empty capture evaluated aromatic rings; inspect that same family | Recorded count zero is known; the metadata helper still computes no query/match outcome. |
| A donor/charge capture is queried for aromatic/charge coverage | Existing charge counts remain known; aromatic evaluation remains missing. |
| Require all six families from a partial request | Preserve each unobserved family explicitly. |
| Reorder/duplicate required family names | Family-set semantics stay canonical; source keys `nm`/`1 nm`, feature multiplicity and matching indices keep their own semantics. |
| Supply invalid required names | Refuse before this helper inspects snapshot metadata. This is not a complete query-geometry preflight. |
| Modify a detached coverage report | Original bytes/request/counts remain unchanged. |
| Use a second supported query with the current study asset | Lookup identity can stay unchanged within its finite domain; no run resumption or full-source-family admission is inferred. |

The first execution had 22 passes/two failures because the initial test/draft
incorrectly allowed outer reformatting. The existing reader was correct: it
requires canonical envelope text. Original first-run evidence is retained and
the controls/draft were corrected without changing that reader. These primitive
controls contain no native matching, feature generation or molecular work.

## Existing public run primitives: inspected, not new asset implementations

| Scenario | Current owner/contract and limit |
| --- | --- |
| Inspect an old plan after runtime changes | `PreparedRunPlan.describe()` preserves original query/context metadata without reconstruction or current-runtime admission. Metadata can contain private caller data. |
| Resume with changed query, declared context or software | Existing prepared-run checks refuse incompatible binding before pulling inputs. Their runtime fingerprint is conservative, not complete molecular/native authentication. |
| Close a prepared run | Only the owned writer closes; caller-owned sources remain owned by the caller. Closed-run resumption refuses. |
| Open historical result evidence | `ScreeningRunView` verifies a read-only run snapshot; its writer must first be closed. It does not compute science or become a feature/index reader. |
| A terminal failure was committed | It stays unscored and authoritative in that run. Retrying uses the existing linked-run/attempt policy. |
| A research driver is interrupted | #183 retains its last committed progress/credit. This is not publication of a new feature/search generation. |

Source audit and previously received owning contracts support these statements;
their full historical scientific/reader suites are not rerun by this design
increment. Existing source/run/installed evidence retains its original identity.

## Required future adapter probes

| Scenario | Required observable acceptance |
| --- | --- |
| Create at an existing destination | Refuse before replacing existing published contents. |
| Open a missing asset | Refuse; opening never creates an empty replacement. |
| Candidate build stops before sealing | Old publication remains; candidate coverage/work stays partial/unknown. |
| Candidate seals but publication stops | Preserve sealed-unpublished versus published state through the selected visibility mechanism. |
| Refresh fails after useful old generation exists | Old publication/read binding remains intact; failed attempt and causes remain inspectable. |
| Refresh while a reader exists | Either pin the qualified old generation or explicitly refuse overlapping publication; never switch/mix generations silently. |
| Open/close/early-stop | Release owned resources predictably; caller resources remain owned, and post-close pulls refuse. |
| Original source changes behind the locator | Refuse stale source/manifest use. An alias/ETag or quantity canonicity token is insufficient. |
| Source is relocated or temporarily unavailable | Distinguish verified identical relocation, accessibility and scientific identity. Retain historical source provenance. |
| Some feature extractions failed/are unsupported | Preserve original denominators and causes; no manufactured native nonmatch or silently complete corpus. |
| Query requires unevaluated families | Follow explicit refusal, declared subset or new extraction policy. Ordinary source-level matching does not reinterpret missing evaluation as zero. |
| Lookup covers a strict subset or is interrupted | Preserve its actual coverage and pending/unknown work. Use an explicit qualified plan/fallback; no complete-recall claim. |
| Query exceeds the backend's feature/shape/constraint domain | Refuse or apply a recorded qualified alternative; no dropped scientific semantics. |
| Precision, definition or reference implementation changes | New binding/requalification or a separately qualified migration, despite a matching family/version label. |
| Required quantity kind/dimension/schema is incompatible | Refuse at the owned reader handshake before scientific use; preserve per-record failure identity. |
| Scientific library/citation provider is absent while reading metadata | Metadata-only inspection needs no scientific recalculation or new attribution; scientific reconstruction keeps its separate dependencies. |
| Persisted bibliography is read/exported | Retain original records/versions without registering old science again. |
| Physical format is migrated | Retain the original, explicit representation/derivation and checked correspondence; do not silently upgrade historical evidence. |
| Physical/native memory, process-cold, storage or scale costs are claimed | Execute those named gates on equivalent qualified workloads; #184's tiny in-memory timings do not establish them. |

Choose the first bounded physical adapter only after reviewing these requirements
against available public operations. MolSysMT#624 remains the molecular collection/
snapshot owner; no PHMT molecular fallback follows. Quantity records remain under
their owning provisional contract. Full source/public/platform/release gates are
separate, and #148/#165 remain stopped.
