"""Invoke the accepted shared preflight outside scientific package imports."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SDK_SHA = "8f00e6d9de943b6e4710ea62936e2ebea00fad24"


def load_sdk(module_name="dependency_routes"):
    """Check immutable SDK identity and the actual administrative import origin."""
    sdk = Path(
        os.environ.get("PHARMACOPHOREMT_SUITE_ROOT", ROOT / ".molsyssuite")
    ).resolve()
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=sdk, text=True
    ).strip()
    dirty = subprocess.check_output(
        ["git", "status", "--porcelain", "--", "devtools"], cwd=sdk, text=True
    ).strip()
    if head != SDK_SHA or dirty:
        raise ValueError("Use the accepted clean immutable dependency SDK")
    sys.path[:0] = [str(sdk), str(ROOT / ".molsyssuite-tools")]
    import importlib

    module = importlib.import_module("devtools.scripts." + module_name)

    if not Path(module.__file__).resolve().is_relative_to(sdk):
        raise ValueError("Another editable SDK namespace was selected")
    return module


def main() -> int:
    routes = load_sdk()
    sys.argv[1:1] = ["--root", str(ROOT)]
    return routes.main()


if __name__ == "__main__":
    raise SystemExit(main())
