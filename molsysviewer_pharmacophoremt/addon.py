"""Addon definition for the PharmacophMT MolSysViewer integration."""

from molsysviewer.addons import (
    AddonContextActionSpec,
    AddonLifecycleSpec,
    AddonPanelSpec,
    AddonSpec,
    AddonWorkspaceSpec,
)

from pharmacophoremt import __version__

from .runtime import ensure_runtime, record_event


def on_enable(view) -> None:
    runtime = ensure_runtime(view)
    runtime.enabled = True
    record_event(view, "enable", workspace=runtime.workspace)


def on_disable(view) -> None:
    from .render import clear_pharmacophore_elements

    runtime = ensure_runtime(view)
    clear_pharmacophore_elements(view)
    runtime.enabled = False
    record_event(view, "disable", workspace=runtime.workspace)


def on_context_action(view, action_id: str, payload: dict) -> None:
    runtime = ensure_runtime(view)
    runtime.last_context_action = {"action_id": action_id, "payload": dict(payload)}
    if action_id == "show-pharmacophore":
        if runtime.pharmacophore is not None:
            from .render import render_pharmacophore_elements

            render_pharmacophore_elements(
                view,
                runtime.pharmacophore,
                tag_prefix=runtime.tag_prefix,
                skip_digestion=True,
            )
    record_event(view, "context_action", action_id=action_id)


lifecycle = AddonLifecycleSpec(
    on_enable=on_enable,
    on_disable=on_disable,
    on_context_action=on_context_action,
)

addon = AddonSpec(
    name="pharmacophoremt",
    package="pharmacophoremt",
    version=__version__,
    description="PharmacophoreMT workspace with a minimal spherical-site renderer.",
    workspaces=(
        AddonWorkspaceSpec(
            id="pharmacophoremt",
            title="PharmacophoreMT",
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
            entry="molsysviewer_pharmacophoremt.addon.on_context_action",
            target_kinds=("structure", "shape"),
            group="pharmacophoremt",
            order=10,
        ),
    ),
    meta={
        "domain": "pharmacophore",
        "status": "minimal",
        "supported_shapes": ["sphere"],
    },
)

ADDON = addon


def get_addon() -> AddonSpec:
    return addon
