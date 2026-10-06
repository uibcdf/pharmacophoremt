"""Bounded observation-to-shared-feature interpretation for aromatic contacts."""

import molsysmt as msm
import numpy as np

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError

from .features import get_features

_PROFILES = {
    "pi_pi": {
        (
            "centroid_angle_offset",
            "least_squares",
        ): "unweighted_orthogonal_least_squares",
        (
            "centroid_angle_offset",
            "three_atom_plane",
        ): "cross_of_first_three_basis_member_atoms",
        (
            "plane_angle_intersection",
            "aromatic_cycles",
        ): "cross_of_centroid_to_first_two_basis_member_atoms",
        (
            "plane_angle_intersection",
            "smarts_5_6",
        ): "cross_of_centroid_to_first_two_smarts_atoms",
    },
    "cation_pi": {
        (
            "centroid_angle_offset",
            "least_squares",
        ): "unweighted_orthogonal_least_squares",
        (
            "centroid_distance_offset",
            "three_atom_plane",
        ): "cross_of_first_three_basis_member_atoms",
        (
            "centroid_distance_angle",
            "smarts_5_6",
        ): "cross_of_centroid_to_first_two_smarts_atoms",
    },
}


def observation_state(interactions, kind):
    """Require a known recognition/profile declaration, retaining original geometry."""
    parameters = interactions.parameters
    state = parameters.get("chemical_state_index")
    profile = (parameters.get("method"), parameters.get("profile"))
    if (
        isinstance(state, (bool, np.bool_))
        or not isinstance(state, (int, np.integer))
        or state < 0
        or profile not in _PROFILES[kind]
        or parameters.get("plane_method") != _PROFILES[kind].get(profile)
    ):
        raise ArgumentError(
            argument="interactions",
            reason="unsupported aromatic observation profile/state contract",
        )
    if profile[1] == "smarts_5_6":
        reference = parameters.get("method_reference")
        valid = (
            parameters.get("participant_definition")
            == "prolif_default_5_6_membered_ring_smarts"
            and isinstance(reference, dict)
            and reference.get("version") == "2.2.2"
        )
    else:
        valid = (
            parameters.get("participant_definition") == "stored_aromatic_bonds"
            and parameters.get("recognition_rule_version")
            == "stored_aromatic_bond_cycles@1"
            and parameters.get("ring_method") == "minimum_cycle_basis"
        )
        if kind == "cation_pi":
            valid = valid and (
                parameters.get("charge_definition") == "formal_charge"
                and parameters.get("charge_rule_version") == "formal_charge_centers@1"
                and parameters.get("charge_source") == "chemical_states.formal_charge"
            )
    if not valid:
        raise ArgumentError(
            argument="interactions",
            reason="unsupported aromatic participant recognition contract",
        )
    return int(state)


def ligand_role(relation, ligand):
    """Preserve whole observed participants and their original role orientation."""
    expected = (
        {"ring_a", "ring_b"}
        if relation["interaction_type"] == "pi_pi"
        else {"cation", "ring"}
    )
    participants = relation["participants"]
    roles = {part["role"]: tuple(part["atom_indices"]) for part in participants}
    if len(participants) != 2 or set(roles) != expected:
        raise ArgumentError(
            argument="interactions", reason="unexpected aromatic participant roles"
        )
    members = [set(atoms) for atoms in roles.values()]
    if any(not atoms for atoms in members) or members[0] & members[1]:
        raise ArgumentError(
            argument="interactions",
            reason="aromatic participants must be nonempty and disjoint",
        )
    if any(atoms & ligand and not atoms <= ligand for atoms in members):
        raise ArgumentError(
            argument="ligand_selection",
            reason="an aromatic/cation participant crosses the selection boundary",
        )
    selected = [role for role, atoms in roles.items() if set(atoms) <= ligand]
    if len(selected) != 1:
        raise ArgumentError(
            argument="interactions",
            reason="aromatic contact must cross the ligand boundary",
        )
    role = selected[0]
    return role, roles[role]


def feature_inventory(source, selected, ligand_indices, structure_index):
    """Extract only the shared families needed by the selected ligand roles."""
    ligand = set(ligand_indices.tolist())
    requested = set()
    kinds = set()
    for index in np.unique(selected.to_dict()["relation_indices"]):
        relation = selected.relation(int(index))
        kind = relation["interaction_type"]
        if kind not in _PROFILES:
            continue
        kinds.add(kind)
        role, _ = ligand_role(relation, ligand)
        requested.add("positive charge" if role == "cation" else "aromatic ring")
    states = {observation_state(selected, kind) for kind in kinds}
    if len(states) != 1:
        raise ArgumentError(
            argument="interactions",
            reason="aromatic observations must resolve one state",
        )
    return get_features(
        source,
        selection=ligand_indices,
        structure_index=structure_index,
        chemical_state=states.pop(),
        features=sorted(requested),
    )


def mapped_feature(inventory, relation, ligand, cation_mapping, *, profile):
    """Match membership exactly or explicitly map an atomic cation into one center."""
    role, atoms = ligand_role(relation, ligand)
    kind = "positive charge" if role == "cation" else "aromatic ring"
    exact = [
        record
        for record in inventory["features"]
        if record["kind"] == kind and set(record["atom_indices"]) == set(atoms)
    ]
    policy = "exact"
    if (
        not exact
        and role == "cation"
        and cation_mapping == "containing_center"
        and profile == "smarts_5_6"
        and len(atoms) == 1
    ):
        exact = [
            record
            for record in inventory["features"]
            if record["kind"] == kind and set(atoms) < set(record["atom_indices"])
        ]
        policy = "containing_center"
    if len(exact) != 1:
        raise ArgumentError(
            argument="interactions",
            reason="observed aromatic/cation participant does not map uniquely to a shared feature; choose an explicit compatible mapping",
        )
    return exact[0], dict(role=role, observed_atom_indices=list(atoms), policy=policy)


def validate_cation_charge(records, row, record, mapping, source, chemical_state):
    """Validate exact-center charge; retain atomic-reference charge separately."""
    values = records["measurements"].get("cation_charge")
    unit = records["measure_units"].get("cation_charge")
    if values is None or unit is None:
        raise ArgumentError(
            argument="interactions",
            reason="cation observations require charge measurements",
        )
    try:
        observed = float(puw.get_value(puw.quantity(values[row], unit), to_unit="e"))
    except Exception as error:
        raise ArgumentError(
            argument="interactions",
            reason="cation measurements require elementary charge units",
        ) from error
    if mapping["policy"] == "containing_center":
        reference = msm.get(
            source,
            element="atom",
            selection=mapping["observed_atom_indices"],
            chemical_state=chemical_state,
            formal_charge=True,
        )
        reference = np.asarray(
            puw.get_value(reference, to_unit="e")
            if puw.is_quantity(reference)
            else reference,
            dtype=float,
        )
        if reference.shape != (1,) or not np.isfinite(reference).all():
            raise ArgumentError(
                argument="interactions",
                reason="require one declared cation-reference formal charge",
            )
        expected = float(reference[0])
    else:
        expected = float(puw.get_value(record["charge"], to_unit="e"))
    if not np.isfinite(observed) or observed != expected:
        raise ArgumentError(
            argument="interactions", reason="cation charge and shared feature disagree"
        )
