"""Real consumer gates for the independent MolSysMT chemical domain (#69)."""

from copy import deepcopy

import molsysmt as msm
import numpy as np
import pytest

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt.modeler import from_ligand, get_features
from pharmacophoremt.screening import PoseEvaluator
from phmt_test_support.absence_inputs import system

pytestmark = pytest.mark.skipif(
    not hasattr(msm, "chemical_states"), reason="requires the #255 source cutover"
)

XYZ = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float)


def ions():
    return system("[Na+].[K+].[Li+].[Cs+]", XYZ)


@pytest.mark.parametrize("kind", ["absent", "zero", "unknown"])
def test_unavailable_chemistry_is_not_a_known_empty_donor_inventory(kind):
    source = ions()
    if kind == "absent":
        topology = msm.convert(source, to_form="molsysmt.Topology")
        assert not hasattr(topology, "bonds")
        source = msm.convert([topology, source.structures], to_form="molsysmt.MolSys")
        assert source.chemical_states is None
    else:
        states = msm.ChemicalStates(n_atoms=4)
        if kind == "unknown":
            states.append_state()
        source.chemical_states = states
        assert states.n_chemical_states == (0 if kind == "zero" else 1)
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    with pytest.raises(Exception) as caught:
        get_features(source, features=["hb donor"])
    assert type(caught.value).__module__.startswith("molsysmt.")
    assert caught.value.code == "MSM-ERR-STRUCT-003"
    assert (
        source.chemical_states is None
        if kind == "absent"
        else (source.chemical_states.n_chemical_states == (0 if kind == "zero" else 1))
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )
    known = ions()
    assert msm.get(known, n_bonds=True, chemical_state=0) == 0
    assert get_features(known, features=["hb donor"])["features"] == []
    assert len(get_features(known, features=["positive charge"])["features"]) == 4


def test_explicit_state_survives_ambiguous_reference_without_mutation():
    source = ions()
    payload = msm.convert(source, to_form="molsysmt.ChemicalStatesDict")
    payload.data["states"].append(deepcopy(payload.data["states"][0]))
    payload.data["reference_chemical_state_index"] = None
    source.chemical_states = msm.convert(payload, to_form="molsysmt.ChemicalStates")
    msm.set(source, chemical_state=1, formal_charge=[0, 0, 0, 0])
    query = from_ligand(source, chemical_state=0, features=["positive charge"])
    before = [
        np.array(msm.get(source, formal_charge=True, chemical_state=state), copy=True)
        for state in (0, 1)
    ]
    with pytest.raises(Exception) as caught:
        get_features(source, features=["positive charge"])
    assert type(caught.value).__module__.startswith("molsysmt.")
    assert caught.value.code == "MSM-ERR-STRUCT-003"
    result = PoseEvaluator(query).evaluate(source, chemical_state=1)
    assert result["status"] == "not_matched" and result["fit_value"] == 0
    assert (
        len(
            get_features(source, chemical_state=0, features=["positive charge"])[
                "features"
            ]
        )
        == 4
    )
    for state, charges in enumerate(before):
        np.testing.assert_array_equal(
            msm.get(source, formal_charge=True, chemical_state=state), charges
        )
    assert source.chemical_states.reference_chemical_state_index is None


def test_nonconsecutive_extraction_copy_and_h5msm_preserve_selected_features(tmp_path):
    source = ions()
    source.structures.append(coordinates=puw.quantity([XYZ + 2], "nm"))
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    extracted = msm.extract(source, selection=[0, 1, 3], structure_indices=[1])
    expected = before[1:2, [0, 1, 3], :]
    np.testing.assert_array_equal(
        puw.get_value(msm.get(extracted, coordinates=True), to_unit="nm"), expected
    )
    clone = msm.copy(extracted)
    msm.set(clone, coordinates=puw.quantity(expected + 5, "nm"))
    path = str(tmp_path / "selected.h5msm")
    msm.convert(extracted, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    inventory = get_features(restored, features=["positive charge"])
    assert [row["atom_indices"] for row in inventory["features"]] == [[0], [1], [2]]
    np.testing.assert_array_equal(
        [puw.get_value(row["center"], to_unit="nm") for row in inventory["features"]],
        expected[0],
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )
    np.testing.assert_array_equal(
        puw.get_value(msm.get(extracted, coordinates=True), to_unit="nm"), expected
    )


def test_connectivity_components_do_not_replace_stable_molecule_membership():
    source = system("CC.CC", [[0, 0, 0], [0.15, 0, 0], [1, 0, 0], [1.15, 0, 0]])
    before = puw.get_value(msm.get(source, coordinates=True), to_unit="nm").copy()
    assert not hasattr(source.topology, "bonds")
    assert not hasattr(source.topology, "components")
    assert msm.get(source, n_molecules=True) == 2
    assert msm.get(source, n_components=True, chemical_state=0) == 2
    source.chemical_states.remove_bonds([0], chemical_state=0)
    assert msm.get(source, n_molecules=True) == 2
    assert msm.get(source, n_components=True, chemical_state=0) == 3
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), before
    )
