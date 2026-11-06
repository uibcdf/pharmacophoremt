# Pharmacophore-tool study registry

Maintained 2026-11-06; accountable owners: PharmacophoreMT maintainers LMMV/dprada.
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
tool. Until default-branch form adoption and live rendering are observed, the
index provides the same usable text fields. Local YAML checks alone do not prove
a live GitHub form. Record its review/adoption state in #128 and PR #127.

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

The automatic form is prepared for the registry-source PR #127. Default-branch
adoption, live rendering, software execution, scientific comparisons and measured
large-library performance retain separate pending states. The text template and
public study records are usable independently of form adoption.
