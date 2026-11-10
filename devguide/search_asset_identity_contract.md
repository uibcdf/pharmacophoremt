# Persistent feature/search assets: identity, coverage and lifetime

Contract revision 1; owners LMMV/dprada; #185; 2026-11-10 UTC. This extends
the [captured-feature contract](prepared_feature_snapshot_contract.md) after
[finite cost receiving](retrieval_cost_workloads.md). It defines acceptance for
the next storage experiment. Public names, a wire schema, physical container and
production index remain undecided. Existing inventories, plans, runs and readers
retain their contracts.

## Separate durable objects and identity namespaces

```mermaid
flowchart LR
    S[Provider prepared source] --> F[Captured feature payloads]
    F --> M[Ordered occurrence manifest]
    M --> I[Optional derived lookup]
    M --> P[Query and execution plan]
    I --> P
    P --> R[Run and committed outcomes]
```

These are semantic layers, not proposed field spellings:

| Layer | Required binding and owner |
| --- | --- |
| Prepared source | MolSysMT owns molecular representation, preparation, source/state/conformer/atom correspondence and collection/lifetime guarantees. An external label, Python object identity or claimed digest is insufficient. |
| Captured payload | PHMT owns ordered features, extraction request, completed family coverage, source correspondence, explicit quantities, recognition and original attribution/producer context. |
| Occurrence manifest | PHMT owns original ordered work keys, multiplicity, payload references, per-record readiness/causes and declared selection. Shared payloads do not merge occurrences or original atom/feature maps. |
| Derived lookup | PHMT owns the exact manifest binding, representation/precision, supported query/predicate domain, construction coverage and qualification. Rebuildable lookup data remains separate from feature extraction. |
| Storage generation | The selected asset adapter owns immutable published contents, locators, verification and handle lifetime. Its container checksum and physical layout do not replace logical payload/manifest identities. |
| Query/run | Existing plan/run owners bind exact query, effective settings, methods, grouping, budgets, original manifest and actual execution. Asset reuse does not resume another run. |

Distinguish exact encoded-byte hashes, canonical payload digests, ordered-manifest
bindings, derived-representation identities and publication-generation names.
Each identity names its namespace and encoding/version. Never compare two bare
digests as though they establish the same claim. The current snapshot study
requires canonical envelope bytes: outer JSON reformatting can retain the inner
payload digest but is refused at format validation before lookup binding checks.
Relocation preserves the original bytes. A future representation migration needs
its own explicit version/reader and retained original; this contract chooses no
new hashing protocol or admissible alternate outer encoding.

Moving verified identical bytes/maps changes a locator, not their logical meaning.
Changing original work keys or ordering changes the manifest even when payloads
can be shared. Optional presentation labels and dated availability observations
stay outside scientific bindings; original source/occurrence keys remain literal
identity data, including `nm`, `1 nm` and repeated aliases. A different quantity
encoding remains a different recorded payload even where explicit conversion
demonstrates equal physical values. Keep both originals and their derivation.

Hashes establish consistency. Self-consistent claimed producer/source metadata
does not authenticate execution, chemistry or origin. Retain the caller/provider
trust precondition and actual qualification evidence independently.

## Coverage is an admission plane, not a match result

Each captured request retains the effective definition, families, selection,
frame/state and coordinate policy. Observed feature kinds cannot reconstruct an
empty request. Complete evaluation of aromatic rings alone establishes no donor
evaluation. The actual old empty fixture requested only aromatic rings; donor/
charge evaluation is unobserved. The earlier #181–#184 experiments deliberately
match captured point inventories; they do not become molecular-family-complete
screening or biological negatives under this new contract.

The first coverage preflight reports evaluated counts for explicitly required
classical families and lists missing evaluations. Required-family order/duplicates
have set semantics; feature multiplicity and native matching indices do not.
Its output leaves query admission and match outcome unset. It checks no quantity
semantics, molecular origin, geometry, predicate/runtime or storage compatibility.
The private [implementation](../phmt_test_support/search_asset_contract.py) reuses
existing request/coverage validation rather than inferring coverage from points.

The initial full-source admission is conservative: require complete evaluation of
all required families before admitting the ordinary matching route. A future
qualified necessary-feature/count bound could prove a mandatory full query
impossible despite other missing families. Such a proof needs explicit mandatory/
optional/query semantics; the coverage helper makes none. A missing evaluation
is never silently substituted with a zero count or native evaluated-empty result.

