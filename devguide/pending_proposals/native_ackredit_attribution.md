---
summary: Capture portable native scientific attribution through optional public Ackredit APIs.
issue: uibcdf/pharmacophoremt#19
status: active
opened: 2026-10-02
closed:
verification: measured
area: [attribution, integration]
guard: tests/test_attribution.py
normative: docs/content/cookbook/attribution.md
blocked_by: []
supersedes: []
---

# Native portable Ackredit attribution

## What

Explicit host activation captures scientific references on native calculations,
keeps the application's Ackredit session, attaches detached bibliography and
versions to models/results, and delegates reports to Ackredit's public API.

## How

`pharmacophoremt.attribution()` activates ContextVar-based instrumentation.
The deferred DepDigest boundary loads Ackredit on the first reached calculation.
Public `capture`, `scope`, `register_item` and `track_item` collect reached
software and method declarations. Composed children share a bounded capture.
JSON-native `pharmacophoremt.attribution@1` metadata embeds the detached public
`ackredit.attribution@1` result and explicit capture status.

References are verified offline. Consumer-owned IDs prevent overwriting provider
records. Assignment records the executed SciPy version and Crouse reference;
BEDROC credits Truchon/Bayly only on its calculated branch. Future clique papers
remain design references. Native model serialization preserves the original
metadata; saved reports use `Attribution.from_dict`, without crediting the reader.
The warning boundary uses the public SMonitor DiagnosticBundle warning API;
its previously unused nonexistent `bundle.emit` alias has been removed.

## Why

A final report needs the methods and software actually reached, not a static
list of dependencies or literature being considered. Session deduplication must
not make a second independent result lose its references.

## What is measured and what is assumed

Real-provider controls cover repeated references, application-session identity,
empty successful recognition, roles/versions, JSON persistence, deferred import,
absence, host provider failures (including warnings promoted to errors),
scientific exceptions and fresh-process reading without molecular engines.
Composed ensemble and retrospective captures are exercised separately.
The Ackredit source revision is
`584328de6efc07cee3a5ddf3ecda2d2e08cc72b4`, alongside the documented controlled
MolSysMT and PyUnitWizard revisions. Exact final results belong in the checkpoint.
This does not establish published wheel closure or a hosted supported matrix.

A separate cross-provider fault injection reproduced a remaining MolSysMT
boundary defect: global Ackredit registration failure plus warnings-as-errors
raises `MSM-WARN-ATTR-001` during recognition, wrapped as PHMT-E103. Provider issue
`uibcdf/molsysmt#295` owns the correction. Host-only failure controls pass; they
do not establish failure isolation inside every participating provider. No sibling
private code was patched or duplicated in PHMT.

## Alternatives and refuted paths

No private registry inspection, subtraction of globally used IDs, isolated host
sessions, automatic DOI enrichment or import hooks. No implicit complete-capture
claim after provider failure. The ordinary scalar metric API remains numerical;
its references contribute to the workflow capture rather than changing its
return type.

## Scope and exclusions

Native reference/interaction construction, placement, rigid/ensemble search,
correspondences/alignment and retrospective metrics participate. Legacy modeler
consolidation, bibliographic work deduplication and provider-wide policies remain
with their owners. PHMT's activation does not disable other providers' policies.

## Acceptance criteria

Review the public activation/payload/report contract and offline references;
keep real provider tests passing and verify published installation and the
supported Python matrix before advertising distribution support. Instrument
future methods only at their reached branches, preserving role/version context.
Local integration is implemented; issue remains open for contract and release
review.


## Public cross-provider receiving review — 2026-10-13

MolSysMT #295 is closed by provider correction `033c12b341abf6e986f9ae9ddd6c84bf167222c8`.
Its historical reproduction above remains valid for the original source. New
consumer controls verify public MolSysMT 0.23.0 with Ackredit 0.12.0 on Linux
x86_64/Python 3.14.8. The consumer is a normal editable copy of source `e912093`
with only the two retained test overlays; no sibling source is installed.

All 39 attribution/public-contract controls pass. Six new cases globally fail
real Ackredit `register_item`, `track_item` or `scope`, under ordinary warnings
and warnings-as-errors. MolSysMT's catalog event proves the failed boundary is
actually reached. The full scientific result equals its unattributed baseline,
while PHMT capture is explicitly failed with offline host records and no complete
bibliography. Application session identity is preserved. A seventh control keeps
the original scientific error's code, cause type and text after an actual completed
recognition with failed tracking. The same 39 controls pass in the qualified local
development environment. The initial scientific-error guard compared two distinct
invalid objects; its address-dependent message mismatch is retained and corrected
by reusing the same input, without changing runtime/provider code.

Public origins and downloaded archive SHA-256 values are verified; `pip check`
and the accepted production-context preflight pass. DepDigest resolves to public
0.14.0 in this fresh environment; this observes compatibility of the existing
boundary, not adoption of `DeclaredRegistry`. The ordinary manager still inherits
`ambermd`, although every installed package URL is `uibcdf`/`conda-forge`; subsequent
test-tool/backend operations use exclusive channels. Shared #116 retains ownership.

Receipt: [original public attribution review](../evidence/public_attribution_review_20261013_summary.json).
It preserves original test output/JUnit, provider/source identities, exact test
patches, environment history and complete manager output. The prior `e912093`
source CI separately passes the actual shared verifier for eleven required jobs,
including eight full Linux/macOS arm64 × Python 3.11–3.14 cells. Those hosted
jobs predate these new controls and use the existing controlled source providers;
they do not execute these new guards with public dependencies on every minor.

Remove #295 from active `blocked_by`. The issue remains active for the public
activation/payload/report contract and delivered-package qualification. No public
PHMT artifact, all-minor public attribution receiving, new minimum provider floor,
provider diagnostic import/construction/emission fault injection, addon delivery
or biological validation is established by this consumer review. The provider's
own diagnostic-construction/fallback regressions remain provider-owned.
