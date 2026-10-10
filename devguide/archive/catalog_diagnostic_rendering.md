---
summary: Restore authored SMonitor catalog messages for PharmacophoreMT diagnostics.
issue: uibcdf/pharmacophoremt#2
status: resolved
opened: 2026-09-27
closed: 2026-10-10
severity: medium
verification: measured
area: [diagnostics, integration]
guard: tests/test_contracts.py::test_catalog_authored_messages_render_through_smonitor
normative:
blocked_by: []
supersedes: []
---

# Catalog diagnostic rendering

## What and implementation

The previous CODES mapping used exception names rather than diagnostic codes,
the catalog used `errors` rather than `exceptions`, and PACKAGE_ROOT pointed
outside the package. The local correction exports code-keyed CODES and SIGNALS
from the package configuration, fixes the catalog/root, and retains authored
messages for PHMT-E001, PHMT-E101 and PHMT-W101.

## Evidence and review state

The guard calls the real SMonitor emitter for all three diagnostics and checks
the rendered messages and codes. Additional tests check positional-message
exception reconstruction and the missing optional MolSysViewer path. Early
InteractionSite validation now has a safe representation for signal capture.

The local implementation is under review. Do not infer a hosted CI pass or
close the owning issue before accepting the reviewed change; archive this
report with its tested guard at closure.


## Reviewed resolution — 2026-10-10

The correction is already committed in the current source. Review confirms
`PACKAGE_ROOT` addresses the package, `_smonitor.py` exports code-keyed mapping
entries and the catalog uses `exceptions`/`warnings`. The durable emitter guard
checks the original three authored messages and their diagnostic codes through
real SMonitor. Neighboring controls retain positional exception reconstruction,
missing-viewer diagnostics and safe early site validation.

The provider-owned `smonitor/devtools/verify_integration.py` is executed read-only
against this repository: configuration, emitted-code/template coverage, nonempty
resolution in user/dev/qa/agent/debug profiles, and reserved-class-name checks.
The installed SMonitor CLI independently validates the package configuration.
These checks qualify this specific rendering defect, not every SMonitor feature,
application policy or distribution floor.

Original commands/output, JUnit, the provider verifier's source/identity and
before/after producer/input/binary identities are linked in the
[closure review](../evidence/diagnostic_angle_closure_review_py314_summary.json).
The review does not modify runtime PHMT or sibling sources. The historical
under-review wording above remains the original checkpoint; this dated acceptance
and archived resolved status supersede it. Local focused checks are separate from
the hosted matrix, public artifacts and wider ecosystem adoption (#6).
