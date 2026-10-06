"""Scoped argument contracts for cached hypothesis curation.

Optional edit fields do not weaken required geometry/InteractionSite contracts.
"""

from collections.abc import Sequence
from numbers import Real

import numpy as np

from pharmacophoremt._private.arg_digestion.argument import _contracts
from pharmacophoremt._private.smonitor.exceptions import ArgumentError


def model(obj):
    from pharmacophoremt.interaction_site import InteractionSite
    from pharmacophoremt.pharmacophore import Pharmacophore

    if (
        not isinstance(obj, Pharmacophore)
        or not isinstance(obj.metadata, dict)
        or not isinstance(obj.interaction_sites, list)
        or obj.n_interaction_sites != len(obj.interaction_sites)
        or any(not isinstance(site, InteractionSite) for site in obj.interaction_sites)
    ):
        raise ArgumentError(
            argument="pharmacophore", reason="expected a consistent native model"
        )
    return obj


def indices(obj):
    if isinstance(obj, str) and obj == "all":
        return obj
    if isinstance(obj, (int, np.integer)) and not isinstance(obj, (bool, np.bool_)):
        values = [obj]
    elif isinstance(obj, np.ndarray):
        values = list(obj) if obj.ndim == 1 else None
    elif isinstance(obj, Sequence) and not isinstance(obj, (str, bytes)):
        values = list(obj)
    else:
        values = None
    if values is None or any(
        isinstance(value, (bool, np.bool_))
        or not isinstance(value, (int, np.integer))
        or value < 0
        for value in values
    ):
        raise ArgumentError(
            argument="site_indices",
            reason="expected all or nonnegative integer site indices",
        )
    values = [int(value) for value in values]
    if len(set(values)) != len(values):
        raise ArgumentError(
            argument="site_indices", reason="site indices must be unique"
        )
    return values


def text(obj):
    if obj is not None and not isinstance(obj, str):
        raise ArgumentError(argument="name/reason", reason="expected text or None")
    return obj


def names(obj):
    if obj is None:
        return []
    values = (
        [obj]
        if isinstance(obj, str)
        else list(obj)
        if isinstance(obj, (list, tuple))
        else None
    )
    if values is None or any(
        not isinstance(value, str) or not value.strip() for value in values
    ):
        raise ArgumentError(
            argument="feature_names/shape_names", reason="expected nonempty names"
        )
    return list(dict.fromkeys(values))


def optional_essential(obj):
    return None if obj is None else _contracts.digest_essential(obj)


def optional_weight(obj):
    if obj is None:
        return None
    if not isinstance(obj, Real):
        raise ArgumentError(
            argument="weight", reason="expected a finite nonnegative real scalar"
        )
    return _contracts.digest_weight(obj)


def optional_radius(obj):
    return None if obj is None else _contracts.digest_radius(obj)


def optional_sigma(obj):
    return None if obj is None else _contracts.digest_sigma(obj)


ARGUMENT_DIGESTERS = dict(
    pharmacophore=model,
    site_indices=indices,
    index=indices,
    feature_names=names,
    shape_names=names,
    name=text,
    reason=text,
    essential=optional_essential,
    weight=optional_weight,
    radius=optional_radius,
    sigma=optional_sigma,
    in_place=_contracts.digest_essential,
    skip_digestion=_contracts.digest_essential,
)
