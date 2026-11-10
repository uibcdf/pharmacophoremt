# Prepared-feature snapshots and retrieval compatibility

Design contract revision 1; owners LMMV/dprada; 2026-11-10 UTC;
[#179](https://github.com/uibcdf/pharmacophoremt/issues/179), following
[#178](retrieval_candidate_controls.md). This is the acceptance contract for the
next capture/preflight implementation. It introduces no public Python name,
persisted schema, automatic compatibility detector or production index.
Existing raw inventories, native persistence, prepared-run plans and historical
reading retain their current contracts.

## Current supported boundary and observed gaps

`modeler.get_features()` produces a native inventory with definition, ordered
features, recognition evidence, selected atom indices, frame and chemical state.
Each feature retains its kind, chemical participants, geometry participants,
center, direction/normal and charge. Existing consumers validate their supported
geometry and use original feature-list indices. Raw inventory reuse requires the
caller to supply the same unchanged molecular source, frame, state, selection
and requested families. Axis/shape admission does not authenticate that source.

The inventory does not explicitly capture the prepared parent, source occurrence,
requested families, completed request coverage or complete producer binding.
Observed feature kinds cannot recover a request whose result was empty. Provider
recognition metadata is evidence, not a substitute for a declared extraction
request or a public inventory persistence contract. No historical inventory is
silently promoted to a verified snapshot.

`PreparedRunPlan` already has six producer compatibility declarations and a
conservative runtime binding. Its provider version labels are not complete
source/native closure. The #177 correction also demonstrates why the unchanged
method family name `rigid_association_cliques@1` cannot identify its exact
numerical implementation. The [source audit](evidence/feature_snapshot_contract_20261110.json)
records inspected fields and original source identities, rather than executing
those scientific studies again.

## Required layers and ownership

These are semantic requirements, not proposed serialized field spellings.

| Layer | Required information | Owner and admission |
| --- | --- | --- |
| Prepared parent | Verified artifact/provider revision, preparation request and output identity, original source occurrence, molecule/state/conformer/frame and atom correspondence, supported lifetime/replay and coverage | MolSysMT; consume qualified public operations/receipts. A caller's opaque identifier alone proves none of these properties. |
| Extraction request | Supported feature definition, explicit effective requested families, resolved atom selection, one frame/state, Cartesian/PBC convention, actual perception/geometry routes and producer context | PHMT feature semantics; molecular recognition/geometry through MolSysMT. Preserve the request even when it yields no features. |
| Captured features | Complete ordered inventory with participant/geometry maps, explicit-unit centers, directions/normals, charge, original recognition evidence and actual attribution | PHMT. Detach data, preserve repeated/coincident feature occurrences and original indices; do not retain a mutable molecular handle as a snapshot. |
| Reference predicate | Method family and exact qualified implementation/runtime identity, numerical admission, supported feature/query domain, finite proposal/fitting/final-acceptance meanings | PHMT. Candidate generation, final fitting/matching and scoring are separate bindings. A version/name or file hash alone is not a complete dependency qualification. |
| Retrieval asset | Exact captured-feature manifest and ordered occurrence maps, representation/precision/bin/chirality settings, supported predicate/query domain, build coverage, qualification record and producer | PHMT. Every posting maps back to original occurrence/feature IDs. Partial build, failed build and an empty complete asset remain distinct. |
| Query and execution | Exact query, resolved constraints/tolerances, method/score/grouping, query/asset capability checks, budgets, failure/stop/resume policy and actual run identity | Existing PHMT plan/run owners. A reusable feature payload does not make an old run compatible with a new query. |

MolSysMT#624 owns reusable heterogeneous molecular collections and source/prepared
snapshots. A format-specific reader, an independent molecular copy or three
individually verified artifacts do not establish that collection contract. PHMT
must not implement a substitute molecular parser, state/conformer manager,
chemical equivalence test or source observer. A missing parent guarantee remains
an explicit provider acceptance item, not a fabricated snapshot identifier.

## Capture and content requirements

1. Resolve a qualified prepared parent and explicit extraction request before
   capture. Keep original source/occurrence keys and local atom/frame/state maps.
   Different occurrences can share verified feature payloads, but their ordered
   manifest bindings remain distinct. Equal names, labels or coordinates do not
   establish molecular equivalence.
2. Invoke/reuse the actual public feature operation under its declared unchanged-
   input precondition. Record the effective requested family set; caller ordering
   and duplicates have no extra scientific meaning where `get_features()` uses
   a set. Record output feature order exactly; never sort or deduplicate features
   merely to produce a stable digest.
3. Seal complete native evidence through the existing quantity/provenance owner.
   The initial classical profile uses explicit nm centers, dimensionless vectors/
   normals and elementary-charge quantities. Preserve scientific units through
   PyUnitWizard `QuantityRecord`; readers name the known field and expected
   dimensionality. Finite geometry remains required. Literal identifiers such as
   `nm`, `1 nm` or an opaque occurrence key remain text.
4. Specify encoding/canonicalization and its version in the implementation before
   promising content IDs. Reuse the existing finite-JSON operation and quantity
   codec; add no competing molecular/quantity codec. Hash exact stored bytes.
   A content hash checks consistency, not authentic origin or correct chemistry.
   A change in unit representation is a new encoded payload, even when an explicit
   provider conversion proves equal physical values. Preserve both records and
   their derivation; do not infer compatibility from a changed session default.
5. Separate scientific bindings from locators, display names, timestamps and
   availability observations. Relocation of verified identical bytes/maps does
   not change scientific identity. Changing a source/occurrence key or ordering
   changes the manifest binding even when the feature bytes can be shared.
6. Keep completed, evaluated-empty, partial, unsupported, failed and unattempted
   coverage explicit for the request and its original occurrences. An empty
   observed feature list is not evidence that every family was requested. A
   failed extraction has no manufactured empty-success payload or negative score.
7. Preserve complete original attribution from the operations actually reached.
   Inspecting, hashing, describing or reading a saved snapshot earns no new
   scientific credit. Version labels and source/native receipts retain their
   original identities rather than being normalized to the current environment.

This contract does not promise binary identity for all equivalent encodings,
automatic atom renumbering, unit-invariant hashes, molecular authentication,
thread-safe access to arbitrary live sources or complete native build attestation.
Those need explicit supported operations and receiving before use.

## Reuse decisions and exact reexecution

Decide separately whether the original feature content is retained, a retrieval
asset remains qualified for the requested predicate/domain, and a plan/run may
continue. An old artifact can remain readable while being unsuitable for a new
calculation. Unknown evidence is not a successful compatibility decision.

The [worked decisions](examples/feature_snapshot_reuse_decisions.json) are
normative design/acceptance examples, not outputs of an implemented detector.
Their short action words are table notation, not new API return values.

| Change | Feature snapshot/content | Retrieval asset | Plan/run |
| --- | --- | --- | --- |
| Exact same verified bindings and request | Reuse | Reuse within its qualified domain | Resume under the existing exact contract |
| Only an external locator/display/stock observation changes | Retain verified content and scientific binding | Reuse after required location verification | Same scientific context; preserve dated metadata separately |
| Prepared topology/state/conformer/geometry/atom mapping changes | New snapshot/capture | Rebuild/requalify from the new parent | New linked plan/run |
| Original occurrence keys, multiplicity or order change | New manifest; payload sharing needs explicit maps | Rebuild/rebind with qualified original mappings | New plan/run |
| A requested family or feature definition changes, including a new empty family | New capture with explicit request coverage | Rebuild/requalify | New plan/run |
| Only request spelling/order changes but the qualified effective family set is equal | Preserve resolved request and feature order | Reuse if all other bindings agree | Existing plan's exact serialized comparison remains authoritative |
| Direction/normal/charge or unit/frame representation changes | New captured/derived payload | Requalify; do not silently rebind old postings | New plan/run |
| Predicate implementation/numerical policy changes under the same method name | Retain original feature evidence; qualify its ingestion | Requalify against the new unchanged reference | New plan/run; current broad runtime binding may already refuse resume |
| Query/tolerance/score/grouping or run budget changes within a qualified asset domain | Reuse compatible captured content | Reuse only the supported retrieval stage | New plan/run with all effective settings |
| Query/domain/required feature semantics are unsupported or unverified | Preserve original evidence; request missing supported capture if necessary | Refuse automatic reuse; no implicit fallback | Explicit new supported method/plan or pending work |
| Bin/precision/representation/build contract changes | Reuse compatible captured content | New asset and qualification | New plan/run |
| Complete evaluated-empty requested family | Valid captured evidence for that request | May answer only its supported finite domain | No automatic molecular inactivity or arbitrary-query negative |
| Missing context, unknown schema, corrupt payload or unverified parent | Reject promotion/reuse or retain unknown state | Refuse automatic use | No calculation or invented negative from that missing evidence |
| Query budget returns only a prefix | Original snapshot remains intact | Asset qualification and query completion remain separate | Unsearched work is unknown/pending; preserve confirmed work |
| Replacement build fails/cancels/is partial | Keep the preceding complete snapshot and original lineage | Keep old qualified asset; failed replacement is distinct | Existing runs keep their original binding; an older snapshot needs explicit selection |

Qualification can later justify finer reuse. Equality of output examples, a new
label or a method-name match does not authorize it by itself. In particular, the
#178 one-bin guard is qualified only for its finite analytical domain. Initial
retrieval there requires the complete typed query, including the selected anchor;
optional/alternative features, other essential-site policies, excluded volumes,
direction-dependent semantics and different scales need their own admission.
A prefilter must preserve the necessary condition of the declared final problem,
not silently replace that problem with its own easier predicate.

## Existing prepared-run compatibility stays unchanged

Use the existing six boundaries: `prepared_snapshot`, `preparation`, `features`,
`index`, `grouping`, `numerical`. A future qualified feature/asset record can be
referenced inside the existing producer declarations; this contract does not
change that plan schema or retroactively enrich saved declarations. `index=None`
continues to describe the supported non-index route. An old declaration that
included a path is compared exactly as originally recorded, not rewritten to
apply this design's separation of locators.

Query bytes, expanded defaults and exact current plan/runtime comparison remain
authoritative for resume. Saved inspection reads original evidence without
comparing current producers, running science, emitting old diagnostics again or
registering another citation. A new plan/run links its parent rather than editing
an old query, terminal failure, outcome or producer record.

## Guided use, expert composition and acceptance

Guided use should explain the owning action: preparation changed, request coverage
is missing, the index needs qualification, the query requires a new plan, or
some work remains unknown. Expert inspection exposes the same original IDs,
resolved request, coverage, producer/predicate/domain and evidence behind that
decision. Both routes must consume the same public capture/preflight operations;
a second hidden decision engine is not acceptable.

The next implementation increment is a bounded capture/inspection prototype on
native feature inventories using the existing public producer and quantity codec.
Freeze its wire profile, finite sizes, explicit parent trust/preconditions,
invalid-input behavior, requested-versus-empty coverage and the worked decisions
before coding. Reuse public providers and qualify real capture/readback/changed-
unit/literal-ID/duplicate-occurrence/producer/unknown-work controls. Receive the
same bodies from source and an exact owned artifact before promoting an API.
Persistent storage, publication/replacement and a production index remain separate
acceptance gates; broader performance/public-platform/biological/human/release
qualification and #148/#165 stops are unchanged.

## Evidence and provider handoff

The [contract receipt](evidence/feature_snapshot_contract_20261110.json) records
exact inspected source, AST facts, unchanged runtime bytes, documentation/local
checks and the provider handoff. MolSysMT#624 receives parent identity, original
mapping, relocation/mutation and failed-refresh acceptance examples; it retains
its choice of API/format/backend and no delivery schedule is imposed.
This increment is design/source inspection only. It does not rerun #175/#177/#178,
execute a molecular calculation, create scientific attribution, qualify an
installed snapshot implementation or modify a provider/shared environment.

## Bounded prototype follow-up — #180, 2026-11-10 UTC

The [capture/inspection receiving](feature_snapshot_prototype.md) now implements
an unshipped fixed-profile tool and explicitly separate quantity reconstruction.
Its [receipt](evidence/feature_snapshot_prototype_20261110.json) receives32guards
and eight complete scientific rows per source/exact-owned218context, plus two
fresh scientific-import-blocked readers of all16original snapshots. The
[24-case mapping](examples/feature_snapshot_prototype_coverage.json) documents
covered/partial/deferred scope. This follow-up does not retroactively change the
source-only #179 review, authenticate declared molecular origin or promote a
public codec, compatibility detector, production index or generic collection.

## Native ingestion follow-up — #181, 2026-11-10 UTC

The [snapshot-ingestion receiving](snapshot_retrieval_ingestion.md) now connects
the original frozen native captures to the existing finite candidate prototype.
Its [receipt](evidence/snapshot_retrieval_20261110.json) receives 41 selected guards,
24 complete rows and 72 independent rational comparisons per source/exact-owned218
context. Original work/feature/atom maps, short/empty/repeated records, provenance
and unknown prefixes survive. An overstrong unsafe-bin control assertion and its
nm/pm rounding diagnosis stay original; only its expected misses were corrected.
This follow-up does not change earlier run identities, promote a stable public
API/index/compatibility detector, authenticate source or qualify cost/biological/
platform/release gates. Next receive wider typed-feature/numerical inputs before
equivalent-cost measurements or production-index selection. #148/#165 stay stopped.
