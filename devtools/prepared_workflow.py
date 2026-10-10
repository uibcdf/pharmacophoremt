"""Opt-in prepared CCD workflow controls; no activity or performance claim.

Run: python -m devtools.prepared_workflow --output FILE
Molecular operations use MolSysMT. This fixed case composes existing PHMT tools;
it is neither a molecular preparation service nor a new screening method.
"""

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from devtools.benchmark_rigid_consensus import THREAD_VARS, _source_record
from devtools.prepared_ccd_ligands import (
    DIRECTORY,
    MANIFEST_PATH,
    ROOT,
    credit_source,
    prepare_case,
    state_payload,
)
from devtools.validate_prepared_ccd_ligands import scientific_projection

FEATURES = ["hydrophobicity", "aromatic ring"]


def models_equivalent(actual, expected):
    """Case oracle: exact evidence/constraints, geometry within 1e-12 nm/unit."""
    import numpy as np

    if {k: v for k, v in actual.items() if k != "interaction_sites"} != {
        k: v for k, v in expected.items() if k != "interaction_sites"
    }:
        return False
    if len(actual["interaction_sites"]) != len(expected["interaction_sites"]):
        return False
    for a, b in zip(actual["interaction_sites"], expected["interaction_sites"]):
        if {k: v for k, v in a.items() if k != "shape"} != {
            k: v for k, v in b.items() if k != "shape"
        }:
            return False
        if (
            a["shape"].keys() != b["shape"].keys()
            or a["shape"]["type"] != b["shape"]["type"]
        ):
            return False
        for key in a["shape"].keys() - {"type"}:
            if not np.allclose(a["shape"][key], b["shape"][key], rtol=0, atol=1e-12):
                return False
    return True


def codecs():
    from pharmacophoremt.io import (
        load_json,
        load_sdf,
        load_yaml,
        to_json,
        to_sdf,
        to_yaml,
    )

    return [
        ("json", to_json, load_json),
        ("yaml", to_yaml, load_yaml),
        ("sdf", to_sdf, load_sdf),
    ]


def native_record(model, directory, stem):
    """Obtain the existing native payload through its public writer."""
    from pharmacophoremt.io import to_json

    path = directory / (stem + ".json")
    to_json(model, path)
    return json.loads(path.read_text())


def build_hypotheses(prepared):
    from pharmacophoremt.modeler import (
        edit_pharmacophore,
        extract_pharmacophore,
        from_feature_inventory,
        get_interaction_site_indices,
    )

    original = from_feature_inventory(
        prepared["inventory"], radius=".02 nm", name="CCD EST observations"
    )
    original.score = 0.9  # Sentinel for invalidation, not an activity score.
    rings = get_interaction_site_indices(original, feature_names="aromatic ring")
    hydrophobic = get_interaction_site_indices(original, feature_names="hydrophobicity")
    selected = extract_pharmacophore(
        original,
        site_indices=[*rings, *hydrophobic],
        reason="declared ring-first hypothesis order",
    )
    optional = edit_pharmacophore(
        selected,
        site_indices=range(1, 10),
        essential=False,
        reason="declared optional hydrophobic support",
    )
    narrow = edit_pharmacophore(
        optional,
        site_indices=0,
        weight=3,
        reason="declared obligatory aromatic weight",
    )
    wide = edit_pharmacophore(
        narrow,
        site_indices=0,
        radius=".10 nm",
        reason="independent 0.05 nm displacement control",
    )
    return original, narrow, wide


