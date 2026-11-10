"""Original microcase composition; molecular files and geometry stay MolSysMT-owned."""

import hashlib
import json
from pathlib import Path

DIRECTORY = Path(__file__).resolve().parents[1] / "tests/data/feature_snapshot"


def identity(path):
    with Path(path).open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"bytes": Path(path).stat().st_size, "sha256": digest}


def declaration():
    data = json.loads((DIRECTORY / "declaration.json").read_text())
    if data["schema"] != "pharmacophoremt.feature-snapshot-case@1":
        raise ValueError("Unknown feature snapshot case")
    return data


def parent_manifest():
    return json.loads((DIRECTORY / "parents.json").read_text())


def load_parent(key):
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    spec = next(c for c in declaration()["cases"] if c["key"] == key)
    row = next(c for c in parent_manifest()["parents"] if c["key"] == key)
    path = DIRECTORY / row["file"]
    assert identity(path) == {k: row[k] for k in ("bytes", "sha256")}
    source = msm.h5msm.read(str(path))
    assert msm.get(source, n_atoms=True) == len(spec["atom_types"])
    assert msm.get(source, element="atom", atom_type=True) == spec["atom_types"]
    assert msm.get(source, formal_charge=True) == spec["formal_charges"]
    assert source.chemical_states.get(n_bonds=True) == spec["n_bonds"]
    assert msm.get(source, n_structures=True) == 1
    np.testing.assert_allclose(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm")[0],
        spec["coordinates_nm"],
        rtol=0,
        atol=declaration()["coordinate_tolerance_nm"],
    )
    parent = {
        "source_key": "nm" if key == "ions" else key,
        "occurrence_key": "1 nm" if key == "ions" else key + ":0",
        "artifact_sha256": row["sha256"],
        "artifact_bytes": row["bytes"],
        "n_atoms": len(spec["atom_types"]),
        "structure_index": 0,
        "chemical_state": 0,
        "trust": "caller-verified-artifact/unchanged-source",
        "preparation": "public MolSysMT construction/aromaticity/native write-read; no repair",
    }
    return source, parent


def producer_context(admission):
    import importlib.metadata

    import pharmacophoremt as phmt

    return {
        "scope": "selected-case-context",
        "admission_sha256": admission,
        "runtime_version": phmt.__version__,
        "versions": {
            name: importlib.metadata.version(name)
            for name in (
                "pharmacophoremt",
                "molsysmt",
                "pyunitwizard",
                "numpy",
                "ackredit",
            )
        },
    }


def projection(inventory):
    from pharmacophoremt import pyunitwizard as puw

    rows = []
    for row in inventory["features"]:
        out = {k: row[k] for k in ("kind", "atom_indices", "geometry_atom_indices")}
        for key, unit in (
            ("center", "nm"),
            ("direction", "dimensionless"),
            ("normal", "dimensionless"),
            ("charge", "e"),
        ):
            value = row[key]
            if value is not None:
                value = puw.get_value(value, to_unit=unit)
                value = value.tolist() if hasattr(value, "tolist") else value
            out[key] = value
        rows.append(out)
    return {
        "definition": inventory["definition"],
        "structure_index": inventory["structure_index"],
        "chemical_state": inventory["chemical_state"],
        "selected_atom_indices": inventory["selected_atom_indices"],
        "features": rows,
    }


def independent_geometry(key, inventory):
    import numpy as np

    rows = projection(inventory)["features"]
    if key == "charges":
        expected = {0: ([0, 0, 0], 1), 1: ([0.5, 0, 0], -1), 2: ([0, 0.5, 0], 1)}
        charges = [
            r for r in rows if r["kind"] in ("positive charge", "negative charge")
        ]
        assert len(charges) == 3
        for row in charges:
            center, charge = expected[row["atom_indices"][0]]
            np.testing.assert_allclose(row["center"], center, rtol=0, atol=1e-12)
            assert row["charge"] == charge
    elif key == "donors":
        assert len(rows) == 2 and {tuple(r["atom_indices"]) for r in rows} == {
            (1, 0),
            (1, 2),
        }
        for row in rows:
            np.testing.assert_allclose(row["center"], [0, 0, 0], rtol=0, atol=1e-12)
            expected = [1, 0, 0] if row["atom_indices"] == [1, 0] else [0, 1, 0]
            np.testing.assert_allclose(row["direction"], expected, rtol=0, atol=1e-12)
    elif key == "aromatic":
        assert len(rows) == 1 and rows[0]["atom_indices"] == list(range(6))
        np.testing.assert_allclose(rows[0]["center"], [0, 0, 0], rtol=0, atol=1e-12)
        np.testing.assert_allclose(
            np.abs(rows[0]["normal"]), [0, 0, 1], rtol=0, atol=1e-12
        )
    elif key == "empty":
        assert rows == []
    else:
        raise ValueError("Unknown original geometry oracle")
