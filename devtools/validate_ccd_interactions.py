"""Retain complete CCD interaction controls, declared placements and actual credits."""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import ackredit as ack
import molsysmt as msm
import numpy as np
import pyunitwizard

import pharmacophoremt as phmt
from devtools.benchmark_rigid_consensus import _source_record
from devtools.ccd_interaction_cases import build_case, observe_case
from devtools.prepared_ccd_ligands import credit_source
from devtools.validate_aromatic_interactions import _fingerprint, observation_report
from devtools.validate_prepared_ccd_ligands import scientific_projection
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt.io import load_json, to_json
from pharmacophoremt.modeler import (
    compose_pharmacophores,
    from_interaction_collection,
    get_excluded_volume_sites,
    get_features,
)
from pharmacophoremt.pharmacophore import Pharmacophore
from pharmacophoremt.screening import PoseEvaluator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests/data/ccd_interaction_cases.json"


def role_workflow(case, analyses, role, directory):
    """Compose existing public steps for either complete molecular participant."""
    source, selection = case["source"], case[role]
    other = case["partner" if role == "ligand" else "ligand"]
    query = from_interaction_collection(source, analyses, selection, radius=".02 nm")
    kept = from_interaction_collection(
        source, analyses, selection, radius=".02 nm", duplicate_policy="keep"
    )
    moved = msm.structure.translate(
        source, selection=selection, translation="[3,0,0] nm", in_place=False
    )
    path = Path(directory) / f"{role}.json"
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        unit_query = from_interaction_collection(
            source, analyses, selection, radius="20 pm"
        )
        to_json(unit_query, path)
        restored = load_json(path)
        roundtrip = PoseEvaluator(restored).evaluate(source, selection=selection)
    evaluator = PoseEvaluator(query)
    evaluations = dict(
        reference=evaluator.evaluate(source, selection=selection),
        displaced=evaluator.evaluate(moved, selection=selection),
        kept=PoseEvaluator(kept).evaluate(source, selection=selection),
        roundtrip=roundtrip,
    )
    inventory = get_features(source, selection=other, features=["included volume"])
    exclusions = get_excluded_volume_sites(inventory, radius=".05 nm")
    excluded = Pharmacophore(ref_struct=0)
    for site in exclusions["interaction_sites"]:
        excluded.add_interaction_site(site)
    joint = compose_pharmacophores({"positive": query, "excluded": excluded})
    evaluations["excluded"] = PoseEvaluator(joint).evaluate(source, selection=selection)
    return dict(
        selection=selection,
        model_metadata=query.metadata,
        sites=[
            dict(
                feature=site.feature_name,
                weight=site.weight,
                shape=site.shape_name,
                center=detached(site.center),
                radius=detached(site.radius),
                direction=detached(site.direction)
                if site.feature_name == "hb donor"
                else None,
                normal=detached(site.shape.normal)
                if site.feature_name == "aromatic ring"
                else None,
                metadata=site.metadata,
            )
            for site in query.interaction_sites
        ],
        kept_n_sites=kept.n_interaction_sites,
        kept_metadata=kept.metadata,
        exclusions=exclusions["report"],
        excluded_n_sites=excluded.n_interaction_sites,
        evaluations=evaluations,
        metadata_preserved=(
            restored.metadata == unit_query.metadata
            and [site.metadata for site in restored.interaction_sites]
            == [site.metadata for site in unit_query.interaction_sites]
        ),
    )


