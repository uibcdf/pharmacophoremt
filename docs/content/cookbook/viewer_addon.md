# Inspect a cached pharmacophore with MolSysViewer

The development PharmacophoreMT distribution bundles its MolSysViewer addon.
MolSysViewer is an optional installation input. The minimal addon displays native
spherical sites; it rejects other shapes before changing the scene. Python-side
installed controls pass with MolSysViewer 0.24.0 on Linux/Python 3.14.
Nine live-widget browser controls pass in the development environment with a
molecular scene. The shape-only workspace remains blocked by
[MolSysViewer #240](https://github.com/uibcdf/molsysviewer/issues/240); public
MolSysViewer 0.24.0 browser behavior has not been qualified.

Create a small analytical model or supply your already constructed native model:

```python
import molsysviewer as viewer
from pharmacophoremt import Pharmacophore
from pharmacophoremt.interaction_site import HBAcceptorSphere
from molsysviewer_pharmacophoremt import (
    clear_pharmacophore_elements,
    ensure_runtime,
    render_pharmacophore_elements,
)

model = Pharmacophore()
model.interaction_sites.append(
    HBAcceptorSphere(center="[0.1, 0.2, 0.3] nm", radius="0.5 nm")
)
model.n_interaction_sites = 1

# The executed browser fixture includes the provider's native molecular demo.
# Its cached pharmacophoric sites are analytical controls, not extracted features.
view = viewer.demo["dialanine"]
ensure_runtime(view).pharmacophore = model
result = render_pharmacophore_elements(view, model)
assert result["n_rendered"] == 1
view.camera.reset()
# Display `view` in the notebook frontend to inspect its scene.
# Remove the addon shapes when finished:
assert clear_pharmacophore_elements(view) == 1
```

For your own molecular scene, use the existing prepared system with
`viewer.new_view(prepared_system)`. Creating a dummy molecular system to enable a
shape-only addon is not the proposed solution to the provider issue.

The host discovers the addon through the installed entry point; no separate addon
distribution or checkout insertion is needed. Its panel summarizes the attached
cached model and offers Render/Clear controls. Rendering again replaces addon
shapes. Clearing preserves unrelated tags; reserve `pharmt-site` for this addon
within the view, or set an explicit prefix for the rendering call.

Lengths carry explicit units and the viewer owns their display conversion. A
provider failure is reported and remaining owned tags can be cleared again.
Neither rendering nor inspecting a saved model prepares or modifies a molecular
system. Use MolSysMT for molecular operations and PharmacophoreMT's native tools
to construct the hypothesis beforehand.
