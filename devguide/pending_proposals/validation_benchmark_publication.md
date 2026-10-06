---
summary: Decide how to collect and publish scientific validation and benchmark evidence.
issue: uibcdf/pharmacophoremt#20
status: open
opened: 2026-10-02
closed:
verification: asserted
area: [documentation, validation, benchmarks]
guard:
normative:
blocked_by: []
supersedes: []
---

# Validation and benchmark publication strategy

## What

Decide whether to maintain a **Validation and benchmarks** documentation section,
a dedicated website, or a common evidence collection published through both.
Collect strategies, cases, executable examples and notebooks without duplicating
their source of truth across the cookbook, developer guide and publication site.

## How

Compare the publication options by discoverability, reproducibility, versioning,
maintenance cost, contribution/review workflow and execution infrastructure.
Define an evidence template covering data provenance/licenses, molecular
preparation through MolSysMT, chemical states/units, method parameters,
software/source/environment versions, seeds, execution commands and Ackredit
references for reached methods and software.

Separate analytical controls, independent scientific validation, retrospective
screening, vertical workflow pilots and computational performance benchmarks.
Record scientific splits/leakage controls, ligand-level counts, failures,
uncertainty and incomplete search. Performance cases require comparable
scientific outputs, hardware/thread/GPU settings, initialization/compilation,
memory/runtime and repeat variability.

Define lightweight CI controls, larger optional executions, result history and
ownership/update policy. Coordinate shared workflow evidence with
`moli-vertical-pilots`, MOLI and MolSysSuite; keep local method/product work here.
Issues #18 and #19 supply consensus and attribution context.

## Why

Users need evidence they can inspect and rerun. Notebook availability alone
does not establish scientific validity, and a fast implementation must still
satisfy the same scientific contract. A publication decision should precede
building a new website or moving evidence into multiple competing collections.

## What is measured and what is assumed

This records a user-requested future decision, not an implemented publication
system or benchmark result. Existing native analytical tests/cookbook examples
are possible seed cases, not biological or performance acceptance evidence.

## Alternatives and refuted paths

All three publication options remain open. Avoid choosing a site first and
leaving datasets, execution, reference outputs and maintenance undefined.

## Scope and exclusions

Choose the evidence/publication model and prove it with one demonstrator.
No website, dataset acquisition, new biological validation or performance claim
is implemented by this proposal.

## Acceptance criteria

A reviewed layout/publication decision, a minimal evidence template, named
owners and execution/update policy, and one case linking executable code,
data/environment, measured results and citations.
