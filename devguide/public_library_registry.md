# Chemical-library registry

Maintained 2026-11-06; accountable triage owners: PharmacophoreMT maintainers
LMMV/dprada. The user requested this dedicated public repository of candidate
libraries, assessments, requirements and reasons why incorporation remains pending.

## Public entry points and durable destination

- [Chemical libraries category](https://github.com/uibcdf/pharmacophoremt/discussions/categories/chemical-libraries).
- [Registry index and contribution guide](https://github.com/uibcdf/pharmacophoremt/discussions/109).
- [Product issue #108](https://github.com/uibcdf/pharmacophoremt/issues/108) and
  [local implementation proposal](pending_proposals/qualify_public_library_workflow.md).
- [Primary-source research](public_library_support_research.md).
- [Intake form](../.github/DISCUSSION_TEMPLATE/chemical-libraries.yml).

The separate [Pharmacophore tools registry](pharmacophore_tools_registry.md) and
[public study index](https://github.com/uibcdf/pharmacophoremt/discussions/129)
record software to study/compare, with evidence levels and open questions. The
[workflow survey](pharmacophore_library_workflow_survey.md) informs #108's design;
tool-study ownership is #128, not a new chemical-library provider entry.

This purposeful local category extends Announcements, Q&A and Ideas without
replacing them. Its open-ended format supports early proposals and source-specific
assessment. The maintainers own triage until explicitly delegated; there is no
response-time promise. Concrete missing capabilities and implementation work go
to owning issues, with discussion/issue links in both directions. Product decisions
belong in #108 or another named versioned record; scientific source admission
remains in #103/#66/#106 and the validation collection.

## Record structure and disposition

A resource record carries scientific use/value, decision status/date, proposed
priority, official access/terms/version/identifier/format evidence, preparation
requirements, current limitations, an observable revisit trigger, owner and durable
issue/evidence links. Preserve dated earlier assessments when adding a correction.

Decision status is distinct from priority and operation coverage:

| Status | Evidence required |
| --- | --- |
| Candidate | A proposed resource and scientific use; assessment has not started. |
| Under review | An assessment is underway, with unresolved requirements explicit. |
| Planned | An owning issue accepts a bounded implementation scope. |
| In progress | A linked issue records actual implementation/qualification work. |
| Partial | Named operations work with documented remaining limitations. |
| Qualified | Reproducible evidence names actual operations, versions, environment and limits. |
| Deferred | A dated reason and concrete revisit condition are recorded. |
| Not selected | A dated decision explains unsuitable scope and what could change it. |

Assess discovery, acquisition, authorized local import, molecular preparation,
pharmacophore screening and availability lookup individually. Listing a provider,
a file format or an API does not establish a functioning PHMT integration.

New proposals use the category form: resource name/official URL, scientific use
and value, known formats/access/terms, preparation limitations and related links.
Unknown technical details are acceptable; contributors need not decide support
status or priority. Until the form is published and its rendering observed, the
same fields in the public index provide the interim text template. Do not claim
that local YAML validation proves a live GitHub form.

Triage reuses the existing resource thread, links duplicates without deleting
history, and moves concrete work to an owning issue. Summarize any accepted,
deferred or rejected disposition in both destinations with date, reason and an
observable revisit trigger. Discussion votes/closure do not accept a contract or
prove implementation. Keep licensed payloads, credentials and private evidence
out of public threads.

## Initial assessments — 2026-11-06

All priorities remain proposals. No provider is newly qualified. No resource has
been rejected outright. DrugBank's automatic-acquisition route is deferred under
the observed download pause; applicable authorized local-file compatibility is
still assessable. Enamine retains an explicit applicable-agreement/access question.

| Resource thread | Proposed priority | Disposition |
| --- | --- | --- |
| [ZINC-22 / ZINC20](https://github.com/uibcdf/pharmacophoremt/discussions/110) | Core | Under review |
| [PubChem / PubChem3D](https://github.com/uibcdf/pharmacophoremt/discussions/111) | Core | Under review |
| [Enamine Stock / REAL](https://github.com/uibcdf/pharmacophoremt/discussions/112) | High, access-dependent | Under review |
| [ChEMBL](https://github.com/uibcdf/pharmacophoremt/discussions/113) | Core | Under review |
| [BindingDB](https://github.com/uibcdf/pharmacophoremt/discussions/114) | Core | Under review |
| [DrugCentral](https://github.com/uibcdf/pharmacophoremt/discussions/115) | High; first small drug-set candidate | Under review |
| [Broad Drug Repurposing Hub](https://github.com/uibcdf/pharmacophoremt/discussions/116) | High | Under review |
| [NCI / DTP / NExT collections](https://github.com/uibcdf/pharmacophoremt/discussions/117) | Extension | Under review |
| [COCONUT](https://github.com/uibcdf/pharmacophoremt/discussions/118) | High; first natural-product candidate | Under review |
| [LOTUS](https://github.com/uibcdf/pharmacophoremt/discussions/119) | Extension | Under review |
| [DrugBank](https://github.com/uibcdf/pharmacophoremt/discussions/120) | Conditional extension | Deferred: automatic acquisition |
| [Mcule](https://github.com/uibcdf/pharmacophoremt/discussions/121) | Extension | Under review |
| [MolPort](https://github.com/uibcdf/pharmacophoremt/discussions/122) | Extension | Under review |
| [Chemspace](https://github.com/uibcdf/pharmacophoremt/discussions/123) | Extension | Under review |
| [eMolecules](https://github.com/uibcdf/pharmacophoremt/discussions/124) | Extension | Under review |
| [LIT-PCBA](https://github.com/uibcdf/pharmacophoremt/discussions/125) | First benchmark candidate | Under review |
| [DUD-E](https://github.com/uibcdf/pharmacophoremt/discussions/126) | Optional benchmark compatibility | Under review |

## Observed launch and remaining evidence

The user created Chemical libraries; API readback observes category ID
`DIC_kwDOP5ch7M4DKjiI`, slug `chemical-libraries`, matching description and
`isAnswerable=false`. Announcements, Ideas and Q&A remain present; Q&A remains
answerable. The requested format is Open-ended discussion; this API readback
cannot independently distinguish it from every non-answerable format. No other
category or existing conversation was edited or deleted.

The index and 17 resource threads were published through supported GraphQL
Discussion operations. Own publication requests/responses remain in the bounded
local capsule `build/phmt-library-discussions-20261106-klzq7bv0`; source-specific
official citations are in each public thread. The product issue records current
dispositions and revisit conditions. Final remote-body and link readback is
recorded in that capsule; publication evidence is not scientific validation.

The intake YAML is prepared locally; source publication, default-branch adoption
and actual form rendering retain their separate observed states. Record its
review route in #108 rather than silently claiming a live form. The text fields
in the public index provide a usable interim proposal route.

Molecular collections/preparation remain MolSysMT-owned. This launch downloads
no chemical dataset, generates no states/conformers, runs no new model/score and
certifies no library integration. The research note's new #108/registry links are
navigation updates after its earlier dated evidence hash; earlier closeout hashes
continue identifying their original bytes, not this maintained revision.
