"""Pharmacophoric exclusion spheres constructed from cached heavy-atom geometry."""

from copy import deepcopy

import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_feature_inventory,
    digest_radius,
)
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt._version import __version__
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere

METHOD = "fixed_radius_heavy_atom_exclusions@1"


@signal(tags=["modeling", "excluded_volume"])
@arg_digest()
@attributed("numpy", "pyunitwizard")
def get_excluded_volume_sites(feature_inventory, *, radius):
    """Build independent exclusion sites from an existing heavy-atom inventory.

    Parameters
    ----------
    feature_inventory : dict
        Native ``get_features(..., features=['included volume'])`` result.
        Only singleton heavy-atom records are accepted. Empty inventories yield
        an empty site list; missing or chemical-only inventories are not a
        replacement for heavy-atom extraction.
    radius : length quantity or explicit-unit str
        Caller-selected positive finite scalar radius shared by the sites.
        There is no default, physical-radius assignment or ligand-based pruning.

    Returns
    -------
    dict
        ``interaction_sites`` contains independent excluded-volume Sphere sites,
        with weight zero and source correspondence. ``report`` is detached JSON
        construction provenance, including source inventory and any original
        cached attribution. Optional attribution credits only construction.

    Notes
    -----
    No molecular access, recognition, chemistry preparation or periodic imaging
    occurs here. The inventory's source/frame identity remains a caller
    declaration. Obtain coordinates, selections and any physical atomic radii
    through MolSysMT. A uniform sphere radius is a pharmacophoric hypothesis,
    not a van der Waals overlap or force-field model.

    Add these sites to a query with positive sites in the same coordinate frame
    using ``Pharmacophore.add_interaction_site``. The current PoseEvaluator vetoes
    candidate heavy-atom centers strictly inside an exclusion. Radius equality
    is permitted; exclusions contribute no weight to positive fit. Essential or
    optional flags do not soften that veto. An exclusion-only query is not a
    valid PoseEvaluator query. No global site indices exist until composition.

    Examples
    --------
    >>> inventory = get_features(receptor, features=['included volume'])
    >>> excluded = get_excluded_volume_sites(inventory, radius='0.10 nm')
    >>> for site in excluded['interaction_sites']:
    ...     query.add_interaction_site(site)
    """
    if feature_inventory is None:
        raise ArgumentError(
            argument="feature_inventory", reason="provide a native heavy-atom inventory"
        )
    digest_feature_inventory(feature_inventory)
    radius = digest_radius(radius)
    seen = set()
    for record in feature_inventory["features"]:
        atoms = record["atom_indices"]
        if (
            record["kind"] != "included volume"
            or len(atoms) != 1
            or list(record.get("geometry_atom_indices", atoms)) != list(atoms)
            or record.get("normal") is not None
            or record.get("direction") is not None
        ):
            raise ArgumentError(
                argument="feature_inventory",
                reason="require singleton included-volume records without orientation",
            )
        atom = int(atoms[0])
        if atom in seen:
            raise ArgumentError(
                argument="feature_inventory", reason="duplicate heavy-atom records"
            )
        seen.add(atom)

    sites, records = [], []
    for feature_index, record in enumerate(feature_inventory["features"]):
        metadata = dict(
            method=METHOD,
            source_feature_index=feature_index,
            atom_indices=list(map(int, record["atom_indices"])),
            structure_index=int(feature_inventory["structure_index"]),
            chemical_state=detached(feature_inventory["chemical_state"]),
            source_definition=feature_inventory["definition"],
        )
        site = InteractionSite(
            Sphere(deepcopy(record["center"]), deepcopy(radius)),
            "excluded volume",
            essential=True,
            weight=0.0,
            metadata=deepcopy(metadata),
        )
        sites.append(site)
        records.append(
            dict(
                local_site_index=feature_index,
                **metadata,
                center=detached(site.center),
                radius=detached(site.radius),
            )
        )
    report = dict(
        schema="pharmacophoremt.excluded_volume_sites@1",
        software={
            "pharmacophoremt": __version__,
            "numpy": np.__version__,
            "pyunitwizard": puw.__version__,
        },
        method=METHOD,
        n_sites=len(sites),
        sites=records,
        radius=detached(radius),
        selected_atom_indices=list(
            map(int, feature_inventory["selected_atom_indices"])
        ),
        structure_index=int(feature_inventory["structure_index"]),
        chemical_state=detached(feature_inventory["chemical_state"]),
        source_inventory=detached(feature_inventory),
        policy=dict(
            radius="caller_declared_uniform",
            physical_radius_assignment=False,
            boundary="candidate_heavy_atom_centers_strictly_inside",
            periodic_imaging="not_performed",
            ligand_pruning="not_performed",
            chemical_preparation="not_performed",
            common_frame="caller_declared",
            site_indices="local_to_returned_list",
            positive_fit_weight=0.0,
        ),
    )
    return dict(interaction_sites=sites, report=report)
