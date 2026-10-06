from pharmacophoremt._private.smonitor.exceptions import ArgumentError


def digest_cation_mapping(obj):
    if not isinstance(obj, str) or obj not in {"exact", "containing_center"}:
        raise ArgumentError(
            argument="cation_mapping", reason="choose exact or containing_center"
        )
    return obj
