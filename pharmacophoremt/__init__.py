
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
