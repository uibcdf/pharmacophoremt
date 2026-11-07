"""Offline fixed-three-record PubChem3D receiving experiment for PHMT #108.

This unshipped client performs no acquisition and implements no molecular parser.
The caller supplies original single-record SDF files under a frozen plan. All
molecular interpretation uses public MolSysMT operations. Original and derived
molecular payloads stay local pending publication-rights review.
"""

import argparse
import hashlib
import json
import math
import re
from dataclasses import asdict, is_dataclass
from pathlib import Path

CIDS = (1983, 2244, 2519)
EXPECTED_COUNTS = {1983: (20, 9), 2244: (21, 8), 2519: (24, 10)}
MAX_INPUT_BYTES = 2 * 1024 * 1024
ALLOWED_IMPORT_LOSSES = {"sdf_properties", "sdf_bond_display"}
RECIPE = {
    "schema": "pharmacophoremt.pubchem3d-fixed-pilot-recipe@1",
    "cids": list(CIDS),
    "import": {"discard_properties": True, "stereo_engine": "rdkit"},
    "preparation": "public aromaticity perception and explicit source-indexed annotation only",
    "new_hydrogens_states_conformers": False,
    "snapshot_float_precision": "double",
    "snapshot_codec": "public H5MSM 0.5 fixed float64",
    "query": {"source_cid": 2519, "features": ["hb acceptor"], "radius": "0.15 nm"},
    "search": {"search_method": "seeded_hit", "max_trials": 10000},
    "translation_control": {"translation_nm": [1, 2, 3], "expected_seeded_score": 1},
}


def _object(pairs):
    output = {}
    for key, value in pairs:
        if key in output:
            raise ValueError("duplicate metadata key")
        output[key] = value
    return output


def _nonfinite(value):
    raise ValueError(f"nonfinite metadata value: {value}")


