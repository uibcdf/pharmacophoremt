"""Opt-in real-chemistry controls; count evidence, not a timing benchmark.

Run from the checkout: python -m devtools.validate_prepared_ccd_ligands --output FILE
MolSysMT owns all molecular access and preparation. CCD ideal coordinates are
reference-data geometry, not experimental conformers or biological truth labels.
"""

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from devtools.benchmark_rigid_consensus import THREAD_VARS, _digest, _source_record
from devtools.prepared_ccd_ligands import (
    DIRECTORY,
    MANIFEST_PATH,
    ROOT,
    credit_source,
    load_cases,
    motion_frames,
    prepare_case,
)


def scientific_projection(value):
    """Exclude only citation payloads from a portable scientific comparison.

    Independently called public steps can attach attribution to input inventories;
    keep those payloads in full evidence, but exclude them from the science hash.
    """
    if isinstance(value, dict):
        return {
            key: scientific_projection(item)
            for key, item in value.items()
            if key != "attribution"
        }
    if isinstance(value, list):
        return [scientific_projection(item) for item in value]
    return value


def self_recovery(prepared, policy):
    """Compose independent public proposals, refinement and explicit-pair check."""
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.modeler import get_features
    from pharmacophoremt.screening import (
        evaluate_feature_correspondence,
        get_rigid_feature_correspondences,
        refine_rigid_feature_correspondences,
    )

    frames = motion_frames(prepared["molecular_system"])
    before_coordinates = puw.get_value(
        msm.get(frames, coordinates=True), to_unit="nm"
    ).copy()
    features = json.loads(MANIFEST_PATH.read_text())["search_features"]
    target = get_features(frames, structure_index=0, features=features)
    source = get_features(frames, structure_index=1, features=features)
    proposals = get_rigid_feature_correspondences(
        target,
        source,
        correspondence_strategy="ranked_triplet_seeds",
        n_seeds=1,
        distance_tolerance=".02 nm",
    )
    result = refine_rigid_feature_correspondences(
        frames,
        target,
        proposals["correspondences"],
        features=features,
        feature_inventory=source,
        structure_index=1,
        orientation_policy=policy,
        min_matches=len(target["features"]),
        distance_tolerance=".02 nm",
        direction_tolerance="20 degrees",
        max_fits=100,
    )
    evaluations = [
        evaluate_feature_correspondence(
            target,
            placement["inventory"],
            placement["matches"]["matches"],
            distance_tolerance=".02 nm",
            direction_tolerance="20 degrees",
        )
        for placement in result["placements"]
    ]
    return dict(
        proposals={
            key: value for key, value in proposals.items() if key != "attribution"
        },
        report={
            key: value
            for key, value in result["report"].items()
            if key != "attribution"
        },
        pair_evaluations=[
            {key: value for key, value in evaluation.items() if key != "attribution"}
            for evaluation in evaluations
        ],
        outcome=dict(
            n_placements=len(result["placements"]),
            n_fits=result["report"]["n_fits"],
            max_matches=max(
                (len(p["matches"]["matches"]) for p in result["placements"]), default=0
            ),
        ),
        source_coordinates_unchanged=bool(
            np.array_equal(
                before_coordinates,
                puw.get_value(msm.get(frames, coordinates=True), to_unit="nm"),
            )
        ),
        returned_pairs_valid=all(
            evaluation["all_pairs_valid"] for evaluation in evaluations
        ),
    )


def cross_consensus(prepared, workload, policy):
    from pharmacophoremt.modeler import from_rigid_ligands
    from pharmacophoremt.validation import summarize_rigid_consensus

    result = from_rigid_ligands(
        [
            dict(
                ligand_id=item["report"]["source"]["case_id"],
                molecular_system=item["molecular_system"],
            )
            for item in prepared
        ],
        orientation_policy=policy,
        **workload["parameters"],
    )
    report = dict(result["report"])
    report.pop("attribution", None)
    summary = summarize_rigid_consensus(report)
    return dict(
        report=report,
        summary=summary,
        outcome={
            key: summary[key] for key in ("n_models", "n_fits", "max_joint_sites")
        },
    )


