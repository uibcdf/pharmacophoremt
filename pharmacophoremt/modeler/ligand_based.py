"""Compatibility facade for explicitly selected native ligand consensus."""

from inspect import signature

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_conformer_rmsd_threshold,
    digest_consensus_method,
    digest_ligands,
    digest_min_actives,
    digest_molecular_systems,
    digest_n_conformers,
    digest_n_points,
)
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.modeler.modeler import Modeler


def _native_tool(method):
    from pharmacophoremt.modeler.aligned_cliques import from_aligned_ligand_cliques
    from pharmacophoremt.modeler.rigid_consensus import from_rigid_ligands

    return {
        "aligned_cliques": from_aligned_ligand_cliques,
        "rigid": from_rigid_ligands,
    }[digest_consensus_method(method)]


def _ligand_records(systems):
    if all(isinstance(item, dict) for item in systems):
        return digest_ligands([dict(item) for item in systems])
    if any(isinstance(item, dict) for item in systems):
        raise ArgumentError(
            argument="molecular_systems",
            reason="use either prepared systems or explicit ligand records throughout",
        )
    if len({id(item) for item in systems}) != len(systems):
        raise ArgumentError(
            argument="molecular_systems",
            reason="repeated raw objects do not establish distinct ligands; provide declared unique ligand records",
        )
    return digest_ligands(
        [
            dict(ligand_id=f"ligand-{index}", molecular_system=item)
            for index, item in enumerate(systems)
        ]
    )


class LigandBasedModeler(Modeler):
    """Build native consensus from prepared ligands with an explicit method.

    consensus_method='aligned_cliques' consumes a caller-declared common frame;
    'rigid' fits prepared frames through existing public MolSysMT operations.
    There is no implicit or legacy consensus method.

    The historical constructor names and list return remain. n_points now means
    minimum native consensus sites, not exact-size legacy subsets; min_actives
    means joint distinct-ligand support, defaulting to all inputs. Native keyword
    options are forwarded to the selected public tool, except min_sites/min_support,
    which use those historical constructor names.

    Inputs may be an iterable of prepared systems (positional ligand IDs, frame
    zero/reference state) or explicit unique ligand_id/molecular_system records
    with optional selection, structure_index and chemical_state. One frame per
    ligand is consumed; frames of one ligand are not independent supporters.
    Raw repeated objects are refused. Chemical identity across different objects
    or declared IDs remains the caller's responsibility.

    Historical n_conformers=50/conformer_rmsd_threshold=0.5 defaults are accepted
    for call compatibility but perform no preparation. Other values are refused;
    conformer generation must be a separate provider-supported operation.

    build() returns the native model list in hypothesis order, including [] for
    evaluated-empty consensus. No dummy model or legacy RMSD score is created.
    result/report retain the complete native result/report after successful
    building; both are cleared before a new attempt, including failed attempts.
    Native failure, search-limit, source and attribution contracts are preserved.
    """

    @signal(tags=["modeler", "ligand", "init"])
    @arg_digest(type_check=True)
    def __init__(
        self,
        molecular_systems,
        n_points=3,
        min_actives=None,
        n_conformers=50,
        conformer_rmsd_threshold=0.5,
        skip_digestion=False,
        *,
        consensus_method=None,
        **kwargs,
    ):
        self.consensus_method = digest_consensus_method(consensus_method)
        self.systems = list(digest_molecular_systems(molecular_systems))
        self.ligands = _ligand_records(self.systems)
        self.n_points = digest_n_points(n_points)
        support = digest_min_actives(min_actives)
        self.min_actives = len(self.ligands) if support is None else support
        for argument, value, default in (
            ("n_conformers", digest_n_conformers(n_conformers), 50),
            (
                "conformer_rmsd_threshold",
                digest_conformer_rmsd_threshold(conformer_rmsd_threshold),
                0.5,
            ),
        ):
            if value != default:
                raise ArgumentError(
                    argument=argument,
                    reason="only the historical default is accepted inertly; prepare conformers explicitly through the provider before consensus",
                )
        if self.min_actives > len(self.ligands):
            raise ArgumentError(
                argument="min_actives",
                reason="require attainable distinct-ligand support",
            )
        tool = _native_tool(self.consensus_method)
        supported = set(signature(tool).parameters) - {
            "ligands",
            "min_support",
            "min_sites",
            "skip_digestion",
        }
        if not kwargs.keys() <= supported:
            raise ArgumentError(
                argument="native_options",
                reason=f"unsupported options for {self.consensus_method}: {sorted(kwargs.keys() - supported)}; use n_points/min_actives for site/support minima",
            )
        self.native_options = dict(kwargs)
        self.result = self.report = None

    @signal(tags=["modeler", "ligand", "build"])
    def build(self):
        """Delegate once to the declared native tool and return its model list."""
        self.result = self.report = None
        result = _native_tool(self.consensus_method)(
            self.ligands,
            min_sites=self.n_points,
            min_support=self.min_actives,
            **self.native_options,
        )
        self.result = result
        self.report = result["report"]
        return result["models"]
