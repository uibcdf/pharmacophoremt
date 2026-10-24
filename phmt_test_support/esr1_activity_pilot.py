"""Opt-in ERα assay pilot; molecular work is delegated to public MolSysMT.

Run this file by path to use an installed PharmacophoreMT, without putting the
checkout's runtime package ahead of that installation. Acquisition uses only
HTTP/archive/CSV operations; it never parses or constructs a molecule.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import io
import json
import math
import platform
import subprocess
import sys
import tarfile
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tests/data/esr1_activity_pilot/manifest.json"
BATH_URL = "https://researchdata.bath.ac.uk/1496/6/ESR1ago.tar.gz"
BATH_SHA256 = "cb4bf0bf156e62944a0d0c7aefa02d0b589d1cc4d80dcdc1858b31f654889900"
ASSAY_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/743075/concise/CSV"
DESCRIPTION_URL = (
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/743075/description/JSON"
)
PREFIX = "phmt-esr1ago-pilot-v1:"
METHOD = dict(
    features=["hb donor", "hb acceptor", "aromatic ring"],
    radius="0.15 nm",
    max_trials=10000,
    point_tolerance="0.10 nm",
    direction_tolerance="30 degrees",
    min_fit_value=0.0,
    ef_fractions=[0.1],
    bedroc_alpha=20.0,
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def identity(path):
    raw = path.read_bytes()
    return dict(file=path.name, sha256=digest(raw), byte_count=len(raw))


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def validate_replay_declaration(manifest_path, declaration_path, reference_query):
    """Check the declared replay against original archived byte identities."""
    declaration = json.loads(declaration_path.read_text())
    original = json.loads(
        (
            ROOT / "devguide/evidence/esr1_activity_pilot_20261023_summary.json"
        ).read_text()
    )
    if (
        declaration.get("schema")
        != "pharmacophoremt.esr1_seeded_hit_replay_declaration@1"
        or declaration.get("method")
        != dict(METHOD, search_method="seeded_hit", score_method="seeded_hit@1")
        or declaration.get("original_report_sha256")
        != original["full_evidence"]["uncompressed_sha256"]
        or declaration.get("input_manifest_sha256") != original["manifest"]["sha256"]
        or digest(manifest_path.read_bytes())
        != declaration.get("input_manifest_sha256")
        or declaration.get("frozen_query_sha256")
        != original["saved_query_archive"]["uncompressed_sha256"]
        or reference_query is None
        or digest(reference_query.read_bytes())
        != declaration.get("frozen_query_sha256")
    ):
        raise ValueError(
            "seeded replay requires its frozen declaration, original inputs and original query bytes"
        )
    return declaration


def frozen_cohort(rows):
    """Case-specific ID sampling; no chemistry/series inference or score access."""
    groups = {"Active": {}, "Inactive": {}}
    for row in rows:
        label, cid = row["PUBCHEM_ACTIVITY_OUTCOME"], row["PUBCHEM_CID"]
        if label in groups:
            groups[label].setdefault(cid, row)
    # Different assayed substances can map to one compound with opposite
    # outcomes. Exclude every such CID, rather than resolve biology by row order.
    ambiguous = groups["Active"].keys() & groups["Inactive"].keys()
    for cid in ambiguous:
        for values in groups.values():
            del values[cid]
    ordered = {
        label: sorted(values, key=lambda cid: digest((PREFIX + cid).encode()))
        for label, values in groups.items()
    }
    if len(ordered["Active"]) != 8 or len(ordered["Inactive"]) < 24:
        raise ValueError("review changed source population before selecting a cohort")
    cohort = []
    for label, cids in ordered.items():
        for index, cid in enumerate(cids if label == "Active" else cids[:24]):
            row = groups[label][cid]
            cohort.append(
                dict(
                    cid=cid,
                    sid=row["PUBCHEM_SID"],
                    label=int(label == "Active"),
                    role="reference"
                    if label == "Active" and index == 0
                    else "held_out",
                    selection_hash=digest((PREFIX + cid).encode()),
                )
            )
    return cohort


def fetch(url, path):
    if not path.exists():
        request = urllib.request.Request(
            url, headers={"User-Agent": "PharmacophoreMT-activity-pilot/1"}
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            path.write_bytes(response.read())
    return path.read_bytes()


def acquire(directory, manifest_path):
    """Freeze this declared case once; changed inputs require a new manifest."""
    if manifest_path.exists():
        raise FileExistsError(
            "preserve the frozen manifest; use a distinct path for a new acquisition"
        )
    directory.mkdir(parents=True, exist_ok=True)
    bath_path = directory / "ESR1ago.tar.gz"
    bath = fetch(BATH_URL, bath_path)
    if digest(bath) != BATH_SHA256:
        raise ValueError("Bath source changed")
    with tarfile.open(fileobj=io.BytesIO(bath)) as archive:
        with archive.extractfile("ESR1ago/ESR1ago_data_full.csv") as stream:
            rows = list(csv.DictReader(io.TextIOWrapper(stream)))
    cohort = frozen_cohort(rows)  # fixed before any structure or score is inspected
    assay_path = directory / "aid743075_concise.csv"
    assay = list(csv.DictReader(io.StringIO(fetch(ASSAY_URL, assay_path).decode())))
    description_path = directory / "aid743075_description.json"
    fetch(DESCRIPTION_URL, description_path)
    for entry in cohort:
        expected = "Active" if entry["label"] else "Inactive"
        matching = [r for r in assay if r["SID"] == entry["sid"]]
        if not matching or any(
            r["CID"] != entry["cid"] or r["Activity Outcome"] != expected
            for r in matching
        ):
            raise ValueError(f"original assay disagrees for SID {entry['sid']}")
        entry["assay_outcome"] = expected
        entry["url"] = (
            f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{entry['cid']}/SDF?record_type=3d"
        )
        path = directory / f"CID{entry['cid']}.sdf"
        try:
            fetch(entry["url"], path)
        except urllib.error.HTTPError as error:
            error_path = directory / f"CID{entry['cid']}.http-error.txt"
            error_path.write_bytes(error.read())
            entry["acquisition"] = dict(
                status="failed", http_status=error.code, response=identity(error_path)
            )
        else:
            entry["acquisition"] = dict(status="completed", **identity(path))
        time.sleep(0.25)  # PubChem <= 5 requests/s; no retries or replacement ligands
    manifest = dict(
        schema="pharmacophoremt.esr1_activity_pilot_inputs@1",
        issue=62,
        acquired_at=datetime.now(timezone.utc).isoformat(),
        source=dict(
            url=BATH_URL,
            doi="10.15125/BATH-01496",
            license="CC-BY-SA-4.0",
            license_url="https://researchdata.bath.ac.uk/1496/",
            **identity(bath_path),
        ),
        source_population=dict(
            rows=len(rows),
            outcomes=dict(Counter(r["PUBCHEM_ACTIVITY_OUTCOME"] for r in rows)),
        ),
        assay=dict(aid=743075, url=ASSAY_URL, **identity(assay_path)),
        assay_description=dict(url=DESCRIPTION_URL, **identity(description_path)),
        selection=dict(
            hash_prefix=PREFIX,
            rule="exclude every CID with contradictory source outcomes; unique CID; hash-order first active reference, remaining 7 actives and first 24 inactives held out; no replacement",
            ambiguous_source_rows=[
                {
                    k: r[k]
                    for k in ("PUBCHEM_CID", "PUBCHEM_SID", "PUBCHEM_ACTIVITY_OUTCOME")
                }
                for r in rows
                if r["PUBCHEM_CID"] in {"17113", "6128", "5361202", "2662"}
            ],
        ),
        structure_policy="one published PubChem computed 3D conformer; supplied state; no generation, pH adjustment or receptor placement",
        redistribution="URLs, hashes and attributed selected labels only; source archive and SDF files are not redistributed",
        method=METHOD,
        cohort=cohort,
    )
    dump(manifest_path, manifest)
    return manifest


def restore(directory, manifest):
    """Reacquire declared bytes with integrity checks, never silently refresh."""
    directory.mkdir(parents=True, exist_ok=True)
    for record in [
        manifest["source"],
        manifest["assay"],
        manifest["assay_description"],
    ]:
        raw = fetch(record["url"], directory / record["file"])
        if digest(raw) != record["sha256"]:
            raise ValueError(f"source identity changed: {record['file']}")
    for entry in manifest["cohort"]:
        record = entry["acquisition"]
        if record["status"] == "completed":
            raw = fetch(entry["url"], directory / record["file"])
            if digest(raw) != record["sha256"]:
                raise ValueError(
                    f"3D record changed for CID {entry['cid']}; do not substitute"
                )
            time.sleep(0.25)


def portable(value):
    import pyunitwizard as puw

    if not isinstance(value, str) and puw.is_quantity(value):
        return puw.QuantityRecord.from_quantity(value).to_dict(encoding="json")
    if isinstance(value, dict):
        return {str(k): portable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [portable(v) for v in value]
    if hasattr(value, "tolist"):
        return portable(value.tolist())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def execute(
    directory, manifest_path, output, *, declaration_path=None, reference_query=None
):
    import ackredit
    import molsysmt as msm
    import numpy as np

    import pharmacophoremt as phmt
    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.io import load_json, to_json
    from pharmacophoremt.modeler import from_feature_inventory, get_features
    from pharmacophoremt.screening import RigidPoseSearch
    from pharmacophoremt.validation.retrospective import RetrospectiveValidator

    if output.exists():
        raise FileExistsError("retain the original run; choose a new output path")
    manifest = json.loads(manifest_path.read_text())
    if manifest["method"] != METHOD:
        raise ValueError("this driver only implements the declared v1 method")
    method = METHOD
    declaration = None
    if declaration_path is not None:
        declaration = validate_replay_declaration(
            manifest_path, declaration_path, reference_query
        )
        method = dict(METHOD, search_method="seeded_hit", score_method="seeded_hit@1")
    elif reference_query is not None:
        raise ValueError("a replay query requires an explicit declaration")
    systems, records = {}, []

    def state(system):
        return portable(
            msm.convert(
                system.chemical_states, to_form="molsysmt.ChemicalStatesDict"
            ).to_dict()
        )

    def prepare(entry):
        path = directory / entry["acquisition"]["file"]
        raw = path.read_bytes()
        if digest(raw) != entry["acquisition"]["sha256"]:
            raise ValueError("3D input hash mismatch")
        source = msm.convert(
            str(path),
            to_form="molsysmt.MolSys",
            discard_properties=True,
            stereo_engine="rdkit",
        )
        before = state(source)
        coordinates = puw.get_value(
            msm.get(source, coordinates=True), to_unit="nm"
        ).copy()
        prepared = msm.convert(
            msm.convert(source, to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
        )
        inventory = get_features(prepared, features=METHOD["features"])
        rmsd = puw.get_value(
            msm.structure.get_rmsd(
                prepared,
                reference_molecular_system=source,
                use_gpu=False,
                parallel=False,
            ),
            to_unit="nm",
        )
        after = state(prepared)
        checks = dict(
            source_bytes_unchanged=raw == path.read_bytes(),
            source_state_unchanged=before == state(source),
            source_coordinates_unchanged=bool(
                np.array_equal(
                    coordinates,
                    puw.get_value(msm.get(source, coordinates=True), to_unit="nm"),
                )
            ),
            atom_ids_preserved=list(msm.get(source, element="atom", atom_id=True))
            == list(msm.get(prepared, element="atom", atom_id=True)),
            elements_preserved=list(msm.get(source, element="atom", atom_type=True))
            == list(msm.get(prepared, element="atom", atom_type=True)),
            coordinates_preserved=bool(np.all(np.asarray(rmsd) < 1e-12)),
        )
        for key in ("formal_charge", "n_unpaired_electrons", "stereochemistry"):
            checks[key + "_preserved"] = (
                before["states"][0]["atom_attributes"]["columns"][key]["values"]
                == after["states"][0]["atom_attributes"]["columns"][key]["values"]
            )
        if not all(checks.values()):
            raise ValueError(f"molecular identity/immutability check failed: {checks}")
        return (
            prepared,
            inventory,
            dict(
                status="completed",
                checks=checks,
                source_state=before,
                prepared_state=after,
                counts=msm.get(
                    prepared,
                    n_atoms=True,
                    n_bonds=True,
                    n_structures=True,
                    output_type="dictionary",
                ),
                feature_counts=dict(Counter(f["kind"] for f in inventory["features"])),
                coordinate_rmsd_nm=float(np.asarray(rmsd).reshape(-1)[0]),
                inventory=inventory,
            ),
        )

    with (
        ackredit.session("ERalpha frozen activity pilot"),
        ackredit.capture("ERalpha pilot", record_evidence=True) as captured,
        phmt.attribution(True),
    ):
        ackredit.register_item(
            id="phmt:dataset:bath-01496",
            type="dataset",
            title='Dataset for "Optimising Drug Activity Using Docking-Informed Machine Learning"',
            doi="10.15125/BATH-01496",
            authors=["Proudfoot, James", "Lewis-Atwell, Toby", "Grayson, Matt"],
            year=2026,
            url="https://researchdata.bath.ac.uk/1496/",
        )
        ackredit.track_item("phmt:dataset:bath-01496", roles=["input_data"])
        ackredit.register_item(
            id="phmt:dataset:aid743075",
            type="dataset",
            title="PubChem BioAssay 743075: ER-alpha signaling agonist assay",
            url=ASSAY_URL,
        )
        ackredit.track_item(
            "phmt:dataset:aid743075",
            roles=["input_data"],
            context={
                "endpoint": "experimental substance Activity Outcome; not binding affinity"
            },
        )
        for entry in manifest["cohort"]:
            record = dict(
                cid=entry["cid"],
                sid=entry["sid"],
                label=entry["label"],
                role=entry["role"],
            )
            try:
                if entry["acquisition"]["status"] != "completed":
                    raise ValueError("frozen acquisition failed; no replacement")
                prepared, inventory, observation = prepare(entry)
            except Exception as error:
                record["preparation"] = dict(
                    status="failed", error_type=type(error).__name__, message=str(error)
                )
            else:
                systems[entry["cid"]] = prepared
                record["preparation"] = observation
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
                    context={"sha256": entry["acquisition"]["sha256"]},
                )
            records.append(record)
            print(
                f"prepared CID {entry['cid']}: {record['preparation']['status']}",
                flush=True,
            )
        journal_path = output.with_suffix(".preparation.json")
        if journal_path.exists():
            raise FileExistsError("preserve original preparation journal")
        dump(
            journal_path,
            portable(dict(manifest=identity(manifest_path), records=records)),
        )
        reference = next(r for r in records if r["role"] == "reference")
        if reference["preparation"]["status"] != "completed":
            raise ValueError(
                "predeclared reference failed; no alternate reference permitted"
            )
        if declaration is None:
            query = from_feature_inventory(
                reference["preparation"]["inventory"],
                radius=METHOD["radius"],
                name="Frozen ESR1ago CID " + reference["cid"],
            )
        else:
            query = load_json(str(reference_query))
        query_path = output.with_suffix(".query.json")
        if query_path.exists():
            raise FileExistsError("preserve saved query")
        output.parent.mkdir(parents=True, exist_ok=True)
        if declaration is None:
            to_json(query, str(query_path))
        else:
            query_path.write_bytes(reference_query.read_bytes())
        search = RigidPoseSearch(
            query,
            **{
                k: METHOD[k]
                for k in (
                    "max_trials",
                    "point_tolerance",
                    "direction_tolerance",
                    "min_fit_value",
                )
            },
            **({"search_method": "seeded_hit"} if declaration is not None else {}),
        )
        self_result = search.evaluate(systems[reference["cid"]])
        held_out = [r for r in records if r["role"] == "held_out"]

        # Passing an unavailable frozen file to the native batch is an explicit
        # failed evaluation; no missing ligand receives a score or negative label.
        def inputs(label):
            return [
                systems.get(
                    r["cid"], str(directory / ("UNAVAILABLE-CID" + r["cid"] + ".sdf"))
                )
                for r in held_out
                if r["label"] == label
            ]

        report = RetrospectiveValidator(query, evaluator=search).run(
            inputs(1),
            inputs(0),
            on_error="record",
            ef_fractions=METHOD["ef_fractions"],
            bedroc_alpha=METHOD["bedroc_alpha"],
        )
        for record, evaluation in zip(held_out, report["evaluations"], strict=True):
            record["evaluation"] = evaluation

    credits = captured.attribution.to_dict()

    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=ROOT, text=True, capture_output=True, check=True
        ).stdout.strip()

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
    runtime_files = {
        name: {
            str(path.relative_to(Path(module.__file__).parent)): digest(
                path.read_bytes()
            )
            for path in sorted(Path(module.__file__).parent.rglob("*"))
            if path.is_file() and path.suffix in {".py", ".so", ".pyd"}
        }
        for name, module in (("pharmacophoremt", phmt), ("molsysmt", msm))
    }
    conda_records = [
        {
            key: record.get(key)
            for key in ("name", "version", "build", "subdir", "sha256", "md5", "url")
        }
        for path in sorted((Path(sys.prefix) / "conda-meta").glob("*.json"))
        for record in [json.loads(path.read_text())]
    ]
    result = dict(
        schema="pharmacophoremt.esr1_seeded_hit_replay_run@1"
        if declaration is not None
        else "pharmacophoremt.esr1_activity_pilot_run@1",
        issue=62,
        measured_at=datetime.now(timezone.utc).isoformat(),
        producer=dict(
            python=sys.version,
            executable=sys.executable,
            platform=platform.platform(),
            git_head=git("rev-parse", "HEAD"),
            dirty=git("status", "--porcelain"),
            driver=identity(Path(__file__)),
            versions={p: importlib.metadata.version(p) for p in packages},
            runtime_origins=dict(pharmacophoremt=phmt.__file__, molsysmt=msm.__file__),
            runtime_files=runtime_files,
            conda_records=conda_records,
        ),
        manifest=identity(manifest_path),
        method=method,
        replay_declaration=identity(declaration_path)
        if declaration is not None
        else None,
        saved_query=identity(query_path),
        preparation_journal=identity(journal_path),
        reference_self_evaluation=self_result,
        records=records,
        retrospective=report,
        data_attribution=credits,
        scope=declaration["claim"]
        if declaration is not None
        else "exploratory held-out assay outcomes; one supplied 3D conformer; CID-disjoint, series overlap unqualified; evaluated-subset metrics; no affinity or full-benchmark claim",
    )
    dump(output, portable(result))
    print(
        json.dumps(
            portable(
                {
                    k: v
                    for k, v in report.items()
                    if k not in {"evaluations", "failures", "attribution"}
                }
            )
        ),
        flush=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--acquire", action="store_true")
    parser.add_argument("--restore", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--replay-declaration", type=Path)
    parser.add_argument("--reference-query", type=Path)
    args = parser.parse_args()
    if args.acquire:
        acquire(args.data_dir, args.manifest)
    if args.restore:
        restore(args.data_dir, json.loads(args.manifest.read_text()))
    if args.output:
        execute(
            args.data_dir,
            args.manifest,
            args.output,
            declaration_path=args.replay_declaration,
            reference_query=args.reference_query,
        )


if __name__ == "__main__":
    main()
