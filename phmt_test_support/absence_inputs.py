"""Self-contained analytical case inputs and fresh-process absence controls.

All molecular construction uses public MolSysMT tools. Direct script execution
runs only a named component case and needs no import of test/support namespaces.
"""

import argparse
import importlib.abc
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "case", choices=("aligned", "attribution", "excluded_volume", "ionic")
    )
    _case = parser.parse_args().case

    class NoAckredit(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            if fullname.split(".")[0] == "ackredit":
                raise ModuleNotFoundError("controlled absence", name=fullname)

    sys.meta_path.insert(0, NoAckredit())

import molsysmt as msm
import numpy as np

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_ligand
from pharmacophoremt.modeler.features import DEFINITION

COORDINATES = np.array(
    [
        [0, 0, 0],
        [0.15, 0, 0],
        [0.3, 0, 0],
        [0.1, 0.5, 0],
        [0, 0.5, 0],
        [0.3, 0.6, 0],
        [0.3, 0.5, 0],
        [0.05, 0.2, 0.7],
    ]
)

SMILES = "CCC.[2H]O.C=O.[NH4+]"

FAMILIES = ["hydrophobicity", "hb donor", "hb acceptor", "positive charge"]


def system(smiles="CCC.CCC", coordinates=None, unit="nm"):
    source = msm.convert(
        msm.convert("smiles:" + smiles, to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
    )
    if coordinates is None:
        coordinates = [
            [0, 0, 0],
            [0.15, 0, 0],
            [0.30, 0, 0],
            [0, 0.3, 0],
            [0.15, 0.3, 0],
            [0.30, 0.3, 0],
        ]
    source.structures.append(coordinates=puw.quantity([coordinates], unit))
    return source


def reference():
    source = system(SMILES, COORDINATES)
    return source, from_ligand(source, features=FAMILIES, radius="0.02 nm")


def moved(source):
    rotated = msm.structure.rotate(
        source,
        rotation=np.array([[0.0, -1, 0], [1, 0, 0], [0, 0, 1]]),
        rotation_center=puw.quantity([0, 0, 0], "nm"),
        in_place=False,
    )
    return msm.structure.translate(
        rotated, translation=puw.quantity([[[2.0, 1, 3]]], "nm"), in_place=False
    )


def inventory(centers, kinds=None, directions=None, normals=None):
    """Synthetic feature geometry for mathematical controls; no molecular claim."""
    n = len(centers)
    kinds = kinds or ["hb acceptor"] * n
    directions = directions or [None] * n
    normals = normals or [None] * n
    return dict(
        definition=DEFINITION,
        structure_index=0,
        chemical_state="reference",
        selected_atom_indices=list(range(max(1, n))),
        recognition={},
        features=[
            dict(
                kind=kind,
                center=puw.quantity(center, "nm"),
                atom_indices=[i],
                geometry_atom_indices=[i],
                charge=None,
                direction=None
                if direction is None
                else puw.quantity(direction, "dimensionless"),
                normal=None
                if normal is None
                else puw.quantity(normal, "dimensionless"),
            )
            for i, (center, kind, direction, normal) in enumerate(
                zip(centers, kinds, directions, normals)
            )
        ],
    )


def _aligned():
    import pharmacophoremt as phmt

    assert "ackredit" not in sys.modules
    with phmt.attribution():
        result = phmt.modeler.get_aligned_consensus_hypotheses(
            [inventory([[0, 0, 0]]), inventory([[0, 0, 0]])], ligand_ids=["a", "b"]
        )
    assert len(result["hypotheses"]) == 1
    assert result["attribution"]["status"] == "unavailable"
    assert "10.1145/362342.362367" in str(result["attribution"]["host_references"])
    assert "ackredit" not in sys.modules


def _attribution():
    import pharmacophoremt as phmt
    from pharmacophoremt.screening import PoseEvaluator

    source, query = reference()
    with phmt.attribution():
        result = PoseEvaluator(query).evaluate(source)
    assert result["status"] == "matched"
    payload = result["attribution"]
    assert payload["status"] == "unavailable" and payload["references"] is None
    assert payload["host_references"] and not payload["errors"]
    assert "ackredit" not in sys.modules


def _excluded_volume():
    import pharmacophoremt as phmt

    assert "ackredit" not in sys.modules
    inventory = phmt.modeler.get_features(
        system(), selection=[3, 4, 5], features=["included volume"]
    )
    plain = phmt.modeler.get_excluded_volume_sites(inventory, radius=".1 nm")
    assert "ackredit" not in sys.modules
    with phmt.attribution(True):
        result = phmt.modeler.get_excluded_volume_sites(inventory, radius=".1 nm")
    assert result["report"] == plain["report"]
    assert result["attribution"]["status"] == "unavailable"
    assert result["attribution"]["host_references"]
    assert "ackredit" not in sys.modules


def _ionic():
    import pharmacophoremt as phmt
    from pharmacophoremt.screening import PoseEvaluator

    assert "ackredit" not in sys.modules
    import molsysmt as msm

    source = system("[Na+].[Cl-]", [[0, 0, 0], [0.3, 0, 0]])
    observed = msm.interactions.ionic.get_ionic_interactions(
        source, ".31 nm", pbc=False
    )
    with phmt.attribution():
        query = phmt.modeler.from_interactions(source, observed, [0])
    assert query.metadata["attribution"]["status"] == "unavailable"
    assert PoseEvaluator(query).evaluate(source, selection=[0])["status"] == "matched"
    assert "ackredit" not in sys.modules


if __name__ == "__main__":
    {
        "aligned": _aligned,
        "attribution": _attribution,
        "excluded_volume": _excluded_volume,
        "ionic": _ionic,
    }[_case]()
