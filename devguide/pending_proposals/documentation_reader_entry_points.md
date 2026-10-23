---
summary: Build reader-oriented documentation entry points around delivered native workflows.
issue: uibcdf/pharmacophoremt#61
status: active
opened: 2026-10-23
closed:
verification: measured
area: [documentation, navigation]
guard: devtools/tests/test_documentation_build.py::test_full_documentation_build_without_warnings
normative: docs/README.md
blocked_by: []
supersedes: []
---

# Documentation reader entry points

## What

Use the existing Sphinx/MyST/PyData pattern shared with MolSysMT and MolSysViewer
while providing PharmacophoreMT's own reader routes. The initial user portal only
links to the cookbook; developer/showcase portals are empty, and landing/cookbook
prose still describes public delivery as pending after 0.4.0. Identity itself is #4.

## How

Guide the reader from installation and prepared inputs to a chosen native modeling
route, evaluation/search, persistence and evidence. Reuse existing recipes and
validation pages. Give contributors entry points to the maintained devguide and a
local documentation guide; include that guide in the developer toctree.

## Why

A shared theme is useful only when readers can locate the operations actually
delivered and distinguish examples, measured scientific evidence and future work.

## What is measured and what is assumed

Local link checks and the complete strict Sphinx guard pass. Six rendered entry
pages expose the intended routes and identity. The initial strict attempt caught
the new contributor guide missing from a toctree; adding it fixes the actual
navigation defect without suppressing warnings. Landing-notebook code cells,
outputs, execution state and metadata match the pre-edit baseline. No notebook
or scientific calculation is executed for this narrative slice. Native deployment
and closeout remain pending at this checkpoint.

## Alternatives and refuted paths

Do not copy sibling methods, version badges, DOI or acceptance claims. Do not add
unqualified demonstrations or a viewer feature to fill the showcase. Existing
source-fixture examples remain explicitly distinguished from installed modules.

## Scope and exclusions

Narrative entry pages and contributor guidance, with existing paths and theme.
No new molecular implementation, runtime API, release artifact or browser acceptance.

## Acceptance criteria

Usable landing/user/developer/showcase routes, honest 0.4.0/fixture guidance,
resolving links, warning-free full build, unchanged notebook execution material,
fresh publication and a maintained resumption checkpoint.
