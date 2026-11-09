"""Shared private admission and diagnostics behind public field projections."""

from pharmacophoremt._private.smonitor.emitter import warn
from pharmacophoremt._private.smonitor.exceptions import (
    ArgumentError,
    ProjectionLossError,
)
from pharmacophoremt._private.smonitor.warnings import ProjectionLossWarning


def _options(return_report, on_loss):
    if type(return_report) is not bool:
        raise ArgumentError(argument="return_report", reason="expected a boolean")
    if not isinstance(on_loss, str) or on_loss not in {"warn", "raise", "ignore"}:
        raise ArgumentError(argument="on_loss", reason="choose warn, raise or ignore")


def _loss_policy(report, on_loss):
    fields = report["losses"]
    if not fields:
        return
    if on_loss == "raise":
        raise ProjectionLossError(operation=report["direction"], fields=list(fields))
    if on_loss == "warn":
        warn(ProjectionLossWarning(operation=report["direction"], fields=list(fields)))
