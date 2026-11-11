# Minimal public feature-asset API proposal

Owners LMMV/dprada; 2026-11-11 UTC;
[#188](https://github.com/uibcdf/pharmacophoremt/issues/188), following
[the guided/expert exercise](feature_store_workflow.md).
All names/signatures below are **proposed, not importable public APIs**. This
increment qualifies design and unshipped argument/diagnostic admission. It does
not publish a package, format, writer or production search index.

## Decision and existing owners

Propose a cold `pharmacophoremt_features` namespace in the **same PharmacophoreMT
distribution**, with native inventory reconstruction in the scientific host.
There is no separate `pip install pharmacophoremt_features` product or new minimal
installation promise. Existing dependency closure and supported delivery remain
#23-owned; an import that avoids science is distinct from an installation without
scientific dependencies.

| Inspected alternative | Disposition and reason |
| --- | --- |
| Put every operation under the current `pharmacophoremt` root | Keep scientific orchestration here. The current root eagerly imports unit/model/IO/viewer modules, so it cannot supply the cold metadata boundary without a separately qualified import redesign |
| Add feature storage to `pharmacophoremt_results` | Reuse its public finite JSON and observed reader/admission patterns. Keep its run/outcome formats and private SQLite tables separate from feature assets |
| Cold `pharmacophoremt_features` namespace | Proposed reader boundary, following the existing same-distribution results pattern; import support providers and standard library only |
| Expose existing `*Study` classes as public names | Refuse direct promotion. Their formats/profiles, twelve-record/2 MiB limits and local POSIX qualification remain experimental evidence |
| Build a general molecular collection in PHMT | MolSysMT#624 owns preparation/source collection, mappings and molecular lifetime; no local substitute |

The [source audit/receipt](evidence/feature_asset_api_20261111.json) records exact
original sources and owning signatures. Source inspection does not prove a new
installed namespace. The current package-discovery prefix is relevant evidence,
not qualification of a package that does not yet exist.

## First public slice: read and explicitly reuse captured features

Keep explicit read-only and writer types. Avoid a generic `open(mode=...)` that
can accidentally create a missing store or turn inspection into mutation.

| Proposed operation | Contract to implement and receive |
| --- | --- |
| `FeatureAssetView.open(path, *, generation=None)` | Open a supported existing public-format asset. None resolves current once, then pins its verified generation; an explicit SHA-256 selects that generation. No creation, repair, extraction or schema migration |
| `view.generation` | Read-only generation identity, independent of locator/display labels |
| `view.summary()` | Detached supported-profile, manifest/coverage/count/byte identity metadata, including unknown/unsupported facts and scope; no quantity interpretation or origin authentication |
| `view.work_items(*, work_keys=None, offset=0, limit=100)` | Metadata page in original manifest order, with original global ordinals and separate selected/returned counts; no molecular source pulls |
| `view.snapshot_bytes(ordinal)` | Exact original completed payload bytes; explicit supported-format/size check. Original geometry and attribution remain caller-controlled data, never automatic diagnostic attachments |
| `view.inspect(required_families, *, work_keys=None)` | Selected evaluation coverage and actionable next steps, without admitting quantities, molecular origin, a query or a lookup |
| `view.close()` / context manager | Idempotent owned close; later access and pending iteration refuse. Already returned detached records remain caller-owned |
| `pharmacophoremt.screening.reuse_feature_inventories(view, required_families, *, expected_generation, work_keys=None)` | Explicit scientific activation: recheck the generation/selection, verify original quantity field/unit/dimension and geometry on every reuse, return complete native inventories with original global work keys/ordinals |

The guided route uses these same operations. A preview report is descriptive
data, not an authorization passport. Native reuse does not accept a mutable
`validated=True` flag or infer compatibility from a prior quantity context.
Required families check evaluation coverage; complete original inventories are
returned without filtering, sorting or renumbering extra captured features.
A whole incomplete manifest and a complete selected subset remain separate.
Query/predicate/source admission and saved-run resume retain their owning tools.

Proposed composition after implementation and delivery (not a current recipe):

```python
from pharmacophoremt_features import FeatureAssetView
from pharmacophoremt.screening import reuse_feature_inventories

with FeatureAssetView.open(path) as features:
    preview = features.inspect(["hb donor"], work_keys=["nm", "1 nm", "repeat=α"])
    inventories = reuse_feature_inventories(
        features,
        ["hb donor"],
        work_keys=["nm", "1 nm", "repeat=α"],
        expected_generation=features.generation,
    )
```

A beginner follows preview/actions; an expert composes the same view, request
and scientific operation. A valid preview may still require quantity validation;
missing family evaluation must be explicitly obtained through a qualified capture
route. This design does not turn aromatic-only empty features into donor negatives.

## Generation, selection and pages

- Opening may resolve None once. Existing handles never follow CURRENT silently.
  Reopen explicitly to choose the newer generation. Reusing an older pinned view
  is allowed only as an explicit captured-generation choice; it does not prove
  current source preparation, stock or query compatibility.
- A generation is an exact lowercase SHA-256, not a version/display name or
  `"current"` magic token. It checks consistency, not chemistry or authentic origin.
- Work keys are literal nonempty strings. Preserve spaces, Unicode and unit-like
  text; do not trim, case-fold, parse quantities or identify molecules by names.
  Duplicate selected work keys refuse. Repeated source/occurrence bindings remain
  distinct original work positions.
- `work_keys=None` chooses all declared occurrences; `[]` chooses none. Unknown
  requested keys refuse rather than produce an empty collection. Selection order
  is original manifest order regardless of the caller's key-list order.
- Required families are explicit and nonempty. Canonicalize the existing classical
  family set; duplicate family names have no extra scientific meaning. Unknown
  families refuse under this profile rather than silently downgrade semantics.
- Snapshot ordinals are nonnegative integers, excluding booleans; validate their
  range against the pinned manifest before accessing a payload. Metadata getters
  and close/iteration retain the handle's explicit lifetime contract.
- Page offsets refer to the **selected** stream, while returned `work_ordinal`
  remains the original manifest position. Return generation/selection binding,
  `selected_count`, `returned_count`, records and `next_offset`; do not present a
  page count as a full denominator. A zero limit returns no rows and no claim that
  the selected corpus is empty. Booleans are not integer limits/offsets.
- The initial bounded profile can know manifest counts from verified metadata.
  Future profiles must keep unknown counts unknown; preview never drains a
  one-pass molecular iterator to obtain them. No unbounded default export or
  transparent full-library materialization is introduced.

## Later writer and recovery slice

Proposed `FeatureAssetStore.create(path, *, profile, limits)` and
`FeatureAssetStore.open(path)` remain explicit and separate from the view.
`seal(records)` must validate domain bindings, incomplete causes, full original
payloads, quantities and geometry before producing an eligible immutable
candidate. Publication is a separate
`store.publish(generation, *, expected_current, retry_of=None)` operation.
`expected_current` is required, including explicit None for first publication.
A retry links an actual retained attempt; a caller cannot fabricate successful
history by supplying an arbitrary identifier.

A public metadata recovery operation can compose store-owned current-view and
attempt inspection under the declared writer lease. It must distinguish receipt
state, current visibility and candidate validation. Inspection performs no retry;
explicit retry uses the same publication validator, refuses an already-current
or displaced candidate and leaves unknown earlier history unchanged. A raised
caller after replacement does not imply rollback. Do not expose a private store
path or require a caller to assemble potentially inconsistent private readers.

This writer/recovery surface requires its own format, publication, resource,
close/interruption and platform qualification. The prototype's no-follow file
checks and cooperating POSIX lease are local evidence, not distributed,
power-loss/fsync or hostile-filesystem guarantees. Read-only metadata should not
import a writer's POSIX/backend requirements merely to access shared constants.

## Argument and diagnostic ownership

Use ArgDigest's function contract **and** value digesters with explicit logical
owners, standardizer/alias scope and registry strictness. In particular, the
same argument `generation` permits None only at view opening; publication requires
an exact identity. Preserve native Python TypeError and ArgDigest's compatible
call-shape exceptions. Do not wrap them into an unrelated storage ValueError.
No broad alias table or string/quantity coercion is proposed.

The unshipped `phmt_test_support.feature_asset_admission` package receives five
logical owners: open, inspect, native reuse, page and publication. It returns
normalized request **data**, touches no input reader/path and registers only its
study catalog through SMonitor's declaration-only provider operation. Its
12-selected-record/text bounds are inherited study-profile controls, not the
public corpus/page-size contract. Public resource limits must be declared and
qualified for each real backend/profile; existing .2 MB bundles establish no
public library scale or persisted-index crossover.

Use catalog-backed `FeatureAssetError` categories for future value/format/storage/
lifetime/quantity/coverage/publication remedies, with original exceptions chained.
Actual final diagnostic IDs are not assigned here. The six
`PHMT-ASSET-STUDY-E...` IDs belong to this unshipped experiment and cannot be
advertised as stable PHMT codes or repurpose existing PHMT-E201 run semantics.
Expected inspection decisions are data; scientific reuse failures emit the
appropriate catalogued remedy. Dependency absence keeps DepDigest's owning
availability semantics instead of becoming an empty inventory.

SMonitor owns rendering, audience/capture policy, handler setup and emission.
Register declarations without replacing application policy or installing another
handler. Include typed safe context such as operation/argument/ordinal when
permitted; never attach raw paths, keys, payloads, coordinates, repr or native
exception text automatically. Restrictive scopes must still produce useful
metadata wording. Do not copy a renderer or turn all errors into one free-text
message template.

The existing distribution floors ArgDigest>=0.17.1 and SMonitor>=0.22.1 cover the
contracts used by this admission study. Actual 125-payload cold support receiving
is evidence for that route, not every supported installation. No new dependency
floor is changed here. Select and receive the owning QuantityRecord capability
floor and lazy scientific activation through DepDigest before public decoding;
its API remains provisional. No competing quantity/molecular codec or source
parser belongs in this reader. Saved references are retained without new Ackredit
usage or automatic enrichment.

`skip_digestion` belongs to internal calls carrying values just constructed by
the library; it is not exposed by these proposed public signatures. The provider
forwards a literal True bypass to the underlying callable rather than removing
a keyword the callable never declared. A plain request dictionary remains data:
the underlying generation, payload, quantity and domain owners always validate
before actual use. There is no replacement validation-passport mechanism.

## Implementation and delivery gates

1. Receive this proposal, owning source audit and real provider admission/capture
   controls. This step introduces no public imports or installed artifact.
2. Select a public **read-only** format/profile and implement the cold view under
   its own issue. Keep original study artifacts unchanged; reject unsupported
   study schemas by default. Any explicit historical reader/converter has a
   separately named policy and retains original bytes, provenance and identities.
3. Implement the scientific inventory adapter through an owning PHMT operation
   and public PyUnitWizard handshakes, with actual capability floors, admitted
   context and captured-scope semantics. Preserve the existing native API and
   select appropriate installed/source/platform gates before promotion.
4. Receive writer/publication/recovery separately after its declared profile,
   bounds, candidate qualification and cross-platform/local filesystem limits.
   Avoid silently making this a general collection or a production backend.
5. Receive exact-candidate public packaging/import closure, documentation/examples,
   diagnostics and supported matrix under#9/#23. Conduct the declared novice/expert
   tasks independently. Human participant count remains zero in current evidence.

The [receipt/archive](evidence/feature_asset_api_20261111.json) preserves initial
control-assumption corrections, final provider tests and cold capture. Original
#186/#187 science and runtime/provider identities remain separate; no new native
matching, molecular operation or benchmark runs. MolSysMT#624, persisted lookup,
biological validation, human receiving and stopped#148/#165 retain their owners.
