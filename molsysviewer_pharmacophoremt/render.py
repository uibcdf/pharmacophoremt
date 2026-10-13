"""Rendering helpers for pharmacophoremt elements in a MolSysViewer view."""

from __future__ import annotations

from typing import Any

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_center,
    digest_radius,
)
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.viewer.color_palettes import get_color_from_palette_for_feature

from .payloads import pharmacophore_payload
from .runtime import ensure_runtime

DEFAULT_SITE_ALPHA = 0.45


def clear_pharmacophore_elements(view, *, skip_digestion: bool = False) -> int:
    """Remove only tags successfully rendered by this add-on in this view.

    Unrelated shapes are preserved. A provider failure propagates and leaves the
    remaining tags recorded so callers can retry; no clear-all fallback is used.
    """
    runtime = ensure_runtime(view)
    cleared = 0
    for tag in runtime.rendered_tags.copy():
        view.shapes.clear(tag=tag, skip_digestion=skip_digestion)
        runtime.rendered_tags.remove(tag)
        cleared += 1
    return cleared


def render_pharmacophore_elements(
    view,
    pharmacophore,
    *,
    tag_prefix: str = "pharmt-site",
    alpha: float = DEFAULT_SITE_ALPHA,
    skip_digestion: bool = False,
) -> dict[str, Any]:
    """Replace this add-on's rendered elements with native spherical sites.

    Only ``sphere`` shapes are supported by this minimal integration. Reject
    every other shape before changing the scene, rather than approximating its
    scientific geometry. MolSysViewer owns sphere creation, units and deletion.
    """
    payload = pharmacophore_payload(pharmacophore)
    for site in payload["sites"]:
        if (
            site["shape"] != "sphere"
            or site["center"] is None
            or site["radius"] is None
        ):
            raise ArgumentError(
                argument="pharmacophore",
                reason=f"minimal add-on supports sphere sites only; got {site['shape']!r}",
            )
        # Reuse native cached-model contracts before touching viewer state.
        digest_center(puw.quantity(site["center"], site["length_unit"]))
        digest_radius(puw.quantity(site["radius"], site["length_unit"]))
    runtime = ensure_runtime(view)
    clear_pharmacophore_elements(view, skip_digestion=skip_digestion)
    rendered: list[dict[str, Any]] = []

    for idx, site in enumerate(payload["sites"]):
        center = site.get("center")
        radius = site["radius"]
        features = site.get("features", [])

        tag = f"{tag_prefix}:{idx}"
        color = get_color_from_palette_for_feature(features[0] if features else "")

        layer = view.shapes.add_sphere(
            center=puw.quantity(center, "nm"),
            radius=puw.quantity(radius, "nm"),
            color=color,
            alpha=alpha,
            tag=tag,
            skip_digestion=skip_digestion,
        )
        runtime.rendered_tags.append(tag)
        rendered.append(
            {"index": idx, "features": features, "tag": tag, "layer": layer}
        )

    return {
        "n_rendered": len(rendered),
        "rendered": rendered,
        "feature_counts": payload["feature_counts"],
    }
