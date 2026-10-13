---
summary: Qualify the minimal addon through real Jupyter widget comms and browser rendering.
issue: uibcdf/pharmacophoremt#58
status: partial
opened: 2026-10-13
closed:
verification: measured
area: [viewer, validation]
guard:
normative: devguide/viewer_addon_workflow.md
blocked_by: [uibcdf/molsysviewer#240]
supersedes: []
---

# Live viewer addon browser qualification

## What

Advance #56's installed Python contract to actual Jupyter/anywidget frontend
communication and visible scene controls. Human UX feedback can follow executed,
reviewable results; it is not required to run these technical controls.

## How

Use the provider-owned WebGL-checked browser launcher, Chrome, a real JupyterLab
server/kernel and the actual PHMT addon. The maintained opt-in scenario in
`devtools/viewer_addon_browser_probe.mjs` drives normal visible controls, executes
backend observations through real notebook cells and preserves its output and
screenshots. It uses the cached analytical model in the adjacent notebook fixture;
the molecular scene is supplied by the native MolSysViewer/MolSysMT demo.
General widget/rendering/molecular infrastructure stays with its provider.

## Why

Passing Python tests do not establish that the panel mounts, that its buttons reach
Python, or that geometry is visible. Shape-only hypotheses must not require a dummy
molecular system to reveal a generic addon workspace.

## What is measured and what is assumed

Nine live controls pass on development Python 3.14.7, JupyterLab 4.6.4,
anywidget 0.11.0 and Chrome 155.0.8059.39 with the native dialanine scene:
initial counts, first and repeated rendering, remount/clear, unsupported point
rejection, visible provider clear failure, retry, empty-model disabled rendering
and lifecycle disable cleanup. Independent known wire coordinates/radii and
unrelated-tag preservation are retained. Screenshots show both native spheres;
`view.camera.reset()` supplies the final framing through the provider API.

The source is `3f76c35`, with development MolSysViewer
`c046fca173f501c6e259761ef8f3d6b1825f17e8` and its existing runtime bundle.
The [receipt](../evidence/live_viewer_addon_20261013_summary.json) retains original
outputs, producer/input identities, helper source, screenshots, failed attempts
and explicit scope. There are no browser page errors in the passing case.
This does not extend #56's public wheel proof into public browser qualification.

The same cached input on a molecular-free `MolSysView()` executes, but the welcome
card remains and the addon workspace button is hidden. The real click fails in an
isolated Jupyter workspace. MolSysViewer #240 owns the missing host behavior;
this theme remains partial. No PHMT molecular or generic host workaround is added.

Early failures included sandbox socket denial and test-driver mistakes concerning
CSS capitalization, modal controls and a retained notebook tab. Their original
outputs are preserved; they are not promoted into product failures or passing
qualification. Shared-launcher WebGL checks were not skipped.

Nonblocking panel empty/absent feedback and anywidget format/teardown review belong
to local #59. The live host's unknown `set_trajectory_summary` operation is reported
in MolSysViewer #239. An unrelated bqplot singleton-version warning is observed,
without a demonstrated PHMT failure. Session save/restore, hardware/visible-window
Qt, public browser delivery and complete installed matrices remain unexecuted.

## Alternatives and refuted paths

A mocked panel/transport cannot replace real widget communication. Force-clicking
hidden controls or creating a dummy molecular system would hide the provider
precondition. Copying generic viewer, transport or molecular preparation code into
PHMT would violate ownership. Screenshots are visibility evidence, not biological
validation or an independent reconstruction of the molecular geometry.

## Scope and exclusions

This is a development live-widget contract review, not a release, installed/public
matrix or scientific discrimination study. The molecular-scene result passes;
shape-only acceptance awaits MolSysViewer #240. Full helper isolation via
MolSysSuite #117 and public receiving remain under #10/#23.

## Acceptance criteria

Both molecular-scene and shape-only addon controls execute through normal public
host/widget APIs with preserved independent expectations and failures. Retain
original evidence and give changed producers fresh measurements. Close only after
the shape-only provider contract is qualified; human visual/UX feedback remains a
separate optional review of the resulting interface.

## 2026-10-13 upstream scope correction

The executed provider checkout was 102 commits behind the inspected upstream
`76c8cee1b2f00821820e05975609262844b27224`. This was checked late in the review;
the original receipt retains its actual older producer and is not relabeled as
current/public evidence. A [separate read-only inspection](../evidence/live_viewer_addon_20261013_upstream_check.json)
finds that current `updateWelcomeState()` still checks molecular structure data,
`getStructureData()` reads the molecular hierarchy, and structure capture reveals
the addon panel. The same generic precondition remains a supported suspected
provider finding, but a fresh current/public browser execution is required before
claiming that whole runtime has reproduced it. The standalone queue stays partial
under #240; current-provider receiving is the next technical qualification step.

## 2026-10-13 current-provider execution

The [new receipt](../evidence/current_viewer_addon_20261013_summary.json) measures
provider source `76c8cee1b2f00821820e05975609262844b27224` in a separate ordinary
Conda environment on Linux x86_64/Python 3.14.8. Public MolSysMT 0.23.0,
JupyterLab 4.6.4 and anywidget 0.11.0 supply the scientific/widget dependencies.
Both PHMT roots and provider imports originate in the receiving prefix. Normal
noneditable wheel installation honors Requires-Python; `pip check` passes.
The receipt preserves the original wheels, lock, native version file, bundle
hash, commands, effective environment records and original browser outputs.

The provider's own `npm ci` and `npm run build:runtime` build its current
frontend. Its only tracked source overlay is generated `viewer.js`; no provider
implementation is changed. Native versioningit identifies that overlay as
`0.24.0+83.g76c8cee1.dirty`, matching the version used by the final bundle build
and installed wheel. This is installed current-source evidence, not public
MolSysViewer 0.24.0 browser qualification or a full installed matrix.

All nine molecular-scene controls pass, with no browser page errors in the final
run. Independent expected angstrom centers, radii, colors and opacity match the
native provider records. Real screenshots show both spherical sites and the
unrelated sphere. Current canvas auto-hide requires the host's normal keyboard
hotspot access; the maintained scenario now uses that public interaction.

The verified shape-only fixture uses `mv.MolSysView()` and no molecular demo.
Its setup executes without page errors, but the welcome card remains and the
workspace button is hidden; the normal click fails before any addon control.
This freshly reproduces #240 on the current runtime. #58 remains partial.
The current runtime also reproduces the nonblocking #239 operation warning.

The archive retains failed attempts separately. One completed all nine controls
but failed the final page-error assertion with 16 JupyterLab
`No active debugger session` exceptions, whose stacks point to
`displayModules` in JupyterLab's frontend. Only its debugger extension was
disabled in task-owned configuration for the final runs; debugger-enabled
compatibility remains unqualified. Another temporary fixture replacement
incorrectly iterated a source string and retained the molecular demo; it is
explicitly excluded from shape-only evidence. The corrected fixture was checked
before the final independent run. Initial missing-beartype diagnostics led to
adding public beartype 0.22.9 before browser execution; no shared prefix changed.

`npm audit --json` reports nine transitive dependency findings, including one
critical finding. Reachability/exploitability was not assessed. Provider review
belongs to [MolSysViewer #242](https://github.com/uibcdf/molsysviewer/issues/242);
no local dependency fix or blanket scientific acceptance follows from the audit.
Session persistence, hardware/Qt and public browser delivery remain unexecuted.
