# Package-qualified coverage XML identities

Owners LMMV/dprada; 2026-11-07 UTC;
[#141](https://github.com/uibcdf/pharmacophoremt/issues/141), source debt#9.
This contract precedes the local correction/receiving. The [receiving receipt](evidence/coverage_xml_20261107_summary.json)
now passes 111 selected local cases. The original frozen
CI4616c78 passes eight source cells with2259 tests each; that test success does
not establish correct XML file identity.

The original XML declares the core and companion directories as separate source
roots. It collapses shared relative filenames, including two package initializers
into one `__init__.py` class. Preserve those original files and aggregate metrics;
do not rewrite them or attribute them to a corrected head.

Implemented correction: use Coverage's `source_pkgs` for both runtime namespaces
and bare pytest-cov `--cov`, so the plugin does not replace the configured scope
with directory roots. Keep branch measurement, unexecuted package files, the
original main-private omission, full test selection and existing upload policy.
No XML rewriting or new coverage implementation is introduced.

The scientific source selection includes a real isolated pytest-cov regression
using the current CI options and copied configuration. Two fixture packages have
shared initializer/module basenames and unused files. Inspect actual XML for
distinct package-qualified names, zero-hit unused files, positive branch counts,
retained companion storage and omitted main private files. The child isolates its
own source paths/data file; it cannot pollute the enclosing coverage run.

Run that guard before/after correction, existing CI route/backlog and saved-reader
controls, affected distribution/declaration checks and reporting/archive/index/
full Ruff. Review the coverage-only workflow diff before updating its acknowledged
dependency-route digest. Preserve original attempts and actual resource limits.

Primary sources: [Coverage XML reporting](https://coverage.readthedocs.io/en/latest/commands/cmd_xml.html),
[Coverage source packages](https://coverage.readthedocs.io/en/latest/api_coverage.html),
[pytest-cov configuration](https://pytest-cov.readthedocs.io/en/latest/config.html).
The qualified installed tool versions and emitted files identify execution;
documentation alone does not prove the correction.

The original guard fails with four bare file classes. The corrected actual
pytest-cov run retains all seven expected qualified files, both unused modules
with zero hits, measured branches and the unchanged private/storage boundaries.
All 66 selected route/reader/export/progress controls, 24 distribution, 3 reporting
and 18 archive cases pass. Full Ruff, declared routes, indexes and whitespace
checks pass. The reviewed workflow digest changes from 26584916... to d361e326...
for the coverage-only argument change. Original source pins/acquisition remain.
Execution is serial CPU19/backend1/nice19/idle I/O with 512MiB per-process address
space and pressure checks; aggregate memory/no-swap/tasks/quota is unavailable.
Raw captures stay in owned ignored `build/phmt-ci-terminal-20261107-0414vm7g`
and `build/phmt-coverage-paths-20261107-mxn2456l`, review2026-11-20.

This changes reporting configuration/guards only. Later exact-head source/policy,
installed/public/platform and release gates remain separate. Do not dispatch
another full matrix for every small change. RDKit projection#140 and the accepted
mature-0.x staircase remain open.