Within a declared profile, distinguish completed populated, evaluated-empty,
unsupported, failed, partial and unattempted extraction outcomes. A terminal build
can finish with failed records without becoming a fully usable source corpus.
Publish coverage and original denominators; unsupported/failing/unknown records
remain unscored. A deliberately admitted subset gets its own explicit scope and
binding. Preserve source order and earlier causes when retrying as a new attempt.
The current successful-capture study envelope does not encode failed/unsupported
captures. Their future manifest records must remain separate; do not weaken that
envelope or fabricate a completed empty payload to represent a failed capture.

## Independent questions before reuse

| Question | Required decision |
| --- | --- |
| Can metadata be inspected? | Recognize the supported header/record format and verify its declared integrity. Keep unsupported/opaque sections explicit; do not execute stored code. |
| Can payloads be interpreted? | Use owned codecs and named reader handshakes, validating quantities, geometry and original maps. Metadata inspection alone does not do this. |
| Is the source/selection applicable? | Verify actual parent/manifest correspondence and trust/lifetime requirements; preserve multiplicity and the requested release/selection. |
| Does captured evaluation cover the query? | Resolve query-only constraints first, then inspect required evaluation coverage. Missing evaluation follows an explicit unsupported/subset/re-extraction policy. |
| Can a derived lookup serve it? | Check representation, precision, supported feature/query domain, conservative predicate guarantees, exact qualified producer/runtime or a separately qualified migration. |
| Is it current? | Compare the requested source/alias/release relationship separately. A superseded generation can remain valid historical evidence. |
| Can a run resume? | Existing exact query/manifest/recipe/software and committed-outcome checks apply. A readable or reusable upstream asset does not imply resumability. |

The current study's byte/work and record/settings checks are useful primitives,
not complete predicate/native dependency qualification. Its settings name a
bounded profile, labels, width and guard but do not automatically capture a full
native/scientific implementation closure. `PreparedRunPlan` separately binds six
declared compatibility boundaries and a conservative current-runtime fingerprint;
caller declarations and version labels do not establish molecular authentication
or complete native/provider source closure.

Query geometry, family names, parameter/unit errors and unsupported methods must
be refused before opening/draining inputs whenever that boundary can decide.
Retain original feature indices through filtering. Three-in-four matching,
orientation/normal checks, conservative proposals, final fitting and scoring keep
their owning scientific definitions. A query change can reuse compatible feature/
lookup assets but creates a new query/plan/run. A numerical method or representation
change requires explicit requalification/rebuild, even if its family name matches.

## Quantities, provenance and reader independence

Reuse PyUnitWizard `QuantityRecord` and the existing finite-JSON owner. Readers
name the known field and expected unit/dimension/kind. A valid sealed time record
in a feature center can pass structural inspection and family coverage, while
the length handshake must refuse it before scientific use. Preserve scalar charge
meaning/sign, vector shape/dimension and original participant/geometry maps.
Session defaults do not supply missing units or convert literal identifiers.

The registered quantity-record API remains provisional until its owning promotion;
closed design/implementation issues do not establish a stable public delivery
promise. Keep qualified source/provider identities and consumer migration/read
evidence. PHMT defines its scientific schema and does not invent a competing
quantity codec, infer units from field names or keep canonicity passports for live
quantity objects. A source-generation token cannot bypass record verification on
read or the receiving field handshake.

Preserve complete detached original bibliography, uses and producer versions with
each capture. Reading, inspecting, relocating or rebuilding an index from old
features does not credit original feature extraction again. New calculations add
their actual branch credit in the application's session. Optional-provider failure
and absence keep completed science and explicit attribution gaps. No hooks,
journals, enrichment or network lookups are enabled by asset opening.

## Generation publication and resource ownership

Keep build state, publication, coverage, qualification, currentness and handle
availability independent. A filesystem path named current is a locator/alias,
not an immutable scientific identity. Resolve and pin one declared generation
per handle; a reader never changes generations silently.

1. Prepare a candidate beside the old published generation. Freeze its declared
   manifest/scope, payload bindings and effective construction settings.
2. Validate each offered payload, explicit failure/coverage records and complete
   lookup-to-original maps under the intended profile. A completed attempt with
   missing records retains those gaps; it does not claim universal corpus recall.
3. Verify supported read/closure behavior and the qualification receipt before
   making the candidate visible as the requested generation.
4. Publish through one adapter-qualified boundary. Update a current alias only
   after the candidate qualifies. Retain old generations/failed attempts and the
   recovery route. Failure before the publication boundary preserves the old
   publication. After that boundary, an interrupted/raised caller can already
   have published the new generation; verify visibility rather than infer rollback.