def _read_json(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        raise ValueError("pilot metadata exceeds the two-MiB bound")
    value = json.loads(raw, object_pairs_hook=_object, parse_constant=_nonfinite)
    if type(value) is not dict:
        raise ValueError("pilot metadata must be a JSON object")
    return raw, value


def _identity(path, *, limit=None):
    digest = hashlib.sha256()
    size = 0
    with Path(path).open("rb") as stream:
        while block := stream.read(64 * 1024):
            size += len(block)
            if limit is not None and size > limit:
                raise ValueError("source artifact exceeds the fixed pilot size bound")
            digest.update(block)
    return {"sha256": digest.hexdigest(), "bytes": size}


def _verify_file(record):
    actual = _identity(record["path"], limit=MAX_INPUT_BYTES)
    if actual != {key: record[key] for key in ("sha256", "bytes")}:
        raise ValueError("source artifact differs from the acquisition identity")
    return actual


def validate_acquisition(plan_path, acquisition_path):
    """Verify fixed metadata and hashes before scientific imports or SDF reads.

    All three records must be received, ordered and valid as acquisition metadata
    before opening an SDF. Source bytes are hashed, not interpreted or rewritten.
    Relative source paths resolve against the acquisition-manifest directory.
    """
    plan_raw, plan = _read_json(plan_path)
    acquisition_raw, acquisition = _read_json(acquisition_path)
    plan_sha = hashlib.sha256(plan_raw).hexdigest()
    if acquisition.get("plan_sha256") != plan_sha:
        raise ValueError("acquisition does not bind the supplied frozen plan")
    if plan.get("cids") != list(CIDS) or any(
        type(cid) is not int for cid in plan["cids"]
    ):
        raise ValueError("the pilot requires the fixed CID order 1983, 2244, 2519")
    if "molecules" in plan:
        molecules = plan["molecules"]
        if (
            type(molecules) is not list
            or len(molecules) != 3
            or any(type(row) is not dict for row in molecules)
            or [row.get("cid") for row in molecules] != list(CIDS)
        ):
            raise ValueError("the molecule table differs from the fixed selection")
        for row in molecules:
            counts = (row.get("n_atoms"), row.get("n_hydrogens"))
            if counts != EXPECTED_COUNTS[row["cid"]] or any(
                type(n) is not int for n in counts
            ):
                raise ValueError(
                    "planned atom/H counts differ from the fixed formula oracle"
                )
    records = acquisition.get("records")
    if type(records) is not list or len(records) != len(CIDS):
        raise ValueError("all three acquisition records are required")
    for expected, record in zip(CIDS, records, strict=True):
        if (
            type(record) is not dict
            or type(record.get("cid")) is not int
            or record["cid"] != expected
        ):
            raise ValueError("acquisition records changed CID order or selection")
        if record.get("status") != "received":
            raise ValueError(
                "every declared record must be received before preparation"
            )
    qualified = []
    for record in records:
        conformer, source = record.get("conformer_id"), record.get("sdf")
        if (
            type(conformer) is not str
            or re.fullmatch(r"[0-9A-Fa-f]{16}", conformer) is None
        ):
            raise ValueError("a concrete 16-hex-digit PubChem conformer ID is required")
        if type(source) is not dict or not {"path", "sha256", "bytes"} <= source.keys():
            raise ValueError("received SDF metadata requires path, sha256 and bytes")
        if type(source["path"]) is not str or not source["path"].strip():
            raise ValueError("received SDF requires a nonempty file path")
        if (
            type(source["sha256"]) is not str
            or re.fullmatch(r"[0-9a-f]{64}", source["sha256"]) is None
        ):
            raise ValueError("received SDF requires a lowercase SHA-256 digest")
        if (
            type(source["bytes"]) is not int
            or not 0 < source["bytes"] <= MAX_INPUT_BYTES
        ):
            raise ValueError("received SDF byte count is outside the pilot bound")
        path = Path(source["path"])
        if not path.is_absolute():
            path = Path(acquisition_path).resolve().parent / path
        qualified.append({**record, "sdf": {**source, "path": str(path.resolve())}})
    for record in qualified:
        _verify_file(record["sdf"])
    return {
        "plan": plan,
        "plan_sha256": plan_sha,
        "records": qualified,
        "acquisition_sha256": hashlib.sha256(acquisition_raw).hexdigest(),
    }


def _plain(value):
    """Detach reports; nullable/nonfinite scalar observations become JSON null."""
    import numpy as np
    import pandas as pd

    from pharmacophoremt._private.molsysmt import detached

    if is_dataclass(value):
        return _plain(asdict(value))
    if value is pd.NA or value is pd.NaT:
        return None
    if isinstance(value, dict):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_plain(item) for item in value]
    if isinstance(value, np.ndarray):
        return _plain(value.tolist())
    if isinstance(value, np.generic):
        return _plain(value.item())
    if type(value) is float and not math.isfinite(value):
        return None
    output = detached(value)
    if output is not value and isinstance(output, (dict, list, tuple)):
        return _plain(output)
    return output


def _write(path, value):
    text = json.dumps(_plain(value), indent=2, allow_nan=False) + "\n"
    with Path(path).open("w", encoding="utf-8") as stream:
        stream.write(text)


def _inventory(system):
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    atoms = msm.get(
        system,
        element="atom",
        chemical_state=0,
        atom_id=True,
        atom_type=True,
        isotope=True,
        formal_charge=True,
        atom_is_aromatic=True,
        n_implicit_hydrogens=True,
        n_explicit_hydrogens=True,
        allows_implicit_hydrogens=True,
        output_type="dictionary",
    )
    bonds = msm.get(
        system,
        element="bond",
        chemical_state=0,
        bond_id=True,
        bonded_atom_pairs=True,
        bond_type=True,
        bond_order=True,
        bond_is_aromatic=True,
        output_type="dictionary",
    )
    n_atoms = int(msm.get(system, n_atoms=True))
    n_structures = int(msm.get(system, n_structures=True))
    coordinates = np.asarray(
        puw.get_value(msm.get(system, coordinates=True), to_unit="nm")
    )
    if (
        coordinates.shape != (n_structures, n_atoms, 3)
        or not np.isfinite(coordinates).all()
    ):
        raise ValueError(
            "received coordinates require a finite aligned structure/atom axis"
        )
    return {
        "atoms": _plain(atoms),
        "bonds": _plain(bonds),
        "coordinates_nm": coordinates.copy(),
        "n_atoms": n_atoms,
        "n_structures": n_structures,
        "n_chemical_states": int(msm.get(system, n_chemical_states=True)),
        "n_hydrogens": sum(str(element) == "H" for element in atoms["atom_type"]),
    }