def candidates(source):
    import molsysmt as msm

    near = msm.structure.translate(source, translation="[0,0,.05] nm", in_place=False)
    far = msm.structure.translate(source, translation="[0,0,2] nm", in_place=False)
    unprepared = msm.convert(
        msm.convert("smiles:CCC", to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
    )
    # Repeated source is an input-order tie control, not another unique molecule.
    return [near, source, far, unprepared, source]


def screen(query, inputs):
    from pharmacophoremt.screening import VirtualScreening

    runner = VirtualScreening(
        query,
        screening_method="placed",
        min_fit_value=0.2,
        direction_tolerance="1 degree",
    )
    hits = runner.run(
        inputs, chemical_state="reference", structure_index=0, on_error="record"
    )
    return dict(
        evaluations=runner.evaluations,
        hit_input_indices=[hit["input_index"] for hit in hits],
        hit_source_references_preserved=all(
            hit["mol"] is inputs[hit["input_index"]] for hit in hits
        ),
        scalar_hits=runner.to_dataframe().to_dict(orient="records"),
    )


def numerical_oracle(prepared):
    """Independent fixed-fixture distance checks, not a molecular tool."""
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    inventory = prepared["inventory"]["features"]
    centers = np.asarray(
        [
            puw.get_value(row["center"], to_unit="nm")
            for row in inventory
            if row["kind"] == "hydrophobicity"
        ]
    )
    return dict(
        hydrophobic_count=len(centers),
        aromatic_count=1,
        near_min_hydrophobic_distance_nm=float(
            np.linalg.norm(
                centers[:, None, :] - (centers[None, :, :] + [0, 0, 0.05]), axis=-1
            ).min()
        ),
        near_aromatic_distance_nm=0.05,
        far_min_hydrophobic_distance_nm=float(
            np.linalg.norm(
                centers[:, None, :] - (centers[None, :, :] + [0, 0, 2]), axis=-1
            ).min()
        ),
        far_aromatic_distance_nm=2.0,
        partial_coverage=3 / (3 + 9),
        narrow_radius_nm=0.02,
        wide_aromatic_radius_nm=0.10,
    )


def read_models(directory, *, model_names=("narrow", "wide", "veto")):
    """Fresh-process public readers: no detection, evaluation or new credits."""
    import ackredit

    records = {}
    with TemporaryDirectory(prefix="phmt-49-reader-") as temporary:
        for suffix, _, read in codecs():
            for name in model_names:
                records[name + "." + suffix] = native_record(
                    read(directory / (name + "." + suffix)), Path(temporary), name
                )
    return dict(models=records, attribution=ackredit.get_attribution().to_dict())


def run_case(directory, *, fresh_reader=False):
    import molsysmt as msm

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.interaction_site import InteractionSite
    from pharmacophoremt.interaction_site.shape import Sphere
    from pharmacophoremt.modeler import copy_pharmacophore

    prepared = prepare_case("EST", features=FEATURES)
    source = prepared["molecular_system"]
    inputs = candidates(source)
    unique_sources = inputs[:3]
    before = [
        dict(
            coordinates_nm=puw.get_value(
                msm.get(item, coordinates=True), to_unit="nm"
            ).tolist(),
            chemical_state=state_payload(item),
        )
        for item in unique_sources
    ]
    original, narrow, wide = build_hypotheses(prepared)
    veto = copy_pharmacophore(wide)
    # Fixed public CCD atom-zero position, independently checked by the guard.
    veto.add_interaction_site(
        InteractionSite(
            Sphere("[.1463,-.0446,-.2486] nm", ".01 nm"),
            "excluded volume",
            essential=False,
            weight=0,
        )
    )
    models = dict(narrow=narrow, wide=wide, veto=veto)
    results, artifacts, native = {}, {}, {}
    with puw.context(standard_units=["pm", "fs", "degrees"]):
        for name, query in models.items():
            native[name] = native_record(query, directory, name + "-original")
            for suffix, write, read in codecs():
                path = directory / (name + "." + suffix)
                write(query, path)
                raw = path.read_bytes()
                artifacts[path.name] = dict(
                    sha256=hashlib.sha256(raw).hexdigest(),
                    byte_count=len(raw),
                    utf8=raw.decode(),
                )
                # Read/evaluate under a different application unit policy.
                with puw.context(standard_units=["angstrom", "ps", "radians"]):
                    restored = read(path)
                    results[path.name] = dict(
                        native=native_record(restored, directory, "restored"),
                        screening=screen(restored, inputs),
                    )
    after = [
        dict(
            coordinates_nm=puw.get_value(
                msm.get(item, coordinates=True), to_unit="nm"
            ).tolist(),
            chemical_state=state_payload(item),
        )
        for item in unique_sources
    ]
    reader = None
    if fresh_reader:
        child = subprocess.run(
            [
                sys.executable,
                "-m",
                "devtools.prepared_workflow",
                "--read",
                str(directory),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        reader = dict(**json.loads(child.stdout), stderr=child.stderr)
    return dict(
        preparation=prepared["report"],
        oracle=numerical_oracle(prepared),
        original_model=native_record(original, directory, "observed"),
        models=native,
        inputs_before=before,
        inputs_after=after,
        source_coordinates_and_states_unchanged=before == after,
        original_source_atom_zero_nm=before[1]["coordinates_nm"][0][0],
        artifacts=artifacts,
        results=results,
        fresh_reader=reader,
    )


def expectations_passed(result):
    """Declared case acceptance; detailed independent guards live in tests."""
    oracle = result["oracle"]
    if not (
        result["source_coordinates_and_states_unchanged"]
        and oracle["near_min_hydrophobic_distance_nm"] > 0.02
        and oracle["far_min_hydrophobic_distance_nm"] > 0.10
        and all(
            abs(a - b) < 1e-12
            for a, b in zip(
                result["original_source_atom_zero_nm"], [0.1463, -0.0446, -0.2486]
            )
        )
    ):
        return False
    for name, record in result["results"].items():
        variant = name.split(".")[0]
        output = record["screening"]
        evaluations = output["evaluations"]
        expected = {
            "narrow": ["not_matched", "matched", "not_matched", "failed", "matched"],
            "wide": ["matched", "matched", "not_matched", "failed", "matched"],
            "veto": ["matched", "not_matched", "not_matched", "failed", "not_matched"],
        }[variant]
        if [row["status"] for row in evaluations] != expected:
            return False
        if [row["fit_value"] for row in evaluations] != [
            0.25 if variant != "narrow" else 0.0,
            1.0,
            0.0,
            None,
            1.0,
        ]:
            return False
        if (
            output["hit_input_indices"]
            != {"narrow": [1, 4], "wide": [1, 4, 0], "veto": [0]}[variant]
        ):
            return False
        if (
            not models_equivalent(record["native"], result["models"][variant])
            or not output["hit_source_references_preserved"]
        ):
            return False
    reader = result["fresh_reader"]
    return reader is None or (
        not reader["attribution"]["uses"]
        and all(
            models_equivalent(value, result["models"][name.split(".")[0]])
            for name, value in reader["models"].items()
        )
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--output", type=Path)
    target.add_argument("--read", type=Path)
    parser.add_argument("--case", choices=("placed", "search"), default="placed")
    args = parser.parse_args(argv)
    if args.read:
        names = ("rigid",) if args.case == "search" else ("narrow", "wide", "veto")
        print(json.dumps(read_models(args.read, model_names=names), allow_nan=False))
        return 0
    review_case, check_case = run_case, expectations_passed
    if args.case == "search":
        from devtools.prepared_search_workflow import (
            expectations_passed as check_case,
        )
        from devtools.prepared_search_workflow import run_case as review_case
    for key in THREAD_VARS:
        os.environ[key] = "1"
    import ackredit
    import molsysmt as msm
    import pyunitwizard

    import pharmacophoremt as phmt

    msm.configure.set_parallelization(parallel=False, num_threads=1)
    packages = dict(
        pharmacophoremt=phmt, molsysmt=msm, pyunitwizard=pyunitwizard, ackredit=ackredit
    )
    before = {name: _source_record(module) for name, module in packages.items()}
    paths = [
        Path(__file__),
        ROOT / "devtools/prepared_ccd_ligands.py",
        MANIFEST_PATH,
        DIRECTORY / "EST_ideal.sdf",
        ROOT / "tests/test_prepared_workflow.py",
        ROOT / "devtools/benchmark_rigid_consensus.py",
        ROOT / "devtools/validate_prepared_ccd_ligands.py",
    ]
    if args.case == "search":
        paths.extend(
            [
                ROOT / "devtools/prepared_search_workflow.py",
                ROOT / "tests/test_prepared_search_workflow.py",
            ]
        )

    def identities():
        return {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths
        }

    inputs_before = identities()
    records = []
    for enabled in (False, True):
        with TemporaryDirectory(prefix="phmt-49-case-") as directory:
            with (
                ackredit.session("prepared end-to-end control"),
                phmt.attribution(enabled),
            ):
                result = review_case(Path(directory), fresh_reader=True)
                if enabled:
                    credit_source("EST")
                attribution = ackredit.get_attribution().to_dict()
            records.append(
                dict(
                    tracking_enabled=enabled,
                    result=result,
                    attribution=attribution,
                    expectations_passed=check_case(result),
                )
            )
    after = {name: _source_record(module) for name, module in packages.items()}

    # Encoded artifacts contain attribution: compare decoded science instead.
    def science(record):
        return scientific_projection(
            {
                key: value
                for key, value in record["result"].items()
                if key not in {"artifacts", "fresh_reader"}
            },
            attribution_keys=("attribution", "source_attribution"),
        )

    extensions = {
        name: dict(
            path=module.__file__,
            sha256=hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest(),
        )
        for name, module in list(sys.modules.items())
        if name.startswith("molsysmt")
        and getattr(module, "__file__", None)
        and Path(module.__file__).suffix in {".so", ".pyd", ".dylib"}
    }

    def git(*arguments):
        return subprocess.check_output(["git", *arguments], cwd=ROOT, text=True).strip()

    report = dict(
        schema=(
            "pharmacophoremt.prepared_search_workflow@1"
            if args.case == "search"
            else "pharmacophoremt.prepared_workflow@1"
        ),
        recorded_at_utc=datetime.now(timezone.utc).isoformat(),
        scope="public CCD ideal prepared workflow controls; no biological/activity/performance claim",
        source_head=git("rev-parse", "HEAD"),
        source_working_state=git("status", "--porcelain"),
        environment=dict(
            python=sys.version,
            executable=sys.executable,
            platform=platform.platform(),
            packages_before=before,
            packages_after=after,
            molecular_extensions=extensions,
        ),
        input_sha256=inputs_before,
        input_hashes_unchanged=inputs_before == identities(),
        source_hashes_unchanged=before == after,
        scientific_outputs_stable=science(records[0]) == science(records[1]),
        records=records,
    )
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    passed = all(record["expectations_passed"] for record in records) and all(
        report[key]
        for key in (
            "input_hashes_unchanged",
            "source_hashes_unchanged",
            "scientific_outputs_stable",
        )
    )
    print("prepared workflow: " + ("PASS" if passed else "FAIL"), file=sys.stderr)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
