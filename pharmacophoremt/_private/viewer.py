"""Optional MolSysViewer construction guarded before importing the provider."""

from depdigest import dep_digest


@dep_digest("molsysviewer")
def new_view():
    from molsysviewer import MolSysView

    return MolSysView()
