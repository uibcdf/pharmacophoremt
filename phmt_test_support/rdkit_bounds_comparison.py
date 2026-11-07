"""Declared fixed-conformer comparison, not a production Pharm3D adapter."""

import json
from copy import deepcopy
from itertools import permutations
from pathlib import Path

from pharmacophoremt._ackredit import attributed

CASES_PATH = Path(__file__).resolve().parents[1] / "tests/data/rdkit_bounds_cases.json"


def load_cases(path=CASES_PATH):
    data = json.loads(Path(path).read_text())
    if data.get("schema") != "pharmacophoremt.rdkit-bounds-cases@1":
        raise ValueError("unsupported bounds-comparison fixture")
    return deepcopy(data["cases"])


def _system(record):
    import molsysmt as msm

    from pharmacophoremt import pyunitwizard as puw

    centers = record["centers"]
    if not 3 <= len(centers) <= 4:
        raise ValueError("this case requires three or four explicit single-atom ions")
    ions = ["[Na+]", "[K+]", "[Li+]", "[Rb+]"][: len(centers)]
    system = msm.convert(
        msm.convert("smiles:" + ".".join(ions), to_form="rdkit.Mol"),
        to_form="molsysmt.MolSys",
    )
    system.structures.append(coordinates=puw.quantity([centers], record["unit"]))
    return system


def _atom_axis(inventory, count):
    records = inventory["features"]
    if (
        len(records) != count
        or any(
            row["kind"] != "positive charge" or len(row["atom_indices"]) != 1
            for row in records
        )
        or sorted(row["atom_indices"][0] for row in records) != list(range(count))
    ):
        raise ValueError("comparison requires one positive-charge feature per atom")
    return [row["atom_indices"][0] for row in records]


