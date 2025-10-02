
"""
PharmacophoreMT
Short description
"""

# versioningit
from ._version import __version__

def __print_version__():
    print("PharmacophoreMT version " + __version__)

#__documentation_web__ = 'https://www.uibcdf.org/pharmacophoremt'
#__github_web__ = 'https://github.com/uibcdf/pharmacophoremt'
#__github_issues_web__ = __github_web__ + '/issues'

from . import config

from ._pyunitwizard import puw as pyunitwizard
