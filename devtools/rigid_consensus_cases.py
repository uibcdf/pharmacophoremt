"""Declared analytical fixtures for tests and opt-in strategy comparison."""

import json
from copy import deepcopy
from pathlib import Path

CASES_PATH = (
    Path(__file__).resolve().parents[1] / "tests/data/rigid_consensus_cases.json"
)


def load_cases(path=CASES_PATH):
    data = json.loads(Path(path).read_text())
    if (
        data.get("schema") != "pharmacophoremt.analytical_rigid_cases@1"
        or data.get("unit") != "nm"
    ):
        raise ValueError("unsupported analytical case schema or unit")
    cases = data["cases"]
    if len({case["case_id"] for case in cases}) != len(cases):
        raise ValueError("analytical case identities must be unique")
    return deepcopy(cases)


def build_case(case):
    """Use public MolSysMT tools to build declared chemistry/frames and motion."""
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    def system(smiles, coordinates):
        source = msm.convert(
            msm.convert("smiles:" + smiles, to_form="rdkit.Mol"),
            to_form="molsysmt.MolSys",
        )
        source.structures.append(coordinates=puw.quantity([coordinates], "nm"))
        return source

    reference = system(case["smiles"], case["reference_coordinates"])
    if case.get("source_motion") == "rotate_translate":
        source = msm.structure.rotate(
            reference,
            rotation=np.array([[0.0, -1, 0], [1, 0, 0], [0, 0, 1]]),
            rotation_center=puw.quantity([0, 0, 0], "nm"),
            in_place=False,
        )
        source = msm.structure.translate(
            source, translation=puw.quantity([[[2.0, 1, 3]]], "nm"), in_place=False
        )
    else:
        source = system(
            case.get("source_smiles", case["smiles"]), case["source_coordinates"]
        )
    return [
        dict(ligand_id="reference", molecular_system=reference),
        dict(ligand_id="source", molecular_system=source),
    ]