5. Pin readers to the old or new generation without mixed payloads. An adapter
   without qualified overlapping-reader/publication support must require closure
   or refuse publication while readers exist. No multiwriter guarantee is assumed.
6. Close only owned resources. Caller-owned molecular readers, plans and other
   generation handles keep their ownership. Closing a handle is idempotent where
   promised; further access/iteration refuses predictably without recomputation.

Single-process/local-file atomicity, SQLite transactions, power-loss durability,
network filesystems and distributed visibility are different claims. The
existing `ScreeningRunStore` is a run/outcome ledger, with a close-writer-before-
reader contract; `ScreeningRunView` pins a verified read-only run snapshot. Reuse
their public run semantics for results, not their private tables as an unqualified
feature/index container. A future asset adapter must qualify its own storage and
lifetime contract. No physical format is selected here.

Before/after-publication interruption probes must distinguish missing candidate,
partial candidate, sealed unpublished generation and published generation. Only
confirmed visibility is authoritative. Uncommitted work stays unknown; a retry
records a new linked attempt and can recompute uncommitted work. Exactly-once
computation/external delivery is not promised. The #183 checkpoint helper retains
progress/credit for research drivers; it is not this publication transaction.

## Guided/expert parity and implementation gates

Guided use offers inspect, reuse compatible features, explicitly capture missing
evaluation, optionally build lookup, execute, recover and inspect/export. Show
effective strategy, generation, scope/omissions and required setup without exposing
routine users to internal file management. Expert operations expose the same
resolved scientific settings, original maps, qualification/binding reasons and
resource ownership. Fallback or subset selection needs an explicit recorded policy;
it cannot silently weaken the requested question.

The next bounded storage experiment should start from already captured original
feature bytes and an explicit manifest. Select a justified implementation route
after reviewing these requirements, then qualify new/create-versus-open refusal,
reopen/relocation, corruption, staged replacement, failed refresh, pinned or
explicitly exclusive readers, early close and retained attribution. Include
non-default unit-policy handshakes and changed source/query/producer/profile
scenarios. Keep source-family coverage distinct from captured-inventory matching.

MolSysMT#624 continues to own heterogeneous molecular collections/snapshots and
lifetime guarantees; no PHMT molecular parser/state/conformer/collection fallback
is authorized by this contract. ArgDigest/SMonitor/DepDigest and public dependency/
quantity floors need boundary review before public API promotion. No new public
API, persisted schema, backend, index default or platform/release qualification
follows. #148/#165 remain stopped; #9/#23 retain complete delivery gates.

## Executed contract receiving — 2026-11-10 UTC

The [receipt/archive](evidence/search_asset_contract_20261110.json) records a
ten-file exact-source audit, 24 passing primitive controls per source/exact-owned218
context, two cold readers of all20original snapshots and two real-provider
metadata sessions reading each twice. Cold readers block scientific imports and
verify125public support payloads; real sessions with PHMT attribution enabled
observe no new credit and unchanged original references. Native matching, feature
generation and molecular operations remain zero. All214wheel payloads/159runtime
bodies/4594provider Python files/native/69final fixtures verify.

The first test execution has22passes/two failures. Its initial draft/control
assumption allowed noncanonical outer reformatting, while the existing reader
correctly requires canonical text. Original first-run evidence is retained and
the draft/tests corrected without changing that reader. The final controls
separate relocation, canonical format refusal, changed byte/work bindings,
explicit unit conversion, synthetic producer consistency and quantity-handshake
failure under nm/pm policies. They are primitive proofs, not complete adapter
publication/lifetime qualification.

Run the focused controls in an admitted compatible environment:

```bash
python -m pytest --receptor=llm tests/test_search_asset_contract.py
```

The [acceptance examples](search_asset_acceptance_examples.md) mark existing public
run semantics as source-inspected and future physical-adapter probes as pending.
Seven local quality/governance gates and strict user-documentation receiving are
linked from the receipt. This source-supported contract and narrow coverage plane
resolve #185; no physical schema, asset writer/reader, index backend, benchmark or
public/platform/release claim follows. Next choose and qualify the bounded store
experiment under these requirements. #148/#165 remain stopped.


## First bounded adapter — 2026-11-10 UTC

The [feature-store study](feature_store_study.md) implements a local POSIX
immutable manifest/payload experiment under#186. This does not select a public
format, molecular collection or persisted lookup backend. Its receiving and
resource limits remain adapter-specific.
