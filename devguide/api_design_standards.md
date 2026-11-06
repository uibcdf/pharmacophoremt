# API Design Standards

Guidelines for writing clean, consistent, and ecosystem-compliant code in PharmacophoreMT.

For the current implemented surface use the [capability inventory](capability_inventory.md)
and [support boundaries](support_library_boundaries.md). Dated receiving sections
below preserve their original scope; they do not imply complete #6 adoption.
The registered root integration guides govern new support-library calls.

## Product design requirements — 2026-11-06

The accepted [product requirements](vision_and_scope.md#design-principles) pair
an intuitive guided workflow with a coherent, detailed public API and measured
scientific/performance quality. High-level workflows should compose the same
documented public operations available to expert users. Expose the effective
settings, source/state/conformer correspondence and failure accounting needed to
understand and reproduce results. Users should not need private modules to inspect
or control a supported scientific operation.

For chemical-library work, the
[comparative workflow survey](pharmacophore_library_workflow_survey.md) precedes
selection of public entry points, persistence/index formats and performance
claims. Early streaming or download sketches remain design candidates until
that comparison and provider-boundary review support their scope. Record tradeoffs
and evidence in #108; a competitor's UI, method name or timing is not an accepted
PHMT contract or equivalent scientific result.

## Molecular-source admission review — 2026-11-05

[#101 review](molecular_source_admission.md) refutes a suspected source overwrite
without changing production. Thirteen direct closed single-source entries require
molecular_system; unknown system/mol_sys names are refused before molecular work.
Only model() currently declares those aliases through its existing scoped table.
The legacy standardizer is not a promise that all APIs accept those names.
153 public-prefix controls pass; closed signatures need no redundant domains or
new alias expansion. Actual bypass, live-reference and provider limits remain.

## Retrospective and saved-result receiving — 2026-11-05

[#100 contracts](retrospective_result_contracts.md) declare saved summary/paired
comparison and retrospective constructor/run ownership. The retrospective run
keeps explicitly open forwarding to its instance-selected native evaluator, whose
own domain decides method-specific membership. Four contracts do not establish
complete #6 adoption. Existing saved-result metric-settings validation now also
prevents retrospective EF-key collisions before cohort materialization/evaluation,
including internal bypass; requested fractions/key names and metric formulae remain.
168 unique selected controls pass, with analytical and real molecular scopes explicit.

## Native screening receiving — 2026-11-05

[Native batch contracts](native_batch_contracts.md), #99/#6, declare nine
definition-owned constructor/evaluate/run contracts. Run option membership comes
from each defining evaluate signature, preserving method-specific frames and
batch-owned pose IDs. Normal unknown-option refusal precedes native iterable
consumption, including empty input. VirtualScreening.run retains cache reset
before native delegation. Inherited native methods keep their defining contract;
applications extending evaluate must own the corresponding batch API/contract.
206 unique selected controls pass; broader #6 remains partial.

## Nested facade receiving — 2026-11-04

[Definition-owned constructor domains](nested_facade_contracts.md) now cover
ligand consensus and screening options under #6; #78 consumes VirtualScreening's
explicit skip control locally. This is method-specific admission before input
consumption, not a change to scoring/search/preparation. Public batch/evaluation
contracts and broader adoption remain partial, preserving cache-clear order.

## Current scoped adoption — 2026-11-04

The public `model` facade declares its method-dependent keyword domain and
existing source aliases through ArgDigest. See the [capability/contract map](capability_inventory.md)
and [receiving evidence](evidence/model_dispatch_contract_20261104_summary.json).
Native shape constructors retain their previously received definition-owned
contracts. Remaining callers are not implicitly migrated; #6 tracks partial
adoption. Model methods, valid scientific inputs and provider ownership are
unchanged. A conflicting alias now raises ArgumentConsistencyError; an unknown
method-specific option raises UnknownArgumentError before downstream digestion,
without the former missing-digester warning.

## 1. Argument Digestion (`argdigest`)
New or changed public argument boundaries use ArgDigest's registered,
definition-owned contracts at the actual defining function/method. Follow
`ARGDIGEST_GUIDE.md`, the existing scoped native declarations and #6; do not copy
an invented decorator/configuration or add redundant placeholder digesters.
Keep scientific validation at its owning boundary, including bypass behavior.
MolSysMT owns molecular selection syntax and preparation; aliases are admitted
only where the actual PHMT signature/contract declares them.

## 2. Diagnostics and Errors (`smonitor`)
Use the `smonitor` catalog for all user-facing warnings and errors.
- **Namespace**: `PHMT` (e.g., `PHMT-E101` for an invalid interaction site type).
- **Levels**: Use `ERROR` for blockers and `WARNING` for non-critical inconsistencies (e.g., units not provided).

## 3. Naming Conventions
- **Internal Variables**: Use snake_case.
- **Classes**: Use PascalCase (e.g., `HBDonorSphere`).
- **I/O Functions**: Use the pattern `load_[software]` for reading and `to_[software]` for writing (e.g., `load_ligandscout`, `to_pharmer`).
- **Private Methods**: Prefix with `_` or `__` as per the Python standard.

## 4. Docstrings
- Use the **NumPy style** for all docstrings.
- Include an `Examples` section demonstrating usage with `molsysmt`.
