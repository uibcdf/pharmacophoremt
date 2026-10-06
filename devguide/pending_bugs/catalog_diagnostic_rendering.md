---
summary: Restore authored SMonitor catalog messages for PharmacophoreMT diagnostics.
issue: uibcdf/pharmacophoremt#2
status: active
opened: 2026-09-27
closed:
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
