"""Execute prepared analytical ionic workflows and retain portable evidence."""

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
from devtools.validate_prepared_ccd_ligands import scientific_projection
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt.io import load_json, to_json
from pharmacophoremt.modeler import from_interactions
from pharmacophoremt.screening import PoseEvaluator


def source(smiles, coordinates):
    """Create declared fixture chemistry and geometry through MolSysMT."""
    result = msm.convert(
        msm.convert("smiles:" + smiles, to_form="rdkit.Mol"),
        to_form="molsysmt.MolSys",
    )
    result.structures.append(coordinates=puw.quantity([coordinates], "nm"))
    return result


def workflow(directory):
    cases = [
        ("atomic", "[Na+].[Cl-]", [[0, 0, 0], [0.3, 0, 0]], [0], [1]),
        (
            "carboxylate",
            "CC(=O)[O-].[Na+].[Na+]",
            [
                [0, -0.15, 0],
                [0, 0, 0],
                [-0.1, 0.1, 0],
                [0.1, 0.1, 0],
                [0.1, 0.4, 0],
                [-0.1, 0.4, 0],
            ],
            [0, 1, 2, 3],
            [4, 5],
        ),
        (
            "guanidinium",
            "NC(=[NH2+])N.[Cl-]",
            [
                [-0.1, 0, 0],
                [0, 0, 0],
                [0.1, 0, 0],
                [0, 0.15, 0],
                [0, 0.4, 0],
            ],
            [0, 1, 2, 3],
            [4],
        ),
    ]
    result = []
    for label, smiles, xyz, ligand, partner in cases:
        molecular_system = source(smiles, xyz)
        before = puw.get_value(
            msm.get(molecular_system, coordinates=True), to_unit="nm"
        ).copy()
        observed = msm.interactions.ionic.get_ionic_interactions(
            molecular_system,
            "0.31 nm",
            selection=ligand,
            selection_2=partner,
            selection_mode="between",
            structure_indices=[0],
            pbc=False,
        )
        positive = []
        for role, selection in (("first", ligand), ("second", partner)):
            query = from_interactions(
                molecular_system, observed, selection, radius="0.02 nm"
            )
            evaluator = PoseEvaluator(query)
            reference = evaluator.evaluate(molecular_system, selection=selection)
            displaced = msm.structure.translate(
                molecular_system,
                translation="[1,0,0] nm",
                selection=selection,
                in_place=False,
            )
            negative = evaluator.evaluate(displaced, selection=selection)
            path = Path(directory) / (label + "_" + role + ".json")
            to_json(query, path)
            restored = load_json(path)
            roundtrip = PoseEvaluator(restored).evaluate(
                molecular_system, selection=selection
            )
            positive.append(
                dict(
                    role=role,
                    selection=selection,
                    model_metadata=query.metadata,
                    sites=[
                        dict(
                            feature=site.feature_name,
                            center=puw.QuantityRecord.from_quantity(
                                site.center
                            ).to_dict(),
                            radius=puw.QuantityRecord.from_quantity(
                                site.radius
                            ).to_dict(),
                            essential=site.essential,
                            weight=site.weight,
                            metadata=site.metadata,
                        )
                        for site in query.interaction_sites
                    ],
                    reference=reference,
                    displaced=negative,
                    roundtrip=roundtrip,
                    roundtrip_metadata_preserved=(
                        restored.metadata == query.metadata
                        and [site.metadata for site in restored.interaction_sites]
                        == [site.metadata for site in query.interaction_sites]
                    ),
                )
            )
        result.append(
            dict(
                label=label,
                input=dict(smiles=smiles, coordinates_nm=xyz),
                observations=detached(observed.to_dict()),
                outcomes=positive,
                source_preserved=np.array_equal(
                    before,
                    puw.get_value(
                        msm.get(molecular_system, coordinates=True), to_unit="nm"
                    ),
                ),
            )
        )
    return result


def valid(cases):
    return len(cases) == 3 and all(
        case["source_preserved"]
        and all(
            outcome["reference"]["status"]
            == outcome["roundtrip"]["status"]
            == "matched"
            and outcome["reference"]["fit_value"]
            == outcome["roundtrip"]["fit_value"]
            == 1
            and outcome["displaced"]["status"] == "not_matched"
            and outcome["displaced"]["fit_value"] == 0
            and outcome["roundtrip_metadata_preserved"]
            for outcome in case["outcomes"]
        )
        for case in cases
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
    with TemporaryDirectory(prefix="phmt-ionic-") as directory:
        for enabled in (False, True):
            with ack.session("ionic-validation"):
                with ack.capture("ionic-workflow") as capture:
                    with phmt.attribution(enabled):
                        cases = workflow(directory)
                runs.append(
                    dict(
                        host_attribution_enabled=enabled,
                        cases=cases,
                        valid=valid(cases),
                        attribution=capture.attribution.to_dict(),
                    )
                )
    files = {
        "ionic_detector": Path(msm.__file__).resolve().parent
        / "interactions/ionic/get_ionic_interactions.py",
        "ionic_modeler": Path(__file__).resolve().parents[1]
        / "pharmacophoremt/modeler/interaction_based.py",
        "shared_features": Path(__file__).resolve().parents[1]
        / "pharmacophoremt/modeler/features.py",
        "validation_driver": Path(__file__).resolve(),
    }
    after = {name: _source_record(module) for name, module in producers.items()}
    report = dict(
        schema="pharmacophoremt.ionic_validation@1",
        created_utc=datetime.now(timezone.utc).isoformat(),
        scope="prepared_analytical_geometries_not_biological_validation",
        environment=dict(
            python=sys.version,
            executable=sys.executable,
            pharmacophoremt=phmt.__version__,
            molsysmt=msm.__version__,
            numpy=np.__version__,
            ackredit=ack.__version__,
        ),
        producer_sources=before,
        producer_sources_unchanged=before == after,
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
        source_files={
            name: dict(
                path=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest()
            )
            for name, path in files.items()
        },
        runs=runs,
        tracking_independent_science=scientific_projection(runs[0]["cases"])
        == scientific_projection(runs[1]["cases"]),
        performance_measured=False,
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
