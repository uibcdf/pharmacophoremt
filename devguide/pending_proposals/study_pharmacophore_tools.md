---
summary: Establish a pharmacophore-tool registry and an evidence-based comparison protocol.
issue: uibcdf/pharmacophoremt#128
status: active
opened: 2026-11-06
closed:
verification: measured
area: [science, design, usability]
guard:
normative: devguide/pharmacophore_tools_registry.md
blocked_by: []
supersedes: []
---

# Pharmacophore-tool study and comparison registry

## What and why

The maintainer requests a dedicated Discussions area for tools to study, compare
against and learn from. This complements #108's library workflow and the
[comparative survey](../pharmacophore_library_workflow_survey.md). The accepted
product targets are powerful capabilities with scientific/performance evidence,
an intuitive guided route and a complete coherent expert public API. Careful
design and quality take precedence over delivery speed.

## How

Maintain an index and canonical source-specific records under the
[registry guidance](../pharmacophore_tools_registry.md). Distinguish toolkits,
engines, hosted services and integrated applications. Each record names role,
source/version scope, evidence level, lessons, comparison questions, access/license
limits, related work and dated dispositions.

Initial records cover Pharmit, Pharmer, CDPKit, LigandScout/XT, Phase, RDKit
Pharm3D, historical OpenPharmacophore, Align-it/Pharao, Discovery Studio/Catalyst
and MOE. A documentation/source comparison is distinct from local execution,
a reproduced benchmark or demonstrated equivalence of scientific answers.

Concrete implementation/benchmark work goes to an owning issue linked both ways.
Maintain accepted/deferred/non-selected decisions with date, reason and observable
revisit conditions. The registry is not a queue bypass or an accepted dependency
list. Molecular identity, formats, preparation, chemistry and reusable geometry
remain MolSysMT-owned; PHMT owns pharmacophore semantics, orchestration/results
and interpretation.

## What is inspected and what remains

The survey reviews primary documentation/source and original publications across
nine ecosystems; Pharmit and Pharmer have separate registry records because they
have different responsibilities. At that original survey no competitor was
executed or benchmarked, and no new PHMT API/index, preparation or score followed.
Versioned historical evidence and current product claims retain distinct scope.

The [declared Pharm3D comparison](../rdkit_bounds_comparison.md) now receives
ten analytical cases/186 exhaustive assignments on installed RDKit2026.09.2,
with106 selected local cases and the separate complete driver passing. Interior
filter equality, proper-fit reflection rejection and exact-boundary divergence
retain their actual scope; nine other tool records remain documentary. Original
resource/harness failures and the prospective data-budget amendment are preserved.
[#140](../archive/qualify_rdkit_projection.md) owns public projection/constraint fidelity.
This does not close the broad comparison registry or biological/performance gates.

## CDPKit source follow-up — 2026-11-08

The [update/identity review](../cdpkit_library_update_review.md) binds ten raw
Git blobs to exact v1.3.0/a8c7985 and authenticates their bytes. Selected source
paths refine duplicate/replacement, conformer, failure/publication, imported versus
searchable and merged-feature compatibility questions. Nine declared acceptance
cases remain unexecuted. Findings and proposed owner-specific requirements go
to #108/MolSysMT#624 and canonical Discussion#132; publication receiving remains
separate from toolkit execution, biological or performance evidence. No engine
adoption or runtime change closes this broad registry.

## Acceptance criteria

1. Observe the dedicated category without changing other categories/history.
2. Publish the index and ten initial tool records with primary sources, explicit
   evidence boundaries, comparison questions and stable links.
3. Deliver the friendly intake template through the authorized direct route and record actual
   default-branch/rendering state; retain the usable interim text template.
4. Maintain the comparison survey and owner/disposition protocol. A future
   executed comparison declares scientific problem, versions, prepared inputs,
   feature/query semantics, stopping rules, denominators and resources first.
5. Verify links and relevant reporting/documentation checks. Keep unexecuted
   performance, scientific and software-adoption claims explicit.

Registry publication does not require running every listed product and does not
qualify a public provider workflow, complete #103 or accept an engine dependency.