def _same_inventory(first, second, *, aromaticity_may_change=False):
    import numpy as np

    for key in ("n_atoms", "n_structures", "n_chemical_states", "n_hydrogens"):
        if first[key] != second[key]:
            raise ValueError(f"prepared inventory changed {key}")
    for domain, aromatic in (
        ("atoms", "atom_is_aromatic"),
        ("bonds", "bond_is_aromatic"),
    ):
        left, right = dict(first[domain]), dict(second[domain])
        if aromaticity_may_change:
            left.pop(aromatic, None)
            right.pop(aromatic, None)
        if left != right:
            raise ValueError(f"prepared {domain} assignments or source mapping changed")
    if first["coordinates_nm"].shape != second[
        "coordinates_nm"
    ].shape or not np.allclose(
        first["coordinates_nm"], second["coordinates_nm"], rtol=0, atol=1e-12
    ):
        raise ValueError("prepared coordinates differ by more than 1e-12 nm")


def _prepare(record, output, event):
    import molsysmt as msm
    import numpy as np

    cid = record["cid"]
    directory = output / f"cid-{cid}"
    directory.mkdir()
    event("import", "started", cid=cid)
    _verify_file(record["sdf"])
    system, conversion = msm.convert(
        record["sdf"]["path"],
        to_form="molsysmt.MolSys",
        discard_properties=True,
        stereo_engine="rdkit",
        return_report=True,
    )
    _write(directory / "import-report.json", conversion)
    unexpected = {
        issue.attribute for issue in conversion.issues
    } - ALLOWED_IMPORT_LOSSES
    if conversion.outcome == "rejected" or unexpected:
        raise ValueError(f"import reports an undeclared loss: {sorted(unexpected)}")
    before = _inventory(system)
    if (before["n_atoms"], before["n_hydrogens"]) != EXPECTED_COUNTS[cid]:
        raise ValueError(
            "received atom/H counts disagree with the fixed formula oracle"
        )
    if before["n_structures"] != 1 or before["n_chemical_states"] != 1:
        raise ValueError("pilot import requires one structure and chemical state")
    report = {
        "cid": cid,
        "conformer_id": record["conformer_id"],
        "source": record["sdf"],
        "conversion": conversion,
        "before": before,
        "readiness_before": msm.physchem.get_chemical_readiness(system),
        "hydrogen_inventory_before": msm.physchem.get_hydrogen_inventory(system),
        "missing_scalar_json_encoding": "null; unknown observations remain unassessed",
        "publication": "local-only original/derived molecular details pending rights review",
    }
    _write(directory / "preparation.json", report)
    event("aromaticity_annotation", "started", cid=cid)
    aromatic = msm.physchem.get_aromaticity(system, chemical_state=0)
    if not np.array_equal(aromatic["atom_indices"], np.arange(before["n_atoms"])):
        raise ValueError("aromaticity output does not cover the ordered atom axis")
    if not np.array_equal(
        aromatic["bond_indices"], np.arange(len(before["bonds"]["bonded_atom_pairs"]))
    ):
        raise ValueError("aromaticity output does not cover the ordered bond axis")
    msm.set(
        system,
        element="atom",
        selection=aromatic["atom_indices"],
        chemical_state=0,
        atom_is_aromatic=aromatic["atom_is_aromatic"],
    )
    msm.set(
        system,
        element="bond",
        selection=aromatic["bond_indices"],
        chemical_state=0,
        bond_is_aromatic=aromatic["bond_is_aromatic"],
    )
    after = _inventory(system)
    _same_inventory(before, after, aromaticity_may_change=True)
    report.update(
        aromaticity=aromatic,
        after=after,
        readiness_after=msm.physchem.get_chemical_readiness(system),
        hydrogen_inventory_after=msm.physchem.get_hydrogen_inventory(system),
    )
    _write(directory / "preparation.json", report)
    event("snapshot", "started", cid=cid)
    snapshot = directory / "prepared.h5msm"
    # Public convert dispatches H5MSM 0.5 and rejects legacy precision kwargs.
    # The explicit 0.5 codec fixes coordinate storage/validation to float64;
    # its public reader plus the mapped nm comparison enforce this gate.
    msm.h5msm.write(system, str(snapshot))
    restored = msm.h5msm.read(str(snapshot))
    roundtrip = _inventory(restored)
    _same_inventory(after, roundtrip)
    _same_inventory(before, _inventory(system), aromaticity_may_change=True)
    _verify_file(record["sdf"])
    report.update(
        roundtrip=roundtrip, roundtrip_verified=True, source_bytes_unchanged=True
    )
    _write(directory / "preparation.json", report)
    snapshot_record = {
        "cid": cid,
        "conformer_id": record["conformer_id"],
        "path": str(snapshot.resolve()),
        **_identity(snapshot),
        "source_sdf": {key: record["sdf"][key] for key in ("sha256", "bytes")},
        "n_atoms": after["n_atoms"],
        "n_hydrogens": after["n_hydrogens"],
        "n_structures": 1,
        "n_chemical_states": 1,
        "preparation_report": {
            "path": str((directory / "preparation.json").resolve()),
            **_identity(directory / "preparation.json"),
        },
    }
    event(
        "preparation", "completed", cid=cid, snapshot_sha256=snapshot_record["sha256"]
    )
    return snapshot_record


