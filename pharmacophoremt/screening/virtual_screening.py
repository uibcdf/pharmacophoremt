"""Hit-list facade over explicitly selected prepared-native screening tools."""

from copy import deepcopy

from argdigest import arg_digest
from smonitor import signal

from pharmacophoremt._private.arg_digestion.argument._contracts import (
    digest_screening_method,
)
from pharmacophoremt._private.smonitor.exceptions import ArgumentError
from pharmacophoremt.screening.conformer_screening import ConformerScreening
from pharmacophoremt.screening.pose_evaluation import PoseEvaluator
from pharmacophoremt.screening.rigid_search import RigidPoseSearch


class VirtualScreening:
    """Screen prepared inputs with an explicitly chosen native method.

    ``screening_method='placed'`` evaluates a declared existing pose; ``'rigid'``
    searches one prepared frame; ``'conformers'`` searches requested prepared
    frames. Native essential-site, one-to-one assignment, angular and search
    budget contracts apply. Coverage is not affinity. Molecular preparation,
    local SMARTS recognition and the historical fit engine are retired.

    Historical min_match_ratio=1.0 and n_conformers=50 defaults are inert;
    other values are refused. All essential sites must match. Set a native
    min_fit_value threshold to bound total weighted coverage. Lengths and angles
    require explicit units. Method-specific keyword options reach the selected
    public tool; evaluate/run options are supplied to run().

    run() returns ranked native hit records with their original ``mol`` reference
    and a source-frame ``conf_id`` alias; ``evaluations`` retains every native
    result including negatives and explicitly recorded failures. No ``rd_mol``
    is synthesized. Both caches clear before each entered run and publish only
    after a successful batch. Ties retain input order. DataFrame/CSV export scalar
    evidence; molecular SDF export requires a separate provider workflow.
    """

    @signal(tags=["screening", "init"])
    @arg_digest()
    def __init__(
        self,
        pharmacophore,
        min_match_ratio=1.0,
        n_conformers=50,
        point_tolerance="0.10 nm",
        direction_tolerance="30 degrees",
        *,
        screening_method=None,
        **native_options,
    ):
        tools = {
            "placed": PoseEvaluator,
            "rigid": RigidPoseSearch,
            "conformers": ConformerScreening,
        }
        screening_method = digest_screening_method(screening_method)
        for argument, value, default in (
            ("min_match_ratio", min_match_ratio, 1.0),
            ("n_conformers", n_conformers, 50),
        ):
            if type(value) not in (int, float) or value != default:
                raise ArgumentError(
                    argument=argument,
                    reason="only the inert historical default is supported; choose native hit criteria and prepare conformers separately through MolSysMT (#219)",
                )
        self.screening_method = screening_method
        self.evaluator = tools[screening_method](
            pharmacophore,
            point_tolerance=point_tolerance,
            direction_tolerance=direction_tolerance,
            **native_options,
        )
        self.matches = []
        self.evaluations = []

    @signal(tags=["screening", "run"])
    def run(
        self,
        molecular_database,
        skip_digestion=False,
        *,
        on_error="raise",
        **evaluation_options,
    ):
        """Return hits while preserving native per-input and per-frame evidence.

        Inputs are materialized once. Failures raise by default; on_error='record'
        keeps fit_value=None without turning a failed calculation into a negative.
        Source atom/frame/state options follow the explicitly selected native tool.
        """
        self.matches = []
        self.evaluations = []
        # Native tools digest evaluation options after the facade has cleared
        # its caches, including invalid-option attempts.
        systems = list(molecular_database)
        evaluations = self.evaluator.run(
            systems, on_error=on_error, **evaluation_options
        )
        matches = []
        for entry in evaluations:
            if entry["status"] == "matched":
                frame = entry.get("best_conformer_index", entry.get("structure_index"))
                matches.append(
                    dict(
                        deepcopy(entry),
                        mol=systems[entry["input_index"]],
                        conf_id=frame,
                    )
                )
        matches.sort(key=lambda entry: entry["fit_value"], reverse=True)
        self.evaluations = evaluations
        self.matches = matches
        return self.matches

    def to_dataframe(self):
        """Format ranked hit evidence without molecular conversion or H removal."""
        import pandas as pd

        columns = ["rank", "input_index", "fit_value", "conf_id", "status"]
        return pd.DataFrame(
            [
                dict(rank=rank, **{key: entry[key] for key in columns[1:]})
                for rank, entry in enumerate(self.matches, start=1)
            ],
            columns=columns,
        )

    def to_csv(self, file_name):
        """Write the same scalar evidence as to_dataframe()."""
        self.to_dataframe().to_csv(file_name, index=False)

    def to_sdf(self, file_name):
        """Refuse the retired implicit H-removing molecular export path."""
        raise ArgumentError(
            argument="file_name",
            reason="molecular SDF export belongs to MolSysMT; collection/property and atom correspondence requirements remain https://github.com/uibcdf/molsysmt/issues/215 and #223; use scalar CSV evidence meanwhile",
        )