def prepared_screening(prepared):
    """Screen two placements of one prepared conformation with public tools."""
    from pharmacophoremt.modeler import from_ligand
    from pharmacophoremt.screening import ConformerScreening

    query = from_ligand(
        prepared["molecular_system"],
        features=["hb donor", "hb acceptor", "aromatic ring"],
        radius=".02 nm",
    )
    result = ConformerScreening(
        query,
        point_tolerance=".02 nm",
        direction_tolerance="20 degrees",
        min_fit_value=1.0,
    ).evaluate(
        motion_frames(prepared["molecular_system"]),
        structure_indices=[1, 0],
        chemical_state="reference",
    )
    return dict(
        result=result,
        outcome=dict(
            status=result["status"],
            fit_value=result["fit_value"],
            best_conformer_index=result["best_conformer_index"],
            n_evaluated=result["ensemble"]["n_evaluated"],
            complete=result["ensemble"]["complete"],
        ),
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    for key in THREAD_VARS:
        os.environ[key] = "1"
    import ackredit
    import molsysmt as msm
    import pyunitwizard as puw

    import pharmacophoremt as phmt

    msm.configure.set_parallelization(parallel=False, num_threads=1)
    tracked = {
        "pharmacophoremt": phmt,
        "molsysmt": msm,
        "pyunitwizard": puw,
        "ackredit": ackredit,
    }
    before = {name: _source_record(module) for name, module in tracked.items()}
    inputs = [
        MANIFEST_PATH,
        Path(__file__),
        ROOT / "devtools/prepared_ccd_ligands.py",
        ROOT / "devtools/benchmark_rigid_consensus.py",
    ]
    inputs.extend(DIRECTORY / case["file"] for case in load_cases())

    def identities():
        return {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in inputs
        }

    input_before = identities()
    manifest = json.loads(MANIFEST_PATH.read_text())
    records, preparations = [], None
    for enabled in (False, True):
        with ackredit.session("prepared CCD validation"), phmt.attribution(enabled):
            prepared = [prepare_case(case["case_id"]) for case in load_cases()]
            observations = [item["report"] for item in prepared]
            if preparations is None:
                preparations = observations
            if observations != preparations:
                raise RuntimeError("preparation observations changed between calls")
            if enabled:
                for case in load_cases():
                    credit_source(case["case_id"])
            results = []
            for item in prepared:
                case = item["report"]["source"]
                for policy in ("final", "each_step"):
                    raw = self_recovery(item, policy)
                    expected = dict(
                        n_placements=1,
                        max_matches=case["expected"]["search_feature_count"],
                        n_fits=case["expected"]["search_feature_count"] - 2,
                    )
                    results.append(
                        dict(
                            kind="self_recovery",
                            case_id=case["case_id"],
                            orientation_policy=policy,
                            expected=expected,
                            expectation_passed=raw["outcome"] == expected
                            and raw["returned_pairs_valid"]
                            and raw["source_coordinates_unchanged"],
                            **raw,
                        )
                    )
                raw = prepared_screening(item)
                expected = dict(
                    status="matched",
                    fit_value=1.0,
                    best_conformer_index=1,
                    n_evaluated=2,
                    complete=True,
                )
                results.append(
                    dict(
                        kind="prepared_screening",
                        case_id=case["case_id"],
                        orientation_policy=None,
                        expected=expected,
                        expectation_passed=raw["outcome"] == expected,
                        **raw,
                    )
                )
            for workload in manifest["cross_workloads"]:
                for policy in ("final", "each_step"):
                    raw = cross_consensus(prepared, workload, policy)
                    expected = workload["expected"][policy]
                    results.append(
                        dict(
                            kind="cross_consensus",
                            case_id=workload["case_id"],
                            orientation_policy=policy,
                            parameters=workload["parameters"],
                            expected=expected,
                            expectation_passed=raw["outcome"] == expected,
                            **raw,
                        )
                    )
            if not enabled:
                fingerprints = [
                    _digest(scientific_projection(result)) for result in results
                ]
            else:
                attribution = ackredit.get_attribution().to_dict()
                records = [
                    dict(
                        result,
                        scientific_output_sha256=_digest(scientific_projection(result)),
                        scientific_outputs_stable=_digest(scientific_projection(result))
                        == expected_hash,
                    )
                    for result, expected_hash in zip(results, fingerprints)
                ]
    after = {name: _source_record(module) for name, module in tracked.items()}

    def git(*arguments):
        return subprocess.run(
            ["git", *arguments], cwd=ROOT, capture_output=True, text=True, check=False
        ).stdout.strip()

    extensions = []
    for name, module in sorted(sys.modules.items()):
        path = getattr(module, "__file__", None)
        if (
            name.startswith("molsysmt")
            and path
            and Path(path).suffix in {".so", ".pyd", ".dylib"}
        ):
            extensions.append(
                dict(
                    module=name,
                    path=path,
                    sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                )
            )
    report = dict(
        schema="pharmacophoremt.prepared_ccd_validation@1",
        recorded_at_utc=datetime.now(timezone.utc).isoformat(),
        scope="CCD ideal geometries of real chemical components; not biological validation, generated conformers or a runtime/memory benchmark",
        manifest=manifest,
        preparations=preparations,
        input_sha256=input_before,
        input_hashes_unchanged=input_before == identities(),
        source_hashes_unchanged=before == after,
        source_head=git("rev-parse", "HEAD"),
        source_working_state=git("status", "--porcelain"),
        environment=dict(
            python=sys.version,
            executable=sys.executable,
            platform=platform.platform(),
            packages=after,
            versions={
                name: importlib.metadata.version(name)
                for name in (
                    "numpy",
                    "scipy",
                    "rdkit",
                    "argdigest",
                    "depdigest",
                    "smonitor",
                )
            },
            molecular_extensions=extensions,
            thread_environment={key: os.environ.get(key) for key in THREAD_VARS},
        ),
        scientific_hash_scope="all portable scientific fields except attribution nodes; full credited payloads retained",
        records=records,
        attribution=attribution,
    )
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    for record in records:
        print(
            f"{record['kind']} / {record['case_id']} / {record['orientation_policy']}: {'PASS' if record['expectation_passed'] and record['scientific_outputs_stable'] else 'FAIL'}",
            file=sys.stderr,
        )
    return (
        0
        if report["input_hashes_unchanged"]
        and report["source_hashes_unchanged"]
        and all(
            r["expectation_passed"] and r["scientific_outputs_stable"] for r in records
        )
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
