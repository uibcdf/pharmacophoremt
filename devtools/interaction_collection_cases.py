"""Prepared analytical selection exercising five independently detected families."""

import molsysmt as msm
import numpy as np

from devtools.aromatic_interaction_cases import ring_coordinates
from pharmacophoremt import pyunitwizard as puw


def build_case():
    """Declare disconnected controls, not a chemical or biological ligand complex."""
    ring = ring_coordinates()
    coordinates = np.vstack(
        (
            ring,
            [0, 0, 0.7],
            [1.1, 0, 0],
            [1, 0, 0],
            [3, 0, 0],
            ring + [0, 0, 0.35],
            [0.25, 0, 0.7],
            [1.3, 0.1, 0],
            [1.3, 0, 0],
            [3.3, 0, 0],
        )
    )
    source = msm.convert(
        msm.convert(
            "smiles:c1ccccc1.[Na+].[2H]O.C.c1ccccc1.[Cl-].C=O.C", to_form="rdkit.Mol"
        ),
        to_form="molsysmt.MolSys",
    )
    source.structures.append(coordinates=puw.quantity([coordinates], "nm"))
    return source, list(range(10)), list(range(10, 20))


def observe(source, ligand, partner, *, include_alternative=True, include_empty=True):
    """Run independent public detectors; no heterogeneous result concatenation."""
    options = dict(
        selection=ligand,
        selection_2=partner,
        selection_mode="between",
        structure_indices=[0],
        pbc=False,
    )
    analyses = dict(
        hydrophobic=msm.interactions.hydrophobic.get_hydrophobic_interactions(
            source, distance_threshold=".4 nm", **options
        ),
        hbonds=msm.interactions.hbonds.get_hbonds(
            source,
            method="donor_acceptor_distance_angle",
            profile="smarts_donor_acceptor",
            **options,
        ),
        ionic=msm.interactions.ionic.get_ionic_interactions(source, ".3 nm", **options),
        pi_prolif=msm.interactions.pi_pi.get_pi_pi_interactions(
            source, method="plane_angle_intersection", profile="smarts_5_6", **options
        ),
        cation_pi=msm.interactions.cation_pi.get_cation_pi_interactions(
            source, method="centroid_distance_angle", profile="smarts_5_6", **options
        ),
    )
    if include_alternative:
        analyses["pi_molstar"] = msm.interactions.pi_pi.get_pi_pi_interactions(
            source,
            method="centroid_angle_offset",
            profile="three_atom_plane",
            **options,
        )
    if include_empty:
        analyses["ionic_empty"] = msm.interactions.ionic.get_ionic_interactions(
            source, ".01 nm", **options
        )
    return analyses
