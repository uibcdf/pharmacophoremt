from __future__ import annotations
from pathlib import Path
from .meta import DOC_URL, ISSUES_URL, API_URL

PACKAGE_ROOT = Path(__file__).resolve().parents[3]

META = {
    "doc_url": DOC_URL,
    "issues_url": ISSUES_URL,
    "api_url": API_URL,
}

CATALOG = {
    "metadata": {
        "namespace": "PHMT",
        "name": "PharmacophoreMT",
    },
    "signals": {
        "pharmacophoremt.io.pharmer.from_pharmer": {
            "tags": ["io", "pharmer", "read"],
        },
        "pharmacophoremt.io.pharmer.to_pharmer": {
            "tags": ["io", "pharmer", "write"],
        },
        "pharmacophoremt.interaction_site.InteractionSite": {
            "tags": ["core", "interaction_site"],
        },
    },
    "warnings": {
        "UnitConsistencyWarning": {
            "code": "PHMT-W101",
            "message": "Possible unit inconsistency in {interaction_site}. Coordinates should be {expected_unit}.",
        },
    },
    "errors": {
        "InvalidInteractionSiteError": {
            "code": "PHMT-E101",
            "message": "Invalid interaction site configuration: {reason}.",
        },
        "LibraryNotFoundError": {
            "code": "PHMT-E001",
            "message": "Optional library '{library}' is required for this operation. Please install it via 'pip install {pypi}' or 'conda install {conda}'.",
        }
    }
}

CODES = {
    "UnitConsistencyWarning": CATALOG["warnings"]["UnitConsistencyWarning"]["code"],
    "InvalidInteractionSiteError": CATALOG["errors"]["InvalidInteractionSiteError"]["code"],
    "LibraryNotFoundError": CATALOG["errors"]["LibraryNotFoundError"]["code"],
}

SIGNALS = CATALOG["signals"]
