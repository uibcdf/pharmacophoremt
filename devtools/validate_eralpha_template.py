"""Offline observed-ligand controls; no timing or biological benchmark.

Run: python -m devtools.validate_eralpha_template --output FILE
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
from devtools.prepare_eralpha_ligand import (
    ROOT,
    SELECTED_FEATURES,
    credit_inputs,
    prepare_case,
)
from devtools.validate_prepared_ccd_ligands import scientific_projection


def placed_controls(case, directory, *, features=None):
    """Compose public placed controls for an explicit feature-family hypothesis.

    The default preserves the heavy-only acceptor/aromatic control. A caller may
    explicitly include directional donors after separate hydrogen preparation.
    """
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.io import load_json, to_json
    from pharmacophoremt.modeler import from_ligand
    from pharmacophoremt.screening import PoseEvaluator

    prepared = case["molecular_system"]
    features = SELECTED_FEATURES if features is None else list(features)
    query = from_ligand(prepared, features=features, radius=".02 nm")
    query.metadata["input_preparation"] = scientific_projection(
        portable(case["report"])
    )
    evaluator = PoseEvaluator(query, direction_tolerance="10 degrees", min_fit_value=1)
    positive = evaluator.evaluate(prepared)
    displaced = msm.structure.translate(
        prepared, translation=puw.quantity([[[2.0, 0.0, 0.0]]], "nm"), in_place=False
    )
    negative = evaluator.evaluate(displaced)
    reversed_query = deepcopy(query)
    tilted_query = deepcopy(query)
    ring_index = next(
        i
        for i, site in enumerate(query.interaction_sites)
        if site.features == ["aromatic ring"]
    )
    normal = puw.get_value(
        query.interaction_sites[ring_index].shape.normal, to_unit="dimensionless"
    )
    reversed_query.interaction_sites[ring_index].shape.normal = puw.quantity(
        -normal, "dimensionless"
    )
    axis = np.eye(3)[int(np.argmin(np.abs(normal)))]
    orthogonal = np.cross(normal, axis)
    orthogonal /= np.linalg.norm(orthogonal)
    tilted_query.interaction_sites[ring_index].shape.normal = puw.quantity(
        orthogonal, "dimensionless"
    )
    normal_sign = PoseEvaluator(
        reversed_query, direction_tolerance="10 degrees", min_fit_value=1
    ).evaluate(prepared)
    angular_negative = PoseEvaluator(
        tilted_query, direction_tolerance="10 degrees", min_fit_value=1
    ).evaluate(prepared)
    directory = Path(directory)
    molecular_path = directory / "prepared_est.h5msm"
    query_path = directory / "observed_est_query.json"
    msm.convert(prepared, to_form="file:h5msm", output_filename=str(molecular_path))
    to_json(query, str(query_path))
    loaded = msm.convert(molecular_path, to_form="molsysmt.MolSys")
    reloaded_query = load_json(str(query_path))
    roundtrip = PoseEvaluator(
        reloaded_query, direction_tolerance="10 degrees", min_fit_value=1
    ).evaluate(loaded)
    from devtools.prepared_ccd_ligands import state_payload

    original_state, reloaded_state = state_payload(prepared), state_payload(loaded)
    expected_reload = deepcopy(original_state)
    # The public H5MSM codec canonicalizes these two fixture string columns.
    # Permit only this recorded representation change; compare every other key,
    # value, null mask and index. Retain both actual payloads in the evidence.
    for column in ("component_name", "component_type"):
        expected_reload["states"][0]["components"]["columns"][column]["dtype"] = (
            "string"
        )

    return dict(
        hypothesis=dict(
            features=features,
            radius=".02 nm",
            direction_tolerance="10 degrees",
            min_fit_value=1,
            n_essential_sites=query.n_interaction_sites,
        ),
        positive=positive,
        displaced_negative=negative,
        reversed_normal=normal_sign,
        orthogonal_normal_negative=angular_negative,
        roundtrip=roundtrip,
        source_state=original_state,
        reloaded_state=reloaded_state,
        persistence=dict(
            chemical_values_preserved=reloaded_state == expected_reload,
            coordinates_preserved=bool(
                np.array_equal(
                    puw.get_value(msm.get(loaded, coordinates=True), to_unit="nm"),
                    puw.get_value(msm.get(prepared, coordinates=True), to_unit="nm"),
                )
            ),
            query_metadata_preserved=reloaded_query.metadata == query.metadata,
        ),
    )


def portable(value):
    """Detach provider arrays; quantity-bearing scientific records stay explicit."""
    return json.loads(
        json.dumps(value, default=lambda array: array.tolist(), allow_nan=False)
    )


def valid_controls(result, *, n_sites=3):
    return (
        result["hypothesis"]["n_essential_sites"] == n_sites
        and all(
            result[key]["status"] == "matched" and result[key]["fit_value"] == 1
            for key in ("positive", "reversed_normal", "roundtrip")
        )
        and all(
            result[key]["status"] == "not_matched"
            for key in ("displaced_negative", "orthogonal_normal_negative")
        )
        and all(result["persistence"].values())
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
    before = {key: _source_record(module) for key, module in producers.items()}
    inputs = [
        ROOT / path
        for path in (
            "tests/data/eralpha_rcsb/1qku.cif",
            "tests/data/eralpha_rcsb/EST.cif",
            "tests/data/eralpha_rcsb/manifest.json",
            "tests/data/eralpha_template/est_template.h5msm",
            "tests/data/eralpha_template/manifest.json",
            "tests/data/eralpha_template/acquisition.json",
            "devtools/prepare_eralpha_ligand.py",
            "devtools/validate_eralpha_template.py",
            "devtools/prepared_ccd_ligands.py",
            "devtools/validate_prepared_ccd_ligands.py",
            "devtools/benchmark_rigid_consensus.py",
        )
    ]
    hashes = {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in inputs
    }
    runs = []
    for enabled in (False, True):
        with (
            ackredit.session("observed EST template controls"),
            phmt.attribution(enabled),
        ):
            case = prepare_case()
            if enabled:
                credit_inputs()
            with tempfile.TemporaryDirectory(prefix="phmt-est-") as directory:
                controls = placed_controls(case, directory)
            run = portable(
                dict(
                    tracking=enabled,
                    preparation=case["report"],
                    controls=controls,
                    attribution=ackredit.get_attribution().to_dict(),
                )
            )
            run["valid"] = (
                valid_controls(run["controls"])
                and case["report"]["pose_preserved"]
                and case["report"]["source_unchanged"]
            )
            science = scientific_projection(
                dict(preparation=run["preparation"], controls=run["controls"])
            )
            run["scientific_sha256"] = hashlib.sha256(
                json.dumps(science, sort_keys=True).encode()
            ).hexdigest()
            runs.append(run)
    after = {key: _source_record(module) for key, module in producers.items()}
    unchanged = hashes == {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in inputs
    }
    valid = (
        all(run["valid"] for run in runs)
        and runs[0]["scientific_sha256"] == runs[1]["scientific_sha256"]
        and before == after
        and unchanged
    )
    report = dict(
        schema="pharmacophoremt.eralpha_template_validation@1",
        executed_utc=datetime.now(timezone.utc).isoformat(),
        python=platform.python_version(),
        environment=dict(
            executable=sys.executable,
            platform=platform.platform(),
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
                    sha256=hashlib.sha256(
                        Path(module.__file__).read_bytes()
                    ).hexdigest(),
                )
                for name, module in sorted(sys.modules.items())
                if name.startswith("molsysmt")
                and getattr(module, "__file__", None)
                and Path(module.__file__).suffix in {".so", ".pyd", ".dylib"}
            ],
        ),
        producers=before,
        producers_unchanged=before == after,
        inputs=hashes,
        inputs_unchanged=unchanged,
        runs=runs,
        valid=valid,
        measurement="scientific controls only; no timing or memory measurements",
    )
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print("PASS" if valid else "FAIL", "observed EST template controls")
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
