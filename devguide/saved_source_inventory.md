# Original saved-source inventory

Owners LMMV/dprada; 2026-11-09; [#170](https://github.com/uibcdf/pharmacophoremt/issues/170),
the accepted mature-0.x milestone2/#108 workflow.

`ScreeningRunView.source_items()` yields detached `source_key`,
`first_manifest_ordinal` and `declared_work` records, ordered by first original
manifest occurrence. Each exact label groups its declared work only: no trimming,
case folding, compound alias, state/conformer inference or chemical equivalence.
All repeated occurrences and every confirmed/unpublished state remain counted.
Publication changes outcomes, not the frozen inventory/order/counts.

The existing stdlib store owns a metadata-only SQL grouping operation, reused
by the public view with its existing ArgDigest definition owner and SMonitor
boundary. The iterator is lazy and caller-owned; closed/foreign-thread/deferred
errors retain the structured reader boundary. Opening verifies the complete
original file, including all outcomes and records outside any displayed prefix.
Subsequent inventory traversal decodes no native/draft body and earns no credit.
SQLite grouping/sorting may need whole-manifest work and temporary storage; no
constant-SQL-memory, index, speed or large-library claim is made.

`--sources` composes that same public iterator in one read-only snapshot. The
opt-in `pharmacophoremt.screening-source-page@1` response retains original
run_id/run_format/work_sha256, global declared_work, distinct-literal
declared_sources, source offset/limit/next_offset and original records. Positive
limits/nonnegative offsets are validated before I/O; arbitrary-precision Python
windows avoid islice overflow. Count the full stream once while retaining only
the requested page. Read/count/view-close failures emit no success JSON.
Source mode excludes all other modes, score/status/source-key selection and
exports; explicit legacy admission remains. Existing response bytes retain their
own original formats. Source pages bind to the immutable run/work hash; selected
status work pages retain their separate publication-sensitive semantics.

The [plan](evidence/source_inventory_plan_20261109.json) predates implementation.
Independent mixed/opaque/repeated/all-state/after-publication, lifetime, legacy,
late-error and full-admission controls and thirteen ordinary byte controls are
required, followed by the same original bodies from one exact owned source-free
reader artifact. The [source receipt](evidence/source_inventory_source_20261109.json) receives
134cases (14new/120existing), thirteen exact ordinary command-byte controls,
strict full docs/rendered navigation,25distribution and reporting/archive checks.
The original red control retains12failures/2passes. The [installed receipt](evidence/source_inventory_installed_20261109.json)
receives the same134bodies from adbecee / owned208,157guarded children,24documented
commands on four unchanged historical stores and thirteen ordinary exact-source
outputs. All214wheel payloads/159runtime identities and seven loaded reader
origins verify. The [archived report](archive/browse_saved_sources.md) resolves
this bounded bridge. Complete discovery-to-detail composition is separate#171. Public guidance is
in the [saved-work cookbook](../docs/content/cookbook/saved_work_inspection.md#browse-the-original-sources).

No persistent schema/index, molecular collection/parser, source connector, provider
floor or attribution/scientific operation is added. The original af408e7 source
checkpoint and its single-cell recovery cannot qualify these later bytes.
Full source/public/platform/installed, human-usability, biological, performance
and release gates retain independent acceptance; #148/#165 remain stopped.
