"""Pinned 1QKU ligand client of MolSysMT's public template tools.

The template is a frozen provider-curated artifact. No chemistry is rebuilt here,
no template coordinates are imported and no hydrogen coordinates are generated.
"""

import hashlib
import json
from collections import Counter
from pathlib import Path

from devtools.prepared_ccd_ligands import state_payload

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "tests/data/eralpha_rcsb"
TEMPLATES = ROOT / "tests/data/eralpha_template"
SELECTED_FEATURES = ["hb acceptor", "aromatic ring"]


def load_manifest():
    """Check pinned artifact bytes against this checkout's declarations."""
    acquisition = json.loads((TEMPLATES / "acquisition.json").read_text())
    manifest = json.loads((TEMPLATES / "manifest.json").read_text())
    source_manifest = json.loads((SOURCES / "manifest.json").read_text())
    for name, expected in acquisition["files"].items():
        if hashlib.sha256((TEMPLATES / name).read_bytes()).hexdigest() != expected:
            raise ValueError("Curated template artifact changed; review before use")
    for name, key in (("1qku.cif", "source_sha256"), ("EST.cif", "ccd_sha256")):
        actual = hashlib.sha256((SOURCES / name).read_bytes()).hexdigest()
        if (
            actual != manifest[key]
            or actual != source_manifest["files"][name]["sha256"]
        ):
            raise ValueError("Observed source or CCD changed; review before use")
    return manifest


def prepare_case():
    """Assess/apply the frozen template and retain actual partial readiness."""
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw
    from pharmacophoremt.modeler import get_features

    manifest = load_manifest()
    source = msm.convert(str(SOURCES / "1qku.cif"), to_form="molsysmt.MolSys")
    before_coordinates = puw.get_value(
        msm.get(source, coordinates=True), to_unit="nm"
    ).copy()
    before_state = state_payload(source)
    indices = list(map(int, msm.select(source, selection=manifest["source_selection"])))
    ligand = msm.extract(source, selection=indices)
    names = list(msm.get(ligand, element="atom", atom_name=True))
    if (
        indices != manifest["source_atom_indices"]
        or names != manifest["source_atom_names"]
    ):
        raise ValueError("Selected ligand correspondence changed; review before use")
    try:
        get_features(ligand)
    except msm.StructuralInconsistencyError as error:
        raw = dict(status="blocked", code=error.code, message=str(error))
    else:
        raw = dict(status="completed")
    options = dict(
        template=TEMPLATES / "est_template.h5msm",
        atom_correspondence=manifest["atom_correspondence"],
        template_provenance=manifest["template_provenance"],
    )
    assessment = msm.physchem.assess_chemical_template(ligand, **options)
    applied = msm.physchem.apply_chemical_template(ligand, **options)
    prepared = applied["molecular_system"]
    inventory = get_features(prepared)
    coordinates = msm.get(prepared, coordinates=True)
    report = dict(
        schema="pharmacophoremt.eralpha_preparation@1",
        manifest=manifest,
        acquisition=json.loads((TEMPLATES / "acquisition.json").read_text()),
        raw_recognition=raw,
        assessment=assessment,
        application=applied["report"],
        source_atom_indices=indices,
        source_atom_names=names,
        source_atom_ids=list(msm.get(ligand, element="atom", atom_id=True)),
        prepared_atom_ids=list(msm.get(prepared, element="atom", atom_id=True)),
        source_ligand_state=state_payload(ligand),
        prepared_state=state_payload(prepared),
        coordinates=puw.QuantityRecord.from_quantity(coordinates).to_dict(),
        prepared_counts=msm.get(
            prepared,
            n_atoms=True,
            n_bonds=True,
            n_structures=True,
            output_type="dictionary",
        ),
        feature_counts=dict(
            Counter(record["kind"] for record in inventory["features"])
        ),
        readiness=dict(
            selected_features=SELECTED_FEATURES,
            directional_donors="pending_explicit_hydrogen_coordinates",
            hydrogen_placement="not_performed",
            receptor="not_prepared",
            biological_validation="not_performed",
        ),
        pose_preserved=bool(
            np.array_equal(
                puw.get_value(coordinates, to_unit="nm"),
                before_coordinates[:, indices, :],
            )
        ),
        source_unchanged=bool(
            state_payload(source) == before_state
            and np.array_equal(
                puw.get_value(msm.get(source, coordinates=True), to_unit="nm"),
                before_coordinates,
            )
        ),
    )
    return dict(
        source=source,
        ligand=ligand,
        molecular_system=prepared,
        inventory=inventory,
        report=report,
    )


def credit_inputs(roles=("observed", "ccd", "template")):
    """Credit the observed data and curated template after successful use.

    Applications own Ackredit sessions. Curation software is historical provenance,
    not software executed by this native artifact-loading calculation.
    Select only roles actually used by the calling stage; the default credits
    all three inputs of the complete template-preparation route.
    """
    import ackredit

    roles = tuple(roles)
    if not set(roles).issubset({"observed", "ccd", "template"}):
        raise ValueError("Unknown ERalpha input role")
    manifest = load_manifest()
    acquisition = json.loads((TEMPLATES / "acquisition.json").read_text())
    records = [
        (
            "observed",
            "RCSB PDB 1QKU deposited asymmetric unit",
            manifest["source_uri"],
            manifest["source_sha256"],
            manifest["source_revision"],
        ),
        (
            "ccd",
            "wwPDB CCD EST chemical definition",
            manifest["template_provenance"]["source_uri"],
            manifest["ccd_sha256"],
            manifest["template_provenance"]["version"],
        ),
        (
            "template",
            "MolSysMT curated EST heavy-atom template",
            acquisition["provider_repository"],
            acquisition["files"]["est_template.h5msm"],
            "local artifact from " + acquisition["provider_head"],
        ),
    ]
    with ackredit.scope("pharmacophoremt.fixture.eralpha_inputs"):
        for role, title, url, checksum, version in records:
            if role not in roles:
                continue
            item_id = "pharmacophoremt:dataset:eralpha:" + role + ":" + checksum
            ackredit.register_item(
                id=item_id, type="dataset", title=title, url=url, version=version
            )
            ackredit.track_item(
                item_id,
                roles=["input_data"],
                context=dict(
                    input_role=role,
                    sha256=checksum,
                    coordinate_policy="preserve_deposited_pose",
                    chemical_component="EST",
                    version=version,
                ),
            )
