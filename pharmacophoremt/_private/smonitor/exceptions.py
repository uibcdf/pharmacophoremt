from smonitor.integrations import CatalogException
from . import CATALOG, META

class PharmacophoreMTException(CatalogException):
    def __init__(self, **kwargs):
        super().__init__(catalog=CATALOG, meta=META, **kwargs)

class LibraryNotFoundError(PharmacophoreMTException):
    catalog_key = "LibraryNotFoundError"

class InvalidInteractionSiteError(PharmacophoreMTException):
    catalog_key = "InvalidInteractionSiteError"
