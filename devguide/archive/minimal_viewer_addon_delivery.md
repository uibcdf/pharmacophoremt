---
summary: Bundle the implemented MolSysViewer addon and qualify its minimal installed Python contract.
issue: uibcdf/pharmacophoremt#56
status: resolved
opened: 2026-10-13
closed: 2026-10-13
verification: measured
area: [viewer, distribution]
guard: tests/test_molsysviewer_pharmacophoremt_addon.py
normative: devguide/viewer_addon_workflow.md
blocked_by: []
supersedes: []
---

# Minimal viewer addon delivery

## What

The existing seven-file addon was excluded from setuptools discovery and the
runtime resource inventory. Its tests inserted the checkout, its spec named a
nonexistent separate distribution, and several declared contributions had no
implementation. Rendering silently collapsed geometry or skipped sites, and
clearing used an unsupported tag-prefix API while suppressing failures.

## How

Bundle the addon in the toolkit distribution with a module entry point and the
actual toolkit version. Declare implemented contributions only. Reuse cached
native shape contracts, the pharmacophoric palette and public MolSysViewer shape,
panel and registry tools. Track successfully rendered tags for exact cleanup.
Reject unsupported geometry before mutation and expose failures in panel state.

## Why

Installed discovery and an honest geometry/cleanup contract are prerequisites for
reviewing the viewer interface. Molecular preparation and general visualization
infrastructure remain with their providers.

## What is measured and what is assumed

The [receipt](../evidence/minimal_viewer_addon_20261013_summary.json) preserves
source overlays, original command output/JUnit, artifact identities/inventories,
provider/environment records and guard inputs. Twenty-two controls pass from a
normal noneditable wheel outside checkouts on public Linux/Python 3.14.8 and on
development Python 3.14.7. Both import orders preserve discovery/lifecycle.
Independent unit, unsupported-shape, invalid-radius, cleanup-failure and
source-shadow negatives pass. All 179 runtime paths are present in the wheel;
the sdist includes the addon and supports a separate wheel build.

An initial zero-radius oracle and an overly exact floating-point comparison
were corrected to the existing native positive-radius contract and a declared
1e-14 conversion tolerance. A misnamed Conda build-tool input failed before
correction to `python-build`; original failures remain in the receipt. An initial
root-export discovery cycle is reported in MolSysViewer #233; importing the
public provider module avoids that cycle. Build metadata warnings are separately
tracked in local #57.

## Alternatives and refuted paths

Adding consumer source to the normal receiving path would conceal omitted addon
payload. A separate distribution conflicts with the existing toolkit delivery
contract. Spherical approximations for every native shape change their meaning.
Copying host registry, molecular routines or generic shape deletion into PHMT
would violate component ownership.

## Scope and exclusions

Closure covers minimal installed Python-side addon delivery. It does not publish
a release or qualify browser rendering, session persistence, all scientific tests,
the full Conda matrix or biological outcomes. Local #10/#23 remain partial;
MolSysSuite #117 and publication all-root helper adoption remain prerequisites
for the complete installed gate. Publication workflow pins are unchanged.

## Acceptance criteria

The real entry point discovers the packaged module and lifecycle. The panel and
sphere renderer have executable positive and independent negative controls.
Source-free runtime origins and complete intended payload are checked; missing
addon files fail the administrative archive guard. Optional viewer absence leaves
core import usable. The maintained contract names the remaining qualification.
