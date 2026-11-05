"""Compatibility facade for explicit cached receptor hypotheses."""

from numbers import Integral

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._ackredit import attributed
from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_feature_inventory,
    digest_projection_specs,
    digest_structure_index,
    digest_structure_indices,
)
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler.excluded_volumes import (
    _attach_receptor_exclusions,
    _receptor_exclusions,
)
from pharmacophoremt.modeler.modeler import Modeler
from pharmacophoremt.modeler.receptor_projections import from_receptor_projections


class StructureBasedModeler(Modeler):
    """Compose explicit projections and optional cached heavy-atom exclusions.

    The unchanged prepared molecular_system is retained as a reference; no
    molecular operation occurs in this facade. Feature inventories and projection
    decisions are explicit. Select/prepare the receptor through MolSysMT first;
    actual pocket identification belongs to TopoMT. Old SMARTS, spherical pocket
    selection, first-neighbor/+z inference and fixed projection rules are retired.

    Optional excluded_volume_inventory must declare the same atom selection,
    structure_index and chemical_state as feature_inventory, and requires an
    explicit excluded_volume_radius. Source identity and coordinate consistency
    remain caller responsibilities; comparing declarations does not authenticate
    cached inventories against molecular_system. Exclusions are constructed by
    get_excluded_volume_sites(), without atom access or physical-radius assignment.

    build() returns one Pharmacophore at the inventory's declared frame. A single
    explicit requested frame must match it. Multiple frames require separately
    obtained inventories/modelers. result is cleared before every build attempt.
    The new explicit hypothesis method is not equivalent to legacy heuristics.
    """

    @signal(tags=["modeler", "structure", "init"])
    @arg_digest(type_check=True)
    def __init__(
        self,
        molecular_system,
        skip_digestion=False,
        *,
        feature_inventory=None,
        projection_specs=None,
        excluded_volume_inventory=None,
        excluded_volume_radius=None,
        radius="0.15 nm",
        name=None,
    ):
        if feature_inventory is None:
            raise ArgumentError(
                argument="feature_inventory",
                reason="provide a cached native receptor inventory",
            )
        digest_feature_inventory(feature_inventory)
        digest_projection_specs(projection_specs)
        self.system = molecular_system
        self.feature_inventory = feature_inventory
        self.projection_specs = projection_specs
        self.excluded_volume_inventory = excluded_volume_inventory
        self.excluded_volume_radius = excluded_volume_radius
        self.native_options = dict(radius=radius, name=name)
        self.result = None

    @signal(tags=["modeler", "structure", "build"])
    @attributed()
    def build(self, structure_indices=None):
        """Build one hypothesis from the declared cached frame, without inference."""
        self.result = None
        if self.feature_inventory is None:
            raise ArgumentError(
                argument="feature_inventory",
                reason="provide a cached native receptor inventory",
            )
        digest_feature_inventory(self.feature_inventory)
        frame = digest_structure_index(self.feature_inventory["structure_index"])
        if structure_indices is None:
            indices = [frame]
        elif isinstance(structure_indices, Integral):
            indices = [digest_structure_index(structure_indices)]
        else:
            indices = digest_structure_indices(structure_indices)
        if isinstance(indices, str) or len(indices) != 1 or indices[0] != frame:
            raise ArgumentError(
                argument="structure_indices",
                reason="request the single cached inventory frame",
            )
        excluded = _receptor_exclusions(
            self.feature_inventory,
            self.excluded_volume_inventory,
            self.excluded_volume_radius,
        )
        model = from_receptor_projections(
            self.feature_inventory,
            projection_specs=self.projection_specs,
            **self.native_options,
        )
        model.molecular_system = self.system
        if excluded is not None:
            _attach_receptor_exclusions(model, excluded)
        self.result = model
        return model
