"""Read-only declared feature evidence, delivered in PharmacophoreMT.

This namespace uses standard/support libraries only. It interprets no scientific
quantities, authenticates no source and creates no new scientific attribution.
Original opaque payload bytes can contain private geometry and provenance.
"""

from pathlib import Path

from smonitor.integrations import register_provider

from ._diagnostics import FeatureAssetError as FeatureAssetError

register_provider(Path(__file__).resolve().parent)

from ._api import FeatureAssetView as FeatureAssetView  # noqa: E402

__all__ = ["FeatureAssetView", "FeatureAssetError"]
