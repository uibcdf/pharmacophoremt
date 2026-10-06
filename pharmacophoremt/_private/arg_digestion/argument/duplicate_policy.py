from pharmacophoremt._private.smonitor.exceptions import ArgumentError


def digest_duplicate_policy(obj):
    if not isinstance(obj, str) or obj not in {"keep", "same_participant"}:
        raise ArgumentError(
            argument="duplicate_policy", reason="choose keep or same_participant"
        )
    return obj
