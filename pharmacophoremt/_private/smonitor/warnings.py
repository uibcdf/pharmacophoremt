"""Catalog warnings for optional attribution and pharmacophore projection."""

from smonitor.integrations import CatalogWarning

from .catalog import CATALOG, META


class ProjectionLossWarning(CatalogWarning):
    catalog_key = "ProjectionLossWarning"

    def __init__(self, message=None, *, operation=None, fields=None):
        if message is not None and operation is None and fields is None:
            super().__init__(message)
        else:
            super().__init__(
                message,
                extra={"operation": operation, "fields": fields},
                catalog=CATALOG,
                meta=META,
            )


class AckreditTrackingWarning(CatalogWarning):
    catalog_key = "AckreditTrackingWarning"

    def __init__(self, message=None, *, extra=None):
        if message is not None and extra is None:
            super().__init__(message)
        else:
            super().__init__(message, extra=extra, catalog=CATALOG, meta=META)
