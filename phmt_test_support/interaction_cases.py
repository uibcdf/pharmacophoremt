"""Self-contained analytical case inputs and fresh-process absence controls.

All molecular construction uses public MolSysMT tools. Direct script execution
runs only a named component case and needs no import of test/support namespaces.
"""

import argparse
import importlib.abc
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("aromatic", "collection"))
    _case = parser.parse_args().case

    class NoAckredit(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            if fullname.split(".")[0] == "ackredit":
                raise ModuleNotFoundError("controlled absence", name=fullname)

    sys.meta_path.insert(0, NoAckredit())

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


def aromatic_build_case(case="parallel", *, unit="nm", transform=False):
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


def aromatic_observe(source, first, second, method, profile, *, family="pi_pi"):
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


def collection_build_case():
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


def collection_observe(
    source, ligand, partner, *, include_alternative=True, include_empty=True
):
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


def _aromatic():
    import pharmacophoremt as phmt
    from pharmacophoremt.screening import PoseEvaluator

    assert "ackredit" not in sys.modules
    source, ligand, partner = aromatic_build_case()
    observed = aromatic_observe(
        source, ligand, partner, "plane_angle_intersection", "smarts_5_6"
    )
    with phmt.attribution():
        query = phmt.modeler.from_interactions(source, observed, ligand)
    assert query.metadata["attribution"]["status"] == "unavailable"
    assert (
        PoseEvaluator(query).evaluate(source, selection=ligand)["status"] == "matched"
    )
    assert "ackredit" not in sys.modules


def _collection():
    import pharmacophoremt as phmt
    from pharmacophoremt.modeler import from_interaction_collection
    from pharmacophoremt.screening import PoseEvaluator

    assert "ackredit" not in sys.modules
    source, ligand, partner = collection_build_case()
    analyses = collection_observe(source, ligand, partner)
    with phmt.attribution():
        result = from_interaction_collection(source, analyses, ligand)
    assert result.n_interaction_sites == 9
    assert (
        PoseEvaluator(result).evaluate(source, selection=ligand)["status"] == "matched"
    )
    assert result.metadata["attribution"]["status"] == "unavailable"


if __name__ == "__main__":
    {"aromatic": _aromatic, "collection": _collection}[_case]()
