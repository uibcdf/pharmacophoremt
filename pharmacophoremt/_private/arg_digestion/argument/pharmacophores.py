from collections.abc import Mapping

from pharmacophoremt._private.smonitor.exceptions import ArgumentError


def digest_pharmacophores(obj):
    from pharmacophoremt.pharmacophore import Pharmacophore

    if (
        not isinstance(obj, Mapping)
        or not obj
        or any(not isinstance(key, str) or not key.strip() for key in obj)
        or any(not isinstance(value, Pharmacophore) for value in obj.values())
    ):
        raise ArgumentError(
            argument="pharmacophores",
            reason="provide a nonempty named mapping of models",
        )
    return dict(obj)