def _mapping(record, ordinal):
    return {
        "work_key": f"pubchem:{record['cid']}:conformer:{record['conformer_id']}:structure:0",
        "source_key": f"PubChemCID:{record['cid']}",
        "occurrence_key": f"selected:{ordinal}",
    }


def _screen(snapshots, output, event):
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.io import to_json
    from pharmacophoremt.modeler import from_ligand
    from pharmacophoremt.screening import get_screening_score
    from phmt_test_support.prepared_library_recovery import (
        build_recovery_plan,
        resume_prepared,
    )
    from phmt_test_support.prepared_library_reference import (
        PreparedInput,
        screen_prepared,
    )
    from phmt_test_support.reference_run_store import ReferenceLedger

    def load_snapshot(record):
        if _identity(record["path"]) != {
            key: record[key] for key in ("sha256", "bytes")
        }:
            raise ValueError("prepared snapshot bytes changed before use")
        return msm.convert(record["path"], to_form="molsysmt.MolSys")

    def reader():
        for ordinal, record in enumerate(snapshots):
            yield PreparedInput(
                **_mapping(record, ordinal), molecular_system=load_snapshot(record)
            )

    if tuple(record["cid"] for record in snapshots) != CIDS:
        raise ValueError("screening requires all three prepared records in fixed order")
    for record in snapshots:
        if _identity(record["path"]) != {
            key: record[key] for key in ("sha256", "bytes")
        }:
            raise ValueError("a prepared snapshot changed before query creation")
    query_source = load_snapshot(snapshots[-1])
    source_coordinates = np.asarray(
        puw.get_value(msm.get(query_source, coordinates=True), to_unit="nm")
    ).copy()
    query = from_ligand(query_source, features=["hb acceptor"], radius="0.15 nm")
    query_path = output / "query.json"
    to_json(query, str(query_path))
    manifest = output / "work.jsonl"
    manifest.write_text(
        "".join(
            json.dumps(_mapping(record, ordinal)) + "\n"
            for ordinal, record in enumerate(snapshots)
        ),
        encoding="utf-8",
    )
    compatibility = {
        "prepared_snapshot": {
            "records": [
                {key: record[key] for key in ("cid", "conformer_id", "sha256", "bytes")}
                for record in snapshots
            ]
        },
        "preparation": {"recipe": RECIPE, "molsysmt_version": msm.__version__},
        "features": {
            "definition": "classical_atomic_formal@1",
            "selected": ["hb acceptor"],
        },
        "index": None,
        "grouping": "one-selected-conformer-per-received-CID@1",
        "numerical": {
            "coordinates": "native nanometers, double-precision H5MSM",
            "backend_threads": 1,
        },
    }
    plan = build_recovery_plan(
        query_path,
        screening_method="rigid",
        score_method="seeded_hit",
        compatibility=compatibility,
        constructor_options={"search_method": "seeded_hit", "max_trials": 10000},
        on_error="record",
    )
    ledger_path = output / "screening.sqlite3"
    event("screening", "started")
    with ReferenceLedger.create(
        ledger_path,
        run_id="pubchem3d-fixed-three-pilot@1",
        query_bytes=plan.query_bytes,
        context=plan.context,
        manifest_path=manifest,
    ) as ledger:
        outcomes = resume_prepared(ledger, reader(), plan=plan)
        first = next(outcomes)
        outcomes.close()
        if len(list(ledger.results())) != 1:
            raise ValueError("interruption did not preserve one confirmed outcome")
    event("screening", "interrupted_after_one_confirmed")
    with ReferenceLedger.open(
        ledger_path,
        query_bytes=plan.query_bytes,
        context=plan.context,
        manifest_path=manifest,
    ) as ledger:
        remaining = list(resume_prepared(ledger, reader(), plan=plan))
        saved = list(ledger.results())
        attempts = len(list(ledger.attempts(first["work_key"])))
        if len(saved) != 3 or len(remaining) != 2 or attempts != 1:
            raise ValueError("recovery skipped or repeated declared work")
    _write(output / "native-outcomes.json", saved)
    event("screening", "all_declared_work_confirmed", n_outcomes=3)
    execution = plan.context["execution"]
    composed = list(
        screen_prepared(
            reader(),
            plan.new_evaluator(),
            score_method=execution["score_method"],
            on_error=execution["on_error"],
            evaluation_options=execution["evaluation_options"],
        )
    )
    _write(output / "composed-outcomes.json", composed)
    if saved != composed:
        raise ValueError("recovered results differ from composed native evidence")
    for ordinal, (record, outcome) in enumerate(zip(snapshots, saved, strict=True)):
        if (
            any(
                outcome[key] != value
                for key, value in _mapping(record, ordinal).items()
            )
            or outcome["native_result"].get("pose_id") != outcome["work_key"]
        ):
            raise ValueError("native result lost source/conformer correspondence")
        if (
            outcome["native_result"]["status"] == "failed"
            and outcome["ranking_score"] is not None
        ):
            raise ValueError("a failed calculation was manufactured into a score")
    if (
        saved[-1]["native_result"]["status"] != "matched"
        or saved[-1]["ranking_score"] != 1
    ):
        raise ValueError("the declared caffeine source-self positive control failed")
    translated = msm.structure.translate(
        query_source, translation=puw.quantity([[[1, 2, 3]]], "nm"), in_place=False
    )
    control = plan.new_evaluator().evaluate(
        translated,
        pose_id="control:caffeine-translated",
        **execution["evaluation_options"],
    )
    _write(output / "translation-control.json", control)
    if (
        control["status"] != "matched"
        or get_screening_score(control, score_method="seeded_hit") != 1
    ):
        raise ValueError("the declared rigid-translation positive control failed")
    if not np.array_equal(
        source_coordinates,
        puw.get_value(msm.get(query_source, coordinates=True), to_unit="nm"),
    ):
        raise ValueError("translation or screening mutated source coordinates")
    for record in snapshots:
        if _identity(record["path"]) != {
            key: record[key] for key in ("sha256", "bytes")
        }:
            raise ValueError("prepared snapshot bytes changed during screening")
    event("screening", "completed", n_outcomes=3)
    return {
        "status": "completed",
        "query": {"path": str(query_path.resolve()), **_identity(query_path)},
        "ledger": {"path": str(ledger_path.resolve()), **_identity(ledger_path)},
        "work_manifest": {"path": str(manifest.resolve()), **_identity(manifest)},
        "native_outcomes": {
            "path": str((output / "native-outcomes.json").resolve()),
            **_identity(output / "native-outcomes.json"),
        },
        "effective_context": plan.context,
        "summary": [
            {
                "cid": record["cid"],
                "conformer_id": record["conformer_id"],
                "work_key": outcome["work_key"],
                "status": outcome["native_result"]["status"],
                "ranking_score": outcome["ranking_score"],
                "fit_value": outcome["native_result"].get("fit_value"),
                "score_method": outcome["score_method"],
            }
            for record, outcome in zip(snapshots, saved, strict=True)
        ],
        "resume": {
            "confirmed_before_interruption": 1,
            "newly_confirmed_after_reopen": 2,
            "first_work_attempts": 1,
            "full_view_count": 3,
        },
        "composed_native_equivalence": True,
        "source_self_control": {
            "cid": 2519,
            "expected_score": 1,
            "observed_score": saved[-1]["ranking_score"],
        },
        "translation_control": {
            "expected_score": 1,
            "observed_score": 1,
            "source_coordinates_unchanged": True,
        },
        "publication": "local-only complete molecular/query/native payloads pending rights review",
    }


