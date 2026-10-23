---
summary: Remove inherited project identity from public PharmacophoreMT documentation.
issue: uibcdf/pharmacophoremt#4
status: resolved
opened: 2026-09-20
closed: 2026-10-23
severity: medium
verification: measured
area: [documentation, identity]
guard:
normative: docs/README.md
blocked_by: []
supersedes: []
---

# Documentation project identity

## What

About pages at inspected source 78580b9 identify the project as PocketMT, link
its repository/license and title the product explanation "What is MolSysMT?".
The installation/citation pages retain defensive references to that other project.
Issue #4 owns removing the inherited identity and deploying the corrected site.

## How

Write the About scope from the delivered native PharmacophoreMT workflows and
its MolSysMT ownership boundary. Correct project/repository/license and authors'
project name, keep verified citation identity and remove stale template comparisons.
The contributor guide explicitly requires component-owned identity and evidence.

## Why

Readers need to identify the installed software and its scientific responsibilities.
Another component's names, DOI or claims cannot supply this project's identity.

## What is measured and what is assumed

The source audit finds no PocketMT identity or incorrect MolSysMT project heading
in maintained documentation text after correction. The complete strict Sphinx
guard passes; rendered entry pages have the intended identity and routes.
No scientific implementation, molecular operation or package artifact changes.
Fresh native publication of the reviewed source is still pending at this checkpoint.

## Alternatives and refuted paths

A global sibling-name replacement would damage valid MolSysMT ownership references.
Another project's DOI must not be copied. Suppressing Sphinx diagnostics does not
repair missing navigation or wrong identity.

## Scope and exclusions

Public documentation identity and deployment. Broader user/developer navigation
is #61; biological/browser acceptance and documentation-badge admission are separate.

## Acceptance criteria

Correct source/rendered identity, retained molecular ownership, complete strict
build, preserved executable notebooks and fresh deployment. Editorial identity
is governed by docs/README.md; the existing full-site guard checks rendering,
references and navigation rather than asserting scientific or editorial truth.

## Completed publication — 2026-10-23

The source checkpoint above preceded publication. Reviewed source
`7aa33cd88806dcde05a01a9416df11d844cb9b62` now passes native Documentation
40011094526, policy 40011098877, Conda governance 40011103894 and administrative
CI probe 40011110286. The probe intentionally omits scientific execution.
Immutable gh-pages commit `c869f6ed18a4dc8ee510efea4d5cf979e8cc0ef0` supplies
six verified rendered entry pages with the corrected identity/routes; Pages API
reports the site built from gh-pages. See the [local strict/render receipt](../evidence/documentation_foundations_20261023.json)
and [native publication receipt](../evidence/documentation_publication_20261023.json).
Notebook code, outputs and metadata remain unchanged; runtime code and molecular
inputs are untouched. These checks establish the documentation slice and deployment,
not new scientific, installed-package, visual/browser or badge acceptance.
