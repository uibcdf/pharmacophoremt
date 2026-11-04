---
summary: Give PHMT-owned native I/O refusals catalog codes while retaining error families.
issue: uibcdf/pharmacophoremt#81
status: resolved
opened: 2026-11-04
closed: 2026-11-04
severity: low
verification: measured
area: [io, diagnostics]
guard: tests/test_native_io_diagnostics.py
normative:
blocked_by: []
supersedes: []
---

# Native pharmacophore I/O diagnostic consistency

## Resolution — 2026-11-04

243 selected cases pass in 25.53 s, including 43 new diagnostic and two
administrative dependency guards. All six attempt source/native/test/input/
metadata identities pass. Original 38-case scope has 34 failures/four preservation
passes; final diagnostics carry PHMT-E108/NativeFormatError and PHMT-E109/
ArgumentTypeError. ValueError/TypeError catch compatibility is retained, while
concrete types/rendered messages change explicitly. PHMT-E102 scientific
validation, parser/provider/filesystem exceptions and writer protection remain.

[Contract](../native_io_diagnostics.md) and
[original receipt/full evidence](../evidence/native_io_diagnostics_20261104_summary.json)
retain every attempt, exact overlays and compatibility boundary. SMonitor owns
rendering; typed context, merged metadata and args-only reconstruction work in
all five configured profiles. The scoped finite-record wrapper retains its
original encoder ValueError cause. Native acceptance conditions and all
writer/reader/payload functions remain unchanged apart from owned diagnostic
raises and that cause boundary; SDF container source is unchanged.

#6 also aligns nglview's existing mandatory classification and declares the
native YAML codec directly as PyYAML>=5.1 in metadata/recipe, three generated
ordinary environments and three scientific environment selectors. Actual
PyYAML 6.0.3 source/native identity is recorded; no older-floor/public installation
claim. SDK 22 distribution/eight environment controls, generated/declared-route
checks and strict real 26-page documentation closure pass with execution off.
The original selector typo, unreached caller-only-extra assumption, metadata
floor refinement and administrative selector/synthetic-version corrections are
retained; no scientific assertion is relaxed.

Guard assertions directly protect coded refusal branches, original exception
families/context/causes, unchanged scientific/parse/encoder/filesystem handling
and destination bytes. Broader #6 ArgDigest/native I/O admission is next;
molecular operations remain MolSysMT-owned. #10/#23/#9, #74/MolSysMT #215 and #66
retain their separate gates; no full-suite, installed/public/all-platform or
predictive qualification.

## What

At 704fe42522f4743163a77d3926374def945d6a7a, owned JSON/YAML schema/envelope/
software/unit refusals raise uncoded ValueError; io.load(42) raises uncoded
TypeError. Native geometric argument errors already use PHMT-E102. This is
the support-library consistency follow-up accepted under #6.

## How

Use catalog-backed ValueError/TypeError subclasses with typed field/argument
context, cause preservation where relevant, args-only reconstruction and real
rendering. Keep the existing rejection conditions and writer preparation order.
No parser, molecular format or quantity codec implementation.

## Why

Callers and diagnostic consumers need stable codes for owned validation failures.
Preserve exception-family compatibility and explicitly document the new concrete
type names and catalog messages.

## What is measured and what is assumed

The original #6 read-only probe confirms uncoded unknown-schema and nonstring
filename errors, contrasting coded negative-radius refusal. Runtime/native
identities are retained separately from source inspection and published delivery.

## Alternatives and refuted paths

Do not wrap all reader/provider errors or add an unrestricted loader catch.
Standard parser/encoder/filesystem and MolSysMT/provider failures retain their
own contracts. Only the native schema's explicit finite-record validation wraps
its encoder ValueError while retaining that original cause.

## Scope and exclusions

Owned native pharmacophore admission and the existing dispatcher filename check.
Scientific site/shape validators retain PHMT-E102. Molecular formats/operations,
other translator diagnostics, broader ArgDigest admission and installed/public
qualification remain separately owned. #6 also aligns nglview's declaration
with its unchanged mandatory package requirement; no dependency optionality change.

## Acceptance criteria

Original uncoded refusals fail new guards; structured refusals pass without
changing data admission, writer destination protection or provider exceptions.
Existing dispatch/persistence/support controls remain green. Record every attempt,
exact overlays and complete identities; update owning reports and checkpoint.
