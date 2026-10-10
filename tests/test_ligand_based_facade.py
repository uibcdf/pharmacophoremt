"""Public facade controls for explicit native prepared-ligand consensus."""

import molsysmt as msm
import numpy as np
import pytest

import pharmacophoremt as phmt
from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler import LigandBasedModeler
from tests.test_pose_evaluation import system
from tests.test_rigid_search import COORDINATES, FAMILIES, SMILES, moved


def test_old_implicit_method_is_refused_even_when_digestion_is_skipped():
    for skip in (False, True):
        with pytest.raises(ArgumentError) as error:
            LigandBasedModeler([object(), object()], skip_digestion=skip)
        assert error.value.extra["argument"] == "consensus_method"


@pytest.mark.parametrize("method", ["legacy", "rdp", "", None, [], True])
def test_invalid_or_unspecified_consensus_method_is_not_a_fallback(method):
    with pytest.raises(ArgumentError) as error:
        LigandBasedModeler([object(), object()], consensus_method=method)
    assert error.value.extra["argument"] == "consensus_method"


def test_dispatcher_routes_ligand_collection_before_single_system_conversion(
    monkeypatch,
):
    import molsysmt as msm

    import pharmacophoremt.modeler.ligand_based as owner

    received = []
    result = [object()]

    class Consumer:
        def __init__(self, molecular_systems, **kwargs):
            received.append((molecular_systems, kwargs))

        def build(self):
            return result

    def forbidden(*args, **kwargs):
        pytest.fail("Ligand collection dispatcher must not convert or unwrap inputs")

    monkeypatch.setattr(owner, "LigandBasedModeler", Consumer)
    monkeypatch.setattr(msm, "convert", forbidden)
    systems = (item for item in [object(), object()])
    assert (
        phmt.model(systems, method="ligand-based", consensus_method="rigid") is result
    )
    assert received == [(systems, {"consensus_method": "rigid"})]
    for options in ({"ligand_selection": "all"}, {"receptor_selection": "all"}):
        with pytest.raises(ArgumentError):
            phmt.model(
                systems, method="ligand-based", consensus_method="rigid", **options
            )


@pytest.mark.parametrize(
    "options",
    [
        {"n_points": True},
        {"n_points": 0},
        {"min_actives": 0},
        {"min_actives": True},
        {"n_conformers": 10},
        {"conformer_rmsd_threshold": 0.2},
        {"min_sites": 4},
        {"min_support": 2},
    ],
)
def test_invalid_or_ambiguous_legacy_parameters_are_refused(options):
    with pytest.raises(ArgumentError):
        LigandBasedModeler(
            [object(), object()], consensus_method="aligned_cliques", **options
        )


def test_same_raw_object_cannot_inflate_distinct_ligand_support():
    source = object()
    with pytest.raises(ArgumentError) as error:
        LigandBasedModeler([source, source], consensus_method="aligned_cliques")
    assert error.value.extra["argument"] == "molecular_systems"


def test_duplicate_ligand_ids_cannot_turn_conformers_into_independent_ligands():
    records = [
        {"ligand_id": "a", "molecular_system": object(), "structure_index": i}
        for i in (0, 1)
    ]
    with pytest.raises(ArgumentError):
        LigandBasedModeler(records, consensus_method="rigid")


def test_legacy_audit_remains_reproducible_without_a_public_legacy_builder():
    from devtools.audit_legacy_cliques import audit

    observed = audit()
    assert observed == {
        "compatible_pair_rmsd": 0.1,
        "compatible_pair_surviving_boxes": 0,
        "duplicated_entries": 4,
        "unique_candidate_identities": 2,
        "unsupported_maximal_cliques": 1,
        "reordered_identical_pattern_vector_equal": False,
        "reflection_vector_equal": True,
    }
    assert not hasattr(LigandBasedModeler, "_recursive_partitioning")


