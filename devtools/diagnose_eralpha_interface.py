"""Case-specific public-tool diagnosis of the prepared 1QKU empty families.

Run: python -m devtools.diagnose_eralpha_interface --output FILE
No chemical inference, plane/intersection engine or geometry refinement lives here.
"""

import argparse
import hashlib
import importlib.metadata
import json
import platform
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

from devtools.audit_eralpha_receptor import _fingerprint
from devtools.benchmark_rigid_consensus import _source_record
from devtools.prepare_eralpha_interface import MANIFEST, prepare_interface
from devtools.prepare_eralpha_ligand import ROOT, credit_inputs
from devtools.validate_eralpha_template import portable
from devtools.validate_prepared_ccd_ligands import scientific_projection

DIAGNOSTICS = MANIFEST.with_name("diagnostics.json")


def diagnose(case):
    """Measure recognized candidates and run fixed, separately labeled criteria.

    Compose public recognition and geometry tools on this one declared fixture.
    The near-candidate table is a diagnostic inventory, never an Interactions
    analysis or pharmacophoric observation. Only provider detectors classify
    interactions. Their complete parameters, empty coverage and provenance stay
    in each comparison. The original cached analyses are not replaced.
    """
    import molsysmt as msm
    import numpy as np

    from pharmacophoremt import pyunitwizard as puw

    declaration = json.loads(DIAGNOSTICS.read_text())
    system = case["molecular_system"]
    before_state = deepcopy(
        msm.convert(
            system.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        ).to_dict()
    )
    before_xyz = puw.get_value(msm.get(system, coordinates=True), to_unit="nm").copy()
    source_before = _fingerprint(case["source"])
    original_analyses = {
        name: portable(msm.convert(analysis, to_form="molsysmt.InteractionsDict").data)
        for name, analysis in case["analyses"].items()
    }
    sources = np.asarray(case["report"]["atom_source_indices"], dtype=np.int64)
    atoms = msm.get(
        system,
        element="atom",
        atom_name=True,
        group_name=True,
        group_id=True,
        chain_id=True,
        output_type="dictionary",
    )
    before_atoms = deepcopy(atoms)

    def atom(index):
        return dict(
            prepared_index=int(index),
            source_index=int(sources[index]),
            **{name: values[index] for name, values in atoms.items()},
        )

    sites = msm.physchem.get_hbond_sites(
        system, method="smarts_donor_acceptor", structure_indices=[0]
    )
    donors, acceptors = sites["donor_hydrogen_pairs"], sites["acceptor_atom_indices"]
    ligand = np.asarray(case["ligand"], dtype=np.int64)
    receptor = np.asarray(case["receptor"], dtype=np.int64)
    triplets = np.asarray(
        [
            [d, h, a]
            for d, h in donors
            for a in acceptors
            if (d in receptor and a in ligand) or (d in ligand and a in receptor)
        ],
        dtype=np.int64,
    )
    distances = puw.get_value(
        msm.structure.get_distances(
            system,
            selection=triplets[:, [0, 2]],
            pairs=True,
            structure_indices=[0],
            pbc=False,
        ),
        to_unit="nm",
    ).ravel()
    radius = float(
        puw.get_value(puw.quantity(declaration["hbond_candidate_radius"]), to_unit="nm")
    )
    near = distances <= radius
    triplets, distances = triplets[near], distances[near]
    angles = puw.get_value(
        msm.structure.get_angles(
            system, triplets=triplets, structure_indices=[0], pbc=False
        ),
        to_unit="degrees",
    ).ravel()
    parameters = case["analyses"]["hbonds"].parameters
    distance_cutoff = parameters["distance_threshold"]
    angle_cutoff = parameters["angle_threshold"]
    distance_limit = float(
        puw.get_value(
            puw.quantity(distance_cutoff["value"], distance_cutoff["unit"]),
            to_unit="nm",
        )
    )
    angle_limit = float(
        puw.get_value(
            puw.quantity(angle_cutoff["value"], angle_cutoff["unit"]), to_unit="degrees"
        )
    )
    candidates = [
        dict(
            donor=atom(d),
            hydrogen=atom(h),
            acceptor=atom(a),
            donor_acceptor_distance=dict(value=float(distance), unit="nm"),
            donor_hydrogen_acceptor_angle=dict(value=float(angle), unit="degrees"),
            passes_declared_distance=bool(distance <= distance_limit),
            passes_declared_angle=bool(angle >= angle_limit),
            kind="recognized_geometric_candidate_not_observation",
        )
        for (d, h, a), distance, angle in zip(triplets, distances, angles, strict=True)
    ]
    scope = dict(
        selection=receptor,
        selection_2=ligand,
        structure_indices=[0],
        selection_mode="between",
        pbc=False,
    )

    def comparison(policy, detector, defaults):
        kwargs = {
            key: value
            for key, value in policy.items()
            if key not in {"name", "expected_count"}
        }
        result = detector(system, **scope, **(defaults | kwargs))
        return dict(
            name=policy["name"],
            declaration=policy,
            n_interactions=result.n_interactions,
            analysis=msm.convert(result, to_form="molsysmt.InteractionsDict").data,
        )

    hbonds = [
        comparison(
            policy,
            msm.interactions.hbonds.get_hbonds,
            dict(
                method="donor_acceptor_distance_angle", profile="smarts_donor_acceptor"
            ),
        )
        for policy in declaration["hbond_sensitivity"]
    ]
    patterns = case["analyses"]["pi_pi"].parameters["smarts_patterns"]
    matches = msm.topology.get_substructure_matches(
        system, patterns, structure_indices=[0]
    )
    rings = sorted(
        [row for matrix in matches["matches"] for row in matrix],
        key=lambda row: tuple(sorted(row)),
    )
    ring_ligand = [ring for ring in rings if np.isin(ring, ligand).all()]
    ring_receptor = [ring for ring in rings if np.isin(ring, receptor).all()]
    # Public centroids/planes are a diagnostic view. They are explicitly not
    # the centroid-edge planes of the original reference profile.
    planes = msm.structure.get_least_squares_plane(
        system, selection=ring_receptor + ring_ligand, structure_indices=[0], pbc=False
    )
    centers = puw.get_value(planes["centers"], to_unit="nm")[0]
    # Use the provider's general distance operation on its measured centroids.
    centroid_distances = puw.get_value(
        msm.structure.get_distances(
            puw.quantity(centers[np.newaxis], "nm"),
            selection=list(range(len(ring_receptor))),
            selection_2=list(range(len(ring_receptor), len(centers))),
            structure_indices=[0],
            pbc=False,
        ),
        to_unit="nm",
    )[0]
    ring_pairs = sorted(
        [
            dict(
                receptor_members=[atom(index) for index in receptor_ring],
                ligand_members=[atom(index) for index in ligand_ring],
                centroid_distance=dict(
                    value=float(centroid_distances[i, j]), unit="nm"
                ),
            )
            for i, receptor_ring in enumerate(ring_receptor)
            for j, ligand_ring in enumerate(ring_ligand)
        ],
        key=lambda pair: pair["centroid_distance"]["value"],
    )
    pi_pi = [
        comparison(policy, msm.interactions.pi_pi.get_pi_pi_interactions, {})
        for policy in declaration["pi_sensitivity"]
    ]
    np.testing.assert_equal(
        before_state,
        msm.convert(
            system.chemical_states, to_form="molsysmt.ChemicalStatesDict"
        ).to_dict(),
    )
    np.testing.assert_array_equal(
        before_xyz, puw.get_value(msm.get(system, coordinates=True), to_unit="nm")
    )
    np.testing.assert_equal(
        before_atoms,
        msm.get(
            system,
            element="atom",
            atom_name=True,
            group_name=True,
            group_id=True,
            chain_id=True,
            output_type="dictionary",
        ),
    )
    unchanged = source_before == _fingerprint(case["source"]) and original_analyses == {
        name: portable(msm.convert(analysis, to_form="molsysmt.InteractionsDict").data)
        for name, analysis in case["analyses"].items()
    }
    return portable(
        dict(
            schema="pharmacophoremt.eralpha_interaction_diagnosis@1",
            declaration=declaration,
            preparation=case["report"],
            hbond_sites=sites,
            hbond_candidates=candidates,
            hbond_comparisons=hbonds,
            aromatic_recognition=matches,
            n_smarts_rings=len(rings),
            diagnostic_planes={
                key: puw.QuantityRecord.from_quantity(value).to_dict()
                if key in {"centers", "rms_deviation", "max_deviation"}
                else value
                for key, value in planes.items()
            },
            diagnostic_plane_method="unweighted_orthogonal_least_squares_not_reference_planes",
            ring_pairs=ring_pairs,
            pi_comparisons=pi_pi,
            unavailable_rejected_reference_geometry=dict(
                fields=[
                    "reference_plane_angles",
                    "reference_normal_angles",
                    "reference_intersection_distance",
                ],
                provider_issue=declaration["rejected_geometry_issue"],
                independent_oracle="tests/test_eralpha_interaction_diagnostics.py::test_reference_intersection_rejects_frozen_phe404_pair",
            ),
            original_input_and_cached_analyses_unchanged=unchanged,
            biological_validation="not_performed",
            environmental_refinement="not_performed",
        )
    )


