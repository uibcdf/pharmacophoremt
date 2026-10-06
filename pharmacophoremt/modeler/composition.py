"""Independent common-frame hypothesis composition with labeled contributions."""

from copy import deepcopy

import numpy as np
from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt import pyunitwizard as puw
from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.arg_digestion.argument.duplicate_policy import (
    digest_duplicate_policy,
)
from pharmacophoremt._private.arg_digestion.argument.pharmacophores import (
    digest_pharmacophores,
)
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt._version import __version__
from pharmacophoremt.pharmacophore import Pharmacophore

METHOD = "common_frame_pharmacophore_composition@1"
_ATOL = 1e-12  # Representation equality in nm/dimensionless, not a merge radius.
_SOURCE_FIELDS = (
    "source_id",
    "source_atom_indices",
    "source_structure_indices",
    "structure_index",
    "ligand_atom_indices",
)


def _native_context(model):
    metadata = model.metadata
    if metadata.get("method") != "observed_interactions" or any(
        field not in metadata for field in _SOURCE_FIELDS
    ):
        raise ArgumentError(
            argument="duplicate_policy",
            reason="same_participant requires native observed-interaction source declarations",
        )
    if model.ref_struct != metadata["structure_index"]:
        raise ArgumentError(
            argument="pharmacophores",
            reason="native reference frame declaration differs",
        )
    state = metadata.get("parameters", {}).get("chemical_state_index")
    if (
        isinstance(state, (bool, np.bool_))
        or not isinstance(state, (int, np.integer))
        or state < 0
    ):
        raise ArgumentError(
            argument="pharmacophores",
            reason="require one explicitly declared chemical state",
        )
    return dict(
        **{field: detached(metadata[field]) for field in _SOURCE_FIELDS},
        chemical_state_index=int(state),
    )


def _participant(site, model):
    metadata = site.metadata
    atoms = metadata.get("atom_indices")
    source_atoms = metadata.get("source_atom_indices")
    if (
        len(site.features) != 1
        or not isinstance(atoms, list)
        or not atoms
        or not isinstance(source_atoms, list)
        or len(atoms) != len(source_atoms)
        or len(set(atoms)) != len(atoms)
        or any(
            isinstance(atom, bool) or not isinstance(atom, int) or atom < 0
            for atom in atoms
        )
        or any(atom >= len(model.metadata["source_atom_indices"]) for atom in atoms)
        or metadata.get("structure_index") != model.metadata["structure_index"]
        or source_atoms
        != [model.metadata["source_atom_indices"][atom] for atom in atoms]
        or not isinstance(metadata.get("observations"), list)
    ):
        raise ArgumentError(
            argument="pharmacophores",
            reason="require complete native participant correspondence",
        )
    return site.feature_name, tuple(sorted(atoms))


def _values(value, unit, shape):
    try:
        array = np.asarray(puw.get_value(value, to_unit=unit), dtype=float)
    except Exception as error:
        raise ArgumentError(
            argument="pharmacophores", reason="invalid site quantity"
        ) from error
    if array.shape != shape or not np.isfinite(array).all():
        raise ArgumentError(
            argument="pharmacophores", reason="require finite native site geometry"
        )
    return array


def _constraint(site):
    if site.shape_name not in {"sphere", "disk", "sphere and vector"}:
        raise ArgumentError(
            argument="duplicate_policy", reason="unsupported native participant shape"
        )
    if (
        not isinstance(site.essential, (bool, np.bool_))
        or not np.isscalar(site.weight)
        or isinstance(site.weight, (bool, np.bool_))
    ):
        raise ArgumentError(
            argument="pharmacophores", reason="invalid essential flag/weight"
        )
    weight = float(site.weight)
    radius = _values(site.radius, "nm", ())
    if not np.isfinite(weight) or weight < 0 or radius <= 0:
        raise ArgumentError(
            argument="pharmacophores", reason="invalid positive-site weight/radius"
        )
    vector = None
    if site.shape_name in {"disk", "sphere and vector"}:
        vector = _values(
            site.shape.normal if site.shape_name == "disk" else site.direction,
            "dimensionless",
            (3,),
        )
        norm = np.linalg.norm(vector)
        if norm == 0:
            raise ArgumentError(
                argument="pharmacophores", reason="site orientation must be nonzero"
            )
        vector = vector / norm
    return dict(
        shape=site.shape_name,
        center=_values(site.center, "nm", (3,)),
        radius=radius,
        vector=vector,
        essential=bool(site.essential),
        weight=weight,
        geometry_atoms=sorted(
            site.metadata.get("geometry_atom_indices", site.metadata["atom_indices"])
        ),
        charge=None
        if site.metadata.get("charge") is None
        else float(
            puw.get_value(
                puw.QuantityRecord.from_dict(site.metadata["charge"]).to_quantity(
                    unit="e"
                ),
                to_unit="e",
            )
        ),
    )