def test_aligned_prepared_generator_retains_all_joint_sites_and_original_sources():
    first = system(SMILES, COORDINATES)
    second = system(SMILES, COORDINATES + [0.01, 0, 0])
    sources = [first, second]
    before = [
        puw.get_value(msm.get(s, coordinates=True), to_unit="nm").copy()
        for s in sources
    ]
    modeler = LigandBasedModeler(
        iter(sources),
        n_points=3,
        consensus_method="aligned_cliques",
        features=FAMILIES,
        distance_tolerance=".02 nm",
    )
    assert modeler.result is modeler.report is None
    models = modeler.build()
    assert (
        models is modeler.result["models"]
        and modeler.report is modeler.result["report"]
    )
    assert modeler.result["complete"] and len(models) == 1
    assert (
        models[0].n_interaction_sites == 5
    )  # n_points is a minimum in the native method.
    assert models[0].score is None
    assert models[0].metadata["hypothesis"]["joint_ligand_ids"] == [
        "ligand-0",
        "ligand-1",
    ]
    assert models[0].metadata["hypothesis"]["joint_support_fraction"] == 1
    for source, original in zip(sources, before, strict=True):
        np.testing.assert_array_equal(
            puw.get_value(msm.get(source, coordinates=True), to_unit="nm"), original
        )


def test_rigid_facade_and_dispatcher_preserve_public_provider_fit_and_hypotheses(
    monkeypatch,
):
    source = system(SMILES, COORDINATES)
    displaced = moved(source)
    records = [
        {"ligand_id": "a", "molecular_system": source},
        {"ligand_id": "b", "molecular_system": displaced},
    ]
    calls = []
    provider = msm.structure.least_rmsd_fit

    def observed(*args, **kwargs):
        calls.append(kwargs)
        return provider(*args, **kwargs)

    monkeypatch.setattr(msm.structure, "least_rmsd_fit", observed)
    modeler = LigandBasedModeler(
        records,
        n_points=5,
        consensus_method="rigid",
        features=FAMILIES,
        min_matches=5,
        distance_tolerance=".02 nm",
    )
    models = modeler.build()
    assert calls and len(models) == 1
    assert modeler.report["n_fits"] == len(calls)
    assert models[0].metadata["hypothesis"]["joint_ligand_ids"] == ["a", "b"]
    assert (
        models[0].metadata["placements"][1]["alignment"]["provider"]
        == "molsysmt.structure.least_rmsd_fit"
    )
    dispatched = phmt.model(
        records,
        method="ligand-based",
        n_points=5,
        consensus_method="rigid",
        features=FAMILIES,
        min_matches=5,
        distance_tolerance=".02 nm",
    )
    assert len(dispatched) == 1 and dispatched[0].n_interaction_sites == 5
    np.testing.assert_allclose(
        puw.get_value(msm.get(displaced, coordinates=True), to_unit="nm")[0],
        COORDINATES @ np.array([[0.0, -1, 0], [1, 0, 0], [0, 0, 1]]).T + [2.0, 1, 3],
        atol=1e-12,
    )


def test_reflected_rigid_input_is_evaluated_empty_without_a_dummy_model():
    records = [
        {"ligand_id": "a", "molecular_system": system(SMILES, COORDINATES)},
        {
            "ligand_id": "mirror",
            "molecular_system": system(SMILES, COORDINATES * [1, 1, -1]),
        },
    ]
    modeler = LigandBasedModeler(
        records,
        n_points=5,
        consensus_method="rigid",
        features=FAMILIES,
        min_matches=5,
        distance_tolerance=".02 nm",
    )
    assert modeler.build() == []
    assert modeler.result["complete"] is True
    assert modeler.report["source_alignments"][1]["status"] == "unplaced"
    assert modeler.report["source_alignments"][1]["rejected_placements"]


def test_failed_rebuild_does_not_leave_a_success_report_or_swallow_provider_failure(
    monkeypatch,
):
    from pharmacophoremt._private.smonitor.exceptions import CliqueLimitError

    source = system(SMILES, COORDINATES)
    modeler = LigandBasedModeler(
        [source, moved(source)],
        n_points=5,
        consensus_method="rigid",
        features=FAMILIES,
        min_matches=5,
        distance_tolerance=".02 nm",
    )
    assert modeler.build()
    modeler.native_options["max_graph_nodes"] = 1
    with pytest.raises(CliqueLimitError):
        modeler.build()
    assert modeler.result is modeler.report is None
    modeler.native_options.pop("max_graph_nodes")

    def failed(*args, **kwargs):
        raise RuntimeError("public provider failure")

    monkeypatch.setattr(msm.structure, "least_rmsd_fit", failed)
    with pytest.raises(RuntimeError, match="public provider failure"):
        modeler.build()
    assert modeler.result is modeler.report is None


