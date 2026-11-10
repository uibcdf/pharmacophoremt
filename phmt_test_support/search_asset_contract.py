"""Declared-family coverage plane for an unshipped search-asset contract study."""

import hashlib

from phmt_test_support.feature_snapshot import FeatureSnapshotStudy, _request


def family_coverage(snapshot, required_families):
    """Inspect recorded evaluation coverage without admitting a query or asset.

    Missing evaluation is unobserved. This deliberately conservative plane
    supplies no optional-feature/count-bound proof and no molecular, quantity,
    geometry, runtime or storage compatibility decision.
    """
    required = _request(required_families)
    if not isinstance(snapshot, FeatureSnapshotStudy):
        raise TypeError("Expected an original FeatureSnapshotStudy")
    description = snapshot.describe()
    coverage = description["coverage"]
    known = {
        family: coverage[family]["count"]
        for family in required
        if family in coverage
        and coverage[family]["status"] in ("completed", "evaluated_empty")
    }
    missing = [family for family in required if family not in known]
    return {
        "scope": "declared completed extraction-family coverage only",
        "required_families": required,
        "captured_request": description["request"]["features"],
        "known_counts": known,
        "unobserved_families": missing,
        "family_coverage_complete": not missing,
        "encoded_sha256": hashlib.sha256(snapshot.to_bytes()).hexdigest(),
        "payload_sha256": description["payload_sha256"],
        "query_admitted": None,
        "match_outcome": None,
        "quantity_semantics_checked": False,
        "molecular_origin_authenticated": False,
    }
