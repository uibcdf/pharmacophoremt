from collections.abc import Mapping

from pharmacophoremt._private.smonitor.exceptions import ArgumentError


def digest_interaction_collection(obj):
    import molsysmt as msm

    if (
        not isinstance(obj, Mapping)
        or not obj
        or any(not isinstance(key, str) or not key.strip() for key in obj)
        or any(not isinstance(value, msm.Interactions) for value in obj.values())
    ):
        raise ArgumentError(
            argument="interaction_collection",
            reason="provide a nonempty named mapping of native MolSysMT analyses",
        )
    return dict(obj)
