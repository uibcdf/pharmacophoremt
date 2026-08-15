
"""
PharmacophoreMT
A state-of-the-art engine for molecular design.
"""

# SMonitor initialization (Must be first)
from smonitor.integrations import ensure_configured
from ._private.smonitor import PACKAGE_ROOT
ensure_configured(PACKAGE_ROOT)

# Versioningit
from ._version import __version__

def __print_version__():
    print("PharmacophoreMT version " + __version__)

# Infrastructure
from . import config
from ._pyunitwizard import puw as pyunitwizard
from . import interaction_site
from .pharmacophore import Pharmacophore
from .modeler.dispatcher import model
from . import io
from . import viewer
from . import validation


# The unit policy is declared when this package is imported, not on first use.
# Reaching it lazily meant `puw.configure.report()` described an empty session
# until something happened to touch it, and a user calling PyUnitWizard
# directly after importing this package got NoStandardsError. The cost is paid
# once per process -- a second suite library costs about 2 ms -- and it is a
# cost the session pays anyway at its first unit operation.
from . import _pyunitwizard  # noqa: E402,F401
