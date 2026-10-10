"""Fixed distinct CCD consensus controls, owned by PHMT #51.

Run through the existing recorder: prepared_workflow --case consensus --output FILE.
Molecular preparation, recognition, frame transforms and fits belong to MolSysMT.
"""

import hashlib
import json
import subprocess
import sys

from devtools.prepared_ccd_ligands import (
    ROOT,
    motion_frames,
    prepare_case,
    state_payload,
)
from devtools.prepared_workflow import codecs, models_equivalent, native_record
from devtools.validate_prepared_ccd_ligands import scientific_projection

FEATURES = ["hb acceptor", "aromatic ring"]
OPTIONS = dict(
    features=FEATURES,
    correspondence_strategy="ranked_triplet_seeds",
    n_seeds=4,
    refinement_strategy="greedy",
    min_matches=3,
    distance_tolerance=".20 nm",
    direction_tolerance="30 degrees",
    max_fits=100,
)
# Independent occurrence domain from the frozen CTABs, not returned hypotheses.
ATOMS = dict(
    EST=[[3], [18], [0, 1, 2, 4, 5, 10]],
    DES=[[7], [15], [3, 4, 5, 6, 8, 9], [11, 12, 13, 14, 16, 17]],
)


def run_case(directory, *, fresh_reader=False):
    import molsysmt as msm

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt._private.smonitor.exceptions import (
        ArgumentError,
        CliqueLimitError,
    )
    from pharmacophoremt.modeler import LigandBasedModeler, from_rigid_ligands

    prepared = {key: prepare_case(key, features=FEATURES) for key in ATOMS}
    systems = {key: value["molecular_system"] for key, value in prepared.items()}
    systems["DES"] = motion_frames(systems["DES"])
    ligands = [
        dict(
            ligand_id=key,
            molecular_system=systems[key],
            structure_index=index,
            chemical_state="reference",
            selection="all",
        )
        for index, key in enumerate(ATOMS)
    ]

    def snapshot():
        return {
            key: dict(
                coordinates_nm=puw.get_value(
                    msm.get(system, coordinates=True), to_unit="nm"
                ).tolist(),
                chemical_state=state_payload(system),
            )
            for key, system in systems.items()
        }

    before = snapshot()
    native = from_rigid_ligands(ligands, min_sites=3, min_support=2, **OPTIONS)
    if len(native["models"]) != 1:
        raise RuntimeError(
            "The declared EST/DES control requires one native hypothesis"
        )
    model = native["models"][0]
    original = native_record(model, directory, "consensus-original")
    facade = LigandBasedModeler(
        ligands, consensus_method="rigid", n_points=3, min_actives=2, **OPTIONS
    )
    built = facade.build()
    facade_success = dict(
        models=[
            native_record(m, directory, f"facade-{i}") for i, m in enumerate(built)
        ],
        report=facade.report,
        complete=facade.result["complete"],
        return_is_native_list=built is facade.result["models"],
    )
    facade.n_points = 4  # Independent bound: EST has only three usable occurrences.
    empty = facade.build()
    empty_result = dict(
        models=empty, report=facade.report, complete=facade.result["complete"]
    )
    facade.native_options["max_fits"] = 1
    try:
        facade.build()
    except CliqueLimitError as error:
        failure = dict(
            status="failed",
            code=error.code,
            message=str(error),
            result=facade.result,
            report=facade.report,
        )
    else:
        raise RuntimeError("Fit exhaustion must raise, never return an empty result")
    try:
        LigandBasedModeler(
            [systems["DES"], systems["DES"]], consensus_method="rigid", **OPTIONS
        )
    except ArgumentError as error:
        duplicate = dict(code=error.code, message=str(error))
    else:
        raise RuntimeError(
            "Repeated raw frames cannot establish distinct ligand support"
        )
    results, artifacts = {}, {}
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        for suffix, write, read in codecs():
            path = directory / ("consensus." + suffix)
            write(model, path)
            raw = path.read_bytes()
            artifacts[path.name] = dict(
                sha256=hashlib.sha256(raw).hexdigest(),
                byte_count=len(raw),
                utf8=raw.decode(),
            )
            with puw.context(standard_units=["angstrom", "ps", "radians"]):
                results[suffix] = native_record(read(path), directory, "restored")
    reader = None
    if fresh_reader:
        child = subprocess.run(
            [
                sys.executable,
                "-m",
                "devtools.prepared_workflow",
                "--case",
                "consensus",
                "--read",
                str(directory),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        reader = dict(**json.loads(child.stdout), stderr=child.stderr)
    after = snapshot()
    return dict(
        preparation={key: value["report"] for key, value in prepared.items()},
        model=original,
        report=native["report"],
        complete=native["complete"],
        facade_success=facade_success,
        empty=empty_result,
        budget_failure=failure,
        repeated_raw_rejection=duplicate,
        inputs_before=before,
        inputs_after=after,
        source_coordinates_and_states_unchanged=before == after,
        oracle=dict(
            original_atom_domains=ATOMS,
            distinct_ligand_ids=["EST", "DES"],
            expected_joint_support=2,
            maximum_joint_sites=3,
            rationale="Disjoint occurrences and support from both ligands require one EST occurrence per site; EST has exactly three.",
            coordinate_tolerance_nm=1e-12,
            frame_policy="EST frame 0; DES frame 1 is Rz(90 degrees)+[2,1,3] nm of frame 0, not an additional ligand or conformer",
        ),
        results=results,
        artifacts=artifacts,
        fresh_reader=reader,
    )


def expectations_passed(result):
    """Bounded case checks; focused tests additionally verify independent geometry."""
    if not result["source_coordinates_and_states_unchanged"] or not result["complete"]:
        return False
    model = result["model"]
    h = model["metadata"]["hypothesis"]
    sites = model["metadata"]["consensus"]["sites"]
    if (
        h["joint_ligand_ids"] != ["DES", "EST"]
        or h["joint_support_count"] != 2
        or len(sites) != 3
    ):
        return False
    for site in sites:
        if {m["ligand_id"] for m in site["members"]} != set(ATOMS):
            return False
        for member in site["members"]:
            if (
                member["atom_indices"]
                != ATOMS[member["ligand_id"]][member["feature_index"]]
            ):
                return False
    success = result["facade_success"]
    if (
        not success["complete"]
        or not success["return_is_native_list"]
        or len(success["models"]) != 1
    ):
        return False

    def project(value):
        return scientific_projection(
            value, attribution_keys=("attribution", "source_attribution")
        )

    if not models_equivalent(project(success["models"][0]), project(model)):
        return False
    if not result["empty"]["complete"] or result["empty"]["models"] != []:
        return False
    failure = result["budget_failure"]
    if (
        failure["code"] != "PHMT-E107"
        or failure["result"] is not None
        or failure["report"] is not None
    ):
        return False
    if not all(models_equivalent(value, model) for value in result["results"].values()):
        return False
    reader = result["fresh_reader"]
    return reader is None or (
        not reader["attribution"]["uses"]
        and all(models_equivalent(value, model) for value in reader["models"].values())
    )
