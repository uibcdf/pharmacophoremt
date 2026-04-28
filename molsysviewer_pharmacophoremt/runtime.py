"""Runtime state for the PharmacophMT MolSysViewer addon."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PharmacophMTAddonRuntime:
    enabled: bool = False
    workspace: str = "pharmacophoremt"
    pharmacophore: Any = None
    tag_prefix: str = "pharmt-site"
    last_context_action: dict[str, Any] | None = None
    event_log: list[dict[str, Any]] = field(default_factory=list)


def ensure_runtime(view: Any) -> PharmacophMTAddonRuntime:
    runtime = getattr(view, "_pharmacophoremt_addon_runtime", None)
    if runtime is None:
        runtime = PharmacophMTAddonRuntime()
        setattr(view, "_pharmacophoremt_addon_runtime", runtime)
    return runtime


def record_event(view: Any, event: str, **payload: Any) -> PharmacophMTAddonRuntime:
    runtime = ensure_runtime(view)
    runtime.event_log.append({"event": event, **payload})
    return runtime
