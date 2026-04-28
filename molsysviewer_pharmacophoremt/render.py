"""Rendering helpers for pharmacophoremt elements in a MolSysViewer view."""

from __future__ import annotations

from typing import Any

from pharmacophoremt import pyunitwizard as puw

from .payloads import pharmacophore_payload

DEFAULT_SITE_ALPHA = 0.45
DEFAULT_SITE_RADIUS_NM = 0.15

_FEATURE_COLORS: dict[str, int] = {
    "positive charge":    0x3498DB,
    "negative charge":    0x884EA0,
    "hb acceptor":        0xB03A2E,
    "hb donor":           0x17A589,
    "included volume":    0x707B7C,
    "excluded volume":    0x283747,
    "hydrophobicity":     0xF5B041,
    "aromatic ring":      0xF1C40F,
    "halogen bond":       0x1ABC9C,
    "metal coordination": 0xE67E22,
    "cation-pi":          0xE91E63,
}
_DEFAULT_COLOR = 0xAAAAAA


def _color_for_site(features: list[str]) -> int:
    for feat in features:
        color = _FEATURE_COLORS.get(feat.lower())
        if color is not None:
            return color
    return _DEFAULT_COLOR


def render_pharmacophore_elements(
    view,
    pharmacophore,
    *,
    tag_prefix: str = "pharmt-site",
    alpha: float = DEFAULT_SITE_ALPHA,
    skip_digestion: bool = False,
) -> dict[str, Any]:
    """Render each pharmacophore interaction site as a sphere."""
    payload = pharmacophore_payload(pharmacophore)
    rendered: list[dict[str, Any]] = []

    for idx, site in enumerate(payload["sites"]):
        center = site.get("center")
        radius = site.get("radius") or DEFAULT_SITE_RADIUS_NM
        features = site.get("features", [])

        if center is None:
            continue

        tag = f"{tag_prefix}:{idx}"
        color = _color_for_site(features)

        layer = view.shapes.add_sphere(
            center=puw.quantity(center, "nm"),
            radius=puw.quantity(radius, "nm"),
            color=color,
            alpha=alpha,
            tag=tag,
            skip_digestion=True,
        )
        rendered.append({"index": idx, "features": features, "tag": tag, "layer": layer})

    return {
        "n_rendered": len(rendered),
        "rendered": rendered,
        "feature_counts": payload["feature_counts"],
    }
