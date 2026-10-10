---
summary: Repair the strict whole-site build and unrelated software identity claims.
issue: uibcdf/pharmacophoremt#53
status: resolved
opened: 2026-10-10
closed: 2026-10-10
severity: medium
verification: measured
area: [documentation, compatibility, attribution]
guard: devtools/tests/test_documentation_build.py::test_full_documentation_build_without_warnings
normative: MOLSYSSUITE_GUIDE.md
blocked_by: []
supersedes: []
---

# Ordinary whole-site documentation repair

## What

The full Sphinx build of `2a800f5` in an actual ordinary public-dependency docs
environment fails with nine warnings. Its citation page and landing page also
advertise an unrelated PocketMT DOI; the landing page has stale Python/release
badges and an unqualified public Conda installation command.

## How

Add the missing API navigation page and prepared ERalpha cookbook entry, put the
landing notebook's headings under an H1, and link source-only publication controls
to their immutable GitHub document. Replace the PocketMT citation with exact
PharmacophoreMT software identity and actual-calculation attribution guidance.
Remove the stale landing badges and point installation/citation to the maintained
pages. The notebook's code, outputs and metadata retain their original values.

## Why

Users need working documentation and accurate installation/citation information.
A rendered page, external project's DOI or configured publisher cannot establish
PharmacophoreMT public delivery or archival.

## What is measured and what is assumed

The original full strict CLI build fails in Linux x86_64/Python 3.12.15 with
public Sphinx 9.1.0. The corrected full site passes in that same ordinary
environment. The durable test executes a clean full Sphinx build with warnings
as errors: it fails against the original source and passes against the correction
in the ordinary development Python 3.14.8 environment. Missing Sphinx is an error
in this explicitly selected gate; the independent administrative unittest lane
does not execute this Pytest-only documentation gate.

Original evidence, scripts, environment/archive identities and before/after logs
are retained through `devguide/evidence/ordinary_environment_review_20261010_summary.json`.
Notebook execution is disabled by the unchanged configuration. This is a local
build, not Pages deployment or full scientific/public-package qualification.

## Alternatives and refuted paths

Suppressing Sphinx warnings would conceal broken navigation and references.
Another project's DOI cannot supply PharmacophoreMT archival evidence. An isolated
two-page render cannot substitute for this complete-site build.

## Scope and exclusions

Documentation and its explicit verification gate. No molecular preparation,
provider implementation, public release, archived scientific data or shared
environment/tool policy is changed. #10/#23 retain installed/public acceptance.

## Acceptance criteria

The full strict site build succeeds; API/cookbook routes are reachable; software
identity and installation guidance do not claim the unrelated release. The guard
protects actual extension loading, toctrees, references and heading validity.
