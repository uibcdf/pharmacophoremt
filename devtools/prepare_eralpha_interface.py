"""Offline, case-specific 1QKU fragment/EST client of public MolSysMT tools.

Chemical algorithms, recognition and detector implementations remain in MolSysMT.
This recipe owns the explicit fragment, chemical-state and atom-map declarations.
"""

import json

from devtools.audit_eralpha_receptor import _fingerprint
from devtools.prepare_eralpha_hydrogens import add_hydrogens
from devtools.prepare_eralpha_ligand import ROOT, prepare_case
from devtools.validate_eralpha_template import portable

MANIFEST = ROOT / "tests/data/eralpha_interface/manifest.json"


def prepare_interface():
    """Return the declared prepared interface, public analyses and full provenance.

    Uses the existing checksum-qualified EST preparation and the provider's peptide
    template, aromatic normalization and fixed-state H operations. All maps refer
    to the original deposited asymmetric unit; generated atoms have source -1.
    This is one offline fixture recipe, not general receptor preparation.
    """
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    declaration = json.loads(MANIFEST.read_text())
    ligand_case = add_hydrogens(prepare_case())
    source = ligand_case["heavy_case"]["source"]
    before = _fingerprint(source)
    if (
        declaration["source_sha256"]
        != ligand_case["heavy_case"]["report"]["manifest"]["source_sha256"]
    ):
        raise ValueError("Interface declaration disagrees with the observed source")
    receptor_source = np.asarray(
        msm.select(source, selection=declaration["receptor_selection"]), dtype=np.int64
    )
    receptor = msm.extract(source, selection=receptor_source)
    names = list(msm.get(receptor, element="group", group_name=True))
    group_ids = list(map(int, msm.get(receptor, element="group", group_id=True)))
    start, stop = declaration["receptor_group_id_range"]
    if group_ids != list(range(start, stop + 1)):
        raise ValueError("Declared closed receptor fragment changed")
    definition = msm.physchem.get_peptide_chemical_template(
        [declaration["residue_states"].get(name, name) for name in names],
        n_terminal_state=declaration["n_terminal_state"],
        c_terminal_state=declaration["c_terminal_state"],
    )
    template = definition["template"]
    if (
        definition["template_provenance"]["checksum"]
        != declaration["peptide_graph_sha256"]
    ):
        raise ValueError("Reviewed peptide graph changed; requalify this case")
    observed_atoms = msm.get(
        receptor,
        element="atom",
        group_index=True,
        atom_name=True,
        output_type="dictionary",
    )
    template_atoms = msm.get(
        template,
        element="atom",
        group_index=True,
        atom_name=True,
        output_type="dictionary",
    )
    lookup = {
        (int(group), name): index
        for index, (group, name) in enumerate(
            zip(observed_atoms["group_index"], observed_atoms["atom_name"], strict=True)
        )
    }
    correspondence = []
    for index, (group, name) in enumerate(
        zip(template_atoms["group_index"], template_atoms["atom_name"], strict=True)
    ):
        observed_name = (
            declaration["template_to_observed_atom_names"]
            .get(names[int(group)], {})
            .get(name, name)
        )
        correspondence.append([index, lookup[(int(group), observed_name)]])
    if len(lookup) != len(receptor_source) or sorted(
        pair[1] for pair in correspondence
    ) != list(range(len(receptor_source))):
        raise ValueError(
            "Reviewed receptor correspondence is not exhaustive and unique"
        )
    normalized = msm.physchem.normalize_aromatic_bond_orders(receptor)
    applied = msm.physchem.apply_chemical_template(
        normalized["molecular_system"],
        template=template,
        atom_correspondence=correspondence,
        template_provenance=definition["template_provenance"],
    )
    prepared_receptor = applied["molecular_system"]
    prepared_receptor.chemical_states.append_preparation_history(
        template.chemical_states.get_preparation_history()
    )
    hydrogenated = msm.build.add_missing_hydrogens(
        prepared_receptor,
        mode="fixed_chemical_state",
        pH=None,
        engine="RDKit",
        attribute_policy="intersection",
        return_report=True,
    )
    partner = hydrogenated["molecular_system"]
    ligand = ligand_case["molecular_system"]

    def source_map(system, addition, indices):
        result = np.full(msm.get(system, n_atoms=True), -1, dtype=np.int64)
        for original, output in addition["atom_correspondence"]:
            result[int(output)] = indices[int(original)]
        return result

    atom_sources = np.concatenate(
        [
            source_map(partner, hydrogenated["report"], receptor_source),
            source_map(
                ligand,
                ligand_case["report"]["hydrogen_addition"],
                ligand_case["report"]["source_atom_indices"],
            ),
        ]
    )
    interface = msm.merge([partner, ligand], to_form="molsysmt.MolSys")
    receptor_atoms = np.arange(msm.get(partner, n_atoms=True), dtype=np.int64)
    ligand_atoms = np.arange(
        len(receptor_atoms), msm.get(interface, n_atoms=True), dtype=np.int64
    )
    observed = np.flatnonzero(atom_sources >= 0)
    xyz = puw.get_value(msm.get(interface, coordinates=True), to_unit="nm")
    original_xyz = puw.get_value(msm.get(source, coordinates=True), to_unit="nm")
    np.testing.assert_array_equal(
        xyz[:, observed], original_xyz[:, atom_sources[observed]]
    )
    np.testing.assert_array_equal(
        np.asarray(msm.get(interface, element="atom", atom_id=True))[observed],
        np.asarray(msm.get(source, element="atom", atom_id=True))[
            atom_sources[observed]
        ],
    )
    detectors = {
        "hydrophobic": msm.interactions.hydrophobic.get_hydrophobic_interactions,
        "hbonds": msm.interactions.hbonds.get_hbonds,
        "pi_pi": msm.interactions.pi_pi.get_pi_pi_interactions,
    }
    analyses = {}
    for label, detector in detectors.items():
        result = detector(
            interface,
            selection=receptor_atoms,
            selection_2=ligand_atoms,
            selection_mode="between",
            structure_indices=[0],
            pbc=False,
            **declaration["detectors"][label],
        )
        payload = msm.convert(result, to_form="molsysmt.InteractionsDict")
        payload.data["atom_source_indices"] = atom_sources.copy()
        payload.data["source_n_atoms"] = msm.get(source, n_atoms=True)
        payload.data["source_id"] = "rcsb:1QKU:deposited-atom-order"
        analyses[label] = msm.convert(payload, to_form="molsysmt.Interactions")
    interface.interactions = analyses
    counts = msm.get(
        interface,
        n_atoms=True,
        n_bonds=True,
        n_structures=True,
        output_type="dictionary",
    )
    if counts != declaration["expected_counts"]:
        raise ValueError("Prepared interface no longer matches the declared graph")
    report = portable(
        dict(
            schema="pharmacophoremt.eralpha_interface_preparation@1",
            declaration=declaration,
            receptor_group_ids=group_ids,
            receptor_atom_correspondence=correspondence,
            receptor_template=definition["report"],
            aromatic_normalization={
                key: value
                for key, value in normalized["report"].items()
                if key
                not in {"original_bond_orders", "original_fractional_bond_orders"}
            },
            original_aromatic_orders="retained with native types/unknowns in H5MSM preparation history",
            receptor_application=applied["report"],
            receptor_hydrogen_addition=hydrogenated["report"],
            ligand_preparation=ligand_case["report"],
            prepared_counts=counts,
            atom_source_indices=atom_sources,
            observations={
                label: dict(
                    n_interactions=analysis.n_interactions,
                    parameters=analysis.parameters,
                    evaluated_structure_indices=analysis.evaluated_structure_indices,
                )
                for label, analysis in analyses.items()
            },
            observed_identity_and_coordinates_preserved=True,
            source_unchanged=before == _fingerprint(source),
            full_receptor_acceptance=False,
            environmental_refinement="not_performed",
            biological_validation="not_performed",
        )
    )
    return dict(
        source=source,
        molecular_system=interface,
        receptor=receptor_atoms,
        ligand=ligand_atoms,
        analyses=analyses,
        report=report,
    )