def _equal(first, second):
    if any(
        first[key] != second[key]
        for key in ("shape", "essential", "weight", "geometry_atoms", "charge")
    ):
        return False
    if not all(
        np.allclose(first[key], second[key], rtol=0, atol=_ATOL)
        for key in ("center", "radius")
    ):
        return False
    if first["vector"] is None:
        return True
    return np.allclose(first["vector"], second["vector"], rtol=0, atol=_ATOL) or (
        first["shape"] == "disk"
        and np.allclose(first["vector"], -second["vector"], rtol=0, atol=_ATOL)
    )


@signal(tags=["modeling", "composition"])
@arg_digest()
@attributed("numpy", "pyunitwizard")
def compose_pharmacophores(pharmacophores, *, duplicate_policy="keep", name=None):
    """Compose named hypotheses declared in one coordinate frame.

    Parameters
    ----------
    pharmacophores : mapping of str to Pharmacophore
        Named components in insertion order. Empty components retain provenance.
        Coordinate alignment/origin is a caller declaration; no molecular access
        occurs. Conflicting declared reference frames are refused.
    duplicate_policy : {'keep', 'same_participant'}, default='keep'
        Keep each constraint independently, or reuse compatible participants of
        native observed-interaction queries with identical source axes, ligand,
        frame and explicit state. Reuse does not add weights or average geometry.
        Conflicting constraints for the same participant raise. Equality uses
        1e-12 nm/dimensionless representation tolerance; disk normal sign is free.
    name : str, optional
        Output name. Input names/descriptions/scores remain component provenance.

    Returns
    -------
    Pharmacophore
        Independent sites/metadata and component-to-output site correspondence.
        Observations carry component labels: native relation/occurrence indices
        are local to their original analysis. Cached citations remain evidence,
        without crediting detection or recognition again. An all-empty composition
        remains empty and is not a valid PoseEvaluator query.

    Notes
    -----
    This constructs a joint hypothesis, not a consensus or logical alternative.
    `keep` can intentionally produce competing constraints. `same_participant`
    is bounded to native observed-interaction components; generic spatial or
    fused-ring clustering and automatic alignment are separate future strategies.
    Source declarations cannot authenticate molecular origin. Use MolSysMT for
    any molecular transformations. Saved components may be composed without the
    original molecular object or Ackredit. This is separate from legacy `merge`.
    """
    components = digest_pharmacophores(pharmacophores)
    duplicate_policy = digest_duplicate_policy(duplicate_policy)
    frames = {
        model.ref_struct
        for model in components.values()
        if model.ref_struct is not None
    }
    if len(frames) > 1:
        raise ArgumentError(
            argument="pharmacophores", reason="component reference frames differ"
        )
    context = None
    if duplicate_policy == "same_participant":
        contexts = [_native_context(model) for model in components.values()]
        context = contexts[0]
        if any(item != context for item in contexts[1:]):
            raise ArgumentError(
                argument="pharmacophores",
                reason="component source axes/ligand/frame/state differ",
            )
    first = next(iter(components.values()))
    result = Pharmacophore(
        name=name,
        molecular_system=first.molecular_system,
        ref_struct=next(iter(frames)) if frames else None,
    )
    result.metadata = dict(
        method=METHOD,
        producer=dict(pharmacophoremt=__version__),
        policy=dict(
            duplicate_policy=duplicate_policy,
            common_frame="caller_declared",
            weight_aggregation="not_performed",
            geometry_averaging=False,
            representation_atol_nm=_ATOL,
            representation_atol_dimensionless=_ATOL,
        ),
        source_context=context,
        components=[],
        site_map=[],
    )
    seen = {}
    for label, model in components.items():
        result.metadata["components"].append(
            detached(
                dict(
                    label=label,
                    name=model.name,
                    description=model.description,
                    score=model.score,
                    ref_mol=model.ref_mol,
                    ref_struct=model.ref_struct,
                    metadata=model.metadata,
                    n_sites=model.n_interaction_sites,
                )
            )
        )
        for local_index, original in enumerate(model.interaction_sites):
            key = constraint = None
            if duplicate_policy == "same_participant":
                key, constraint = _participant(original, model), _constraint(original)
            reused = key is not None and key in seen
            if reused:
                index, previous = seen[key]
                if not _equal(previous, constraint):
                    raise ArgumentError(
                        argument="duplicate_policy",
                        reason="same participant has conflicting constraints; choose keep or revise the hypothesis",
                    )
                site = result.interaction_sites[index]
            else:
                index = result.n_interaction_sites
                site = deepcopy(original)
                site.metadata = detached(original.metadata)
                site.metadata["composition_contributions"] = []
                if "observations" in site.metadata:
                    site.metadata["observations"] = []
                result.add_interaction_site(site)
                if key is not None:
                    seen[key] = index, constraint
            site.metadata["composition_contributions"].append(
                dict(
                    component=label,
                    component_site_index=local_index,
                    metadata=detached(original.metadata),
                )
            )
            if "observations" in original.metadata:
                site.metadata["observations"].extend(
                    dict(detached(observation), component=label)
                    for observation in original.metadata["observations"]
                )
            result.metadata["site_map"].append(
                dict(
                    component=label,
                    component_site_index=local_index,
                    site_index=index,
                    action="reused" if reused else "added",
                )
            )
    return result
