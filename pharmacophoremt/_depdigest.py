# DepDigest configuration for PharmacophoreMT
from pharmacophoremt._private.smonitor.exceptions import LibraryNotFoundError

LIBRARIES = {
    "numpy": {"type": "hard", "pypi": "numpy"},
    "scipy": {"type": "hard", "pypi": "scipy"},
    "molsysmt": {"type": "hard", "pypi": "molsysmt"},
    "pyunitwizard": {"type": "hard", "pypi": "pyunitwizard"},
    "argdigest": {"type": "hard", "pypi": "argdigest"},
    "smonitor": {"type": "hard", "pypi": "smonitor"},
    "depdigest": {"type": "hard", "pypi": "depdigest"},
    "rdkit": {"type": "hard", "pypi": "rdkit"},
    "networkx": {"type": "hard", "pypi": "networkx"},
    "nglview": {"type": "soft", "pypi": "nglview"},
    "molsysviewer": {"type": "soft", "pypi": "molsysviewer"},
    "ackredit": {"type": "soft", "pypi": "ackredit"},
}

MAPPING = {
    "nglview_NGLWidget": "nglview",
    "molsysviewer_MolSysView": "molsysviewer",
}

SHOW_ALL_CAPABILITIES = True
EXCEPTION_CLASS = LibraryNotFoundError
