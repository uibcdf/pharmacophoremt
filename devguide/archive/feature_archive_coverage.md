---
summary: Include the feature-archive namespace in CI coverage before the 0.5.0 cut.
issue: uibcdf/pharmacophoremt#190
status: resolved
opened: 2026-11-11
closed: 2026-11-11
severity: medium
verification: reproduced
guard: tests/test_coverage_xml_identity.py
normative: devguide/coverage_xml_identity.md
area: [ci, api]
blocked_by: []
supersedes: []
---

# Cover the saved-feature reader

The new shipped pharmacophoremt_features reader was absent from source_pkgs.
The existing actual CI-command XML guard is extended from two to three roots,
with identical basenames and unexecuted modules in each. The source configuration
and actual XML controls fail before the correction; two other CI-route guards
pass. Adding the third coverage root makes all four pass. Private core omissions,
complete native CI selection and the original results namespaces remain intact.

The release [source-cut decision](../release_0_5_0_source_cut.md) owns the candidate
checkpoint. This local correction does not infer a hosted report, full source
matrix or installed/public qualification. Original local red/green XML and
resource records remain in the owned source-cut capsule; #95/#9 receive the
exact candidate's actual coverage evidence separately.
