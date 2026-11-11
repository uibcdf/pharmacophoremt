# Read-only feature-evidence archives, version 1

Owners LMMV/dprada; 2026-11-11 UTC;
[#189](https://github.com/uibcdf/pharmacophoremt/issues/189). This implements the
first reader slice of the [API proposal](feature_asset_public_api.md).
`pharmacophoremt_features.FeatureAssetView` is a same-distribution public source API.
Its public-channel/platform/release qualification stays separately #23-owned.

## Meaning and validation planes

The first profile is `declared-classical-inventory@1`. It stores ordered declared
extraction metadata plus exact **opaque original bytes**. The reader validates
canonical structure, bounds, metadata consistency and byte hashes. It does not
parse those original payloads, recalculate their feature counts, interpret units,
authenticate molecular origin or admit a query. Even a payload-format identifier
is a producer declaration, not evidence that this reader understands that codec.

`inspect()` reports `declared_counts` and `unobserved_families`. An evaluated-empty
family is a recorded producer declaration; missing evaluation stays unobserved.
All results state `original_payloads_interpreted=False`,
`quantity_semantics_checked=False`, `molecular_origin_authenticated=False`, with
query/match decisions unset. A complete family request requires a separately
qualified original decoder and quantity/geometry validation before scientific
reuse. No metadata dictionary can substitute for those checks.

This narrower metadata boundary intentionally does not claim the snapshot-study
reader's original-body structural/quantity admission. The explicit unshipped
exporter validates original snapshots through their existing owner and copies
that metadata into a new archive. Its output does not make those study codecs
public or promote their original producer context. Public format readers remain
usable for other explicitly labelled opaque originals with the same declared
metadata profile. No competing quantity codec or molecular parser is added.

## Physical profile and bounds

A caller owns a trusted local directory containing canonical UTF-8 JSON:

- `STORE.json`: exactly schema `pharmacophoremt.feature-archive@1` and profile
  `declared-classical-inventory@1`.
- `CURRENT`: exactly that store schema, a lowercase 64-hex generation SHA-256 and
  the referenced generation document's exact `bytes` count.
- `generations/<sha256>.json`: one canonical generation document. Its exact
  SHA-256 is its identity. Paths, current aliases and relocation do not change it.

The generation has exactly `schema`, `profile`, `origin`, `records` and `payloads`.
Its schema is `pharmacophoremt.feature-archive-generation@1`; profile is as above.
`origin` retains the producer's source-format identifier, original generation
identity and explicit export policy. It is provenance data, not authentication.

At most 4096 records, 8 MiB encoded generation JSON, 4 MiB unique decoded original
bytes and 2 MiB per original are accepted. All bounds apply together. They are
reader limits for a bounded metadata-evidence profile, not public-library scale,
streaming, performance or persisted-index qualification. Finite text is bounded;
counts/parent indices use nonnegative signed 64-bit integers, excluding booleans.
Metadata strings are UTF-8; literal keys are nonempty and at most 512 UTF-8 bytes.

Every record retains exact `work_key`, `source_key`, `occurrence_key` and `status`.
Work keys are unique; repeated sources/occurrences/payloads preserve multiplicity.
Ready records also contain `payload_sha256` and `extraction`. Other statuses are
`failed`, `partial`, `unsupported`, `unattempted`, with exact cause type/reason
instead of a fake empty payload. Causes retain their original text as explicitly
requested data; they are not automatically attached to diagnostics.

`extraction` declares `classical_atomic_formal@1`, the canonical nonempty requested
classical-family set, coverage, prepared-parent metadata and original producer.
Coverage has exactly those requested families. Counts are bounded to 64 features
in total; a positive count uses `completed`, zero uses `evaluated_empty`. These
are metadata consistency checks, not counts recomputed from the opaque original.
Parent source/occurrence bindings agree with their record; original artifact
hash/bytes, atom count, frame/state, preparation and trust declaration are retained.
The trust string is not verified by the reader. Producer scope, admission digest,
runtime version and version mapping remain original declarations.

`payloads` maps each original SHA-256 to exactly `format` and canonical base64
`data`. Original bytes are nonempty, bounded and match their hash. Repeated
original bytes can be shared; unused or missing originals refuse. Ready/nonready
records, an explicitly empty complete archive and an unreadable store are distinct.
Unknown fields, unsupported schema/profile/definition, noncanonical encoding,
nonfinite JSON, malformed mappings or inconsistent counts/checksums refuse.

## Opening, selection, paging and close

`FeatureAssetView.open(path, generation=None)` resolves CURRENT once and verifies
one bounded generation. An explicit generation reads that exact generation without
consulting CURRENT. A missing store/generation refuses; opening never creates,
repairs, migrates, follows an updated alias or starts molecular work. Public-format
markers are mandatory: raw study directories refuse.

The reader uses no-follow/nonblocking descriptors and regular-file checks on the
qualified local POSIX route; store/generation directories must be real directories.
It imports no writer lease or `fcntl`. Hostile ancestor races, noncooperating
mutations, distributed/network-filesystem visibility and power-loss/fsync behavior
are outside this reader's claim. An unsupported filesystem reader profile refuses.

All selected metadata/payloads detach at open. A reader remains pinned if CURRENT
changes, its directory moves or another view closes. Close is idempotent; further
view access/context entry refuses. Returned metadata pages and original immutable
bytes remain caller-owned after close. No live owned iterator is exposed in this
slice; iteration over a returned detached list belongs to its caller.

Keys preserve case, spaces, Unicode and unit-like text. None selects all; [] selects
none; duplicates/unknown keys refuse. Selection follows original manifest order.
`work_items()` offsets index the selected stream, while `work_ordinal` remains the
original manifest position. Responses include generation, complete selected count,
returned count, page controls, `has_more` and `next_offset`. Zero limit is count-only:
no rows/next offset, while `has_more` may remain true. An empty page does not imply
an empty corpus. No molecular source is sampled to count work.

`snapshot_bytes(ordinal)` returns original completed opaque bytes at a global
ordinal. `inspect(required_families, work_keys=...)` explains incomplete extraction,
missing evaluation, explicit empty scope or the need for payload validation.
Required families admit neither a molecular source nor a matching method.

## Diagnostics and integration

ArgDigest owns definition-bound function/value admission. Native Python and
provider-compatible TypeErrors retain their call-shape meaning. No internal bypass
keyword is exposed. SMonitor owns catalog rendering/emission and application
policy. Codes PHMT-E301 through PHMT-E307 distinguish argument, integrity, read I/O,
closed view, unknown selection, absent completed payload and unsupported format/
reader profile. Original exceptions remain causes. Raw paths/keys/payloads/native
error text are not constructed as diagnostic extras; applications own capture.
Declaration-only catalog registration preserves configured policy/handlers.

Metadata import needs only standard library and existing support providers,
reusing public `pharmacophoremt_results.canonical_json`. It imports no main PHMT,
NumPy, MolSysMT, PyUnitWizard, RDKit, SciPy, Ackredit or test support. Avoiding
scientific imports is not a new minimal-installation or dependency-closure promise.
Native decoding remains a later API slice with the public provisional QuantityRecord
contract and qualified availability handling. Saved reading retains original
references/versions without registering new scientific use or enrichment.

The unshipped `export_study_feature_archive()` creates a **new** directory with
an explicit `explicit-study-evidence-export@1` origin policy. It retains old store/
payload bytes and identities, refuses an existing destination and leaves partial
new output for inspection. It is a one-shot fixture/export tool, not a public writer,
transaction, automatic conversion, publication or recovery implementation.

## Qualification and next boundary

The [completed reader receipt/archive](evidence/feature_asset_view_20261111.json)
receives 98 selected source controls and 98 installed controls, the exact owned
wheel from implementation commit `64bd805`, 221 wheel payload files and 166
non-generated runtime Python bodies. Both cold readers verify eleven original
payloads, the seven actual catalog errors, preserved application policy and three
exact documentation code blocks. Real Ackredit sessions preserve original bytes,
producer labels and detached references without adding new credit. The earlier
[source-only receipt](evidence/feature_asset_view_source_20261111.json) remains
unchanged as historical evidence.

The installed test context differs from the original source context: live
MolSysMT Python/native files changed in between. The first installed fence refused
before imports; the old native binary could not be recovered. Installed tests
instead use an independently copied and hashed current provider context (4608
Python files, versus the original 4594). This does not relabel old captures or
qualify the changed molecular provider scientifically. Cold readers import none
of those providers. Their SDK-only origin checks admit measured QA dependencies
after reader actions; the existing improvement is MolSysSuite#176.

The original pytest collection, controller dependency/bibliography assertions,
distribution-test corrections and the pressure-interrupted first build remain
recorded. One wheel-build resume used the same limits and existing private
checkout after pressure subsided. The distribution inventory now includes the
seven reader modules and 65 previously absent selected support/input files;
26 administrative distribution controls pass. No shared prefix was changed.

Selected source/owned evidence is separate from full supported public/platform/
release acceptance and human/biological validation. Keep #9/#23, MolSysMT#624,
persisted lookup/cost/scale and stopped #148/#165 separate.

Next connect a qualified native inventory reconstruction operation to this view,
with explicit accepted original formats, expected generation, QuantityRecord floor
and preserved original maps/attribution. Do not infer payload validity from public
archive metadata or silently accept every opaque-format identifier.
