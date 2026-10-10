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

## Scientific evidence archives

Prepared end-to-end qualification: `python -m devtools.prepared_workflow --output FILE`
composes the existing CCD fixture client, cached-model tools, three native codecs
and placed screening with independent negative/failure controls. Its
[contract](../devguide/prepared_end_to_end_workflow.md),
[recipe](../docs/content/cookbook/prepared_workflow.md) and
[case](../docs/content/validation/prepared_workflow.md) declare the scope.
This opt-in driver requires the development checkout and Ackredit for its
explicit application-session review. It is not biological or performance evidence.
Its explicit `--case search` continuation exercises saved rigid queries and
prepared-frame budget/score accounting; see the
[search contract](../devguide/prepared_search_workflow.md). The default placed
case retains its original contract and evidence identity.

`evidence_archive.read_archived_evidence()` reads the existing local gzip/JSON
archive envelope with compressed/uncompressed SHA-256 and optional byte-count
checks. It preserves original failed, partial and unknown fields, requires a
sibling archive and imports no scientific providers. Scientific schema and
acceptance remain with each producer/caller. Use
`python -m devtools.evidence_archive SUMMARY.json` for archive integrity only.
The [collection contract](../devguide/validation_collection.md) and
[case template](../devguide/templates/evidence_case.md) define contribution,
ownership, execution and historical-result rules.
