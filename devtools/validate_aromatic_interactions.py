"""Retain bounded aromatic profile and participant-policy comparison evidence."""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import ackredit as ack
import molsysmt as msm
import pyunitwizard

import pharmacophoremt as phmt
from devtools.aromatic_interaction_cases import (
    CATION_PROFILES,
    PI_PROFILES,
    build_case,
    observe,
)
from devtools.benchmark_rigid_consensus import _source_record
from devtools.prepared_ccd_ligands import state_payload
from devtools.validate_prepared_ccd_ligands import scientific_projection
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.io import load_json, to_json
from pharmacophoremt.modeler import from_interactions
from pharmacophoremt.screening import PoseEvaluator


def _fingerprint(source):
    """Hash the domains declared by these isolated analytical molecular inputs."""
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="nm")
    atoms = msm.get(
        source,
        element="atom",
        atom_id=True,
        atom_name=True,
        atom_type=True,
        output_type="dictionary",
    )
    return dict(
        coordinates_sha256=hashlib.sha256(coordinates.tobytes()).hexdigest(),
        coordinates_shape=list(coordinates.shape),
        chemical_state_sha256=hashlib.sha256(
            json.dumps(state_payload(source), sort_keys=True).encode()
        ).hexdigest(),
        atom_identity_sha256=hashlib.sha256(
            json.dumps(detached(atoms), sort_keys=True).encode()
        ).hexdigest(),
    )


def observation_report(observations):
    """Detach native column evidence with explicit-unit quantity-column encoding."""
    data = observations.to_dict()
    data["measurements"] = {
        key: puw.quantity(values, data["measure_units"][key])
        for key, values in data["measurements"].items()
    }
    # This is host evidence, not a dictionary for Interactions.from_dict.
    return dict(
        codec="pharmacophoremt.quantity_column_observation_evidence@1",
        data=detached(data),
    )


def workflow(directory):
    records = []
    for case in ("parallel", "edge", "atomic_cation", "compound_cation"):
        family = "pi_pi" if case in {"parallel", "edge"} else "cation_pi"
        profiles = PI_PROFILES if family == "pi_pi" else CATION_PROFILES
        for method, profile in profiles:
            source, first, second = build_case(case)
            before = _fingerprint(source)
            observations = observe(
                source, first, second, method, profile, family=family
            )
            outcomes = []
            for role, selection in (("first", first), ("second", second)):
                mapping = "exact"
                strict_outcome = None
                if (
                    case == "compound_cation"
                    and profile == "smarts_5_6"
                    and role == "first"
                ):
                    try:
                        from_interactions(source, observations, selection)
                    except ArgumentError as error:
                        strict_outcome = dict(
                            status="failed",
                            fit_value=None,
                            error_code=error.code,
                            reason=str(error),
                            cation_mapping="exact",
                        )
                    else:
                        raise AssertionError(
                            "strict membership must reject the declared partial cation reference"
                        )
                    mapping = "containing_center"
                query = from_interactions(
                    source,
                    observations,
                    selection,
                    radius=".02 nm",
                    cation_mapping=mapping,
                )
                evaluator = PoseEvaluator(query, direction_tolerance="10 degrees")
                positive = evaluator.evaluate(source, selection=selection)
                moved = msm.structure.translate(
                    source,
                    selection=selection,
                    translation="[1,0,0] nm",
                    in_place=False,
                )
                negative = evaluator.evaluate(moved, selection=selection)
                path = Path(directory) / (case + profile + role + ".json")
                to_json(query, path)
                restored = load_json(path)
                roundtrip = PoseEvaluator(
                    restored, direction_tolerance="10 degrees"
                ).evaluate(source, selection=selection)
                outcomes.append(
                    dict(
                        role=role,
                        selection=selection,
                        cation_mapping=mapping,
                        strict_outcome=strict_outcome,
                        model_metadata=query.metadata,
                        sites=[
                            dict(
                                feature=site.feature_name,
                                shape=site.shape_name,
                                center=detached(site.center),
                                radius=detached(site.radius),
                                normal=None
                                if site.shape_name != "disk"
                                else detached(site.shape.normal),
                                metadata=site.metadata,
                            )
                            for site in query.interaction_sites
                        ],
                        reference=positive,
                        displaced=negative,
                        roundtrip=roundtrip,
                        metadata_preserved=(
                            restored.metadata == query.metadata
                            and [site.metadata for site in restored.interaction_sites]
                            == [site.metadata for site in query.interaction_sites]
                        ),
                    )
                )
            records.append(
                dict(
                    case=case,
                    family=family,
                    method=method,
                    profile=profile,
                    observations=observation_report(observations),
                    outcomes=outcomes,
                    source_before=before,
                    source_after=_fingerprint(source),
                )
            )
    return records


def valid(records):
    return len(records) == 14 and all(
        record["source_before"] == record["source_after"]
        and len(record["outcomes"]) == 2
        and all(
            len(outcome["sites"]) == 1
            and outcome["metadata_preserved"]
            and outcome["reference"]["status"]
            == outcome["roundtrip"]["status"]
            == "matched"
            and outcome["reference"]["fit_value"]
            == outcome["roundtrip"]["fit_value"]
            == 1
            and outcome["displaced"]["status"] == "not_matched"
            and outcome["displaced"]["fit_value"] == 0
            for outcome in record["outcomes"]
        )
        for record in records
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args(argv)
    producers = dict(
        pharmacophoremt=phmt, molsysmt=msm, pyunitwizard=pyunitwizard, ackredit=ack
    )
    before = {name: _source_record(module) for name, module in producers.items()}
    runs = []
    with TemporaryDirectory(prefix="phmt-aromatic-") as directory:
        for enabled in (False, True):
            with ack.session("aromatic-validation"):
                with ack.capture("aromatic-workflow") as capture:
                    with phmt.attribution(enabled):
                        records = workflow(directory)
                runs.append(
                    dict(
                        host_tracking=enabled,
                        valid=valid(records),
                        records=records,
                        attribution=capture.attribution.to_dict(),
                    )
                )
    after = {name: _source_record(module) for name, module in producers.items()}
    root = Path(__file__).resolve().parents[1]
    report = dict(
        schema="pharmacophoremt.aromatic_validation@1",
        created_utc=datetime.now(timezone.utc).isoformat(),
        python=sys.version,
        executable=sys.executable,
        scope="prepared_analytical_profiles_not_biological_or_timing_benchmark",
        environment=before,
        producer_sources_unchanged=before == after,
        source_files={
            str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in [
                Path(__file__).resolve(),
                root / "devtools/aromatic_interaction_cases.py",
                root / "devtools/prepared_ccd_ligands.py",
                root / "devtools/validate_prepared_ccd_ligands.py",
            ]
        },
        molecular_extensions=[
            dict(
                module=name,
                path=str(module.__file__),
                sha256=hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest(),
            )
            for name, module in sorted(sys.modules.items())
            if name.startswith("molsysmt.")
            and getattr(module, "__file__", None)
            and str(module.__file__).endswith(".so")
        ],
        runs=runs,
        performance_measured=False,
        tracking_independent_science=scientific_projection(runs[0]["records"])
        == scientific_projection(runs[1]["records"]),
    )
    arguments.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    passed = (
        all(run["valid"] for run in runs)
        and report["tracking_independent_science"]
        and report["producer_sources_unchanged"]
    )
    print("PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
