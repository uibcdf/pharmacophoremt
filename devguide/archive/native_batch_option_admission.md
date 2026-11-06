---
summary: Native batches must reject unknown evaluation options independently of input length.
issue: uibcdf/pharmacophoremt#99
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: medium
verification: measured
area: [screening, contracts]
guard: tests/test_native_batch_contracts.py
normative: devguide/native_batch_contracts.md
blocked_by: []
supersedes: []
---

# Native batch option admission

## What

The native `run(**evaluation_options)` methods defer option admission to the
closed `evaluate()` signature inside their loop. Empty batches can therefore
accept typos silently. Nonempty batches warn about an unknown digester before
the downstream refusal. Baseline controls will distinguish measured failures
from the proposed declaration coverage.

## How

Declare each native run domain from its defining evaluate signature through
public ArgDigest. Keep the native closed constructor/evaluate signatures and
value digesters, defining ownership for inherited methods, batch-owned pose IDs,
on_error policy and all scientific calculations. VirtualScreening.run must keep
clearing both caches before native delegation. No domain derived from self.

## Why

Input length must not decide whether a spelling error is accepted. A rejected
option is an API error, independent of pose failure/negative accounting.

## Scope and acceptance

Target PoseEvaluator, RigidPoseSearch and ConformerScreening. Guard empty and
nonempty admission, literal kwargs names, method-specific frames, inheritance,
valid forwarding, cache reset and batch identity/error policy. Preserve molecular
ownership in MolSysMT. A subclass defining a different evaluate API must also
own its batch API/contract. No dynamic instance-domain emulation, provider edit,
dependency/version/release or full #6 qualification.

## Resolution — 2026-11-05

The [maintained contract](../native_batch_contracts.md) and
[original receipt](../evidence/native_batch_contracts_20261105_summary.json)
retain every attempt and actual provider/resource identity. Definition-owned
FunctionContracts cover nine native callables; three run domains derive from
their defining evaluate signatures. Scientific bodies and batch/facade accounting
remain unchanged. Normal unknown-option admission now precedes input digestion
and iteration for empty and nonempty native batches. The guard asserts early
refusal without missing-digester warnings, method-specific frames, literal kwargs
names, inherited declarations, valid forwarding, batch IDs/error policy and
facade cache reset.

Original 45 controls: 33 failures/12 passes, including nine new declaration
requirements and two erroneous facade scoring fixtures. Corrected fixtures on
original production confirm all three empty-facade typo failures. Final public
prefix 84/84 and modern source 167/167 pass, 206 unique selectors including 45
new. The source run retains one intentional attribution-warning test. No skips.
The original fixture mistake, source overlays and all logs/JUnit remain visible.
Broader #6, scientific validity and installed/public/platform/hosted qualification
are separate; no release or provider implementation is changed.
