"""Small native owner inputs and controls for BindingMT's H0/H1 receiving."""

import argparse
import hashlib
import json
from pathlib import Path

import ackredit as ack
import molsysmt as msm
import numpy as np

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.interaction_site import InteractionSite
from pharmacophoremt.interaction_site.shape import Sphere
from pharmacophoremt.modeler import (
    copy_pharmacophore,
    edit_pharmacophore,
    from_interaction_collection,
)
from pharmacophoremt.screening import PoseEvaluator

PARTICIPANTS = {"A": [0], "B": [1], "C": [2], "D": [3]}
COORDINATES = [[0, 0, 0], [0.2, 0, 0], [0, 0.25, 0], [0, 0.45, 0]]
EXPECTED_PAIRS = [[0, 1], [0, 2], [2, 3]]


def build_source():
    """Construct the independent four-ion input through public molecular tools."""
    source = msm.convert(
        msm.convert("smiles:[Cl-].[Na+].[Na+].[Cl-]", to_form="rdkit.Mol"),
        to_form="molsysmt.MolSys",
    )
    source.structures.append(coordinates=puw.quantity([COORDINATES], "nm"))
    return source


def observe(source):
    """Run three explicitly declared native ionic analyses, including empty."""
    return {
        name: msm.interactions.ionic.get_ionic_interactions(
            source,
            threshold,
            selection="all",
            structure_indices=[0],
            selection_mode="internal",
            pbc=False,
        )
        for name, threshold in (
            ("ionic_031", "0.31 nm"),
            ("ionic_035", "0.35 nm"),
            ("ionic_empty", "0.01 nm"),
        )
    }


def observation_rows(observed):
    """Inspect occurrence correspondence; this is not native serialization."""
    data = observed.to_dict()
    rows = []
    for relation, occurrence in zip(
        data["relation_indices"], data["occurrence_indices"]
    ):
        members = sorted(
            int(atom)
            for part in observed.relation(int(relation))["participants"]
            for atom in part["atom_indices"]
        )
        rows.append(
            dict(pair=members, relation=int(relation), occurrence=int(occurrence))
        )
    return rows


def scope(analyses):
    """Use the public owner query without changing source axes or original data."""
    return {
        name: result.between_selections(
            [0, 1], [2], structure_indices=[0], exclusive=True
        )
        for name, result in analyses.items()
    }


def construct(source):
    """Build one observed-participant model from compatible cached analyses."""
    return from_interaction_collection(
        source, scope(source.interactions), [2], radius="0.02 nm"
    )


def curated_controls(model):
    """Separate native controls: zero-weight essential and exclusion veto."""
    missing = copy_pharmacophore(model)
    missing.add_interaction_site(
        InteractionSite(Sphere("[9,0,0] nm", "0.02 nm"), "hydrophobicity")
    )
    zero = edit_pharmacophore(
        missing,
        site_indices=1,
        weight=0,
        reason="analytical missing essential site; zero weight is not optional",
    )
    veto = copy_pharmacophore(model)
    veto.add_interaction_site(
        InteractionSite(
            Sphere("[0,0.25,0] nm", "0.05 nm"),
            "excluded volume",
            essential=False,
            weight=0,
        )
    )
    return {"zero_essential": zero, "excluded": veto}


def _artifact(path):
    return {
        "path": path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "bytes": path.stat().st_size,
    }


