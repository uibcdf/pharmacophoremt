---
summary: Competing molecular-source argument names must not silently replace the source.
issue: uibcdf/pharmacophoremt#101
status: withdrawn
opened: 2026-11-05
closed: 2026-11-05
severity: high
verification: measured
area: [contracts, molecular-boundary]
guard: tests/test_molecular_source_aliases.py
normative: devguide/molecular_source_admission.md
blocked_by: []
supersedes: []
---

# Molecular source alias overwrite

## What

The dispatcher already declares safe source aliases. Other public single-source
APIs retain a legacy standardizer that assigns system/mol_sys directly into
molecular_system, potentially replacing an explicit source. Original-production
probes will distinguish executed overwrite from new declaration requirements.

## How

Use public ArgDigest AliasTable for only existing aliases, with explicit scopes
for all public single-molecular_system entries: seven native free functions,
three evaluator methods and three constructors, plus existing dispatcher evidence.
Definition ownership protects inherited implementations. Retain global legacy
policy for unrelated callers, valid canonical/single-alias inputs, native domains,
defaults/internal bypass and all scientific bodies. No local collision engine.

## Acceptance

Refuse competing canonical/alias names in both orders before scientific/value
work, even for the same object. Preserve source identity for valid single names,
optional defaults, prepared-molecular results, selection/frame/state/provenance
and existing native failures. Record actual providers, original probes, attempts
and shared-machine resource bounds. Molecular operations remain MolSysMT-owned;
broader #6, provider delivery and full qualification gates remain separate.

## Withdrawal — original suspicion refuted, 2026-11-05

The [measured contract](../molecular_source_admission.md) and
[original receipt](../evidence/molecular_source_admission_20261105_summary.json)
refute the initial suspicion. Public ArgDigest0.17.1 keeps unknown closed-signature
extras away from the legacy standardizer; system/mol_sys are refused before
molecular access outside the dispatcher. Only model() declares those aliases,
with existing collision-safe ArgumentConsistencyError. No production overwrite
is reproduced and no runtime migration is justified. Initial severity is a
suspected impact classification, not a confirmed high-severity defect.

The initial132 cases yield119 failures/13 passes: most candidate expectations
incorrectly demand new aliases/declarations or another error type. The proposed
overwrite probe itself fails with protective UnknownArgumentError. One direct
array/dictionary comparison is also an invalid fixture; the corrected controls
use the unchanged detached quantity/array helper. Original candidate bytes,
outputs and identities are preserved, not relabeled as a failing library.

The revised guard protects actual closed-source refusal, the dispatcher's
declared aliases/collisions, optional canonical references, inherited evaluators,
no molecular access on refusal, and real prepared-feature/model/pose behavior.
153 final cases pass:89 new guards, one independent probe and63 existing controls;
136 old public-provider Pandas warnings remain visible. Production/provider/
dependency/scientific behavior is unchanged; #6 remains partial.
