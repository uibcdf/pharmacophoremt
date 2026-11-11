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
    "PHMT-E308": {
        "message": "The expected feature-asset generation differs from this view.",
        "hint": "Inspect the intended generation and select it explicitly.",
    },
    "PHMT-E309": {
        "message": "A required feature family was not evaluated in this selection.",
        "hint": "Inspect coverage and request missing extraction explicitly.",
    },
    "PHMT-E310": {
        "message": "The original feature payload and its declared metadata disagree.",
        "hint": "Preserve the original evidence and inspect its supported profile and integrity.",
    },
    "PHMT-E311": {
        "message": "Original feature quantities or native geometry failed reconstruction.",
        "hint": "Inspect the retained cause; no default units or replacement features are inferred.",
    },
    "PHMT-E312": {
        "message": "PyUnitWizard lacks the required quantity-record capability.",
        "hint": "Use the documented qualified PyUnitWizard dependency for native reconstruction.",
    },
    "PHMT-E313": {
        "message": "This selection exceeds the native reconstruction batch limits.",
        "hint": "Select at most 64 occurrences and 8 MiB of original payload bytes per call.",
    },
    "PHMT-E320": {
        "message": "Another cooperating writer holds this archive.",
        "hint": "Close the owning writer before opening another writer handle.",
    },
    "PHMT-E321": {
        "message": "This archive writer is closed or belongs to another process.",
        "hint": "Open an explicit writer handle in the process that will use it.",
    },
    "PHMT-E322": {
        "message": "The archive's current generation differs from the expected publication state.",
        "hint": "Inspect current visibility before choosing the intended candidate and expected generation.",
    },
    "PHMT-E323": {
        "message": "This archive has reached its bounded operation-attempt limit.",
        "hint": "Retain its history and explicitly create a linked new archive; do not delete old receipts.",
    },
    "PHMT-E324": {
        "message": "This publication or retained attempt is not eligible for the requested retry.",
        "hint": "Inspect retained publication history and actual current visibility; no retry runs automatically.",
    },
    "PHMT-E325": {
        "message": "Archive operation receipts failed structural or lineage verification.",
        "hint": "Preserve the original receipt files for inspection; history is never repaired implicitly.",
    },
    "PHMT-E326": {
        "message": "An incomplete feature generation cannot replace published evidence.",
        "hint": "Inspect its original extraction statuses and causes before preparing a complete candidate.",
    },
    "PHMT-E327": {
        "message": "The feature-archive writer could not complete its local file operation.",
        "hint": "Preserve partial evidence and inspect the retained native cause and current visibility.",
    },
    "PHMT-E328": {
        "message": "This directory is not a supported writer-owned feature archive.",
        "hint": "Create a new writer archive explicitly and stage a supported source view.",
    },
    "PHMT-E329": {
        "message": "The requested new archive destination already exists.",
        "hint": "Choose a new path or explicitly open an existing supported writer archive.",
    },
    "PHMT-E330": {
        "message": "The native feature payload has invalid structure, provenance or atom maps.",
        "hint": "Preserve the original input and review the declared source axis, complete inventory and finite metadata.",
    },
    "PHMT-E331": {
        "message": "This native feature payload format or scientific profile is unsupported.",
        "hint": "Select the documented native profile explicitly; historical snapshots and modeled sites have separate readers.",
    },
    "PHMT-E332": {
        "message": "Native feature quantities or geometry failed payload validation.",
        "hint": "Inspect the retained cause and explicit quantity fields, units, shapes and charge signs.",
    },
    "PHMT-E333": {
        "message": "The native feature payload exceeds its bounded admission profile.",
        "hint": "Use at most 256 atoms, 64 features and 2 MiB of payload bytes, with bounded finite provenance.",
    },
    "PHMT-E334": {
        "message": "A required feature family was not declared evaluated in this native payload.",
        "hint": "Inspect retained evaluation coverage; missing families require explicit new extraction.",
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
