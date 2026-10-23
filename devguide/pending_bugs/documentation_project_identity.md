---
summary: Remove inherited project identity from public PharmacophoreMT documentation.
issue: uibcdf/pharmacophoremt#4
status: partial
opened: 2026-09-20
closed:
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
