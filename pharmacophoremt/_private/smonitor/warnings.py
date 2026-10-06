"""Host warnings for optional attribution-provider failures."""

from smonitor.integrations import CatalogWarning

from .catalog import CATALOG, META


class AckreditTrackingWarning(CatalogWarning):
    catalog_key = "AckreditTrackingWarning"

    def __init__(self, message=None, *, extra=None):
        if message is not None and extra is None:
            super().__init__(message)
        else:
            super().__init__(message, extra=extra, catalog=CATALOG, meta=META)
