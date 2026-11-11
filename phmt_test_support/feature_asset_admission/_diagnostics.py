"""Catalog-backed admission failures without scientific imports or value capture."""

from smonitor.integrations import CatalogException

from ._smonitor import CODES

CATALOG = {
    "metadata": {
        "namespace": "PHMT-ASSET-STUDY",
        "name": "Unshipped feature-asset admission",
    },
    "exceptions": {},
}


class AssetAdmissionErrorStudy(CatalogException, ValueError):
    """Study error category; original provider call-shape exceptions stay native."""

    def __init__(self, message=None, *, category=None, argument=None):
        super().__init__(
            message,
            code=category,
            extra={} if argument is None else {"argument": argument},
            catalog=CATALOG,
        )


def refuse(number, argument):
    code = f"PHMT-ASSET-STUDY-E{number:03d}"
    assert code in CODES
    raise AssetAdmissionErrorStudy(category=code, argument=argument)
