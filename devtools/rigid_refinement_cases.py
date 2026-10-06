"""Shared analytical donor fixtures for refinement controls and comparisons."""

import json
from copy import deepcopy
from pathlib import Path

CASES_PATH = (
    Path(__file__).resolve().parents[1] / "tests/data/rigid_refinement_cases.json"
)


def load_refinement_cases(path=CASES_PATH):
    data = json.loads(Path(path).read_text())
    if (
        data.get("schema") != "pharmacophoremt.analytical_refinement_cases@1"
        or data.get("unit") != "nm"
    ):
        raise ValueError("unsupported analytical refinement cases")
    return deepcopy(data["cases"])


def build_refinement_case(case):
    """Build declared O–H donor fragments using public MolSysMT conversion."""
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    systems = []
    for side in ("reference", "source"):
        coordinates = []
        centers, directions = case[side + "_centers"], case[side + "_directions"]
        if len(centers) != len(directions):
            raise ValueError("donor center/direction axes disagree")
        for center, direction in zip(centers, directions):
            center, direction = (
                np.asarray(center, dtype=float),
                np.asarray(direction, dtype=float),
            )
            coordinates.extend(
                [center + 0.1 * direction / np.linalg.norm(direction), center]
            )
        smiles = "smiles:" + ".".join(["[2H]O"] * len(centers))
        system = msm.convert(
            msm.convert(smiles, to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
        )
        system.structures.append(coordinates=puw.quantity([coordinates], "nm"))
        systems.append(system)
    return systems
