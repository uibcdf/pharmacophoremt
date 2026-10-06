from smonitor.integrations import CatalogException

from . import CATALOG, META


class PharmacophoreMTException(CatalogException):
    def __init__(self, message=None, *, code=None, extra=None, **context):
        super().__init__(
            message,
            code=code,
            extra={**(extra or {}), **context},
            catalog=CATALOG,
            meta=META,
        )


class LibraryNotFoundError(PharmacophoreMTException):
    catalog_key = "LibraryNotFoundError"

    def __init__(
        self,
        message=None,
        *,
        library=None,
        pypi=None,
        conda=None,
        extra=None,
        **context,
    ):
        details = dict(extra or {})
        if library is not None:
            details["library"] = library
        details.setdefault("pypi", pypi or details.get("library", "unknown"))
        details.setdefault("conda", conda or details.get("library", "unknown"))
        super().__init__(message, extra=details, **context)


class InvalidInteractionSiteError(PharmacophoreMTException):
    catalog_key = "InvalidInteractionSiteError"


class ArgumentError(PharmacophoreMTException, ValueError):
    catalog_key = "ArgumentError"


class PoseEvaluationError(PharmacophoreMTException, ValueError):
    catalog_key = "PoseEvaluationError"


class ProviderCapabilityError(PharmacophoreMTException, NotImplementedError):
    catalog_key = "ProviderCapabilityError"


class SearchLimitError(PharmacophoreMTException, RuntimeError):
    catalog_key = "SearchLimitError"


class ConsensusLimitError(PharmacophoreMTException, RuntimeError):
    catalog_key = "ConsensusLimitError"


class CliqueLimitError(PharmacophoreMTException, RuntimeError):
    catalog_key = "CliqueLimitError"
