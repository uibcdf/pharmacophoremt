"""Optional attribution: public provider capture, offline host provenance."""

import sys
from contextvars import ContextVar
from copy import deepcopy
from functools import wraps

from depdigest import dep_digest, is_installed

_ENABLED = ContextVar("pharmacophoremt_attribution_enabled", default=False)
_CURRENT = ContextVar("pharmacophoremt_attribution_calculation", default=None)


@dep_digest("ackredit")
def _load_backend():
    import ackredit

    return ackredit


def backend():
    """Load only on explicit attribution/report requests."""
    if not is_installed("ackredit"):
        return None
    try:
        return _load_backend()
    except ModuleNotFoundError as error:
        if error.name == "ackredit":
            return None
        raise


def _warn(operation, error):
    try:
        from ._private.smonitor.emitter import warn
        from ._private.smonitor.warnings import AckreditTrackingWarning

        warn(
            AckreditTrackingWarning(extra=dict(operation=operation, reason=str(error)))
        )
    except Exception:
        # Even a warning promoted to an error must not erase completed science.
        pass


class _Calculation:
    def __init__(self, target):
        from ._version import __version__

        self.target = target
        self.producer = dict(software="pharmacophoremt", version=__version__)
        self.provider = self.capture = self.scope = None
        self.status = "unavailable"
        self.host = {}
        self.errors = []

    def failed(self, operation, error):
        self.status = "failed"
        self.errors.append(
            dict(operation=operation, reason=f"{type(error).__name__}: {error}")
        )
        _warn(operation, error)

    def start(self):
        try:
            self.provider = backend()
            if self.provider is not None:
                # Public capture is required; incompatible installed providers
                # are explicit tracking failures, never a private-registry fallback.
                self.capture = self.provider.capture(self.target, context=self.producer)
                self.capture.__enter__()
                self.scope = self.provider.scope(self.target)
                self.scope.__enter__()
                self.status = "captured"
        except Exception as error:
            self.failed("start attribution", error)

    def credit(self, declaration, target):
        import json

        entry = dict(deepcopy(declaration), used_by=target)
        key = json.dumps(entry, sort_keys=True)
        if key in self.host:
            return  # Bounded credit per reached operation/branch, not per fit/frame.
        self.host[key] = entry
        if self.provider is None or self.status != "captured":
            return
        try:
            with self.provider.scope(target):
                self.provider.register_item(**deepcopy(entry["record"]))
                self.provider.track_item(
                    entry["record"]["id"],
                    used_by=target,
                    roles=entry["roles"],
                    context=entry["context"],
                )
        except Exception as error:
            self.failed("record attribution", error)

    def finish(self, exception_info):
        for context in (self.scope, self.capture):
            if context is not None:
                try:
                    context.__exit__(*exception_info)
                except Exception as error:
                    self.failed("finish attribution", error)

    def payload(self):
        references = None
        if self.status == "captured":
            try:
                references = self.capture.attribution.to_dict()
            except Exception as error:
                self.failed("export attribution", error)
        return dict(
            schema="pharmacophoremt.attribution@1",
            status=self.status,
            producer=deepcopy(self.producer),
            provider=None
            if self.provider is None
            else dict(
                software="ackredit",
                version=str(getattr(self.provider, "__version__", "unknown")),
            ),
            host_references=deepcopy(list(self.host.values())),
            references=references,
            errors=deepcopy(self.errors),
        )


def credit_software(library, target):
    calculation = _CURRENT.get()
    if calculation is not None:
        from ._private.references import software_declarations

        for declaration in software_declarations(library):
            calculation.credit(declaration, target)


def credit_criterion(name, target):
    calculation = _CURRENT.get()
    if calculation is not None:
        from ._private.references import criterion_declaration

        calculation.credit(criterion_declaration(name), target)


def attributed(*libraries, model_results=False):
    """Capture an outer calculation; composed children share bounded credit."""

    def decorate(function):
        target = function.__module__ + "." + function.__qualname__

        @wraps(function)
        def observed(*args, **kwargs):
            if not _ENABLED.get():
                return function(*args, **kwargs)
            parent = _CURRENT.get()
            calculation = parent or _Calculation(target)
            if parent is None:
                calculation.start()
            token = _CURRENT.set(calculation)
            try:
                # Scientific exceptions are outside all provider-error handlers.
                result = function(*args, **kwargs)
                for library in ("pharmacophoremt", *libraries):
                    credit_software(library, target)
            finally:
                _CURRENT.reset(token)
                if parent is None:
                    calculation.finish(sys.exc_info())
            if parent is None:
                payload = calculation.payload()
                payload["scientific_outcome"] = (
                    result.get("status", "completed")
                    if isinstance(result, dict)
                    else "completed"
                )
                if isinstance(result, dict):
                    result["attribution"] = payload
                    if model_results:
                        for model in result["models"]:
                            model.metadata["attribution"] = deepcopy(payload)
                elif hasattr(result, "metadata"):
                    result.metadata["attribution"] = payload
            return result

        return observed

    return decorate
