"""Serialization helpers for pharmacophoremt objects."""

from __future__ import annotations

from typing import Any

from pharmacophoremt import pyunitwizard as puw


def interaction_site_record(site: Any) -> dict[str, Any]:
    """Return a JSON-serializable record for a single interaction site."""
    center = site.center
    if center is not None and puw.is_quantity(center):
        center = puw.get_value(center, to_unit="nm").tolist()
    elif center is not None:
        center = [float(v) for v in center]

    radius = site.radius
    if radius is not None and puw.is_quantity(radius):
        radius = float(puw.get_value(radius, to_unit="nm"))
    elif radius is not None:
        radius = float(radius)

    features = list(site.features) if site.features else []
    return {
        "features": features,
        "center": center,
        "radius": radius,
        "essential": bool(site.essential),
        "weight": float(site.weight),
    }


def pharmacophore_payload(pharmacophore: Any) -> dict[str, Any]:
    """Return a JSON-serializable summary of a Pharmacophore object."""
    sites: list[dict[str, Any]] = []
    feature_counts: dict[str, int] = {}

    for site in pharmacophore.interaction_sites:
        record = interaction_site_record(site)
        for feat in record["features"]:
            feature_counts[feat] = feature_counts.get(feat, 0) + 1
        sites.append(record)

    return {
        "n_sites": len(sites),
        "feature_counts": feature_counts,
        "sites": sites,
        "name": getattr(pharmacophore, "name", None),
    }
