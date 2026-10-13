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
