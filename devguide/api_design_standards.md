# API Design Standards

Guidelines for writing clean, consistent, and ecosystem-compliant code in PharmacophoreMT.

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
