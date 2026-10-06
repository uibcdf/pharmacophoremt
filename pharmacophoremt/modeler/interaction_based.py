"""Build pharmacophores from already evaluated MolSysMT interactions."""

import molsysmt as msm
import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.arg_digestion.argument._contracts import digest_radius
from pharmacophoremt._private.arg_digestion.argument.cation_mapping import (
    digest_cation_mapping,
)
from pharmacophoremt._private.molsysmt import detached, source_frame
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    ProviderCapabilityError,
)
from pharmacophoremt._version import __version__
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere, SphereAndVector
from pharmacophoremt.pharmacophore import Pharmacophore

from . import _aromatic_interactions as aromatic
from .features import get_features
from .reference_ligand import from_feature_inventory


def _ionic_state(parameters):
    """Validate the bounded provider definition before molecular selections."""
    state = parameters.get("chemical_state_index")
    if (
        parameters.get("participant_definition") != "formal_charge"
        or parameters.get("recognition_rule_version") != "formal_charge_centers@1"
        or parameters.get("charge_source") != "chemical_states.formal_charge"
        or isinstance(state, (bool, np.bool_))
        or not isinstance(state, (int, np.integer))
        or state < 0
    ):
        raise ArgumentError(
            argument="interactions",
            reason="ionic observations require the formal_charge_centers@1 state contract",
        )
    return int(state)


def _ionic_features(molecular_system, interactions, ligand_indices, structure_index):
    """Resolve the supported observation definition through the shared tool."""
    parameters = interactions.parameters
    state = _ionic_state(parameters)
    inventory = get_features(
        molecular_system,
        selection=ligand_indices,
        structure_index=structure_index,
        chemical_state=int(state),
        features=["positive charge", "negative charge"],
    )
    recognition = inventory["recognition"]["formal_charge"]
    if (
        recognition["rule_version"] != parameters["recognition_rule_version"]
        or recognition["chemical_state_index"] != state
    ):
        raise ArgumentError(
            argument="interactions",
            reason="charge recognition and observation state differ",
        )
    return inventory


def _ionic_role(relation, ligand):
    """Require exactly two whole, disjoint charge participants across the boundary."""
    participants = relation["participants"]
    roles = {part["role"]: tuple(part["atom_indices"]) for part in participants}
    if len(participants) != 2 or set(roles) != {"positive", "negative"}:
        raise ArgumentError(
            argument="interactions",
            reason="ionic contacts require positive and negative roles",
        )
    members = {role: set(atoms) for role, atoms in roles.items()}
    if (
        any(not atoms for atoms in members.values())
        or members["positive"] & members["negative"]
    ):
        raise ArgumentError(
            argument="interactions",
            reason="ionic participants must be nonempty and disjoint",
        )
    if any(atoms & ligand and not atoms <= ligand for atoms in members.values()):
        raise ArgumentError(
            argument="ligand_selection",
            reason="a compound charge center crosses the selection boundary",
        )
    ligand_roles = [role for role, atoms in members.items() if atoms <= ligand]
    if len(ligand_roles) != 1:
        raise ArgumentError(
            argument="interactions",
            reason="ionic contact must cross the ligand boundary",
        )
    role = ligand_roles[0]
    return role, roles[role]


