---
summary: Identify installed distribution metadata from the independent reader CLI.
issue: uibcdf/pharmacophoremt#173
status: open
opened: 2026-11-10
closed:
verification: asserted
area: [results, usability]
guard:
normative:
blocked_by: []
supersedes: []
---

# Reader distribution version

## What and why

Add conventional `--version` so a user preparing a saved-inspection exercise can
identify the installed PharmacophoreMT distribution without providing a run,
score criterion or scientific provider context. Clearly label distribution
metadata; it does not identify current editable/source bodies or qualify them.

## How and ownership

A private CLI argparse action reads stdlib `importlib.metadata.version` lazily
for the exact `pharmacophoremt` distribution. Missing/invalid metadata is an
explicit parser error with no success stdout. Do not import the scientific host,
its generated version module or a new provider. Help and ordinary operations
must not add a metadata request. This is CLI presentation, with no public library
signature/argument, quantity, optional-engine or attribution boundary.

## What is measured and what is assumed

The [prospective plan](../evidence/reader_version_plan_20261110.json) freezes five
independent controls plus134existing reader bodies, thirteen ordinary stdout-byte
controls, fresh process guards and exact owned same-body receiving. The [source receipt](../evidence/reader_version_source_20261110.json) receives
139cases, thirteen original stdout-byte controls, strict docs and25distribution/
local reporting checks. Original red controls retain4failures/1pass. Exact owned
receiving remains pending; af408e7 full-source acceptance is separate.

## Alternatives and limits

Do not invent a source version, import scientific `pharmacophoremt` just to read
its version, add a runtime versioning provider or silently use another package's
metadata. Installed metadata alone cannot certify feature/body compatibility.
No runtime path/schema/index/connector, provider floor or scientific operation.
#148/#165remain stopped; full public/platform/release gates remain independent.

## Acceptance criteria

Ledger-free labeled exact version, missing/invalid refusal, lazy ordinary/help
behavior and fresh scientific-import exclusion; same139bodies in source and one
owned artifact with real wheel/version agreement, ordinary exact output bytes,
strict docs and relevant distribution/reporting checks.
