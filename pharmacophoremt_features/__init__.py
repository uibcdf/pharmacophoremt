"""Feature evidence and explicit writer activation, delivered in PharmacophoreMT.

Import and metadata operations use standard/support libraries only. Explicit
ready-payload writing activates scientific validation. Historical reading stays
opaque; native-v2 metadata binds layout without scientific quantity decoding.
These operations authenticate no source and create no new extraction attribution.
Original opaque payload bytes can contain private geometry and provenance.
"""

from pathlib import Path

from smonitor.integrations import register_provider

from ._diagnostics import FeatureAssetError as FeatureAssetError

register_provider(Path(__file__).resolve().parent)

from ._api import FeatureAssetView as FeatureAssetView  # noqa: E402

__all__ = [
    "FeatureAssetView",
    "FeatureAssetError",
    "FeatureAssetStore",
    "FeatureInventoryPayload",
    "FeatureAssetRecord",
]


def __getattr__(name):
    if name == "FeatureAssetRecord":
        from ._record import FeatureAssetRecord

        globals()[name] = FeatureAssetRecord
        return FeatureAssetRecord
    if name == "FeatureInventoryPayload":
        from ._payload import FeatureInventoryPayload

        globals()[name] = FeatureInventoryPayload
        return FeatureInventoryPayload
    if name == "FeatureAssetStore":
        from ._writer import FeatureAssetStore

        globals()[name] = FeatureAssetStore
        return FeatureAssetStore
    raise AttributeError(name)
