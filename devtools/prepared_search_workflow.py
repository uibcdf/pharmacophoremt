"""Fixed CCD rigid-search continuation, owned by PHMT #50.

Reuse the evidence driver: python -m devtools.prepared_workflow --case search
--output FILE. All molecular access, placement and fitting belongs to MolSysMT.
This is case-specific orchestration and independent acceptance, not a new method.
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
from devtools.prepared_workflow import (
    FEATURES,
    build_hypotheses,
    codecs,
    models_equivalent,
    native_record,
)

RING_ATOMS = [0, 1, 2, 4, 5, 10]
ESSENTIAL_SITES = [0, 1, 5]  # Aromatic center, source atom 0, source atom 8.


def build_query(prepared):
    from pharmacophoremt.modeler import edit_pharmacophore

    _, narrow, _ = build_hypotheses(prepared)
    rigid = edit_pharmacophore(
        narrow,
        site_indices=[1, 5],
        essential=True,
        reason="declared rigid-search anchors: source atoms 0 and 8 plus aromatic center",
    )
    return narrow, rigid


def evaluate_query(query, source, frames, unprepared):
    import molsysmt as msm

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.screening import (
        ConformerScreening,
        PoseEvaluator,
        RigidPoseSearch,
        VirtualScreening,
        align_to_pharmacophore,
    )

    placed = PoseEvaluator(query).evaluate(frames, structure_index=1)
    search = RigidPoseSearch(query, max_trials=10000, direction_tolerance="1 degree")
    recovered = search.evaluate(frames, structure_index=1)
    negative = search.evaluate(source, selection=RING_ATOMS)
    exhausted = RigidPoseSearch(query, max_trials=1).run(
        [frames], structure_index=1, on_error="record"
    )[0]
    ensembles = {}
    for budget in (10000, 1):
        runner = ConformerScreening(
            query, max_trials=budget, direction_tolerance="1 degree"
        )
        for order in ([1, 0], [0, 1]):
            ensembles[f"{budget}:{order}"] = runner.evaluate(
                frames, structure_indices=order, on_error="record"
            )
    facade = VirtualScreening(
        query,
        screening_method="rigid",
        max_trials=10000,
        direction_tolerance="1 degree",
    )
    inputs = [frames, unprepared, frames]
    hits = facade.run(inputs, structure_index=1, on_error="record")
    if recovered["alignment"] is None:
        raise RuntimeError("The declared moved frame must require a fitted placement")
    aligned = align_to_pharmacophore(
        frames, query, recovered["alignment"]["correspondence"], structure_index=1
    )
    return dict(
        placed=placed,
        recovered=recovered,
        selected_negative=negative,
        budget_failure=exhausted,
        ensembles=ensembles,
        facade=dict(
            evaluations=facade.evaluations,
            hit_input_indices=[row["input_index"] for row in hits],
            scalar_hits=facade.to_dataframe().to_dict(orient="records"),
            original_input_references=all(
                row["mol"] is inputs[row["input_index"]] for row in hits
            ),
        ),
        replayed_coordinates_nm=puw.get_value(
            msm.get(aligned["molecular_system"], coordinates=True), to_unit="nm"
        ).tolist(),
        replayed_state=state_payload(aligned["molecular_system"]),
        replayed_pose=PoseEvaluator(query).evaluate(
            aligned["molecular_system"], structure_index=1
        ),
    )


def run_case(directory, *, fresh_reader=False):
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt._private.smonitor.exceptions import ArgumentError
    from pharmacophoremt.screening import RigidPoseSearch

    prepared = prepare_case("EST", features=FEATURES)
    source = prepared["molecular_system"]
    frames = motion_frames(source)
    unprepared = msm.convert(
        msm.convert("smiles:CCC", to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
    )
    narrow, query = build_query(prepared)
    try:
        RigidPoseSearch(narrow)
    except ArgumentError as error:
        rejected = dict(code=error.code, message=str(error))
    else:
        raise RuntimeError(
            "The old single-essential-site query cannot seed rigid search"
        )

    def snapshot(system):
        return dict(
            coordinates_nm=puw.get_value(
                msm.get(system, coordinates=True), to_unit="nm"
            ).tolist(),
            chemical_state=state_payload(system),
        )

    before = dict(source=snapshot(source), frames=snapshot(frames))
    centers = np.array(
        [
            puw.get_value(query.interaction_sites[i].center, to_unit="nm")
            for i in ESSENTIAL_SITES
        ]
    )
    source_positions = np.array(before["source"]["coordinates_nm"])[0]
    selected_positions = source_positions[RING_ATOMS]
    oracle = dict(
        essential_site_indices=ESSENTIAL_SITES,
        anchor_atom_indices=[
            query.interaction_sites[i].metadata["atom_indices"] for i in ESSENTIAL_SITES
        ],
        anchor_triangle_area_nm2=float(
            np.linalg.norm(np.cross(centers[1] - centers[0], centers[2] - centers[0]))
            / 2
        ),
        query_ring_to_atom8_distance_nm=float(np.linalg.norm(centers[2] - centers[0])),
        selected_max_atom_distance_nm=float(
            np.linalg.norm(
                selected_positions[:, None] - selected_positions[None, :], axis=-1
            ).max()
        ),
        matching_pair_slack_nm=0.04,
        expected_selected_coverage=8 / 12,
        coordinate_tolerance_nm=1e-12,
        placements="Same conformation: frame 0 original, frame 1 Rz(90 degrees) plus [2,1,3] nm",
    )
    results, artifacts = {}, {}
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        original = native_record(query, directory, "rigid-original")
        for suffix, write, read in codecs():
            path = directory / ("rigid." + suffix)
            write(query, path)
            raw = path.read_bytes()
            artifacts[path.name] = dict(
                sha256=hashlib.sha256(raw).hexdigest(),
                byte_count=len(raw),
                utf8=raw.decode(),
            )
            with puw.context(standard_units=["angstrom", "ps", "radians"]):
                restored = read(path)
                results[suffix] = dict(
                    native=native_record(restored, directory, "restored"),
                    controls=evaluate_query(restored, source, frames, unprepared),
                )
    reader = None
    if fresh_reader:
        child = subprocess.run(
            [
                sys.executable,
                "-m",
                "devtools.prepared_workflow",
                "--case",
                "search",
                "--read",
                str(directory),
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        reader = dict(**json.loads(child.stdout), stderr=child.stderr)
    after = dict(source=snapshot(source), frames=snapshot(frames))
    return dict(
        preparation=prepared["report"],
        model=original,
        prior_query=native_record(narrow, directory, "prior-query"),
        incompatible_query_rejection=rejected,
        oracle=oracle,
        inputs_before=before,
        inputs_after=after,
        source_coordinates_and_states_unchanged=before == after,
        artifacts=artifacts,
        results=results,
        fresh_reader=reader,
    )


def expectations_passed(result):
    import numpy as np

    if not result["source_coordinates_and_states_unchanged"]:
        return False
    oracle = result["oracle"]
    if not (
        oracle["anchor_triangle_area_nm2"] > 0.01
        and oracle["query_ring_to_atom8_distance_nm"]
        > oracle["selected_max_atom_distance_nm"] + 0.04
    ):
        return False
    original = np.array(result["inputs_before"]["source"]["coordinates_nm"])
    for entry in result["results"].values():
        if not models_equivalent(entry["native"], result["model"]):
            return False
        c = entry["controls"]
        if c["placed"]["status"] != "not_matched" or c["placed"]["fit_value"] != 0:
            return False
        if c["recovered"]["status"] != "matched" or c["recovered"]["fit_value"] != 1:
            return False
        if (
            c["selected_negative"]["status"] != "not_matched"
            or c["selected_negative"]["fit_value"] != 8 / 12
        ):
            return False
        if not c["selected_negative"]["search"]["enumeration_complete"]:
            return False
        if (
            c["budget_failure"]["status"] != "failed"
            or c["budget_failure"]["fit_value"] is not None
        ):
            return False
        for name, ensemble in c["ensembles"].items():
            budget, order = name.split(":", 1)
            expected_frame = json.loads(order)[0] if budget == "10000" else 0
            if not (
                ensemble["status"] == "matched"
                and ensemble["fit_value"] == 1
                and ensemble["best_conformer_index"] == expected_frame
                and ensemble["ensemble"]["score_resolved"]
                and ensemble["ensemble"]["complete"] == (budget == "10000")
                and ensemble["ensemble"]["n_failed"] == (0 if budget == "10000" else 1)
            ):
                return False
        if (
            c["facade"]["hit_input_indices"] != [0, 2]
            or not c["facade"]["original_input_references"]
        ):
            return False
        replay = np.array(c["replayed_coordinates_nm"])
        if not np.allclose(replay, np.repeat(original, 2, axis=0), rtol=0, atol=1e-12):
            return False
        if c["replayed_state"] != result["inputs_before"]["frames"]["chemical_state"]:
            return False
    reader = result["fresh_reader"]
    return reader is None or (
        not reader["attribution"]["uses"]
        and all(
            models_equivalent(value, result["model"])
            for value in reader["models"].values()
        )
    )
