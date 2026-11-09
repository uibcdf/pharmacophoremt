"""Independent original-ion chemistry, coordinate and export-lifetime controls."""

import json

import pytest

from phmt_test_support.pharmer_p1 import DIRECTORY, load_declaration
from phmt_test_support.pharmer_p1_export import export_case


@pytest.mark.parametrize(
    "key,expected",
    [
        ("proper-motion", [[20, -10, 5], [20, -5, 5], [10, -10, 5]]),
        ("permuted-source", [[10, -10, 5], [20, -10, 5], [20, -5, 5]]),
        ("uniform-stretch", [[20, -10, 5], [20, 0, 5], [0, -10, 5]]),
    ],
)
def test_original_sources_export_and_roundtrip_without_changed_geometry(
    tmp_path, key, expected
):
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    declaration, _ = load_declaration()
    case = next(c for c in declaration["cases"] if c["key"] == key)
    path = tmp_path / (key + ".sdf")
    record = export_case(case, path)
    recovered = msm.convert(path, to_form="molsysmt.MolSys")
    np.testing.assert_allclose(
        puw.get_value(msm.get(recovered, coordinates=True), to_unit="angstrom")[0],
        expected,
        rtol=0,
        atol=1e-11,
    )
    assert msm.get(recovered, element="atom", atom_type=True) == ["Na", "K", "Li"]
    assert msm.get(recovered, formal_charge=True) == [1, 1, 1]
    assert recovered.chemical_states.get(n_bonds=True) == 0
    assert msm.get(recovered, n_structures=True) == 1
    assert record["source_atom_indices"] == [0, 1, 2]
    assert record["source_unchanged"] and record["external"] == "not_executed"
    assert path.read_bytes() == (DIRECTORY / "external" / path.name).read_bytes()
    before = path.read_bytes()
    with pytest.raises(FileExistsError):
        export_case(case, path)
    assert path.read_bytes() == before


def test_existing_export_directory_is_refused_without_overwrite(tmp_path):
    from devtools.prepare_pharmer_p1 import main

    marker = tmp_path / "original.txt"
    marker.write_text("preserve original")
    with pytest.raises(FileExistsError):
        main(["--output-directory", str(tmp_path)])
    assert list(tmp_path.iterdir()) == [marker]
    assert marker.read_text() == "preserve original"


def test_failed_export_stays_a_failure_in_the_complete_manifest(tmp_path, monkeypatch):
    from devtools.prepare_pharmer_p1 import main
    from phmt_test_support import pharmer_p1_export

    real = pharmer_p1_export.export_case

    def fail_second(case, destination):
        if case["key"] == "permuted-source":
            raise RuntimeError("controlled original export failure")
        return real(case, destination)

    monkeypatch.setattr(pharmer_p1_export, "export_case", fail_second)
    output = tmp_path / "new"
    assert main(["--output-directory", str(output)]) == 1
    report = json.loads((output / "manifest.json").read_text())
    assert [r["status"] for r in report["cases"]] == [
        "verified-export",
        "failed-export",
        "verified-export",
    ]
    assert report["cases"][1]["error_type"] == "RuntimeError"
    assert not report["passed"] and report["external"] == "not_executed"
