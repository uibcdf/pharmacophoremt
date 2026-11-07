"""Compatibility entry point for the unshipped legacy screening ledger.

The single implementation is the shipped private stdlib core. Loading this file
directly deliberately bypasses the public facade and its support dependencies;
legacy format, class names and scalar command behavior remain unchanged.
"""

import importlib.util
from pathlib import Path


def _load_core():
    # Top-level spec discovery does not import the public package. Prefer an
    # actual installed core when private support is staged outside site-packages.
    package = importlib.util.find_spec("pharmacophoremt_results")
    locations = () if package is None else package.submodule_search_locations or ()
    candidate = next(
        (
            Path(location) / "_store.py"
            for location in locations
            if (Path(location) / "_store.py").is_file()
        ),
        None,
    )
    if candidate is None:
        # Direct -I loading of this source file has no checkout on sys.path.
        candidate = (
            Path(__file__).resolve().parents[1]
            / "pharmacophoremt_results"
            / "_store.py"
        )
        if not candidate.is_file():
            raise ImportError("The PharmacophoreMT screening-run core is unavailable")
    spec = importlib.util.spec_from_file_location("_phmt_reference_run_core", candidate)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_core = _load_core()
ReferenceLedger = _core.ReferenceLedger
ReferenceRunView = _core.ReferenceRunView
canonical_json = _core.canonical_json
main = _core.main

if __name__ == "__main__":
    raise SystemExit(main())
