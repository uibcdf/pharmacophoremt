"""MolSysViewer addon for PharmacophMT — pharmacophore visualization."""

from .addon import ADDON, addon, get_addon, lifecycle, on_enable, on_disable, on_context_action
from .runtime import PharmacophMTAddonRuntime, ensure_runtime, record_event
from .panels import PharmacophMTPharmacophorePanel
from .payloads import interaction_site_record, pharmacophore_payload
from .render import render_pharmacophore_elements

__all__ = [
    "ADDON",
    "addon",
    "get_addon",
    "lifecycle",
    "on_enable",
    "on_disable",
    "on_context_action",
    "PharmacophMTAddonRuntime",
    "ensure_runtime",
    "record_event",
    "PharmacophMTPharmacophorePanel",
    "interaction_site_record",
    "pharmacophore_payload",
    "render_pharmacophore_elements",
]