def run(plan_path, acquisition_path, output_dir):
    """Run the fixed offline pilot, retaining failure journals in fresh output.

    Metadata/source preflight precedes output creation and scientific imports.
    Every received record is attempted once during preparation. Any preparation
    failure prevents scoring; no record, state, H or conformer is substituted.
    Runtime failures return a failed result and preserve all local artifacts.
    """
    validated = validate_acquisition(plan_path, acquisition_path)
    output = Path(output_dir).resolve()
    output.mkdir(parents=True, exist_ok=False)
    result = {
        "schema": "pharmacophoremt.pubchem3d-receiving-pilot@1",
        "status": "running",
        "plan_sha256": validated["plan_sha256"],
        "acquisition_sha256": validated["acquisition_sha256"],
        "recipe": json.loads(json.dumps(RECIPE)),
        "records": [],
        "screening": {"status": "not_run"},
        "scope": "Unlabeled fixed-three computed-conformer workflow; no receptor, predictive or performance validation",
    }

    def event(stage, status, **details):
        with (output / "stages.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(
                json.dumps(
                    _plain({"stage": stage, "status": status, **details}),
                    allow_nan=False,
                )
                + "\n"
            )

    try:
        _write(output / "result.json", result)
        snapshots = []
        for source in validated["records"]:
            try:
                prepared = _prepare(source, output, event)
            except Exception as error:
                failure = {
                    "type": type(error).__name__,
                    "code": getattr(error, "code", None),
                    "message": str(error),
                }
                result["records"].append(
                    {
                        "cid": source["cid"],
                        "conformer_id": source["conformer_id"],
                        "status": "preparation_failed",
                        "error": failure,
                    }
                )
                event("preparation", "failed", cid=source["cid"], error=failure)
            else:
                snapshots.append(prepared)
                result["records"].append(
                    {
                        "cid": source["cid"],
                        "conformer_id": source["conformer_id"],
                        "status": "prepared",
                        "snapshot": prepared,
                    }
                )
            _write(output / "result.json", result)
        result["preparation_counts"] = {
            "declared": 3,
            "prepared": len(snapshots),
            "failed": 3 - len(snapshots),
        }
        _write(
            output / "snapshot-manifest.json",
            {
                "schema": "pharmacophoremt.pubchem3d-prepared-snapshots@1",
                "plan_sha256": validated["plan_sha256"],
                "records": snapshots,
            },
        )
        for source in validated["records"]:
            _verify_file(source["sdf"])
        if len(snapshots) != 3:
            result["status"] = "preparation_failed"
            result["screening"] = {
                "status": "not_run",
                "reason": "at least one declared preparation failed; no filtering or substitution",
            }
        else:
            result["screening"] = {"status": "running"}
            _write(output / "result.json", result)
            result["screening"] = _screen(snapshots, output, event)
            result["status"] = "completed"
        for source in validated["records"]:
            _verify_file(source["sdf"])
        result["original_source_bytes_unchanged"] = True
    except Exception as error:
        result["status"] = "failed"
        result["error"] = {
            "type": type(error).__name__,
            "code": getattr(error, "code", None),
            "message": str(error),
        }
        if result["screening"]["status"] == "running":
            result["screening"]["status"] = "failed"
        event("pilot", "failed", error=result["error"])
    _write(output / "result.json", result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("acquisition", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args(argv)
    result = run(args.plan, args.acquisition, args.output)
    print(
        json.dumps(
            {"status": result["status"], "output": str(args.output)}, allow_nan=False
        )
    )
    return 0 if result["status"] == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
