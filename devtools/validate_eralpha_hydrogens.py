"""Donor-inclusive observed EST controls after provider-owned H placement.

Run: python -m devtools.validate_eralpha_hydrogens --output FILE
No receptor refinement, energy qualification or timing measurement is performed.
"""

import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
import tempfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from devtools.benchmark_rigid_consensus import _source_record
from devtools.prepare_eralpha_hydrogens import SELECTED_FEATURES, add_hydrogens
from devtools.prepare_eralpha_ligand import ROOT, credit_inputs, prepare_case
from devtools.validate_eralpha_template import placed_controls, portable, valid_controls
from devtools.validate_prepared_ccd_ligands import scientific_projection, self_recovery


def donor_controls(case):
    """Change one query direction and withhold generated H geometry explicitly."""
    from pharmacophoremt.modeler import from_ligand
    from pharmacophoremt.screening import PoseEvaluator

    query = from_ligand(
        case["molecular_system"], features=SELECTED_FEATURES, radius=".02 nm"
    )
    heavy_only = PoseEvaluator(
        query, direction_tolerance="10 degrees", min_fit_value=1
    ).evaluate(case["heavy_case"]["molecular_system"])
    reversed_query = deepcopy(query)
    donor = next(
        site
        for site in reversed_query.interaction_sites
        if site.features == ["hb donor"]
    )
    donor.shape.direction = -donor.shape.direction
    reversed_direction = PoseEvaluator(
        reversed_query, direction_tolerance="10 degrees", min_fit_value=1
    ).evaluate(case["molecular_system"])
    return dict(heavy_only=heavy_only, reversed_donor_direction=reversed_direction)


def workflow(directory):
    """Compose the already independent preparation, placement and rigid steps."""
    case = add_hydrogens(prepare_case())
    placed = placed_controls(case, directory, features=SELECTED_FEATURES)
    donors = donor_controls(case)
    recovery = {
        policy: self_recovery(case, policy) for policy in ("final", "each_step")
    }
    return dict(
        preparation=case["report"],
        placed=placed,
        donor_controls=donors,
        recovery=recovery,
    )


def valid_workflow(run):
    report = run["preparation"]
    return (
        report["prepared_counts"] == dict(n_atoms=44, n_bonds=47, n_structures=1)
        and report["feature_counts"]
        == {"hydrophobicity": 9, "hb donor": 2, "hb acceptor": 2, "aromatic ring": 1}
        and report["hydrogen_addition"]["n_added_hydrogens"] == 24
        and report["heavy_coordinates_preserved"]
        and report["input_unchanged"]
        and valid_controls(run["placed"], n_sites=5)
        and all(
            value["status"] == "not_matched" for value in run["donor_controls"].values()
        )
        and all(
            value["outcome"]["n_placements"] == 1
            and value["outcome"]["max_matches"] == 5
            and value["returned_pairs_valid"]
            and value["source_coordinates_unchanged"]
            for value in run["recovery"].values()
        )
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    import ackredit
    import molsysmt as msm
    import pyunitwizard

    import pharmacophoremt as phmt

    producers = {
        "pharmacophoremt": phmt,
        "molsysmt": msm,
        "pyunitwizard": pyunitwizard,
        "ackredit": ackredit,
    }
    before = {name: _source_record(module) for name, module in producers.items()}
    paths = [
        ROOT / path
        for path in (
            "tests/data/eralpha_rcsb/1qku.cif",
            "tests/data/eralpha_rcsb/EST.cif",
            "tests/data/eralpha_rcsb/manifest.json",
            "tests/data/eralpha_template/est_template.h5msm",
            "tests/data/eralpha_template/manifest.json",
            "tests/data/eralpha_template/acquisition.json",
            "tests/data/prepared_ccd/manifest.json",
            "devtools/prepare_eralpha_ligand.py",
            "devtools/prepare_eralpha_hydrogens.py",
            "devtools/validate_eralpha_template.py",
            "devtools/validate_eralpha_hydrogens.py",
            "devtools/prepared_ccd_ligands.py",
            "devtools/validate_prepared_ccd_ligands.py",
            "devtools/benchmark_rigid_consensus.py",
        )
    ]

    def input_hashes():
        return {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths
        }

    inputs = input_hashes()
    runs = []
    for enabled in (False, True):
        with (
            ackredit.session("observed EST donor-inclusive controls"),
            phmt.attribution(enabled),
        ):
            with tempfile.TemporaryDirectory(prefix="phmt-est-h-") as directory:
                with ackredit.capture(
                    "observed ligand preparation and evaluation",
                    context=dict(
                        consumer="pharmacophoremt",
                        hydrogen_geometry="generated_local_geometry",
                        chemical_state="reference",
                        environment_refinement=False,
                    ),
                ) as capture:
                    run = portable(workflow(directory))
                    if enabled:
                        credit_inputs()
            run["attribution"] = capture.attribution.to_dict()
            run["tracking"] = enabled
            run["valid"] = valid_workflow(run)
            science = scientific_projection(
                {
                    key: value
                    for key, value in run.items()
                    if key not in {"tracking", "valid"}
                }
            )
            run["scientific_sha256"] = hashlib.sha256(
                json.dumps(science, sort_keys=True).encode()
            ).hexdigest()
            runs.append(run)
    after = {name: _source_record(module) for name, module in producers.items()}
    unchanged = before == after and inputs == input_hashes()
    valid = (
        unchanged
        and all(run["valid"] for run in runs)
        and runs[0]["scientific_sha256"] == runs[1]["scientific_sha256"]
    )
    report = dict(
        schema="pharmacophoremt.eralpha_hydrogen_validation@1",
        recorded_utc=datetime.now(timezone.utc).isoformat(),
        python=platform.python_version(),
        executable=sys.executable,
        platform=platform.platform(),
        producers=before,
        inputs=inputs,
        producers_and_inputs_unchanged=unchanged,
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
        molecular_extensions=[
            dict(
                module=name,
                path=module.__file__,
                sha256=hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest(),
            )
            for name, module in sorted(sys.modules.items())
            if name.startswith("molsysmt")
            and getattr(module, "__file__", None)
            and Path(module.__file__).suffix in {".so", ".pyd", ".dylib"}
        ],
        runs=runs,
        valid=valid,
        scope="generated local H on an observed heavy pose; no receptor/energy/biological acceptance or performance measurements",
    )
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print("PASS" if valid else "FAIL", "donor-inclusive observed EST controls")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
