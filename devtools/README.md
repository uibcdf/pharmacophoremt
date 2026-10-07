# Development and publication tools

Optional, checked environment generation/create/update calls are documented in
[conda-envs/README.md](conda-envs/README.md). Runtime comes from `pyproject.toml`;
`environment_tools.toml` selects ordinary generated files and `requirements.yaml`
contains local tools. The shared environment SDK is fixed and qualified; recipe,
plan, science/source-manifest and artifact controls remain separate.

Publication controls: [conda-build/README.md](conda-build/README.md).
Source/context preflight: `check_dependency_routes.py`. Run it in the actual
selected environment before tests; declaration success is not installed evidence.
Routine workspace development uses `molsyssuite@uibcdf_3.14`; install eligible
local clones with `python -m pip install --no-deps --editable PATH`.

Contributions follow the root instructions and synchronized suite guide. External
contributions require owner review through a PR; authorized internal direct pushes
retain the common checkpoint rules. Scientific repairs and release decisions stay
local. Independent governance runs the reporting, route and distribution/helper
guards without importing the scientific package.
