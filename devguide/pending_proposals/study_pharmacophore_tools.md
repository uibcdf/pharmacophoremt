---
summary: Establish a pharmacophore-tool registry and an evidence-based comparison protocol.
issue: uibcdf/pharmacophoremt#128
status: active
opened: 2026-11-06
closed:
verification: inspected
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
have different responsibilities. No competitor has been installed, executed or
benchmarked, and no new PHMT API/index, molecular preparation or score follows.
Versioned historical evidence and current product claims retain distinct scope.

## Acceptance criteria

1. Observe the dedicated category without changing other categories/history.
2. Publish the index and ten initial tool records with primary sources, explicit
   evidence boundaries, comparison questions and stable links.
3. Deliver the friendly intake template through normal review and record actual
   default-branch/rendering state; retain the usable interim text template.
4. Maintain the comparison survey and owner/disposition protocol. A future
   executed comparison declares scientific problem, versions, prepared inputs,
   feature/query semantics, stopping rules, denominators and resources first.
5. Verify links and relevant reporting/documentation checks. Keep unexecuted
   performance, scientific and software-adoption claims explicit.

Registry publication does not require running every listed product and does not
qualify a public provider workflow, complete #103 or accept an engine dependency.
