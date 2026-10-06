"""Single-reference ligand pharmacophores using the shared native inventory."""

import molsysmt as msm
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt._version import __version__
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Disk, Sphere, SphereAndVector
from pharmacophoremt.pharmacophore import Pharmacophore

from .features import CLASSICAL_FEATURES, get_features


@signal(tags=["modeling", "feature_inventory"])
@arg_digest()
@attributed("pyunitwizard")
def from_feature_inventory(feature_inventory, *, radius="0.15 nm", name=None):
    """Construct a query from an existing native feature inventory.

    Parameters
    ----------
    feature_inventory : dict
        Nonempty native get_features result, retaining explicit-unit geometry.
        Classical features and included heavy-atom volumes are supported.
    radius : length quantity, default='0.15 nm'
        Emitted shape radius, independent of chemical recognition.
    name : str, optional
        Query name.

    Returns
    -------
    Pharmacophore
        Essential sites of weight one, with detached inventory provenance.

    Notes
    -----
    No molecular access, recognition or fitting occurs. Inventory origin and
    coordinate frame remain caller declarations. Native quantity objects are
    required; this is not a decoder for detached inventory JSON. Previously
    captured attribution is retained without crediting another recognition run.

    Examples
    --------
    >>> query = from_feature_inventory(get_features(prepared_ligand))
    """
    if feature_inventory is None or not feature_inventory["features"]:
        raise ArgumentError(
            argument="feature_inventory", reason="require a nonempty native inventory"
        )
    model = Pharmacophore(name=name, ref_struct=feature_inventory["structure_index"])
    model.metadata = detached(
        dict(
            method="feature_inventory_query@1",
            definition=feature_inventory["definition"],
            structure_index=feature_inventory["structure_index"],
            selected_atom_indices=feature_inventory["selected_atom_indices"],
            chemical_state=feature_inventory["chemical_state"],
            recognition=feature_inventory["recognition"],
            source_inventory=feature_inventory,
            emitted_radius=radius,
        )
    )
    if "attribution" in feature_inventory:
        model.metadata["source_attribution"] = detached(
            feature_inventory["attribution"]
        )
    for record in feature_inventory["features"]:
        normal, direction = record.get("normal"), record.get("direction")
        if (record["kind"] == "aromatic ring") != (normal is not None) or (
            record["kind"] == "hb donor"
        ) != (direction is not None):
            raise ArgumentError(
                argument="feature_inventory",
                reason="feature kind and orientation geometry disagree",
            )
        if normal is not None:
            shape = Disk(
                record["center"], puw.get_value(normal, to_unit="dimensionless"), radius
            )
        elif direction is not None:
            shape = SphereAndVector(record["center"], radius, direction)
        else:
            shape = Sphere(record["center"], radius)
        model.add_interaction_site(
            InteractionSite(
                shape,
                record["kind"],
                metadata=detached(
                    dict(
                        atom_indices=record["atom_indices"],
                        geometry_atom_indices=record.get(
                            "geometry_atom_indices", record["atom_indices"]
                        ),
                        structure_index=feature_inventory["structure_index"],
                        charge=record.get("charge"),
                    )
                ),
            )
        )
    return model


@signal(tags=["modeling", "reference_ligand"])
@arg_digest()
@attributed("numpy", "molsysmt", "pyunitwizard")
def from_ligand(
    molecular_system,
    *,
    selection="all",
    structure_index=0,
    chemical_state="reference",
    features=CLASSICAL_FEATURES,
    radius="0.15 nm",
    name=None,
):
    """Build a classical query from one prepared, experimentally placed ligand.

    Parameters
    ----------
    molecular_system : molecular system
        Prepared source accepted by MolSysMT; its coordinates are left intact.
    selection : MolSysMT selection, default='all'
        Ligand atoms; use an explicit selection for a complex.
    structure_index : int, default=0
        Reference coordinate frame.
    chemical_state : str or int, default='reference'
        MolSysMT chemical state for recognition.
    features : sequence of str
        Families requested from :func:`get_features`.
    radius : length quantity, default='0.15 nm'
        Matching tolerance, independent of recognition or interaction cutoffs.
    name : str, optional
        Query name.

    Returns
    -------
    Pharmacophore
        Essential, equally weighted sites: atomic/group spheres, donor-H directed
        spheres, and aromatic disks. Geometry, state and recognition are recorded.

    Notes
    -----
    A reference query is a hypothesis, not evidence that every chemical feature
    contributes to binding. Callers may edit essential flags and weights. Empty
    inventories raise. This function performs no alignment or multi-ligand consensus.

    Examples
    --------
    >>> query = from_ligand(prepared_ligand, features=['aromatic ring', 'hb acceptor'])
    >>> result = PoseEvaluator(query).evaluate(prepared_ligand)
    """
    inventory = get_features(
        molecular_system,
        selection=selection,
        structure_index=structure_index,
        chemical_state=chemical_state,
        features=features,
    )
    if not inventory["features"]:
        raise ArgumentError(
            argument="features",
            reason="no requested chemical participants in the selected reference",
        )
    model = from_feature_inventory(inventory, radius=radius, name=name)
    model.molecular_system = molecular_system
    model.metadata.update(
        method="reference_ligand",
        software={"pharmacophoremt": __version__, "molsysmt": msm.__version__},
    )
    return model
