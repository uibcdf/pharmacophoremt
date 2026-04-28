"""Addon definition for the PharmacophMT MolSysViewer integration."""

from molsysviewer import (
    AddonContextActionSpec,
    AddonExportHelperSpec,
    AddonLifecycleSpec,
    AddonPanelSpec,
    AddonShapeProviderSpec,
    AddonSpec,
    AddonWorkbenchSectionSpec,
    AddonWorkspaceSpec,
)

from .runtime import ensure_runtime, record_event


def on_enable(view) -> None:
    runtime = ensure_runtime(view)
    runtime.enabled = True
    record_event(view, "enable", workspace=runtime.workspace)


def on_disable(view) -> None:
    runtime = ensure_runtime(view)
    runtime.enabled = False
    record_event(view, "disable", workspace=runtime.workspace)


def on_context_action(view, action_id: str, payload: dict) -> None:
    runtime = ensure_runtime(view)
    runtime.last_context_action = {"action_id": action_id, "payload": dict(payload)}
    if action_id == "show-pharmacophore":
        if runtime.pharmacophore is not None:
            from .render import render_pharmacophore_elements
            render_pharmacophore_elements(
                view, runtime.pharmacophore, tag_prefix=runtime.tag_prefix, skip_digestion=True
            )
    record_event(view, "context_action", action_id=action_id)


lifecycle = AddonLifecycleSpec(
    on_enable=on_enable,
    on_disable=on_disable,
    on_context_action=on_context_action,
)

addon = AddonSpec(
    name="pharmacophoremt",
    package="molsysviewer-pharmacophoremt",
    version="0.1.0",
    description="PharmacophMT workspace for pharmacophore visualization in MolSysViewer.",
    workspaces=(
        AddonWorkspaceSpec(
            id="pharmacophoremt",
            title="PharmacophMT",
            entry_panel="pharmacophore",
            description="Workspace for pharmacophore model visualization.",
            order=30,
        ),
    ),
    panels=(
        AddonPanelSpec(
            id="pharmacophore",
            title="Pharmacophore",
            entry="molsysviewer_pharmacophoremt.panels.pharmacophore",
            description="Summary panel with interaction site render controls.",
            order=10,
            widget_class="molsysviewer_pharmacophoremt.panels.pharmacophore.PharmacophMTPharmacophorePanel",
        ),
    ),
    context_actions=(
        AddonContextActionSpec(
            id="show-pharmacophore",
            title="Show Pharmacophore",
            entry="molsysviewer_pharmacophoremt.context.show_pharmacophore",
            target_kinds=("structure", "shape"),
            group="pharmacophoremt",
            order=10,
        ),
    ),
    workbench_sections=(
        AddonWorkbenchSectionSpec(
            id="pharmacophore-summary",
            title="Pharmacophore Summary",
            entry="molsysviewer_pharmacophoremt.workbench.pharmacophore_summary",
            target_panel="workbench",
            order=10,
        ),
    ),
    shape_providers=(
        AddonShapeProviderSpec(
            id="pharmacophore-spheres",
            title="Pharmacophore Site Spheres",
            entry="molsysviewer_pharmacophoremt.shapes.pharmacophore_spheres",
            kinds=("pharmacophore", "sphere", "site"),
            order=10,
        ),
    ),
    export_helpers=(
        AddonExportHelperSpec(
            id="pharmacophore-export",
            title="PharmacophMT Export",
            entry="molsysviewer_pharmacophoremt.exports.export_pharmacophore",
            formats=("json", "html"),
            order=10,
        ),
    ),
    meta={
        "domain": "pharmacophore",
        "status": "skeleton",
        "rendering_ready": True,
    },
)

ADDON = addon


def get_addon() -> AddonSpec:
    return addon
