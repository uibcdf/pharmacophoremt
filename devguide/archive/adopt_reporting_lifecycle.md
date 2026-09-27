---
summary: Adopt the MolSysSuite issue-backed reporting lifecycle locally.
issue: uibcdf/pharmacophoremt#8
status: resolved
opened: 2026-09-27
closed: 2026-09-27
verification: inspected
area: [governance, reporting]
guard: tests/test_reporting_protocol.py::TestReportingProtocol::test_existing_reports_have_valid_metadata_and_generated_indexes
normative:
blocked_by: []
supersedes: []
---

# Adopt the reporting lifecycle

## What

Provide the local template, generated indexes, offline metadata validator and
independent governance CI job required by `uibcdf/molsyssuite#60`.

## How

Preserve the active policy review `uibcdf/pharmacophoremt#6` and archived
scientific defect `uibcdf/pharmacophoremt#5`. Index both with their existing
identity and status. Add a stdlib-only validator and test it with negative
metadata and guard-selector cases. Run the check in a job independent of the
scientific package matrix.

## Why

The current queue and archive are maintained manually. A missing issue,
stale index, false closure or nonexistent guard can be committed without an
offline governance failure. The common suite protocol requires an executable
local check.

## What is measured and what is assumed

Inspection of `main` on 2026-09-27 found queue and archive documents but no
local template, generated index, offline validator or reporting CI job. The
existing archived guard names an exact pytest node and can be checked
mechanically without executing the scientific test.

## Scope and exclusions

This change governs report records. It does not modify scientific test
expectations, package dependencies, or the separate Python CI-lane rollout.

## Acceptance criteria

The validator accepts the existing records and rejects missing issue identity,
false closure and unresolvable pytest selectors. Generated indexes are current.
The governance job passes on the published commit independently of the
scientific matrix. The local issue is closed with the durable guard and
archived report path.

## Resolution

Commit `59aaef1` added the local protocol, template, offline validator,
generated indexes and independent governance job. The guard checks the
existing issue-backed records and current generated indexes; the additional
negative tests reject false closure and missing or invalid guard targets.
Local reporting tests and Ruff checks passed. Hosted CI run `36357320876`
passed its independent Reporting governance job, and MolSysSuite policy run
`36357321213` passed. Scientific matrix jobs in the same CI run are separate
and are not required to establish this reporting outcome.
