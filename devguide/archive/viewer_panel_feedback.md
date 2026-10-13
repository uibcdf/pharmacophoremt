---
summary: Distinguish cached input states and clean panel listeners through the existing anywidget lifecycle.
issue: uibcdf/pharmacophoremt#59
status: resolved
opened: 2026-10-13
closed: 2026-10-13
verification: measured
area: [viewer, validation]
guard: tests/test_molsysviewer_pharmacophoremt_addon.py
normative: devguide/viewer_addon_workflow.md
blocked_by: []
supersedes: []
---

# Panel input feedback and lifecycle

## What

The attached empty model was displayed as absent, and anywidget 0.11.0 warned
about the panel's named render export. The renderer subscribed to custom
messages and button clicks without returning explicit cleanup. Provider cleanup
already cleared listener arrays; a retained-listener leak was not demonstrated.

## How

The panel state explicitly carries model presence and payload-read failure,
separate from action status. The frontend shows absent, empty and unreadable
input accurately. It uses a default object export and returns a callback that
removes the same custom-message and click handlers it registered.
MolSysViewer invokes cleanup and continues to own transport, mounting and
general visualization. No new dependency floor or provider implementation
is introduced.

## Why

Empty input is a valid cached model. A payload failure must retain its error,
and a failed Clear must not describe a readable empty model as unreadable.
Explicit teardown also makes detached controls inert without depending on
the provider clearing its listener arrays.

## What is measured and what is assumed

The [fresh receipt](../evidence/viewer_panel_feedback_20261013_final_summary.json)
preserves real Jupyter/anywidget/Chrome outputs, source overlay and hashes,
screenshots and the prior runs. Fourteen controls pass, including normal
remounts, empty/absent/error feedback, visible Clear failure on an empty model,
retry and detached button activation without new backend events. The PHMT
anywidget deprecation warning and browser page errors are absent in the final run.
Twenty-three native addon tests pass, including empty-model Clear failure.

The executed provider remains development `c046fca1`, Python 3.14.7 and
anywidget 0.11.0; the exact versions are observations, not added minima.
Jupyter's debugger extension is disabled in task-owned configuration.
This does not relabel earlier or current installed-provider results.
The initial 12-control run passed before the extra empty-model Clear-failure
control. A subsequent 13-control run passed its visible assertions but captured
empty error strings after a notebook observation; it is retained as an earlier
capture, not substituted for the final corrected measurements.
The driver now saves visible error text before observing backend state.
The [separate 13-control receipt](../evidence/viewer_panel_feedback_20261013_summary.json)
remains unchanged. The final 14-control run additionally checks that a
successful Clear preserves an existing payload-read error; Clear now uses
the freshly built state without replacing its error status with idle.

## Alternatives and refuted paths

A zero site count alone cannot distinguish absent, empty and unreadable input.
Action error status alone cannot identify payload-read failure. A signal-only
renderer would require APIs absent from older supported anywidget revisions.
Using the existing cleanup callback preserves the current dependency contract.
No molecular dummy or PHMT host/transport implementation is needed.

## Scope and exclusions

Local panel presentation and lifecycle only. MolSysViewer #240 still owns the
shape-only workspace blocker and #58 remains partial. Installed/public matrices,
session persistence, physical GPU/Qt and scientific discrimination are excluded.
No new scientific attribution boundary is reached by this UI review.

## Acceptance criteria

Native controls distinguish presence and read failure; real browser controls
distinguish absent, empty and unreadable summaries and retain action errors.
Default export mounting succeeds without the named-render warning, remounts
preserve behavior, and detached controls cannot send actions. Original evidence
and the maintained workflow contract remain linked rather than overwritten.