@attributed()
def compare_case(case, *, max_graph_nodes=64):
    """Retain actual filter decisions and native fits for one fixed case.

    The RDKit arm uses common PHMT-recognized single-atom features and fixed
    conformer distances, not RDKit perception or topology-derived flexibility.
    Every assignment is enumerated. Boundary probes are explicitly separate
    from common interior-filter equivalence. Scientific/provider errors propagate.
    """
    import molsysmt as msm
    import numpy as np
    from rdkit.Chem import rdmolops
    from rdkit.Chem.Pharm3D import EmbedLib

    import pharmacophoremt as phmt
    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt._private.molsysmt import detached

    reference, source = _system(case["reference"]), _system(case["source"])
    options = dict(selection="all", structure_index=0, chemical_state=0)
    target = phmt.modeler.get_features(
        reference, features=["positive charge"], **options
    )
    inventory = phmt.modeler.get_features(
        source, features=["positive charge"], **options
    )
    n = len(target["features"])
    reference_atoms = _atom_axis(target, n)
    source_atoms = _atom_axis(inventory, n)
    before_target, before_inventory = detached(target), detached(inventory)
    before_coordinates = np.array(
        puw.get_value(msm.get(source, coordinates=True), to_unit="angstrom"), copy=True
    )
    tolerance = case["distance_tolerance"]
    query = phmt.modeler.from_feature_inventory(target, radius=tolerance)
    rd_query = phmt.io.to_rdkit(query)
    if [row.GetFamily() for row in rd_query.getFeatures()] != ["PosIonizable"] * n:
        raise ValueError(
            "query family projection differs from the declared charge axis"
        )
    delta = float(puw.get_value(puw.quantity(tolerance), to_unit="angstrom"))
    for i in range(n):
        for j in range(i + 1, n):
            distance = rd_query.getUpperBound(i, j)
            rd_query.setLowerBound(i, j, distance - 2 * delta)
            rd_query.setUpperBound(i, j, distance + 2 * delta)
    rd_molecule = msm.convert(source, to_form="rdkit.Mol")
    if rd_molecule.GetNumAtoms() != n or rd_molecule.GetNumConformers() != 1:
        raise ValueError("source conversion changed the declared atom/frame axis")
    np.testing.assert_allclose(
        rd_molecule.GetConformer().GetPositions(),
        before_coordinates[0],
        rtol=0,
        atol=1e-12,
    )
    bounds = rdmolops.Get3DDistanceMatrix(rd_molecule, confId=0, force=True)
    boundary = None
    if case["boundary"] is not None:
        i, j = case["boundary"]["reference_pair"]
        atom_i, atom_j = source_atoms[i], source_atoms[j]
        value = float(bounds[atom_i, atom_j])
        endpoint = case["boundary"]["endpoint"]
        getter = (
            rd_query.getLowerBound if endpoint == "lower" else rd_query.getUpperBound
        )
        setter = (
            rd_query.setLowerBound if endpoint == "lower" else rd_query.setUpperBound
        )
        original = getter(i, j)
        if abs(value - original) > 1e-12:
            raise ValueError(
                "boundary probe differs from the declared analytical endpoint"
            )
        setter(i, j, value)
        boundary = dict(
            pair=[i, j],
            endpoint=endpoint,
            original_angstrom=original,
            exact_source_angstrom=value,
        )
    accepted = []
    evaluated = 0
    for assignment in permutations(range(n)):
        evaluated += 1
        atom_match = tuple((source_atoms[index],) for index in assignment)
        if EmbedLib.CoarseScreenPharmacophore(atom_match, bounds, rd_query):
            accepted.append([[i, index] for i, index in enumerate(assignment)])
    proposals = phmt.screening.get_rigid_feature_correspondences(
        target,
        inventory,
        correspondence_strategy="association_cliques",
        distance_tolerance=tolerance,
        min_matches=n,
        max_graph_nodes=max_graph_nodes,
        max_cliques=1000,
    )
    placement_report, evaluations = None, []
    if boundary is None:
        placed = phmt.screening.get_rigid_feature_placements(
            source,
            target,
            proposals["correspondences"],
            feature_inventory=inventory,
            features=["positive charge"],
            **options,
            distance_tolerance=tolerance,
            min_matches=n,
            max_fits=32,
            max_matrix_entries=1000000,
        )
        placement_report = placed["report"]
        evaluator = phmt.screening.PoseEvaluator(query, point_tolerance=tolerance)
        for index, placement in enumerate(placed["placements"]):
            native = evaluator.evaluate(
                placement["molecular_system"],
                pose_id=f"{case['key']}:{index}",
                **options,
            )
            evaluations.append(
                dict(
                    native_result=native,
                    score_method="checked_pose_coverage@1",
                    ranking_score=phmt.screening.get_screening_score(
                        native, score_method="checked_pose_coverage"
                    ),
                )
            )
    if detached(target) != before_target or detached(inventory) != before_inventory:
        raise ValueError("comparison mutated a supplied feature inventory")
    if not np.array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="angstrom"),
        before_coordinates,
    ):
        raise ValueError("comparison mutated its source coordinates")
    return detached(
        dict(
            case=case["key"],
            feature_count=n,
            reference_atom_axis=reference_atoms,
            source_atom_axis=source_atoms,
            assignments_evaluated=evaluated,
            rdkit_mappings=accepted,
            native_proposals=proposals,
            mapping_sets_equal=accepted == proposals["correspondences"],
            boundary=boundary,
            native_placement_report=placement_report,
            native_evaluations=evaluations,
            inputs_unchanged=True,
        )
    )


def expectation_passed(case, result):
    """Evaluate declared expectations without changing or filtering actual data."""
    if not result["native_proposals"]["complete"] or not result["inputs_unchanged"]:
        return False
    n = result["feature_count"]
    if result["assignments_evaluated"] != (24 if n == 4 else 6):
        return False
    if case["boundary"] is not None:
        identity = [[i, i] for i in range(n)]
        return (
            identity in result["native_proposals"]["correspondences"]
            and identity not in result["rdkit_mappings"]
        )
    expected = case["expected"]
    return (
        result["mapping_sets_equal"]
        and len(result["rdkit_mappings"]) == expected["coarse_mappings"]
        and result["native_placement_report"]["complete"]
        and result["native_placement_report"]["n_fits"] == expected["coarse_mappings"]
        and len(result["native_evaluations"]) == expected["placements"]
        and all(
            row["native_result"]["status"] == "matched" and row["ranking_score"] == 1
            for row in result["native_evaluations"]
        )
    )
