"""Saved screening evidence without importing molecular or citation providers.

This namespace is delivered in the PharmacophoreMT distribution. It requires the
normal ArgDigest/SMonitor support dependencies and uses no molecular calculation.
Original result/query bodies can contain geometry; callers own their disclosure.
"""

# Diagnostics bootstrap preserves an already configured application policy.
from smonitor.integrations import ensure_configured

from ._diagnostics import PACKAGE_ROOT

ensure_configured(PACKAGE_ROOT)

from ._api import (  # noqa: E402
    ScreeningRunStore as ScreeningRunStore,
)
from ._api import ScreeningRunView as ScreeningRunView  # noqa: E402
from ._api import canonical_json as canonical_json  # noqa: E402
from ._api import main as main  # noqa: E402
from ._diagnostics import ScreeningRunError as ScreeningRunError  # noqa: E402

__all__ = [
    "ScreeningRunError",
    "ScreeningRunStore",
    "ScreeningRunView",
    "canonical_json",
    "main",
]
