"""Opt-in #64 training stage; never acquire or score evaluation compounds.

Run by file path against the recorded installed providers. Reuse the original
case's HTTP/identity/serialization and MolSysMT preservation orchestration.
Model choice is this study's predeclared pharmacophore decision, not chemistry.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import importlib.util
import json
import platform
import subprocess
import sys
import time
import traceback
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DECLARATION = ROOT / "tests/data/esr1_consensus_comparison/declaration.json"
DECLARATION_SHA256 = "a1a476e7e94fd3480ee3845fbc5cca138221c4052eb7165a254499fd526ff647"
spec = importlib.util.spec_from_file_location(
    "esr1_training_pilot_support", Path(__file__).with_name("esr1_activity_pilot.py")
)
pilot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pilot)


def declaration(path=DECLARATION):
    if pilot.digest(path.read_bytes()) != DECLARATION_SHA256:
        raise ValueError("training requires the original committed #64 declaration")
    return json.loads(path.read_text())


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.strip()


def acquire_training(directory, declaration_path=DECLARATION):
    """Acquire exactly the three declared training responses, without retries."""
    protocol = declaration(declaration_path)
    entries = [e for e in protocol["cohort"] if e["role"] == "training"]
    directory.mkdir(parents=True, exist_ok=False)
    records = []
    for entry in entries:
        record = dict(entry)
        path = directory / f"CID{entry['cid']}.sdf"
        try:
            pilot.fetch(entry["url"], path)
        except urllib.error.HTTPError as error:
            response = directory / f"CID{entry['cid']}.http-error.txt"
            with error:
                response.write_bytes(error.read())
            record["acquisition"] = dict(
                status="failed",
                http_status=error.code,
                response=pilot.identity(response),
            )
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            record["acquisition"] = dict(
                status="failed", error_type=type(error).__name__, message=str(error)
            )
        else:
            record["acquisition"] = dict(status="completed", **pilot.identity(path))
        records.append(record)
        print(
            f"acquired training CID {entry['cid']}: {record['acquisition']['status']}",
            flush=True,
        )
        time.sleep(0.25)
    receipt = dict(
        schema="pharmacophoremt.esr1_consensus_training_acquisition@1",
        issue=64,
        acquired_at=datetime.now(timezone.utc).isoformat(),
        declaration=pilot.identity(declaration_path),
        producer=dict(
            git_head=git("rev-parse", "HEAD"),
            dirty=git("status", "--porcelain"),
            driver=pilot.identity(Path(__file__)),
        ),
        records=records,
        evaluation_acquired=False,
        scope="unchanged PubChem computed 3D training responses; no replacement or molecular interpretation",
    )
    pilot.dump(directory / "acquisition.json", receipt)
    return receipt


def validate_acquisition(directory, protocol):
    receipt = json.loads((directory / "acquisition.json").read_text())
    expected = [e for e in protocol["cohort"] if e["role"] == "training"]
    if (
        receipt.get("schema") != "pharmacophoremt.esr1_consensus_training_acquisition@1"
        or receipt["declaration"]["sha256"] != DECLARATION_SHA256
        or receipt.get("evaluation_acquired") is not False
        or len(receipt["records"]) != len(expected)
    ):
        raise ValueError("invalid frozen training acquisition")
    for record, entry in zip(receipt["records"], expected, strict=True):
        if any(record[key] != value for key, value in entry.items()):
            raise ValueError("training acquisition substituted a declared input")
        acquired = record["acquisition"]
        identity = (
            acquired if acquired["status"] == "completed" else acquired.get("response")
        )
        if identity is not None:
            name = identity["file"]
            expected_name = f"CID{entry['cid']}." + (
                "sdf" if acquired["status"] == "completed" else "http-error.txt"
            )
            if name != expected_name or pilot.identity(directory / name) != {
                k: identity[k] for k in ("file", "sha256", "byte_count")
            }:
                raise ValueError("training response identity changed")
    return receipt


def choose_model(models):
    """Apply only the fixed training-only site/support/identifier ordering."""
    if not models:
        raise ValueError("completed consensus has no model; evaluation stays unopened")
    ranking = sorted(
        range(len(models)),
        key=lambda i: (
            -models[i].n_interaction_sites,
            -models[i].metadata["hypothesis"]["joint_support_count"],
            models[i].metadata["layout"]["layout_id"],
            models[i].metadata["hypothesis"]["hypothesis_id"],
        ),
    )
    return ranking[0], ranking


def producer(phmt, msm):
    packages = (
        "pharmacophoremt",
        "molsysmt",
        "numpy",
        "scipy",
        "rdkit",
        "pandas",
        "pyunitwizard",
        "argdigest",
        "smonitor",
        "depdigest",
        "ackredit",
    )
    return dict(
        python=sys.version,
        executable=sys.executable,
        platform=platform.platform(),
        git_head=git("rev-parse", "HEAD"),
        dirty=git("status", "--porcelain"),
        driver=pilot.identity(Path(__file__)),
        preparation_support=pilot.identity(Path(pilot.__file__)),
        versions={p: importlib.metadata.version(p) for p in packages},
        runtime_origins=dict(pharmacophoremt=phmt.__file__, molsysmt=msm.__file__),
        runtime_files={
            name: {
                str(path.relative_to(Path(module.__file__).parent)): pilot.digest(
                    path.read_bytes()
                )
                for path in sorted(Path(module.__file__).parent.rglob("*"))
                if path.is_file() and path.suffix in {".py", ".so", ".pyd"}
            }
            for name, module in (("pharmacophoremt", phmt), ("molsysmt", msm))
        },
        conda_records=[
            {
                key: record.get(key)
                for key in (
                    "name",
                    "version",
                    "build",
                    "subdir",
                    "sha256",
                    "md5",
                    "url",
                )
            }
            for path in sorted((Path(sys.prefix) / "conda-meta").glob("*.json"))
            for record in [json.loads(path.read_text())]
        ],
    )


def execute(directory, output, declaration_path=DECLARATION):
    """Prepare training inputs and freeze the selected query or honest stop."""
    protocol = declaration(declaration_path)
    acquisition = validate_acquisition(directory, protocol)
    query_path = output.with_suffix(".query.json")
    for path in (output, query_path):
        if path.exists():
            raise FileExistsError("retain the original training output/query")
    import ackredit
    import molsysmt as msm

    import pharmacophoremt as phmt
    from pharmacophoremt.io import to_json
    from pharmacophoremt.modeler import from_rigid_ligands
    from pharmacophoremt.screening import RigidPoseSearch, get_screening_score
    from pharmacophoremt.validation import summarize_rigid_consensus

    initial_producer = producer(phmt, msm)
    systems, records = {}, []
    outcome = dict(status="stopped", stage="preparation", evaluation_opened=False)
    consensus, selected, readiness = None, None, []
    with (
        ackredit.session("ERalpha #64 training"),
        ackredit.capture("training-only consensus", record_evidence=True) as captured,
        phmt.attribution(True),
    ):
        ackredit.register_item(
            id="phmt:dataset:aid743075",
            type="dataset",
            title="PubChem BioAssay 743075: ER-alpha signaling agonist assay",
            url=pilot.ASSAY_URL,
        )
        ackredit.track_item(
            "phmt:dataset:aid743075",
            roles=["input_data"],
            context={
                "scope": "three predeclared training actives; no evaluation scores"
            },
        )
        for entry in acquisition["records"]:
            record = {
                key: entry[key]
                for key in ("cid", "sid", "label", "role", "acquisition")
            }
            try:
                if entry["acquisition"]["status"] != "completed":
                    raise ValueError(
                        "frozen training acquisition failed; no replacement"
                    )
                item_id = "phmt:dataset:pubchem-3d:" + entry["cid"]
                ackredit.register_item(
                    id=item_id,
                    type="dataset",
                    title="PubChem computed 3D CID " + entry["cid"],
                    url=entry["url"],
                )
                ackredit.track_item(
                    item_id,
                    roles=["input_data"],
                    context={
                        "sha256": entry["acquisition"]["sha256"],
                        "scope": "training read/preparation attempt",
                    },
                )
                prepared, _, observation = pilot._prepare_pilot_entry(
                    entry,
                    directory,
                    features=protocol["consensus"]["parameters"]["features"],
                )
            except Exception as error:
                record["preparation"] = dict(
                    status="failed",
                    error_type=type(error).__name__,
                    message=str(error),
                    traceback=traceback.format_exc(),
                )
            else:
                systems[entry["cid"]] = prepared
                record["preparation"] = observation
            records.append(record)
            print(
                f"prepared training CID {entry['cid']}: {record['preparation']['status']}",
                flush=True,
            )
        if len(systems) == 3:
            outcome["stage"] = "consensus"
            try:
                result = from_rigid_ligands(
                    [
                        dict(ligand_id=e["cid"], molecular_system=systems[e["cid"]])
                        for e in acquisition["records"]
                    ],
                    **protocol["consensus"]["parameters"],
                )
                if result["complete"] is not True:
                    raise ValueError("incomplete consensus; evaluation stays unopened")
                consensus = dict(
                    method=result["method"],
                    complete=result["complete"],
                    report=result["report"],
                    attribution=result.get("attribution"),
                    summary=summarize_rigid_consensus(result["report"]),
                )
                index, ranking = choose_model(result["models"])
                model = result["models"][index]
                selected = dict(
                    model_index=index,
                    training_only_ranking=ranking,
                    n_models=len(result["models"]),
                    n_sites=model.n_interaction_sites,
                    metadata=model.metadata,
                )
                output.parent.mkdir(parents=True, exist_ok=True)
                to_json(model, str(query_path))
                selected["saved_query"] = pilot.identity(query_path)
                outcome["stage"] = "training_readiness"
                search = RigidPoseSearch(
                    model,
                    **{
                        key: protocol["screening"][key]
                        for key in (
                            "search_method",
                            "max_trials",
                            "point_tolerance",
                            "direction_tolerance",
                            "min_fit_value",
                        )
                    },
                )
                for entry in acquisition["records"]:
                    evaluation = search.evaluate(systems[entry["cid"]])
                    readiness.append(
                        dict(
                            cid=entry["cid"],
                            evaluation=evaluation,
                            ranking_score=get_screening_score(
                                evaluation, score_method="seeded_hit"
                            ),
                        )
                    )
                if not any(r["ranking_score"] == 1 for r in readiness):
                    raise ValueError(
                        "selected query has no native training hit; no alternate model"
                    )
            except Exception as error:
                outcome.update(
                    error_type=type(error).__name__,
                    message=str(error),
                    traceback=traceback.format_exc(),
                )
            else:
                outcome.update(status="ready", stage="training_complete")
        else:
            outcome["message"] = (
                "not all three training inputs prepared; no consensus or evaluation"
            )
    final_producer = producer(phmt, msm)
    stable = initial_producer == final_producer
    if not stable:
        outcome.update(
            status="stopped",
            stage="producer_changed",
            message="source/runtime changed during training; not qualified",
        )
    run = dict(
        schema="pharmacophoremt.esr1_consensus_training_run@1",
        issue=64,
        measured_at=datetime.now(timezone.utc).isoformat(),
        producer=initial_producer,
        producer_stable=stable,
        producer_after=final_producer if not stable else None,
        declaration=pilot.identity(declaration_path),
        acquisition=pilot.identity(directory / "acquisition.json"),
        records=records,
        consensus=consensus,
        selected=selected,
        training_readiness=readiness,
        outcome=outcome,
        attribution=captured.attribution.to_dict(),
        scope="training-only molecular preparation/consensus/readiness; no evaluation acquisition or scores, no biological validation",
    )
    pilot.dump(output, pilot.portable(run))
    print(json.dumps(outcome), flush=True)
    return run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--declaration", type=Path, default=DECLARATION)
    parser.add_argument("--acquire", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.acquire:
        acquire_training(args.data_dir, args.declaration)
    if args.output:
        execute(args.data_dir, args.output, args.declaration)


if __name__ == "__main__":
    main()
