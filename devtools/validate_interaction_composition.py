"""Retain five-family composition controls and actual optional attribution."""

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
from devtools.benchmark_rigid_consensus import _source_record
from devtools.interaction_collection_cases import build_case, observe
from devtools.validate_aromatic_interactions import _fingerprint, observation_report
from devtools.validate_prepared_ccd_ligands import scientific_projection
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt.io import load_json, to_json
from pharmacophoremt.modeler import (
    compose_pharmacophores,
    from_interaction_collection,
    from_interactions,
    get_excluded_volume_sites,
    get_features,
)
from pharmacophoremt.pharmacophore import Pharmacophore
from pharmacophoremt.screening import PoseEvaluator


def workflow(directory):
    source, ligand, partner = build_case()
    before = _fingerprint(source)
    analyses = observe(source, ligand, partner)
    query = from_interaction_collection(source, analyses, ligand, radius=".02 nm")
    components = {
        label: from_interactions(source, observed, ligand, radius=".02 nm")
        for label, observed in analyses.items()
    }
    modular = compose_pharmacophores(components, duplicate_policy="same_participant")
    kept = compose_pharmacophores(components)
    moved = msm.structure.translate(
        source, selection=ligand, translation="[1,0,0] nm", in_place=False
    )
    reversed_h = msm.structure.translate(
        source, selection=[7], translation="[-.2,0,0] nm", in_place=False
    )
    path = Path(directory) / "query.json"
    to_json(query, path)
    restored = load_json(path)
    evaluator = PoseEvaluator(query)
    evaluations = dict(
        reference=evaluator.evaluate(source, selection=ligand),
        displaced=evaluator.evaluate(moved, selection=ligand),
        donor_reversed=evaluator.evaluate(reversed_h, selection=ligand),
        roundtrip=PoseEvaluator(restored).evaluate(source, selection=ligand),
        modular=PoseEvaluator(modular).evaluate(source, selection=ligand),
        kept=PoseEvaluator(kept).evaluate(source, selection=ligand),
    )
    broad = from_interaction_collection(source, analyses, ligand, radius=".4 nm")
    inventory = get_features(source, selection=[16], features=["included volume"])
    exclusions = get_excluded_volume_sites(inventory, radius=".05 nm")
    excluded = Pharmacophore(ref_struct=0)
    for site in exclusions["interaction_sites"]:
        excluded.add_interaction_site(site)
    joint = compose_pharmacophores({"positive": broad, "excluded": excluded})
    collision = msm.structure.translate(
        source, selection=[6], translation="[.25,0,0] nm", in_place=False
    )
    evaluations.update(
        broad_reference=PoseEvaluator(joint).evaluate(source, selection=ligand),
        collision_positive=PoseEvaluator(broad).evaluate(collision, selection=ligand),
        collision_excluded=PoseEvaluator(joint).evaluate(collision, selection=ligand),
    )
    return dict(
        ligand=ligand,
        partner=partner,
        observations={
            label: observation_report(observed) for label, observed in analyses.items()
        },
        model_metadata=query.metadata,
        sites=[
            dict(
                feature=site.feature_name,
                weight=site.weight,
                shape=site.shape_name,
                center=detached(site.center),
                radius=detached(site.radius),
                metadata=site.metadata,
            )
            for site in query.interaction_sites
        ],
        modular_metadata=modular.metadata,
        kept_metadata=kept.metadata,
        exclusions=exclusions["report"],
        evaluations=evaluations,
        metadata_preserved=(
            restored.metadata == query.metadata
            and [site.metadata for site in restored.interaction_sites]
            == [site.metadata for site in query.interaction_sites]
        ),
        source_before=before,
        source_after=_fingerprint(source),
    )


def valid(report):
    outcomes = report["evaluations"]
    return (
        report["source_before"] == report["source_after"]
        and report["metadata_preserved"]
        and len(report["sites"]) == 9
        and sum(site["weight"] for site in report["sites"]) == 9
        and all(
            outcomes[name]["status"] == "matched" and outcomes[name]["fit_value"] == 1
            for name in (
                "reference",
                "roundtrip",
                "modular",
                "broad_reference",
                "collision_positive",
            )
        )
        and outcomes["displaced"]["status"] == "not_matched"
        and outcomes["displaced"]["fit_value"] == 0
        and outcomes["donor_reversed"]["status"] == "not_matched"
        and outcomes["donor_reversed"]["fit_value"] == 8 / 9
        and outcomes["kept"]["status"] == "not_matched"
        and outcomes["kept"]["fit_value"] == 9 / 11
        and outcomes["collision_excluded"]["status"] == "not_matched"
        and outcomes["collision_excluded"]["fit_value"] == 1
        and outcomes["collision_excluded"]["excluded_volume_clashes"]
        == [dict(site_index=9, atom_index=6)]
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
    with TemporaryDirectory(prefix="phmt-composition-") as directory:
        for enabled in (False, True):
            with ack.session("composition-validation"):
                with ack.capture("detect-compose-evaluate") as capture:
                    with phmt.attribution(enabled):
                        result = workflow(directory)
                runs.append(
                    dict(
                        host_tracking=enabled,
                        valid=valid(result),
                        result=result,
                        attribution=capture.attribution.to_dict(),
                    )
                )
    after = {name: _source_record(module) for name, module in producers.items()}
    root = Path(__file__).resolve().parents[1]
    report = dict(
        schema="pharmacophoremt.interaction_composition_validation@1",
        created_utc=datetime.now(timezone.utc).isoformat(),
        python=sys.version,
        executable=sys.executable,
        scope="disconnected_prepared_analytical_selection_not_binding_complex_or_timing_benchmark",
        environment=before,
        producer_sources_unchanged=before == after,
        source_files={
            str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (
                Path(__file__).resolve(),
                root / "devtools/interaction_collection_cases.py",
                root / "devtools/aromatic_interaction_cases.py",
                root / "devtools/validate_aromatic_interactions.py",
                root / "devtools/prepared_ccd_ligands.py",
                root / "devtools/validate_prepared_ccd_ligands.py",
            )
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
        tracking_independent_science=scientific_projection(runs[0]["result"])
        == scientific_projection(runs[1]["result"]),
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