def valid(run):
    """Check the predeclared case outcomes, without choosing a winning profile."""
    declaration = run["declaration"]
    triplets = [
        [row[key]["prepared_index"] for key in ("donor", "hydrogen", "acceptor")]
        for row in run["hbond_candidates"]
    ]
    return (
        run["original_input_and_cached_analyses_unchanged"]
        and triplets == declaration["expected_near_hbond_triplets"]
        and run["n_smarts_rings"] == declaration["expected_smarts_ring_count"]
        and all(
            row["n_interactions"] == row["declaration"]["expected_count"]
            for row in run["hbond_comparisons"] + run["pi_comparisons"]
        )
    )


def main(argv=None):
    import ackredit
    import molsysmt as msm
    import pyunitwizard

    import pharmacophoremt as phmt

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    packages = dict(
        pharmacophoremt=phmt, molsysmt=msm, pyunitwizard=pyunitwizard, ackredit=ackredit
    )
    before = {name: _source_record(package) for name, package in packages.items()}
    paths = [DIAGNOSTICS, MANIFEST] + [
        ROOT / name
        for name in (
            "devtools/diagnose_eralpha_interface.py",
            "devtools/prepare_eralpha_interface.py",
            "devtools/prepare_eralpha_ligand.py",
            "devtools/prepare_eralpha_hydrogens.py",
            "devtools/audit_eralpha_receptor.py",
            "devtools/prepared_ccd_ligands.py",
            "devtools/validate_eralpha_template.py",
            "devtools/validate_prepared_ccd_ligands.py",
            "devtools/benchmark_rigid_consensus.py",
            "tests/data/eralpha_rcsb/1qku.cif",
            "tests/data/eralpha_rcsb/EST.cif",
            "tests/data/eralpha_rcsb/manifest.json",
            "tests/data/eralpha_template/est_template.h5msm",
            "tests/data/eralpha_template/manifest.json",
            "tests/data/eralpha_template/acquisition.json",
        )
    ]

    def hashes():
        return {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in paths
        }

    inputs, runs = hashes(), []
    for enabled in (False, True):
        with (
            ackredit.session("ERalpha interaction diagnosis"),
            phmt.attribution(enabled),
        ):
            with ackredit.capture(
                "fixed candidate and criterion comparisons"
            ) as capture:
                run = diagnose(prepare_interface())
                if enabled:
                    credit_inputs()
            run["attribution"] = capture.attribution.to_dict()
        run["tracking"] = enabled
        run["valid"] = valid(run)
        run["scientific_sha256"] = hashlib.sha256(
            json.dumps(
                scientific_projection(
                    {
                        key: value
                        for key, value in run.items()
                        if key not in {"tracking", "valid"}
                    }
                ),
                sort_keys=True,
            ).encode()
        ).hexdigest()
        runs.append(run)
        print(
            "PASS" if run["valid"] else "FAIL",
            "diagnostic comparisons",
            "tracking=",
            enabled,
            flush=True,
        )
    unchanged = (
        before == {name: _source_record(package) for name, package in packages.items()}
        and inputs == hashes()
    )
    accepted = (
        unchanged
        and all(run["valid"] for run in runs)
        and runs[0]["scientific_sha256"] == runs[1]["scientific_sha256"]
    )
    report = dict(
        schema="pharmacophoremt.eralpha_interaction_diagnostic_validation@1",
        recorded_utc=datetime.now(timezone.utc).isoformat(),
        python=platform.python_version(),
        executable=sys.executable,
        platform=platform.platform(),
        producers=before,
        inputs=inputs,
        producers_and_inputs_unchanged=unchanged,
        versions={
            name: importlib.metadata.version(name)
            for name in (
                "numpy",
                "scipy",
                "rdkit",
                "argdigest",
                "depdigest",
                "smonitor",
            )
        },
        molecular_extensions=[
            dict(
                module=name,
                path=module.__file__,
                sha256=hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest(),
            )
            for name, module in sorted(sys.modules.items())
            if name.startswith("molsysmt")
            and getattr(module, "__file__", None)
            and Path(module.__file__).suffix in {".so", ".pyd", ".dylib"}
        ],
        runs=runs,
        valid=accepted,
        scope="fixed diagnostic comparisons; no refinement, profile optimization or biological acceptance",
    )
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
