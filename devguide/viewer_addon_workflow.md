# Minimal MolSysViewer addon

Owned by [PharmacophoreMT #56](https://github.com/uibcdf/pharmacophoremt/issues/56).
The `pharmacophoremt` distribution includes the top-level
`molsysviewer_pharmacophoremt` package and a module entry point in
`molsysviewer.addons`. Its spec uses the installed toolkit version and package
identity. MolSysViewer remains optional for importing the scientific core.

## Tools and ownership

`pharmacophore_payload(model)` reads cached native sites and returns explicit
shape names, feature counts and lengths in nm. It performs no molecular
preparation, recognition, selection or placement. Those operations belong to
MolSysMT; pharmacophoric hypothesis construction belongs to PharmacophoreMT.

`render_pharmacophore_elements(view, model)` accepts spherical sites only.
Every site's shape, center and strictly positive radius must pass the existing
native contracts before the scene changes. Unsupported shapes and invalid cached
values raise `ArgumentError`; points, Gaussians and directional shapes are not
approximated as spheres. Explicit PyUnitWizard quantities pass to the public
MolSysViewer shape API, which owns viewer units, color normalization and rendering.
The local palette expresses pharmacophoric feature colors.

Successful additions are recorded in the view's addon runtime.
`clear_pharmacophore_elements(view)` clears those exact tags through the public
provider API, preserves unrelated tags and returns the cleared count. Rendering
again replaces the previous addon shapes; disabling the addon clears them.
The configured prefix (default `pharmt-site`) is reserved for this addon within
the view. Provider failure propagates; successfully added or uncleared tags remain
recorded for cleanup/retry. Replacement is not transactional.

The existing workspace exposes one summary panel and one context action. The
panel reads the attached cached model, requests a refresh after its frontend
listener is ready, and offers Render/Clear actions. Failed rendering, clearing or
payload reading yields an error state; a failed clear does not record success.
The summary distinguishes absent input ("No pharmacophore loaded."), a valid
empty model ("No interaction sites.") and a failed payload read ("Unable to
read pharmacophore."). The state carries `has_pharmacophore` and
`payload_error` separately from the action status: an unsuccessful Clear on
a valid empty model must retain its empty summary. A successful Clear retains
any payload-read error instead of resetting its status to idle. Render stays disabled for
absent, empty and unreadable input; Clear remains available to clean owned tags.
The module uses the anywidget default object export and returns a cleanup
callback that removes its exact custom-message and button listeners. The host
owns widget transport and invokes that callback on panel teardown. These use
the existing [AFM lifecycle](https://anywidget.dev/en/afm/) without requiring
newer signal/composition APIs or raising dependency floors.
Workbench sections, export helpers and shape adapters are undeclared until they
have implementations. The bulk `Pharmacophore.show()` route has a separate
contract and is not qualified by this addon review.

Specs and widgets are imported from the public `molsysviewer.addons` module to
avoid discovery during partial addon initialization. The generic root-export
discovery issue is tracked in
[MolSysViewer #233](https://github.com/uibcdf/molsysviewer/issues/233).

## Executed qualification

The [original receipt](evidence/minimal_viewer_addon_20261013_summary.json)
records an exploratory wheel/sdist built from `ad2e426` plus the preserved source
overlay. Normal noneditable wheel installation outside both consumer/provider
checkouts passes 22 addon controls on public Linux x86_64/Python 3.14.8 with
MolSysViewer 0.24.0. The same selection passes on development Python 3.14.7.
These versions are observations, not new compatibility minima.

Controls exercise metadata entry-point discovery, both fresh-process import
orders, lifecycle, real host panel resolution, cached summaries, provider sphere
messages, exact-tag cleanup/retry, unsupported geometry, zero-radius rejection
and a nondefault unit policy with independent nm-to-angstrom expected values.
The wheel contains all 179 declared runtime resources including seven addon
Python files, and the sdist preserves the addon source. A separate sdist-derived
wheel builds successfully. Core import also succeeds when viewer imports are
deliberately blocked; this does not physically uninstall its dependency closure.

The delivered all-root guard from MolSysSuite
`948d0267de8fa43c542ab7eba28b9f8b7fbf095e` checks loaded core/addon origins before
and after the installed controls. An independent deliberate source-shadow control
fails for the secondary addon root. Only shared developer-tool code is staged
for that guard; normal scientific imports come from the installed environment.
The existing publication workflow pins remain unchanged. Before full candidate
qualification, adopt a reviewed shared helper with all-root protection and resolve
scientific test-helper isolation through MolSysSuite #117 under local #10/#23.

This review does not publish a release, execute a Conda receiving matrix, qualify
browser DOM/WebGL rendering or establish biological discrimination. Browser
interaction, visible geometry and session behavior are the next viewer gate.

## 2026-10-13 live browser continuation

The [live review receipt](evidence/live_viewer_addon_20261013_summary.json) advances
#58 to a partial development result. Nine real Jupyter/anywidget/Chrome controls
pass with the native molecular demo and existing development providers. The
panel mounts, initial counts arrive, Render/Clear reach Python, repeated renders
replace owned shapes, remounting recovers the summary, unsupported points preserve
the scene with an error, provider cleanup failures remain retryable, an empty model
disables rendering, and disable clears owned tags. Screenshots show the native
geometry after the public `view.camera.reset()` operation.

The same cached input in a shape-only `MolSysView()` executes but retains the
welcome card and hides the addon workspace. [MolSysViewer #240](https://github.com/uibcdf/molsysviewer/issues/240)
owns that host prerequisite; #58 remains partial. Do not build a dummy molecular
system or a local host workaround to conceal it. The real provider observation
uses development commit `c046fca173f501c6e259761ef8f3d6b1825f17e8`, Python 3.14.7,
JupyterLab 4.6.4, anywidget 0.11.0 and Chrome 155.0.8059.39 with the provider's
WebGL-checked headless launcher and ANGLE/SwiftShader configuration. Browser page
errors are absent in the passing case. This is separate from the public wheel
proof, hardware/Qt observation, public browser receiving and session persistence.

The existing named-render anywidget warning and empty-versus-absent model feedback
are tracked in local #59; no listener leak was demonstrated. The unrelated live
host operation warning is tracked in [MolSysViewer #239](https://github.com/uibcdf/molsysviewer/issues/239).

### Repeat the opt-in scenario

Use the canonical development Python and a reviewed MolSysViewer checkout with
its declared Node test tools installed. Keep provider implementation unchanged;
when qualifying a rebuilt runtime, use its own build commands and retain the
source/lock identity, generated overlay, version and artifact bytes.
Copy `devtools/viewer_addon_browser_fixture.ipynb` to `addon.ipynb` under an owned
temporary Jupyter notebook root. Start JupyterLab on loopback with that root,
the canonical kernel and task-owned config/data/runtime directories. Keep its
authentication enabled. Put the local port/token in a private
`connection.json` in the task workspace; never publish credentials or kernel
connection files. The archived setup/config source documents the original launch.

Build the existing provider browser helper into the temporary workspace, using
its installed esbuild, and make its Node dependencies resolvable there:

```bash
"$PHMT_VIEWER_SOURCE/molsysviewer/js/node_modules/.bin/esbuild" \
  "$PHMT_VIEWER_SOURCE/molsysviewer/js/tests/e2e/e2e-browser.ts" \
  --bundle --platform=node --format=esm --external:playwright \
  --outfile="$PHMT_BROWSER_WORKSPACE/e2e-browser.mjs"
ln -s "$PHMT_VIEWER_SOURCE/molsysviewer/js/node_modules" \
  "$PHMT_BROWSER_WORKSPACE/node_modules"
PHMT_BROWSER_HELPER="$PHMT_BROWSER_WORKSPACE/e2e-browser.mjs" \
  node devtools/viewer_addon_browser_probe.mjs
```

`PHMT_BROWSER_WORKSPACE` names the owned workspace containing `connection.json`;
`PHMT_VIEWER_SOURCE` names the provider checkout. Export the former for the Node
process. The probe creates an isolated Jupyter frontend workspace per run, uses
real visible controls and writes `live-controls.json`, original PNG captures and
failure diagnostics there. Its process exits unsuccessfully on a failed control;
a retained failure is not a passing result. It uses no mocked widget transport
or external molecular downloads. Do not enable the provider's explicit skip flag
when collecting qualification evidence.

For the shape-only reproduction, change only the view construction in a temporary
notebook copy to `mv.MolSysView()` and set `PHMT_BROWSER_NOTEBOOK` to that copy's
basename. Preserve both runs independently. The fixture's model and molecule are
analytical scene controls, not extracted or biologically validated pharmacophores.
The nine controls do not execute save/restore, every platform or public providers.
Stop the owned Jupyter server/kernels and remove temporary data after archiving
results. Human feedback can then assess the visible panel; it does not replace
an unexecuted technical gate.

The executed development provider was subsequently found to be 102 commits behind
upstream. The [bounded upstream inspection](evidence/live_viewer_addon_20261013_upstream_check.json)
records the same molecular-structure premise in current source
`76c8cee1b2f00821820e05975609262844b27224`. It supports the owning issue while
keeping source inspection separate from browser execution. Qualify an updated
provider before generalizing the older run to current/public runtime or asking for
human acceptance of the current interface. The original measured archive remains
unchanged.

## 2026-10-13 installed current-provider continuation

The [current-provider receipt](evidence/current_viewer_addon_20261013_summary.json)
repeats the scenario with installed source `76c8cee1`, built through the
provider's `npm ci` and `npm run build:runtime`. A separate Conda receiving
prefix uses public MolSysMT 0.23.0 and Python 3.14.8; PHMT and the viewer are
normal noneditable wheel installations. Both PHMT package roots and scientific
providers load from that prefix, and `pip check` passes. The generated runtime
overlay yields the native version `0.24.0+83.g76c8cee1.dirty`; the archive keeps
both original wheel files and the exact generated bundle hash. This does not
qualify a published MolSysViewer artifact or broaden the platform matrix.

Nine molecular-scene controls pass without page errors in the final configuration.
The molecular-free fixture still retains the welcome card and hides the addon
workspace; #240 is now freshly reproduced on the current runtime. #58 remains
partial. The #239 operation warning also persists.

For this configuration, the receiving kernel is explicitly registered with its
own interpreter. The maintained probe reveals auto-hidden controls through the
provider's visible keyboard hotspot before activating panel mode. Preserve
fixtures as whole notebook source strings or line arrays according to their
actual representation; verify the shape-only construction before running.
The receiving environment includes public beartype 0.22.9 after observed import
diagnostics. Its task-owned Jupyter configuration disables only
`@jupyterlab/debugger-extension`, following captured JupyterLab exceptions in
the initial run; the failed debugger-enabled result is retained separately.
Do not infer debugger-enabled compatibility from the final passing run.

Current lock audit findings are reported in MolSysViewer #242. The review does
not change provider dependency code or add a PHMT host/molecular workaround.

## 2026-10-13 panel feedback and teardown

Local #59 is resolved by the summary and lifecycle contract above. The
[fresh panel receipt](evidence/viewer_panel_feedback_20261013_final_summary.json)
records 14 real Jupyter/Chrome controls and preserves the earlier 12-control
run separately. It verifies empty/absent/unreadable messages, action-error versus
payload-error feedback, disabled rendering, repeated mounts, error recovery,
unrelated-tag preservation and detached buttons that cannot dispatch actions.
The panel's named-render anywidget deprecation warning is absent in the final
run; page errors are absent.

This is development Python 3.14.7 with anywidget 0.11.0, JupyterLab 4.6.4 and the
existing development viewer `c046fca1`, not the current installed-provider
receipt above. The exact source overlay and input hashes identify the modified
panel. The task-owned Jupyter configuration disables its debugger extension,
as in the earlier current-provider run. Native addon controls pass 23 tests.
No generic host or molecular operation is implemented or modified. This local
panel qualification does not close #58/#240, execute session persistence or
replace full installed/public delivery gates.