@signal(tags=["modeling", "interactions"])
@arg_digest()
@attributed("numpy", "molsysmt", "pyunitwizard")
def from_interactions(
    molecular_system,
    interactions,
    ligand_selection,
    *,
    structure_index=0,
    radius="0.15 nm",
    name=None,
    cation_mapping="exact",
):
    """Construct sites from native hydrophobic, H-bond, ionic and aromatic contacts.

    The caller supplies the same, unchanged molecular system and index space
    used to calculate ``interactions``. Axis checks cannot authenticate origin.
    Only cross-boundary observations involving the selected ligand contribute.
    A ligand donor becomes a directed sphere along its indexed donor-H bond;
    an acceptor or hydrophobic atom becomes a sphere. An ionic ligand participant
    becomes a positive/negative charge sphere at the unweighted centroid of its
    provider-defined geometry members, using the shared ``get_features`` tool.
    Repeated observations of the same participant contribute evidence to one site.

    Parameters
    ----------
    molecular_system : molecular system
        Source accepted by MolSysMT, with the evaluated coordinates intact.
    interactions : molsysmt.Interactions
        Native observations, including evaluated-frame coverage.
    ligand_selection : selection
        MolSysMT selection containing all participating ligand atoms.
    structure_index : int, default=0
        One evaluated frame in the result's local index space.
    radius : length quantity, default='0.15 nm'
        Pharmacophore matching radius; independent of interaction cutoffs.
    name : str, optional
        Model name.
    cation_mapping : {'exact', 'containing_center'}, default='exact'
        For cation-pi observations, require exact shared charge-center membership
        or explicitly map a smaller observed cation into one containing positive
        center. Original reference atoms and charge measurements remain evidence.

    Returns
    -------
    Pharmacophore
        A model retaining source indices, criteria, versions and attribution.
        A covered frame with no qualifying observations yields an empty model.

    Notes
    -----
    This bounded route does not reconstruct periodic images. Nonzero image
    vectors and unsupported interaction kinds raise instead of losing evidence.
    No protonation, hydrogen addition, coordinate generation or repair occurs.
    Ionic observations require ``formal_charge_centers@1`` and their explicit
    chemical-state index. Whole-center membership and charge are checked against
    current recognition. The minimum-contact distance is retained as evidence;
    it is not the sphere center, matching radius or an electrostatic energy.
    Pi-pi and cation-pi ring participants become shared least-squares aromatic
    disks, independently of the detector's recorded plane/profile. Rings must
    match shared membership exactly. Supported upstream profiles and original
    criteria remain distinct from this hypothesis geometry; neither plane-axis
    sign nor an observed ring-normal direction determines a binding vector.

    Examples
    --------
    Given a source complex and native MolSysMT observations in its index space:

    >>> query = from_interactions(source, observations, ligand_selection='molecule_type == "small molecule"')
    """
    radius = digest_radius(radius)
    cation_mapping = digest_cation_mapping(cation_mapping)
    native_type = getattr(msm, "Interactions", None)
    if native_type is None:
        raise ProviderCapabilityError(capability="Interactions")
    if not isinstance(interactions, native_type):
        raise ArgumentError(
            argument="interactions", reason="expected native MolSysMT interactions"
        )
    states = set()
    if "ionic_contact" in interactions.relation_types:
        states.add(_ionic_state(interactions.parameters))
    for kind in ("pi_pi", "cation_pi"):
        if kind in interactions.relation_types:
            states.add(aromatic.observation_state(interactions, kind))
    if len(states) > 1:
        raise ArgumentError(
            argument="interactions",
            reason="observations must resolve one chemical state",
        )
    chemical_state = states.pop() if states else "reference"
    coordinates, ligand_indices = source_frame(
        molecular_system,
        ligand_selection,
        structure_index,
        chemical_state=chemical_state,
    )
    n_structures = msm.get(molecular_system, n_structures=True)
    if (
        interactions.n_atoms != len(coordinates)
        or interactions.n_structures != n_structures
    ):
        raise ArgumentError(
            argument="interactions", reason="source atom/structure axes differ"
        )
    if structure_index not in interactions.evaluated_structure_indices:
        raise ArgumentError(
            argument="structure_index", reason="this frame was not evaluated"
        )
    receptor_indices = np.setdiff1d(np.arange(len(coordinates)), ligand_indices)
    selected = interactions.between_selections(
        ligand_indices, receptor_indices, structure_indices=[structure_index]
    )
    records = selected.to_dict()
    if records["image_vectors"] is not None and np.any(records["image_vectors"]):
        raise ArgumentError(
            argument="interactions",
            reason="nonzero periodic images need a provider-prepared frame",
        )
    model = Pharmacophore(
        name=name, molecular_system=molecular_system, ref_struct=int(structure_index)
    )
    model.metadata = detached(
        {
            "method": "observed_interactions",
            "interaction_method": interactions.method,
            "producer": {"pharmacophoremt": __version__},
            "source_id": interactions.source_id,
            "source_atom_indices": interactions.atom_source_indices,
            "source_structure_indices": interactions.structure_source_indices,
            "evaluated_structure_indices": interactions.evaluated_structure_indices,
            "structure_index": int(structure_index),
            "ligand_atom_indices": ligand_indices,
            "software": interactions.software,
            "parameters": interactions.parameters,
            "execution_records": records["execution_records"],
        }
    )
    sites = {}
    ligand = set(ligand_indices.tolist())
    ionic_inventory = None
    ionic_records = None
    aromatic_inventory = None
    for row, relation_index in enumerate(records["relation_indices"]):
        relation = selected.relation(int(relation_index))
        roles = {
            part["role"]: tuple(part["atom_indices"])
            for part in relation["participants"]
        }
        kind = relation["interaction_type"]
        charge_record = None
        shared_record = None
        participant_mapping = None
        if kind in {"pi_pi", "cation_pi"}:
            if aromatic_inventory is None:
                aromatic_inventory = aromatic.feature_inventory(
                    molecular_system, selected, ligand_indices, structure_index
                )
                model.metadata["aromatic_feature_inventory"] = detached(
                    aromatic_inventory
                )
                model.metadata["aromatic_conversion_policy"] = dict(
                    geometry="shared_classical_geometry@1",
                    ring_membership="exact",
                    cation_mapping=cation_mapping,
                )
            shared_record, participant_mapping = aromatic.mapped_feature(
                aromatic_inventory,
                relation,
                ligand,
                cation_mapping,
                profile=interactions.parameters.get("profile"),
            )
            atoms = tuple(shared_record["atom_indices"])
            feature, direction = shared_record["kind"], None
            if participant_mapping["role"] == "cation":
                aromatic.validate_cation_charge(
                    records,
                    row,
                    shared_record,
                    participant_mapping,
                    molecular_system,
                    aromatic_inventory["chemical_state"],
                )
        elif kind == "ionic_contact":
            role, atoms = _ionic_role(relation, ligand)
            if ionic_inventory is None:
                ionic_inventory = _ionic_features(
                    molecular_system, interactions, ligand_indices, structure_index
                )
                ionic_records = {
                    (record["kind"], frozenset(record["atom_indices"])): record
                    for record in ionic_inventory["features"]
                }
                model.metadata["ionic_feature_inventory"] = detached(ionic_inventory)
            feature, direction = role + " charge", None
            charge_record = ionic_records.get((feature, frozenset(atoms)))
            if charge_record is None:
                raise ArgumentError(
                    argument="interactions",
                    reason="ionic participant does not match current charge recognition",
                )
            atoms = tuple(charge_record["atom_indices"])
            charge_column = records["measurements"].get(role + "_charge")
            charge_unit = records["measure_units"].get(role + "_charge")
            if charge_column is None or charge_unit is None:
                raise ArgumentError(
                    argument="interactions",
                    reason="ionic observations require participant charge measurements",
                )
            try:
                observed_charge = float(
                    puw.get_value(
                        puw.quantity(charge_column[row], charge_unit), to_unit="e"
                    )
                )
            except Exception as error:
                raise ArgumentError(
                    argument="interactions",
                    reason="ionic charge measurements require elementary charge units",
                ) from error
            if observed_charge != float(
                puw.get_value(charge_record["charge"], to_unit="e")
            ):
                raise ArgumentError(
                    argument="interactions",
                    reason="ionic charge measurement and recognition disagree",
                )
        elif kind == "hydrophobic_contact":
            atoms = next(atoms for atoms in roles.values() if set(atoms) <= ligand)
            feature, direction = "hydrophobicity", None
        elif kind == "hbond":
            if any(len(roles[role]) != 1 for role in ("donor", "hydrogen", "acceptor")):
                raise ArgumentError(
                    argument="interactions",
                    reason="expected singleton hydrogen-bond roles",
                )
            if bool(set(roles["donor"]) & ligand) != bool(
                set(roles["hydrogen"]) & ligand
            ):
                raise ArgumentError(
                    argument="ligand_selection",
                    reason="a donor-H participant crosses the selection boundary",
                )
            if set(roles["donor"]) <= ligand and set(roles["hydrogen"]) <= ligand:
                atoms = roles["donor"] + roles["hydrogen"]
                feature = "hb donor"
                direction = coordinates[atoms[1]] - coordinates[atoms[0]]
            elif set(roles["acceptor"]) <= ligand and not set(roles["donor"]) & ligand:
                atoms, feature, direction = roles["acceptor"], "hb acceptor", None
            else:
                raise ArgumentError(
                    argument="ligand_selection",
                    reason="a donor-H participant crosses the selection boundary",
                )
        else:
            raise ArgumentError(
                argument="interactions", reason=f"unsupported interaction kind '{kind}'"
            )
        if (kind == "hydrophobic_contact" and len(atoms) != 1) or (
            feature == "hb donor" and len(atoms) != 2
        ):
            raise ArgumentError(
                argument="interactions",
                reason="expected atomic participants for this definition",
            )
        key = (feature, atoms)
        if key not in sites:
            site_metadata = {
                "atom_indices": [int(atom) for atom in atoms],
                "source_atom_indices": interactions.atom_source_indices[
                    list(atoms)
                ].tolist(),
                "structure_index": int(structure_index),
                "observations": [],
            }
            if shared_record is not None:
                subset = dict(aromatic_inventory, features=[shared_record])
                site = from_feature_inventory(subset, radius=radius).interaction_sites[
                    0
                ]
                site.metadata.update(site_metadata)
                site.metadata.update(
                    detached(
                        dict(
                            source_geometry_atom_indices=interactions.atom_source_indices[
                                shared_record["geometry_atom_indices"]
                            ].tolist(),
                            chemical_state_index=aromatic_inventory["chemical_state"],
                            definition=aromatic_inventory["definition"],
                            conversion_geometry="shared_classical_geometry@1",
                        )
                    )
                )
            else:
                center = (
                    charge_record["center"]
                    if charge_record is not None
                    else puw.quantity(coordinates[atoms[0]], "nm")
                )
                shape = (
                    Sphere(center, radius)
                    if direction is None
                    else SphereAndVector(center, radius, direction)
                )
                site = InteractionSite(
                    shape,
                    feature,
                    metadata=site_metadata,
                )
            if charge_record is not None:
                site.metadata.update(
                    detached(
                        {
                            "geometry_atom_indices": charge_record[
                                "geometry_atom_indices"
                            ],
                            "source_geometry_atom_indices": interactions.atom_source_indices[
                                charge_record["geometry_atom_indices"]
                            ].tolist(),
                            "charge": charge_record["charge"],
                            "chemical_state_index": ionic_inventory["chemical_state"],
                            "definition": ionic_inventory["definition"],
                            "recognition_rule_version": interactions.parameters[
                                "recognition_rule_version"
                            ],
                            "geometry_method": "molsysmt.structure.get_center",
                            "geometry_weighting": "uniform",
                        }
                    )
                )
            sites[key] = site
            model.add_interaction_site(site)
        sites[key].metadata["observations"].append(
            detached(
                {
                    "occurrence_index": records["occurrence_indices"][row],
                    "relation_index": relation_index,
                    "relation": relation,
                    "evidence": records["evidence"][row],
                    **(
                        {"participant_mapping": participant_mapping}
                        if participant_mapping is not None
                        else {}
                    ),
                    "measurements": {
                        key: puw.quantity(values[row], records["measure_units"][key])
                        for key, values in records["measurements"].items()
                    },
                }
            )
        )
    return model
