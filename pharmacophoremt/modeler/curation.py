"""Reusable selection, independent copying and explicit constraint curation."""

from copy import deepcopy

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._ackredit import attributed, credit_software
from pharmacophoremt._private.arg_digestion import curation as contracts
from pharmacophoremt._private.molsysmt import detached
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt._version import __version__
from pharmacophoremt.io.phmt import _to_dict
from pharmacophoremt.pharmacophore import Pharmacophore

METHOD = "explicit_pharmacophore_curation@1"
_DIGEST = dict(
    digestion_source="pharmacophoremt._private.arg_digestion.curation",
    digestion_style="registry",
)


@signal(tags=["modeling", "curation", "selection"])
@arg_digest(**_DIGEST)
def get_interaction_site_indices(
    pharmacophore, *, site_indices="all", feature_names=None, shape_names=None
):
    """Select cached site indices in requested order, without molecular access.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        Native hypothesis, unchanged.
    site_indices : 'all', int or sequence of int, default='all'
        Unique nonnegative local site indices. An explicit empty sequence is valid.
        These are model indices, not MolSysMT molecular selections.
    feature_names, shape_names : str or sequence of str, optional
        Exact cached names. Any selected feature may match; feature and shape
        filters combine with AND. Unknown names raise instead of hiding a typo.

    Returns
    -------
    list of int
        Independent indices, possibly empty. No sorting or geometry clustering.

    Examples
    --------
    >>> donors = get_interaction_site_indices(query, feature_names='hb donor')
    """
    model = contracts.model(pharmacophore)
    selected = contracts.indices(site_indices)
    selected = list(range(model.n_interaction_sites)) if selected == "all" else selected
    if any(index >= model.n_interaction_sites for index in selected):
        raise ArgumentError(
            argument="site_indices", reason="site index outside the model"
        )
    features, shapes = contracts.names(feature_names), contracts.names(shape_names)
    from pharmacophoremt.data.smarts import FEAT_TO_CHAR

    known_shapes = {
        "point",
        "sphere",
        "sphere and vector",
        "disk",
        "cylinder",
        "gaussian kernel",
        "shapelet",
    }
    known_shapes.update(site.shape_name for site in model.interaction_sites)
    known_features = set(FEAT_TO_CHAR)
    known_features.update(
        feature for site in model.interaction_sites for feature in site.features
    )
    if not set(features) <= known_features or not set(shapes) <= known_shapes:
        raise ArgumentError(
            argument="feature_names/shape_names",
            reason="unknown cached feature or shape name",
        )
    return [
        index
        for index in selected
        if (
            not features
            or set(features).intersection(model.interaction_sites[index].features)
        )
        and (not shapes or model.interaction_sites[index].shape_name in shapes)
    ]


@signal(tags=["modeling", "curation", "copy"])
@arg_digest(**_DIGEST)
def copy_pharmacophore(pharmacophore, *, name=None):
    """Copy all native sites, geometry and metadata independently.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        Cached model. The linked molecular system stays the same reference; it
        is neither copied nor queried. Use MolSysMT to copy molecular systems.
    name : str, optional
        Override the copied name; None preserves it.

    Returns
    -------
    Pharmacophore
        Independent sites, quantities, feature lists and nested metadata. Scores,
        reference fields and original bibliography remain unchanged. Pure copying
        neither credits a new calculation nor changes the hypothesis provenance.

    Examples
    --------
    >>> variant = copy_pharmacophore(query, name='alternative')
    """
    source = contracts.model(pharmacophore)
    name = contracts.text(name)
    result = Pharmacophore(
        name=source.name if name is None else name,
        description=source.description,
        molecular_system=source.molecular_system,
        score=source.score,
        ref_mol=source.ref_mol,
        ref_struct=source.ref_struct,
    )
    result.metadata = deepcopy(source.metadata)
    for site in source.interaction_sites:
        result.add_interaction_site(deepcopy(site))
    return result


def _history(source, operation, site_map, parameters, reason, changes):
    return dict(
        method=METHOD,
        producer=dict(pharmacophoremt=__version__),
        operation=operation,
        policy="caller_declared_no_automatic_fit_or_weighting",
        reason=contracts.text(reason),
        parameters=detached(parameters),
        source_model=detached(_to_dict(source)),
        site_map=site_map,
        changes=changes,
        score_policy="invalidated_source_score_retained_in_snapshot",
    )


@signal(tags=["modeling", "curation", "extract"])
@arg_digest(**_DIGEST)
def extract_pharmacophore(pharmacophore, *, site_indices="all", name=None, reason=None):
    """Make an independent subset with explicit source-to-output correspondence.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        Native-serializable cached hypothesis, unchanged.
    site_indices : 'all', int or sequence of int, default='all'
        Unique local site indices in output order, obtainable with
        get_interaction_site_indices(). Empty extraction remains an empty model.
    name, reason : str, optional
        Output name and caller's explanation for the selection.

    Returns
    -------
    Pharmacophore
        Independent selected sites; original complete native model snapshot,
        observations/bibliography and site mapping in metadata. The score is None
        until reevaluated. Extraction does not align, deduplicate or rerun detection.

    Examples
    --------
    >>> subset = extract_pharmacophore(query, site_indices=[2, 0])
    """
    selected = get_interaction_site_indices(pharmacophore, site_indices=site_indices)
    result = copy_pharmacophore(pharmacophore, name=name)
    result.interaction_sites = [result.interaction_sites[index] for index in selected]
    result.n_interaction_sites = len(selected)
    result.score = None
    result.metadata = _history(
        pharmacophore,
        "extract_sites",
        [
            dict(source_site_index=original, site_index=index)
            for index, original in enumerate(selected)
        ],
        dict(site_indices=selected),
        reason,
        [],
    )
    return result


