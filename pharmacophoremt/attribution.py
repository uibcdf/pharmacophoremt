"""Explicit optional attribution activation and provider-owned reporting."""

from contextlib import contextmanager

from argdigest import arg_digest
from smonitor import signal

from . import _ackredit
from ._private.smonitor.exceptions import ArgumentError, LibraryNotFoundError


@signal(tags=["attribution"])
@arg_digest()
@contextmanager
def attribution(enabled=True):
    """Activate bounded attribution without replacing the application session.

    Parameters
    ----------
    enabled : bool, default=True
        Enable tracking in this context; False temporarily suspends host tracking.

    Examples
    --------
    >>> with attribution():
    ...     result = evaluator.evaluate(prepared_ligand)
    """
    token = _ackredit._ENABLED.set(enabled)
    try:
        yield
    finally:
        _ackredit._ENABLED.reset(token)


@signal(tags=["attribution", "report"])
@arg_digest()
def attribution_report(attribution_data=None, format="markdown"):
    """Render a saved result or the current workflow using public Ackredit APIs.

    Parameters
    ----------
    attribution_data : dict, optional
        The host attribution payload from result['attribution'] or model metadata.
        Omit to report the current application-owned Ackredit session.
    format : str, default='markdown'
        An Ackredit report format, for example 'bibtex', 'csl-json' or 'markdown'.

    Examples
    --------
    >>> bibliography = attribution_report(result['attribution'], format='bibtex')
    """
    if attribution_data is not None and (
        not isinstance(attribution_data, dict)
        or attribution_data.get("schema") != "pharmacophoremt.attribution@1"
        or attribution_data.get("status") != "captured"
        or attribution_data.get("references") is None
    ):
        raise ArgumentError(
            argument="attribution_data",
            reason="expected a successfully captured host payload",
        )
    provider = _ackredit.backend()
    if provider is None:
        raise LibraryNotFoundError(library="ackredit", pypi="ackredit")
    saved = (
        provider.get_attribution()
        if attribution_data is None
        else provider.Attribution.from_dict(attribution_data["references"])
    )
    return saved.report(format=format)
