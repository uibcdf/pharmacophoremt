"""Generate only this owner's explicit environment profile, never recipes."""

from __future__ import annotations

import sys

from conda_environment import main

if __name__ == "__main__":
    sys.argv[1:1] = ["generate"]
    raise SystemExit(main())
