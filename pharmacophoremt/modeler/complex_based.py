"""Compatibility facade for prepared native complex observations."""

from numbers import Integral

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_ligand_selection,
    digest_structure_index,
    digest_structure_indices,
)
from pharmacophoremt._private.arg_digestion.argument.interaction_collection import (
    digest_interaction_collection,
)
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler.interaction_collection import from_interaction_collection
from pharmacophoremt.modeler.modeler import Modeler


class ComplexBasedModeler(Modeler):
    """Build complex hypotheses from explicit cached MolSysMT observations.

    The source must be the same unchanged prepared system used by every analysis
    in interaction_collection. ligand_selection is explicit; the observations
    define the partner boundary. No receptor selection, chemical preparation,
    interaction detection or legacy threshold/merging policy is inferred here.
    The native scientific definitions are not equivalent to the retired heuristics.

    build() returns one Pharmacophore for frame zero, an integer frame or a
    one-element frame sequence; multiple explicit frames return a list in caller
    order. Every frame must have been evaluated by every supplied analysis.
    Empty observed models remain empty. Failures raise without publishing partial
    results; result is cleared before each attempt and stores a successful return.
    Original native evidence, profile/state and optional attribution are retained
    by from_interaction_collection().
    """

    @signal(tags=["modeler", "complex", "init"])
    @arg_digest(type_check=True)
    def __init__(
        self,
        molecular_system,
        ligand_selection=None,
        receptor_selection=None,
        skip_digestion=False,
        *,
        interaction_collection=None,
        radius="0.15 nm",
        name=None,
        cation_mapping="exact",
        duplicate_policy="same_participant",
    ):
        if ligand_selection is None:
            raise ArgumentError(
                argument="ligand_selection",
                reason="provide an explicit ligand selection on the prepared source",
            )
        if receptor_selection is not None:
            raise ArgumentError(
                argument="receptor_selection",
                reason="native observations define the partner boundary; calculate the requested selection in MolSysMT before modeling",
            )
        self.ligand_selection = digest_ligand_selection(ligand_selection)
        self.interaction_collection = digest_interaction_collection(
            interaction_collection
        )
        self.system = molecular_system
        self.native_options = dict(
            radius=radius,
            name=name,
            cation_mapping=cation_mapping,
            duplicate_policy=duplicate_policy,
        )
        self.result = None

    @signal(tags=["modeler", "complex", "build"])
    def build(self, structure_indices=None):
        """Convert declared evaluated structures through the public native tool.

        Parameters
        ----------
        structure_indices : int or sequence of int, optional
            Default frame zero, or explicit unique nonnegative local indices.
            'all' is not accepted: select assessed structures explicitly.

        Returns
        -------
        Pharmacophore or list of Pharmacophore
            One model for a single requested structure, otherwise ordered models.
            Provider/coverage/conversion failures propagate without partial return.
        """
        self.result = None
        if structure_indices is None:
            indices = [0]
        elif isinstance(structure_indices, Integral):
            indices = [digest_structure_index(structure_indices)]
        else:
            indices = digest_structure_indices(structure_indices)
            if isinstance(indices, str):
                raise ArgumentError(
                    argument="structure_indices",
                    reason="select evaluated local structure indices explicitly",
                )
        models = [
            from_interaction_collection(
                self.system,
                self.interaction_collection,
                self.ligand_selection,
                structure_index=index,
                **self.native_options,
            )
            for index in indices
        ]
        self.result = models if len(models) > 1 else models[0]
        return self.result