def workflow(expected, directory):
    case = build_case(expected["case_id"], expected["placement"])
    credit_source(expected["case_id"])
    source = case["source"]
    before = _fingerprint(source)
    analyses = observe_case(case)
    roles = {
        role: role_workflow(case, analyses, role, directory)
        for role in ("ligand", "partner")
    }
    # Redetect in the transformed common frame; native evidence from the original
    # frame is never passed to the moved source.
    rotation = np.array([[0.0, -1, 0], [1, 0, 0], [0, 0, 1]])
    translation = np.array([2.0, 1, -3])
    moved = msm.structure.rotate(
        source, rotation=rotation, rotation_center="[0,0,0] nm", in_place=False
    )
    moved = msm.structure.translate(
        moved, translation=puw.quantity(translation, "nm"), in_place=False
    )
    fresh = observe_case(dict(case, source=moved))
    original_query = from_interaction_collection(
        source, analyses, case["ligand"], radius=".02 nm"
    )
    moved_query = from_interaction_collection(
        moved, fresh, case["ligand"], radius=".02 nm"
    )
    covariance = dict(
        rotation=rotation.tolist(),
        translation=detached(puw.quantity(translation, "nm")),
        observations={
            label: observation_report(value) for label, value in fresh.items()
        },
        counts={label: value.n_interactions for label, value in fresh.items()},
        metadata=moved_query.metadata,
        membership_preserved=all(
            old.metadata["atom_indices"] == new.metadata["atom_indices"]
            for old, new in zip(
                original_query.interaction_sites,
                moved_query.interaction_sites,
                strict=True,
            )
        ),
        centers_covariant=all(
            np.allclose(
                puw.get_value(new.center, to_unit="nm"),
                puw.get_value(old.center, to_unit="nm") @ rotation.T + translation,
                rtol=0,
                atol=1e-14,
            )
            for old, new in zip(
                original_query.interaction_sites,
                moved_query.interaction_sites,
                strict=True,
            )
        ),
        evaluation=PoseEvaluator(moved_query).evaluate(moved, selection=case["ligand"]),
    )
    directional = None
    if expected["placement"] == "donor_contact":
        donor = next(
            site
            for site in original_query.interaction_sites
            if site.feature_name == "hb donor"
        )
        shift = -0.2 * puw.get_value(donor.direction, to_unit="dimensionless")
        candidate = msm.structure.translate(
            source,
            selection=[donor.metadata["atom_indices"][1]],
            translation=puw.quantity(shift, "nm"),
            in_place=False,
        )
        partner = from_interaction_collection(
            source, analyses, case["partner"], radius=".02 nm"
        )
        directional = dict(
            hydrogen=donor.metadata["atom_indices"][1],
            translation=detached(puw.quantity(shift, "nm")),
            ligand=PoseEvaluator(original_query).evaluate(
                candidate, selection=case["ligand"]
            ),
            partner=PoseEvaluator(partner).evaluate(
                candidate, selection=case["partner"]
            ),
        )
    return dict(
        expected=expected,
        fixture=case["report"],
        observations={
            label: observation_report(value) for label, value in analyses.items()
        },
        counts={label: value.n_interactions for label, value in analyses.items()},
        roles=roles,
        covariance=covariance,
        directional=directional,
        source_before=before,
        source_after=_fingerprint(source),
    )