def test_screening_also_refuses_local_conformer_generation():
    from pharmacophoremt import Pharmacophore
    from pharmacophoremt.screening.virtual_screening import VirtualScreening

    with pytest.raises(ArgumentError, match="MolSysMT"):
        VirtualScreening(Pharmacophore(), screening_method="placed", n_conformers=7)


def test_aligned_method_does_not_fit_unaligned_sources(monkeypatch):
    source = system(SMILES, COORDINATES)
    displaced = moved(source)

    def forbidden(*args, **kwargs):
        pytest.fail("Aligned consensus must consume the declared common frame")

    monkeypatch.setattr(msm.structure, "least_rmsd_fit", forbidden)
    modeler = LigandBasedModeler(
        [source, displaced],
        consensus_method="aligned_cliques",
        n_points=5,
        features=FAMILIES,
        distance_tolerance=".02 nm",
    )
    assert modeler.build() == []
    assert modeler.result["complete"] is True


def test_empty_feature_ligand_counts_in_default_support_and_denominator():
    sources = [
        system(SMILES, COORDINATES),
        system(SMILES, COORDINATES + [0.01, 0, 0]),
        system("[Na+]", [[6, 6, 6]]),
    ]
    options = dict(
        consensus_method="aligned_cliques",
        features=FAMILIES,
        distance_tolerance=".02 nm",
    )
    all_inputs = LigandBasedModeler(sources, **options)
    assert all_inputs.build() == []
    subset = LigandBasedModeler(sources, min_actives=2, **options)
    model = subset.build()[0]
    assert model.metadata["hypothesis"]["joint_support_fraction"] == pytest.approx(
        2 / 3
    )
    assert model.metadata["hypothesis"]["joint_ligand_ids"] == ["ligand-0", "ligand-1"]


def test_explicit_frame_selection_units_and_native_attribution_roundtrip(tmp_path):
    import ackredit

    from pharmacophoremt.io.phmt import load_json, to_json

    coordinates = np.vstack((COORDINATES, [[4, 5, 6]]))
    first = system(SMILES + ".[Na+]", coordinates)
    first.structures.append(
        coordinates=puw.quantity([coordinates + [0.03, 0, 0]], "nm")
    )
    second = system(SMILES + ".[Na+]", coordinates)
    records = [
        dict(
            ligand_id="a",
            molecular_system=first,
            structure_index=1,
            selection=list(range(8)),
            chemical_state="reference",
        ),
        dict(
            ligand_id="b",
            molecular_system=second,
            structure_index=0,
            selection=list(range(8)),
            chemical_state="reference",
        ),
    ]
    with puw.context(standard_units=["angstrom", "ps", "degrees"]):
        with ackredit.session("facade"), phmt.attribution():
            modeler = LigandBasedModeler(
                records,
                consensus_method="aligned_cliques",
                features=FAMILIES,
                distance_tolerance=".04 nm",
                radius=".05 nm",
            )
            model = modeler.build()[0]
        assert modeler.result["attribution"]["status"] == "captured"
        assert [item["structure_index"] for item in model.metadata["sources"]] == [1, 0]
        assert all(
            item["selected_atom_indices"] == list(range(8))
            for item in model.metadata["sources"]
        )
        path = tmp_path / "facade.json"
        to_json(model, path)
        loaded = load_json(path)
        assert loaded.metadata == model.metadata
        for original, restored in zip(
            model.interaction_sites, loaded.interaction_sites, strict=True
        ):
            np.testing.assert_allclose(
                puw.get_value(restored.center, to_unit="nm"),
                puw.get_value(original.center, to_unit="nm"),
                atol=1e-14,
            )
            assert puw.get_value(restored.radius, to_unit="nm") == pytest.approx(0.05)
    bibliography = phmt.attribution_report(
        loaded.metadata["attribution"], format="bibtex"
    )
    assert "10.1145/362342.362367" in bibliography
    assert "10.1021/ci7000583" not in bibliography  # Retired RDP was not executed.
