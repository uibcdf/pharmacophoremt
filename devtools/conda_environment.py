"""Invoke the fixed shared environment operations with this owner's root."""

from __future__ import annotations

import sys

from check_dependency_routes import ROOT, load_sdk


def main() -> int:
    tools = load_sdk("conda_environment_tools")
    sys.argv[1:1] = ["--root", str(ROOT)]
    return tools.main()


if __name__ == "__main__":
    raise SystemExit(main())