def create_package(directory):
    """Emit fresh native assets; existing destinations are never overwritten."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=False)
    source = build_source()
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    source.interactions = observe(source)
    msm.h5msm.write(source, str(directory / "source.h5msm"), format_version="1.0")
    recovered = msm.h5msm.read(str(directory / "source.h5msm"))
    primary = construct(recovered)
    alternative = msm.structure.translate(
        source, selection=[2], translation="[0,.05,0] nm", in_place=False
    )
    alternative.interactions = observe(alternative)
    msm.h5msm.write(
        alternative, str(directory / "alternative.h5msm"), format_version="1.0"
    )
    alt_read = msm.h5msm.read(str(directory / "alternative.h5msm"))
    hypotheses = {"primary": primary, "alternative": construct(alt_read)}
    hypotheses.update(curated_controls(primary))
    for name, model in hypotheses.items():
        phmt.io.to_json(model, str(directory / (name + ".json")))
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )
    scoped = scope(recovered.interactions)
    links = [
        dict(
            source="source.h5msm",
            analysis=name,
            relation=row["relation"],
            occurrence=row["occurrence"],
            hypothesis="primary.json",
            site=0,
        )
        for name, observed in scoped.items()
        for row in observation_rows(observed)
    ]
    manifest = {
        "test_case": "phmt-binding-interface-native-handoff-v1",
        "scope": "authored analytical owner inputs; not BindingMT records or adoption",
        "participants": PARTICIPANTS,
        "grouping": [["A", "B"], ["C"]],
        "coordinates_nm": COORDINATES,
        "expected_original_pairs": EXPECTED_PAIRS,
        "expected_scoped_pairs": [[0, 2]],
        "structure_index": 0,
        "chemical_state": 0,
        "atom_map_profile": "identity; no nonidentity/chemical-state transfer qualified",
        "analysis_site_links": links,
        "expected_primary": {
            "sites": 1,
            "kind": "positive charge",
            "weight": 1,
            "essential": True,
        },
        "artifacts": {p.name: _artifact(p) for p in sorted(directory.iterdir())},
        "producer": {
            "pharmacophoremt": phmt.__version__,
            "molsysmt": msm.__version__,
            "pyunitwizard": puw.__version__,
        },
        "license": "Newly authored synthetic controls; repository license applies",
    }
    (directory / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def load_package(directory):
    """Verify exact frozen assets, then explicitly invoke their owner readers."""
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text())
    for name, expected in manifest["artifacts"].items():
        if _artifact(directory / name) != expected:
            raise ValueError("Handoff artifact differs from its manifest: " + name)
    source = msm.h5msm.read(str(directory / "source.h5msm"))
    models = {
        name: phmt.io.load_json(str(directory / (name + ".json")))
        for name in ("primary", "alternative", "zero_essential", "excluded")
    }
    return manifest, source, models


def receive_package(directory):
    """Return measured native outcomes for comparison with independent oracles."""
    manifest, source, models = load_package(directory)
    alternative = msm.h5msm.read(str(Path(directory) / "alternative.h5msm"))
    kept = from_interaction_collection(
        source,
        scope(source.interactions),
        [2],
        radius="0.02 nm",
        duplicate_policy="keep",
    )
    rebuilt = construct(source)
    evaluations = {
        name: PoseEvaluator(query).evaluate(candidate, selection=[2])
        for name, query, candidate in (
            ("primary_self", models["primary"], source),
            ("primary_alternative", models["primary"], alternative),
            ("alternative_self", models["alternative"], alternative),
            ("alternative_primary", models["alternative"], source),
            ("zero_essential", models["zero_essential"], source),
            ("excluded", models["excluded"], source),
            ("keep", kept, source),
        )
    }
    return {
        "test_case": manifest["test_case"],
        "original_rows": {
            name: observation_rows(observed)
            for name, observed in source.interactions.items()
        },
        "scoped_rows": {
            name: observation_rows(observed)
            for name, observed in scope(source.interactions).items()
        },
        "rebuilt_primary_sites": rebuilt.n_interaction_sites,
        "evaluations": {
            name: {
                "status": result["status"],
                "fit_value": result["fit_value"],
                "missing_essential_sites": result["missing_essential_sites"],
                "excluded_volume_clashes": result["excluded_volume_clashes"],
            }
            for name, result in evaluations.items()
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--output-directory")
    action.add_argument("--read-directory")
    parser.add_argument("--length-unit", choices=("nm", "pm"), default="nm")
    args = parser.parse_args(argv)
    puw.configure.set_standard_units(
        [args.length_unit, "fs", "K", "mole", "dalton", "e", "kJ/mol", "radians"],
        provenance="phmt-native-handoff-application",
    )
    with ack.capture("native-handoff-owner-operations") as capture:
        if args.output_directory:
            result = create_package(args.output_directory)
            result = {
                "created": args.output_directory,
                "artifacts": result["artifacts"],
            }
        else:
            result = receive_package(args.read_directory)
    result["attribution"] = capture.attribution.to_dict()
    print(json.dumps(result))


if __name__ == "__main__":
    main()
