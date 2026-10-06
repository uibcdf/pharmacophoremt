"""Declared analytical workloads; chemistry/rigid motions belong to MolSysMT."""

import json
from copy import deepcopy
from pathlib import Path

from devtools.rigid_consensus_cases import build_case, load_cases
from devtools.rigid_refinement_cases import build_refinement_case, load_refinement_cases

ROOT = Path(__file__).resolve().parents[1]
WORKLOADS_PATH = ROOT / "tests/data/rigid_refinement_workloads.json"
INPUT_FILES = (
    WORKLOADS_PATH,
    ROOT / "tests/data/rigid_refinement_cases.json",
    ROOT / "tests/data/rigid_consensus_cases.json",
)


def load_workloads():
    """Expand declared overrides, preserving original control expectations."""
    plan = json.loads(WORKLOADS_PATH.read_text())
    if plan.get("schema") != "pharmacophoremt.refinement_workloads@1":
        raise ValueError("unsupported refinement workload schema")
    base = {case["case_id"]: case for case in load_refinement_cases()}
    molecular = {case["case_id"]: case for case in load_cases()}
    workloads = []
    for entry in plan["workloads"]:
        case = deepcopy(base[entry["base_case"]]) if "base_case" in entry else {}
        case["parameters"] = dict(
            case.get("parameters", {}), **entry.get("parameters", {})
        )
        case.update(
            deepcopy({key: val for key, val in entry.items() if key != "parameters"})
        )
        case.setdefault("features", ["hb donor"])
        if "molecular_case_id" in case:
            case["molecular_case"] = deepcopy(molecular[case["molecular_case_id"]])
            case["features"] = case["molecular_case"]["parameters"]["features"]
        workloads.append(case)
    if not workloads or len({case["case_id"] for case in workloads}) != len(workloads):
        raise ValueError("workload identities must be nonempty and unique")
    return workloads


def build_workload(case):
    """Build prepared fragment controls with the existing provider-based tools."""
    if "molecular_case" in case:
        return [
            entry["molecular_system"] for entry in build_case(case["molecular_case"])
        ]
    reference, source = build_refinement_case(case)
    if case.get("source_motion") == "rotate_translate":
        import molsysmt as msm
        import numpy as np

        from pharmacophoremt import pyunitwizard as puw

        source = msm.structure.rotate(
            source,
            rotation=np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]),
            rotation_center=puw.quantity([0, 0, 0], "nm"),
            in_place=False,
        )
        source = msm.structure.translate(
            source,
            translation=puw.quantity([[[2.0, 1.0, 3.0]]], "nm"),
            in_place=False,
        )
    return reference, source
