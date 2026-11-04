# API Design Standards

Guidelines for writing clean, consistent, and ecosystem-compliant code in PharmacophoreMT.

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
All public-facing API functions MUST be decorated with `@arg_digest`.
- **Contract Definition**: Use the `_argdigest.py` configuration to map parameters to their respective digesters.
- **Validation**: Ensure that `selection` arguments are compatible with `molsysmt` syntax.

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
