"""Checksum-qualified CCD fixtures, prepared exclusively with public MolSysMT.

This is a fixture client, not a generic chemistry preparation/readiness API.
Original SD properties remain in the source files; ideal coordinates are not
observed binding poses. No conformers, hydrogens or chemical states are generated.
"""

import hashlib
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "tests/data/prepared_ccd"
MANIFEST_PATH = DIRECTORY / "manifest.json"


def load_cases():
    manifest = json.loads(MANIFEST_PATH.read_text())
    if manifest.get("schema") != "pharmacophoremt.prepared_ccd_ligands@1":
        raise ValueError("unsupported prepared CCD manifest")
    return deepcopy(manifest["cases"])


def state_payload(system):
    import molsysmt as msm

    payload = msm.convert(
        system.chemical_states, to_form="molsysmt.ChemicalStatesDict"
    ).to_dict()
    return json.loads(json.dumps(payload, default=lambda array: array.tolist()))


def prepare_case(case_id):
    """Load one fixed fixture and retain the actual preparation observations."""
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.modeler import get_features

    case = next(case for case in load_cases() if case["case_id"] == case_id)
    path = DIRECTORY / case["file"]
    raw = path.read_bytes()
    if (
        hashlib.sha256(raw).hexdigest() != case["sha256"]
        or len(raw) != case["byte_count"]
    ):
        raise ValueError(
            "CCD source changed; review identity and preparation before use"
        )
    source = msm.convert(
        str(path),
        to_form="molsysmt.MolSys",
        discard_properties=True,
        stereo_engine="rdkit",
    )
    before_state = state_payload(source)
    before_coordinates = puw.get_value(
        msm.get(source, coordinates=True), to_unit="nm"
    ).copy()
    try:
        get_features(source)
    except msm.StructuralInconsistencyError as error:
        raw_recognition = dict(status="blocked", code=error.code, message=str(error))
    else:
        raw_recognition = dict(status="completed")
    prepared = msm.convert(
        msm.convert(source, to_form="rdkit.Mol"), to_form="molsysmt.MolSys"
    )
    inventory = get_features(prepared)
    rmsd = msm.structure.get_rmsd(
        prepared,
        selection="all",
        reference_molecular_system=source,
        reference_selection="all",
        use_gpu=False,
        parallel=False,
    )
    after_state = state_payload(prepared)

    def atom_ids(system):
        return list(msm.get(system, element="atom", atom_id=True))

    def elements(system):
        return list(msm.get(system, element="atom", atom_type=True))

    # These aggregates are observations of the two declared fixtures, not a
    # reusable molecular readiness/chemistry algorithm.
    report = dict(
        schema="pharmacophoremt.prepared_ccd_observation@1",
        source=case,
        preparation=json.loads(MANIFEST_PATH.read_text())["preparation"],
        raw_recognition=raw_recognition,
        source_state=before_state,
        prepared_state=after_state,
        source_atom_ids=atom_ids(source),
        prepared_atom_ids=atom_ids(prepared),
        source_elements=elements(source),
        prepared_elements=elements(prepared),
        prepared_counts=msm.get(
            prepared,
            n_atoms=True,
            n_bonds=True,
            n_structures=True,
            output_type="dictionary",
        ),
        element_counts=dict(Counter(elements(prepared))),
        feature_counts=dict(
            Counter(feature["kind"] for feature in inventory["features"])
        ),
        coordinate_rmsd_nm=float(puw.get_value(rmsd, to_unit="nm").reshape(-1)[0]),
        source_coordinates_unchanged=bool(
            np.array_equal(
                before_coordinates,
                puw.get_value(msm.get(source, coordinates=True), to_unit="nm"),
            )
        ),
        source_state_unchanged=before_state == state_payload(source),
        source_bytes_unchanged=raw == path.read_bytes(),
        complete=True,
    )
    return dict(molecular_system=prepared, inventory=inventory, report=report)


def credit_source(case_id):
    """Explicit fixture-client resource credit, called only after successful use.

    Use an application-owned Ackredit session. Only an explicit call registers
    these fixture-client data references; provider tools may carry their own
    optional attribution. This does not credit G3PS.
    """
    import ackredit

    case = next(case for case in load_cases() if case["case_id"] == case_id)
    source_id = "pharmacophoremt:dataset:ccd:" + case_id + ":" + case["sha256"]
    article_id = "pharmacophoremt:doi:10.1093/bioinformatics/btu789"
    ackredit.register_item(
        id=source_id,
        type="dataset",
        title="wwPDB CCD " + case_id + " ideal coordinates",
        url=case["source_url"],
        publisher="Worldwide Protein Data Bank",
    )
    ackredit.register_item(
        id=article_id,
        type="article",
        title="The chemical component dictionary: complete descriptions of constituent molecules in experimentally determined 3D macromolecules in the Protein Data Bank",
        authors=[
            "Westbrook, John D.",
            "Shao, Chenghua",
            "Feng, Zukang",
            "Zhuravleva, Marina",
            "Velankar, Sameer",
            "Young, Jasmine",
        ],
        journal="Bioinformatics",
        year=2015,
        volume="31",
        number="8",
        pages="1274-1278",
        doi="10.1093/bioinformatics/btu789",
    )
    target = "devtools.prepared_ccd_ligands.prepare_case"
    context = dict(
        component_id=case_id,
        source_url=case["source_url"],
        sha256=case["sha256"],
        coordinate_kind="CCD ideal",
    )
    ackredit.track_item(
        source_id, used_by=target, roles=["input_data"], context=context
    )
    ackredit.track_item(
        article_id, used_by=target, roles=["resource_description"], context=context
    )


def motion_frames(system):
    """Fixture recipe: preserve frame zero and add a rigidly moved copy as one.

    The two frames are the same conformation in different placements.
    """
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    frames = msm.copy(system)
    original_ids = msm.get(system, structure_id=True)
    frames.structures.append(
        coordinates=msm.get(system, coordinates=True),
        structure_id=None if original_ids is None else np.asarray([1], dtype=np.int64),
        box=msm.get(system, box=True),
    )
    frames = msm.structure.rotate(
        frames,
        structure_indices=[1],
        rotation=np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]),
        rotation_center=puw.quantity([0, 0, 0], "nm"),
        in_place=False,
    )
    return msm.structure.translate(
        frames,
        structure_indices=[1],
        translation=puw.quantity([[[2.0, 1.0, 3.0]]], "nm"),
        in_place=False,
    )
