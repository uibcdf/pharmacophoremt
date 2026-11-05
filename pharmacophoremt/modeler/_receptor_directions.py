"""Receive cached direction evidence for pharmacophoric choices, without molecules."""

import numpy as np

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError

_CODES = {
    "site_roles": {0: "donor", 1: "acceptor"},
    "site_models": {
        0: "unsupported",
        1: "observed_donor_hydrogen",
        2: "carbonyl_trigonal",
        3: "aromatic_nitrogen_bisector",
        4: "nitrile_linear",
    },
    "status": {0: "unsupported", 1: "defined", 2: "undefined"},
}


def _require(condition, reason):
    if not condition:
        raise ArgumentError(argument="acceptor_directions", reason=reason)


def _integers(value, shape=None):
    values = np.asarray(value)
    _require(
        values.dtype.kind in "iu" and (shape is None or values.shape == shape),
        "require typed integer correspondence arrays of the declared shape",
    )
    return values


def _receive(inventory, cache, position):
    _require(isinstance(cache, dict), "provide a native MolSysMT direction cache")
    _require(
        cache["schema"] == "molsysmt.hbond_site_directions@1"
        and cache["method"] == "ideal_local_geometry"
        and cache["site_method"] == "smarts_donor_acceptor",
        "unsupported cached direction schema or scientific method",
    )
    _require(
        isinstance(cache["parameters"]["pbc"], (bool, np.bool_))
        and not cache["parameters"]["pbc"],
        "this experimental profile requires explicitly nonperiodic geometry",
    )
    for name, expected in _CODES.items():
        _require(
            {int(k): v for k, v in cache["codes"][name].items()} == expected,
            "unknown cached numeric code meanings",
        )
    source = _integers(cache["atom_source_indices"])
    _require(
        source.ndim == 1 and np.array_equal(source, np.arange(len(source))),
        "require the original canonical source axis",
    )
    selected = _integers(cache["selected_atom_indices"])
    _require(
        selected.ndim == 1
        and len(np.unique(selected)) == len(selected)
        and np.isin(selected, source).all(),
        "invalid cached source selection",
    )
    _require(
        np.array_equal(np.sort(selected), np.sort(inventory["selected_atom_indices"])),
        "feature and direction caches declare different atom selections",
    )
    frames = _integers(cache["evaluated_structure_indices"])
    _require(
        frames.ndim == 1 and np.all(frames >= 0) and position < len(frames),
        "invalid requested structure position",
    )
    _require(
        frames[position] == inventory["structure_index"],
        "selected structure position differs from feature frame",
    )
    state = cache["chemical_state_index"]
    _require(
        not isinstance(state, (bool, np.bool_))
        and isinstance(state, (int, np.integer))
        and state >= 0,
        "invalid resolved chemical state",
    )
    recognition = inventory["recognition"].get("hydrogen_bond")
    _require(
        isinstance(recognition, dict),
        "retain original hydrogen_bond recognition metadata in the feature cache",
    )
    sites = cache["sites"]
    for name in [
        "method",
        "chemical_state_index",
        "software",
        "assume_complete_connectivity",
        "method_reference",
        "smarts_patterns",
        "profile",
        "method_definition",
    ]:
        _require(
            detached(recognition.get(name)) == detached(sites.get(name)),
            "feature and direction caches declare different chemical recognition",
        )
    _require(
        sites["method"] == cache["site_method"]
        and sites["chemical_state_index"] == state,
        "incoherent cached recognition/state",
    )
    _require(
        cache["assume_complete_connectivity"] == sites["assume_complete_connectivity"],
        "incoherent declared connectivity assumption",
    )
    _require(
        isinstance(cache["software"], dict)
        and isinstance(cache["software"].get("molsysmt"), str)
        and bool(cache["software"]["molsysmt"])
        and cache["software"]["molsysmt"] == sites["software"]["molsysmt"],
        "missing or inconsistent original provider version",
    )
    selector = inventory["chemical_state"]
    if selector == "reference":
        _require(state == 0, "reference feature cache requires resolved state zero")
    elif isinstance(selector, (int, np.integer)):
        _require(state == selector, "resolved state differs from feature selector")
    for name in [
        "atom_source_indices",
        "selected_atom_indices",
        "donor_hydrogen_pairs",
        "acceptor_atom_indices",
    ]:
        first, second = _integers(cache[name]), _integers(sites[name])
        metadata = np.asarray(recognition[name])
        # get_features detaches recognition as JSON-compatible metadata: an
        # empty (0,2) participant table becomes []. Native geometry stays typed.
        if metadata.size == 0:
            _require(first.size == 0, "missing recognition participants")
            third = np.empty(first.shape, dtype=first.dtype)
        else:
            third = _integers(metadata)
        if name == "selected_atom_indices":
            first, second, third = np.sort(first), np.sort(second), np.sort(third)
        _require(
            np.array_equal(first, second) and np.array_equal(first, third),
            "inconsistent cached recognition participants/source axis",
        )
    anchors = _integers(cache["site_atom_indices"])
    _require(
        anchors.ndim == 1 and np.isin(anchors, source).all(),
        "invalid cached site anchors",
    )
    n = len(anchors)
    roles = _integers(cache["site_roles"], (n,))
    models = _integers(cache["site_models"], (n,))
    statuses = _integers(cache["status"], (len(frames), n))
    _require(
        set(roles.tolist()) <= {0, 1}
        and set(models.tolist()) <= set(_CODES["site_models"])
        and set(statuses.ravel().tolist()) <= {0, 1, 2},
        "unknown cached role/model/status",
    )
    pairs = _integers(cache["donor_hydrogen_pairs"])
    acceptors = _integers(cache["acceptor_atom_indices"])
    _require(
        pairs.shape == (int(sum(roles == 0)), 2)
        and acceptors.ndim == 1
        and len(np.unique(acceptors)) == len(acceptors)
        and np.isin(pairs, source).all(),
        "invalid cached donor/acceptor participant tables",
    )
    _require(
        np.array_equal(roles, [0] * len(pairs) + [1] * len(acceptors))
        and np.array_equal(anchors, np.concatenate([pairs[:, 0], acceptors])),
        "site roles/anchors disagree with chemical participants",
    )
    offsets = _integers(cache["support_atom_offsets"], (n + 1,))
    support = _integers(cache["support_atom_indices"])
    _require(
        support.ndim == 1
        and np.isin(support, source).all()
        and offsets[0] == 0
        and offsets[-1] == len(support)
        and np.all(np.diff(offsets) >= 1),
        "malformed cached support CSR",
    )
    for site in range(n):
        atoms = support[offsets[site] : offsets[site + 1]]
        _require(
            atoms[0] == anchors[site] and len(np.unique(atoms)) == len(atoms),
            "invalid support anchor/membership",
        )
        _require((roles[site] == 0) == (models[site] == 1), "incoherent role/model")
        _require(
            np.all(statuses[:, site] == 0)
            if models[site] == 0
            else np.all(statuses[:, site] != 0),
            "incoherent supported/undefined status",
        )
        if roles[site] == 0:
            _require(
                np.array_equal(atoms, pairs[site]),
                "donor support differs from its indexed pair",
            )
        if models[site] == 2:
            _require(len(atoms) in (2, 3), "invalid carbonyl support multiplicity")
            _require(
                len(atoms) == 3 or np.all(statuses[:, site] == 2),
                "defined carbonyl directions require plane support",
            )
    directions = np.asarray(cache["directions"], dtype=float)
    _require(
        directions.ndim == 2
        and directions.shape[1] == 3
        and np.isfinite(directions).all()
        and np.allclose(np.linalg.norm(directions, axis=1), 1, atol=1e-12, rtol=0),
        "require finite normalized cached directions",
    )
    count = len(directions)
    _require(
        puw.is_quantity(cache["origins"]),
        "cached origins must be native length quantities",
    )
    try:
        origins = np.asarray(puw.get_value(cache["origins"], to_unit="nm"))
        scale = puw.get_value(
            puw.quantity(1, cache["units"]["origins"]),
            to_unit=puw.get_unit(cache["origins"]),
        )
    except Exception as error:
        raise ArgumentError(
            argument="acceptor_directions",
            reason="invalid origin length/unit declaration",
        ) from error
    _require(
        origins.shape == (count, 3)
        and np.isfinite(origins).all()
        and np.isclose(scale, 1, atol=1e-12, rtol=0)
        and cache["units"]["directions"] == "dimensionless",
        "inconsistent cached geometry/declared units",
    )
    positions = _integers(cache["direction_structure_positions"], (count,))
    site_indices = _integers(cache["direction_site_indices"], (count,))
    local = _integers(cache["direction_indices"], (count,))
    expected = [
        (p, s, k)
        for p in range(len(frames))
        for s in range(n)
        if statuses[p, s] == 1
        for k in range(2 if models[s] == 2 else 1)
    ]
    _require(
        list(
            zip(positions.tolist(), site_indices.tolist(), local.tolist(), strict=True)
        )
        == expected,
        "invalid sparse position/site/local-direction correspondence",
    )
    _require(
        np.array_equal(
            _integers(cache["direction_structure_indices"], (count,)),
            [int(frames[p]) for p, _, _ in expected],
        ),
        "sparse source frames disagree with requested positions",
    )
    image_offsets = _integers(cache["image_offsets"], (count + 1,))
    images = _integers(cache["image_vectors"])
    lengths = [int(offsets[s + 1] - offsets[s]) for _, s, _ in expected]
    _require(
        image_offsets[0] == 0
        and np.array_equal(np.diff(image_offsets), lengths)
        and images.shape == (sum(lengths), 3)
        and not np.any(images),
        "invalid nonperiodic image packing",
    )
    for i, (p, s, k) in enumerate(expected):
        if k:
            _require(
                np.allclose(origins[i], origins[i - k], atol=1e-12, rtol=0),
                "alternative directions have different origins",
            )
    admitted, omitted, seen = {}, {}, set()
    provider = {
        key: cache[key]
        for key in [
            "schema",
            "method",
            "site_method",
            "chemical_state_index",
            "software",
            "parameters",
            "method_reference",
            "attribution",
        ]
        if key in cache
    }
    provider["recognition"] = {
        key: sites[key]
        for key in [
            "method",
            "profile",
            "method_definition",
            "method_reference",
            "evidence",
            "software",
            "attribution",
        ]
        if key in sites
    }
    for index, feature in enumerate(inventory["features"]):
        if feature["kind"] != "hb acceptor":
            continue
        _require(
            len(feature["atom_indices"]) == 1,
            "acceptor features require one source anchor",
        )
        anchor = int(feature["atom_indices"][0])
        _require(anchor not in seen, "duplicate acceptor feature anchor")
        seen.add(anchor)
        found = np.flatnonzero((roles == 1) & (anchors == anchor))
        _require(len(found) == 1, "feature acceptor missing from provider recognition")
        site = int(found[0])
        model, status = int(models[site]), int(statuses[position, site])
        context = dict(
            provider_site_index=site,
            site_model=model,
            status=status,
            source_structure_position=position,
            source_structure_index=int(frames[position]),
            support_atom_indices=support[offsets[site] : offsets[site + 1]],
        )
        if model != 2 or status != 1:
            reason = (
                "unsupported_acceptor_geometry"
                if model == 0
                else "undefined_acceptor_geometry"
                if model == 2
                else "outside_carbonyl_profile"
            )
            omitted[index] = dict(
                feature_index=index,
                kind=feature["kind"],
                atom_indices=feature["atom_indices"],
                reason=reason,
                provider_context=context,
            )
            continue
        records = np.flatnonzero((positions == position) & (site_indices == site))
        choices = []
        for record in records:
            _require(
                np.allclose(
                    origins[record],
                    puw.get_value(feature["center"], to_unit="nm"),
                    atol=1e-12,
                    rtol=0,
                ),
                "acceptor origin differs from cached feature center",
            )
            choices.append(
                dict(
                    axis=directions[record],
                    local_direction_index=int(local[record]),
                    provider_record_index=int(record),
                    evidence=dict(
                        provider=provider,
                        context=context,
                        origin=cache["origins"][record],
                    ),
                )
            )
        admitted[index] = choices
    return dict(admitted=admitted, omitted=omitted)


def cached_carbonyl_choices(inventory, cache, position):
    """Receive versioned cached evidence; retain native causes on malformed input."""
    try:
        return _receive(inventory, cache, position)
    except ArgumentError:
        raise
    except (
        KeyError,
        TypeError,
        ValueError,
        IndexError,
        AttributeError,
        OverflowError,
    ) as error:
        raise ArgumentError(
            argument="acceptor_directions", reason="malformed native direction cache"
        ) from error
