"""Case-specific P1 export; all molecular serialization belongs to MolSysMT."""

import hashlib
from pathlib import Path


def export_case(case, destination):
    """Export one original three-ion source, then verify chemistry and geometry.

    The caller owns a new directory. Existing files are refused. V2000 uses
    angstrom coordinates; readback uses the original P1 absolute tolerance in
    nm, with no relative allowance. Original source coordinates stay byte-equal.
    No external feature perception or engine execution occurs.
    """
    destination = Path(destination)
    if destination.exists():
        raise FileExistsError(destination)

    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw
    from phmt_test_support.absence_inputs import system
    from phmt_test_support.pharmer_p1 import load_declaration

    declaration, _ = load_declaration()
    if case not in declaration["cases"]:
        raise ValueError("Export requires an unchanged original P1 case")
    source = system(
        declaration["smiles"], case["centers"], unit=declaration["source_unit"]
    )
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    atoms = msm.get(source, element="atom", atom_type=True)
    charges = msm.get(source, formal_charge=True)
    if atoms != ["Na", "K", "Li"] or charges != [1, 1, 1]:
        raise ValueError("P1 export requires original atom order and charges")
    if source.chemical_states.get(n_bonds=True) != 0:
        raise ValueError("P1 export requires the original disconnected graph")
    msm.convert(source, to_form=destination, ctfile_version="V2000")
    recovered = msm.convert(destination, to_form="molsysmt.MolSys")
    after = puw.get_value(msm.get(recovered, coordinates=True), to_unit="nm")
    np.testing.assert_allclose(
        after, before, rtol=0, atol=declaration["position_error_limit_nm"]
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )
    if (
        msm.get(recovered, element="atom", atom_type=True) != atoms
        or msm.get(recovered, formal_charge=True) != charges
        or recovered.chemical_states.get(n_bonds=True) != 0
        or msm.get(recovered, n_structures=True) != 1
    ):
        raise ValueError("P1 round-trip changed chemistry, atom order or frame count")
    return {
        "key": case["key"],
        "file": destination.name,
        "bytes": destination.stat().st_size,
        "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
        "format": "SDF V2000",
        "coordinate_unit": "angstrom",
        "source_atom_indices": [0, 1, 2],
        "atom_types": atoms,
        "formal_charges": charges,
        "n_bonds": 0,
        "n_frames": 1,
        "coordinates_nm": before[0].tolist(),
        "roundtrip_coordinates_nm": after[0].tolist(),
        "max_roundtrip_error_nm": float(np.max(np.abs(after - before))),
        "roundtrip_tolerance_nm": declaration["position_error_limit_nm"],
        "source_unchanged": True,
        "external_atom_membership": "not observed",
        "external": "not_executed",
    }
