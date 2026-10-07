---
summary: Decide how to collect and publish scientific validation and benchmark evidence.
issue: uibcdf/pharmacophoremt#20
status: resolved
opened: 2026-10-02
closed: 2026-10-07
verification: measured
area: [documentation, validation, benchmarks]
guard: tests/test_evidence_archive.py
normative: devguide/validation_collection.md
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

## Reviewed decision and demonstrator — 2026-10-07

The options and future-state descriptions above are historical. The maintained
[collection decision](../validation_collection.md) selects a Validation and
benchmarks section in the existing library documentation as the first view of
the original evidence collection. A dedicated website is deferred; a later view
must consume the same immutable records. Inputs, drivers, scientific guards,
results and recipes retain their owning source locations.

The decision compares the three options, defines the five evidence classes,
names PHMT maintainer ownership and review/update triggers, separates cheap
archive CI checks from opt-in science/performance execution and preserves shared
pilot/MOLI/suite ownership. The [case template](../templates/evidence_case.md)
records data/license/preparation, versions/source overlays, explicit units,
oracles, counts/failures, leakage/uncertainty, search limits and benchmark scope.
Root documentation navigation now includes the new collection section.

The [prepared CCD EST/DES demonstrator](../../docs/content/validation/prepared_ccd.md)
links frozen SDFs/manifest, public MolSysMT preparation, the existing executable
driver, the actual historical environment, all 12 original count comparisons
and portable actual Ackredit references. Both documentation Python blocks
execute; a fresh detached bibliography reader preserves the enclosing session.
The archive's dirty producer overlay is explicit: its Git head alone is not
claimed to reconstruct the original scientific environment. The original driver
is documented for fresh measurements; no new scientific run, biological result
or performance benchmark is claimed by this publication decision.

`devtools.evidence_archive.read_archived_evidence()` is an independently usable
standard-library operation for the existing checksum-qualified gzip/JSON
envelope. It preserves failed/unknown fields and verifies both byte identities,
optional sizes and sibling paths without provider imports or stored execution.
Nine guards cover corruption, repacked altered output, identities/sizes, paths,
historical spelling, unchanged files, original CCD inputs/counts/references and
CLI use without site packages. CI invokes these in the existing reporting job.

The focused archive/CI selection passes **16 tests**, the integrated shared
SDK's distribution/environment selection **23 tests**, and the reporting
protocol **3 tests** on Python 3.14.7. Declaration and generated-environment
checks pass against the SDK adopted by concurrent commit `448e47e`;
its workflow identity is updated for the single added local archive command.
Strict isolated Sphinx rendering of the new pages passes. Original compressed
records are preserved; the [review receipt](../evidence/validation_collection_review_py314.json)
retains their hashes and the bounded verification scope. Ruff and generated
indexes pass. Complete website/hosted/installed/public qualification remains
separate under #9/#23; MolSysMT code and its environmental-H blocker are untouched.
