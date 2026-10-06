"""Observed EST fixture client of public MolSysMT fixed-state H placement.

The chemical-template stage remains independent. Generated H positions are local
geometry, not observed coordinates or an environment-refined orientation.
"""

from collections import Counter

from devtools.prepared_ccd_ligands import state_payload

SELECTED_FEATURES = ["hb donor", "hb acceptor", "aromatic ring"]


def add_hydrogens(prepared_case):
    """Materialize the declared EST state without choosing chemistry or pH.

    This fixture orchestration calls public provider tools. It intentionally uses
    intersection attribute policy; the detached provider report records dropped
    atom annotations. Inputs and the earlier preparation report remain unchanged.
    """
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.modeler import get_features

    source = prepared_case["molecular_system"]
    before_coordinates = puw.get_value(
        msm.get(source, coordinates=True), to_unit="nm"
    ).copy()
    before_state = state_payload(source)
    before_ids = list(msm.get(source, element="atom", atom_id=True))
    inventory_before = msm.physchem.get_hydrogen_inventory(source)
    result = msm.build.add_missing_hydrogens(
        source,
        mode="fixed_chemical_state",
        pH=None,
        engine="RDKit",
        chemical_state="reference",
        structure_indices=[0],
        return_report=True,
        attribute_policy="intersection",
    )
    output = result["molecular_system"]
    inventory_after = msm.physchem.get_hydrogen_inventory(output)
    features = get_features(output)
    coordinates = msm.get(output, coordinates=True)
    pairs = result["report"]["parent_hydrogen_pairs"]
    bond_lengths = msm.structure.get_distances(
        output,
        selection=pairs[:, 0],
        selection_2=pairs[:, 1],
        pairs=True,
        pbc=False,
        parallel=False,
        use_gpu=False,
    )
    cip_declared = msm.physchem.get_cip_stereochemistry(output)
    cip_pose = msm.physchem.get_cip_stereochemistry(
        output, structure_indices=[0], from_coordinates=True
    )
    report = dict(
        schema="pharmacophoremt.eralpha_hydrogen_preparation@1",
        template_preparation=prepared_case["report"],
        hydrogen_addition=result["report"],
        inventory_before=inventory_before,
        inventory_after=inventory_after,
        source_state=before_state,
        prepared_state=state_payload(output),
        original_atom_ids=before_ids,
        prepared_atom_ids=list(msm.get(output, element="atom", atom_id=True)),
        source_atom_indices=prepared_case["report"]["source_atom_indices"],
        coordinates=puw.QuantityRecord.from_quantity(coordinates).to_dict(),
        added_bond_lengths=puw.QuantityRecord.from_quantity(bond_lengths).to_dict(),
        cip_declared=cip_declared,
        cip_from_coordinates=cip_pose,
        prepared_counts=msm.get(
            output,
            n_atoms=True,
            n_bonds=True,
            n_structures=True,
            output_type="dictionary",
        ),
        feature_counts=dict(
            Counter(feature["kind"] for feature in features["features"])
        ),
        heavy_coordinates_preserved=bool(
            np.array_equal(
                puw.get_value(coordinates, to_unit="nm")[:, : len(before_ids)],
                before_coordinates,
            )
        ),
        input_unchanged=bool(
            before_state == state_payload(source)
            and np.array_equal(
                before_coordinates,
                puw.get_value(msm.get(source, coordinates=True), to_unit="nm"),
            )
        ),
        readiness=dict(
            selected_features=SELECTED_FEATURES,
            directional_donors="available_generated_local_geometry",
            environment_refinement="not_performed",
            receptor="not_prepared",
            biological_validation="not_performed",
        ),
    )
    return dict(
        molecular_system=output,
        inventory=features,
        report=report,
        heavy_case=prepared_case,
    )
