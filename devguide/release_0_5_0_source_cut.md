# 0.5.0 source-only consolidation

Owners LMMV/dprada; decision received 2026-11-11 UTC;
[PHMT#95](https://github.com/uibcdf/pharmacophoremt/issues/95).
This is the current release decision. Earlier 0.5.0 reviews retain their dated
scope and pending statements; they do not describe this later source candidate.

## Delivered source checkpoint — 2026-11-11 UTC

Annotated [tag 0.5.0](https://github.com/uibcdf/pharmacophoremt/tree/0.5.0) now
identifies tested source `2bff5dcf454bc5230f473237a49939215a60aab2`; annotated
object `46cfa9abf3aaecf930ff5bd57ea4d2c51d69eddb` is verified remotely. The
[immutable qualification receipt](evidence/release_050_candidate_qualification_20261111.json)
is bound by SHA-256 in its annotation. Its pre-tag limits remain historical;
the [delivery receipt](evidence/release_050_tag_delivery_20261111.json) receives
the actual tag and subsequent conformance without rewriting that receipt.

| Exact-source gate | Received result |
| --- | --- |
| [Full source 42943148415](https://github.com/uibcdf/pharmacophoremt/actions/runs/42943148415) | All eight Linux x86_64/macOS arm64 × Python 3.11–3.14 cells: 3,088 passed each, zero skipped scientific cases, 115 exact unique coverage paths each. The same suite repeats across cells. |
| Reporting governance | 3 reporting, 18 archive, 8 route/recovery and 161 administrative controls. Optional skipped-backlog probe deliberately disabled. |
| [Source conformance](https://github.com/uibcdf/pharmacophoremt/actions/runs/42943155481) / [publication controls](https://github.com/uibcdf/pharmacophoremt/actions/runs/42943162141) | Both pass at that exact source; reviewed policy/SDK pins unchanged. |
| [Actual tag conformance 42950847682](https://github.com/uibcdf/pharmacophoremt/actions/runs/42950847682) | Passed at the actual 0.5.0 ref; one explicit dispatch received after no automatic run was observed. |

The [Linux 3.13 XML](evidence/release_050_ci_linux313_20261111_coverage.xml.gz)
retains the timestamp-stripped printed report; it is not an independent runner-file
checksum. Warnings remain recorded: Python 3.11 has 46 per cell; 3.12–3.14 have
63, including 17 threaded-parent fork deprecations tracked under
[#192](pending_proposals/interruption_process_isolation.md). No deadlock or
scientific failure occurred in the completed cells.

A private tagged wheel receives canonical 0.5.0, 221 exact installed payloads,
166 source-equal runtime bodies, cold original-byte reading, CLI and strict full
docs. Source CI retains its pre-tag `0.4.0+232.g2bff5dc` identity. These local
installed checks are not the full supported public-artifact matrix. No GitHub
Release exists; no package/docs publisher was invoked. The required suite notice
is [MolSysSuite#182](https://github.com/uibcdf/molsyssuite/issues/182).

The later main closeout contains documentation/evidence/reporting only and stays
distinct from the tested tag; #9 retains exact-head coverage for later skipped
commits. At tag closeout the [#193 reconstruction contract](archive/native_feature_reconstruction.md)
was queued for 0.6.0; its later source/owned receiving remains separate from this
0.5.0 tag. #192 owns the independent test-isolation improvement. #95 remains the
intermediate-milestone umbrella; only its 0.5.0 source-cut event is completed.
The [closeout receipt](evidence/release_050_closeout_20261111.json) receives the
later documentation/reporting checks without extending the tag's source result.
The delivery rules below retain the reviewed pre-tag contract.

## Delivery and candidate

Deliver one immutable annotated Git tag named exactly `0.5.0` after the required
source checks pass. The maintainer selected **source tag only**: no GitHub Release,
package upload/promotion or hosted documentation publication. The next development
series is 0.6.0. Native feature reconstruction and new capabilities do not expand
this cut while it is being qualified.

The review starts at `5fba1c8792a83f26fd81be5547d020fd217f15c9`, 231 commits after
0.4.0 (`60b21b7d183217d50c29ea3e6bc0d05fb5b797a2`). The
[static source review](evidence/release_050_source_review_20261111.json) records
1,932 changed paths, 76 changed runtime Python paths and eight changed declared
existing argument signatures in its explicit scope. No removed declaration was
found. The later #191 preparation repair changes only unit bootstrap and is
received separately in the [preparation receipt](evidence/release_050_preparation_20261111.json). Added declaration counts include implementation-owned definitions and
are not a count of independent public APIs. Neither these counts nor historical
selected test totals establish candidate readiness.

The final preparation commit is the candidate. Record its complete SHA under
#95 and #9 before requesting exact-head workflows. Tag that same tested commit;
do not add another source commit between its qualification and tagging. Terminal
run evidence and the annotation are the pre-tag receipt. A later evidence-only
main commit may archive those results without moving the tag or relabelling the
tested source. No candidate is accepted merely by creating this document.

## Included implemented scope

| Boundary | Included source and owning contract |
| --- | --- |
| Native modeling, evaluation and validation | Classical prepared-input workflows, explicit cached receptor profiles, any-of/essential/exclusion semantics, independent model composition, physical quantities and original-cohort metrics. Preserve the bounded scientific contracts and [earlier migration review](release_0_5_0_post_review.md). |
| Prepared screening | Public `PreparedInput`, `screen_prepared`, plan/create/open/resume and separate friendly/expert run ownership. See [incremental screening](public_prepared_screening.md) and [recoverable runs](public_prepared_runs.md). |
| Saved results | Independent `pharmacophoremt_results` reading/CLI, original work/source identities, progress, selection/detail, protected JSONL/CSV exports and original/common-cohort run summaries/comparison. See [saved-run analysis](saved_run_analysis.md). |
| Saved feature evidence | Public `pharmacophoremt_features.FeatureAssetView`, pinned declared-metadata inspection, complete page counts and exact opaque originals; [format and limits](feature_archive_format.md). Explicit unshipped study export preserves old evidence. |
| Interchange | Qualified native JSON/YAML admission plus explicit RDKit and Pharmer point interchange, loss reports and preserved mappings. See [RDKit](../docs/content/user/rdkit_interoperability.md) and [Pharmer](../docs/content/user/pharmer_interoperability.md). |
| Numerical corrections | Conservative essential-triplet candidate roundoff and rigid pair-distance association correction; final physical matching remains authoritative. See [pair-distance receiving](pair_distance_pruning.md). |
| Evidence and developer delivery | Original analytical inputs/results, attribution, public-library/tool registries, guided/expert technical exercises, resource-limited measurements, private installed-test staging and executable documentation. These retain their own scope rather than becoming new biological or scale claims. |

## Compatibility and migration

The [release notes](../docs/content/about/release_notes.md) retain earlier native
ranking, merge, I/O and argument changes. This later review adds:

- RDKit conversion now exposes explicit point/feature representation, radius and
  loss/report options; Pharmer reading exposes loss/report policy. Interchange
  is a documented projection, not complete query/constraint equivalence.
- Saved reading, export and cohort comparison remain separate from scientific
  resumption. Conservative exact software bindings may require a new linked run
  after a code/version change; a readable historical run is not an execution
  compatibility certificate.
- Work/source/occurrence keys are literal. Global ordinals, incomplete causes,
  zero negatives and unscored failures retain their different meanings. Empty
  pages or an unobserved feature family do not establish a negative result.
- The feature reader accepts its public metadata archive, not raw study stores.
  Original payloads remain opaque and producer counts remain declarations;
  quantity/geometry validation, molecular authentication and query admission are
  separate. No public native decoder/writer is present in this cut.
- Earlier source/generated/wheel/provider versions stay original in saved data.
  No retrospective migration or attribution enrichment is performed at tagging.

[#191](archive/preloaded_pint_bootstrap.md) additionally preserves an already
loaded Pint registry/cache when the application has not selected standard units.
The newly published canonical guide is synchronized through its owning tool;
this adopts its bootstrap guidance, not a new numerical conversion provider.

Direct dependency names and minima remain the reviewed current metadata:
ArgDigest >=0.17.1, SMonitor >=0.22.1 and PyYAML >=5.1 among the existing runtime
requirements. Controlled source qualification retains exact declared provider
pins. The provisional QuantityRecord used by unshipped studies does not become a
new public native feature-codec minimum. No sibling, shared prefix or source pin
is changed solely to make a release check appear green.

## Required source-cut checks

| Check | Acceptance and evidence owner |
| --- | --- |
| Local preparation | Ruff/format, report/archive/index controls, dependency/environment/resource inventory, complete administrative distribution selection, scope/migration review and strict documentation with notebook execution off. |
| Exact hosted source | All eight full Linux/macOS arm64 Python 3.11–3.14 scientific cells and reporting governance at the same candidate. Inspect actual native job/step results, counts, skips and coverage; #9 owns recovery. |
| Exact conformance | Frozen policy-v1.5.4 and publication-governance workflows execute successfully for the candidate. Current guide/instruction applicability remains a separate audit; no caller pin is silently upgraded. |
| Coverage | Three core/reader roots, qualified same-basename file identities and unexecuted files. [#190](archive/feature_archive_coverage.md) receives the missing feature-reader root; actual hosted XML remains candidate-owned. |
| Version and trigger safety | Canonical dynamic tag parser, absent remote 0.5.0, source tag matching candidate, and a private tagged build/metadata probe. Tag push triggers conformance only; existing package/docs workflows require a separate Release/dispatch event. |
| Publication decision and closeout | A reviewed #95 receipt before the tag push; verify the remote tag target and actual tag conformance afterward. Send the required source-only version notice to MolSysSuite. Never move an existing tag or infer package availability. |

The prospective Conda plan now names 0.5.0 to keep its intended identity explicit,
but remains staged, `dependencies_public=false` and installed-gated. Updating
that declaration builds/publishes nothing and does not qualify a package. The
source-only decision does not waive a failed source/scientific gate.

## Separate pending work and 0.6.0

Package build/promotion, complete public dependency closure, exact installed
platform/minor qualification and fresh public installation remain #10/#23-owned
and are **not delivered by this source-only tag**. The public 0.4.0 package keeps
its original identity and installation instructions. Historical local owned
wheels are evidence of their exact producers, not public 0.5.0 artifacts.

Future work includes native reconstruction with accepted original formats,
expected-generation and quantity validation; public feature writing/recovery;
MolSysMT#624 molecular collections; persisted lookup/index size, native/cold/scale
costs; and broader retrospective/receptor validation. Representative human
usability, live viewer, biological prediction and performance qualification keep
their owning issues. #148/#165 remain stopped under their original resource
limitations. None is silently completed or added as a new source-tag feature.
