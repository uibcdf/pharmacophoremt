"""Study-only catalog; these IDs are not published PHMT diagnostic codes."""

CODES = {
    "PHMT-ASSET-STUDY-E001": {
        "message": "Provide a nonempty text path for feature-asset opening.",
        "hint": "Opening never creates or repairs a store.",
    },
    "PHMT-ASSET-STUDY-E002": {
        "message": "Provide an exact generation SHA-256 for {argument}.",
        "hint": "Only opening may resolve generation=None once; existing handles stay pinned.",
        "metadata_message": "Review the generation identity.",
        "metadata_hint": "Use the inspected generation; do not infer it from a display label.",
    },
    "PHMT-ASSET-STUDY-E003": {
        "message": "Choose one or more supported classical feature families.",
        "hint": "Missing evaluation must be requested explicitly; it is not an empty result.",
    },
    "PHMT-ASSET-STUDY-E004": {
        "message": "Choose a finite list of distinct, nonempty literal work keys.",
        "hint": "Preserve case, spaces and Unicode; [] selects no occurrences.",
    },
    "PHMT-ASSET-STUDY-E005": {
        "message": "Use nonnegative integer page offsets and limits.",
        "hint": "A zero limit requests no rows; it does not describe the total selected work.",
    },
    "PHMT-ASSET-STUDY-E006": {
        "message": "Provide a retained publication attempt identifier or None for an unlinked publication.",
        "hint": "A retry links existing history and revalidates the candidate; it never rewrites that history.",
    },
}
SIGNALS = {}
