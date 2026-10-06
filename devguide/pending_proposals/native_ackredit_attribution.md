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
blocked_by: [uibcdf/molsysmt#295]
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
