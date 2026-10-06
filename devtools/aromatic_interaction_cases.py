"""Declared analytical fixtures and provider profiles for aromatic validation."""

import molsysmt as msm
import numpy as np

from pharmacophoremt import pyunitwizard as puw

PI_PROFILES = (
    ("centroid_angle_offset", "least_squares"),
    ("centroid_angle_offset", "three_atom_plane"),
    ("plane_angle_intersection", "aromatic_cycles"),
    ("plane_angle_intersection", "smarts_5_6"),
)
CATION_PROFILES = (
    ("centroid_angle_offset", "least_squares"),
    ("centroid_distance_offset", "three_atom_plane"),
    ("centroid_distance_angle", "smarts_5_6"),
)
REFERENCE_DOIS = {
    "three_atom_plane": "10.1093/nar/gkab314",
    "aromatic_cycles": "10.1016/j.bpj.2015.08.015",
    "smarts_5_6": "10.1186/s13321-021-00548-6",
}


def ring_coordinates():
    theta = np.arange(6) * np.pi / 3
    return np.column_stack((0.14 * np.cos(theta), 0.14 * np.sin(theta), np.zeros(6)))


def build_case(case="parallel", *, unit="nm", transform=False):
    """Prepare declared chemistry/coordinates with public MolSysMT operations."""
    ring = ring_coordinates()
    if case in {"parallel", "edge", "repeated"}:
        other = ring if case != "edge" else ring[:, [2, 0, 1]]
        xyz = np.vstack((ring, other + [0, 0, 0.35]))
        smiles = "c1ccccc1.c1ccccc1"
        if case == "repeated":
            xyz = np.vstack((xyz, ring + [0, 0, -0.35]))
            smiles += ".c1ccccc1"
        ligand, partner = list(range(6)), list(range(6, len(xyz)))
    elif case == "atomic_cation":
        xyz = np.vstack(([0, 0, 0.35], ring))
        smiles, ligand, partner = "[Na+].c1ccccc1", [0], list(range(1, 7))
    elif case == "compound_cation":
        xyz = np.vstack(
            ([[-0.05, 0, 0.35], [0, 0, 0.35], [0.05, 0, 0.35], [0, 0.03, 0.35]], ring)
        )
        smiles, ligand, partner = (
            "NC(=[NH2+])N.c1ccccc1",
            list(range(4)),
            list(range(4, 10)),
        )
    else:
        raise ValueError(case)
    if transform:
        xyz = xyz @ np.array([[0.0, -1, 0], [1, 0, 0], [0, 0, 1]]).T + [2, 1, -3]
    if unit == "angstrom":
        xyz = xyz * 10
    elif unit != "nm":
        raise ValueError(unit)
    source = msm.convert(
        msm.convert("smiles:" + smiles, to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
    )
    source.structures.append(coordinates=puw.quantity([xyz], unit))
    return source, ligand, partner


def observe(source, first, second, method, profile, *, family="pi_pi"):
    """Choose explicitly among actual provider strategies; infer no preference."""
    parameters = {}
    if profile == "least_squares":
        parameters = dict(
            distance_threshold=".5 nm",
            angle_threshold="30 degrees",
            offset_threshold=".2 nm",
            planarity_threshold=".02 nm",
        )
    detector = (
        msm.interactions.pi_pi.get_pi_pi_interactions
        if family == "pi_pi"
        else msm.interactions.cation_pi.get_cation_pi_interactions
    )
    return detector(
        source,
        selection=first,
        selection_2=second,
        structure_indices=[0],
        selection_mode="between",
        method=method,
        profile=profile,
        pbc=False,
        **parameters,
    )
