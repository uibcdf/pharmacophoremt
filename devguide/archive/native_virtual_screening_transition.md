---
summary: Replace implicit legacy screening and validation preparation with explicit prepared-native tools.
issue: uibcdf/pharmacophoremt#45
status: resolved
opened: 2026-10-10
closed: 2026-10-10
verification: measured
area: [screening, validation, architecture]
guard: tests/test_virtual_screening.py
normative: devguide/virtual_screening_workflow.md
blocked_by: []
supersedes: []
---

# Explicit prepared-native screening transition

## What

Under #41, retire local conformer preparation, legacy SMARTS matching and
hydrogen-removing molecular exports from `VirtualScreening`. Require an explicit
native method and prepared coordinates. Retrospective/LOO validation must choose
its evaluator instead of falling back to the legacy engine.

## How

Reuse `PoseEvaluator`, `RigidPoseSearch` and `ConformerScreening`. Preserve the
class's ranked hit-list surface and all native evaluation evidence. CSV/DataFrame
format scalar results; SDF export is explicitly retired. Molecular preparation
remains MolSysMT #219 and collection/property fidelity #215/#223.

## Why

The old public route generated H/conformers and minimized/pruned molecules
inside PHMT, using a different matching contract. A silent native substitution
would obscure one-to-one assignment, mandatory essential sites and donor-H
geometry. Explicit choices keep those scientific differences reviewable.

## What is measured and what is assumed

Source inspection establishes the retired call paths. Focused prepared analytical
controls will qualify the new consumer. No legacy numerical equivalence,
biological ranking, complete receptor preparation, provider-main qualification,
released distribution or performance claim is intended.

## Alternatives and refuted paths

Do not add a second conformer generator while MolSysMT #219 is pending. Do not
recreate molecular library codecs to mask #215/#223. Do not translate partial
essential coverage into the native contract or equate full coverage with a hit
when essential/exclusion criteria fail.

## Scope and exclusions

Reachable screening facade and its two validation callers. Unused preparation
utilities, native donor-vector migration (MolSysMT #375) and complete #41 audit
closure remain independent work. LOO retains first-hypothesis selection; it does
not perform affinity selection or prove an activity validation pipeline.

## Acceptance criteria

Explicit method/preparation/unit guards, real native placed/rigid/multi-frame
controls, failure versus negative accounting, deterministic ranking/cache reset,
scalar exports without molecular manipulation, explicit validator selection,
maintained guidance and passing reporting/distribution checks. Preserve original
measurement outputs and distinguish focused checks from complete hosted CI.

## Executed resolution — 2026-10-10

Implemented the explicit placed/rigid/conformer facade, removed its legacy
matching/preparation engine and molecular codecs, required native validation
tools and retained scalar hit exports. The normal editable Linux/Python 3.14.7
tree passes **185 focused tests in 145.34 s**, including actual rigid recovery,
prepared frame selection, one-to-one/essential matching, donor geometry and
steric veto, stable ranking, negative/failure accounting, transactional caches,
units, optional attribution, CSV and LOO adapter controls. One warning is the
deliberately failed optional Ackredit provider control.

Both actual modified cookbook recipes execute all Python blocks; strict scoped
Sphinx rendering passes with original navigation and explicit stubs for other
pages. This is not a full-site build. Reporting/index/archive, 23 distribution
and helper guards, declared dependency routes, environment-generation drift,
7 CI route guards and Ruff/format checks pass. No package module was added, so
the complete 179-path distribution inventory is unchanged.

The [summary](../evidence/native_virtual_screening_review_py314_summary.json)
links the checksum-qualified original archive with full output/JUnit, recipe
records, executable driver, source/fixture hashes, dirty overlay, actual provider
heads/versions and installed binary inventory. Producer sources, binaries and
inputs were unchanged during measurement; all **23 prior gzip archives** remain
byte-identical. The binary inventory is not subprocess import tracing. Three
incomplete development diagnostics remain original and excluded from acceptance:
an unsupported fixture codec shortcut, cache retention on invalid options and
an incorrect expected native failure-stage name. Only the cache finding required
a facade fix; native evaluation now validates options after cache clearing.

The owned review context, documentation output and SDK clone were removed after
recording original evidence. This scoped cleanup does not complete #43's whole
component resource review. Full hosted matrix/installed/public delivery and
biological qualification remain separate. #41 stays partial for unused generic
utilities/library ingestion and donor geometry delegation under MolSysMT #375.