def valid(result):
    expected, fixture = result["expected"], result["fixture"]
    checks = [
        result["source_before"] == result["source_after"],
        fixture["prepared_source_before"] == fixture["prepared_source_after"],
        fixture["component_chemistry_preserved"],
        fixture["component_atom_identity_preserved"],
        fixture["ligand_coordinates_preserved"],
        fixture["partner_translation_preserved"],
        fixture["input_bytes_unchanged"],
        result["counts"] == expected["observations"],
        result["covariance"]["counts"] == expected["observations"],
        result["covariance"]["membership_preserved"],
        result["covariance"]["centers_covariant"],
        result["covariance"]["evaluation"]["status"] == "matched",
    ]
    for role in result["roles"].values():
        evaluations = role["evaluations"]
        n_sites = expected["n_sites"]
        checks.extend(
            [
                len(role["sites"]) == n_sites,
                role["metadata_preserved"],
                all(
                    evaluations[key]["status"] == "matched"
                    and evaluations[key]["fit_value"] == 1
                    for key in ("reference", "roundtrip")
                ),
                evaluations["displaced"]["status"] == "not_matched",
                evaluations["displaced"]["fit_value"] == 0,
                role["kept_n_sites"] == n_sites + expected["n_duplicate_rings"],
                evaluations["kept"]["status"] == "not_matched",
                np.isclose(
                    evaluations["kept"]["fit_value"], n_sites / role["kept_n_sites"]
                ),
                len(evaluations["kept"]["missing_essential_sites"])
                == expected["n_duplicate_rings"],
                evaluations["excluded"]["fit_value"] == 1,
                len(evaluations["excluded"]["excluded_volume_clashes"])
                == expected["n_steric_clashes"],
                evaluations["excluded"]["status"]
                == ("not_matched" if expected["n_steric_clashes"] else "matched"),
            ]
        )
    if result["directional"] is not None:
        directional = result["directional"]
        checks.extend(
            [
                directional["ligand"]["status"] == "not_matched",
                np.isclose(
                    directional["ligand"]["fit_value"],
                    (expected["n_sites"] - 1) / expected["n_sites"],
                ),
                directional["partner"]["status"] == "matched",
            ]
        )
    return all(checks)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--provider-snapshot-record", type=Path)
    arguments = parser.parse_args(argv)
    expected = json.loads(MANIFEST.read_text())["cases"]
    producers = dict(
        pharmacophoremt=phmt, molsysmt=msm, pyunitwizard=pyunitwizard, ackredit=ack
    )
    before = {name: _source_record(module) for name, module in producers.items()}
    snapshot = None
    if arguments.provider_snapshot_record is not None:
        snapshot = json.loads(arguments.provider_snapshot_record.read_text())
        if (
            Path(snapshot["snapshot_package_path"]).resolve()
            != Path(msm.__file__).resolve().parent
            or snapshot["python_source_sha256"]
            != before["molsysmt"]["python_source_sha256"]
            or not snapshot["origin_unchanged_during_copy"]
            or not snapshot["snapshot_matches_origin"]
        ):
            raise ValueError(
                "provider snapshot must match the actually imported source"
            )
    runs = []
    with TemporaryDirectory(prefix="phmt-ccd-interactions-") as directory:
        for enabled in (False, True):
            with ack.session("complete-CCD-interactions"):
                with ack.capture("prepare-detect-compose-evaluate") as capture:
                    with phmt.attribution(enabled):
                        results = [workflow(case, directory) for case in expected]
                runs.append(
                    dict(
                        host_tracking=enabled,
                        valid=all(valid(result) for result in results),
                        results=results,
                        attribution=capture.attribution.to_dict(),
                    )
                )
    after = {name: _source_record(module) for name, module in producers.items()}
    paths = (
        Path(__file__).resolve(),
        ROOT / "devtools/ccd_interaction_cases.py",
        ROOT / "devtools/interaction_collection_cases.py",
        ROOT / "devtools/aromatic_interaction_cases.py",
        ROOT / "devtools/validate_aromatic_interactions.py",
        ROOT / "devtools/prepared_ccd_ligands.py",
        ROOT / "devtools/validate_prepared_ccd_ligands.py",
        MANIFEST,
        ROOT / "tests/data/prepared_ccd/manifest.json",
        ROOT / "tests/data/prepared_ccd/EST_ideal.sdf",
        ROOT / "tests/data/prepared_ccd/DES_ideal.sdf",
    )
    report = dict(
        schema="pharmacophoremt.ccd_interaction_validation@1",
        created_utc=datetime.now(timezone.utc).isoformat(),
        python=sys.version,
        executable=sys.executable,
        scope="complete_CCD_components_in_designed_placements_not_biological_complex_or_timing_benchmark",
        environment=before,
        environment_after=after,
        provider_snapshot=snapshot,
        producer_sources_unchanged=before == after,
        source_files={
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths
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
        tracking_independent_science=scientific_projection(runs[0]["results"])
        == scientific_projection(runs[1]["results"]),
    )
    arguments.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    passed = (
        all(run["valid"] for run in runs)
        and report["producer_sources_unchanged"]
        and report["tracking_independent_science"]
    )
    print("PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
