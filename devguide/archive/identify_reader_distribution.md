---
summary: Identify installed distribution metadata from the independent reader CLI.
issue: uibcdf/pharmacophoremt#173
status: resolved
opened: 2026-11-10
closed: 2026-11-10
verification: measured
area: [results, usability]
guard: tests/test_public_reader_version.py
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
local reporting checks. Original red controls retain4failures/1pass. The [installed receipt](../evidence/reader_version_installed_20261110.json)
receives the same139bodies from source bc084f9 / owned214,159guarded children,
24documented commands on four historical stores, thirteen ordinary source-byte
controls and an actual metadata response equal to the exact wheel version.
All214payloads/159runtime identities and seven loaded reader origins verify.
The af408e7 full-source acceptance remains separate.

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

## Received 2026-11-10 UTC

Five independent new bodies plus134existing bodies pass from source and the
same exact owned artifact. Original red controls retain4failures/1pass; one
initial mistyped capsule path refuses before collecting any test and is retained
separately. The private version action and its one parser registration are the
only changes to the original API AST; existing public signatures/bodies remain
unchanged. Actual owned CLI metadata is0.4.0+214.gbc084f9, agreeing with its wheel.
Help and normal operations add no version request; missing/invalid metadata fails
with empty success stdout. No scientific namespace is imported.

All159guarded children retain127expected exit0/32expected exit2results. The
24historical commands and thirteen ordinary outputs preserve original file/
source bytes. Strict full docs,25distribution, declared routes/generated
environments, Ruff and reporting/archive checks pass. The raw archive retains
controls, original failures and exact observations. Reader peaks are about
109/125MiB under unchanged serial DATA512MiB/AS1GiB/observed-group512MiB controls;
docs uses its separately declared DATA512MiB/AS-unlimited/observed-group1GiB
route. Capacity is not reserved and no kernel aggregate enforcement is claimed.

The bounded CLI/version bridge resolves. Installed distribution metadata is
explicitly distinct from source-body/current feature qualification. Later-head
full source, complete public/installed-platform, actual human usability,
scientific prediction, scale/performance and release gates remain separate.