@signal(tags=["modeling", "curation", "edit"])
@arg_digest(**_DIGEST)
@attributed()
def edit_pharmacophore(
    pharmacophore,
    *,
    site_indices="all",
    essential=None,
    weight=None,
    radius=None,
    sigma=None,
    name=None,
    reason=None,
    in_place=False,
    skip_digestion=False,
):
    """Apply explicit constraints after validating the entire edit.

    Parameters
    ----------
    pharmacophore : Pharmacophore
        Native-serializable cached model. Molecular data is never accessed.
    site_indices : 'all', int or sequence of int, default='all'
        Nonempty unique target indices; untargeted sites remain in the result.
    essential : bool, optional
        New obligatory flag. None leaves it unchanged.
    weight : finite nonnegative real, optional
        New independent site weight. Zero does not remove essential or exclusion
        semantics; use extraction to remove a constraint.
    radius : positive length quantity, optional
        Actual radius of Sphere, SphereAndVector, Disk or Cylinder. No bare units.
    sigma : positive length quantity, optional
        GaussianKernel width, distinct from a radius. A mixed incompatible target
        set raises without modifying any site. At least one edit field is required.
    name, reason : str, optional
        Variant name and caller explanation.
    in_place : bool, default=False
        Return an independent variant, or commit to the original model after all
        validation. Existing native site identities remain when editing in place.
    skip_digestion : bool, default=False
        Skip optional argument preprocessing. Scientific validation and atomic
        rejection of incompatible edits still apply.

    Returns
    -------
    Pharmacophore
        Edited model with score None, original full model snapshot, local mapping
        and before/after values. Source observations and bibliography are retained.
        Optional capture records actual host/quantity work, not another detection.

    Notes
    -----
    This edits hypothesis constraints, not molecular coordinates or the rigid
    correspondence refinement algorithm. Curation provenance is a distinct root;
    compose curated models using generic keep. Bounded native participant reuse
    should precede curation. Pure copy/extraction preserve citations without a new
    scientific attribution boundary. No paper is assigned to caller choices.

    Examples
    --------
    >>> variant = edit_pharmacophore(query, site_indices=[0], weight=2.0,
    ...                             reason='declared anchor preference')
    """
    selected = get_interaction_site_indices(pharmacophore, site_indices=site_indices)
    in_place = contracts._contracts.digest_essential(in_place)
    edits = dict(
        essential=contracts.optional_essential(essential),
        weight=contracts.optional_weight(weight),
        radius=contracts.optional_radius(radius),
        sigma=contracts.optional_sigma(sigma),
    )
    edits = {key: value for key, value in edits.items() if value is not None}
    if not selected or not edits:
        raise ArgumentError(
            argument="site_indices/edits",
            reason="require targets and at least one explicit edit",
        )
    result = copy_pharmacophore(pharmacophore, name=name)
    from pharmacophoremt.interaction_site.shape import (
        Cylinder,
        Disk,
        GaussianKernel,
        Sphere,
        SphereAndVector,
    )

    radius_shapes = (Sphere, SphereAndVector, Disk, Cylinder)
    changes = []
    for index in selected:
        site = result.interaction_sites[index]
        values = {}
        for field, value in edits.items():
            if field in {"radius", "sigma"}:
                supported = radius_shapes if field == "radius" else (GaussianKernel,)
                if not isinstance(site.shape, supported):
                    raise ArgumentError(
                        argument=field,
                        reason=f"{site.shape_name} does not have an editable {field}",
                    )
                owner = site.shape
            else:
                owner = site
            before = detached(getattr(owner, field))
            setattr(owner, field, deepcopy(value))
            values[field] = dict(before=before, after=detached(getattr(owner, field)))
        changes.append(dict(source_site_index=index, site_index=index, fields=values))
    result.metadata = _history(
        pharmacophore,
        "edit_constraints",
        [
            dict(source_site_index=index, site_index=index)
            for index in range(result.n_interaction_sites)
        ],
        dict(site_indices=selected, **edits),
        reason,
        changes,
    )
    result.score = None
    if "radius" in edits or "sigma" in edits:
        credit_software("pyunitwizard", __name__ + ".edit_pharmacophore")
    if in_place:
        for index in selected:
            original, updated = (
                pharmacophore.interaction_sites[index],
                result.interaction_sites[index],
            )
            if "radius" in edits or "sigma" in edits:
                original.shape = updated.shape
            if "essential" in edits:
                original.essential = updated.essential
            if "weight" in edits:
                original.weight = updated.weight
        pharmacophore.name = result.name
        pharmacophore.metadata = result.metadata
        pharmacophore.score = None
        return pharmacophore
    return result
