---
summary: Gate native I/O ArgDigest receiving on preserved call shape and exception families.
issue: uibcdf/pharmacophoremt#82
status: blocked
opened: 2026-11-04
closed:
verification: measured
area: [io, tooling]
guard: tests/test_native_io_admission.py
normative:
blocked_by: [uibcdf/argdigest#47, uibcdf/argdigest#48]
supersedes: []
---

# Native I/O ArgDigest receiving gate

## What

At 6dc3da62a5d4623b6c22617b8d528582a52b1f79, candidate ArgDigest 0.17.0
decoration fails the native I/O call-compatibility gate. Closed endpoints lose
TypeError family compatibility on unknown/False-skip options (eight of twelve
calls). A literal keyword named like VAR_KEYWORD is flattened twice: values
disappear or become top-level arguments, including replacement of file_name.

The latter also affects current decorated model dispatch: a nested kwargs
mapping can replace an explicit molecular source before endpoint admission.
Routing-spy evidence measures argument identity, not molecular science.

## How

Preserve existing public I/O behavior with focused controls. Retain original
candidate and current-consumer probes under complete recorded source/native/
test/input/metadata identities. Prepare two exact provider issue drafts; generic
binding/exception policy belongs in ArgDigest. No local contract engine,
keyword-renaming workaround, private provider patch or premature decoration.

## Why

An adoption which silently changes a source or drops an option can produce a
plausible result on the wrong input. Successful legacy controls do not qualify
the failing candidate. Existing model-source replacement remains an open defect
until the provider correction is received and regression-qualified.

## What is measured and what is assumed

Public 0.17.0 is the measured provider; current sibling cd9c4f3 is read-only
context with the same relevant implementation. Opaque, mapping and named-value
collision probes reproduce the loss; an ordinary option and explicit True-skip
control preserve it. Both original probe identities are stable. This is not a
chemical identity comparison, validation study or public-closure qualification.

## Alternatives and refuted paths

Warn/ignore admission cannot preserve reliable option refusal. Undocumented skip
configuration, local exception engines, renaming VAR_KEYWORD and copying a
binding implementation are not accepted provider fixes. Native reader/writer
and dispatcher runtime remain unchanged while the receiving gate is unmet.

## Scope and exclusions

Native Python call compatibility and provider handoff. Molecular forms/options/
inspection/calculation remain MolSysMT-owned. Broader #6 migration, #74/MolSysMT
#215 and scientific/installed/public gates retain their own scope.

## Acceptance criteria

Provider-owned correction preserves literal keyword/value identities and
explicit named parameters, including current model-source identity. Supported
closed-signature refusal retains TypeError compatibility, or a separately
accepted migration changes that requirement. Receive published supported bytes,
then activate scoped native I/O contracts and rerun these guards plus the
provider reproductions. Baseline passing tests alone cannot close this report.

## Current blocker and owner — 2026-11-04

Owner LMMV/dprada under #6/#82. After two rejected publication attempts and
review of the concrete drafts, the user explicitly authorized both issues.
They are now [ArgDigest #47](https://github.com/uibcdf/argdigest/issues/47)
(literal keyword identity/source replacement) and
[#48](https://github.com/uibcdf/argdigest/issues/48) (TypeError compatibility),
both labeled component:pharmacophoremt. The [readiness checkpoint](../native_io_admission_readiness.md)
retains exact published material and original measurements. No provider source
change or local workaround. 260 selected compatibility cases pass, including
41 new baseline controls; these do not fix or qualify the failing candidate.
Wait for supported published provider correction/API, then receive it with the
original reproductions and legacy controls before activation. Review 2026-11-18
or provider readiness. Broader #6 remains partial.
