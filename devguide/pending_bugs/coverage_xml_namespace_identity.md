---
summary: Preserve package-qualified coverage XML identities for both runtime namespaces.
issue: uibcdf/pharmacophoremt#141
status: partial
opened: 2026-11-07
closed:
severity: medium
verification: reproduced
area: [ci, coverage, reporting]
guard: tests/test_coverage_xml_identity.py::test_ci_xml_keeps_same_basename_files_separate_and_unexecuted_files_visible
normative: devguide/coverage_xml_identity.md
blocked_by: []
supersedes: []
---

# Coverage XML namespace identity

Frozen4616c78 CI passes all eight source cells with2259 tests each, but its
original XML uses separate package-directory roots and collapses shared file
basenames. The two initializers appear as one root `__init__.py` class. Raw
files/totals remain preserved; native test success does not establish faithful
per-file XML attribution. See the [owning contract](../coverage_xml_identity.md).

The isolated actual-pytest-cov regression reproduces the original failure:
four bare classes replace seven intended qualified files. The implemented source
correction uses both `source_pkgs` and bare `--cov`, retaining branches, zero-hit
source discovery, main-private omission and full test selection/upload policy.
The corrected guard and all 111 selected local cases pass, with a reviewed
coverage-only workflow digest and unchanged acquisition/pins. See the
[receipt](../evidence/coverage_xml_20261107_summary.json).
Updated-head hosted XML and public upload remain separate#9/#23 gates; keep this
report partial until that declared receiving is complete.
