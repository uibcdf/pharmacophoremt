"""Feature-archive diagnostics; no scientific or test-support imports."""

from smonitor.integrations import CatalogException

CODES = {
    "PHMT-E301": {
        "message": "Review the feature-asset argument {argument}.",
        "hint": "Use the documented literal keys, generation and nonnegative integer bounds.",
        "metadata_message": "Review the feature-asset arguments.",
        "metadata_hint": "Use the documented argument contract.",
    },
    "PHMT-E302": {
        "message": "Feature-asset integrity verification failed.",
        "hint": "Preserve the evidence and restore a complete, unchanged archive.",
    },
    "PHMT-E303": {
        "message": "Feature-asset files could not be read.",
        "hint": "Check that the existing archive and its selected generation are readable.",
    },
    "PHMT-E304": {
        "message": "The feature-asset view is closed.",
        "hint": "Open a new view explicitly; existing views do not follow a refreshed generation.",
    },
    "PHMT-E305": {
        "message": "A requested work key is absent from this feature-asset generation.",
        "hint": "Inspect the manifest and preserve exact case, spaces and Unicode.",
    },
    "PHMT-E306": {
        "message": "The selected occurrence has no completed original payload.",
        "hint": "Inspect its retained extraction status and cause before requesting new work.",
    },
    "PHMT-E307": {
        "message": "This feature-asset format or reader profile is unsupported.",
        "hint": "Use a supported archive; study stores require an explicit separate export.",
    },
}
SIGNALS = {}
CATALOG = {
    "metadata": {"namespace": "PHMT", "name": "PharmacophoreMT feature archives"},
    "exceptions": {},
}


class FeatureAssetError(CatalogException, ValueError):
    """Catalogued asset failure with native errors preserved as causes."""

    def __init__(self, message=None, *, code=None, argument=None):
        super().__init__(
            message,
            code=code,
            catalog=CATALOG,
            extra={} if argument is None else {"argument": argument},
        )


def fail(number, *, argument=None):
    raise FeatureAssetError(code=f"PHMT-E{number}", argument=argument)
