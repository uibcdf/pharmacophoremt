# Pharmacophore-tool study registry

Maintained 2026-11-09; accountable owners: PharmacophoreMT maintainers LMMV/dprada.
The maintainer requests this separate registry for tools to study, compare against
and learn from. It covers scientific methods, workflows, public APIs, performance
engineering and usability. It complements the chemical-library registry.

## Entry points and durable authority

- [Pharmacophore tools category](https://github.com/uibcdf/pharmacophoremt/discussions/categories/pharmacophore-tools).
- [Index and comparison guide](https://github.com/uibcdf/pharmacophoremt/discussions/129).
- [Owning issue #128](https://github.com/uibcdf/pharmacophoremt/issues/128) and
  [local proposal](pending_proposals/study_pharmacophore_tools.md).
- [Comparative library-workflow survey](pharmacophore_library_workflow_survey.md),
  [product vision](vision_and_scope.md), [public API standards](api_design_standards.md).
- [Tool intake form](../.github/DISCUSSION_TEMPLATE/pharmacophore-tools.yml).
- [Chemical libraries index](https://github.com/uibcdf/pharmacophoremt/discussions/109)
  and [#108 workflow](pending_proposals/qualify_public_library_workflow.md).

The category is a purposeful local extension with an open-ended study/intake
purpose. Existing Announcements, Ideas, Q&A and Chemical libraries retain their
roles/history. Maintainers own triage until explicitly delegated; there is no
response-time promise. A thread is not an implementation queue or accepted
engine/dependency list. Concrete work goes to owning issues with links both ways.

## What each record contains

Name/role, official sources, version/evidence scope, why study it, documented
workflow, lessons, comparison questions, actual evidence/access/license limits,
owner, related issues and dated dispositions. Use one canonical record per tool
or clearly scoped family; retain historical version observations within the record.
Pharmit and Pharmer have separate records for service/workflow and search-engine
responsibilities. Do not collapse a toolkit and complete screening product into
one undifferentiated capability comparison.

| Study disposition | Required meaning |
| --- | --- |
| Candidate | Proposed resource and scientific/design reason to examine it. |
| Under study | Documentation, implementation or scientific assumptions are being examined. |
| Comparison planned | An owning issue declares the bounded question and comparison plan. |
| Comparison recorded | Dated conclusions identify documentary or executed scope and evidence. |
| Deferred | Date, reason, responsible owner and observable revisit condition. |
| Not selected for this study | Dated reason, current scope and what could change the decision. |

Record evidence level separately: documentation/source inspection, local
execution, or a reproduced declared comparison/benchmark. Similar names, product
claims and documentation do not establish scientific or performance equivalence.
Even a reproduced timing requires its inputs, coverage, environment and budget
before it supports a design decision.

## Intake and disposition

The friendly category form asks for name/official source, role, why study it,
known version/access/license/documents, comparison questions and related links.
Unknown details are welcome, and no local test/benchmark is required to suggest a
tool. Form source is maintained in this repository; default-branch delivery and
live rendering are separate observations. Until rendering is verified, the index
provides the same usable text fields. Local YAML checks alone do not prove a live
GitHub form. Record actual delivery/rendering in #128.

Search/reuse the canonical tool thread, link duplicates and preserve discussion
history. Concrete implementations or executed benchmark proposals use owning
issues, linked both ways. Record conclusions and accepted/deferred/non-selected
decisions in #128 or a named versioned record with date, reason and revisit
condition, then summarize/link the destination in the tool thread. Keep credentials,
private evidence and licensed payloads out of public discussions.

## Initial tool records — 2026-11-06

All ten records are Under study with documentary/source evidence. No competitor
was installed, executed or benchmarked, and no tool is accepted as a dependency.
Historical documentation and current product descriptions remain distinguished.

| Tool/family | Public record |
| --- | --- |
| Pharmit | [Study, lessons and questions](https://github.com/uibcdf/pharmacophoremt/discussions/130) |
| Pharmer | [Study, lessons and questions](https://github.com/uibcdf/pharmacophoremt/discussions/131) |
| CDPKit | [Study, lessons and questions](https://github.com/uibcdf/pharmacophoremt/discussions/132) |
| LigandScout / LigandScout XT | [Study, lessons and questions](https://github.com/uibcdf/pharmacophoremt/discussions/133) |
| Schrödinger Phase | [Study, lessons and questions](https://github.com/uibcdf/pharmacophoremt/discussions/134) |
| RDKit Pharm3D | [Study, lessons and questions](https://github.com/uibcdf/pharmacophoremt/discussions/135) |
| OpenPharmacophore — historical implementation | [Study, lessons and questions](https://github.com/uibcdf/pharmacophoremt/discussions/136) |
| Align-it / Pharao family | [Study, lessons and questions](https://github.com/uibcdf/pharmacophoremt/discussions/137) |
| BIOVIA Discovery Studio / Catalyst | [Study, lessons and questions](https://github.com/uibcdf/pharmacophoremt/discussions/138) |
| MOE | [Study, lessons and questions](https://github.com/uibcdf/pharmacophoremt/discussions/139) |

## Useful comparisons and product criteria

The [Pharmer query/pruning review](pharmer_query_pruning_review.md) binds24selected
official standalone files to SourceForge SVN revision95, separately from the2011
paper and current Pharmit integration. It distinguishes retained/disabled/optional
query fields, staged filters, final fit/score, reduced precision, exclusions and
output limits. Twelve proposed comparison cases remain unexecuted. Three separate
stdlib arithmetic controls expose a PHMT predicate mismatch now owned by#160;
they are not competitor or public-native execution. Canonical Discussion#131
publication/readback identities are separately retained under#128. No index,
adapter, engine adoption or timing result follows.

The [CDPKit update/identity review](cdpkit_library_update_review.md) now follows
CREATE/APPEND/UPDATE/merge through exact v1.3.0 source. Ten captured Git blobs
authenticate the selected observations. Replacement/session scope, imported versus
searchable counts, transferred features and per-record transaction boundaries
produce nine explicit follow-up cases and consumer requirements for #108 and
MolSysMT#624. This remains documentary/source evidence: no CDPKit installation,
execution, chemical-equivalence or performance comparison occurred. The other
tool records retain their own evidence levels; no engine is adopted.

The first [executed Pharm3D comparison](rdkit_bounds_comparison.md) is now
recorded separately from the original documentary intake. On installed
RDKit2026.09.2, ten fixed analytical controls evaluate186 assignments: common
interior distance filters agree, the proper-fit stage rejects a noncoplanar
reflection, and exact boundary predicates differ as declared. This is a
reproduced analytical comparison, not a timing benchmark, feature-perception
comparison or acceptance of a production engine. The other nine initial records
retain documentary evidence only. [#140](https://github.com/uibcdf/pharmacophoremt/issues/140)
owns the discovered public projection/constraint-qualification task.

The [public RDKit projection](rdkit_projection.md) now has source/same-owned-wheel receiving for
explicit sphere/radius exchange and detached field/loss/default reports. It
retains complete preflight and the default point target/reader assumptions.
The same214 bodies and exact recipe pass outside the checkout; this adds no broader tool-equivalence,
feature-perception or benchmark claim.

The canonical [RDKit record update](https://github.com/uibcdf/pharmacophoremt/discussions/135#discussioncomment-19463143)
is published with `Comparison recorded` and executed analytical evidence.
Its exact body/identity is independently read back; the original documentary
record and all other threads/categories remain unchanged.

A [dated correction](https://github.com/uibcdf/pharmacophoremt/discussions/135#discussioncomment-19465896)
now preserves the earlier update while receiving the exact-boundary revision.
Original decimal-generated inputs did not define a backend-independent exact
native endpoint. Revision `binary-exact-nm@2` preserves relative geometry/cutoffs,
all eight interior inputs and production predicates. Corrected controls pass
inside frozen8db2a53's eight full source cells,2357tests each. [Independent
readback](evidence/rdkit_record_correction_20261107.json) binds the actual body and
identity. Local186-assignment counts retain their own measurement context; the
other nine tool records remain documentary rather than executed comparisons.

The accepted ambition is powerful pharmacophore work with evidence, an intuitive
guided route, and a complete coherent expert public API, with quality ahead of a
delivery deadline. High-level and composed public routes should resolve to the
same scientific settings; inspectable provenance/results and live molecular handles
have distinct persistence contracts. Use the survey to specify the lifecycle and
alternatives before fixing API names or an indexing strategy.

A declared comparison names the question, exact version/source, molecular
preparation/stereo/state/conformer coverage, feature/query/constraint semantics,
original/evaluated/failed counts, finite budgets, stopping/aggregation policies and
resource context. Study preparation/build/storage separately from cold/warm query
latency, throughput and memory. Report unselective/no-hit cases and incomplete
searches. A fast truncated search is not equivalent to a complete answer, and
geometric or timing evidence is distinct from biological predictive utility.

Learning a workflow does not adopt another tool's code, molecular policy, score
scale or license. MolSysMT owns reusable molecular identity/formats/preparation,
chemistry and geometry. PHMT owns pharmacophore semantics, search artifacts,
orchestration/results and interpretation. Any optional external-engine adapter
requires its own semantics, identity, installation/license and evidence contract.

## Observed publication and pending delivery

The user created the category; API readback observes ID
`DIC_kwDOP5ch7M4DKjnD`, slug `pharmacophore-tools`, the requested description and
`isAnswerable=false`. The requested format is Open-ended discussion; that API flag
alone does not certify every UI-only format setting. Existing category names and
Q&A answerability remain preserved. No prior conversation was moved or deleted.

Index #129 and ten records #130–#139 were published with their primary sources,
questions and links to #128/#108. Exact remote bodies/categories and bidirectional
index links are verified in the owned local publication capsule
`build/phmt-public-library-20261106-0mxdo3ak`. This is administrative/research
publication evidence, not scientific validation.

The principal maintainer explicitly authorizes direct commit/push with routine
`[skip ci]` commits on 2026-11-06. The source follows that route; PR #127 retains
the initial preparation history and is not an approval gate. Default-branch
delivery, live rendering, software execution, scientific comparisons and measured
large-library performance retain separate evidence. The text template and public
records remain usable independently of a rendered form check.


## Subsequent PHMT numerical receiving — 2026-11-09

The original study and its unexecuted comparator cases retain their scope.
[PHMT#160](https://github.com/uibcdf/pharmacophoremt/issues/160) now has a
separate conservative pair-filter correction, independent public guard and
real public-native before/after witness. All116selected source/same-file owned
installed cases pass and twelve ordinary outputs/counters remain unchanged.
See the [numerical contract](pair_distance_pruning.md) and
[installed receipt](evidence/pruning_slack_installed_20261109.json).
This does not execute a competitor, qualify#148or establish biology/scale.


## P1 preparation and PHMT receiving — 2026-11-09

Pharmer disposition for this bounded case: **Comparison planned**. The frozen
[P1contract](pharmer_p1_comparison.md) and
[resolved preparation report](archive/prepare_pharmer_p1.md) define one
all-enabled spherical query, two exact positive mappings and one provably
impossible stretch. The same 29 selected cases and complete three-case PHMT driver
pass from source and unchanged owned wheel192, with nine actual attribution
items / 22 uses each. The
[installed receipt](evidence/pharmer_p1_installed_20261109.json) retains
current provider/mapping identities and the initial stale-metadata refusal.
Pharmer itself remains unexecuted: exact executable, molecular export, perception,
database coverage and search/output admission stay open under#128. This is not an
executed external comparison, benchmark or general interchange claim. The actual
public disabled-point import loss is separately open as#162; P1 uses only enabled
points. Canonical Discussion#131 publication/readback is recorded separately in#128.


## Enabled-point correction received — 2026-11-09

The separately owned [#162 reader correction](pharmer_interoperability.md)
now receives disabled-point omission, strict Boolean admission and original-point
mappings in source/exact owned wheel196. All34same selected cases, two ordinary
profiles and the complete P1driver pass; the bundled original19point JSON has
only10enabled constraints. Earlier P1/source-study claims and receipts retain
their original scope. Broader scientific input/loss policy is separately open
as#163; actual Pharmer execution remains unqualified under#128.


## Supported Pharmer profile received — 2026-11-09

[#163](pharmer_interoperability.md) now qualifies explicit supported
fields/loss reports, preserves enabled omission and honors inactive vectors.
The same141source/exact owned wheel198cases pass (48new/93existing), together
with three unchanged supported ordinary profiles and the complete P1driver.
The [installed receipt](evidence/pharmer_profile_installed_20261109.json)
verifies214payload/159runtime files,12fixtures and155loaded runtime origins,
without PHMT checkout fallback. Original source-study/P1/#162receipts remain
historical; this does not execute Pharmer or qualify its perception, angular
policy, molecular export, database/search behavior or performance.

The next bounded research task is a reproducible executable/build/dependency and
resource admission declaration for the frozen external P1arm under#128. Keep
those oracles and engine-specific meanings explicit before attempting execution.


## External P1 admission prepared — 2026-11-09

[#164](pharmer_p1_external_admission.md) freezes source/build identity,
CLI/resource behavior, native observation limits and three real MolSysMT exports.
Source76ac909 and unchanged owned wheel198 receive the same17case bodies and
complete export driver, with byte-identical original SDFs. The
[installed receipt](evidence/pharmer_p1_external_installed_20261109.json)
verifies214payload/159runtime files,14fixtures and155loaded runtime origins.
The r95 build remains unreceived; the old published binary is not substituted.
One database per source avoids equal-title conformer grouping and multiplied
process/worker counts. Stock output lacks explicit memberships/correspondences;
full native mapping still needs admitted diagnostics. No external engine runs.


## r95 research build stopped — 2026-11-09

[#165](pharmer_r95_build_receiving.md) receives the complete66-file
original source and15fixed private dependency artifacts. A legacy-ABI/selected-SDF
dependency probe passes; it is not Pharmer perception. The serial core build and
one distinct lower-memory collector pilot both reach the unchanged group512MiB
cutoff. No Pharmer executable/help/perception/database/search/native mapping is
executed; comparison disposition remains Under study. Both profiles stop without
budget escalation or shared-prefix/provider changes. Source diagnostics must
observe actual atom/cluster/indexed-feature/correspondence records; that observer
remains unimplemented. Receive a distinct managed build context before another
attempt, while independent PHMT/library/provider work continues.
