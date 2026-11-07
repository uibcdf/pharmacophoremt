"""Catalog diagnostics that do not import the scientific host package."""

from pathlib import Path

from smonitor.integrations import CatalogException

from ._meta import API_URL, DOC_URL, ISSUES_URL

PACKAGE_ROOT = Path(__file__).resolve().parent
META = {"doc_url": DOC_URL, "issues_url": ISSUES_URL, "api_url": API_URL}
CATALOG = {
    "metadata": {"namespace": "PHMT", "name": "PharmacophoreMT results"},
    "signals": {},
    "warnings": {},
    "exceptions": {
        "ScreeningRunError": {
            "code": "PHMT-E201",
            "message": "Cannot {operation} screening-run evidence: {reason}.",
        }
    },
}
CODES = {
    entry["code"]: {"message": entry["message"]}
    for entry in CATALOG["exceptions"].values()
}
SIGNALS = CATALOG["signals"]


class ScreeningRunError(CatalogException, ValueError):
    """Run admission/storage failure, retaining its original exception as cause."""

    catalog_key = "ScreeningRunError"

    def __init__(self, message=None, *, operation=None, reason=None, **context):
        super().__init__(
            message,
            catalog=CATALOG,
            meta=META,
            extra={"operation": operation, "reason": reason, **context},
        )
