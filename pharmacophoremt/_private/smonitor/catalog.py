from __future__ import annotations

from pathlib import Path

from .meta import API_URL, DOC_URL, ISSUES_URL

PACKAGE_ROOT = Path(__file__).resolve().parents[2]

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
        "AckreditTrackingWarning": {
            "code": "PHMT-W102",
            "message": "Optional attribution failed at {operation}: {reason}. The scientific result is preserved.",
        },
        "UnitConsistencyWarning": {
            "code": "PHMT-W101",
            "message": "Possible unit inconsistency in {interaction_site}. Coordinates should be {expected_unit}.",
        },
    },
    "exceptions": {
        "InvalidInteractionSiteError": {
            "code": "PHMT-E101",
            "message": "Invalid interaction site configuration: {reason}.",
        },
        "LibraryNotFoundError": {
            "code": "PHMT-E001",
            "message": "Optional library '{library}' is required for this operation. Please install it via 'pip install {pypi}' or 'conda install {conda}'.",
        },
        "ArgumentError": {
            "code": "PHMT-E102",
            "message": "Invalid '{argument}': {reason}.",
        },
        "PoseEvaluationError": {
            "code": "PHMT-E103",
            "message": "Cannot evaluate pose '{pose_id}' at {stage}: {reason}.",
        },
        "ProviderCapabilityError": {
            "code": "PHMT-E104",
            "message": "MolSysMT does not provide the required capability '{capability}'.",
        },
        "SearchLimitError": {
            "code": "PHMT-E105",
            "message": "Rigid search reached its limit of {max_trials} trials after {n_trials} candidate products; the best possible fit remains unresolved.",
        },
        "ConsensusLimitError": {
            "code": "PHMT-E106",
            "message": "Consensus assignment requires {matrix_entries} matrix entries, exceeding its limit of {max_matrix_entries}; matching remains unresolved.",
        },
        "CliqueLimitError": {
            "code": "PHMT-E107",
            "message": "Clique consensus requires {observed} {resource} at stage '{stage}', exceeding its limit of {limit}; hypothesis discovery remains unresolved.",
        },
    },
}

CODES = {
    entry["code"]: {"message": entry["message"]}
    for group in ("exceptions", "warnings")
    for entry in CATALOG[group].values()
}

SIGNALS = CATALOG["signals"]
